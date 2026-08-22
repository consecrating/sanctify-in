# Hero background video — /digital-marketing-agency-goa/

| File | Role | Size |
|---|---|---|
| `hero-loop.mp4` | Magnific/Kling 2.5 Pro raw output (1660x1244, 24fps, 11.2 Mbps) | 6.77 MB |
| `loop-boomerang.mp4` | Shipped H.264 (1600px, CRF 30, faststart) | 0.67 MB |
| `loop-boomerang.webm` | Shipped VP9 (preferred by Chrome/Firefox) | 0.47 MB |

Generated with Magnific image-to-video (`kling-v2-5-pro`), seeded from
`digital-marketing-agency-goa-hero-banner.jpeg` so the video matches the poster frame.

Seamless loop via boomerang (forward + reversed concat). First-vs-last frame
mean abs difference: **1.08** (raw clip was 11.09) = visually seamless wrap.

Served from `wp-content/uploads/2026/08/` (uploaded via FTP — the WP REST
media endpoint returns 406 for video binaries, blocked by ModSecurity).

Re-encode commands are in the project history; ffmpeg via `pip install imageio-ffmpeg`.

## Local-focus section visual

The right column of "Built for Goa's local market" is a **CSS-only map-pack card**,
not an image: stylised service-area map, three ranked rows with the client at
position 1, and a tracked-position footer. Zero image weight, crisp at any DPR,
and it illustrates the four services listed in that section (GBP, location pages,
NAP, AI visibility).

Earlier candidates, both rejected:
- `nbp-local-market.png` - Nano Banana Pro 1K generation of a Goa shop owner.
  Good image, but a generic person adds no proof to a local-SEO section.
- A composite of a client-supplied portrait. Not used: subject's age could not be
  established, so it was not appropriate to publish as a commercial page centrepiece.
  All derivatives were deleted rather than committed.

Orphaned on the server (safe to delete via FTP if unwanted):
`wp-content/uploads/2026/08/local-seo-goa-business-owner.{webp,jpg}`
