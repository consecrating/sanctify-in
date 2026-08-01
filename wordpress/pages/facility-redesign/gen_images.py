#!/usr/bin/env python3
"""Generate 6 on-brand hero images via Freepik/Magnific text-to-image, decode to _img/."""
import json, base64, urllib.request, os, time

KEY = "MS570b8aa3c8c34c7d9bf9ab86402c9b47"
URL = "https://api.freepik.com/v1/ai/text-to-image"
os.makedirs("_img", exist_ok=True)

BRAND = ("brand palette deep magenta #c20b58 and violet #7a00df, "
         "no text, no words, no letters, no logos, no watermark")

JOBS = [
    # slug, kind(light/dark), aspect, prompt
    ("social-media-marketing-agency-goa", "dark", "widescreen_16_9",
     "abstract premium background, flowing magenta and violet gradient smoke, light streaks and soft bokeh particles on a dark plum base, elegant cinematic, "+BRAND),
    ("local-seo-services-goa", "light", "square_1_1",
     "clean modern glossy 3D illustration of a glowing location map pin floating above a stylised minimal city street map, soft studio lighting, light lavender background, premium, "+BRAND),
    ("ppc-google-ads-agency-goa", "dark", "widescreen_16_9",
     "abstract premium background, dynamic magenta and violet gradient light streaks and glowing particles on dark plum, sense of speed momentum and performance, cinematic, "+BRAND),
    ("content-marketing-agency-goa", "light", "square_1_1",
     "clean modern glossy 3D illustration of stacked editorial magazines with a stylised pen and floating document pages, soft studio lighting, light background, premium minimal, "+BRAND),
    ("digital-marketing-agency-north-goa", "light", "square_1_1",
     "clean modern stylised illustration of a North Goa coastline, palm trees and boutique cafe buildings at golden hour, glossy premium, light background, magenta and violet duotone accents, "+BRAND),
    ("digital-marketing-agency-south-goa", "dark", "widescreen_16_9",
     "atmospheric South Goa beach coastline at dusk, palm tree silhouettes, calm sea, moody gradient sky, cinematic premium, magenta and violet duotone, "+BRAND),
]

def gen(prompt, aspect):
    body = json.dumps({"prompt": prompt, "aspect_ratio": aspect, "num_images": 1,
                       "styling": {"style": "photo"}}).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
        headers={"x-freepik-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return d["data"][0]["base64"]

for slug, kind, aspect, prompt in JOBS:
    for attempt in range(3):
        try:
            b64 = gen(prompt, aspect)
            raw = base64.b64decode(b64)
            path = f"_img/{slug}.jpg"
            open(path, "wb").write(raw)
            print(f"OK  {slug} ({kind},{aspect}) -> {len(raw)} bytes")
            break
        except Exception as e:
            print(f"retry {slug} attempt {attempt+1}: {e}")
            time.sleep(3)
    else:
        print(f"FAIL {slug}")
    time.sleep(1)
print("done")
