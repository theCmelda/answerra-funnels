#!/usr/bin/env python3
"""
Generate 9 direct-to-calendar funnel pages (v8 — minimal).

v8 = the client's "plain and simple" call:
  - Outcome-led headline (Haynes framework)
  - iClosed calendar embed
  - That's it.

No subhead. No urgency strip. No benefits. No logos. No video. No footer. Nothing else.
"""

from pathlib import Path

CAL_URL = "https://app.iclosed.io/e/answrra/free-ai-receptionist-demo-build"


# ============================================================
#  FUNNEL CONTENT — only the headline matters here
# ============================================================
FUNNELS = {
    "dental-01-two-kinds": {
        "code": "DEN-01",
        "title": "Recover $244K-$305K A Year From Missed Dental Calls",
        "headline": "How AU Dental Practices Are Recovering [$244K-$305K A Year] In Missed Calls Without Hiring Another Receptionist",
    },
    "dental-02-freest-job": {
        "code": "DEN-02",
        "title": "Save $88K A Year Without Training Another Receptionist",
        "headline": "How AU Dental Practices Are Saving [$88K A Year In Hiring Costs] Without Training Another Receptionist From Scratch",
    },
    "dental-03-mrs-henderson": {
        "code": "DEN-03",
        "title": "Unlock $1.4M In Lapsed Patients Without Lifting A Finger",
        "headline": "How AU Dental Practices Are Unlocking [$1.4M In Lapsed Patient Value] Without Asking Their Receptionist To Make A Single Call",
    },
    "dental-04-647pm": {
        "code": "DEN-04",
        "title": "Capture Every After-Hours Call Without Answering The Phone",
        "headline": "How AU Dental Practices Are Capturing [$1,348 Per After-Hours Call] Without The Owner Ever Answering The Phone Again",
    },
    "medspa-01-1500-lapsed": {
        "code": "MED-01",
        "title": "Reactivate $675K In Lapsed Mindbody Clients",
        "headline": "How AU Medspas Are Reactivating [$675K In Lapsed Mindbody Clients] Without Their Nurse Making A Single Call",
    },
    "medspa-02-two-kinds": {
        "code": "MED-02",
        "title": "Book 3x More Meta Leads Without Calling Anyone Back",
        "headline": "How AU Medspas Are Booking [3x More Consults From The Same Meta Spend] Without Calling Leads Back Themselves",
    },
    "medspa-03-sunday-instagram": {
        "code": "MED-03",
        "title": "Add 4-5 Extra Weekend Bookings Without Working Sundays",
        "headline": "How AU Medspas Are Adding [4-5 Extra Weekend Bookings A Week] Without Working A Single Sunday Night",
    },
    "plumbing-01-phone-cant-answer": {
        "code": "PLU-01",
        "title": "Recover $1,500-$1,800 In Lost Jobs Every Week",
        "headline": "How AU Plumbers Are Recovering [$1,500-$1,800 In Lost Jobs Every Week] Without Dropping Their Tools To Answer The Phone",
    },
    "plumbing-02-hipages-bleed": {
        "code": "PLU-02",
        "title": "Book 3x More Hipages Jobs From The Same Spend",
        "headline": "How AU Plumbers Are Booking [3x More Hipages Jobs From The Same Lead Spend] Without Dropping Tools To Call Anyone Back",
    },
}


# ============================================================
#  TEMPLATE (minimal)
# ============================================================
TEMPLATE = """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=Inter:wght@500;600;700&display=swap" rel="stylesheet">
<style data-v="v8-minimal">
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  html,body{{background:#fff;color:#0a0a0a;font-family:'Inter','Open Sans',Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.45}}
  main{{max-width:960px;margin:0 auto;padding:48px 22px 40px;text-align:center}}
  @media (min-width:900px){{main{{padding:80px 40px 60px}}}}
  h1{{font-family:'Oswald',Impact,sans-serif;color:#0a0a0a;font-size:32px;line-height:1.06;font-weight:700;margin-bottom:36px;letter-spacing:-.005em;text-transform:uppercase}}
  @media (min-width:900px){{h1{{font-size:54px;line-height:1.04;margin-bottom:48px;max-width:980px;margin-left:auto;margin-right:auto}}}}
  h1 .red{{color:#D90429}}
  .iclosed-widget{{min-height:680px;width:100%;border:0;outline:0;background:transparent}}
  .iclosed-widget iframe{{border:0!important;outline:0!important}}
  @media (min-width:900px){{.iclosed-widget{{min-height:760px}}}}

  /* Invisible-but-compliant footer */
  .footer{{padding:20px 22px 28px;text-align:center;font-family:'Inter',sans-serif;font-size:10.5px;font-weight:400;color:#bcbcbc;line-height:1.7;letter-spacing:.01em;max-width:780px;margin:0 auto}}
  .footer a{{color:#bcbcbc;text-decoration:none;border-bottom:1px solid transparent;transition:color .15s, border-color .15s}}
  .footer a:hover{{color:#0a0a0a;border-bottom-color:#0a0a0a}}
  .footer .sep{{color:#dadada;margin:0 6px}}
  .footer .legal{{display:block;margin-top:6px;color:#cfcfcf;font-size:10px;letter-spacing:.02em}}
</style>
<!-- Meta Pixel via /pixel.js -->
<script src="/pixel.js" async></script>
<noscript><img height="1" width="1" style="display:none" src="https://www.facebook.com/tr?id=1511657447261837&ev=PageView&noscript=1" alt=""/></noscript>
</head>
<body>
<main>
  <h1>{HEADLINE_HTML}</h1>
  <div class="iclosed-widget" data-url="{CAL_URL}"></div>
  <script async src="https://app.iclosed.io/assets/widget.js"></script>
</main>

<footer class="footer">
  <a href="mailto:hello@answerra.ai">hello@answerra.ai</a><span class="sep">&middot;</span><a href="/privacy">Privacy</a><span class="sep">&middot;</span><a href="/terms">Terms</a><span class="sep">&middot;</span>&copy; <span class="urg-year"></span> Answerra
  <span class="legal">Results referenced are case examples and not guaranteed. Not affiliated with Meta, Mindbody, Praktika, Simpro or any other software shown. Australia.</span>
</footer>

<script>
  (function(){{ var y=new Date().getFullYear(); document.querySelectorAll(".urg-year").forEach(function(e){{e.textContent=y}}); }})();
</script>
</body>
</html>
"""


def render_headline_with_red(headline):
    import re
    return re.sub(r"\[([^\]]+)\]", r'<span class="red">\1</span>', headline)


def render(cfg):
    return TEMPLATE.format(
        TITLE=cfg["title"],
        HEADLINE_HTML=render_headline_with_red(cfg["headline"]),
        CAL_URL=CAL_URL,
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
