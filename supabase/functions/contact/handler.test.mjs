// Tests for the contact handler. Run with:  node --test supabase/functions/contact/
// Supabase (PostgREST) and Resend are simulated, so no network or secrets are needed.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHandler } from './handler.js';

const ORIGIN = 'https://trustroutetechnologies.com';
const baseEnv = {
  RESEND_API_KEY: 're_test',
  CONTACT_FROM: 'TrustRoute Website <website@trustroutetechnologies.com>',
  CONTACT_TO: 'najeeb@trustroutetechnologies.com',
  ALLOWED_ORIGINS: `${ORIGIN},https://www.trustroutetechnologies.com`,
  SUPABASE_URL: 'https://proj.supabase.co',
  SUPABASE_SERVICE_ROLE_KEY: 'service_key',
};

function setup({ env = {}, rateRows = [], insertOk = true, resendOk = true } = {}) {
  const calls = [];
  const fetch = async (url, init = {}) => {
    const method = init.method || 'GET';
    const body = init.body ? JSON.parse(init.body) : undefined;
    calls.push({ url, method, body, headers: init.headers });
    if (url.startsWith('https://api.resend.com')) {
      return resendOk
        ? new Response(JSON.stringify({ id: 'email_123' }), { status: 200 })
        : new Response(JSON.stringify({ message: 'domain not verified' }), { status: 403 });
    }
    if (url.includes('/rest/v1/enquiries?select=')) return new Response(JSON.stringify(rateRows), { status: 200 });
    if (method === 'POST') {
      return insertOk
        ? new Response(JSON.stringify([{ id: 'row-1' }]), { status: 201 })
        : new Response('db down', { status: 500 });
    }
    if (method === 'PATCH') return new Response(null, { status: 204 });
    throw new Error('unexpected ' + url);
  };
  const all = { ...baseEnv, ...env };
  const handle = createHandler({ env: (k) => all[k], fetch, log: { error() {} } });
  return { handle, calls };
}

function post(fields, { origin = ORIGIN, ip = '203.0.113.9' } = {}) {
  const fd = new FormData();
  for (const [k, v] of Object.entries(fields)) fd.append(k, v);
  const headers = { 'x-forwarded-for': ip };
  if (origin) headers.origin = origin;
  return new Request('https://proj.supabase.co/functions/v1/contact', { method: 'POST', body: fd, headers });
}

const valid = {
  name: 'Ada Lovelace', organisation: 'Example Bank', role: 'CIO', email: 'ada@example.com',
  phone: '+1 604 000 0000', country: 'Canada', interest: 'meridian', message: 'We would like a demo. <script>x</script>',
  consent: 'on', website: '',
};

test('answers CORS preflight', async () => {
  const { handle } = setup();
  const res = await handle(new Request('https://x/', { method: 'OPTIONS', headers: { origin: ORIGIN } }));
  assert.equal(res.status, 204);
  assert.equal(res.headers.get('access-control-allow-origin'), ORIGIN);
});

test('rejects other methods', async () => {
  const { handle } = setup();
  assert.equal((await handle(new Request('https://x/', { headers: { origin: ORIGIN } }))).status, 405);
});

test('rejects foreign or missing origin', async () => {
  const { handle, calls } = setup();
  assert.equal((await handle(post(valid, { origin: 'https://evil.example' }))).status, 403);
  assert.equal((await handle(post(valid, { origin: '' }))).status, 403);
  assert.equal(calls.length, 0);
});

test('reports missing configuration', async () => {
  const { handle } = setup({ env: { RESEND_API_KEY: '' } });
  assert.equal((await handle(post(valid))).status, 500);
});

test('honeypot submissions get a silent success and nothing is stored or sent', async () => {
  const { handle, calls } = setup();
  const res = await handle(post({ ...valid, website: 'http://spam' }));
  assert.equal(res.status, 200);
  assert.equal(calls.length, 0);
});

test('validates required fields', async () => {
  const { handle, calls } = setup();
  const res = await handle(post({ name: '', organisation: 'X', email: 'not-an-email', message: '', consent: '' }));
  assert.equal(res.status, 422);
  const body = await res.json();
  assert.deepEqual(body.fields.sort(), ['consent', 'email', 'message', 'name']);
  assert.equal(calls.length, 0);
});

test('stores, emails and records success', async () => {
  const { handle, calls } = setup();
  const res = await handle(post(valid));
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { ok: true });

  const insert = calls.find((c) => c.method === 'POST' && c.url.endsWith('/rest/v1/enquiries'));
  assert.equal(insert.body.interest, 'Meridian (customer intelligence)');
  assert.equal(insert.body.consent, true);
  assert.match(insert.body.ip_hash, /^[0-9a-f]{64}$/);
  assert.ok(!JSON.stringify(insert.body).includes('203.0.113.9'), 'raw IP must not be stored');
  assert.equal(insert.headers.Authorization, 'Bearer service_key');

  const email = calls.find((c) => c.url.startsWith('https://api.resend.com'));
  assert.deepEqual(email.body.to, ['najeeb@trustroutetechnologies.com']);
  assert.equal(email.body.reply_to, 'ada@example.com');
  assert.equal(email.body.subject, 'Website enquiry: Meridian (customer intelligence) · Ada Lovelace, Example Bank');
  assert.ok(email.body.html.includes('&lt;script&gt;'), 'message must be HTML-escaped');
  assert.ok(!email.body.html.includes('<script>'));

  const patch = calls.find((c) => c.method === 'PATCH');
  assert.ok(patch.url.endsWith('enquiries?id=eq.row-1'));
  assert.deepEqual(patch.body, { email_status: 'sent', email_id: 'email_123' });
});

test('rate limit blocks after the hourly allowance', async () => {
  const { handle, calls } = setup({ rateRows: [1, 2, 3, 4, 5].map((id) => ({ id })) });
  assert.equal((await handle(post(valid))).status, 429);
  assert.ok(!calls.some((c) => c.method === 'POST'));
});

test('if email fails the enquiry is still saved and marked failed', async () => {
  const { handle, calls } = setup({ resendOk: false });
  assert.equal((await handle(post(valid))).status, 200);
  const patch = calls.find((c) => c.method === 'PATCH');
  assert.equal(patch.body.email_status, 'failed');
  assert.match(patch.body.email_error, /^403/);
});

test('if the database fails the email still goes out', async () => {
  const { handle, calls } = setup({ insertOk: false });
  assert.equal((await handle(post(valid))).status, 200);
  assert.ok(calls.some((c) => c.url.startsWith('https://api.resend.com')));
  assert.ok(!calls.some((c) => c.method === 'PATCH'));
});

test('if both fail the visitor is told to email directly', async () => {
  const { handle } = setup({ insertOk: false, resendOk: false });
  const res = await handle(post(valid));
  assert.equal(res.status, 502);
  assert.match((await res.json()).error, /email us directly/);
});

test('optional acknowledgement goes to the enquirer', async () => {
  const { handle, calls } = setup({ env: { SEND_ACKNOWLEDGEMENT: 'true' } });
  await handle(post(valid));
  const sends = calls.filter((c) => c.url.startsWith('https://api.resend.com'));
  assert.equal(sends.length, 2);
  assert.deepEqual(sends[1].body.to, ['ada@example.com']);
});

test('unknown interest falls back to "Something else"', async () => {
  const { handle, calls } = setup();
  await handle(post({ ...valid, interest: 'bogus' }));
  assert.equal(calls.find((c) => c.method === 'POST').body.interest, 'Something else');
});

test('accepts JSON bodies too', async () => {
  const { handle } = setup();
  const req = new Request('https://x/', {
    method: 'POST',
    headers: { origin: ORIGIN, 'content-type': 'application/json' },
    body: JSON.stringify({ ...valid, consent: true }),
  });
  assert.equal((await handle(req)).status, 200);
});
