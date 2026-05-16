#!/usr/bin/env python3
"""
Generate 9 direct-to-calendar funnel pages.

Structure (no VSL, outcome-led, press-authority instead of testimonials):
  Urgency bar
  Hero (pretitle + outcome H1 + math subhead + scroll CTA)
  60-sec audio sample (Bunny Stream iframe)
  Press authority collage (6 layers)
  Calendar (iClosed embed)
  Below-calendar outcomes + cohort badge
  Trust strip footer
"""

import os
from pathlib import Path

LIBRARY = "660166"
CAL_URL = "https://app.iclosed.io/e/answrra/free-ai-receptionist-demo-build"

# Per-funnel config: copy + audio GUID + niche.
FUNNELS = {
    "dental-01-two-kinds": {
        "code": "DEN-01",
        "niche": "Dental",
        "audience": "AU Dental Owners",
        "audio_guid": "9f39ef51-df5b-4dd0-8a44-38b41ea8e3fd",
        "title": "Recover $244K-$305K A Year Without Hiring Another Receptionist",
        "urgency": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dental Practices Missing 4+ Calls A Week",
        "h1_pre": "How AU Dental Practices Are Recovering",
        "h1_red": "$244K-$305K A Year",
        "h1_post": "Without Hiring Another Receptionist",
        "subhead": "4 missed calls a week. $1,348 in year-one production lost per call. 24/7 coverage, built in 48 hours, $0 until it books.",
        "audio_label": "Hear The Full Live Demo + How It Works",
        "audio_caption": "Sarah at Bright Smile Dental takes a real call. Then Daniel walks you through what just happened.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "Daniel takes the call himself. Bring your worst missed-call type. Leave with a working AI receptionist by Friday.",
        "outcome_1_num": "+4-7",
        "outcome_1_label": "New patient bookings recovered each week",
        "outcome_2_num": "48hr",
        "outcome_2_label": "Built and live on your real number",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until the first booking lands",
        "risk_reversal": "If it doesn't sound like your front desk on day one, walk. We eat the build cost.",
        "compat_label": "Plugs Into:",
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Built In Melbourne · $0 Until It Books · 48-Hour Build · Cancel Anytime",
    },
    "dental-02-freest-job": {
        "code": "DEN-02",
        "niche": "Dental",
        "audience": "AU Dentists On Their 3rd Receptionist This Year",
        "audio_guid": "cd65316a-b2ca-4bff-9af3-4480b1a25c73",
        "title": "Replace The Receptionist Role Once, Save $88K A Year",
        "urgency": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dentists On Their 3rd Receptionist This Year",
        "h1_pre": "How AU Dentists Are Saving",
        "h1_red": "$88,000 A Year",
        "h1_post": "Without Hiring Or Training A Single Receptionist",
        "subhead": "$22K wasted per hire in ads, training, mistakes and lost bookings. Build it once, in 48 hours, on your real number. Free.",
        "audio_label": "Hear The Full Live Demo + How It Works",
        "audio_caption": "Sarah takes a real new-patient call. Daniel walks you through what makes it work.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "Daniel takes the call. Bring your last bad receptionist call. Leave with a working AI by Friday.",
        "outcome_1_num": "$88K",
        "outcome_1_label": "Saved a year on hiring + training + churn",
        "outcome_2_num": "24/7",
        "outcome_2_label": "Coverage, no sick days, no resignations",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until the first booking lands",
        "risk_reversal": "If it doesn't outperform your last receptionist on day one, walk. We eat the build cost.",
        "compat_label": "Plugs Into:",
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Replaces 1 Hire · Saves $22K A Year · 48-Hour Build · Cancel Anytime",
    },
    "dental-03-mrs-henderson": {
        "code": "DEN-03",
        "niche": "Dental",
        "audience": "AU Dental Practices Over 5 Years Old",
        "audio_guid": "efae6361-4d33-47cf-a543-a5092e733497",
        "title": "Unlock The $1.4M In Lapsed Patients Sitting In Your Praktika",
        "urgency": "REACTIVATING 10 AU DENTAL LISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dental Practices Over 5 Years Old",
        "h1_pre": "How AU Dental Practices Unlock",
        "h1_red": "$1.4M In Lapsed Patients",
        "h1_post": "Without Their Receptionist Making A Single Call",
        "subhead": "1,400 dormant patients. $9,000 lifetime value each. 35 hours of calls a month, done by AI in your tone. Free first batch of 50.",
        "audio_label": "Hear A Real Lapsed Patient Get Rebooked",
        "audio_caption": "Outbound reactivation call exactly as the patient heard it. Daniel breaks down how it books her in under 90 seconds.",
        "calendar_header": "Book Your 15-Minute Reactivation Build",
        "calendar_sub": "Daniel mines your Praktika list live on the call. Bring the export. Leave with 50 patients getting called by Friday.",
        "outcome_1_num": "47",
        "outcome_1_label": "Patients rebooked in 14 days (Caulfield case)",
        "outcome_2_num": "$43,800",
        "outcome_2_label": "In new production from that one batch",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until a patient actually rebooks",
        "risk_reversal": "If we don't rebook at least 3 patients in the first batch, we walk and you keep the recordings.",
        "compat_label": "Plugs Into:",
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Works With Praktika · $0 Until A Patient Books · 48-Hour Build · Cancel Anytime",
    },
    "dental-04-647pm": {
        "code": "DEN-04",
        "niche": "Dental",
        "audience": "AU Dentists Still Taking Calls After 6PM",
        "audio_guid": "9f39ef51-df5b-4dd0-8a44-38b41ea8e3fd",  # reuse DEN-01 (same dental inbound agent)
        "title": "24/7 Phone Coverage Without Taking Calls From Your Car Park",
        "urgency": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dentists Still Taking Calls After 6PM",
        "h1_pre": "How AU Dental Practices Cover Every",
        "h1_red": "6PM-9AM Booking Call",
        "h1_post": "Without Touching Their Phone After Hours",
        "subhead": "Reception closes at six. The phone keeps ringing till nine. Every after-hours call costs you $1,348 or your evening. We answer both.",
        "audio_label": "Hear The Full Live Demo + How It Works",
        "audio_caption": "Sarah takes a real call. Daniel walks you through how it covers every 6pm-9am ring.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "Daniel takes the call. Bring your worst after-hours call type. Leave with 24/7 coverage by Friday.",
        "outcome_1_num": "24/7",
        "outcome_1_label": "Phone coverage including weekends",
        "outcome_2_num": "2 rings",
        "outcome_2_label": "Answer time, evenings and Saturdays",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until the first after-hours booking",
        "risk_reversal": "If it doesn't book a patient between 6pm and 10pm this week, you owe us nothing.",
        "compat_label": "Plugs Into:",
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Answers 24/7 · $0 Until It Books · 48-Hour Build · Cancel Anytime",
    },
    "medspa-01-1500-lapsed": {
        "code": "MED-01",
        "niche": "Medspa",
        "audience": "AU Medspa Owners With 1,000+ Past Clients In Mindbody",
        "audio_guid": "1ce58350-f8a4-473f-ab34-e2191e937d60",
        "title": "Unlock $675K In Lapsed Clients Sitting In Your Mindbody",
        "urgency": "REACTIVATING 10 AU MEDSPA LISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Medspa Owners With 1,000+ Past Clients",
        "h1_pre": "How AU Medspas Are Reactivating",
        "h1_red": "$675K In Lapsed Clients",
        "h1_post": "Without Their Nurse Making A Single Call",
        "subhead": "1,500 dormant clients. $400-$900 per reactivation. AHPRA-compliant calls in your nurse's tone. Free first batch of 50.",
        "audio_label": "Hear A Lapsed Medspa Client Get Rebooked",
        "audio_caption": "Outbound reactivation call, AHPRA-compliant. Daniel breaks down how it rebooks 30+ clients per 500 called.",
        "calendar_header": "Book Your 15-Minute Reactivation Build",
        "calendar_sub": "Daniel mines your Mindbody live on the call. Bring the export. Leave with 50 clients getting called by Friday.",
        "outcome_1_num": "30-47",
        "outcome_1_label": "Rebookings per 500 dormant clients called",
        "outcome_2_num": "$640",
        "outcome_2_label": "Average rebooking value (anti-wrinkle, filler)",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until a client actually rebooks",
        "risk_reversal": "First 50 calls free. Cooling-off notice on every booking. You see the rebookings before you pay a cent.",
        "compat_label": "Plugs Into:",
        "compat_list": "Mindbody · Vagaro · Acuity · Fresha",
        "trust_strip": "AHPRA Cooling-Off Auto-Sent · $0 Until A Client Books · 48-Hour Build · Audit-Ready Logs",
    },
    "medspa-02-two-kinds": {
        "code": "MED-02",
        "niche": "Medspa",
        "audience": "AU Clinic Owners Spending $2K+/Month On Meta Lead Ads",
        "audio_guid": "da46f471-ae3a-41b2-88eb-0f0c87fac221",
        "title": "Convert 3x More Meta Leads Without Touching Your Phone",
        "urgency": "BUILDING 10 AU MEDSPA RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For Clinic Owners Spending $2,000+ A Month On Meta Lead Ads",
        "h1_pre": "How AU Medspas Book",
        "h1_red": "3x More Meta Leads",
        "h1_post": "Without Picking Up The Phone Themselves",
        "subhead": "Leads called inside 5 minutes book 21x more consults. Our AI answers in 30 seconds, AHPRA-compliant, in your clinic's voice. Built in 48 hours. Free.",
        "audio_label": "Hear A Meta Lead Booked In 30 Seconds",
        "audio_caption": "Inbound call from a real Meta lead form submission. Daniel breaks down the 21x conversion math.",
        "calendar_header": "Book Your 15-Minute Speed-To-Lead Demo",
        "calendar_sub": "Daniel times your current callback live. Bring your last Meta lead. Leave with 30-second response by Friday.",
        "outcome_1_num": "30 sec",
        "outcome_1_label": "Callback time on every Meta lead",
        "outcome_2_num": "3-4x",
        "outcome_2_label": "More booked consults from the same ad spend",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until a lead actually books",
        "risk_reversal": "We dial your real Meta lead form on the demo and time the response. If 30 seconds doesn't beat your current setup, walk.",
        "compat_label": "Plugs Into:",
        "compat_list": "Mindbody · Vagaro · Acuity · Fresha",
        "trust_strip": "AHPRA-Aware · Australian Voice · $0 Until A Lead Books · 48-Hour Build",
    },
    "medspa-03-sunday-instagram": {
        "code": "MED-03",
        "niche": "Medspa",
        "audience": "AU Medspa Owners Losing Leads Every Saturday And Sunday Night",
        "audio_guid": "49a5eba1-6e4b-46e0-8f0a-cd31f962eacf",
        "title": "Capture Every 10:47PM Sunday DM Without Touching Instagram",
        "urgency": "BUILDING 10 AU MEDSPA RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Clinic Owners Losing Leads Every Saturday And Sunday Night",
        "h1_pre": "How AU Medspas Capture Every",
        "h1_red": "After-Hours DM &amp; Phone Lead",
        "h1_post": "Without Working A Single Sunday Night",
        "subhead": "60-70% of medspa enquiries arrive after 7PM. Our AI replies in 11 seconds, AHPRA-compliant. 4-5 extra weekend bookings a week.",
        "audio_label": "Hear A Sunday Night Booking Call",
        "audio_caption": "Real after-hours inbound DM-to-booking. Daniel breaks down the AHPRA cooling-off receipt.",
        "calendar_header": "Book Your 15-Minute After-Hours Demo",
        "calendar_sub": "Daniel pulls your last 30 days of DMs and counts the misses. Bring your Instagram. Leave with 24/7 coverage by Friday.",
        "outcome_1_num": "11 sec",
        "outcome_1_label": "DM reply time, 24/7",
        "outcome_2_num": "+4-5",
        "outcome_2_label": "Extra weekend bookings per week",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until a DM actually books",
        "risk_reversal": "On the demo we play the actual midnight DM that became a Friday consult, with the AHPRA cooling-off notice attached. You see the whole receipt.",
        "compat_label": "Plugs Into:",
        "compat_list": "Instagram · Mindbody · Vagaro · Acuity · Fresha",
        "trust_strip": "AHPRA Cooling-Off Auto-Sent · 7 Days A Week · $0 Until A DM Books · 48-Hour Build",
    },
    "plumbing-01-phone-cant-answer": {
        "code": "PLU-01",
        "niche": "Plumbing",
        "audience": "AU Plumbers Doing $400K-$1.2M And Stuck There",
        "audio_guid": "96d46ce7-4ddd-48fb-886a-42222ed3fcad",
        "title": "Book Every Missed Call Without Ever Leaving The Tools",
        "urgency": "BUILDING 10 AU PLUMBING RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Plumbers Doing $400K-$1.2M And Stuck There",
        "h1_pre": "How AU Plumbers Book",
        "h1_red": "$1,500-$1,800 More A Week",
        "h1_post": "While Still On The Tools",
        "subhead": "Average plumbing job: $396 with parts. Average missed call: $0. Our AI answers in 2 rings, dispatches the job, texts your ute rego.",
        "audio_label": "Hear A Burst-Pipe Call Booked In 2 Rings",
        "audio_caption": "Sarah at Reliable Plumbing dispatches a real emergency. Daniel breaks down the Simpro auto-booking.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "Daniel builds her live on the call. Bring 3 missed call types. Leave with your phone answered by Friday. Headphones in the ute work fine.",
        "outcome_1_num": "+$1,500",
        "outcome_1_label": "To $1,800/week in recovered jobs",
        "outcome_2_num": "2 rings",
        "outcome_2_label": "Answer time, even after-hours emergencies",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until a job actually books",
        "risk_reversal": "If she doesn't book at least 3 jobs in the first week, you owe us nothing. No deposit, no contract.",
        "compat_label": "Plugs Into:",
        "compat_list": "Simpro · ServiceM8 · AroFlo · Tradify",
        "trust_strip": "Works With Simpro &amp; ServiceM8 · $0 Until A Job Books · 48-Hour Build · 90-Day Money Back",
    },
    "plumbing-02-hipages-bleed": {
        "code": "PLU-02",
        "niche": "Plumbing",
        "audience": "AU Plumbers On Hipages, Oneflare Or Service.com.au",
        "audio_guid": "06be51b5-56fe-467d-9f07-30bd9f1c05ca",
        "title": "Convert 3x More Hipages Leads From The Same Spend",
        "urgency": "BUILDING 10 AU PLUMBING RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Plumbers On Hipages, Oneflare Or Service.com.au",
        "h1_pre": "How AU Plumbers Convert",
        "h1_red": "3x More Hipages Leads",
        "h1_post": "From The Same Spend, Without Picking Up The Phone",
        "subhead": "$200/lead. 4-hour callback kills you. Our AI fires off the Hipages notification and calls the lead back in 22 seconds. 3x more booked jobs.",
        "audio_label": "Hear A Hipages Lead Booked In 22 Seconds",
        "audio_caption": "Real inbound lead callback. Daniel breaks down how 22-second response triples booked jobs.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "Daniel pulls last month's Hipages report on the call. Bring it. Leave with 22-second callback by Friday. Headphones in the ute work fine.",
        "outcome_1_num": "22 sec",
        "outcome_1_label": "Hipages lead callback time",
        "outcome_2_num": "3x",
        "outcome_2_label": "More booked jobs from the same Hipages spend",
        "outcome_3_num": "$0",
        "outcome_3_label": "Until a job actually books",
        "risk_reversal": "We dial your real Hipages number on the demo and you hear her answer. If it doesn't beat your callback time, walk.",
        "compat_label": "Plugs Into:",
        "compat_list": "Hipages · Oneflare · Service.com.au · ServiceM8 · Simpro",
        "trust_strip": "Works With Hipages &amp; Oneflare · Pays For Itself In 3 Jobs · 48-Hour Build · 90-Day Money Back",
    },
}


TEMPLATE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{SUBHEAD_PLAIN}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Open+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:#f4f4f4;color:#0a0a0a;font-family:'Open Sans',Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.45}}
  .shell{{max-width:420px;margin:0 auto;background:#fff}}
  @media (min-width:900px){{.shell{{max-width:780px}}}}

  /* ===== URGENCY ===== */
  .urgency{{background:#FFE100;color:#000;text-align:center;font-family:'Inter',sans-serif;font-size:13px;font-weight:700;padding:10px 14px;letter-spacing:.04em;border-bottom:2px solid #000;line-height:1.3}}
  .urgency .pulse{{display:inline-block;width:8px;height:8px;background:#D90429;border-radius:50%;margin-right:8px;vertical-align:middle;animation:p 1.4s infinite}}
  @keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
  @media (min-width:900px){{.urgency{{font-size:15px;padding:13px 24px}}}}

  /* ===== HERO ===== */
  .hero{{padding:28px 22px 24px;text-align:center}}
  .pretitle{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#666;margin-bottom:14px}}
  h1{{font-family:'Oswald',Impact,sans-serif;color:#0a0a0a;font-size:30px;line-height:1.05;font-weight:700;margin-bottom:14px;letter-spacing:-.005em;text-transform:uppercase}}
  h1 .red{{color:#D90429}}
  .subhead{{font-size:15px;line-height:1.5;font-weight:500;color:#222;margin:0 auto 22px;max-width:520px}}
  @media (min-width:900px){{
    .hero{{padding:48px 32px 32px}}
    h1{{font-size:48px}}
    .subhead{{font-size:18px;margin-bottom:28px}}
    .pretitle{{font-size:13px;letter-spacing:.14em}}
  }}
  .cta-scroll{{display:inline-block;background:#0066CC;color:#fff;text-align:center;padding:14px 28px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;border:0;cursor:pointer;text-decoration:none;font-family:'Inter',sans-serif}}
  .cta-scroll:hover{{background:#0052a3}}

  /* ===== AUDIO SAMPLE CARD ===== */
  .audio-block{{padding:22px 22px 28px;background:#fafafa;border-top:1px solid #e8e8e8;border-bottom:1px solid #e8e8e8}}
  .audio-label{{font-family:'Oswald',sans-serif;font-size:16px;font-weight:700;text-transform:uppercase;letter-spacing:.02em;text-align:center;color:#0a0a0a;margin-bottom:6px;line-height:1.2}}
  .audio-caption{{font-size:12px;color:#666;text-align:center;margin-bottom:14px;line-height:1.4}}
  .audio-card{{max-width:420px;margin:0 auto;background:#000;border:3px solid #000;position:relative;overflow:hidden}}
  .audio-card iframe{{width:100%;height:200px;border:0;display:block}}
  @media (min-width:900px){{
    .audio-block{{padding:32px 32px 36px}}
    .audio-label{{font-size:20px}}
    .audio-card{{max-width:560px}}
    .audio-card iframe{{height:240px}}
  }}

  /* ===== PRESS COLLAGE ===== */
  section.press-section{{padding:24px 20px;border-bottom:1px solid #e8e8e8}}
  .bar-label{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#666;text-align:center;margin-bottom:14px}}
  .section-h{{font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;letter-spacing:.01em;text-transform:uppercase;text-align:center;margin-bottom:18px;line-height:1.05;color:#0a0a0a}}
  @media (min-width:900px){{.section-h{{font-size:28px}}}}

  .press-bar{{background:#fafafa}}
  .logo-row{{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:14px 22px}}
  .logo-pub{{font-family:'Inter',sans-serif;font-size:13px;font-weight:700;letter-spacing:.04em;color:#222;opacity:.78;padding:4px 0}}
  @media (min-width:900px){{.logo-pub{{font-size:16px}}}}

  .hero-stat{{background:#0a0a0a;color:#fff;text-align:center;padding:32px 22px}}
  .stat-big{{font-family:'Oswald',Impact,sans-serif;font-size:80px;line-height:.95;font-weight:700;color:#FFE100;letter-spacing:-.01em;margin-bottom:8px}}
  @media (min-width:900px){{.stat-big{{font-size:112px}}}}
  .stat-label{{font-family:'Oswald',sans-serif;font-size:17px;font-weight:600;letter-spacing:.01em;text-transform:uppercase;line-height:1.18;margin-bottom:10px}}
  @media (min-width:900px){{.stat-label{{font-size:20px}}}}
  .stat-sub{{font-size:13px;color:#bbb;line-height:1.5;max-width:380px;margin:0 auto}}

  .cards{{display:flex;flex-direction:column;gap:12px}}
  @media (min-width:900px){{.cards{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}}}
  .card{{display:block;background:#fff;border:1px solid #e0e0e0;padding:16px 16px 14px;text-decoration:none;color:#0a0a0a;transition:all .15s}}
  .card:hover{{border-color:#D90429;box-shadow:0 4px 14px rgba(0,0,0,.06)}}
  .card-pub{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#D90429;margin-bottom:6px}}
  .card-headline{{font-family:'Oswald',sans-serif;font-size:17px;font-weight:600;line-height:1.18;color:#0a0a0a;margin-bottom:8px}}
  .card-blurb{{font-size:12.5px;line-height:1.5;color:#444;margin-bottom:8px}}
  .card-link{{font-family:'Inter',sans-serif;font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#0066CC}}

  .stats-bg{{background:#fafafa}}
  .stats-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:#e8e8e8;border:1px solid #e8e8e8}}
  @media (min-width:900px){{.stats-grid{{grid-template-columns:1fr 1fr 1fr 1fr}}}}
  .stat-tile{{background:#fff;padding:16px 12px;text-align:center}}
  .stat-num{{font-family:'Oswald',Impact,sans-serif;font-size:30px;line-height:1;font-weight:700;color:#D90429;margin-bottom:6px}}
  @media (min-width:900px){{.stat-num{{font-size:38px}}}}
  .stat-line{{font-size:11.5px;font-weight:600;line-height:1.35;color:#0a0a0a;margin-bottom:4px}}
  .stat-src{{font-size:10px;font-weight:500;color:#888}}

  .tech-proof{{background:#0a0a0a;color:#fff}}
  .tech-proof .bar-label{{color:#FFE100}}
  .tech-proof .logo-pub{{color:#fff;opacity:1;font-size:15px;font-weight:700;letter-spacing:.05em}}

  .software-compat{{background:#fafafa}}
  .compat-niche{{background:#fff;border:1px solid #e8e8e8;padding:14px 16px;text-align:center}}
  .niche-label{{font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#D90429;margin-bottom:6px}}
  .compat-row{{font-size:13px;font-weight:600;color:#222;line-height:1.5}}

  /* ===== CALENDAR ===== */
  .calendar{{padding:32px 22px 24px;background:#fff}}
  .calendar-h{{font-family:'Oswald',sans-serif;font-size:24px;font-weight:700;text-transform:uppercase;letter-spacing:.01em;text-align:center;margin-bottom:8px;line-height:1.1;color:#0a0a0a}}
  @media (min-width:900px){{.calendar-h{{font-size:32px}}}}
  .calendar-sub{{font-size:14px;color:#444;text-align:center;line-height:1.5;margin-bottom:20px;max-width:540px;margin-left:auto;margin-right:auto}}
  .iclosed-widget{{min-height:680px;width:100%;border:1px solid #e8e8e8}}
  @media (min-width:900px){{.iclosed-widget{{min-height:760px}}}}

  /* ===== OUTCOMES UNDER CALENDAR ===== */
  .outcomes{{padding:28px 22px;background:#fafafa;border-top:1px solid #e8e8e8}}
  .outcomes-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:#e8e8e8;border:1px solid #e8e8e8;margin-bottom:18px}}
  .outcome-tile{{background:#fff;padding:18px 10px;text-align:center}}
  .outcome-num{{font-family:'Oswald',Impact,sans-serif;font-size:32px;line-height:1;font-weight:700;color:#0066CC;margin-bottom:6px}}
  @media (min-width:900px){{.outcome-num{{font-size:42px}}}}
  .outcome-label{{font-size:11.5px;font-weight:600;color:#0a0a0a;line-height:1.35}}
  .risk{{font-family:'Inter',sans-serif;font-size:13px;font-weight:500;color:#444;text-align:center;line-height:1.55;padding:14px 12px;background:#fff;border:1px solid #e8e8e8;max-width:600px;margin:0 auto}}
  .risk b{{color:#D90429;font-weight:700}}

  /* ===== COHORT ===== */
  .cohort{{background:#FFE100;color:#0a0a0a;text-align:center;padding:32px 22px}}
  .cohort-badge{{display:inline-block;background:#0a0a0a;color:#FFE100;font-family:'Inter',sans-serif;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:6px 14px;margin-bottom:14px}}
  .cohort-h{{font-family:'Oswald',sans-serif;font-size:24px;font-weight:700;letter-spacing:.01em;text-transform:uppercase;line-height:1.1;margin-bottom:12px}}
  @media (min-width:900px){{.cohort-h{{font-size:30px}}}}
  .cohort-body{{font-size:14px;line-height:1.55;font-weight:500;max-width:480px;margin:0 auto}}

  /* ===== TRUST STRIP ===== */
  .trust-strip{{background:#000;color:#fff;text-align:center;padding:14px 18px;font-family:'Inter',sans-serif;font-size:11.5px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;line-height:1.5}}
  @media (min-width:900px){{.trust-strip{{font-size:13.5px;padding:18px 24px}}}}

</style>
</head>
<body>

<div class="shell">

  <!-- URGENCY -->
  <div class="urgency"><span class="pulse"></span>{URGENCY}</div>

  <!-- HERO -->
  <section class="hero">
    <div class="pretitle">{PRETITLE}</div>
    <h1>{H1_PRE} <span class="red">{H1_RED}</span> {H1_POST}</h1>
    <p class="subhead">{SUBHEAD}</p>
    <a href="#book" class="cta-scroll">Book Your 15-Min Call &rarr;</a>
  </section>

  <!-- AUDIO SAMPLE -->
  <section class="audio-block">
    <div class="audio-label">{AUDIO_LABEL}</div>
    <p class="audio-caption">{AUDIO_CAPTION}</p>
    <div class="audio-card">
      <iframe src="https://iframe.mediadelivery.net/embed/{LIBRARY}/{AUDIO_GUID}?autoplay=false&preload=true&responsive=true"
              title="Answerra Audio Sample - {CODE}"
              loading="lazy"
              allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture;"
              allowfullscreen="true"></iframe>
    </div>
  </section>

  <!-- PRESS LOGO BAR -->
  <section class="press-section press-bar">
    <div class="bar-label">The AI Receptionist Shift, Covered By:</div>
    <div class="logo-row">
      <span class="logo-pub">OpenAI</span>
      <span class="logo-pub">McKinsey</span>
      <span class="logo-pub">CBS News</span>
      <span class="logo-pub">Fast Company</span>
      <span class="logo-pub">Salesforce</span>
      <span class="logo-pub">Bloomberg</span>
    </div>
  </section>

  <!-- HERO STAT -->
  <section class="press-section hero-stat">
    <div class="stat-big">700</div>
    <div class="stat-label">Customer Service Agents<br>Replaced By AI At Klarna</div>
    <div class="stat-sub">2.3 million conversations in month one. Resolution time cut from 11 minutes to under 2. $40M/year saved. Same voice AI infrastructure powers Answerra. (OpenAI Case Study, Klarna, 2024)</div>
  </section>

  <!-- ARTICLE CARDS -->
  <section class="press-section">
    <h2 class="section-h">What The Press Is Reporting</h2>
    <div class="cards">
      <a class="card" href="https://openai.com/index/klarna/" target="_blank" rel="noopener">
        <div class="card-pub">OpenAI Case Study &middot; 2024</div>
        <div class="card-headline">"Klarna's AI assistant does the work of 700 full-time agents."</div>
        <div class="card-blurb">2.3M conversations in month one. Two-thirds of all customer service chats. Resolution time cut from 11 min to under 2.</div>
        <div class="card-link">Read source &rarr;</div>
      </a>
      <a class="card" href="https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai" target="_blank" rel="noopener">
        <div class="card-pub">McKinsey &amp; Company &middot; 2025</div>
        <div class="card-headline">"80% of businesses will integrate voice AI into customer service by end of 2026."</div>
        <div class="card-blurb">78% of organisations already using AI in at least one business function. Voice AI growth concentrated in healthcare and SMB services.</div>
        <div class="card-link">Read source &rarr;</div>
      </a>
      <a class="card" href="https://www.cbsnews.com/news/klarna-ceo-ai-chatbot-replacing-workers-sebastian-siemiatkowski/" target="_blank" rel="noopener">
        <div class="card-pub">CBS News &middot; 2024</div>
        <div class="card-headline">"Klarna CEO: AI can do the job of 700 workers."</div>
        <div class="card-blurb">Sebastian Siemiatkowski on how Klarna's AI assistant handled two-thirds of all customer service chats in its first month.</div>
        <div class="card-link">Read source &rarr;</div>
      </a>
      <a class="card" href="https://smallbizai.au/chime-labs-sydney-ai-receptionist-tradies-australia/" target="_blank" rel="noopener">
        <div class="card-pub">SmallBizAI &middot; 2026</div>
        <div class="card-headline">"Sydney AI receptionist startup raises $900K to help Aussie tradies."</div>
        <div class="card-blurb">Australian tradies miss an estimated 270,000 calls a day. The AI receptionist category is moving fast in AU.</div>
        <div class="card-link">Read source &rarr;</div>
      </a>
    </div>
  </section>

  <!-- STATS GRID -->
  <section class="press-section stats-bg">
    <h2 class="section-h">The Math On Missed Calls</h2>
    <div class="stats-grid">
      <div class="stat-tile">
        <div class="stat-num">270K</div>
        <div class="stat-line">Calls missed by AU tradies every day</div>
        <div class="stat-src">SmallBizAI, 2026</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num">62%</div>
        <div class="stat-line">Of small business calls go unanswered</div>
        <div class="stat-src">Nextiva, 2024</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num">88%</div>
        <div class="stat-line">Of AU SMBs using AI report higher revenue</div>
        <div class="stat-src">Salesforce, 2025</div>
      </div>
      <div class="stat-tile">
        <div class="stat-num">$40M</div>
        <div class="stat-line">Klarna's annual saving from AI customer service</div>
        <div class="stat-src">Klarna PR, 2024</div>
      </div>
    </div>
  </section>

  <!-- TECH PROOF -->
  <section class="press-section tech-proof">
    <div class="bar-label">Built On The Same AI Infrastructure As Klarna:</div>
    <div class="logo-row">
      <span class="logo-pub">OpenAI</span>
      <span class="logo-pub">Retell AI</span>
      <span class="logo-pub">ElevenLabs</span>
      <span class="logo-pub">Twilio</span>
    </div>
  </section>

  <!-- SOFTWARE COMPAT (niche-specific) -->
  <section class="press-section software-compat">
    <div class="bar-label">{COMPAT_LABEL} The Software You Already Use:</div>
    <div class="compat-niche">
      <div class="niche-label">{NICHE}</div>
      <div class="compat-row">{COMPAT_LIST}</div>
    </div>
  </section>

  <!-- CALENDAR -->
  <section id="book" class="calendar">
    <h2 class="calendar-h">{CALENDAR_HEADER}</h2>
    <p class="calendar-sub">{CALENDAR_SUB}</p>
    <div class="iclosed-widget" data-url="{CAL_URL}"></div>
    <script async src="https://app.iclosed.io/assets/widget.js"></script>
  </section>

  <!-- OUTCOMES UNDER CALENDAR -->
  <section class="outcomes">
    <div class="outcomes-grid">
      <div class="outcome-tile">
        <div class="outcome-num">{OUT_1_NUM}</div>
        <div class="outcome-label">{OUT_1_LABEL}</div>
      </div>
      <div class="outcome-tile">
        <div class="outcome-num">{OUT_2_NUM}</div>
        <div class="outcome-label">{OUT_2_LABEL}</div>
      </div>
      <div class="outcome-tile">
        <div class="outcome-num">{OUT_3_NUM}</div>
        <div class="outcome-label">{OUT_3_LABEL}</div>
      </div>
    </div>
    <p class="risk"><b>Our promise:</b> {RISK_REVERSAL}</p>
  </section>

  <!-- COHORT -->
  <section class="cohort">
    <div class="cohort-badge">Founding AU Cohort &middot; <span class="urg-month"></span> 2026</div>
    <div class="cohort-h">10 Free Builds This Month<br>8 Slots Left</div>
    <p class="cohort-body">You get the full build at <b>$0</b> in exchange for a 60-second testimonial when it's live. No deposit. No contract. Live on your real number in 48 hours.</p>
  </section>

  <!-- TRUST STRIP -->
  <div class="trust-strip">{TRUST_STRIP}</div>

</div>

<script>
  document.querySelectorAll(".urg-month").forEach(function(e){{
    e.textContent = new Date().toLocaleString("en-AU", {{month: "long"}}).toUpperCase();
  }});
</script>
</body>
</html>
"""


def render(cfg):
    subhead_plain = cfg["subhead"].replace("&amp;", "&")
    return TEMPLATE.format(
        TITLE=cfg["title"],
        SUBHEAD_PLAIN=subhead_plain[:180],
        URGENCY=cfg["urgency"].replace("{MONTH}", '<span class="urg-month"></span>'),
        PRETITLE=cfg["pretitle"],
        H1_PRE=cfg["h1_pre"],
        H1_RED=cfg["h1_red"],
        H1_POST=cfg["h1_post"],
        SUBHEAD=cfg["subhead"],
        AUDIO_LABEL=cfg["audio_label"],
        AUDIO_CAPTION=cfg["audio_caption"],
        AUDIO_GUID=cfg["audio_guid"],
        LIBRARY=LIBRARY,
        CODE=cfg["code"],
        NICHE=cfg["niche"],
        COMPAT_LABEL=cfg["compat_label"],
        COMPAT_LIST=cfg["compat_list"],
        CALENDAR_HEADER=cfg["calendar_header"],
        CALENDAR_SUB=cfg["calendar_sub"],
        CAL_URL=CAL_URL,
        OUT_1_NUM=cfg["outcome_1_num"],
        OUT_1_LABEL=cfg["outcome_1_label"],
        OUT_2_NUM=cfg["outcome_2_num"],
        OUT_2_LABEL=cfg["outcome_2_label"],
        OUT_3_NUM=cfg["outcome_3_num"],
        OUT_3_LABEL=cfg["outcome_3_label"],
        RISK_REVERSAL=cfg["risk_reversal"],
        TRUST_STRIP=cfg["trust_strip"],
    )


def main():
    outdir = Path(__file__).parent
    written = []
    for slug, cfg in FUNNELS.items():
        html = render(cfg)
        outfile = outdir / f"funnel-{slug}-direct.html"
        outfile.write_text(html, encoding="utf-8")
        written.append((slug, outfile.stat().st_size))
    print(f"Wrote {len(written)} pages:")
    for slug, size in written:
        print(f"  funnel-{slug}-direct.html  ({size:,} bytes)")


if __name__ == "__main__":
    main()
