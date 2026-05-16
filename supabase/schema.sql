-- Answerra · Supabase schema
-- Run this in Supabase → SQL editor. Creates two tables: bookings (from iClosed)
-- + quiz_responses (form completions), plus indexes and RLS policies.

-- ============ BOOKINGS ============
create table if not exists public.bookings (
  id                uuid primary key default gen_random_uuid(),
  booking_id        text unique,                  -- iClosed event id
  first_name        text,
  last_name         text,
  email             text,
  phone             text,
  niche             text,                         -- dental | medspa | plumbing
  booked_at         timestamptz,                  -- scheduled call time
  source_url        text,                         -- referrer / funnel slug
  retell_call_id    text,                         -- Retell outbound call id
  capi_event_id     text,                         -- Meta event_id for dedup
  raw_payload       jsonb,                        -- full iClosed payload
  created_at        timestamptz default now()
);
create index if not exists bookings_email_idx     on public.bookings (email);
create index if not exists bookings_phone_idx     on public.bookings (phone);
create index if not exists bookings_booked_at_idx on public.bookings (booked_at);

-- ============ QUIZ RESPONSES ============
create table if not exists public.quiz_responses (
  id                  uuid primary key default gen_random_uuid(),
  booking_id          text references public.bookings(booking_id) on delete set null,
  first_name          text,
  email               text,
  phone               text,
  niche               text,
  business_name       text,
  business_address    text,
  business_phone      text,
  business_website    text,
  business_place_id   text,                       -- Google Places ID
  business_rating     numeric(3,2),
  business_reviews    integer,
  revenue             text,                       -- e.g. "$1M-$2.5M"
  benefits            text[],                     -- multi-select array
  notes               text,                       -- free text
  urgency             text,                       -- yesterday | today | 2weeks | 1month | exploring
  showup_commitment   text,                       -- confirmed | reschedule
  pixel_fired         boolean default false,      -- true only if revenue≥$1M AND urgency∈{today,yesterday}
  capi_event_id       text,                       -- Meta event_id (same as booking for dedup)
  user_agent          text,
  ip_address          text,
  created_at          timestamptz default now()
);
create index if not exists quiz_email_idx        on public.quiz_responses (email);
create index if not exists quiz_pixel_fired_idx  on public.quiz_responses (pixel_fired);
create index if not exists quiz_urgency_idx      on public.quiz_responses (urgency);
create index if not exists quiz_created_at_idx   on public.quiz_responses (created_at);

-- ============ RLS ============
-- Only the service role (server functions) can write. Anonymous reads disabled.
alter table public.bookings        enable row level security;
alter table public.quiz_responses  enable row level security;

create policy "service writes bookings"
  on public.bookings for insert
  to service_role with check (true);
create policy "service updates bookings"
  on public.bookings for update
  to service_role using (true);

create policy "service writes quiz"
  on public.quiz_responses for insert
  to service_role with check (true);
create policy "service updates quiz"
  on public.quiz_responses for update
  to service_role using (true);

-- Optional: a view that shows the qualifying lead funnel
create or replace view public.qualified_leads as
select
  q.created_at,
  q.first_name,
  q.business_name,
  q.revenue,
  q.urgency,
  q.benefits,
  q.notes,
  q.pixel_fired,
  q.showup_commitment,
  b.booked_at,
  b.phone,
  b.email,
  b.niche
from public.quiz_responses q
left join public.bookings b on b.booking_id = q.booking_id
order by q.created_at desc;
