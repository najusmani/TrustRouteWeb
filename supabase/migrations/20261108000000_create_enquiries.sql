-- TrustRoute Technologies · website enquiries
-- Every contact-form submission is stored here by the `contact` Edge Function.

create table if not exists public.enquiries (
  id            uuid primary key default gen_random_uuid(),
  created_at    timestamptz not null default now(),
  name          text not null check (char_length(name) between 1 and 120),
  organisation  text not null check (char_length(organisation) between 1 and 160),
  role          text check (char_length(role) <= 120),
  email         text not null check (char_length(email) between 3 and 200),
  phone         text check (char_length(phone) <= 40),
  country       text check (char_length(country) <= 80),
  interest      text not null,
  message       text not null check (char_length(message) between 1 and 5000),
  consent       boolean not null default false,
  ip_hash       text,                       -- SHA-256 hash, never the raw IP
  email_status  text not null default 'pending' check (email_status in ('pending', 'sent', 'failed')),
  email_id      text,                       -- Resend message id
  email_error   text
);

comment on table public.enquiries is 'Contact-form enquiries from trustroutetechnologies.com';

create index if not exists enquiries_created_at_idx on public.enquiries (created_at desc);
create index if not exists enquiries_ip_hash_idx    on public.enquiries (ip_hash, created_at desc);

-- Lock the table down: Row Level Security on, and no policies.
-- The public (anon) key cannot read or write anything; only the Edge Function,
-- which uses the service-role key on the server, can insert and update rows.
alter table public.enquiries enable row level security;
revoke all on public.enquiries from anon, authenticated;
