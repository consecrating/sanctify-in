# Root `.htaccess` — file protection hardening

Applied: 2026-09-08 via FTPS to `/.htaccess` on `ftp.sanctify.biz`

## Files

| File | Purpose |
|---|---|
| `BEFORE-htaccess.txt` | Exact copy of the live file before the change. **Rollback source.** |
| `AFTER-htaccess.txt` | Exact copy of what is live now (md5 `fff01fe07ac8560e2e525328653c9ff1`, 10594 bytes, 267 lines) |

A server-side copy also exists at `/.htaccess.pre-kiro-20260908-221606.bak` (itself blocked from HTTP).

## Why

Eight archive files totalling **3.43 GB** were publicly downloadable from the web root,
including `wp-configbackup27Feb202.php.zip` — a 2 KB zip whose central directory lists
`wp-config.php`, i.e. the database credentials. Confirmed by live HTTP range requests
returning `206 Partial Content` with full `Content-Length`.

`.htaccessold` (11,550 bytes) and `.htaccess.phpupgrader.*` were also being served in
full: this host does **not** apply the usual `^\.ht` deny that most Apache configs ship.

## What changed

One new block, `# BEGIN Sanctify File Protection`, inserted after the existing
`# END Sanctify Performance & Security` marker. Nothing else was touched — the WP Rocket
block, the WordPress block, the `sitemap.xml` rewrite and the
`E=HTTP_AUTHORIZATION` line (which is what makes REST application passwords work) are
all byte-identical to before.

| Rule | Effect |
|---|---|
| 1 | Deny `zip tar gz tgz bz2 xz 7z rar sql dump bak backup old save orig swp swo tmp log` |
| 2 | Re-allow `sitemap*.xml` / `.xml.gz` (placed after rule 1 so it wins) |
| 3 | Deny `^\.ht` — catches `.htaccessold`, `.htaccess.phpupgrader.*` |
| 4 | Deny `readme.html`, `license.txt`, `wp-config-sample.php`, `.user.ini`, `.ftpquota`, `error_log` |
| 5 | Deny `wp-config*` in any backup guise |
| 6 | `Options -Indexes` |

## Googlebot safety

The explicit requirement was that Googlebot must not be banned. The block therefore
matches **file names and extensions only**:

- No `User-Agent` matching, no `BrowserMatch`, no IP/country blocking, no rate limiting
- No `X-Robots-Tag`, no `noindex`
- CSS, JS, images, fonts, `/wp-content/uploads/`, `robots.txt`, `sitemap.xml` untouched

Verified after deployment, all as `Googlebot/2.1`:

| Check | Result |
|---|---|
| 12 pages from `sitemap.xml` | all **200** |
| Googlebot desktop + smartphone on `/` | **200** |
| `robots.txt`, `sitemap.xml` (79 URLs) | **200** |
| 8 homepage CSS/JS assets | all **200** |
| `/wp-content/uploads/` images (Image Search) | **200** |
| 8 exposed archives | all **403** |
| `.htaccessold`, `readme.html`, `wp-content/debug.log` | all **403** |
| REST auth (`/wp-json/wp/v2/users/me`) | still authenticates |
| Executable lines containing a crawler directive | **zero** |

`Options -Indexes` was proven safe first by deploying it to a throwaway
`/kiro-probe/` directory and confirming HTTP 200 — a rejected `Options` directive would
have returned 500 for the entire site. The probe directory was then removed.

## Still outstanding — needs a human

1. **The 3.43 GB of archives are still on disk**, merely unreachable over HTTP. Download
   them somewhere safe and delete them from the web root.
2. **Rotate the database password.** `wp-configbackup27Feb202.php.zip` was publicly
   downloadable for an unknown period, so those credentials must be considered
   compromised. Blocking access does not undo prior downloads.
3. `/local-seo-services-goa/` 301-redirects to `/sanctify-facility/local-seo-services-goa/`
   while `.htaccess` redirects `/sanctify-facility/digital-marketing-agency-goa/` the
   opposite way. Pre-existing, unrelated to this change, worth reconciling for SEO.

## Rollback

```bash
# from this directory, over FTPS
python3 /path/to/ftps.py put wordpress/htaccess/BEFORE-htaccess.txt /.htaccess
# or, entirely server-side, restore the timestamped copy:
#   /.htaccess.pre-kiro-20260908-221606.bak
```
