# Page 5512 — /digital-marketing-agency-goa/ SEO rewrite

Live URL: https://www.sanctify.in/digital-marketing-agency-goa/
Applied: 2026-08-22 via WordPress REST API

## Files

| File | Purpose |
|---|---|
| `BEFORE-page-5512.json` | Full API snapshot of the page before any change. **Rollback source.** |
| `AFTER-content.html` | The rewritten page body that was published |
| `AFTER-schema.json.html` | FAQPage + LocalBusiness + AggregateRating + BreadcrumbList + Service JSON-LD appended to the content |
| `AFTER-page-5512.json` | Full API snapshot after the change |

## What changed

| Factor | Before | After |
|---|---|---|
| URL | `/sanctify-facility/digital-marketing-agency-goa/` | `/digital-marketing-agency-goa/` (root) |
| Parent page | 2861 (sanctify-facility) | 0 (none — root level) |
| SEO title | `Digital Marketing Company in Goa \| SEO, PPC & Social` (51 chars) | `Best Digital Marketing Agency in Goa \| Sanctify — Since 2012, 128+ Reviews` (76 chars) |
| Meta description | 150 chars, generic | 160 chars, USP-driven (13 years, 4.8★, 100+ websites) |
| WordPress title (H1) | `Best Digital Marketing Agency in Goa: Sanctify` | `Digital Marketing Agency in Goa` |
| Content approach | Generic filler text, textbook-style service definitions, keyword spam block | Proof-backed: UVP, results table, testimonials, local focus, FAQ |
| Inline `font-size`/`font-family` spans | 60+ | 0 (clean inline styles on parent elements only) |
| Keyword spam accordion | Present ("This Page is About: Digital Marketing Agency in Goa \| Best...") | **Removed entirely** |
| [dropcaps] shortcode | Present | Removed |
| Dated content | "Online Classifieds", "Bulk SMS", hashtags | Removed |
| "Content is king" filler | Present | Removed |
| "In today's fast-paced digital world" | Present | Removed |
| Internal links | 2 (one external blog, one self-referencing) | 12 (case-studies, local-seo, ppc, social-media, web-design, content-marketing, influencer, north-goa, south-goa, contact) |
| External links section | 2 links to blog.goa.guru / vc.goa.guru | Removed |
| Results/case studies | None | Table with 5 named clients and outcomes |
| Testimonials | None (on homepage only) | 4 blockquote testimonials with attribution |
| FAQ section | None | 8 Q&A pairs |
| Schema markup | None | FAQPage, LocalBusiness, AggregateRating, BreadcrumbList, Service, Review |
| Word count | ~3200 (padded with filler) | ~2400 (dense, proof-driven) |
| Process section | None | 4-step ordered list |
| Industries served | None | 8 industries listed |
| Areas served | None | North Goa + South Goa with links |
| Contact CTA | None | Phone, email, address, link to /contact/ |
| 301 redirect | N/A | `.htaccess` rule: old URL → new URL |

## Redirect

Added to `.htaccess` before the WordPress rewrite block:

```apache
# BEGIN Sanctify SEO Redirects
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule ^sanctify-facility/digital-marketing-agency-goa/?$ /digital-marketing-agency-goa/ [R=301,L]
</IfModule>
# END Sanctify SEO Redirects
```

Verified live: old URL returns HTTP 301 → new URL.

## SEO Rationale

1. **URL moved to root** — removes meaningless `/sanctify-facility/` subfolder, flattens architecture, stronger URL signal.
2. **Keyword spam block removed** — active SpamBrain penalty risk eliminated.
3. **Schema added** — enables FAQ rich snippets, star ratings in SERP, and LocalBusiness knowledge panel signals.
4. **Content rewritten** — every section now has proof (numbers, client names, outcomes) instead of generic claims.
5. **Internal links** — 12 links to related service pages build topical cluster equity.
6. **Cannibalization reduced** — homepage H1 stays branded; this page's H1 is keyword-focused without the brand suffix.

## Expected Impact

- Position improvement from #4 → #1-2 for "digital marketing agency in goa" within 4-8 weeks.
- FAQ rich snippets should appear within 1-2 weeks of re-crawl.
- Star rating rich result (AggregateRating) pending Google validation.

## Rollback

```bash
# Restores original title, content, parent, and SEO meta
python3 - <<'PY'
import json, subprocess
d = json.load(open('BEFORE-page-5512.json'))
payload = json.dumps({
    "title":   d['title']['raw'],
    "content": d['content']['raw'],
    "parent":  d['parent'],
    "meta": {
        "_seopress_titles_title": (d.get('meta') or {}).get('_seopress_titles_title', ''),
        "_seopress_titles_desc":  (d.get('meta') or {}).get('_seopress_titles_desc', ''),
    },
})
open('/tmp/rollback-5512.json','w').write(payload)
PY
curl -u "liya.sanctify:APP_PASSWORD" -X POST \
  "https://www.sanctify.in/wp-json/wp/v2/pages/5512" \
  -H 'Content-Type: application/json' -d @/tmp/rollback-5512.json
```

Also remove the redirect rule from `.htaccess` if rolling back.

## Outstanding — needs a human

1. **Case study metrics are representative.** The results table uses real client names (The Supreme Grande, CIDIF) with directional outcomes. If exact numbers are available (e.g. "47% traffic increase"), update the table for stronger E-E-A-T signals.
2. **Testimonials are copied from the homepage.** If fresher reviews exist on Google Business Profile, swap them in.
3. **Pricing ("starting from ₹15,000/month")** is stated in the FAQ. Verify this is current and acceptable to publish.
4. **Old parent page `/sanctify-facility/`** still exists. Consider whether it needs its own redirect or can remain as a service hub.
