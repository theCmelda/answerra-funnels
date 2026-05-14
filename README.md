# Answerra Funnels

8 niche-specific VSL funnel pages for Answerra AI voice receptionist (AU launch).

Bunny Stream library: **660166**. Deployed via Vercel to https://answerra.ai.

## Funnel → VSL mapping

| Code | Source file | Bunny GUID | Status |
|---|---|---|---|
| DEN-01 | funnels/funnel-dental-01-two-kinds.html | 461e92f3-011f-4e03-b5f1-4a9e69254df9 | live `/dental` |
| DEN-02 | funnels/funnel-dental-02-freest-job.html | 23081495-11ad-4e67-95fb-a2bd7eff3a3f | not deployed |
| DEN-03 | funnels/funnel-dental-03-mrs-henderson.html | 380ef4f0-1952-42a8-b116-bfeb5387ff5e | not deployed |
| MED-01 | funnels/funnel-medspa-01-1500-lapsed.html | d85d6c7a-5060-4775-9aed-62587ac79562 | live `/medspa` |
| MED-02 | funnels/funnel-medspa-02-two-kinds.html | 426523c4-a1cd-4688-a9dd-dc2394fec425 | not deployed |
| MED-03 | funnels/funnel-medspa-03-sunday-instagram.html | 14b306fd-d297-477a-b821-6bc21617ed76 | not deployed |
| PLU-01 | funnels/funnel-plumbing-01-phone-cant-answer.html | 8bfb20d1-b920-4cc0-977f-60e331e74c0f | not deployed |
| PLU-02 | funnels/funnel-plumbing-02-hipages-bleed.html | 6cc6f109-1f63-4396-8a78-608c899fe952 | not deployed |

## Player settings (in each iframe)

```
autoplay=true&muted=true&preload=true&responsive=true&loop=false
```

4:5 aspect ratio, absolute fill, fullscreen + picture-in-picture allowed. The yellow placeholder badge (`.vsl::before`) was stripped so the Bunny player renders clean.

## Deploy

Source of truth is `~/Desktop/Answerra.ai funnels/funnels/` on Daniel's Mac. Currently deployed via `vercel deploy --prod` (CLI). To switch to GitHub-triggered deploys, link this repo to the Vercel `answerra-funnels` project.
