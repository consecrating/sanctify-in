#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deploy redesigned facility pages to sanctify.in via WordPress REST API."""
import os, sys, json, base64, urllib.request, urllib.error
import build  # provides build.PAGES and build.BUILD

SITE = "https://www.sanctify.in"
USER = os.environ.get("WPUSER", "kiara")
PASS = os.environ.get("WPPASS", "exTR w1a8 9fBZ CsOZ 0JzM PjOZ")
AUTH = "Basic " + base64.b64encode(f"{USER}:{PASS}".encode()).decode()

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(SITE + path, data=data, method=method)
    req.add_header("Authorization", AUTH)
    req.add_header("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36")
    req.add_header("Accept", "application/json")
    if data: req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8", "ignore") or "{}")

def deploy(slug):
    d = build.PAGES[slug]; pid = d["id"]
    content = open(os.path.join(build.BUILD, slug + ".content.html")).read()
    payload = {
        "content": content,
        "meta": {
            "_seopress_titles_title": d["meta_title"],
            "_seopress_titles_desc": d["meta_desc"],
        },
    }
    st, resp = api("POST", f"/wp-json/wp/v2/pages/{pid}", payload)
    ok = st == 200
    link = resp.get("link") if ok else None
    rlen = len(resp.get("content", {}).get("rendered", "")) if ok else 0
    mt = (resp.get("meta") or {}).get("_seopress_titles_title") if ok else None
    print(f"  [{st}] {slug} (id {pid}) -> rendered={rlen}B  meta_title={'OK' if mt else '??'}  {link or resp}")
    return ok, link

if __name__ == "__main__":
    slugs = sys.argv[1:] or list(build.PAGES.keys())
    results = []
    for s in slugs:
        results.append((s,) + deploy(s))
    print("\n== summary ==")
    for r in results:
        print("  ", "OK " if r[1] else "ERR", r[0], r[2] or "")
