#!/usr/bin/env python3
import json, base64, urllib.request, time, os

KEY="MS570b8aa3c8c34c7d9bf9ab86402c9b47"
BASE="https://api.freepik.com/v1/ai/image-upscaler"
DARK=["social-media-marketing-agency-goa","ppc-google-ads-agency-goa","digital-marketing-agency-south-goa"]

def post(slug):
    b64=base64.b64encode(open(f"_img/{slug}.jpg","rb").read()).decode()
    body=json.dumps({"image":b64,"scale_factor":"2x","optimized_for":"art_and_illustration"}).encode()
    req=urllib.request.Request(BASE,data=body,method="POST",
        headers={"x-freepik-api-key":KEY,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.load(r)["data"]["task_id"]

def poll(tid):
    req=urllib.request.Request(f"{BASE}/{tid}",headers={"x-freepik-api-key":KEY})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.load(r)["data"]

tasks={s:post(s) for s in DARK}
print("submitted:",tasks)
done={}
for _ in range(40):
    time.sleep(6)
    allok=True
    for s,tid in tasks.items():
        if s in done: continue
        d=poll(tid); st=d.get("status")
        if st=="COMPLETED" and d.get("generated"):
            url=d["generated"][0]; done[s]=url; print("DONE",s,url[:80])
        elif st in ("FAILED",):
            print("FAILED",s,d); done[s]="FAIL"
        else:
            allok=False
    if len(done)==len(tasks): break
    if not allok: print("...waiting", {s:('ok' if s in done else 'pending') for s in tasks})

for s,url in done.items():
    if url=="FAIL": continue
    raw=urllib.request.urlopen(url,timeout=120).read()
    open(f"_img/{s}-2x.jpg","wb").write(raw)
    print("saved",f"_img/{s}-2x.jpg",len(raw),"bytes")
print("done")
