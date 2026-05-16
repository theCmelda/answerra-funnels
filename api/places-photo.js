// /api/places-photo.js — proxy for Google Places Photos
// Hides our API key from the browser. Stream the JPEG/PNG bytes through.

export default async function handler(req, res) {
  const key = process.env.GOOGLE_PLACES_API_KEY;
  if (!key) return res.status(500).end("no key");

  const ref = (req.query.ref || "").toString();
  if (!ref) return res.status(400).end("ref required");

  const w = Math.min(parseInt(req.query.w, 10) || 800, 1600);

  const url = `https://maps.googleapis.com/maps/api/place/photo?maxwidth=${w}&photo_reference=${encodeURIComponent(ref)}&key=${encodeURIComponent(key)}`;
  try {
    const r = await fetch(url, { redirect: "follow" });
    if (!r.ok) {
      console.error("[places-photo] google", r.status);
      return res.status(r.status).end();
    }
    const contentType = r.headers.get("content-type") || "image/jpeg";
    res.setHeader("Content-Type", contentType);
    res.setHeader("Cache-Control", "public, max-age=86400, s-maxage=86400, immutable");
    const buf = Buffer.from(await r.arrayBuffer());
    return res.status(200).send(buf);
  } catch (e) {
    console.error("[places-photo] error", e.message);
    return res.status(500).end();
  }
}

export const config = { runtime: "nodejs" };
