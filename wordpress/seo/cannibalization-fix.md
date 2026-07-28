# Keyword Cannibalization Fix — 2026-07-28

Consolidated competing URLs onto pillar pages, validated with Google Search Console
(last-6-months Pages export). Goal: stop internal competition **without losing rankings**.
Method: 301 redirects (equity-preserving) + draft the source + de-optimize + internal-link fixes.

## Redirects created (Redirection plugin, all 301)

| From (drafted) | To (pillar/winner) | GSC before |
|---|---|---|
| /sanctify-facility/best-digital-marketing-agency-goa/ | /sanctify-facility/digital-marketing-agency-goa/ | 0 clk |
| /digital-marketing-agency-in-goa/ | ↑ pillar | 4 clk, pos 32 |
| /sanctify-facility/digital-marketing-agency-goa/best-digital-marketing-services-for-local-businesses-in-goa/ | ↑ pillar | 0 clk |
| /sanctify-the-best-digital-marketing-agency-in-vasco/ | ↑ pillar | 2 clk, pos 27 |
| /unleash-your-brands-with-sanctify-best-digital-marketing-agency-in-goa/ | ↑ pillar | 2 clk, pos 31 |
| /on-page-seo-best-practices.../ | /on-page-seo-content-optimization-hub/ | pos 70 → hub pos 10 |
| /finding-the-best-branding-agency-in-goa-a-comprehensive-guide/ | /sanctify-best-branding-agency-in-goa-redefining-branding-in-goa/ | pos 50 → winner pos 15 |
| /maximizing-business-growth-a-beginners-guide-to-social-media-optimization/ | /sanctify-10-social-media-optimization-tips.../ | 3 impr → winner pos 17 |

## Pillar (5512) improvements
- Removed circular internal link to the Vasco page (which now 301s back to the pillar)
- Absorbed the "local businesses in Goa" angle from the redirected 6510 (new H2 section)
- Fixed heading structure: 3 H1s → 1 H1 (demoted 2 content H1s to H2; keywords retained)

## Kept (NOT redirected) — distinct intent or actively ranking
- Homepage, /about-sanctify/, /contact/, /case-studies/ (distinct intent)
- /digital-marketing-agency-in-goa-2026-guide/, /how-to-choose.../, /top-digital-marketing-companies.../ (informational)
- SEO: /basic-search-engine-optimization-seo-techniques/ (29,222 impr), /technical-seo-masterclass/
- Branding: /graphic-designing.../logo-designing/, /sanctify-logo-story/

## Ranking-protection decisions
- **Hanuman Jayanti post (5385): left completely untouched** — ranks position 3.68 with 4,407
  impressions for seasonal queries. Not redirected, title not changed.
- **Onam post (6541): SEO title de-optimized only** (negligible impressions) to stop it
  diluting the DM cluster. Content untouched.
- Internal link from Ram Navami post checked — was a false positive (attachment URL), no change needed.

## Rollback
- Redirection rules: delete via Redirection plugin (IDs 5–12) or REST bulk delete
- Drafted pages: full edit-context originals saved in cannibal/originals/*.json — restore status to 'publish'
- Pillar: original saved as cannibal/pillar-5512-original.json

## Verification (all passed)
- 8/8 redirects return 301 to the correct target
- All 4 targets return 200 (no redirect chains)
- All drafted URLs removed from SEOPress sitemap; kept pages remain
- Pillar renders exactly 1 H1 live; local-business section live; circular link gone
- Key URLs (home, pillar, hub, winners, case-studies, kept guides, Hanuman) all 200

## Follow-ups (separate tasks)
- robots.txt still points to the old flat /sitemap.xml (not SEOPress's) — may still list
  redirected URLs (harmless, they 301). Part of the sitemap/robots cleanup task.
- Social Media cluster has no service-page pillar — consider creating one.
- basic-seo-techniques: 29,222 impressions at pos 28 — biggest single optimization opportunity.
