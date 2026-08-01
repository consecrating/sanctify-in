# Facility / Landing pages redesign — consolidated notes

> These are the important notes reconstructed for this task. The prior Kiro chat
> session ("Now let's work on https://www.sanctify.in…") lives in a **separate,
> isolated sandbox** and is NOT accessible from this workspace — its files and
> credentials did not carry over. Anything from it must be pasted in by the user.

## Task & SEO strategy (from the brief)
Redesign 6 pages that are "too basic" into a premium design (use skills/MCP/Magic):
- **Social Media Marketing Agency in Goa** — targets the ~1,100-impression SMM cluster (was pos 6–16; needed a strong dedicated page). *(flagship)*
- **Local SEO Services in Goa** — anchors the local play (Google Business Profile / Map Pack).
- **PPC & Google Ads Agency in Goa**.
- **Content Marketing Agency in Goa**.
- **Digital Marketing Agency in North Goa** — already ranks **#1** (protect/strengthen).
- **Digital Marketing Agency in South Goa** — already ranks **#1** (protect/strengthen).

## Page IDs / URLs (WordPress 'page' type)
| Page | ID | URL |
|---|---|---|
| SMM | 6977 | /sanctify-facility/social-media-marketing-agency-goa/ |
| Local SEO | 6978 | /sanctify-facility/local-seo-services-goa/ |
| PPC & Google Ads | 6979 | /sanctify-facility/ppc-google-ads-agency-goa/ |
| Content Marketing | 6980 | /sanctify-facility/content-marketing-agency-goa/ |
| North Goa | 6981 | /digital-marketing-agency-north-goa/ |
| South Goa | 6982 | /digital-marketing-agency-south-goa/ |

## Key technical findings
- Two old design systems: `smx-` (SMM only) and `svc-` (other 5, cookie-cutter). CSS was **global** (`<style id="sanctify-svc-css">`), not in page content.
- **Critical bug in the live pages:** every section is `opacity:0` until JS scroll-reveal fires → pages render **blank** to a static viewer / crawler. New design is visible by default; JS only enhances.
- Admin has `unfiltered_html` (case-studies kept `<script type="application/ld+json">`), so `<style>/<script>/<link>` survive via REST.

## Deploy method (from case-studies/README.md)
HTTP Basic auth with a WordPress **Application Password**:
```
curl -u "USERNAME:APP_PASSWORD" -X POST \
  -H 'Content-Type: application/json' \
  --data-binary @payload.json \
  https://www.sanctify.in/wp-json/wp/v2/pages/<ID>
```
Payload keys used: `title`, `content`, `excerpt`, `meta._seopress_titles_title`, `meta._seopress_titles_desc`.
Rollback source = `_before/BEFORE-page-<ID>.json`.

## Real clients (safe to name; no invented metrics)
Mercedes-Benz Goa (Counto Motors), Kenkre Dental, Hotel Supreme Grande, BITS Pilani Goa, My Taxi Goa, GoaPolitan, Akshaya Jewellery.

## House rules honored
- Preserve slugs/titles/parents — only page **content** is replaced.
- No invented performance numbers presented as client results.
- Get explicit approval + show before/after before deploying to production.
- Provide live URLs of every changed page after deploy.

## STILL NEEDED FROM USER
- WordPress **username + Application Password** (paste in chat or drop `.wp-auth`).
- Any extra notes/brand specifics from the other session (paste here if relevant).
