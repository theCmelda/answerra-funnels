#!/usr/bin/env python3
"""
Generate 9 direct-to-calendar funnel pages (v6 — Daniel's locked simplified structure).

Final structure (9 sections only):
  1. Urgency bar (yellow, dynamic month)
  2. Hero (text + CTA, no video in hero)
  3. Calendar 1 (right after hero)
  4. News articles (polaroid stack, no pills)
  5. 3 Benefits (green-tick checklist)
  6. Integrates With (software badges, real logos)
  7. Hear It In Action (video block)
  8. Calendar 2 (repeat CTA)
  9. Urgency Closer

NO "As Covered By" logo wall (removed per Daniel's feedback).
Copy by Haynes-trained copywriter agent.
"""

from pathlib import Path

LIBRARY = "660166"
CAL_URL = "https://app.iclosed.io/e/answrra/free-ai-receptionist-demo-build"

# ============================================================
#  SOFTWARE LOGOS (real favicons in repo)
# ============================================================
SOFTWARE_LOGOS = {
    "praktika": ("/logos/sw-praktika.png", "Praktika"),
    "d4w": ("/logos/sw-d4w.png", "Dental4Windows"),
    "centaur": ("/logos/sw-d4w.png", "Centaur"),
    "corepractice": ("/logos/sw-core-practice.png", "Core Practice"),
    "mindbody": ("/logos/sw-mindbody.png", "Mindbody"),
    "vagaro": ("/logos/sw-vagaro.png", "Vagaro"),
    "acuity": ("/logos/sw-acuity.png", "Acuity"),
    "fresha": ("/logos/sw-fresha.png", "Fresha"),
    "simpro": ("/logos/sw-simpro.png", "Simpro"),
    "servicem8": ("/logos/sw-servicem8.png", "ServiceM8"),
    "aroflo": ("/logos/sw-aroflo.png", "AroFlo"),
    "tradify": ("/logos/sw-tradify.png", "Tradify"),
    "hipages": ("/logos/sw-hipages.png", "hipages"),
    "oneflare": ("/logos/sw-oneflare.png", "Oneflare"),
    "service-cs": ("/logos/sw-service-cs.png", "Service.com.au"),
}

NICHE_SOFTWARE = {
    "Dental": ["praktika", "d4w", "centaur", "corepractice"],
    "Medspa": ["mindbody", "vagaro", "acuity", "fresha"],
    "Plumbing": ["simpro", "servicem8", "aroflo", "tradify", "hipages", "oneflare"],
}


# ============================================================
#  FUNNEL CONTENT (Haynes-framework copy per funnel)
# ============================================================
FUNNELS = {
    "dental-01-two-kinds": {
        "code": "DEN-01",
        "niche": "Dental",
        "audio_guid": "d983be50-d8c9-417d-9b91-428b432a298a",
        "title": "Recover $244K-$305K A Year From Missed Dental Calls",
        "urgency_bar": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Australian Dental Practices Doing $1.2M-$2.8M A Year",
        "hero_headline": "How AU Dental Practices Are Recovering [$244K-$305K A Year] In Missed Calls Without Hiring Another Receptionist",
        "hero_subhead": "Your front desk misses 35-62% of inbound calls. At $1,348 in year-one production per booked patient, that is $244K-$305K walking to the practice down the road. We build the AI receptionist that catches every one. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. On the call we map your current missed-call leak and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Recovers $244K-$305K a year in production from missed calls",
            "Answers every call in under 2 rings, 24 hours a day",
            "Cancel anytime. No deposit. No contract.",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Bright Smile Dental answer an after-hours new-patient call and book the appointment in 90 seconds, so you can hear exactly what your patients will hear.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Grab one before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "dental-02-freest-job": {
        "code": "DEN-02",
        "niche": "Dental",
        "audio_guid": "b742b098-cf3a-44b3-8909-e348a8873401",
        "title": "Save $88K A Year Without Training Another Receptionist",
        "urgency_bar": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Practice Owners Tired Of Re-Training Front Desk Staff",
        "hero_headline": "How AU Dental Practices Are Saving [$88K A Year In Hiring Costs] Without Training Another Receptionist From Scratch",
        "hero_subhead": "The average AU practice burns through 4 front desk hires a year at $22K each in recruiting, training and lost production. Your AI receptionist gets trained once, never quits, never has a sick day, and books straight into Praktika. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will walk you through the turnover math on your specific practice and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Cuts $88K a year out of your hiring and training cycle",
            "Trained once on your practice, never forgets, never quits",
            "Live in your practice in 48 hours, not 8 weeks",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Bright Smile Dental handle a new-patient enquiry, quote pricing and book the chair, so you can hear the receptionist you will never have to train again.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Lock yours in before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "dental-03-mrs-henderson": {
        "code": "DEN-03",
        "niche": "Dental",
        "audio_guid": "fb5613e0-e9f0-478d-95b3-057b37485606",
        "title": "Unlock $1.4M In Lapsed Patients Without Lifting A Finger",
        "urgency_bar": "REACTIVATING 10 AU DENTAL LISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Practices Sitting On 1,000+ Lapsed Patients",
        "hero_headline": "How AU Dental Practices Are Unlocking [$1.4M In Lapsed Patient Value] Without Asking Their Receptionist To Make A Single Call",
        "hero_subhead": "The average AU practice has 1,400 dormant patients sitting in Praktika worth $9,000 each in lifetime value. Your receptionist does not have 80 hours to call them. Your AI does. Live in 48 hours, dialling your dormant list by day three.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will pull your dormant patient math live on the call and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Unlocks up to $1.4M from your 1,400 dormant patients",
            "Calls every lapsed patient in your database without front desk lifting a finger",
            "Cancel anytime. No deposit. No contract.",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Bright Smile Dental ring a 2-year-lapsed patient, handle the polite brush-off and rebook the chair, so you can hear what an outbound shift sounds like.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Grab yours before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "dental-04-647pm": {
        "code": "DEN-04",
        "niche": "Dental",
        "audio_guid": "d983be50-d8c9-417d-9b91-428b432a298a",
        "title": "Capture Every After-Hours Call Without Answering The Phone",
        "urgency_bar": "BUILDING 10 AU DENTAL RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Owners Still Taking 6:47pm Calls In The Car Park",
        "hero_headline": "How AU Dental Practices Are Capturing [$1,348 Per After-Hours Call] Without The Owner Ever Answering The Phone Again",
        "hero_subhead": "67% of new patient calls land outside 9-5. Every one your front desk misses is worth $1,348 in year-one production and $9K in lifetime value. Your AI receptionist covers 6pm to 9am, weekends and lunch, books straight into Praktika. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will calculate your after-hours leak on the call and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Captures $1,348 in production on every after-hours call",
            "Covers 6pm to 9am, weekends and lunch breaks automatically",
            "Books new patients straight into your chair while you sleep",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Bright Smile Dental handle a 7:14pm emergency enquiry and book the next-day appointment, so you can hear what your phone is missing at dinner.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Lock yours in before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "medspa-01-1500-lapsed": {
        "code": "MED-01",
        "niche": "Medspa",
        "audio_guid": "b5bcf9d5-a5e8-4e6c-957a-ece830e58e6f",
        "title": "Reactivate $675K In Lapsed Mindbody Clients",
        "urgency_bar": "REACTIVATING 10 AU MEDSPA LISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For AU Medspas And Cosmetic Injectables Clinics",
        "hero_headline": "How AU Medspas Are Reactivating [$675K In Lapsed Mindbody Clients] Without Their Nurse Making A Single Call",
        "hero_subhead": "The average AU medspa has 1,500 dormant clients in Mindbody worth $400 to $900 in reactivation value. Your nurses are in treatment rooms, not on phones. Your AI receptionist calls every one and books straight back into Mindbody. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will pull your dormant Mindbody list math live on the call and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Reactivates up to $675K from your dormant Mindbody clients",
            "Frees your nurses from the phone, keeps them in treatment rooms",
            "Cancel anytime. No deposit. No contract.",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Refined Skin and Injectables ring a 14-month-lapsed Botox client and rebook her for a refresh, so you can hear what reactivation actually sounds like.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Grab yours before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "medspa-02-two-kinds": {
        "code": "MED-02",
        "niche": "Medspa",
        "audio_guid": "643a901e-40e2-4530-93d4-140db84cc26c",
        "title": "Book 3x More Meta Leads Without Calling Anyone Back",
        "urgency_bar": "BUILDING 10 AU MEDSPA RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Clinics Burning Meta Spend On Slow Lead Follow-Up",
        "hero_headline": "How AU Medspas Are Booking [3x More Consults From The Same Meta Spend] Without Calling Leads Back Themselves",
        "hero_subhead": "Meta leads contacted in 5 minutes book 3-4x more than leads called back in 4-12 hours. Your front desk is in a treatment room. Your AI receptionist hits every lead inside 60 seconds and books straight into Mindbody. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will look at your current lead-to-book rate on the call and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Triples consult bookings from your existing Meta ad spend",
            "Calls every new lead inside 60 seconds, automatically",
            "Books straight into Mindbody without your team touching the phone",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Refined Skin and Injectables call a fresh Meta lead in under a minute and book a consult, so you can hear what fast follow-up actually closes.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Lock yours in before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "medspa-03-sunday-instagram": {
        "code": "MED-03",
        "niche": "Medspa",
        "audio_guid": "b096c8a7-e0f3-42cd-bc80-4fe9fda86a60",
        "title": "Add 4-5 Extra Weekend Bookings Without Working Sundays",
        "urgency_bar": "BUILDING 10 AU MEDSPA RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Clinics Losing Sunday-Night DM Enquiries To Monday",
        "hero_headline": "How AU Medspas Are Adding [4-5 Extra Weekend Bookings A Week] Without Working A Single Sunday Night",
        "hero_subhead": "Most Botox and skin enquiries hit at 8pm Sunday on Instagram. By Monday at 9am, half have booked somewhere else. Your AI receptionist answers DMs and books straight into Mindbody seven nights a week. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will count the weekend enquiries you are losing right now and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Adds 4-5 extra weekend bookings a week, every week",
            "Answers Sunday-night DMs and calls without you lifting a finger",
            "Books straight into Mindbody seven nights a week",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Refined Skin and Injectables handle a 9:47pm Sunday enquiry and book a Tuesday consult, so you can hear the booking you would have lost by Monday.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Grab yours before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "plumbing-01-phone-cant-answer": {
        "code": "PLU-01",
        "niche": "Plumbing",
        "audio_guid": "f2d9461c-5e88-4d3b-88bf-c0265ed7449f",
        "title": "Recover $1,500-$1,800 In Lost Jobs Every Week",
        "urgency_bar": "BUILDING 10 AU PLUMBING RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For AU Plumbers Still On The Tools And On The Phone",
        "hero_headline": "How AU Plumbers Are Recovering [$1,500-$1,800 In Lost Jobs Every Week] Without Dropping Their Tools To Answer The Phone",
        "hero_subhead": "Every missed call under a sink is a $300-$450 job booked by the bloke down the road. Your AI receptionist answers every call, qualifies the job and books it straight into Simpro or ServiceM8. Live in 48 hours. You stay on the tools.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will count how much you are losing under sinks this month and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Recovers $1,500 to $1,800 a week in jobs you would have missed",
            "Answers every call inside 2 rings while you stay on the tools",
            "Books straight into Simpro or ServiceM8 with full job details",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Reliable Plumbing handle a burst-pipe call, qualify the urgency and book it in ServiceM8, so you can hear what your phone is missing today.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Lock yours in before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
    },
    "plumbing-02-hipages-bleed": {
        "code": "PLU-02",
        "niche": "Plumbing",
        "audio_guid": "4fd05080-1d50-4413-a9c3-8bad2caa4993",
        "title": "Book 3x More Hipages Jobs From The Same Spend",
        "urgency_bar": "BUILDING 10 AU PLUMBING RECEPTIONISTS THIS [MONTH] · 8 SLOTS LEFT",
        "hero_pretitle": "For Plumbers Burning Money On Hipages And Oneflare Leads",
        "hero_headline": "How AU Plumbers Are Booking [3x More Hipages Jobs From The Same Lead Spend] Without Dropping Tools To Call Anyone Back",
        "hero_subhead": "Hipages leads called back in 22 seconds book 3x more than leads called back in 4 hours. You are under a vanity. Your AI receptionist hits every Hipages and Oneflare lead in seconds and books into Simpro. Live in 48 hours.",
        "hero_cta": "Book Your Custom Receptionist Demo Call",
        "calendar_section_h": "Book Your Custom Receptionist Demo Call",
        "calendar_section_sub": "Pick a time below. We will pull your current Hipages conversion rate on the call and show you the build.",
        "news_section_h": "What The Press Is Saying",
        "benefits": [
            "Triples booked jobs from your existing Hipages and Oneflare spend",
            "Calls every fresh lead in 22 seconds, automatically",
            "Books qualified jobs straight into Simpro while you stay on the tools",
        ],
        "integrates_label": "Books Straight Into:",
        "video_section_h": "Hear It In Action",
        "video_caption": "Watch Sarah at Reliable Plumbing call a fresh Hipages lead in under a minute, qualify the job and book it, so you can hear what 22-second follow-up actually wins.",
        "calendar2_section_h": "Ready To Build Yours? Pick A Time.",
        "calendar2_section_sub": "Two of the ten [MONTH] slots are gone. Grab yours before the cohort closes.",
        "urgency_closer": "8 of 10 [MONTH] slots left. Cancel anytime, no lock-in.",
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
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Open+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style data-v="v7-white-everywhere">
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:#f4f4f4;color:#0a0a0a;font-family:'Open Sans',Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.45;overflow-x:hidden}}
  .shell{{max-width:420px;margin:0 auto;background:#fff}}
  @media (min-width:900px){{.shell{{max-width:1100px}}}}

  /* ===== URGENCY BAR ===== */
  .urgency{{background:#FFE100;color:#000;text-align:center;font-family:'Inter',sans-serif;font-size:13px;font-weight:700;padding:11px 14px;letter-spacing:.04em;border-bottom:2px solid #000;line-height:1.3}}
  .urgency .pulse{{display:inline-block;width:8px;height:8px;background:#D90429;border-radius:50%;margin-right:8px;vertical-align:middle;animation:p 1.4s infinite}}
  @keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
  @media (min-width:900px){{.urgency{{font-size:15px;padding:14px 24px}}}}

  /* ===== HERO ===== */
  .hero{{padding:36px 22px 32px;text-align:center}}
  @media (min-width:900px){{.hero{{padding:64px 40px 48px;max-width:920px;margin:0 auto}}}}
  .pretitle{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#666;margin-bottom:16px}}
  @media (min-width:900px){{.pretitle{{font-size:13px;letter-spacing:.14em;margin-bottom:22px}}}}
  h1{{font-family:'Oswald',Impact,sans-serif;color:#0a0a0a;font-size:32px;line-height:1.06;font-weight:700;margin-bottom:18px;letter-spacing:-.005em;text-transform:uppercase}}
  @media (min-width:900px){{h1{{font-size:54px;line-height:1.04;margin-bottom:24px}}}}
  h1 .red{{color:#D90429}}
  .subhead{{font-size:15.5px;line-height:1.55;font-weight:500;color:#222;margin:0 auto 26px;max-width:600px}}
  @media (min-width:900px){{.subhead{{font-size:19px;line-height:1.55;margin-bottom:32px;max-width:780px}}}}
  .cta-scroll{{display:inline-block;background:#D90429;color:#fff;text-align:center;padding:16px 32px;font-size:15px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;border:0;cursor:pointer;text-decoration:none;font-family:'Inter',sans-serif;box-shadow:0 8px 24px rgba(217,4,41,.28);transition:transform .15s, box-shadow .15s}}
  .cta-scroll:hover{{background:#b80323;transform:translateY(-2px);box-shadow:0 10px 28px rgba(217,4,41,.4)}}
  @media (min-width:900px){{.cta-scroll{{font-size:17px;padding:18px 38px}}}}

  /* ===== CALENDAR BLOCK ===== */
  .calendar{{padding:40px 22px 28px;background:#fff;border-top:1px solid #e8e8e8}}
  @media (min-width:900px){{.calendar{{padding:60px 40px 40px;max-width:900px;margin:0 auto}}}}
  .calendar-h{{font-family:'Oswald',sans-serif;font-size:26px;font-weight:700;text-transform:uppercase;letter-spacing:.01em;text-align:center;margin-bottom:12px;line-height:1.1;color:#0a0a0a}}
  @media (min-width:900px){{.calendar-h{{font-size:38px}}}}
  .calendar-sub{{font-size:14.5px;color:#444;text-align:center;line-height:1.55;margin-bottom:26px;max-width:640px;margin-left:auto;margin-right:auto}}
  @media (min-width:900px){{.calendar-sub{{font-size:16.5px;margin-bottom:32px}}}}
  .iclosed-widget{{min-height:680px;width:100%;border:1px solid #e8e8e8;border-radius:6px}}
  @media (min-width:900px){{.iclosed-widget{{min-height:760px}}}}

  /* ===== 3 BENEFITS CHECKLIST (white) ===== */
  .benefits{{padding:48px 22px 40px;background:#fff;border-bottom:1px solid #f0f0f0}}
  @media (min-width:900px){{.benefits{{padding:72px 40px 48px}}}}
  .benefits-list{{max-width:720px;margin:0 auto;list-style:none;padding:0}}
  .benefits-list li{{display:flex;gap:16px;align-items:flex-start;padding:18px 22px;background:#fafafa;border:1px solid #ececec;margin-bottom:12px;font-size:15.5px;line-height:1.5;font-weight:600;color:#0a0a0a;border-radius:12px}}
  @media (min-width:900px){{.benefits-list li{{font-size:18px;padding:22px 28px;gap:18px}}}}
  .benefits-list .tick{{flex-shrink:0;width:28px;height:28px;border-radius:50%;background:#22a06b;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:15px;margin-top:1px;box-shadow:0 4px 10px rgba(34,160,107,.3)}}
  .benefits-list .tick::before{{content:"\\2713"}}

  /* ===== NEWS POLAROID STACK (WHITE, single row of 5) ===== */
  .news{{background:#fff;padding:60px 22px 80px;text-align:center;border-bottom:1px solid #f0f0f0}}
  @media (min-width:900px){{.news{{padding:80px 40px 100px}}}}
  .news-h{{color:#0a0a0a;font-family:'Oswald',sans-serif;font-size:28px;text-transform:uppercase;text-align:center;margin-bottom:46px;letter-spacing:.02em;line-height:1.12;font-weight:700;max-width:760px;margin-left:auto;margin-right:auto}}
  @media (min-width:900px){{.news-h{{font-size:38px;margin-bottom:60px;line-height:1.1}}}}
  .news-row{{position:relative;max-width:1100px;margin:0 auto;height:360px}}
  @media (min-width:900px){{.news-row{{height:400px}}}}
  @media (max-width:700px){{.news-row{{height:280px;max-width:400px}}}}
  .ns-card{{position:absolute;background:#fff;border-radius:10px;box-shadow:0 14px 36px rgba(0,0,0,0.16), 0 3px 10px rgba(0,0,0,0.08);overflow:hidden;border:5px solid #fff}}
  .ns-card img{{width:100%;height:100%;display:block;object-fit:cover;border-radius:2px}}
  .ns-a1{{width:260px;height:275px;top:50px;left:2%;transform:rotate(-6deg);z-index:2}}
  .ns-a2{{width:270px;height:285px;top:25px;left:21%;transform:rotate(3deg);z-index:4}}
  .ns-a3{{width:260px;height:275px;top:55px;left:40%;transform:rotate(-3deg);z-index:3}}
  .ns-a4{{width:270px;height:285px;top:30px;right:20%;transform:rotate(4deg);z-index:5}}
  .ns-a5{{width:250px;height:265px;top:60px;right:2%;transform:rotate(-5deg);z-index:2}}
  @media (max-width:700px){{
    .ns-a1,.ns-a2,.ns-a3,.ns-a4,.ns-a5{{width:155px;height:170px;border-width:4px}}
    .ns-a1{{top:50px;left:0}} .ns-a2{{top:20px;left:65px}} .ns-a3{{top:65px;left:130px}}
    .ns-a4{{top:30px;right:65px}} .ns-a5{{top:65px;right:0}}
  }}

  /* ===== BOOKS STRAIGHT INTO (software logo card, white) ===== */
  .integrates{{padding:48px 22px;background:#fff;text-align:center;border-bottom:1px solid #f0f0f0}}
  @media (min-width:900px){{.integrates{{padding:72px 40px}}}}
  .integrates-label{{font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;letter-spacing:.02em;text-transform:uppercase;color:#0a0a0a;margin-bottom:26px;line-height:1.15}}
  @media (min-width:900px){{.integrates-label{{font-size:32px;margin-bottom:36px}}}}
  .integrates-row{{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:14px 16px;max-width:900px;margin:0 auto}}
  @media (min-width:900px){{.integrates-row{{gap:18px 24px}}}}
  .integrate-badge{{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1px solid #e0e0e0;border-radius:999px;padding:11px 20px;box-shadow:0 2px 6px rgba(0,0,0,.05);transition:transform .15s, box-shadow .15s}}
  .integrate-badge:hover{{transform:translateY(-2px);box-shadow:0 6px 16px rgba(0,0,0,.10)}}
  .integrate-badge img{{width:22px;height:22px;object-fit:contain;border-radius:4px}}
  .integrate-badge span{{font-family:'Inter',sans-serif;font-size:14px;font-weight:600;color:#0a0a0a;letter-spacing:-.005em;line-height:1}}
  @media (min-width:900px){{
    .integrate-badge{{padding:14px 26px;gap:12px}}
    .integrate-badge img{{width:28px;height:28px}}
    .integrate-badge span{{font-size:17px}}
  }}

  /* ===== HEAR IT IN ACTION (Wistia-clean, white) ===== */
  .video-block{{padding:60px 22px 70px;background:#fff;text-align:center;border-bottom:1px solid #f0f0f0}}
  @media (min-width:900px){{.video-block{{padding:84px 40px 90px}}}}
  .video-h{{font-family:'Oswald',sans-serif;font-size:28px;font-weight:700;text-transform:uppercase;letter-spacing:.02em;color:#0a0a0a;margin-bottom:14px;line-height:1.12}}
  @media (min-width:900px){{.video-h{{font-size:38px;margin-bottom:18px}}}}
  .video-caption{{font-size:14.5px;color:#444;line-height:1.55;margin-bottom:32px;max-width:680px;margin-left:auto;margin-right:auto;font-weight:500}}
  @media (min-width:900px){{.video-caption{{font-size:17px;margin-bottom:40px}}}}
  .video-card{{max-width:380px;margin:0 auto;background:#0a0a0a;border-radius:14px;position:relative;aspect-ratio:4/5;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.25), 0 6px 16px rgba(0,0,0,.10)}}
  @media (min-width:900px){{.video-card{{max-width:480px;border-radius:18px}}}}
  .video-card iframe{{position:absolute;inset:0;width:100%;height:100%;border:0;display:block;border-radius:inherit}}

  /* ===== URGENCY CLOSER ===== */
  .urgency-closer{{background:#0a0a0a;color:#FFE100;text-align:center;padding:24px 22px;font-family:'Inter',sans-serif;font-size:13.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;line-height:1.5}}
  @media (min-width:900px){{.urgency-closer{{font-size:16px;padding:30px 24px;letter-spacing:.06em}}}}
  .urgency-closer .pulse{{display:inline-block;width:9px;height:9px;background:#D90429;border-radius:50%;margin-right:10px;vertical-align:middle;animation:p 1.4s infinite}}

  /* ===== FOOTER ===== */
  .site-footer{{background:#0a0a0a;color:#888;padding:40px 22px 32px;text-align:center;font-family:'Inter',sans-serif}}
  @media (min-width:900px){{.site-footer{{padding:56px 40px 40px}}}}
  .footer-brand{{font-family:'Oswald',sans-serif;font-size:24px;font-weight:700;color:#fff;letter-spacing:.04em;text-transform:uppercase;margin-bottom:6px}}
  @media (min-width:900px){{.footer-brand{{font-size:28px}}}}
  .footer-tagline{{font-size:13px;color:#999;margin-bottom:24px;letter-spacing:.01em}}
  .footer-links{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 18px;margin-bottom:22px;font-size:12.5px}}
  .footer-links a{{color:#aaa;text-decoration:none;letter-spacing:.04em;transition:color .15s}}
  .footer-links a:hover{{color:#FFE100}}
  .footer-sep{{color:#444}}
  .footer-copy{{font-size:11px;color:#666;letter-spacing:.06em}}

</style>
</head>
<body>

<div class="shell">

  <!-- 1. URGENCY BAR -->
  <div class="urgency"><span class="pulse"></span>{URGENCY_BAR}</div>

  <!-- 2. HERO -->
  <section class="hero">
    <div class="pretitle">{HERO_PRETITLE}</div>
    <h1>{HERO_HEADLINE_HTML}</h1>
    <p class="subhead">{HERO_SUBHEAD}</p>
    <a href="#book" class="cta-scroll">{HERO_CTA} &rarr;</a>
  </section>

  <!-- 3. CALENDAR (first) -->
  <section id="book" class="calendar">
    <h2 class="calendar-h">{CAL_SECTION_H}</h2>
    <p class="calendar-sub">{CAL_SECTION_SUB}</p>
    <div class="iclosed-widget" data-url="{CAL_URL}"></div>
    <script async src="https://app.iclosed.io/assets/widget.js"></script>
  </section>

  <!-- 4. 3 BENEFITS (white) -->
  <section class="benefits">
    <ul class="benefits-list">
      {BENEFITS_HTML}
    </ul>
  </section>

  <!-- 5. NEWS POLAROID STACK (white, single row) -->
  <section class="news">
    <h2 class="news-h">{NEWS_SECTION_H}</h2>
    <div class="news-row">
      <div class="ns-card ns-a1"><img src="/moodboard/M01.jpg" alt=""></div>
      <div class="ns-card ns-a2"><img src="/moodboard/M02.jpg" alt=""></div>
      <div class="ns-card ns-a3"><img src="/moodboard/M07.jpg" alt=""></div>
      <div class="ns-card ns-a4"><img src="/moodboard/M04.jpg" alt=""></div>
      <div class="ns-card ns-a5"><img src="/moodboard/M10.jpg" alt=""></div>
    </div>
  </section>

  <!-- 6. BOOKS STRAIGHT INTO (software logos) -->
  <section class="integrates">
    <div class="integrates-label">{INTEGRATES_LABEL}</div>
    <div class="integrates-row">
      {SOFTWARE_HTML}
    </div>
  </section>

  <!-- 7. HEAR IT IN ACTION (Wistia-clean video) -->
  <section class="video-block">
    <h2 class="video-h">{VIDEO_SECTION_H}</h2>
    <p class="video-caption">{VIDEO_CAPTION}</p>
    <div class="video-card">
      <iframe src="https://iframe.mediadelivery.net/embed/{LIBRARY}/{AUDIO_GUID}?autoplay=false&preload=true&responsive=true"
              title="Answerra Demo Video - {CODE}"
              loading="lazy"
              allow="accelerometer;gyroscope;autoplay;encrypted-media;picture-in-picture;"
              allowfullscreen="true"></iframe>
    </div>
  </section>

  <!-- 8. CALENDAR (second) -->
  <section id="book2" class="calendar">
    <h2 class="calendar-h">{CAL2_SECTION_H}</h2>
    <p class="calendar-sub">{CAL2_SECTION_SUB}</p>
    <div class="iclosed-widget" data-url="{CAL_URL}"></div>
  </section>
</div>

<!-- 9. URGENCY CLOSER -->
<div class="urgency-closer"><span class="pulse"></span>{URGENCY_CLOSER}</div>

<!-- 10. FOOTER -->
<footer class="site-footer">
  <div class="footer-brand">Answerra</div>
  <div class="footer-tagline">The AI receptionist that books while you work.</div>
  <div class="footer-links">
    <a href="mailto:hello@answerra.ai">hello@answerra.ai</a>
    <span class="footer-sep">·</span>
    <a href="/privacy">Privacy</a>
    <span class="footer-sep">·</span>
    <a href="/terms">Terms</a>
  </div>
  <div class="footer-copy">&copy; <span class="urg-year"></span> Answerra &middot; Built in Australia</div>
</footer>

<script>
  (function() {{
    var now = new Date();
    var month = now.toLocaleString("en-AU", {{month: "long"}}).toUpperCase();
    var monthMixed = now.toLocaleString("en-AU", {{month: "long"}});
    var year = now.getFullYear();
    document.querySelectorAll(".urg-month").forEach(function(e){{ e.textContent = month; }});
    document.querySelectorAll(".urg-month-mixed").forEach(function(e){{ e.textContent = monthMixed; }});
    document.querySelectorAll(".urg-year").forEach(function(e){{ e.textContent = year; }});
  }})();
</script>
</body>
</html>
"""


def render_headline_with_red(headline):
    """Convert [bracketed] portion into <span class="red">...</span>"""
    import re
    return re.sub(r"\[([^\]]+)\]", r'<span class="red">\1</span>', headline)


def render_month_placeholder(text):
    """Replace [MONTH] (all caps) and any 'Month' word with span placeholders.
    For caps fields like urgency_bar, use uppercase span.
    For mixed-case body text fields, use mixed-case span."""
    return text.replace("[MONTH]", '<span class="urg-month"></span>')


def render(cfg):
    subhead_plain = cfg["hero_subhead"].replace("&amp;", "&")
    benefits_html = "\n      ".join(
        f'<li><span class="tick" aria-hidden="true"></span><span>{b}</span></li>'
        for b in cfg["benefits"]
    )
    sw_keys = NICHE_SOFTWARE[cfg["niche"]]
    software_html = "\n      ".join(
        f'<a class="integrate-badge"><img src="{SOFTWARE_LOGOS[k][0]}" alt="{SOFTWARE_LOGOS[k][1]}"><span>{SOFTWARE_LOGOS[k][1]}</span></a>'
        for k in sw_keys
    )
    # For body text, we need lowercase-mixed month names, so replace [MONTH] with mixed-case span where appropriate.
    cal2_sub = cfg["calendar2_section_sub"].replace("[MONTH]", '<span class="urg-month-mixed"></span>')
    urgency_closer = cfg["urgency_closer"].replace("[MONTH]", '<span class="urg-month-mixed"></span>')

    return TEMPLATE.format(
        TITLE=cfg["title"],
        SUBHEAD_PLAIN=subhead_plain[:180],
        URGENCY_BAR=render_month_placeholder(cfg["urgency_bar"]),
        HERO_PRETITLE=cfg["hero_pretitle"],
        HERO_HEADLINE_HTML=render_headline_with_red(cfg["hero_headline"]),
        HERO_SUBHEAD=cfg["hero_subhead"],
        HERO_CTA=cfg["hero_cta"],
        CAL_SECTION_H=cfg["calendar_section_h"],
        CAL_SECTION_SUB=cfg["calendar_section_sub"],
        CAL_URL=CAL_URL,
        NEWS_SECTION_H=cfg["news_section_h"],
        BENEFITS_HTML=benefits_html,
        INTEGRATES_LABEL=cfg["integrates_label"],
        SOFTWARE_HTML=software_html,
        VIDEO_SECTION_H=cfg["video_section_h"],
        VIDEO_CAPTION=cfg["video_caption"],
        AUDIO_GUID=cfg["audio_guid"],
        LIBRARY=LIBRARY,
        CODE=cfg["code"],
        CAL2_SECTION_H=cfg["calendar2_section_h"],
        CAL2_SECTION_SUB=cal2_sub,
        URGENCY_CLOSER=urgency_closer,
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
