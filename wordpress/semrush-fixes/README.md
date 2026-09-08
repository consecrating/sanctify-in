# Semrush Site Audit — top issues resolved

Applied 2026-09-08 to www.sanctify.in via FTPS and the WordPress REST API.

Semrush reported three errors:

| # | Reported | Status |
|---|---|---|
| 1 | 1 hreflang conflict within page source code | **Cannot reproduce** — needs the URL from Semrush |
| 2 | 55 items with markup errors | **Fixed** — root cause found and corrected |
| 3 | 3 pages don't have a unique title | **Fixed** |

---

## Issue 2 — 55 items with markup errors (the real one)

### Root cause

`auto-keyword-links` was injecting `<a href="...">` markup **inside**
`<script type="application/ld+json">`, so the `href="` quotes terminated the JSON
string early and the whole block became unparseable.

Proven by comparing the stored value against the rendered output on post 7164:

| | `description` |
|---|---|
| In the database | `Award-winning advertising and digital marketing agency in Goa.` |
| Rendered HTML | `Award-winning advertising and <a href="https://…">Digital Marketing Agency in Goa</a>.` |

The data was never corrupt — the corruption happened at render time.

**The arithmetic matches Semrush exactly: 11 affected pages × 5 `@graph` nodes = 55 items.**

### Why the plugin's own protection failed

`split_html_tags()` had its logic in the wrong order:

1. It first split on **every individual tag** (`/(<[^>]+>)/`), which separated
   `<script …>` and `</script>` into their own parts and left the JSON body as a
   plain text part.
2. It *then* tried to protect scripts by matching `<script>…</script>` — a pattern
   that **can never match**, because step 1 had already removed the wrapper.

The protection was dead code, so the JSON body was treated as ordinary
replaceable text.

### The fix

Locate protected blocks **first**, then split only what remains.

A trap avoided: the original pattern has a *nested* capture group, and
`preg_split` with `PREG_SPLIT_DELIM_CAPTURE` emits **every** captured group — so
simply reordering the original code would have injected bare tag names such as
`script` into page content. The replacement uses `preg_match_all` with
`PREG_OFFSET_CAPTURE` and manual slicing instead.

### Verification

`test-split-html-tags.php` runs the old and new implementations side by side with
no WordPress present — **16/16 pass**:

- Old code reproduces the bug (invalid JSON) — confirms the diagnosis
- New code produces valid JSON
- New code **still auto-links body text**, so the plugin keeps working
- Reconstruction invariant holds byte-for-byte across 8 edge cases, including
  unclosed `<script>`, two scripts, `<style>`, `<pre>`, existing anchors, and
  attributes containing `>`

Live, after deployment — all 11 previously-broken pages:

```
page                                    valid invalid items links
digital-marketing-cost-goa-pricing          3       0    10    31  OK
influencer-instagram-marketing-goa          3       0    10    30  OK
email-marketing-goa-guide                   3       0    10    31  OK
digital-marketing-for-restaurants-goa       3       0    10    32  OK
local-seo-google-business-profile-goa       3       0    10    30  OK
google-ads-ppc-goa-guide                    3       0    10    30  OK
content-marketing-goa-guide                 3       0    10    31  OK
web-design-goa-websites-that-convert        3       0    10    29  OK
social-media-marketing-goa-playbook         3       0    10    31  OK
seo-services-goa-best-seo-company           3       0    10    31  OK
seo-techniques-complete-guide-2026          3       0    10    32  OK
--> pages still containing invalid JSON-LD: 0
```

Site-wide regression across 12 diverse URLs: **0 problems**, 0 invalid JSON-LD,
auto-linking still active on 12/12, no leaked tag names in visible text.

The plugin is custom (not on wordpress.org — the API returns 404), so no update
will overwrite this patch.

---

## Issue 3 — pages without a unique title

Crawled **173 URLs** (79 from `sitemap.xml` plus 94 that Semrush would reach by
following links but which the sitemap omits — categories, tags, archives).

Analysing by **final** URL rather than requested URL mattered here. One apparent
duplicate was a false positive:
`/sanctify-facility/digital-marketing-agency-goa/` already 301-redirects to
`/digital-marketing-agency-goa/`, so both were the same page.

Two genuine duplicates remained — a category and a tag sharing a name, so the
title template rendered identically:

| Term | Before | After |
|---|---|---|
| Category `Goa` (id 27) | `Goa - Best Advertising and Digital Marketing Agency in Goa` | `Goa Classifieds News & Listings \| Sanctify Goa` |
| Tag `Goa` (id 227) | *(identical to above)* | `Goa Marketing Insights & Articles \| Sanctify` |
| Category `Google` (id 53) | `Google - Best Advertising and Digital Marketing Agency in Goa` | `Google Marketing & Ads News \| Sanctify Goa` |
| Tag `Google` (id 241) | *(identical to above)* | `Google Updates & Tips \| Sanctify Goa` |

Meta descriptions were written for all four at the same time. All titles are
36–50 characters, so none truncate in SERPs.

Term-level SEO meta was not exposed to the REST API, so
`mu-sanctify-term-seo-rest.php` registers `_seopress_titles_title` and
`_seopress_titles_desc` for `category` and `post_tag`, gated on
`manage_categories`. The values live **in SEOPress**, so they remain editable in
the normal admin UI rather than being hidden inside a custom filter.

Verified live: all four rendered titles now unique, **0 duplicates remaining**.

---

## Bonus — invalid HTML in the theme header

While tracing the above, the rendered pages showed one more `</script>` than
`<script>`. Traced to `header.php`, which had **2 openers and 3 closers in
source**: line 192 was an orphaned `</script>` with no opener anywhere between
lines 69 and 192, followed by an empty `<script></script>` pair on 193–195.

Those four lines were the end of the file; the header correctly ends after
opening `content_inner` on line 190. Removed them.

This was confirmed **pre-existing and not caused by the plugin patch** — the
imbalance is visible in the theme source itself, and the patch is proven not to
add or remove any bytes.

Verified live: `/`, `/privacy-policy/`, `/case-studies/`, `/tag/goa/` all now
report balanced script tags (55/55, 44/44, 45/45, 42/42) and HTTP 200.

---

## Issue 1 — hreflang conflict: cannot reproduce

Checked exhaustively and found **zero `hreflang` attributes anywhere**:

- All 173 crawled URLs — 0 pages emit any `hreflang`
- `/page/2/`, `/feed/`, `/category/sanctify-news/page/2/`, `/?s=goa` — 0
- `sitemap.xml` contains no `xhtml:link hreflang`
- Theme `functions.php` and `header.php` contain no `hreflang`

The site is single-language with no multilingual plugin active, so there is
nothing generating the tag. Either the finding is from an older crawl, or it is on
a URL outside the set above.

**To resolve:** open that row in the Semrush report — it links to the specific
affected URL. With that URL this is a quick fix.

---

## Files

| File | Purpose |
|---|---|
| `BEFORE-auto-keyword-links.php` | Plugin before the patch. **Rollback source.** |
| `AFTER-auto-keyword-links.php` | Deployed version |
| `BEFORE-theme-header.php` | `header.php` before the patch. **Rollback source.** |
| `AFTER-theme-header.php` | Deployed version |
| `mu-sanctify-term-seo-rest.php` | mu-plugin exposing SEOPress term meta to REST |
| `test-split-html-tags.php` | Standalone 16-test proof of the parser fix |

Server-side backups, all HTTP-blocked by the `.htaccess` hardening:

```
/wp-content/plugins/auto-keyword-links-plugin/auto-keyword-links.php.pre-kiro-20260908-224731.bak
/wp-content/themes/digital-marketing/header.php.pre-kiro-20260908-225748.bak
```

## Rollback

```bash
# plugin
python3 ftps.py put BEFORE-auto-keyword-links.php \
  /wp-content/plugins/auto-keyword-links-plugin/auto-keyword-links.php

# theme header
python3 ftps.py put BEFORE-theme-header.php \
  /wp-content/themes/digital-marketing/header.php

# term titles: clear the four overrides
# POST /wp-json/wp/v2/categories/27  {"meta":{"_seopress_titles_title":""}}
# POST /wp-json/wp/v2/tags/227       {"meta":{"_seopress_titles_title":""}}
# POST /wp-json/wp/v2/categories/53  {"meta":{"_seopress_titles_title":""}}
# POST /wp-json/wp/v2/tags/241       {"meta":{"_seopress_titles_title":""}}
```

Every PHP file was checked with `php -l` before upload. This matters for an active
plugin and a mu-plugin, where a syntax error is a site-wide white screen.

## Also worth fixing — not done, needs your call

1. **Redirect chain.** Two Redirection-plugin rules point at
   `/sanctify-facility/digital-marketing-agency-goa/`, which then 301s again to
   `/digital-marketing-agency-goa/`. Two hops where one would do:
   - `/sanctify-facility/digital-marketing-agency-goa/best-digital-marketing-services-for-local-businesses-in-goa/`
   - `/sanctify-facility/best-digital-marketing-agency-goa/`
2. **27 pages have an H1 count other than 1** — 26 with two H1s and `/contact/`
   with none.
3. **Thin tag archives.** Unique titles fix the Semrush error, but tag archives
   that near-duplicate a category are usually better set to `noindex, follow`.
   That is a strategy decision, so it was not made unilaterally.
