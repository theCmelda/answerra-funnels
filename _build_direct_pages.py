#!/usr/bin/env python3
"""
Generate 9 direct-to-calendar funnel pages (v4).

Changes from v3:
  * Press section now = AS COVERED BY logo wall (real SVG logos) + Polaroid Stack (10 articles, 2 tilted rows).
  * Old text logo bar, hero stat, article cards, stats grid, tech proof sections removed.
  * Software compatibility section retained (niche-specific value).
  * Vertical checkmark benefits list, no Daniel-takes-the-call, no $0-until, Australian Build, dynamic year.
"""

from pathlib import Path

LIBRARY = "660166"
CAL_URL = "https://app.iclosed.io/e/answrra/free-ai-receptionist-demo-build"

# ============================================================
#  FUNNEL CONTENT
# ============================================================
FUNNELS = {
    "dental-01-two-kinds": {
        "code": "DEN-01",
        "niche": "Dental",
        "audio_guid": "d983be50-d8c9-417d-9b91-428b432a298a",
        "title": "Recover $244K-$305K A Year Without Hiring Another Receptionist",
        "urgency": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dental Practices Missing 4+ Calls A Week",
        "h1_pre": "How AU Dental Practices Are Recovering",
        "h1_red": "$244K-$305K A Year",
        "h1_post": "Without Hiring Another Receptionist",
        "subhead": "4 missed calls a week. $1,348 in year-one production lost per call. 24/7 phone coverage built in 48 hours, in your own tone, on your real number.",
        "audio_label": "Watch Daniel Call His AI Receptionist Live",
        "audio_caption": "Sarah at Bright Smile Dental takes a real new-patient call. This is what 24/7 phone coverage sounds like in your own tone.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "On the call you'll hear what your own AI receptionist sounds like, built to your practice in your tone, on your real number. Test it on real booking calls before you commit to anything.",
        "benefits": [
            "4 to 7 new patient calls recovered every week",
            "24/7 phone coverage, including after reception closes at 6PM",
            "Built in 48 hours, in your own tone, on your real number",
            "Plugs into Praktika &amp; Dental4Windows out of the box",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Australian Build · 48-Hour Turnaround · No Deposit · Cancel Anytime",
    },
    "dental-02-freest-job": {
        "code": "DEN-02",
        "niche": "Dental",
        "audio_guid": "b742b098-cf3a-44b3-8909-e348a8873401",
        "title": "Replace The Receptionist Role Once And Save $88K A Year",
        "urgency": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dentists On Their 3rd Receptionist This Year",
        "h1_pre": "How AU Dentists Are Saving",
        "h1_red": "$88,000 A Year",
        "h1_post": "Without Hiring Or Training A Single Receptionist",
        "subhead": "$22K wasted per hire in ads, training, mistakes and lost bookings. Times four. Build the role once, in 48 hours, in your own tone.",
        "audio_label": "Watch Daniel Call His AI Receptionist Live",
        "audio_caption": "Sarah takes a real new-patient call. The role that doesn't quit, doesn't call in sick, doesn't go on Seek every 14 months.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "You'll walk away with a working AI receptionist tailored to your practice, voice and call types. Built to your real number, live in 48 hours, ready to test.",
        "benefits": [
            "One build replaces the hiring cycle forever",
            "No job ads, no training, no 14-month resignation reset",
            "24/7 coverage, zero sick days, zero attrition",
            "Built in 48 hours, in your own tone, on your real number",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Australian Build · Replaces 1 Hire · 48-Hour Turnaround · Cancel Anytime",
    },
    "dental-03-mrs-henderson": {
        "code": "DEN-03",
        "niche": "Dental",
        "audio_guid": "fb5613e0-e9f0-478d-95b3-057b37485606",
        "title": "Unlock The $1.4M In Lapsed Patients Sitting In Your Praktika",
        "urgency": "REACTIVATING 10 AU DENTAL LISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dental Practices Over 5 Years Old",
        "h1_pre": "How AU Dental Practices Unlock",
        "h1_red": "$1.4M In Lapsed Patients",
        "h1_post": "Without Their Receptionist Making A Single Call",
        "subhead": "1,400 dormant patients. $9,000 lifetime value each. 35 hours of calls a month, done by AI in your tone. Free first batch of 50.",
        "audio_label": "Watch A Lapsed Patient Get Rebooked, Live",
        "audio_caption": "Outbound reactivation call exactly as the patient heard it. The AI books her in under 90 seconds, in your tone, on your real number.",
        "calendar_header": "Book Your 15-Minute Reactivation Build",
        "calendar_sub": "We'll pull your Praktika export live on the call, sample 50 lapsed patients, and rebuild your reactivation script in your own tone. You see exactly how it works on your list.",
        "benefits": [
            "1,400 dormant patients called automatically, in your tone",
            "30 to 47 rebookings per 500 lapsed patients called",
            "35 hours of calls a month handled, none of it your front desk's job",
            "Plugs into Praktika &amp; Dental4Windows exports directly",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Australian Build · Works With Praktika · 48-Hour Turnaround · Cancel Anytime",
    },
    "dental-04-647pm": {
        "code": "DEN-04",
        "niche": "Dental",
        "audio_guid": "d983be50-d8c9-417d-9b91-428b432a298a",  # reuse DEN-01 audio
        "title": "24/7 Phone Coverage Without Taking Calls From Your Car Park",
        "urgency": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Dentists Still Taking Calls After 6PM",
        "h1_pre": "How AU Dental Practices Cover Every",
        "h1_red": "6PM-9AM Booking Call",
        "h1_post": "Without Touching Their Phone After Hours",
        "subhead": "Reception closes at six. The phone keeps ringing till nine. Every after-hours call costs you $1,348 or your evening. We answer both.",
        "audio_label": "Watch Daniel Call His AI Receptionist Live",
        "audio_caption": "Sarah takes a real new-patient call. The same agent that covers every 6PM-9AM ring while you're at the dinner table.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "You'll hear your own AI receptionist take a live after-hours call, built to your practice in your tone. Test it on a real evening booking before you commit.",
        "benefits": [
            "Every 6PM-9AM booking call answered in 2 rings",
            "24/7 coverage, including weekends and public holidays",
            "Books direct into Praktika, sends confirmation SMS",
            "Your evenings back. Your phone silent after six.",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Praktika · Dental4Windows · Centaur · Core Practice",
        "trust_strip": "Answers 24/7 · Australian Build · 48-Hour Turnaround · Cancel Anytime",
    },
    "medspa-01-1500-lapsed": {
        "code": "MED-01",
        "niche": "Medspa",
        "audio_guid": "b5bcf9d5-a5e8-4e6c-957a-ece830e58e6f",
        "title": "Unlock $675K In Lapsed Clients Sitting In Your Mindbody",
        "urgency": "REACTIVATING 10 AU MEDSPA LISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Medspa Owners With 1,000+ Past Clients",
        "h1_pre": "How AU Medspas Are Reactivating",
        "h1_red": "$675K In Lapsed Clients",
        "h1_post": "Without Their Nurse Making A Single Call",
        "subhead": "1,500 dormant clients. $400-$900 per reactivation. AHPRA-compliant calls in your senior nurse's tone. Free first batch of 50.",
        "audio_label": "Watch A Lapsed Client Get Rebooked, Live",
        "audio_caption": "Outbound reactivation call, AHPRA-compliant. The same agent that rebooks 30+ dormant clients per 500 called.",
        "calendar_header": "Book Your 15-Minute Reactivation Build",
        "calendar_sub": "We'll pull your Mindbody export live on the call, sample 50 lapsed clients, and build your reactivation script in your senior nurse's tone, AHPRA-compliant.",
        "benefits": [
            "1,500 dormant Mindbody clients called in your nurse's tone",
            "30 to 47 rebookings per 500 lapsed clients called",
            "AHPRA cooling-off notice sent automatically on every booking",
            "Audit-ready call logs, fully compliant from day one",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Mindbody · Vagaro · Acuity · Fresha",
        "trust_strip": "AHPRA Cooling-Off Auto-Sent · Audit-Ready Logs · Australian Build · Cancel Anytime",
    },
    "medspa-02-two-kinds": {
        "code": "MED-02",
        "niche": "Medspa",
        "audio_guid": "643a901e-40e2-4530-93d4-140db84cc26c",
        "title": "Convert 3x More Meta Leads Without Touching Your Phone",
        "urgency": "BUILDING 10 AU MEDSPA RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For Clinic Owners Spending $2,000+ A Month On Meta Lead Ads",
        "h1_pre": "How AU Medspas Book",
        "h1_red": "3x More Meta Leads",
        "h1_post": "Without Picking Up The Phone Themselves",
        "subhead": "Leads called inside 5 minutes book 21x more consults. Our AI answers in 30 seconds, AHPRA-compliant, in your clinic's voice.",
        "audio_label": "Watch A Meta Lead Booked In 30 Seconds",
        "audio_caption": "Real inbound call from a Meta lead form submission. AHPRA-compliant, in your clinic's voice, booked direct to your calendar.",
        "calendar_header": "Book Your 15-Minute Speed-To-Lead Demo",
        "calendar_sub": "On the call you'll hear a real Meta lead get called back in 30 seconds, AHPRA-compliant, in your clinic's voice. Tested on your real lead funnel.",
        "benefits": [
            "Every Meta lead called in under 30 seconds",
            "3 to 4x more booked consults from the same ad spend",
            "AHPRA cooling-off notice sent automatically on every booking",
            "Books direct into Mindbody, Vagaro, Acuity or Fresha",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Mindbody · Vagaro · Acuity · Fresha",
        "trust_strip": "AHPRA-Aware · Australian Voice · 48-Hour Turnaround · Cancel Anytime",
    },
    "medspa-03-sunday-instagram": {
        "code": "MED-03",
        "niche": "Medspa",
        "audio_guid": "b096c8a7-e0f3-42cd-bc80-4fe9fda86a60",
        "title": "Capture Every 10:47PM Sunday DM Without Touching Instagram",
        "urgency": "BUILDING 10 AU MEDSPA RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Clinic Owners Losing Leads Every Saturday And Sunday Night",
        "h1_pre": "How AU Medspas Capture Every",
        "h1_red": "After-Hours DM &amp; Phone Lead",
        "h1_post": "Without Working A Single Sunday Night",
        "subhead": "60-70% of medspa enquiries arrive after 7PM. Our AI replies in 11 seconds, AHPRA-compliant. 4-5 extra weekend bookings a week.",
        "audio_label": "Watch A Sunday-Night DM Booked, Live",
        "audio_caption": "Real after-hours inbound DM-to-booking. AHPRA cooling-off notice attached, in your clinic's voice.",
        "calendar_header": "Book Your 15-Minute After-Hours Demo",
        "calendar_sub": "You'll hear your own AI handle a Sunday-night DM live, built to your clinic in your tone, AHPRA cooling-off notice attached. Tested on a real enquiry.",
        "benefits": [
            "Every after-hours DM answered in 11 seconds",
            "4 to 5 extra weekend bookings every week",
            "AHPRA cooling-off notice sent automatically on every booking",
            "Audit-ready logs for every after-hours interaction",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Instagram · Mindbody · Vagaro · Acuity · Fresha",
        "trust_strip": "AHPRA Cooling-Off Auto-Sent · 7 Days A Week · Australian Build · Cancel Anytime",
    },
    "plumbing-01-phone-cant-answer": {
        "code": "PLU-01",
        "niche": "Plumbing",
        "audio_guid": "f2d9461c-5e88-4d3b-88bf-c0265ed7449f",
        "title": "Book Every Missed Call Without Ever Leaving The Tools",
        "urgency": "BUILDING 10 AU PLUMBING RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Plumbers Doing $400K-$1.2M And Stuck There",
        "h1_pre": "How AU Plumbers Book",
        "h1_red": "$1,500-$1,800 More A Week",
        "h1_post": "While Still On The Tools",
        "subhead": "Average plumbing job: $396 with parts. Average missed call: $0. Our AI answers in 2 rings, dispatches the job, texts your ute rego.",
        "audio_label": "Watch A Burst-Pipe Call Booked In 2 Rings",
        "audio_caption": "Sarah at Reliable Plumbing dispatches a real emergency. Same agent that books into Simpro automatically while you're under a sink.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "You'll hear your own AI receptionist dispatch a real emergency call, in your business name, on your real number. Built for Aussie plumbers, tested on the tools.",
        "benefits": [
            "Every missed call answered in 2 rings",
            "$1,500 to $1,800 a week in recovered jobs",
            "Books direct into Simpro, ServiceM8, AroFlo or Tradify",
            "Texts the customer your ute rego &amp; tech photo",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Simpro · ServiceM8 · AroFlo · Tradify",
        "trust_strip": "Australian Build · 48-Hour Turnaround · 90-Day Money Back · Cancel Anytime",
    },
    "plumbing-02-hipages-bleed": {
        "code": "PLU-02",
        "niche": "Plumbing",
        "audio_guid": "4fd05080-1d50-4413-a9c3-8bad2caa4993",
        "title": "Convert 3x More Hipages Leads From The Same Spend",
        "urgency": "BUILDING 10 AU PLUMBING RECEPTIONISTS THIS {MONTH} · 8 SLOTS LEFT",
        "pretitle": "For AU Plumbers On Hipages, Oneflare Or Service.com.au",
        "h1_pre": "How AU Plumbers Convert",
        "h1_red": "3x More Hipages Leads",
        "h1_post": "From The Same Spend, Without Picking Up The Phone",
        "subhead": "$200 a lead. 4-hour callback kills you. Our AI triggers off the Hipages notification and calls the lead back in 22 seconds.",
        "audio_label": "Watch A Hipages Lead Booked In 22 Seconds",
        "audio_caption": "Real inbound lead callback. The same agent that triples your booked jobs from the same Hipages spend.",
        "calendar_header": "Book Your 15-Minute Build Call",
        "calendar_sub": "We'll pull last month's Hipages report on the call and show you exactly how 22-second callback would convert. You hear your own AI answer a real Hipages lead.",
        "benefits": [
            "Every Hipages lead called back in 22 seconds",
            "3x more booked jobs from the same Hipages spend",
            "Triggers automatically off the Hipages notification",
            "Books direct into ServiceM8, Simpro &amp; Oneflare",
            "Cancel anytime. No deposits. No contracts.",
        ],
        "compat_list": "Hipages · Oneflare · Service.com.au · ServiceM8 · Simpro",
        "trust_strip": "Works With Hipages &amp; Oneflare · 48-Hour Turnaround · 90-Day Money Back · Cancel Anytime",
    },
}


# ============================================================
#  TEMPLATE
# ============================================================
TEMPLATE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{SUBHEAD_PLAIN}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Open+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;800;900&family=Source+Serif+Pro:wght@600;700;900&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:#f4f4f4;color:#0a0a0a;font-family:'Open Sans',Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.45;overflow-x:hidden}}
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
  @media (min-width:900px){{.hero{{padding:48px 32px 32px}}h1{{font-size:48px}}.subhead{{font-size:18px;margin-bottom:28px}}.pretitle{{font-size:13px;letter-spacing:.14em}}}}
  .cta-scroll{{display:inline-block;background:#0066CC;color:#fff;text-align:center;padding:14px 28px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;border:0;cursor:pointer;text-decoration:none;font-family:'Inter',sans-serif}}
  .cta-scroll:hover{{background:#0052a3}}

  /* ===== VIDEO DEMO CARD ===== */
  .video-block{{padding:22px 22px 28px;background:#fafafa;border-top:1px solid #e8e8e8;border-bottom:1px solid #e8e8e8}}
  .video-label{{font-family:'Oswald',sans-serif;font-size:18px;font-weight:700;text-transform:uppercase;letter-spacing:.02em;text-align:center;color:#0a0a0a;margin-bottom:6px;line-height:1.18}}
  .video-caption{{font-size:13px;color:#444;text-align:center;margin-bottom:14px;line-height:1.45;font-weight:500;max-width:520px;margin-left:auto;margin-right:auto}}
  .video-card{{max-width:380px;margin:0 auto;background:#000;border:3px solid #000;position:relative;aspect-ratio:4/5;overflow:hidden}}
  .video-card iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}}
  @media (min-width:900px){{.video-block{{padding:36px 32px 40px}}.video-label{{font-size:24px}}.video-card{{max-width:440px;border-width:4px}}}}

  /* ===== AS COVERED BY LOGO WALL (full-bleed, dark) ===== */
  .logo-wall{{background:#000;padding:60px 22px 50px;width:100vw;margin-left:calc(-50vw + 50%);text-align:center;position:relative}}
  .lw-h{{color:#fff;font-family:'Oswald',sans-serif;font-size:32px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;display:block;margin-bottom:34px;line-height:1.1}}
  @media (min-width:900px){{.lw-h{{font-size:46px;margin-bottom:42px}}}}
  .lw-card{{max-width:1100px;margin:0 auto;background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.08);border-radius:22px;padding:36px 28px}}
  @media (min-width:900px){{.lw-card{{padding:50px 60px}}}}
  .lw-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:30px 18px;align-items:center;justify-items:center}}
  @media (min-width:700px){{.lw-grid{{grid-template-columns:repeat(4,1fr);gap:32px 24px}}}}
  @media (min-width:900px){{.lw-grid{{grid-template-columns:repeat(6,1fr);gap:38px 28px}}}}
  .lw-item{{display:flex;align-items:center;justify-content:center;height:40px;width:100%}}
  .lw-item img{{height:26px;width:auto;max-width:120px;object-fit:contain;filter:brightness(0) invert(1) opacity(0.9)}}
  @media (min-width:900px){{.lw-item img{{height:30px;max-width:140px}}}}
  .lw-item .wm{{color:#fff;font-weight:800;line-height:1;white-space:nowrap}}
  .wm-openai{{font-family:'Inter',sans-serif;font-weight:700;letter-spacing:-.02em;font-size:18px}}
  .wm-mckinsey{{font-family:'Source Serif Pro','Playfair Display',serif;font-weight:900;letter-spacing:-.01em;font-size:18px}}
  .wm-smartcompany{{font-family:'Inter',sans-serif;font-weight:800;letter-spacing:-.01em;font-size:16px}}
  .wm-afr{{font-family:'Playfair Display',serif;font-weight:900;font-style:italic;letter-spacing:-.01em;font-size:17px}}

  /* ===== POLAROID STACK PRESS SECTION ===== */
  .polaroid-stack{{background:#000;padding:30px 22px 80px;width:100vw;margin-left:calc(-50vw + 50%);text-align:center}}
  .ps-h{{color:#fff;font-family:'Oswald',sans-serif;font-size:28px;text-transform:uppercase;text-align:center;margin-bottom:40px;letter-spacing:.04em;line-height:1.1;font-weight:700}}
  @media (min-width:900px){{.ps-h{{font-size:40px;margin-bottom:56px}}}}
  .ps-row{{position:relative;max-width:1000px;margin:0 auto 40px;height:340px}}
  @media (max-width:700px){{.ps-row{{height:240px;max-width:380px;margin-bottom:30px}}}}
  .ps-card{{position:absolute;background:#fff;border-radius:10px;box-shadow:0 16px 40px rgba(0,0,0,0.55), 0 3px 10px rgba(0,0,0,0.3);overflow:hidden;border:7px solid #fff;border-bottom-width:38px}}
  .ps-card .pill{{position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:3;display:inline-flex;align-items:center;background:#fff;border-radius:999px;padding:5px 14px;box-shadow:0 4px 12px rgba(0,0,0,0.25);height:28px;white-space:nowrap}}
  .ps-card .pill img{{height:16px;max-width:80px;object-fit:contain}}
  .ps-card .pill .wm{{font-size:12px;color:#0a0a0a;line-height:1;letter-spacing:-.005em;font-weight:800}}
  .ps-card img.thumb{{width:100%;height:100%;display:block;object-fit:cover;border-radius:3px}}
  /* Row 1 (5 cards, varied tilts) */
  .ps-a1{{width:240px;height:255px;top:55px;left:4%;transform:rotate(-6deg);z-index:2}}
  .ps-a2{{width:250px;height:265px;top:25px;left:22%;transform:rotate(3deg);z-index:4}}
  .ps-a3{{width:240px;height:255px;top:55px;left:41%;transform:rotate(-3deg);z-index:3}}
  .ps-a4{{width:250px;height:265px;top:30px;right:21%;transform:rotate(4deg);z-index:5}}
  .ps-a5{{width:230px;height:245px;top:60px;right:4%;transform:rotate(-5deg);z-index:2}}
  /* Row 2 */
  .ps-b1{{width:250px;height:265px;top:50px;left:5%;transform:rotate(4deg);z-index:3}}
  .ps-b2{{width:240px;height:255px;top:30px;left:23%;transform:rotate(-3deg);z-index:5}}
  .ps-b3{{width:250px;height:265px;top:55px;left:42%;transform:rotate(2deg);z-index:4}}
  .ps-b4{{width:230px;height:245px;top:40px;right:23%;transform:rotate(-4deg);z-index:3}}
  .ps-b5{{width:250px;height:265px;top:50px;right:4%;transform:rotate(5deg);z-index:5}}
  @media (max-width:700px){{
    .ps-a1,.ps-a2,.ps-a3,.ps-a4,.ps-a5,.ps-b1,.ps-b2,.ps-b3,.ps-b4,.ps-b5{{width:140px;height:160px;border-width:5px;border-bottom-width:28px}}
    .ps-a1{{top:35px;left:0}}
    .ps-a2{{top:15px;left:60px}}
    .ps-a3{{top:50px;left:120px}}
    .ps-a4{{top:25px;right:60px}}
    .ps-a5{{top:50px;right:0}}
    .ps-b1{{top:30px;left:10px}}
    .ps-b2{{top:50px;left:70px}}
    .ps-b3{{top:25px;left:130px}}
    .ps-b4{{top:50px;right:70px}}
    .ps-b5{{top:30px;right:0}}
    .ps-card .pill{{padding:3px 9px;height:22px}}
    .ps-card .pill img{{height:13px;max-width:50px}}
    .ps-card .pill .wm{{font-size:10px}}
  }}

  /* ===== SOFTWARE COMPAT (kept) ===== */
  .software-compat{{padding:30px 22px;background:#fafafa;border-bottom:1px solid #e8e8e8}}
  .sc-label{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#666;text-align:center;margin-bottom:14px}}
  .compat-niche{{background:#fff;border:1px solid #e8e8e8;padding:16px 18px;text-align:center;max-width:760px;margin:0 auto;border-radius:8px}}
  .niche-label{{font-family:'Oswald',sans-serif;font-size:14px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#D90429;margin-bottom:6px}}
  .compat-row{{font-size:13px;font-weight:600;color:#222;line-height:1.5}}

  /* ===== CALENDAR ===== */
  .calendar{{padding:42px 22px 28px;background:#fff}}
  .calendar-h{{font-family:'Oswald',sans-serif;font-size:24px;font-weight:700;text-transform:uppercase;letter-spacing:.01em;text-align:center;margin-bottom:8px;line-height:1.1;color:#0a0a0a}}
  @media (min-width:900px){{.calendar-h{{font-size:32px}}}}
  .calendar-sub{{font-size:14px;color:#444;text-align:center;line-height:1.5;margin-bottom:20px;max-width:540px;margin-left:auto;margin-right:auto}}
  .iclosed-widget{{min-height:680px;width:100%;border:1px solid #e8e8e8}}
  @media (min-width:900px){{.iclosed-widget{{min-height:760px}}}}

  /* ===== BENEFITS (vertical checklist) ===== */
  .benefits{{padding:28px 22px;background:#fafafa;border-top:1px solid #e8e8e8}}
  .benefits-h{{font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;text-transform:uppercase;letter-spacing:.01em;text-align:center;margin-bottom:16px;line-height:1.1;color:#0a0a0a}}
  @media (min-width:900px){{.benefits-h{{font-size:26px}}}}
  .benefits-list{{max-width:560px;margin:0 auto;list-style:none;padding:0}}
  .benefits-list li{{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;background:#fff;border:1px solid #e8e8e8;margin-bottom:8px;font-size:14.5px;line-height:1.45;font-weight:500;color:#0a0a0a}}
  @media (min-width:900px){{.benefits-list li{{font-size:16px;padding:14px 18px}}}}
  .benefits-list .tick{{flex-shrink:0;width:22px;height:22px;border-radius:50%;background:#22a06b;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:13px;margin-top:1px}}
  .benefits-list .tick::before{{content:"\\2713"}}

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

<!-- Meta Pixel via /pixel.js -->
<script src="/pixel.js" async></script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=1511657447261837&ev=PageView&noscript=1" alt=""/></noscript>
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

  <!-- VIDEO DEMO -->
  <section class="video-block">
    <div class="video-label">{AUDIO_LABEL}</div>
    <p class="video-caption">{AUDIO_CAPTION}</p>
    <div class="video-card">
      <iframe src="https://iframe.mediadelivery.net/embed/{LIBRARY}/{AUDIO_GUID}?autoplay=false&preload=true&responsive=true"
              title="Answerra Demo Video - {CODE}"
              loading="lazy"
              allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture;"
              allowfullscreen="true"></iframe>
    </div>
  </section>
</div>

<!-- ============ AS COVERED BY LOGO WALL (full-bleed) ============ -->
<section class="logo-wall">
  <div class="lw-h">As Covered By</div>
  <div class="lw-card">
    <div class="lw-grid">
      <div class="lw-item"><img src="/logos/cnbc.svg" alt="CNBC"></div>
      <div class="lw-item"><span class="wm wm-openai">OpenAI</span></div>
      <div class="lw-item"><span class="wm wm-mckinsey">McKinsey</span></div>
      <div class="lw-item"><img src="/logos/cbs.svg" alt="CBS"></div>
      <div class="lw-item"><img src="/logos/forbes.svg" alt="Forbes"></div>
      <div class="lw-item"><img src="/logos/bloomberg.svg" alt="Bloomberg"></div>
      <div class="lw-item"><img src="/logos/cnn.svg" alt="CNN"></div>
      <div class="lw-item"><span class="wm wm-afr">Financial Review</span></div>
      <div class="lw-item"><span class="wm wm-smartcompany">SmartCompany</span></div>
      <div class="lw-item"><img src="/logos/techcrunch.svg" alt="TechCrunch"></div>
      <div class="lw-item"><img src="/logos/wsj.svg" alt="Wall Street Journal"></div>
      <div class="lw-item"><img src="/logos/ft.svg" alt="Financial Times"></div>
    </div>
  </div>
</section>

<!-- ============ POLAROID STACK PRESS (full-bleed) ============ -->
<section class="polaroid-stack">
  <div class="ps-h">As Covered By The Press</div>
  <div class="ps-row">
    <div class="ps-card ps-a1"><span class="pill"><img src="/logos/cnbc.svg" alt=""></span><img class="thumb" src="/moodboard/M01.jpg" alt=""></div>
    <div class="ps-card ps-a2"><span class="pill"><span class="wm wm-openai" style="font-size:11px">OpenAI</span></span><img class="thumb" src="/moodboard/M02.jpg" alt=""></div>
    <div class="ps-card ps-a3"><span class="pill"><span class="wm wm-mckinsey" style="font-size:11px">McKinsey</span></span><img class="thumb" src="/moodboard/M03.jpg" alt=""></div>
    <div class="ps-card ps-a4"><span class="pill"><img src="/logos/cbs.svg" alt=""></span><img class="thumb" src="/moodboard/M04.jpg" alt=""></div>
    <div class="ps-card ps-a5"><span class="pill"><img src="/logos/forbes.svg" alt=""></span><img class="thumb" src="/moodboard/M05.jpg" alt=""></div>
  </div>
  <div class="ps-row">
    <div class="ps-card ps-b1"><span class="pill"><span class="wm wm-afr" style="font-size:11px">Financial Review</span></span><img class="thumb" src="/moodboard/M06.jpg" alt=""></div>
    <div class="ps-card ps-b2"><span class="pill"><span class="wm wm-smartcompany" style="font-size:11px">SmartCompany</span></span><img class="thumb" src="/moodboard/M07.jpg" alt=""></div>
    <div class="ps-card ps-b3"><span class="pill"><img src="/logos/bloomberg.svg" alt=""></span><img class="thumb" src="/moodboard/M08.jpg" alt=""></div>
    <div class="ps-card ps-b4"><span class="pill"><img src="/logos/cnn.svg" alt=""></span><img class="thumb" src="/moodboard/M09.jpg" alt=""></div>
    <div class="ps-card ps-b5"><span class="pill"><img src="/logos/techcrunch.svg" alt=""></span><img class="thumb" src="/moodboard/M10.jpg" alt=""></div>
  </div>
</section>

<div class="shell">

  <!-- SOFTWARE COMPAT -->
  <section class="software-compat">
    <div class="sc-label">Plugs Into The Software You Already Use:</div>
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

  <!-- BENEFITS -->
  <section class="benefits">
    <h2 class="benefits-h">What You Get</h2>
    <ul class="benefits-list">
      {BENEFITS_HTML}
    </ul>
  </section>

  <!-- COHORT -->
  <section class="cohort">
    <div class="cohort-badge">Founding AU Cohort &middot; <span class="urg-month"></span> <span class="urg-year"></span></div>
    <div class="cohort-h">10 Free Builds This Month<br>8 Slots Left</div>
    <p class="cohort-body">You get the full build at <b>$0</b> in exchange for a 60-second testimonial when it's live. No deposit. No contracts. Live on your real number in 48 hours.</p>
  </section>

  <!-- TRUST STRIP -->
  <div class="trust-strip">{TRUST_STRIP}</div>

</div>

<script>
  (function() {{
    var now = new Date();
    var month = now.toLocaleString("en-AU", {{month: "long"}}).toUpperCase();
    var year = now.getFullYear();
    document.querySelectorAll(".urg-month").forEach(function(e){{ e.textContent = month; }});
    document.querySelectorAll(".urg-year").forEach(function(e){{ e.textContent = year; }});
  }})();
</script>
</body>
</html>
"""


def render(cfg):
    subhead_plain = cfg["subhead"].replace("&amp;", "&")
    benefits_html = "\n      ".join(
        f'<li><span class="tick" aria-hidden="true"></span><span>{b}</span></li>'
        for b in cfg["benefits"]
    )
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
        COMPAT_LIST=cfg["compat_list"],
        CALENDAR_HEADER=cfg["calendar_header"],
        CALENDAR_SUB=cfg["calendar_sub"],
        CAL_URL=CAL_URL,
        BENEFITS_HTML=benefits_html,
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
