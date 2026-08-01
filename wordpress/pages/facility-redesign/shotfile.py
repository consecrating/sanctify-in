#!/usr/bin/env python3
import sys, os, glob
from playwright.sync_api import sync_playwright
CHROME = glob.glob("/opt/playwright/chromium-*/chrome-linux64/chrome")[0]
OUT = "/projects/sandbox/.kiro/artifacts/screenshots"
def shot(path, out, device="desktop"):
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox"])
        vp = {"width":1280,"height":900} if device=="desktop" else {"width":390,"height":844}
        pg = b.new_page(viewport=vp, device_scale_factor=1 if device=="desktop" else 2)
        pg.goto("file://"+os.path.abspath(path), wait_until="networkidle")
        pg.wait_for_timeout(1200)
        pg.screenshot(path=os.path.join(OUT,out), full_page=True)
        b.close(); print("saved", out)
if __name__=="__main__":
    shot(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "desktop")
