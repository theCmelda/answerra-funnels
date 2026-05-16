/* Answerra · Meta Pixel + CAPI dedup + first-party click attribution
   - Loads pixel base code
   - Generates a persistent visitor_id cookie (1y) for backend attribution
   - Captures fbclid / gclid / utm_* on first hit and beacons to /api/track-click
   - Fires PageView client-side AND beacons to /api/capi-pageview for browser+server dedup
   - One source of truth: change PIXEL here OR set PIXEL_ID env var on the backend. */
(function(){
  var PIXEL = '1511657447261837';

  // ===== Standard Meta Pixel base =====
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
  (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');

  // ===== Cookie helpers =====
  function setCookie(k, v, days){
    var d = new Date(); d.setTime(d.getTime() + (days*24*60*60*1000));
    document.cookie = k + '=' + encodeURIComponent(v) + '; expires=' + d.toUTCString() + '; path=/; domain=.answerra.ai; SameSite=Lax';
  }
  function getCookie(k){
    var m = document.cookie.match(new RegExp('(?:^|; )' + k + '=([^;]*)'));
    return m ? decodeURIComponent(m[1]) : null;
  }
  function uuid(){
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return 'v_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2);
  }

  // ===== visitor_id (first-party, 1 year) =====
  var visitorId = getCookie('v_id');
  if (!visitorId) { visitorId = uuid(); setCookie('v_id', visitorId, 365); }
  window.AnswerraVisitorId = visitorId;

  // ===== Capture URL params on first hit =====
  var params = new URLSearchParams(window.location.search);
  var fbclid = params.get('fbclid');
  var gclid  = params.get('gclid');
  var ttclid = params.get('ttclid');
  var msclkid= params.get('msclkid');
  var utm = {
    utm_source:   params.get('utm_source'),
    utm_medium:   params.get('utm_medium'),
    utm_campaign: params.get('utm_campaign'),
    utm_content:  params.get('utm_content'),
    utm_term:     params.get('utm_term'),
    utm_id:       params.get('utm_id'),
  };

  // Persist click ids in cookies so they survive across pages
  if (fbclid) setCookie('aa_fbclid', fbclid, 90);
  if (gclid)  setCookie('aa_gclid',  gclid,  90);
  if (ttclid) setCookie('aa_ttclid', ttclid, 90);
  Object.keys(utm).forEach(function(k){ if (utm[k]) setCookie('aa_' + k, utm[k], 90); });

  // Build _fbc cookie from fbclid if browser hasn't (helps server-side attribution)
  // Meta format: fb.1.<timestamp>.<fbclid>
  if (fbclid && !getCookie('_fbc')) {
    var fbc = 'fb.1.' + Date.now() + '.' + fbclid;
    setCookie('_fbc', fbc, 90);
  }

  // ===== Init pixel + PageView (with eventID for dedup) =====
  var eventId = uuid();
  fbq('init', PIXEL);
  fbq('track', 'PageView', {}, { eventID: eventId });

  function beacon(url, payload){
    try {
      var json = JSON.stringify(payload);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(url, new Blob([json], { type: 'application/json' }));
      } else {
        fetch(url, { method:'POST', headers:{'Content-Type':'application/json'}, body: json, keepalive:true });
      }
    } catch(e) {}
  }

  // ===== Server-side PageView (CAPI dedup via eventID) =====
  beacon('/api/capi-pageview', {
    event_id: eventId,
    event_name: 'PageView',
    event_source_url: window.location.href,
    referrer: document.referrer || '',
    visitor_id: visitorId
  });

  // ===== Click + campaign attribution =====
  // Always beacon (cheap, upserts on visitor_id+landing_path)
  beacon('/api/track-click', {
    visitor_id: visitorId,
    landing_path: window.location.pathname,
    referrer: document.referrer || '',
    fbclid:  fbclid || getCookie('aa_fbclid'),
    gclid:   gclid  || getCookie('aa_gclid'),
    ttclid:  ttclid || getCookie('aa_ttclid'),
    msclkid: msclkid|| null,
    utm_source:   utm.utm_source   || getCookie('aa_utm_source'),
    utm_medium:   utm.utm_medium   || getCookie('aa_utm_medium'),
    utm_campaign: utm.utm_campaign || getCookie('aa_utm_campaign'),
    utm_content:  utm.utm_content  || getCookie('aa_utm_content'),
    utm_term:     utm.utm_term     || getCookie('aa_utm_term'),
    utm_id:       utm.utm_id       || getCookie('aa_utm_id'),
    fbc:          getCookie('_fbc'),
    fbp:          getCookie('_fbp'),
  });

  // ===== Auto-append visitor_id to every iClosed link/widget =====
  // Captures clicks on <a> tags pointing to app.iclosed.io and rewrites the href to include
  // ?visitor_id=<v_id> so iClosed's "Forward event parameters" config flows it back to
  // /api/booking-confirm webhook for full attribution.
  // Derive niche from current page path so iClosed forwards it back to /quiz
  function deriveNiche() {
    var p = window.location.pathname.toLowerCase();
    if (p.indexOf('dental') !== -1) return 'dental';
    if (p.indexOf('medspa') !== -1 || p.indexOf('skin') !== -1 || p.indexOf('injectable') !== -1) return 'medspa';
    if (p.indexOf('plumb') !== -1 || p.indexOf('trade') !== -1 || p.indexOf('hvac') !== -1) return 'plumbing';
    return null;
  }
  var pageNiche = deriveNiche();

  function appendVidToUrl(href, vId) {
    try {
      var u = new URL(href, window.location.origin);
      if (!/iclosed\.io/.test(u.hostname)) return null;
      if (!u.searchParams.has('visitor_id')) u.searchParams.set('visitor_id', vId);
      if (pageNiche && !u.searchParams.has('niche')) u.searchParams.set('niche', pageNiche);
      // Pass through any captured fbclid / utm_campaign for downstream attribution display
      var passThrough = ['fbclid','gclid','utm_source','utm_medium','utm_campaign','utm_content'];
      passThrough.forEach(function(k){
        var v = getCookie('aa_' + k.replace('utm_','utm_')) || getCookie('aa_' + k);
        if (k === 'fbclid') v = getCookie('aa_fbclid');
        if (k === 'gclid') v = getCookie('aa_gclid');
        if (v && !u.searchParams.has(k)) u.searchParams.set(k, v);
      });
      return u.toString();
    } catch (e) { return null; }
  }

  // Rewrite any existing iClosed links on the page now
  document.querySelectorAll('a[href*="iclosed.io"]').forEach(function(a){
    var nu = appendVidToUrl(a.href, visitorId);
    if (nu) a.href = nu;
  });

  // Also rewrite any iClosed iframes
  document.querySelectorAll('iframe[src*="iclosed.io"]').forEach(function(f){
    var nu = appendVidToUrl(f.src, visitorId);
    if (nu) f.src = nu;
  });

  // Catch clicks on iClosed links added later (dynamic CTAs)
  document.addEventListener('click', function(ev){
    var a = ev.target.closest('a');
    if (!a || !a.href || !/iclosed\.io/.test(a.href)) return;
    if (a.href.indexOf('visitor_id=') !== -1) return;
    var nu = appendVidToUrl(a.href, visitorId);
    if (nu) a.href = nu;
  }, true);

  // Expose for debugging
  window.AnswerraVisitorId = visitorId;
})();
