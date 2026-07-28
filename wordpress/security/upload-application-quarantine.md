# Security: quarantined `Upload_Application/` — 2026-07-28

## What it was
`wp-content/plugins/Upload_Application/` — **not a WordPress plugin**. A standalone
**"UIForm – Universal Form Builder"** app (CodeIgniter 2.x, HMVC) with a bundled
**elFinder 2.0 rc1 (2012)** file manager. Modules present: formbuilder, user, visitor, activities.

## Why it was dangerous (CRITICAL)
Confirmed LIVE and reachable over HTTP (all returned 200):
- `/filemanager/php/connector.php` — **unauthenticated elFinder connector**. Verified functional
  (returned valid elFinder JSON `errFolderNotFound`). elFinder 2.0rc1 has known RCE/arbitrary-upload
  CVEs. An attacker could upload a PHP webshell into a web-served folder and execute it.
- `/install/index.php` — **live installer** ("INSTALLING UIFORM"). Re-install / config hijack risk.
- `/filemanager/elfinder.html` — file manager UI, live.

The app was **unconfigured** (empty DB credentials, empty base_url, encryption_key='test',
index.php redirects to installer) → not wired to any database, i.e. not actually in use.

## Compromise check
No webshells found. Writable dirs (`uploads/`, `filemanager/files/`) contained only elFinder's
default `.tmb` (thumbnail cache) and `.quarantine` folders. `application/logs/` empty. No WordPress
page or post references the app (zero dependency). No visible sign of prior abuse.

## Remediation (2 layers, reversible)
1. Uploaded a deny-all `.htaccess` at the app root (`Require all denied` / `Deny from all`)
   → connector, installer, filemanager all return **403**.
2. Renamed the directory:
   `Upload_Application` → `Upload_Application__QUARANTINED_kiro_20260728`
   → all original URLs now return **404**.

## Verification
- Original connector/installer/dir URLs → **404**
- Quarantined-path connector → **403** (deny-all still applies; defense in depth)
- WordPress site unaffected: homepage, DM pillar, case-studies all **200**

## Rollback
Rename the directory back and remove the deny-all `.htaccess`. Files are intact on the server
under the quarantined name.

## Recommended next step (owner decision)
**Permanently delete** the quarantined directory — it is unconfigured, unused, not a WP plugin,
and nothing depends on it. If the form-builder is ever needed, reinstall a current, patched
version *outside* wp-content/plugins and behind authentication, and never leave `install/` or an
open elFinder connector reachable.

## Related
This is the same class of issue as `sitemap-to-urllist.php` (an unauthenticated upload form,
disabled in the sitemap/robots cleanup) and the loose plugin zips flagged earlier. A full
security sweep of the web root is recommended.
