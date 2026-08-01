#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanctify Facility / Landing pages - v2 premium redesign generator.

Produces, per page:
  build/<slug>.content.html   -> the exact HTML to POST to WP page content
  preview/<slug>.html         -> a standalone preview (mock header/footer + content) for screenshotting

Design system namespace: .sfy2  (self-contained, does not depend on the site's
global inline <style id="sanctify-svc-css"> block; new namespace = no collisions).
Robust reveal: content is visible by default; JS only *enhances* with a subtle
entrance. No-JS / crawlers see everything.
"""
import os, html, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
PREVIEW = os.path.join(HERE, "preview")
os.makedirs(BUILD, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

SITE = "https://www.sanctify.in"

# ---------------------------------------------------------------------------
# Fonts + CSS
# ---------------------------------------------------------------------------
FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&'
    'family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

CSS = r"""
<style id="sfy2-css">
.sfy2{
  --pink:#ff0066; --mag:#c8177f; --vio:#6d28d9; --grape:#4c1d95;
  --ink:#140b22; --body:#4b445c; --muted:#7a7388;
  --line:rgba(20,11,34,.09); --line2:rgba(20,11,34,.06);
  --paper:#ffffff; --mist:#f7f2fb; --mist2:#efe7f7;
  --grad:linear-gradient(120deg,#ff0066 0%,#d21a86 45%,#7b2ff7 100%);
  --grad-soft:linear-gradient(120deg,#ff0066,#7b2ff7);
  --r:22px; --r-lg:30px; --maxw:1160px;
  --shadow:0 1px 2px rgba(20,11,34,.05),0 18px 40px -22px rgba(76,29,149,.35);
  --shadow-hi:0 30px 70px -30px rgba(200,23,127,.5);
  font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  color:var(--body); line-height:1.65; font-size:17px;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
.sfy2 *{box-sizing:border-box}
.sfy2 h1,.sfy2 h2,.sfy2 h3,.sfy2 h4{font-family:'Sora',var(--sfy-fallback,inherit);color:var(--ink);
  line-height:1.08;letter-spacing:-.02em;margin:0 0 .4em;font-weight:800}
.sfy2 p{margin:0 0 1em}
.sfy2 a{color:inherit;text-decoration:none}
.sfy2 img,.sfy2 svg{display:block;max-width:100%}
.sfy-wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}
.sfy-sec{padding:74px 0}
.sfy-grad-txt{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}

/* ---- buttons ---- */
.sfy-btn{display:inline-flex;align-items:center;gap:.55em;font-weight:700;font-size:15.5px;
  padding:15px 28px;border-radius:999px;transition:.28s cubic-bezier(.2,.7,.3,1);cursor:pointer;
  border:1px solid transparent;letter-spacing:.01em;white-space:nowrap}
.sfy-btn svg{width:18px;height:18px}
.sfy-btn.p{background:var(--grad);color:#fff;box-shadow:0 12px 26px -10px rgba(255,0,102,.6)}
.sfy-btn.p:hover{transform:translateY(-2px);box-shadow:0 20px 40px -12px rgba(255,0,102,.7)}
.sfy-btn.g{background:rgba(255,255,255,.7);color:var(--ink);border-color:var(--line);backdrop-filter:blur(6px)}
.sfy-btn.g:hover{border-color:var(--pink);color:var(--pink);transform:translateY(-2px)}
.sfy-btn.w{background:#fff;color:var(--ink)}
.sfy-btn.w:hover{transform:translateY(-2px);box-shadow:0 16px 34px -14px rgba(0,0,0,.4)}
.sfy-btn.o{background:transparent;color:#fff;border-color:rgba(255,255,255,.5)}
.sfy-btn.o:hover{background:rgba(255,255,255,.12);border-color:#fff}

/* ---- chips / eyebrow ---- */
.sfy-eyebrow{display:inline-flex;align-items:center;gap:9px;font-weight:700;font-size:12.5px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--mag);
  background:rgba(255,0,102,.08);border:1px solid rgba(255,0,102,.18);
  padding:8px 16px;border-radius:999px}
.sfy-eyebrow .dot{width:8px;height:8px;border-radius:50%;background:var(--grad);
  box-shadow:0 0 0 4px rgba(255,0,102,.15)}

/* ---- HERO ---- */
.sfy-hero{position:relative;border-radius:var(--r-lg);overflow:hidden;margin-top:26px;
  background:
    radial-gradient(120% 120% at 88% -10%,rgba(123,47,247,.20),transparent 55%),
    radial-gradient(120% 130% at 6% 4%,rgba(255,0,102,.16),transparent 52%),
    radial-gradient(90% 90% at 55% 120%,rgba(123,47,247,.12),transparent 60%),
    linear-gradient(180deg,#fdf9ff,#f4ecfb);
  border:1px solid rgba(123,47,247,.12);
  box-shadow:0 40px 90px -50px rgba(76,29,149,.5)}
.sfy-hero::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.5;
  background-image:radial-gradient(rgba(20,11,34,.05) 1px,transparent 1px);background-size:22px 22px;
  -webkit-mask-image:linear-gradient(180deg,#000,transparent 70%);mask-image:linear-gradient(180deg,#000,transparent 70%)}
.sfy-hero-in{position:relative;display:grid;grid-template-columns:1.05fr .95fr;gap:46px;align-items:center;
  padding:60px 56px 64px}
.sfy-hero h1{font-size:clamp(34px,5vw,58px);font-weight:800;margin:18px 0 0}
.sfy-hero .lead{font-size:clamp(16px,1.5vw,19px);color:var(--body);margin:20px 0 30px;max-width:34em}
.sfy-hero-cta{display:flex;gap:14px;flex-wrap:wrap}
.sfy-hero-trust{display:flex;align-items:center;gap:14px;margin-top:26px;flex-wrap:wrap}
.sfy-stars{display:inline-flex;gap:2px;color:#ff9d00}
.sfy-stars svg{width:17px;height:17px}
.sfy-hero-trust small{color:var(--muted);font-size:13.5px;font-weight:500}
.sfy-hero-trust b{color:var(--ink)}

/* ---- device: shared glass ---- */
.sfy-art{position:relative;display:flex;justify-content:center;align-items:center;min-height:340px}
.sfy-glass{position:relative;background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.9);
  border-radius:22px;box-shadow:var(--shadow),0 40px 80px -40px rgba(76,29,149,.55);
  backdrop-filter:blur(14px)}
.sfy-float{position:absolute;background:#fff;border:1px solid var(--line);border-radius:14px;
  box-shadow:0 20px 40px -18px rgba(20,11,34,.35);padding:11px 14px;display:flex;align-items:center;gap:9px;
  font-size:13px;font-weight:700;color:var(--ink);animation:sfy-bob 5s ease-in-out infinite}
.sfy-float .fi{width:30px;height:30px;border-radius:9px;display:grid;place-items:center;color:#fff}
.sfy-float svg{width:16px;height:16px}
@keyframes sfy-bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}

/* phone (SMM) */
.sfy-phone{width:270px;height:540px;border-radius:44px;background:linear-gradient(160deg,#1b1030,#0e0720);
  padding:12px;box-shadow:0 50px 90px -40px rgba(20,11,34,.7),inset 0 0 0 2px rgba(255,255,255,.06);position:relative}
.sfy-phone::after{content:"";position:absolute;top:20px;left:50%;transform:translateX(-50%);
  width:96px;height:22px;background:#0e0720;border-radius:0 0 16px 16px;z-index:3}
.sfy-scr{position:relative;height:100%;border-radius:34px;overflow:hidden;background:#fff;display:flex;flex-direction:column}
.sfy-ptop{display:flex;align-items:center;gap:9px;padding:14px 12px 10px}
.sfy-pav{width:34px;height:34px;border-radius:50%;background:var(--grad);flex:0 0 auto;
  box-shadow:0 0 0 2px #fff,0 0 0 4px rgba(255,0,102,.4)}
.sfy-ptop b{font-size:13px;color:var(--ink);display:block;line-height:1.1}
.sfy-ptop small{font-size:11px;color:var(--muted)}
.sfy-pimg{flex:1;background:
    radial-gradient(90% 70% at 30% 20%,rgba(255,0,102,.5),transparent 60%),
    linear-gradient(150deg,#ff5aa8,#a34bff 60%,#6d28d9);position:relative}
.sfy-play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:56px;height:56px;border-radius:50%;
  background:rgba(255,255,255,.9);display:grid;place-items:center;box-shadow:0 10px 24px -8px rgba(0,0,0,.4)}
.sfy-play::after{content:"";width:0;height:0;margin-left:4px;border-left:16px solid #6d28d9;
  border-top:10px solid transparent;border-bottom:10px solid transparent}
.sfy-pact{display:flex;gap:16px;padding:12px 14px;color:var(--ink)}
.sfy-pact svg{width:22px;height:22px}
.sfy-pcap{padding:0 14px 16px;font-size:12px;color:var(--body);line-height:1.4}
.sfy-pcap b{color:var(--ink)}

/* map card (Local SEO / city) */
.sfy-mapcard{width:360px;max-width:100%;overflow:hidden}
.sfy-map{height:196px;position:relative;
  background:
   linear-gradient(90deg,rgba(123,47,247,.10) 1px,transparent 1px) 0 0/40px 40px,
   linear-gradient(rgba(123,47,247,.10) 1px,transparent 1px) 0 0/40px 40px,
   radial-gradient(140% 120% at 70% 20%,#efe7fb,#e5f6ef);}
.sfy-road{position:absolute;background:#fff;box-shadow:0 0 0 1px rgba(20,11,34,.05)}
.sfy-road.r1{height:12px;left:-10px;right:-10px;top:64px;transform:rotate(-6deg)}
.sfy-road.r2{width:14px;top:-10px;bottom:-10px;left:120px;transform:rotate(8deg)}
.sfy-road.r3{height:9px;left:-10px;right:-10px;top:132px;transform:rotate(3deg)}
.sfy-pin{position:absolute;top:58px;left:150px;width:34px;height:34px;transform:translate(-50%,-100%);
  background:var(--grad);border-radius:50% 50% 50% 0;rotate:-45deg;
  box-shadow:0 10px 20px -6px rgba(255,0,102,.7);display:grid;place-items:center}
.sfy-pin::after{content:"";width:11px;height:11px;background:#fff;border-radius:50%}
.sfy-pin.p2{top:120px;left:250px;width:22px;height:22px;opacity:.55}
.sfy-pin.p3{top:150px;left:70px;width:22px;height:22px;opacity:.45}
.sfy-pack{padding:14px 16px 16px;background:#fff}
.sfy-pack h5{font-family:'Sora';font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.sfy-prow{display:flex;align-items:center;gap:11px;padding:9px 0;border-top:1px solid var(--line2)}
.sfy-prow:first-of-type{border-top:0}
.sfy-prank{width:26px;height:26px;border-radius:8px;display:grid;place-items:center;font-weight:800;font-size:13px;flex:0 0 auto;
  font-family:'Sora'}
.sfy-prow.top .sfy-prank{background:var(--grad);color:#fff}
.sfy-prow:not(.top) .sfy-prank{background:var(--mist);color:var(--muted)}
.sfy-prow .nm{font-weight:700;color:var(--ink);font-size:13.5px;line-height:1.2}
.sfy-prow .rt{font-size:11.5px;color:var(--muted)}
.sfy-prow .rt b{color:#ff9d00}

/* google ads card (PPC) */
.sfy-adcard{width:370px;max-width:100%;padding:18px}
.sfy-searchbar{display:flex;align-items:center;gap:10px;border:1px solid var(--line);border-radius:999px;padding:10px 16px;
  box-shadow:0 6px 16px -10px rgba(20,11,34,.3);background:#fff}
.sfy-searchbar .q{font-weight:600;color:var(--ink);font-size:14px}
.sfy-gdot{width:14px;height:14px;border-radius:50%;
  background:conic-gradient(#4285F4 0 25%,#EA4335 0 50%,#FBBC05 0 75%,#34A853 0)}
.sfy-adres{margin-top:16px;border:1px solid var(--line);border-radius:14px;padding:14px}
.sfy-adtag{display:inline-block;font-weight:800;font-size:11px;color:#0a7d33;margin-right:8px}
.sfy-adres .u{font-size:12px;color:var(--muted)}
.sfy-adres .t{color:#1a0dab;font-weight:700;font-size:15px;margin:3px 0}
.sfy-adres .d{font-size:12.5px;color:var(--body);margin:0}
.sfy-adstats{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px}
.sfy-adstat{background:var(--mist);border-radius:12px;padding:12px 14px}
.sfy-adstat b{font-family:'Sora';font-size:22px;color:var(--ink);display:block}
.sfy-adstat span{font-size:11.5px;color:var(--muted);font-weight:600}
.sfy-bars{display:flex;align-items:flex-end;gap:6px;height:44px;margin-top:12px}
.sfy-bars i{flex:1;background:var(--grad);border-radius:5px 5px 0 0;opacity:.85}

/* serp/content card */
.sfy-serpcard{width:372px;max-width:100%;padding:18px}
.sfy-serprow{display:flex;gap:12px;align-items:flex-start;padding:12px;border-radius:14px}
.sfy-serprow.win{background:linear-gradient(120deg,rgba(255,0,102,.07),rgba(123,47,247,.07));
  border:1px solid rgba(123,47,247,.16)}
.sfy-serprk{width:28px;height:28px;border-radius:8px;background:var(--grad);color:#fff;display:grid;place-items:center;
  font-weight:800;font-family:'Sora';font-size:13px;flex:0 0 auto}
.sfy-serprow:not(.win) .sfy-serprk{background:var(--mist);color:var(--muted)}
.sfy-serprow .st{font-size:12px;color:#1a0dab;font-weight:700}
.sfy-serprow.win .st{color:var(--ink)}
.sfy-serprow .sl{height:7px;background:var(--line);border-radius:5px;margin-top:7px;width:90%}
.sfy-serprow .sl.s2{width:64%;margin-top:6px}
.sfy-spark{margin-top:14px;background:var(--mist);border-radius:14px;padding:12px 14px}
.sfy-spark .lab{display:flex;justify-content:space-between;font-size:11.5px;color:var(--muted);font-weight:600;margin-bottom:8px}
.sfy-spark .lab b{font-family:'Sora';font-size:18px;color:var(--ink)}

/* ---- marquee ---- */
.sfy-marq{overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);
  margin-top:0;padding:16px 0;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);
  mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.sfy-marq .tr{display:inline-flex;gap:0;white-space:nowrap;animation:sfy-marq 28s linear infinite;font-weight:700;
  color:var(--ink);font-size:15px}
.sfy-marq .tr span{padding:0 22px;display:inline-flex;align-items:center;gap:22px}
.sfy-marq .tr b{color:var(--pink)}
@keyframes sfy-marq{to{transform:translateX(-50%)}}

/* ---- trusted-by ---- */
.sfy-trust{text-align:center}
.sfy-trust .cap{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:700;margin-bottom:18px}
.sfy-logos{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}
.sfy-logo{font-family:'Sora';font-weight:700;color:var(--ink);opacity:.72;font-size:15px;
  border:1px solid var(--line);border-radius:999px;padding:9px 18px;background:#fff;transition:.25s}
.sfy-logo:hover{opacity:1;border-color:rgba(255,0,102,.3);transform:translateY(-2px)}

/* ---- section head ---- */
.sfy-head{max-width:720px;margin:0 auto 44px;text-align:center}
.sfy-kicker{display:inline-block;font-weight:700;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--mag);margin-bottom:14px}
.sfy-head h2{font-size:clamp(28px,3.6vw,42px)}
.sfy-head p{font-size:17px;color:var(--body);margin:14px 0 0}
.sfy-head.left{margin-left:0;text-align:left}

/* ---- bento / service grid ---- */
.sfy-bento{display:grid;grid-template-columns:repeat(6,1fr);gap:18px}
.sfy-tile{grid-column:span 2;background:var(--paper);border:1px solid var(--line);border-radius:var(--r);
  padding:26px;position:relative;overflow:hidden;transition:.3s cubic-bezier(.2,.7,.3,1)}
.sfy-tile:hover{transform:translateY(-6px);border-color:rgba(123,47,247,.22);box-shadow:var(--shadow-hi)}
.sfy-tile.feat{grid-column:span 3;grid-row:span 2;color:#fff;border:0;
  background:linear-gradient(150deg,#ff0066,#c8177f 45%,#6d28d9)}
.sfy-tile.feat h3,.sfy-tile.feat p{color:#fff}
.sfy-tile.feat .sfy-ic{background:rgba(255,255,255,.16);color:#fff;border-color:rgba(255,255,255,.25)}
.sfy-tile.wide{grid-column:span 3}
.sfy-badge{position:absolute;top:18px;right:18px;font-size:10.5px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;background:rgba(255,255,255,.2);color:#fff;padding:6px 11px;border-radius:999px}
.sfy-ic{width:52px;height:52px;border-radius:15px;display:grid;place-items:center;margin-bottom:18px;
  background:linear-gradient(150deg,rgba(255,0,102,.12),rgba(123,47,247,.12));
  color:var(--pink);border:1px solid rgba(255,0,102,.14)}
.sfy-ic svg{width:26px;height:26px}
.sfy-tile h3{font-size:19px;margin:0 0 8px}
.sfy-tile.feat h3{font-size:26px}
.sfy-tile p{font-size:14.5px;color:var(--body);margin:0}
.sfy-tile.feat p{font-size:15.5px;color:rgba(255,255,255,.9)}
.sfy-tile .spacer{flex:1}

/* ---- metrics ---- */
.sfy-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;
  background:linear-gradient(120deg,#fff,var(--mist));border:1px solid var(--line);
  border-radius:var(--r-lg);padding:38px 30px;box-shadow:var(--shadow)}
.sfy-metric{text-align:center;position:relative}
.sfy-metric+.sfy-metric::before{content:"";position:absolute;left:-10px;top:14%;height:72%;width:1px;background:var(--line)}
.sfy-metric b{font-family:'Sora';font-size:clamp(30px,4vw,46px);line-height:1;display:block;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;font-weight:800}
.sfy-metric span{font-size:13.5px;color:var(--muted);font-weight:600;margin-top:8px;display:block}

/* ---- why / feature cards ---- */
.sfy-why{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.sfy-wcard{display:flex;gap:16px;background:var(--paper);border:1px solid var(--line);border-radius:var(--r);padding:22px 24px;transition:.3s}
.sfy-wcard:hover{border-color:rgba(123,47,247,.22);box-shadow:var(--shadow);transform:translateY(-3px)}
.sfy-chk{width:42px;height:42px;border-radius:12px;flex:0 0 auto;display:grid;place-items:center;color:#fff;background:var(--grad)}
.sfy-chk svg{width:22px;height:22px}
.sfy-wcard b{font-family:'Sora';font-size:17px;color:var(--ink);display:block;margin-bottom:4px}
.sfy-wcard span{font-size:14.5px;color:var(--body)}

/* ---- process ---- */
.sfy-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;position:relative}
.sfy-steps::before{content:"";position:absolute;top:26px;left:8%;right:8%;height:2px;
  background:linear-gradient(90deg,var(--pink),var(--vio));opacity:.35}
.sfy-step{position:relative;text-align:left}
.sfy-snum{width:54px;height:54px;border-radius:16px;background:#fff;border:1px solid var(--line);
  display:grid;place-items:center;font-family:'Sora';font-weight:800;font-size:20px;color:var(--pink);
  box-shadow:var(--shadow);margin-bottom:18px;position:relative}
.sfy-snum::after{content:"";position:absolute;inset:-1px;border-radius:16px;padding:1px;
  background:var(--grad);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;opacity:.5}
.sfy-step h4{font-size:17px;margin:0 0 6px}
.sfy-step p{font-size:14px;color:var(--body);margin:0}

/* ---- FAQ ---- */
.sfy-faq{max-width:820px;margin:0 auto;display:flex;flex-direction:column;gap:12px}
.sfy-q{background:var(--paper);border:1px solid var(--line);border-radius:16px;overflow:hidden;transition:.25s}
.sfy-q[open]{border-color:rgba(123,47,247,.28);box-shadow:var(--shadow)}
.sfy-q summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;
  padding:19px 22px;font-family:'Sora';font-weight:700;color:var(--ink);font-size:16px}
.sfy-q summary::-webkit-details-marker{display:none}
.sfy-qi{width:30px;height:30px;border-radius:9px;flex:0 0 auto;display:grid;place-items:center;background:var(--mist);color:var(--pink);transition:.3s}
.sfy-qi svg{width:18px;height:18px}
.sfy-q[open] .sfy-qi{background:var(--grad);color:#fff;transform:rotate(135deg)}
.sfy-a{padding:0 22px 20px;font-size:15px;color:var(--body)}
.sfy-a p{margin:0}

/* ---- CTA band ---- */
.sfy-cta{position:relative;overflow:hidden;border-radius:var(--r-lg);padding:64px 40px;text-align:center;color:#fff;
  background:radial-gradient(120% 130% at 12% 0%,rgba(255,0,102,.55),transparent 55%),
    radial-gradient(120% 130% at 90% 100%,rgba(123,47,247,.6),transparent 55%),
    linear-gradient(140deg,#2a0f3f,#160a26)}
.sfy-cta::before{content:"";position:absolute;inset:0;opacity:.35;
  background-image:radial-gradient(rgba(255,255,255,.14) 1px,transparent 1px);background-size:24px 24px}
.sfy-cta h2{position:relative;color:#fff;font-size:clamp(26px,3.4vw,40px)}
.sfy-cta p{position:relative;color:rgba(255,255,255,.82);font-size:17px;max-width:36em;margin:14px auto 26px}
.sfy-cta .sfy-hero-cta{position:relative;justify-content:center}
.sfy-cta .mini{font-size:14px;color:rgba(255,255,255,.72);margin-top:22px}
.sfy-cta .mini a{color:#fff;text-decoration:underline;text-underline-offset:3px;text-decoration-color:rgba(255,255,255,.4)}

/* ---- reveal (visible by default; JS enhances) ---- */
.sfy2.sfy-js .r{opacity:0;transform:translateY(22px)}
.sfy2.sfy-js .r.in{opacity:1;transform:none;transition:opacity .7s ease,transform .7s cubic-bezier(.2,.7,.3,1)}
@media (prefers-reduced-motion:reduce){
  .sfy2.sfy-js .r{opacity:1;transform:none}
  .sfy-float,.sfy-marq .tr{animation:none}
}

/* ---- responsive ---- */
@media(max-width:900px){
  .sfy-hero-in{grid-template-columns:1fr;gap:34px;padding:44px 30px 48px}
  .sfy-art{min-height:0;order:2}
  .sfy-bento{grid-template-columns:repeat(2,1fr)}
  .sfy-tile,.sfy-tile.feat,.sfy-tile.wide{grid-column:span 1;grid-row:auto}
  .sfy-tile.feat{grid-column:span 2}
  .sfy-metrics{grid-template-columns:repeat(2,1fr);gap:26px}
  .sfy-metric+.sfy-metric::before{display:none}
  .sfy-why{grid-template-columns:1fr}
  .sfy-steps{grid-template-columns:repeat(2,1fr)}
  .sfy-steps::before{display:none}
}
@media(max-width:560px){
  .sfy2{font-size:16px}
  .sfy-sec{padding:52px 0}
  .sfy-hero-in{padding:34px 20px 40px}
  .sfy-bento{grid-template-columns:1fr}
  .sfy-tile.feat{grid-column:span 1}
  .sfy-steps{grid-template-columns:1fr}
  .sfy-hero-cta .sfy-btn{flex:1;justify-content:center}
}
</style>
"""

JS = r"""
<script>
(function(){
  var root=document.currentScript&&document.currentScript.closest?document.currentScript.parentNode.querySelector('.sfy2'):document.querySelector('.sfy2');
  root=document.querySelector('.sfy2');
  if(!root||root.dataset.sfyInit)return; root.dataset.sfyInit='1';
  root.classList.add('sfy-js');
  // reveal
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.12,rootMargin:'0px 0px -8% 0px'});
  root.querySelectorAll('.r').forEach(function(el){io.observe(el);});
  // count-up
  function ease(t){return 1-Math.pow(1-t,3);}
  var cio=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return; cio.unobserve(e.target);
    var el=e.target,raw=el.getAttribute('data-to'),num=parseFloat(raw),suf=el.getAttribute('data-suf')||'',dec=(raw.split('.')[1]||'').length,t0=null,dur=1400;
    function step(ts){if(!t0)t0=ts;var p=Math.min((ts-t0)/dur,1),v=num*ease(p);el.textContent=(dec?v.toFixed(dec):Math.round(v))+suf;if(p<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  });},{threshold:.5});
  root.querySelectorAll('[data-to]').forEach(function(el){cio.observe(el);});
})();
</script>
"""

# ---------------------------------------------------------------------------
# Icons (stroke, consistent) + solid where noted
# ---------------------------------------------------------------------------
def _svg(inner, fill=False):
    if fill:
        return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">%s</svg>' % inner
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>') % inner

ICON = {
 "target": _svg('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>'),
 "spark":  _svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>'),
 "chart":  _svg('<path d="M4 4v16h16"/><path d="M7 14l3-3 3 3 5-6"/>'),
 "chat":   _svg('<path d="M21 12a8 8 0 0 1-11.5 7.2L4 21l1.8-5.5A8 8 0 1 1 21 12z"/>'),
 "users":  _svg('<circle cx="9" cy="8" r="3.4"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><path d="M16 5.2a3.4 3.4 0 0 1 0 6.4M21 20c0-2.6-1.4-4.5-3.5-5.2"/>'),
 "camera": _svg('<rect x="3" y="6" width="18" height="14" rx="3"/><circle cx="12" cy="13" r="3.4"/><path d="M8 6l1.5-2h5L16 6"/>'),
 "pin":    _svg('<path d="M20 10c0 5.5-8 12-8 12s-8-6.5-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="2.8"/>'),
 "search": _svg('<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>'),
 "list":   _svg('<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>'),
 "star":   _svg('<path d="M12 3l2.7 5.8 6.3.7-4.7 4.3 1.3 6.2L12 17.8 6.1 20.9l1.3-6.2L2.7 9.5l6.3-.7z"/>'),
 "page":   _svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
 "trend":  _svg('<path d="M3 17l6-6 4 4 8-8"/><path d="M21 7v5h-5"/>'),
 "check":  _svg('<path d="M20 6L9 17l-5-5"/>'),
 "phone":  _svg('<path d="M4 5c0-1 .8-2 2-2h2.3c.5 0 .9.3 1 .8l1 3.3c.1.5 0 1-.4 1.3L8.4 11a13 13 0 0 0 4.6 4.6l1.6-1.5c.3-.4.8-.5 1.3-.4l3.3 1c.5.1.8.5.8 1V18c0 1.2-.9 2-2 2A16 16 0 0 1 4 5z"/>'),
 "mail":   _svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 7l8 5 8-5"/>'),
 "cal":    _svg('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>'),
 "rocket": _svg('<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2M9 11a10 10 0 0 1 8-8c1 0 2 0 2 2a10 10 0 0 1-8 8"/><path d="M9 11l4 4M8.5 14.5L6 14l1-2M9.5 15.5l.5 2.5 2-1"/><circle cx="14.5" cy="9.5" r="1.3"/>'),
 "google": _svg('<path d="M21 12.2c0-.7-.1-1.4-.2-2H12v3.8h5.1a4.4 4.4 0 0 1-1.9 2.9v2.4h3.1c1.8-1.7 2.7-4.1 2.7-7.1z" fill="currentColor" stroke="none"/><path d="M12 21c2.5 0 4.6-.8 6.1-2.3l-3.1-2.4c-.9.6-2 .9-3 .9-2.3 0-4.3-1.6-5-3.7H3.8v2.4A9 9 0 0 0 12 21z" fill="currentColor" stroke="none"/><path d="M7 13.5a5.4 5.4 0 0 1 0-3.4V7.7H3.8a9 9 0 0 0 0 8.1z" fill="currentColor" stroke="none"/><path d="M12 6.4c1.3 0 2.5.5 3.4 1.4l2.6-2.6A9 9 0 0 0 3.8 7.7L7 10.1c.8-2.1 2.7-3.7 5-3.7z" fill="currentColor" stroke="none"/>'),
 "doc":    _svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 12h6M9 16h6"/>'),
 "link":   _svg('<path d="M10 13a5 5 0 0 0 7 0l2-2a5 5 0 0 0-7-7l-1 1"/><path d="M14 11a5 5 0 0 0-7 0l-2 2a5 5 0 0 0 7 7l1-1"/>'),
 "mega":   _svg('<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1z"/><path d="M15 8a5 5 0 0 1 0 8M18 5a9 9 0 0 1 0 14"/>'),
 "gauge":  _svg('<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 14l4-4"/><circle cx="12" cy="18" r="1.2" fill="currentColor" stroke="none"/>'),
 "bulb":   _svg('<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>'),
 "shield": _svg('<path d="M12 3l8 3v6c0 4.5-3.2 7.6-8 9-4.8-1.4-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>'),
 "compass":_svg('<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z" fill="currentColor" stroke="none"/>'),
 "pen":    _svg('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>'),
 "map":    _svg('<path d="M9 4L3 6v14l6-2 6 2 6-2V4l-6 2-6-2z"/><path d="M9 4v14M15 6v14"/>'),
 "clock":  _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 "cart":   _svg('<circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/><path d="M3 4h2l2.2 11.2a1 1 0 0 0 1 .8h8.4a1 1 0 0 0 1-.8L20 8H6"/>'),
 "heart":  _svg('<path d="M12 21s-7-4.4-9.5-8.5C.5 9 2 5.5 5.5 5.5c2 0 3.2 1.2 3.9 2.3.7-1.1 1.9-2.3 3.9-2.3C16.8 5.5 18.3 9 16.5 12.5 14 16.6 12 21 12 21z"/>', fill=True),
}
print("framework loaded: icons=%d" % len(ICON))



# ---------------------------------------------------------------------------
# Component renderers
# ---------------------------------------------------------------------------
def ic(name):
    return '<span class="sfy-ic">%s</span>' % ICON[name]

def hero(d):
    trust = d.get("hero_trust", "Since 2012 · Vasco &amp; Panjim, Goa")
    stars = '<span class="sfy-stars">%s</span>' % (ICON["star"] * 5)
    return f'''
<section class="sfy-hero r">
  <div class="sfy-hero-in">
    <div class="sfy-hero-left">
      <span class="sfy-eyebrow"><span class="dot"></span>{d["eyebrow"]}</span>
      <h1>{d["h1"]}</h1>
      <p class="lead">{d["lead"]}</p>
      <div class="sfy-hero-cta">
        <a class="sfy-btn p" href="{SITE}/contact/">{ICON["rocket"]}{d.get("cta1","Get a Free Proposal")}</a>
        <a class="sfy-btn g" href="#sfy-work">{d.get("cta2","See What We Do")}</a>
      </div>
      <div class="sfy-hero-trust">{stars}<small><b>4.9/5</b> client rating &nbsp;·&nbsp; {trust}</small></div>
    </div>
    <div class="sfy-art">{d["art"]}</div>
  </div>
</section>'''

def marquee(items):
    row = '<span>' + '<b>•</b>'.join(f'&nbsp;{i}&nbsp;' for i in items) + '<b>•</b></span>'
    return f'<div class="sfy-marq"><div class="tr">{row}{row}</div></div>'

def trust(names):
    chips = ''.join(f'<span class="sfy-logo">{n}</span>' for n in names)
    return f'''
<section class="sfy-sec"><div class="sfy-wrap sfy-trust r">
  <div class="cap">Trusted by brands across Goa &amp; beyond &mdash; since 2012</div>
  <div class="sfy-logos">{chips}</div>
</div></section>'''

def head(kicker, h2, sub=None):
    s = f'<p>{sub}</p>' if sub else ''
    return f'<div class="sfy-head r"><span class="sfy-kicker">{kicker}</span><h2>{h2}</h2>{s}</div>'

def bento(d):
    tiles = []
    feat = d["services"][0]
    tiles.append(f'''<div class="sfy-tile feat r"><span class="sfy-badge">Most requested</span>
      {ic(feat["icon"])}<h3>{feat["t"]}</h3><p>{feat["d"]}</p></div>''')
    for s in d["services"][1:]:
        cls = "sfy-tile r" + (" wide" if s.get("wide") else "")
        tiles.append(f'<div class="{cls}">{ic(s["icon"])}<h3>{s["t"]}</h3><p>{s["d"]}</p></div>')
    return f'''
<section class="sfy-sec" id="sfy-work"><div class="sfy-wrap">
  {head(d["svc_kicker"], d["svc_h2"], d["svc_sub"])}
  <div class="sfy-bento">{''.join(tiles)}</div>
</div></section>'''

def metrics(items):
    cells = ''
    for val, lab in items:
        m = re.match(r'^([\d.]+)(.*)$', val)
        if m:
            num, suf = m.group(1), m.group(2)
            b = f'<b data-to="{num}" data-suf="{html.escape(suf)}">{html.escape(val)}</b>'
        else:
            b = f'<b>{val}</b>'
        cells += f'<div class="sfy-metric">{b}<span>{lab}</span></div>'
    return f'<section class="sfy-sec"><div class="sfy-wrap"><div class="sfy-metrics r">{cells}</div></div></section>'

def why(d):
    cards = ''
    for w in d["why"]:
        cards += f'''<div class="sfy-wcard r"><span class="sfy-chk">{ICON["check"]}</span>
          <span><b>{w["t"]}</b><span>{w["d"]}</span></span></div>'''
    return f'''<section class="sfy-sec"><div class="sfy-wrap">
      {head(d["why_kicker"], d["why_h2"], d.get("why_sub"))}
      <div class="sfy-why">{cards}</div></div></section>'''

def process(d):
    steps = ''
    for i, s in enumerate(d["process"], 1):
        steps += f'<div class="sfy-step r"><div class="sfy-snum">{i}</div><h4>{s["t"]}</h4><p>{s["d"]}</p></div>'
    return f'''<section class="sfy-sec"><div class="sfy-wrap">
      {head(d["proc_kicker"], d["proc_h2"], d.get("proc_sub"))}
      <div class="sfy-steps">{steps}</div></div></section>'''

def faq(d):
    qs = ''
    for q in d["faq"]:
        qs += f'''<details class="sfy-q"><summary>{q["q"]}<span class="sfy-qi">{ICON["spark"] if False else '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>'}</span></summary>
        <div class="sfy-a"><p>{q["a"]}</p></div></details>'''
    return f'''<section class="sfy-sec"><div class="sfy-wrap">
      {head("FAQ", d["faq_h2"], d.get("faq_sub"))}
      <div class="sfy-faq">{qs}</div></div></section>'''

def cta(d):
    rel = ''
    if d.get("related"):
        links = ' · '.join(f'<a href="{u}">{t}</a>' for t, u in d["related"])
        rel = f'<p class="mini">Related: {links}</p>'
    return f'''<section class="sfy-sec"><div class="sfy-wrap"><div class="sfy-cta r">
      <h2>{d["cta_h2"]}</h2><p>{d["cta_sub"]}</p>
      <div class="sfy-hero-cta">
        <a class="sfy-btn w" href="{SITE}/contact/">{d.get("cta_b1","Get a Free Proposal")}</a>
        <a class="sfy-btn o" href="{SITE}/sanctify-facility/">{d.get("cta_b2","View All Services")}</a>
      </div>{rel}</div></div></section>'''

def schema(d, url):
    graph = [{
        "@type": "Service", "@id": url + "#service", "name": d["schema_name"],
        "serviceType": d["schema_name"], "url": url,
        "areaServed": {"@type": "Place", "name": d.get("area", "Goa, India")},
        "provider": {"@type": "Organization", "name": "Sanctify",
                     "url": SITE + "/", "areaServed": "Goa, India"},
        "description": d["meta_desc"],
    }, {
        "@type": "FAQPage", "@id": url + "#faq",
        "mainEntity": [{"@type": "Question", "name": q["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', q["a"])}}
                       for q in d["faq"]],
    }, {
        "@type": "BreadcrumbList", "@id": url + "#bc",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Facility", "item": SITE + "/sanctify-facility/"},
            {"@type": "ListItem", "position": 3, "name": d["title"], "item": url},
        ],
    }]
    obj = {"@context": "https://schema.org", "@graph": graph}
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(obj, indent=2, ensure_ascii=False)

# ---------------------------------------------------------------------------
# Hero device visuals
# ---------------------------------------------------------------------------
def art_phone():
    return '''<div class="sfy-phone"><div class="sfy-scr">
      <div class="sfy-ptop"><span class="sfy-pav"></span><span><b>sanctifygoa</b><small>Panjim, Goa</small></span></div>
      <div class="sfy-pimg"><span class="sfy-play"></span></div>
      <div class="sfy-pact">%s%s%s</div>
      <div class="sfy-pcap"><b>sanctifygoa</b> New campaign just dropped &#128640; reach that actually converts &#10024;</div>
    </div>
    <span class="sfy-float" style="top:8%%;left:-38px;animation-delay:.2s"><span class="fi" style="background:linear-gradient(135deg,#ff0066,#c8177f)">%s</span>2.4k</span>
    <span class="sfy-float" style="top:44%%;right:-34px;animation-delay:1.1s"><span class="fi" style="background:linear-gradient(135deg,#7b2ff7,#4c1d95)">%s</span>+312 leads</span>
    <span class="sfy-float" style="bottom:9%%;left:-30px;animation-delay:.6s"><span class="fi" style="background:linear-gradient(135deg,#00b37e,#0a7d33)">%s</span>45k views</span>
    </div>''' % (ICON["heart"], ICON["chat"], _svg('<path d="M6 4l14 8-14 8z" fill="currentColor" stroke="none"/>'),
                 ICON["heart"], ICON["users"], ICON["trend"])

def art_map(title, rows):
    r = ''
    for i, (nm, meta, top) in enumerate(rows, 1):
        cls = 'sfy-prow top' if top else 'sfy-prow'
        r += f'<div class="{cls}"><span class="sfy-prank">{i}</span><span><span class="nm">{nm}</span><br><span class="rt">{meta}</span></span></div>'
    return f'''<div class="sfy-glass sfy-mapcard">
      <div class="sfy-map"><span class="sfy-road r1"></span><span class="sfy-road r2"></span><span class="sfy-road r3"></span>
        <span class="sfy-pin"></span><span class="sfy-pin p2"></span><span class="sfy-pin p3"></span></div>
      <div class="sfy-pack"><h5>{title}</h5>{r}</div></div>
    <span class="sfy-float" style="top:-14px;right:6px;animation-delay:.4s"><span class="fi" style="background:linear-gradient(135deg,#ff0066,#c8177f)">{ICON["pin"]}</span>#1 in Map Pack</span>'''

def art_ads():
    bars = ''.join(f'<i style="height:{h}%"></i>' for h in [34,46,40,58,66,74,88])
    return f'''<div class="sfy-glass sfy-adcard">
      <div class="sfy-searchbar"><span class="sfy-gdot"></span><span class="q">digital marketing agency near me</span>{ICON["search"]}</div>
      <div class="sfy-adres"><span class="sfy-adtag">Ad</span><span class="u">www.sanctify.in</span>
        <div class="t">Digital Marketing Agency in Goa | Sanctify</div>
        <p class="d">Data-driven Google Ads &amp; PPC that turn clicks into calls, bookings and sales.</p></div>
      <div class="sfy-adstats">
        <div class="sfy-adstat"><b>6.8x</b><span>Avg. return on ad spend</span></div>
        <div class="sfy-adstat"><b>&#8377;19</b><span>Avg. cost per lead</span></div></div>
      <div class="sfy-bars">{bars}</div></div>
    <span class="sfy-float" style="top:-14px;left:-24px;animation-delay:.5s"><span class="fi" style="background:linear-gradient(135deg,#00b37e,#0a7d33)">{ICON["trend"]}</span>Conversions &#8593; 143%</span>'''

def art_serp():
    return f'''<div class="sfy-glass sfy-serpcard">
      <div class="sfy-serprow win"><span class="sfy-serprk">1</span><span style="flex:1"><span class="st">Your brand &mdash; the answer Google shows first</span><span class="sl"></span><span class="sl s2"></span></span></div>
      <div class="sfy-serprow"><span class="sfy-serprk">2</span><span style="flex:1"><span class="st">competitor-a.in</span><span class="sl"></span></span></div>
      <div class="sfy-serprow"><span class="sfy-serprk">3</span><span style="flex:1"><span class="st">competitor-b.com</span><span class="sl"></span></span></div>
      <div class="sfy-spark"><div class="lab"><span>Organic traffic</span><b>&#8593; 218%</b></div>
        <svg viewBox="0 0 300 70" style="width:100%;height:56px"><defs><linearGradient id="sfg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#ff0066" stop-opacity=".35"/><stop offset="1" stop-color="#7b2ff7" stop-opacity="0"/></linearGradient></defs>
        <path d="M0 58 C40 54 60 40 100 38 S170 24 210 18 260 8 300 6" fill="none" stroke="url(#sfl)" stroke-width="3"/>
        <linearGradient id="sfl" x1="0" x2="1"><stop offset="0" stop-color="#ff0066"/><stop offset="1" stop-color="#7b2ff7"/></linearGradient>
        <path d="M0 58 C40 54 60 40 100 38 S170 24 210 18 260 8 300 6 L300 70 L0 70Z" fill="url(#sfg)"/></svg></div>
    </div>
    <span class="sfy-float" style="top:-12px;right:-10px;animation-delay:.4s"><span class="fi" style="background:linear-gradient(135deg,#ff0066,#c8177f)">{ICON["search"]}</span>Ranked #1</span>'''
print("renderers loaded")



def G(s):  # gradient keyword span
    return f'<span class="sfy-grad-txt">{s}</span>'

TRUST = ["Mercedes-Benz Goa", "Kenkre Dental", "Hotel Supreme Grande",
         "BITS Pilani Goa", "My Taxi Goa", "GoaPolitan", "Akshaya Jewellery"]

# ---------------------------------------------------------------------------
# PAGE DATA
# ---------------------------------------------------------------------------
PAGES = {}

PAGES["social-media-marketing-agency-goa"] = dict(
    id=6977, url_path="/sanctify-facility/social-media-marketing-agency-goa/",
    title="Social Media Marketing Agency in Goa",
    meta_title="Social Media Marketing Agency in Goa | Instagram &amp; Meta Ads | Sanctify",
    meta_desc="Sanctify is a social media marketing agency in Goa running strategy, reels, paid social and community management on Instagram, Facebook, YouTube & LinkedIn. Built for Goa brands, measured on real results.",
    schema_name="Social Media Marketing", area="Goa, India",
    eyebrow="Social Media Marketing · Goa",
    h1=f'Make Goa {G("stop scrolling")} and start buying.',
    lead="We turn feeds into funnels. Strategy, scroll-stopping content, paid social and community management across Instagram, Facebook, YouTube &amp; LinkedIn &ndash; built for Goa audiences and measured on bookings, leads and sales.",
    art=art_phone(),
    marquee=["Instagram Growth", "Reels &amp; UGC", "Meta Ads", "Community", "Influencer Collabs", "Analytics"],
    trust=TRUST,
    svc_kicker="What we do", svc_h2=f'A full {G("creator studio")}, in one team.',
    svc_sub="Strategy, content, ads and community &ndash; the complete social system that grows reach and revenue for Goa brands.",
    services=[
        dict(icon="target", t="Paid Social Advertising", d="High-ROI Instagram &amp; Facebook campaigns with precise targeting, creative testing and conversion tracking that turn ad spend into measurable bookings and sales."),
        dict(icon="camera", t="Content &amp; Reels", d="Reels, posts, stories &amp; graphics designed to stop the scroll.", wide=True),
        dict(icon="compass", t="Strategy &amp; Audit", d="A data-backed monthly plan tuned to your niche."),
        dict(icon="chat", t="Community Management", d="On-brand engagement and DMs that build loyalty."),
        dict(icon="users", t="Influencer &amp; Creator Collabs", d="Authentic partnerships with Goa creators that expand reach and trust.", wide=True),
        dict(icon="chart", t="Analytics &amp; Reporting", d="Clear monthly reporting on the metrics that grow revenue."),
    ],
    metrics=[("14+", "Years growing Goa brands"), ("500+", "Campaigns delivered"),
             ("30+", "Creators in our network"), ("100%", "In-house, no outsourcing")],
    why_kicker="Why Sanctify", why_h2=f'Social that is built to {G("convert")}, not just post.',
    why=[
        dict(t="Local audience intelligence", d="We know how Goa buys &ndash; tourists, locals and NRI audiences each need a different hook."),
        dict(t="Creative that stops the scroll", d="An in-house studio for reels, photography and graphics, so output never stalls."),
        dict(t="Paid + organic, together", d="Ads amplify your best organic content instead of fighting it for budget."),
        dict(t="Measured on revenue", d="Every account gets goal tracking so spend maps to leads and sales, not vanity likes."),
    ],
    proc_kicker="How we work", proc_h2=f'How we {G("grow your account")}',
    process=[
        dict(t="Discover", d="We audit your presence, competitors and audience, then define clear goals."),
        dict(t="Plan", d="A monthly content calendar and paid-social roadmap mapped to those goals."),
        dict(t="Create &amp; Launch", d="Our studio produces content and launches optimised campaigns."),
        dict(t="Optimise &amp; Scale", d="We test relentlessly and scale what drives leads, bookings and sales."),
    ],
    faq_h2=f'Questions, {G("answered")}',
    faq=[
        dict(q="How much does social media marketing cost in Goa?", a="Pricing depends on platforms, content volume and ad spend. We offer flexible monthly retainers scaled to your goals and budget &ndash; ask us for a proposal built around your business."),
        dict(q="Which platforms are best for my business?", a="For most Goa businesses Instagram and Facebook drive the strongest results, with LinkedIn for B2B and YouTube for video. We recommend the mix based on your audience and objective."),
        dict(q="Do you create the content too?", a="Yes &ndash; reels, posts, stories, graphics and captions are handled end-to-end by our in-house creative team."),
        dict(q="How soon will I see results?", a="Engagement and reach improve within the first few weeks; paid campaigns can drive leads almost immediately, while organic growth compounds over months."),
        dict(q="Do you run influencer campaigns in Goa?", a="We do &ndash; through our <a href='"+SITE+"/sanctify-facility/influencer-marketing-agency-goa/'>influencer marketing</a> service we match you with vetted Goa creators and manage the whole collaboration."),
    ],
    cta_h2="Let&rsquo;s make your brand impossible to scroll past.",
    cta_sub="Book a free strategy call and get a custom social media plan for your Goa business.",
    related=[("Influencer Marketing", SITE+"/sanctify-facility/influencer-marketing-agency-goa/"),
             ("PPC &amp; Google Ads", SITE+"/sanctify-facility/ppc-google-ads-agency-goa/"),
             ("Content Marketing", SITE+"/sanctify-facility/content-marketing-agency-goa/")],
)

PAGES["local-seo-services-goa"] = dict(
    id=6978, url_path="/sanctify-facility/local-seo-services-goa/",
    title="Local SEO Services in Goa",
    meta_title="Local SEO Services in Goa | Google Business Profile &amp; Map Pack | Sanctify",
    meta_desc="Local SEO services in Goa that win the Google Map Pack and 'near me' searches. We optimise your Google Business Profile, citations, reviews and location pages to drive calls, visits and bookings.",
    schema_name="Local SEO Services", area="Goa, India",
    eyebrow="Local SEO · Goa",
    h1=f'Own the {G("Map Pack")} in every corner of Goa.',
    lead="Get found in the Google Map Pack and &ldquo;near me&rdquo; searches across North and South Goa. We optimise your Google Business Profile, citations, reviews and location pages to drive calls, visits and bookings.",
    art=art_map("Dentists near Panjim", [
        ("Your Business", "&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 (128) · Open now", True),
        ("A Competitor Clinic", "&#9733;&#9733;&#9733;&#9733;&#9734; 4.2 (54)", False),
        ("Another Listing", "&#9733;&#9733;&#9733;&#9733;&#9734; 4.0 (31)", False),
    ]),
    marquee=["Google Business Profile", "Map Pack", "Citations &amp; NAP", "Reviews", "Location Pages", "&ldquo;Near me&rdquo; SEO"],
    trust=TRUST,
    svc_kicker="What we do", svc_h2=f'Local SEO that fills the {G("Map Pack")}.',
    svc_sub="A complete local visibility system engineered for ready-to-buy customers in your area.",
    services=[
        dict(icon="pin", t="Google Business Profile", d="Full GBP setup, optimisation, categories, services and weekly posts that keep you ranking and clickable."),
        dict(icon="search", t="Local Keyword SEO", d="On-page optimisation for local, high-intent searches.", wide=True),
        dict(icon="list", t="Citations &amp; NAP", d="Consistent listings across the directories that matter."),
        dict(icon="star", t="Reviews &amp; Reputation", d="Review-generation flows and reputation management."),
        dict(icon="page", t="Location Pages", d="Optimised service-area and city landing pages that rank.", wide=True),
        dict(icon="gauge", t="Map Pack Tracking", d="Local rank tracking and clear monthly reporting."),
    ],
    metrics=[("14+", "Years of local SEO in Goa"), ("500+", "Projects delivered"),
             ("4.9", "Average client rating"), ("100%", "In-house team")],
    why_kicker="Why Sanctify", why_h2=f'Why local SEO {G("wins in Goa")}.',
    why=[
        dict(t="Highest-intent traffic", d="&ldquo;Near me&rdquo; searchers are ready to call, visit or book &ndash; the closest thing to a walk-in."),
        dict(t="Map Pack visibility", d="We put you in the 3-pack where the majority of local clicks actually happen."),
        dict(t="Multi-location ready", d="Individual optimised profiles and pages for each branch across Goa."),
        dict(t="Proven local playbook", d="Local strategies refined for the Goa market since 2012."),
    ],
    proc_kicker="How we work", proc_h2="Our local SEO process",
    process=[
        dict(t="Audit", d="We assess your GBP, citations and current local rankings."),
        dict(t="Optimise", d="Profile, on-page and citation cleanup and build-out."),
        dict(t="Content", d="Location pages, GBP posts and review generation."),
        dict(t="Track", d="Map Pack tracking and monthly optimisation."),
    ],
    faq_h2="Frequently asked questions",
    faq=[
        dict(q="How long does local SEO take?", a="Google Business Profile improvements can show within weeks; competitive Map Pack rankings typically build over three to six months of consistent work."),
        dict(q="Do you manage reviews and GBP posts?", a="Yes &ndash; we optimise the profile, publish regular posts and set up a review-generation flow while helping you respond professionally."),
        dict(q="Can you help a multi-location business?", a="Absolutely &ndash; we create individual optimised profiles and location pages for each branch across Goa."),
        dict(q="Is local SEO different from regular SEO?", a="It overlaps with our <a href='"+SITE+"/sanctify-facility/search-engine-optimization-seo-company-in-goa-india/'>SEO services</a>, but local SEO adds Google Business Profile, map ranking, citations and reviews to win &lsquo;near me&rsquo; searches specifically."),
    ],
    cta_h2="Own your local market.",
    cta_sub="Rank in the Map Pack across North and South Goa and turn local searches into customers.",
    cta_b1="Get in Touch", cta_b2="View Services",
    related=[("North Goa", SITE+"/digital-marketing-agency-north-goa/"),
             ("South Goa", SITE+"/digital-marketing-agency-south-goa/"),
             ("SEO Services", SITE+"/sanctify-facility/search-engine-optimization-seo-company-in-goa-india/")],
)

PAGES["ppc-google-ads-agency-goa"] = dict(
    id=6979, url_path="/sanctify-facility/ppc-google-ads-agency-goa/",
    title="PPC &amp; Google Ads Agency in Goa",
    meta_title="PPC &amp; Google Ads Agency in Goa | Search, Shopping &amp; Meta Ads | Sanctify",
    meta_desc="A PPC & Google Ads agency in Goa that turns ad spend into calls, bookings and sales. Search, Shopping, Performance Max and Meta Ads managed by a certified in-house team, measured on ROAS.",
    schema_name="PPC &amp; Google Ads Management", area="Goa, India",
    eyebrow="PPC &amp; Google Ads · Goa",
    h1=f'Ad spend that comes back as {G("revenue")}.',
    lead="Certified Google Ads and Meta management for Goa businesses. Search, Shopping, Performance Max and paid social &ndash; engineered around conversions, cost-per-lead and return on ad spend, not clicks.",
    art=art_ads(),
    marquee=["Google Search Ads", "Performance Max", "Shopping", "Meta Ads", "Remarketing", "Conversion Tracking"],
    trust=TRUST,
    svc_kicker="What we do", svc_h2=f'Full-funnel {G("paid media")}, managed end-to-end.',
    svc_sub="From first click to booked customer &ndash; campaigns built, tracked and optimised for measurable return.",
    services=[
        dict(icon="google", t="Google Search &amp; PMax", d="High-intent Search, Performance Max and Shopping campaigns that capture people actively looking for what you sell."),
        dict(icon="target", t="Meta &amp; Instagram Ads", d="Prospecting and retargeting that fills the funnel.", wide=True),
        dict(icon="gauge", t="Conversion Tracking", d="Proper GA4 and pixel setup so every rupee is measured."),
        dict(icon="link", t="Landing Pages", d="Fast, focused pages that turn clicks into leads."),
        dict(icon="trend", t="Remarketing", d="Win back visitors who didn&rsquo;t convert the first time.", wide=True),
        dict(icon="chart", t="ROAS Reporting", d="Transparent reporting on spend, leads and return."),
    ],
    metrics=[("6.8x", "Avg. return on ad spend"), ("500+", "Campaigns delivered"),
             ("14+", "Years managing ad budgets"), ("100%", "Certified in-house team")],
    why_kicker="Why Sanctify", why_h2=f'Paid media with {G("nothing wasted")}.',
    why=[
        dict(t="Certified &amp; hands-on", d="Real specialists manage your account daily &ndash; not a dashboard on autopilot."),
        dict(t="Conversion-first setup", d="We fix tracking before we spend, so decisions are based on real leads and sales."),
        dict(t="Creative + media together", d="In-house creative means ads and landing pages are built as one system."),
        dict(t="Clear, honest reporting", d="You always know what you spent, what it returned and what we&rsquo;re changing next."),
    ],
    proc_kicker="How we work", proc_h2="Our PPC process",
    process=[
        dict(t="Audit &amp; Plan", d="We review your account, tracking and competitors, then build a plan."),
        dict(t="Build", d="Campaigns, keywords, creative and landing pages set up properly."),
        dict(t="Launch &amp; Track", d="Go live with full conversion tracking from day one."),
        dict(t="Optimise", d="Weekly optimisation to lower cost-per-lead and grow ROAS."),
    ],
    faq_h2="Frequently asked questions",
    faq=[
        dict(q="What&rsquo;s the minimum ad budget to start?", a="It depends on your industry and goals, but we work with a wide range of Goa budgets and will tell you honestly what a realistic starting spend looks like for your market."),
        dict(q="Is the ad spend separate from your fee?", a="Yes &ndash; ad spend is paid directly to Google or Meta. Our management fee is separate and scaled to the work and budget involved."),
        dict(q="How soon will I see leads?", a="Search campaigns can generate enquiries within days of launch because they target people actively searching. We then optimise to bring the cost-per-lead down over the following weeks."),
        dict(q="Do you handle both Google and social ads?", a="We do &ndash; and they work best together. We often pair Google Ads with <a href='"+SITE+"/sanctify-facility/social-media-marketing-agency-goa/'>social media marketing</a> for full-funnel coverage."),
    ],
    cta_h2="Turn your ad budget into booked customers.",
    cta_sub="Get a free account audit and a paid-media plan built around your cost-per-lead and ROAS targets.",
    related=[("Social Media Marketing", SITE+"/sanctify-facility/social-media-marketing-agency-goa/"),
             ("Local SEO", SITE+"/sanctify-facility/local-seo-services-goa/"),
             ("Content Marketing", SITE+"/sanctify-facility/content-marketing-agency-goa/")],
)

PAGES["content-marketing-agency-goa"] = dict(
    id=6980, url_path="/sanctify-facility/content-marketing-agency-goa/",
    title="Content Marketing Agency in Goa",
    meta_title="Content Marketing Agency in Goa | SEO Content &amp; Strategy | Sanctify",
    meta_desc="A content marketing agency in Goa that builds topical authority: SEO blogs, website copy, video and content strategy that rank, earn trust and turn readers into customers.",
    schema_name="Content Marketing", area="Goa, India",
    eyebrow="Content Marketing · Goa",
    h1=f'Content that {G("ranks, earns trust")} and sells.',
    lead="SEO-led content that makes your brand the answer people find in Goa. Strategy, blogs, website copy, video and topical authority &ndash; written to rank on Google and convince real buyers.",
    art=art_serp(),
    marquee=["Content Strategy", "SEO Blogs", "Website Copy", "Topical Authority", "Video &amp; Scripts", "Email"],
    trust=TRUST,
    svc_kicker="What we do", svc_h2=f'Words and stories that build {G("authority")}.',
    svc_sub="A content engine that compounds &ndash; every piece supports the next and moves you up the rankings.",
    services=[
        dict(icon="doc", t="SEO Blog &amp; Articles", d="Search-optimised articles that target the questions your customers actually ask &ndash; the foundation of topical authority."),
        dict(icon="compass", t="Content Strategy", d="A topic map and calendar tied to real search demand.", wide=True),
        dict(icon="pen", t="Website &amp; Landing Copy", d="Clear, persuasive copy that converts visitors."),
        dict(icon="camera", t="Video &amp; Scripts", d="Short-form scripts and video content that travels."),
        dict(icon="bulb", t="Topical Authority", d="Interlinked content clusters that make Google trust your site.", wide=True),
        dict(icon="mail", t="Email &amp; Newsletters", d="Nurture sequences that keep leads warm."),
    ],
    metrics=[("218%", "Avg. organic traffic lift"), ("500+", "Content pieces produced"),
             ("14+", "Years telling Goa stories"), ("100%", "Human, original writing")],
    why_kicker="Why Sanctify", why_h2=f'Content built on {G("search demand")}, not guesswork.',
    why=[
        dict(t="SEO from the first word", d="Every piece is mapped to a real keyword and search intent before we write."),
        dict(t="Clusters, not one-offs", d="We build interlinked topic clusters that lift the whole site, not isolated posts."),
        dict(t="Written for people too", d="Content that ranks and actually persuades a reader to enquire."),
        dict(t="Local &amp; sector fluency", d="We write for Goa audiences and understand hospitality, healthcare, auto and more."),
    ],
    proc_kicker="How we work", proc_h2="Our content process",
    process=[
        dict(t="Research", d="Keyword, intent and competitor research to find the gaps."),
        dict(t="Plan", d="A topic map and editorial calendar built around demand."),
        dict(t="Create", d="Original, SEO-optimised content produced and edited in-house."),
        dict(t="Distribute", d="Publish, interlink, promote and measure what performs."),
    ],
    faq_h2="Frequently asked questions",
    faq=[
        dict(q="How is content marketing different from just blogging?", a="Blogging is one tactic; content marketing is a strategy. We map topics to search demand and buyer journeys, then interlink everything to build authority that compounds over time."),
        dict(q="Do you write the content or just plan it?", a="Both &ndash; strategy, writing, editing and publishing are handled by our in-house team. All content is original and written for humans and search engines."),
        dict(q="How does content help my rankings?", a="Well-structured content clusters signal topical authority to Google, support your <a href='"+SITE+"/sanctify-facility/search-engine-optimization-seo-company-in-goa-india/'>SEO</a> and earn links and trust &ndash; which lifts rankings across the site."),
        dict(q="When will I see results?", a="Content is a compounding asset. Early pieces can rank within weeks for low-competition terms, while authority and traffic build meaningfully over three to six months."),
    ],
    cta_h2="Become the answer Goa searches for.",
    cta_sub="Get a content strategy session and a topic map built around what your customers are actually searching.",
    related=[("SEO Services", SITE+"/sanctify-facility/search-engine-optimization-seo-company-in-goa-india/"),
             ("Local SEO", SITE+"/sanctify-facility/local-seo-services-goa/"),
             ("Social Media Marketing", SITE+"/sanctify-facility/social-media-marketing-agency-goa/")],
)

# -- City pages --------------------------------------------------------------
def city_page(pid, slug, region, region_low, places, hero_rows, other_region, other_url):
    return dict(
        id=pid, url_path="/"+slug+"/",
        title=f"Digital Marketing Agency in {region}",
        meta_title=f"Digital Marketing Agency in {region} | SEO, Ads &amp; Social | Sanctify",
        meta_desc=f"Sanctify is a digital marketing agency serving {region}, Goa &ndash; SEO, Google Ads, social media, web design and content for businesses in {places[0]}, {places[1]} and across {region_low}.",
        schema_name=f"Digital Marketing Agency in {region}", area=f"{region}, Goa, India",
        eyebrow=f"Digital Marketing · {region}",
        h1=f'The digital marketing partner {region} {G("brands trust")}.',
        lead=f"Full-service digital marketing for businesses across {region}, Goa &ndash; from {places[0]} to {places[1]}. SEO, Google Ads, social media, web design and content, all under one roof and measured on real results.",
        art=art_map(f"Marketing agency in {region}", hero_rows),
        marquee=["SEO", "Google Ads", "Social Media", "Web Design", "Local SEO", "Content"],
        trust=TRUST,
        svc_kicker="What we do", svc_h2=f'Everything {region} businesses need to {G("grow online")}.',
        svc_sub=f"One team for search, ads, social, web and content &ndash; so your marketing pulls in the same direction across {region_low}.",
        services=[
            dict(icon="search", t="SEO &amp; Local SEO", d=f"Rank on Google and in the Map Pack for {region} &lsquo;near me&rsquo; searches that bring ready-to-buy customers."),
            dict(icon="google", t="Google &amp; Meta Ads", d="High-ROI paid campaigns that drive leads fast.", wide=True),
            dict(icon="camera", t="Social Media", d="Content and community that grows your local audience."),
            dict(icon="page", t="Web Design", d="Fast, mobile-first websites built to convert."),
            dict(icon="doc", t="Content Marketing", d="SEO content that builds authority and trust.", wide=True),
            dict(icon="chart", t="Analytics", d="Tracking and reporting tied to leads and revenue."),
        ],
        metrics=[("#1", f"Ranked for {region} marketing"), ("14+", "Years serving Goa"),
                 ("500+", "Projects delivered"), ("100%", "In-house team")],
        why_kicker="Why Sanctify", why_h2=f'Why {region} businesses {G("choose us")}.',
        why=[
            dict(t=f"On the ground in {region_low}", d=f"We know {places[0]}, {places[1]} and the {region_low} market &ndash; not a remote agency guessing."),
            dict(t="Everything under one roof", d="SEO, ads, social, web and content from one accountable team."),
            dict(t="Local since 2012", d="Over a decade building brands and rankings across Goa."),
            dict(t="Measured on results", d="Goal tracking on every engagement, so spend maps to enquiries."),
        ],
        proc_kicker="How we work", proc_h2="How we grow your business",
        process=[
            dict(t="Discover", d=f"We learn your goals, market and {region_low} competitors."),
            dict(t="Strategy", d="A channel plan built around your best opportunities."),
            dict(t="Execute", d="Search, ads, social, web and content, delivered in-house."),
            dict(t="Optimise", d="Continuous improvement tied to leads and revenue."),
        ],
        faq_h2="Frequently asked questions",
        faq=[
            dict(q=f"Do you work with small businesses in {region}?", a=f"Yes &ndash; from single-location shops and clinics to hotels and multi-branch brands across {region_low}. We scale the plan to your goals and budget."),
            dict(q="Which services should I start with?", a=f"It depends on your goals. Most {region} businesses start with <a href='"+SITE+"/sanctify-facility/local-seo-services-goa/'>local SEO</a> and <a href='"+SITE+"/sanctify-facility/ppc-google-ads-agency-goa/'>Google Ads</a> for fast, high-intent leads, then add social and content."),
            dict(q="Do you also serve "+other_region+"?", a="We do &ndash; we work across all of Goa. See our <a href='"+other_url+"'>"+other_region+"</a> page, or our main <a href='"+SITE+"/digital-marketing-agency-goa/'>Goa digital marketing</a> hub."),
            dict(q="How do we get started?", a="Get in touch for a free consultation. We&rsquo;ll audit your current presence and show you the fastest route to more enquiries."),
        ],
        cta_h2=f"Grow your business across {region}.",
        cta_sub=f"Book a free consultation and get a digital marketing plan tailored to your {region_low} audience.",
        related=[(other_region, other_url),
                 ("SEO Services", SITE+"/sanctify-facility/search-engine-optimization-seo-company-in-goa-india/"),
                 ("Local SEO", SITE+"/sanctify-facility/local-seo-services-goa/")],
    )

PAGES["digital-marketing-agency-north-goa"] = city_page(
    6981, "digital-marketing-agency-north-goa", "North Goa", "North Goa",
    ["Panjim", "Calangute"],
    [("Your Business", "&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 &middot; Panjim", True),
     ("A Competitor", "&#9733;&#9733;&#9733;&#9733;&#9734; 4.3 &middot; Mapusa", False),
     ("Another Agency", "&#9733;&#9733;&#9733;&#9733;&#9734; 4.1 &middot; Calangute", False)],
    "South Goa", SITE+"/digital-marketing-agency-south-goa/")

PAGES["digital-marketing-agency-south-goa"] = city_page(
    6982, "digital-marketing-agency-south-goa", "South Goa", "South Goa",
    ["Margao", "Vasco da Gama"],
    [("Your Business", "&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 &middot; Vasco", True),
     ("A Competitor", "&#9733;&#9733;&#9733;&#9733;&#9734; 4.2 &middot; Margao", False),
     ("Another Agency", "&#9733;&#9733;&#9733;&#9733;&#9734; 4.0 &middot; Colva", False)],
    "North Goa", SITE+"/digital-marketing-agency-north-goa/")

# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
def build_content(slug, d):
    url = SITE + d["url_path"]
    body = "\n".join([
        FONTS, CSS,
        '<div class="sfy2">',
        hero(d),
        marquee(d["marquee"]),
        trust(d["trust"]),
        bento(d),
        metrics(d["metrics"]),
        why(d),
        process(d),
        faq(d),
        cta(d),
        '</div>',
        JS,
        schema(d, url),
    ])
    return body

PREVIEW_DOC = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | Sanctify (preview)</title>
<style>
 body{{margin:0;background:#fff;color:#140b22;font-family:'Inter',system-ui,sans-serif}}
 .pv-bar{{background:#faf7fb;border-bottom:1px solid #eee;font-size:12px;color:#8a8397;padding:6px 0;text-align:center;letter-spacing:.06em}}
 .pv-nav{{display:flex;align-items:center;justify-content:space-between;max-width:1200px;margin:0 auto;padding:16px 22px}}
 .pv-logo{{font-family:'Sora',sans-serif;font-weight:800;font-size:22px;letter-spacing:-.02em}}
 .pv-logo b{{color:#ff0066}}
 .pv-menu{{display:flex;gap:22px;font-size:14px;color:#3a3348;font-weight:500}}
 .pv-content{{max-width:1200px;margin:0 auto;padding:0 18px 40px}}
 .pv-foot{{background:linear-gradient(120deg,#1a0b2e,#2a0f3f);color:#cbbfe0;text-align:center;padding:40px 20px;font-size:13px;margin-top:20px}}
</style></head>
<body>
 <div class="pv-bar">LOCAL PREVIEW &mdash; not published &mdash; {url}</div>
 <div class="pv-nav"><div class="pv-logo">SANCT<b>I</b>FY</div>
   <div class="pv-menu"><span>Home</span><span>About</span><span>Competency</span><span>Facility</span><span>Journal</span><span>Showcase</span><span>Contact</span></div></div>
 <div class="pv-content">{body}</div>
 <div class="pv-foot">SANCTIFY &middot; advertise to promote &middot; Vasco-da-Gama, Goa &middot; &copy; 2012&ndash;2026</div>
</body></html>"""

def main():
    index = []
    for slug, d in PAGES.items():
        content = build_content(slug, d)
        cpath = os.path.join(BUILD, slug + ".content.html")
        open(cpath, "w").write(content)
        preview = PREVIEW_DOC.format(title=re.sub('<[^>]+>', '', d["title"]),
                                     url=SITE + d["url_path"], body=content)
        ppath = os.path.join(PREVIEW, slug + ".html")
        open(ppath, "w").write(preview)
        index.append((slug, d["id"], len(content)))
        print(f"  built {slug:38s} id={d['id']} content={len(content):6d}B")
    print("\nDONE. %d pages built." % len(index))

if __name__ == "__main__":
    main()
