// TrustRoute Technologies · contact form handler
//
// 1. Checks the request came from our website, isn't spam and isn't over the rate limit.
// 2. Validates the enquiry.
// 3. Saves it to the `enquiries` table in Supabase.
// 4. Emails it to our inbox through Resend (reply goes straight to the enquirer).
//
// No external libraries: Supabase (PostgREST) and Resend are called over HTTPS,
// so this file runs unchanged on Supabase Edge Functions and in local tests.

export const INTERESTS = {
  consultation: 'Advisory consultation',
  flexcube: 'Oracle FLEXCUBE advisory',
  demo: 'Solution demonstration',
  sms: 'SMS Banking',
  whatsapp: 'WhatsApp Banking',
  wallet: 'Wallet Banking',
  simulators: 'SwitchProof (FLEXCUBE testing & switch)',
  feip: 'FEIP (FLEXCUBE parameterization)',
  meridian: 'Meridian (customer intelligence)',
  other: 'Something else',
};

const LIMITS = { name: 120, organisation: 160, role: 120, email: 200, phone: 40, country: 80, message: 5000 };
const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[^\s@<>()[\]\\,;:"]{2,}$/;

const list = (v) => String(v || '').split(',').map((s) => s.trim()).filter(Boolean);
const oneLine = (v) => v.replace(/[\r\n\t]+/g, ' ').trim();
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

async function sha256(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function createHandler({ env, fetch: doFetch = fetch, log = console }) {
  const cfg = {
    resendKey: env('RESEND_API_KEY') || '',
    from: env('CONTACT_FROM') || '',
    to: list(env('CONTACT_TO')),
    origins: list(env('ALLOWED_ORIGINS')),
    ack: String(env('SEND_ACKNOWLEDGEMENT') || '').toLowerCase() === 'true',
    limit: Number(env('RATE_LIMIT_PER_HOUR') || 5),
    salt: env('IP_HASH_SALT') || 'trustroute',
    dbUrl: (env('SUPABASE_URL') || '').replace(/\/$/, ''),
    dbKey: env('SUPABASE_SERVICE_ROLE_KEY') || '',
  };

  const db = (path, init = {}) =>
    doFetch(`${cfg.dbUrl}/rest/v1/${path}`, {
      ...init,
      headers: {
        apikey: cfg.dbKey,
        Authorization: `Bearer ${cfg.dbKey}`,
        'Content-Type': 'application/json',
        ...(init.headers || {}),
      },
    });

  const sendEmail = (payload) =>
    doFetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${cfg.resendKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

  return async function handle(req) {
    const origin = req.headers.get('origin') || '';
    const allowed = cfg.origins.length === 0 || cfg.origins.includes(origin);
    const cors = {
      'Access-Control-Allow-Origin': allowed && origin ? origin : cfg.origins[0] || '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'content-type',
      Vary: 'Origin',
    };
    const reply = (status, body) =>
      new Response(JSON.stringify(body), {
        status,
        headers: { ...cors, 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
      });

    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (req.method !== 'POST') return reply(405, { ok: false, error: 'Method not allowed.' });
    if (!allowed || (cfg.origins.length > 0 && !origin)) return reply(403, { ok: false, error: 'Request not allowed.' });

    if (!cfg.resendKey || !cfg.from || cfg.to.length === 0 || !cfg.dbUrl || !cfg.dbKey) {
      log.error('contact: configuration is incomplete');
      return reply(500, { ok: false, error: 'The form is not configured yet. Please email us directly.' });
    }

    // Read the submission (form post or JSON).
    let raw = {};
    try {
      const type = req.headers.get('content-type') || '';
      if (type.includes('application/json')) {
        raw = await req.json();
      } else {
        const fd = await req.formData();
        for (const [k, v] of fd.entries()) if (typeof v === 'string') raw[k] = v;
      }
    } catch {
      return reply(400, { ok: false, error: 'Could not read the form.' });
    }

    const get = (k) => String(raw[k] ?? '').replace(/\0/g, '').trim().slice(0, LIMITS[k] ?? 200);

    // Honeypot: hidden from people, often filled in by bots. Pretend success.
    if (String(raw.website ?? '').trim() !== '') return reply(200, { ok: true });

    const data = {
      name: oneLine(get('name')),
      organisation: oneLine(get('organisation')),
      role: oneLine(get('role')),
      email: oneLine(get('email')),
      phone: oneLine(get('phone')),
      country: oneLine(get('country')),
      message: get('message'),
      consent: ['on', 'true', '1', 'yes'].includes(String(raw.consent ?? '').toLowerCase()),
      interestKey: INTERESTS[raw.interest] ? String(raw.interest) : 'other',
    };
    const interest = INTERESTS[data.interestKey];

    const missing = [];
    if (!data.name) missing.push('name');
    if (!data.organisation) missing.push('organisation');
    if (!data.message) missing.push('message');
    if (!data.consent) missing.push('consent');
    if (!EMAIL_RE.test(data.email)) missing.push('email');
    if (missing.length) return reply(422, { ok: false, error: 'Please complete the required fields.', fields: missing });

    // Rate limit per connection (hashed IP), counted from stored enquiries.
    const ip = (req.headers.get('x-forwarded-for') || '').split(',')[0].trim() || 'unknown';
    const ipHash = await sha256(`${cfg.salt}:${ip}`);
    try {
      const since = new Date(Date.now() - 3600_000).toISOString();
      const res = await db(`enquiries?select=id&ip_hash=eq.${ipHash}&created_at=gte.${encodeURIComponent(since)}&limit=${cfg.limit}`);
      if (res.ok) {
        const rows = await res.json();
        if (Array.isArray(rows) && rows.length >= cfg.limit) {
          return reply(429, { ok: false, error: 'Too many enquiries from this connection. Please try again later or email us directly.' });
        }
      }
    } catch (e) {
      log.error('contact: rate-limit check failed', e);
    }

    // 1. Store the enquiry.
    let id = null;
    try {
      const res = await db('enquiries', {
        method: 'POST',
        headers: { Prefer: 'return=representation' },
        body: JSON.stringify({
          name: data.name, organisation: data.organisation, role: data.role || null,
          email: data.email, phone: data.phone || null, country: data.country || null,
          interest, message: data.message, consent: data.consent, ip_hash: ipHash,
        }),
      });
      if (res.ok) id = (await res.json())?.[0]?.id ?? null;
      else log.error('contact: insert failed', res.status, await res.text());
    } catch (e) {
      log.error('contact: insert error', e);
    }

    // 2. Email it to the inbox.
    const rows = [
      ['Name', data.name], ['Institution', data.organisation], ['Role', data.role], ['Email', data.email],
      ['Phone', data.phone], ['Country', data.country], ['Interest', interest],
    ].filter(([, v]) => v);
    const html =
      '<div style="max-width:620px;font-family:Georgia,serif;color:#1A2133">' +
      '<p style="font:11px Arial,sans-serif;letter-spacing:3px;color:#A8833F;margin:0 0 6px">TRUSTROUTE TECHNOLOGIES · WEBSITE ENQUIRY</p>' +
      `<h1 style="font-weight:400;font-size:26px;color:#0E1F3F;margin:0 0 20px">${esc(interest)}</h1>` +
      '<table cellpadding="0" cellspacing="0" style="border-collapse:collapse;margin-bottom:24px">' +
      rows.map(([k, v]) =>
        `<tr><td style="padding:6px 16px 6px 0;color:#7C7768;font:12px Arial,sans-serif;letter-spacing:1px;text-transform:uppercase;vertical-align:top">${esc(k)}</td>` +
        `<td style="padding:6px 0;color:#1A2133;font:15px Arial,sans-serif">${esc(v)}</td></tr>`).join('') +
      '</table>' +
      `<div style="border-top:1px solid #E5DFD3;padding-top:18px;font:15px/1.6 Arial,sans-serif;white-space:pre-wrap">${esc(data.message)}</div>` +
      `<p style="font:12px Arial,sans-serif;color:#7C7768;margin-top:28px">Reply to this email to respond directly to ${esc(data.name)}.${id ? ` Reference: ${esc(id)}` : ''}</p></div>`;
    const text = `New website enquiry\n\n${rows.map(([k, v]) => `${k}: ${v}`).join('\n')}\n\nMessage:\n${data.message}\n`;

    let sent = false;
    let emailId = null;
    let emailError = null;
    try {
      const res = await sendEmail({
        from: cfg.from,
        to: cfg.to,
        reply_to: data.email,
        subject: `Website enquiry: ${interest} · ${data.name}, ${data.organisation}`,
        html,
        text,
      });
      const body = await res.text();
      if (res.ok) {
        sent = true;
        try { emailId = JSON.parse(body).id ?? null; } catch { /* ignore */ }
      } else {
        emailError = `${res.status} ${body.slice(0, 300)}`;
      }
    } catch (e) {
      emailError = String(e).slice(0, 300);
    }
    if (!sent) log.error('contact: email failed', emailError);

    // 3. Record the email outcome against the stored enquiry.
    if (id) {
      try {
        await db(`enquiries?id=eq.${id}`, {
          method: 'PATCH',
          body: JSON.stringify(sent ? { email_status: 'sent', email_id: emailId } : { email_status: 'failed', email_error: emailError }),
        });
      } catch (e) {
        log.error('contact: status update failed', e);
      }
    }

    // 4. Optional acknowledgement to the enquirer.
    if (sent && cfg.ack) {
      try {
        await sendEmail({
          from: cfg.from,
          to: [data.email],
          subject: 'We have received your enquiry · TrustRoute Technologies',
          html:
            '<div style="max-width:560px;font:15px/1.7 Arial,sans-serif;color:#1A2133">' +
            `<p>Dear ${esc(data.name)},</p><p>Thank you for contacting TrustRoute Technologies. We have received your enquiry about <strong>${esc(interest)}</strong> and will reply shortly.</p>` +
            '<p>Kind regards,<br>TrustRoute Technologies<br><span style="color:#7C7768">Trusted counsel for the future of banking</span></p></div>',
          text: `Dear ${data.name},\n\nThank you for contacting TrustRoute Technologies. We have received your enquiry about ${interest} and will reply shortly.\n\nKind regards,\nTrustRoute Technologies\n`,
        });
      } catch (e) {
        log.error('contact: acknowledgement failed', e);
      }
    }

    // Saved or emailed: either way the enquiry is not lost.
    if (id || sent) return reply(200, { ok: true });
    return reply(502, { ok: false, error: 'Your enquiry could not be sent just now. Please email us directly.' });
  };
}
