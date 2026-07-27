# Page 6789 — /case-studies/ SEO rewrite

Live URL: https://www.sanctify.in/case-studies/
Applied: 2026-07-28 via WordPress REST API

## Files

| File | Purpose |
|---|---|
| `BEFORE-page-6789.json` | Full API snapshot of the page before any change. **Rollback source.** |
| `AFTER-content.html` | The rewritten page body that was published |
| `AFTER-schema.json.html` | FAQPage + ItemList JSON-LD appended to the content |
| `AFTER-page-6789.json` | Full API snapshot after the change |

## What changed

| Factor | Before | After |
|---|---|---|
| H1 count | 2 (one wrapped an image) | 1, keyword-led |
| H2 / H3 | 6 / 0 | 8 / 15 |
| Hero image alt | empty `""` | descriptive |
| Image wrapped in link to raw PNG | yes | removed |
| Internal links | 1 | 19 (all verified 200) |
| Inline `font-size` declarations | 27 | 0 |
| `Myriad Pro` (font never loaded) | 34 refs | 0 |
| Unreplaced placeholder text | present | removed |
| Scannable client table | none | 11 rows |
| FAQ section | none | 5 Q&A + FAQPage schema |
| Word count | 730 | 1531 |
| Named real clients | 0 | 20 |
| SEO title tag | `Case Studies ` (13 chars) | 57 chars, keyword-led |
| Meta description | auto-generated, truncated | hand-written, 153 chars |
| `og:image` | missing | set (featured image 6796) |
| Schema | WebPage, Organization, BreadcrumbList | + FAQPage, ItemList |

## Notes

- Slug left as `case-studies` — unchanged, so no redirect is required.
- Page title changed to `Case Studies: Advertising & Digital Marketing Work in Goa` because the
  `digital-marketing` theme renders the page title as the `<h1>`. Nav menu item **6793** had its
  label explicitly pinned to `Case Studies` so the menu is unaffected. Both verified live.
- Media **6796** alt text and title were also updated (affects the image everywhere it is used).

## Outstanding — needs a human

1. **No performance metrics.** Nothing in this rewrite invents numbers. Real figures
   (traffic lift, lead volume, ROAS, ranking movement) would materially strengthen the page,
   but only Sanctify can supply them, and client consent is needed before publishing them.
2. `twitter:card` is still `summary`. Upgrading to `summary_large_image` is a global SEOPress
   setting not exposed over REST — toggle in SEOPress → Social Networks.
3. `seopress_social_accounts_twitter` is set to the placeholder `@#`. Should be the real handle
   or cleared.

## Rollback

```bash
# restores original title, content, excerpt and SEO meta
python3 - <<'PY'
import json, subprocess
d = json.load(open('BEFORE-page-6789.json'))
payload = json.dumps({
    "title":   d['title']['raw'],
    "content": d['content']['raw'],
    "excerpt": d['excerpt']['raw'],
    "featured_media": d.get('featured_media', 0),
    "meta": {
        "_seopress_titles_title": (d.get('meta') or {}).get('_seopress_titles_title', ''),
        "_seopress_titles_desc":  (d.get('meta') or {}).get('_seopress_titles_desc', ''),
    },
})
open('/tmp/rollback.json','w').write(payload)
PY
curl -u "USER:APP_PASSWORD" -X POST \
  "https://www.sanctify.in/wp-json/wp/v2/pages/6789" \
  -H 'Content-Type: application/json' --data-binary @/tmp/rollback.json
```

Also reset the menu label if rolling back: `POST /wp-json/wp/v2/menu-items/6793` with
`{"title":"Case Studies"}` (harmless either way).
