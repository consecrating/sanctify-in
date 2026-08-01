#!/usr/bin/env python3
import sys, os, glob
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PREVIEW = os.path.join(HERE, "preview")
OUT = "/projects/sandbox/.kiro/artifacts/screenshots"
os.makedirs(OUT, exist_ok=True)
CHROME = glob.glob("/opt/playwright/chromium-*/chrome-linux64/chrome")[0]

FORCE = """() => {
  document.querySelectorAll('.sfy2').forEach(r=>r.classList.add('sfy-js'));
  document.querySelectorAll('.r').forEach(e=>e.classList.add('in'));
}"""

def shot(slug, device="desktop"):
    path = os.path.join(PREVIEW, slug + ".html")
    url = "file://" + path
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        vp = {"width": 1280, "height": 900} if device == "desktop" else {"width": 390, "height": 844}
        pg = b.new_page(viewport=vp, device_scale_factor=2 if device != "desktop" else 1)
        pg.goto(url, wait_until="networkidle")
        pg.wait_for_timeout(900)          # fonts
        pg.evaluate(FORCE)
        pg.wait_for_timeout(500)
        out = os.path.join(OUT, f"v2-{slug}-{device}.png")
        pg.screenshot(path=out, full_page=True)
        b.close()
        print("saved", out)

if __name__ == "__main__":
    slug = sys.argv[1]
    devices = sys.argv[2:] or ["desktop"]
    for d in devices:
        shot(slug, d)
