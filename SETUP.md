# TrustRoute Technologies · Go-live setup

How the pieces fit:

```
Visitor ──> trustroutetechnologies.com  (GitHub Pages: the /site folder)
               │  contact form (POST)
               ▼
        Supabase Edge Function "contact"
               ├──> saves the enquiry  ──> Supabase table "enquiries"
               └──> sends the email    ──> Resend ──> your inbox
```

Do the steps in order. Anything in `<angle brackets>` is yours to fill in.
Never paste an API key into any file in this folder: keys go only into Supabase secrets (step 3).

---

## 1. Receiving email (do this first)

Resend only **sends** email. To **receive** mail at `najeeb@` and `hello@trustroutetechnologies.com`
you need a mailbox provider, for example GoDaddy Professional Email, Microsoft 365, Google Workspace
or Zoho Mail. Set it up for your domain and create:

- `najeeb@trustroutetechnologies.com`
- `hello@trustroutetechnologies.com` (an alias that forwards to you is enough)

## 2. Resend (sending the enquiry emails)

1. Create an account at <https://resend.com>.
2. **Domains → Add domain** → `trustroutetechnologies.com`.
   Resend shows a few DNS records (TXT / MX). Add each one in **GoDaddy → My Products → Domain → DNS**.
   These do not interfere with your mailbox records from step 1. Wait until Resend shows **Verified**.
3. **API Keys → Create API key**, permission **Sending access**, domain `trustroutetechnologies.com`.
   Copy it somewhere safe for step 3; Resend shows it only once.

## 3. Supabase (storing enquiries and running the form function)

1. Create an account at <https://supabase.com> and a **new project** (choose a region close to you,
   e.g. *Canada (Central)*). Note the **project reference**: the `abcd1234` part of
   `https://abcd1234.supabase.co` (Project Settings → General).
2. In a terminal in this folder (`D:\trustroutetechnologies`), run:

```bash
npx supabase login
```

```bash
npx supabase link --project-ref <your-project-ref>
```

```bash
npx supabase db push --remote
```

   `db push` creates the `enquiries` table (locked down with Row Level Security). `--remote` makes it
   target your online project; without it, newer CLI versions try a local Docker database instead.

3. Store the secrets. Replace each `<...>`; for `IP_HASH_SALT` type any long random phrase:

```bash
npx supabase secrets set --project-ref <your-project-ref> RESEND_API_KEY=<your-resend-key> CONTACT_TO=najeeb@trustroutetechnologies.com "CONTACT_FROM=TrustRoute Website <website@trustroutetechnologies.com>" ALLOWED_ORIGINS=https://trustroutetechnologies.com,https://www.trustroutetechnologies.com IP_HASH_SALT=<long-random-phrase>
```

   Optional: `SEND_ACKNOWLEDGEMENT=true` also emails the enquirer a short "we received your enquiry"
   note; `RATE_LIMIT_PER_HOUR=5` changes how many enquiries one connection may send per hour.
   To send to more than one inbox, separate addresses with commas in `CONTACT_TO`.

4. Deploy the function:

```bash
npx supabase functions deploy contact --project-ref <your-project-ref> --no-verify-jwt
```

5. Open `site/contact.html` and replace `YOUR-PROJECT-REF` in the form's `action` with your project
   reference, so it reads `https://<your-project-ref>.supabase.co/functions/v1/contact`.

**Reading enquiries:** Supabase dashboard → **Table Editor → enquiries**. Each row shows whether the
email was `sent` or `failed`, so nothing is lost even if an email bounces.

> **Free plan note:** Supabase pauses free projects after about a week without activity. If the form
> shows "could not reach our server", restore the project from the dashboard. Upgrading to the Pro plan
> removes pausing.

## 4. GitHub Pages (hosting the website)

1. Create a GitHub account and a **public** repository, e.g. `trustroute-website`.
2. Upload this folder to it (from `D:\trustroutetechnologies`):

```bash
git init -b main
```

```bash
git add .
```

```bash
git commit -m "TrustRoute website"
```

```bash
git remote add origin https://github.com/<your-username>/trustroute-website.git
```

```bash
git push -u origin main
```

3. In the repository: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
   The included workflow (`.github/workflows/pages.yml`) publishes the `site` folder on every push.
4. **Settings → Pages → Custom domain**: enter `trustroutetechnologies.com` and save.

## 5. GoDaddy DNS for the website

In **GoDaddy → Domain → DNS**, point the domain at GitHub Pages:

| Type  | Name | Value |
|-------|------|-------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | `<your-username>.github.io` |

Remove any old `A @` record GoDaddy added (often "Parked"). Leave your email (MX) and Resend records alone.
After DNS updates (minutes to a few hours), go back to **Settings → Pages** and tick **Enforce HTTPS**.

## 6. Test it

Open `https://trustroutetechnologies.com/contact.html`, send a test enquiry, and check that:

- the page says *"Thank you. Your enquiry has been received…"*,
- the email arrives in your inbox (reply goes straight to the enquirer),
- a new row appears in the `enquiries` table with `email_status = sent`.

The function's own tests run locally with Node, without any accounts or keys:

```bash
node --test supabase/functions/contact/handler.test.mjs
```

## What lives where

| Path | Purpose |
|------|---------|
| `site/` | The website (published to GitHub Pages) |
| `supabase/migrations/` | Database table for enquiries |
| `supabase/functions/contact/` | The contact-form function (`handler.js` holds the logic) |
| `.github/workflows/pages.yml` | Publishes `site/` to GitHub Pages |
| `brand/` | Logo files, brand guidelines, stationery (not published) |
| `mockups/` | Earlier design options (not published) |
