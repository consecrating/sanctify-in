# Facility / Landing pages — v2 premium redesign (DEPLOYED)

Applied **2026-08-01** to https://www.sanctify.in via WordPress REST API (user `kiara`, admin, `unfiltered_html`).

## Pages redesigned (live)
| Page | ID | Live URL |
|---|---|---|
| Social Media Marketing Agency in Goa | 6977 | https://www.sanctify.in/sanctify-facility/social-media-marketing-agency-goa/ |
| Local SEO Services in Goa | 6978 | https://www.sanctify.in/sanctify-facility/local-seo-services-goa/ |
| PPC & Google Ads Agency in Goa | 6979 | https://www.sanctify.in/sanctify-facility/ppc-google-ads-agency-goa/ |
| Content Marketing Agency in Goa | 6980 | https://www.sanctify.in/sanctify-facility/content-marketing-agency-goa/ |
| Digital Marketing Agency in North Goa | 6981 | https://www.sanctify.in/digital-marketing-agency-north-goa/ |
| Digital Marketing Agency in South Goa | 6982 | https://www.sanctify.in/digital-marketing-agency-south-goa/ |

## What changed
- New self-contained premium design system (`.sfy2`) with inline scoped CSS/JS (Sora + Inter, mesh-gradient hero, glass cards, gradient CTA). Does not depend on / conflict with the old global `sanctify-svc-css` / `smx-css`.
- **Distinct hero device mockups per page:** SMM = Instagram phone/reel; Local SEO + city pages = Google **Map Pack** card; PPC = Google Ads result + ROAS bars; Content = SERP ranking + traffic sparkline. All CSS/SVG (no raster images → no blur/upscaling issues).
- **Fixed the blank-render bug:** the previous pages hid every section with `opacity:0` until a JS IntersectionObserver fired, so below-fold content was invisible to a static viewer and to crawlers. v2 uses a pure on-load CSS keyframe (`sfy-in`) that **always ends visible** — no JS/observer dependency. Verified live.
- Working stroke-icon set (old bento had empty icon chips), animated stat counters (real values baked into the DOM for SEO; JS only enhances), process timeline, FAQ.
- **Schema per page:** `Service` + `FAQPage` + `BreadcrumbList` JSON-LD.
- **SEOPress meta** updated per page (`_seopress_titles_title`, `_seopress_titles_desc`).
- Internal links between all six + to SEO / influencer / contact.

## Files
- `build.py` — generator (design system + per-page content model). `python3 build.py` → `build/*.content.html` + `preview/*.html`.
- `deploy.py` — REST deploy driver (curl is used in practice; urllib is blocked by the Sucuri WAF client fingerprint).
- `shot.py` — local Chromium full-page screenshotter (points at `/opt/playwright`).
- `build/<slug>.content.html` — exact content POSTed to each page.
- `build/<slug>.payload.json` — `{content, meta}` payload per page.
- `_before/RAW-<id>.json` — **true raw backup (context=edit)** = rollback source.
- `_before/BEFORE-page-<id>.json` — earlier rendered snapshot.

## Rollback (restores original content + SEO meta for one page)
```bash
WPUSER="kiara"; WPPASS="<app password>"
python3 - <<'PY'
import json
d=json.load(open('_before/RAW-6977.json'))
json.dump({"content":d['content']['raw'],
           "meta":{"_seopress_titles_title":(d.get('meta') or {}).get('_seopress_titles_title',''),
                   "_seopress_titles_desc":(d.get('meta') or {}).get('_seopress_titles_desc','')}},
          open('/tmp/rb.json','w'))
PY
curl -u "$WPUSER:$WPPASS" -X POST -H "Content-Type: application/json" \
  --data-binary @/tmp/rb.json "https://www.sanctify.in/wp-json/wp/v2/pages/6977"
```
Repeat with the matching `RAW-<id>.json` for other pages.

## Notes
- Slugs / titles / parents unchanged — only page **content** + SEO meta replaced. No redirects needed.
- Deploy transport: `curl` (WAF blocks python-urllib UA). App-password auth over HTTPS.
- Magnific API key verified working (Freepik/Magnific text-to-image, base64 sync). Not yet used on-page — clean CSS/SVG design needs no raster imagery. Candidate next use: custom 1200×630 Open Graph share images per page (og:image is currently unset).
