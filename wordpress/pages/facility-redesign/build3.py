#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3 'Editorial Ink' generator - 6 facility/landing pages, each a DISTINCT structure."""
import os, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build3"); PREVIEW = os.path.join(HERE, "preview3")
os.makedirs(BUILD, exist_ok=True); os.makedirs(PREVIEW, exist_ok=True)
SITE = "https://www.sanctify.in"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&'
 'family=Inter:wght@400;500;600&display=swap" rel="stylesheet">')

CSS = r"""
<style id="sfy3-css">
.sfy3{--ink:#0e0b14;--ink2:#171320;--paper:#f6f3ee;--paper2:#ece7df;
  --mag:#ff0066;--mag2:#ff4d88;--txt:#17131f;--body:#4c4658;
  --muted:#8a8296;--line:rgba(20,15,30,.14);--dline:rgba(255,255,255,.16);--maxw:1200px;--pad:28px;
  font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--txt);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.sfy3 *{box-sizing:border-box}
.sfy3 h1,.sfy3 h2,.sfy3 h3,.sfy3 h4{font-family:'Space Grotesk',sans-serif;font-weight:600;letter-spacing:-.03em;line-height:1;margin:0}
.sfy3 p{margin:0}
.sfy3 a{color:inherit;text-decoration:none}
.sfy3 .wrap{max-width:var(--maxw);margin:0 auto;padding:0 var(--pad)}
.sfy3 .mag{color:var(--mag)}
.sfy3 .ey{font-family:'Space Grotesk';font-size:12.5px;font-weight:600;letter-spacing:.24em;text-transform:uppercase}
.sfy3 .reveal{opacity:0;transform:translateY(22px);animation:sfy3rv .8s cubic-bezier(.2,.7,.3,1) forwards}
@keyframes sfy3rv{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.sfy3 .reveal{animation:none;opacity:1;transform:none}.sfy3 .tk,.sfy3 .chipF{animation:none}}
/* buttons */
.sfy3 .btn{display:inline-flex;align-items:center;gap:.6em;font-family:'Space Grotesk';font-weight:600;font-size:15px;padding:15px 26px;border-radius:2px;transition:.25s;border:1px solid transparent}
.sfy3 .btn.b-mag{background:var(--mag);color:#fff}.sfy3 .btn.b-mag:hover{background:#e0005c;transform:translateY(-2px)}
.sfy3 .btn.b-ll{border-color:var(--line);color:var(--txt)}.sfy3 .btn.b-ll:hover{border-color:var(--txt)}
.sfy3 .btn.b-ld{border-color:var(--dline);color:#fff}.sfy3 .btn.b-ld:hover{border-color:#fff;background:rgba(255,255,255,.06)}
.sfy3 .btn.b-dark{background:var(--ink);color:#fff}.sfy3 .btn.b-dark:hover{transform:translateY(-2px)}
.sfy3 .btn .ar{transition:.25s}.sfy3 .btn:hover .ar{transform:translate(3px,-3px)}
/* HERO */
.sfy3 .hero{background:var(--ink);color:#fff;position:relative;overflow:hidden}
.sfy3 .hero::before{content:"";position:absolute;width:760px;height:760px;right:-160px;top:-220px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,0,102,.4),transparent 70%);filter:blur(20px)}
.sfy3 .hero::after{content:"";position:absolute;inset:0;opacity:.5;pointer-events:none;background-image:radial-gradient(rgba(255,255,255,.05) 1px,transparent 1px);background-size:26px 26px;-webkit-mask-image:linear-gradient(180deg,#000,transparent 80%);mask-image:linear-gradient(180deg,#000,transparent 80%)}
.sfy3 .hero-top{display:flex;justify-content:space-between;align-items:center;padding:26px 0 44px;border-bottom:1px solid var(--dline);position:relative}
.sfy3 .hero-top .ey{color:var(--mag2)}
.sfy3 .hero-top .loc{font-size:12.5px;color:rgba(255,255,255,.55);letter-spacing:.1em}
.sfy3 .hero-in{position:relative;display:grid;grid-template-columns:1.02fr .98fr;gap:52px;align-items:center;padding:34px 0 70px}
.sfy3 .hero-in.center{grid-template-columns:1fr;text-align:center;place-items:center;padding-bottom:60px}
.sfy3 .hero h1{font-size:clamp(42px,6.6vw,88px);color:#fff;margin:36px 0 0}
.sfy3 .hero h1 .thin{font-weight:500;color:rgba(255,255,255,.5)}
.sfy3 .hero .lead{font-size:19px;color:rgba(255,255,255,.72);max-width:32em;margin:26px 0 34px;line-height:1.55}
.sfy3 .hero-in.center .lead{margin-left:auto;margin-right:auto}
.sfy3 .hero-cta{display:flex;gap:14px;flex-wrap:wrap}
.sfy3 .hero-figs{display:flex;gap:34px;margin-top:46px;padding-top:26px;border-top:1px solid var(--dline)}
.sfy3 .hero-in.center .hero-figs{justify-content:center}
.sfy3 .hero-figs .f b{font-family:'Space Grotesk';font-size:30px;font-weight:600;color:#fff;display:block;line-height:1}
.sfy3 .hero-figs .f span{font-size:12.5px;color:rgba(255,255,255,.5);letter-spacing:.04em}
/* feed wall */
.sfy3 .feed{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:96px;gap:12px;position:relative}
.sfy3 .tileF{border-radius:10px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.1)}
.sfy3 .tileF .pl{position:absolute;inset:0;display:grid;place-items:center}
.sfy3 .tileF .pl::after{content:"";border-left:14px solid rgba(255,255,255,.92);border-top:9px solid transparent;border-bottom:9px solid transparent;margin-left:3px}
.sfy3 .g1{background:linear-gradient(150deg,#ff0066,#ff5aa8)}.sfy3 .g2{background:linear-gradient(150deg,#7b2ff7,#b06bff)}
.sfy3 .g3{background:linear-gradient(150deg,#12101a,#2a2440)}.sfy3 .g4{background:linear-gradient(150deg,#ff9d00,#ff5aa8)}
.sfy3 .g5{background:linear-gradient(150deg,#00b37e,#38d9a9)}
.sfy3 .tileF.tall{grid-row:span 2}.sfy3 .tileF.wide{grid-column:span 2}
.sfy3 .chipF{position:absolute;background:#fff;color:var(--ink);border-radius:8px;padding:8px 11px;font-family:'Space Grotesk';font-weight:600;font-size:12.5px;box-shadow:0 16px 30px -12px rgba(0,0,0,.5);display:flex;align-items:center;gap:7px;z-index:4}
.sfy3 .chipF .d{width:8px;height:8px;border-radius:50%;background:var(--mag)}
/* generic light card used on hero */
.sfy3 .card{background:#fff;color:var(--txt);border-radius:16px;box-shadow:0 40px 90px -45px rgba(0,0,0,.7);width:100%;max-width:430px;margin:0 auto;overflow:hidden}
/* map card */
.sfy3 .mp{height:200px;position:relative;background:linear-gradient(90deg,rgba(123,47,247,.10) 1px,transparent 1px) 0 0/40px 40px,linear-gradient(rgba(123,47,247,.10) 1px,transparent 1px) 0 0/40px 40px,radial-gradient(140% 120% at 70% 20%,#efe7fb,#e5f6ef)}
.sfy3 .rd0{position:absolute;background:#fff;box-shadow:0 0 0 1px rgba(20,11,34,.05)}
.sfy3 .rdA{height:12px;left:-10px;right:-10px;top:70px;transform:rotate(-6deg)}
.sfy3 .rdB{width:14px;top:-10px;bottom:-10px;left:130px;transform:rotate(8deg)}
.sfy3 .pin0{position:absolute;top:62px;left:160px;width:34px;height:34px;transform:translate(-50%,-100%);background:linear-gradient(150deg,#ff0066,#7b2ff7);border-radius:50% 50% 50% 0;rotate:-45deg;box-shadow:0 10px 20px -6px rgba(255,0,102,.7);display:grid;place-items:center}
.sfy3 .pin0::after{content:"";width:11px;height:11px;background:#fff;border-radius:50%}
.sfy3 .pin0.s{width:22px;height:22px;opacity:.5}.sfy3 .pin0.p2{top:120px;left:260px}.sfy3 .pin0.p3{top:150px;left:70px}
.sfy3 .pack{padding:16px 18px}
.sfy3 .pack h5{font-family:'Space Grotesk';font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.sfy3 .prow{display:flex;align-items:center;gap:11px;padding:9px 0;border-top:1px solid rgba(20,15,30,.07)}
.sfy3 .prow:first-of-type{border-top:0}
.sfy3 .prk{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;font-family:'Space Grotesk';font-weight:700;font-size:13px;flex:0 0 auto}
.sfy3 .prow.top .prk{background:linear-gradient(150deg,#ff0066,#7b2ff7);color:#fff}
.sfy3 .prow:not(.top) .prk{background:var(--paper2);color:var(--muted)}
.sfy3 .prow .nm{font-family:'Space Grotesk';font-weight:600;font-size:13.5px;color:var(--txt)}
.sfy3 .prow .rt2{font-size:11.5px;color:var(--muted)}.sfy3 .prow .rt2 b{color:#ff9d00}
/* dashboard card */
.sfy3 .dash{padding:20px}
.sfy3 .dash .dbig{display:flex;align-items:flex-end;gap:10px;margin-bottom:4px}
.sfy3 .dash .dbig b{font-family:'Space Grotesk';font-size:48px;font-weight:700;line-height:.9;color:var(--txt)}
.sfy3 .dash .dbig span{color:#0a7d33;font-weight:600;font-size:13px;padding-bottom:8px}
.sfy3 .dash .dcap{font-size:12.5px;color:var(--muted);letter-spacing:.02em;margin-bottom:14px}
.sfy3 .bars{display:flex;align-items:flex-end;gap:7px;height:70px;margin-bottom:16px}
.sfy3 .bars i{flex:1;background:linear-gradient(180deg,#ff0066,#7b2ff7);border-radius:5px 5px 0 0;opacity:.9}
.sfy3 .dstats{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.sfy3 .dstat{background:var(--paper);border-radius:10px;padding:12px 14px}
.sfy3 .dstat b{font-family:'Space Grotesk';font-size:22px;color:var(--txt);display:block}
.sfy3 .dstat span{font-size:11.5px;color:var(--muted);font-weight:500}
/* serp card */
.sfy3 .serp{padding:18px}
.sfy3 .srow{display:flex;gap:11px;align-items:flex-start;padding:11px;border-radius:11px;margin-bottom:6px}
.sfy3 .srow.win{background:linear-gradient(120deg,rgba(255,0,102,.07),rgba(123,47,247,.07));border:1px solid rgba(123,47,247,.16)}
.sfy3 .srk{width:26px;height:26px;border-radius:7px;display:grid;place-items:center;font-family:'Space Grotesk';font-weight:700;font-size:13px;flex:0 0 auto}
.sfy3 .srow.win .srk{background:linear-gradient(150deg,#ff0066,#7b2ff7);color:#fff}
.sfy3 .srow:not(.win) .srk{background:var(--paper2);color:var(--muted)}
.sfy3 .srow .stt{font-size:13px;color:#1a0dab;font-weight:600}.sfy3 .srow.win .stt{color:var(--txt)}
.sfy3 .srow .sl{height:7px;background:rgba(20,15,30,.09);border-radius:5px;margin-top:7px}.sfy3 .srow .sl.s2{width:62%;margin-top:5px}
.sfy3 .spk{background:var(--paper);border-radius:11px;padding:12px 14px;margin-top:8px}
.sfy3 .spk .lb{display:flex;justify-content:space-between;font-size:11.5px;color:var(--muted);font-weight:600;margin-bottom:6px}
.sfy3 .spk .lb b{font-family:'Space Grotesk';font-size:17px;color:var(--txt)}
/* ticker rule */
.sfy3 .rule{background:var(--ink);color:#fff;border-top:1px solid var(--dline);overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.sfy3 .tk{display:inline-flex;white-space:nowrap;animation:sfy3tk 30s linear infinite;padding:16px 0;font-family:'Space Grotesk';font-weight:500;font-size:14px;letter-spacing:.04em;color:rgba(255,255,255,.6)}
.sfy3 .tk span{padding:0 26px}.sfy3 .tk b{color:var(--mag2)}
@keyframes sfy3tk{to{transform:translateX(-50%)}}
/* bands + split + labels */
.sfy3 .band{padding:100px 0}
.sfy3 .band.paper{background:var(--paper)}.sfy3 .band.paper2{background:var(--paper2)}
.sfy3 .band.ink{background:var(--ink);color:#fff}
.sfy3 .split{display:grid;grid-template-columns:262px 1fr;gap:56px}
.sfy3 .slabel{position:sticky;top:36px;align-self:start}
.sfy3 .slabel .n{font-family:'Space Grotesk';font-size:13px;font-weight:600;color:var(--mag);letter-spacing:.1em}
.sfy3 .slabel h2{font-size:clamp(27px,3.3vw,40px);margin:14px 0 0;color:inherit}
.sfy3 .slabel p{font-size:15px;color:var(--muted);margin-top:16px;max-width:23em}
.sfy3 .band.ink .slabel p{color:rgba(255,255,255,.55)}
/* index rows */
.sfy3 .idx{border-top:1px solid var(--line)}.sfy3 .band.ink .idx{border-top-color:var(--dline)}
.sfy3 .row{display:grid;grid-template-columns:60px 1fr auto;gap:6px 22px;align-items:start;padding:26px 8px;border-bottom:1px solid var(--line);transition:.3s}
.sfy3 .band.ink .row{border-bottom-color:var(--dline)}
.sfy3 .row .rn{font-family:'Space Grotesk';font-size:15px;color:var(--muted);font-weight:600;transition:.3s;padding-top:6px}
.sfy3 .row h3{font-family:'Space Grotesk';font-size:clamp(21px,2.5vw,29px);font-weight:600;color:inherit;transition:.3s}
.sfy3 .row .rd{font-size:15.5px;color:var(--body);grid-column:2;line-height:1.55;max-width:64ch;margin-top:9px}
.sfy3 .band.ink .row .rd{color:rgba(255,255,255,.62)}
.sfy3 .row .rt{font-family:'Space Grotesk';font-size:12.5px;color:var(--muted);white-space:nowrap;border:1px solid var(--line);border-radius:999px;padding:5px 12px;height:fit-content;margin-top:4px}
.sfy3 .band.ink .row .rt{border-color:var(--dline)}
.sfy3 .row:hover{padding-left:18px}.sfy3 .row:hover .rn,.sfy3 .row:hover h3{color:var(--mag)}
.sfy3 .row:hover .rt{border-color:var(--mag);color:var(--mag)}
.sfy3 .row .rd b{font-weight:600}
/* statement */
.sfy3 .state{font-family:'Space Grotesk';font-weight:500;font-size:clamp(28px,4.4vw,58px);line-height:1.05;letter-spacing:-.03em;max-width:17ch}
.sfy3 .state .num{color:var(--mag)}.sfy3 .state .thin{color:rgba(255,255,255,.4)}
/* horizontal strip */
.sfy3 .strip-h{display:flex;gap:20px;overflow-x:auto;padding:6px 4px 24px;scroll-snap-type:x mandatory}
.sfy3 .strip-h::-webkit-scrollbar{height:6px}.sfy3 .strip-h::-webkit-scrollbar-thumb{background:var(--dline);border-radius:3px}
.sfy3 .scard{flex:0 0 300px;scroll-snap-align:start;background:var(--ink2);border:1px solid var(--dline);border-radius:14px;overflow:hidden}
.sfy3 .band.paper .scard{background:#fff;border-color:var(--line)}
.sfy3 .scard .im{height:172px;position:relative}
.sfy3 .scard .im .pl{position:absolute;inset:0;display:grid;place-items:center}
.sfy3 .scard .im .pl::after{content:"";border-left:16px solid rgba(255,255,255,.92);border-top:10px solid transparent;border-bottom:10px solid transparent}
.sfy3 .scard .cap{padding:16px 18px}
.sfy3 .scard .cap .k{font-family:'Space Grotesk';font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mag);font-weight:600}
.sfy3 .scard .cap h4{font-family:'Space Grotesk';font-size:17px;margin:8px 0 0;color:inherit}
.sfy3 .band.ink .scard .cap h4{color:#fff}
/* compare */
.sfy3 .cmp{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.sfy3 .col{border:1px solid var(--line);border-radius:16px;padding:24px;background:#fff}
.sfy3 .col.win{border-color:var(--mag);box-shadow:0 30px 60px -34px rgba(255,0,102,.4)}
.sfy3 .col .ct{font-family:'Space Grotesk';font-weight:600;font-size:18px;margin-bottom:16px;display:flex;align-items:center;gap:10px}
.sfy3 .col.win .ct{color:var(--mag)}
.sfy3 .ci{display:flex;gap:11px;padding:10px 0;border-top:1px solid var(--line);font-size:14.5px;color:var(--body)}
.sfy3 .ci:first-of-type{border-top:0}
.sfy3 .ci .mk{width:22px;height:22px;border-radius:6px;flex:0 0 auto;display:grid;place-items:center;font-weight:700;font-size:13px}
.sfy3 .ci .yes{background:rgba(0,179,126,.14);color:#0a7d33}.sfy3 .ci .no{background:rgba(20,15,30,.06);color:var(--muted)}
/* funnel */
.sfy3 .funnel{display:flex;flex-direction:column;gap:12px;align-items:center}
.sfy3 .fstage{border-radius:12px;padding:18px 22px;color:#fff;display:flex;justify-content:space-between;align-items:center;width:100%}
.sfy3 .fstage b{font-family:'Space Grotesk';font-size:18px}.sfy3 .fstage span{font-family:'Space Grotesk';font-weight:600;opacity:.9}
.sfy3 .fstage.s1{background:#2a2440;max-width:100%}
.sfy3 .fstage.s2{background:#4c1d95;max-width:82%}
.sfy3 .fstage.s3{background:#7b2ff7;max-width:64%}
.sfy3 .fstage.s4{background:var(--mag);max-width:46%}
/* clusters */
.sfy3 .clus{text-align:center}
.sfy3 .pillar{display:inline-block;background:var(--mag);color:#fff;font-family:'Space Grotesk';font-weight:600;font-size:18px;padding:16px 28px;border-radius:12px;box-shadow:0 20px 40px -18px rgba(255,0,102,.5)}
.sfy3 .cline{width:2px;height:34px;background:var(--line);margin:0 auto}
.sfy3 .chips{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.sfy3 .chip{border:1px solid var(--line);background:#fff;border-radius:999px;padding:11px 18px;font-family:'Space Grotesk';font-weight:500;font-size:14px;color:var(--txt);transition:.25s}
.sfy3 .chip:hover{border-color:var(--mag);color:var(--mag);transform:translateY(-2px)}
/* coverage */
.sfy3 .cov{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}
.sfy3 .area{border:1px solid var(--line);border-radius:12px;padding:16px 16px;background:#fff;display:flex;align-items:center;gap:10px;font-family:'Space Grotesk';font-weight:600;font-size:15px;transition:.25s}
.sfy3 .area:hover{border-color:var(--mag);transform:translateY(-3px);box-shadow:0 20px 40px -24px rgba(255,0,102,.4)}
.sfy3 .area .pn{width:9px;height:9px;border-radius:50%;background:var(--mag);flex:0 0 auto}
/* process editorial */
.sfy3 .steps3{border-top:1px solid var(--dline)}
.sfy3 .band.paper .steps3{border-top-color:var(--line)}
.sfy3 .st3{display:grid;grid-template-columns:120px 1fr;gap:34px;padding:32px 0;border-bottom:1px solid var(--dline);align-items:baseline}
.sfy3 .band.paper .st3{border-bottom-color:var(--line)}
.sfy3 .st3 .bn{font-family:'Space Grotesk';font-size:clamp(38px,6vw,72px);font-weight:600;color:rgba(255,255,255,.14);line-height:.8}
.sfy3 .band.paper .st3 .bn{color:rgba(20,15,30,.12)}
.sfy3 .st3 h4{font-family:'Space Grotesk';font-size:23px;color:inherit;margin:0 0 8px}
.sfy3 .st3 p{color:rgba(255,255,255,.6);font-size:16px;max-width:54ch}
.sfy3 .band.paper .st3 p{color:var(--body)}
/* faq */
.sfy3 .faq3{border-top:1px solid var(--line)}
.sfy3 .q3{border-bottom:1px solid var(--line)}
.sfy3 .q3 summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:20px;align-items:center;padding:24px 4px;font-family:'Space Grotesk';font-weight:600;font-size:clamp(17px,1.9vw,21px);color:var(--txt)}
.sfy3 .q3 summary::-webkit-details-marker{display:none}
.sfy3 .q3 .pm{width:24px;height:24px;position:relative;flex:0 0 auto}
.sfy3 .q3 .pm::before,.sfy3 .q3 .pm::after{content:"";position:absolute;background:var(--mag);inset:0;margin:auto}
.sfy3 .q3 .pm::before{width:18px;height:2px}.sfy3 .q3 .pm::after{width:2px;height:18px;transition:.3s}
.sfy3 .q3[open] .pm::after{transform:rotate(90deg);opacity:0}
.sfy3 .q3 .a3{padding:0 4px 26px;color:var(--body);font-size:16px;max-width:72ch}
.sfy3 .q3 .a3 a{color:var(--mag);text-decoration:underline;text-underline-offset:3px}
/* cta */
.sfy3 .cta3{background:var(--mag);color:#fff;position:relative;overflow:hidden}
.sfy3 .cta3::after{content:"";position:absolute;inset:0;opacity:.5;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1px);background-size:26px 26px}
.sfy3 .cta3-in{position:relative;padding:92px 0;text-align:center}
.sfy3 .cta3 h2{font-size:clamp(34px,5.6vw,74px);color:#fff}
.sfy3 .cta3 p{color:rgba(255,255,255,.85);font-size:18px;margin:22px auto 32px;max-width:34em}
.sfy3 .cta3 .hero-cta{justify-content:center}
.sfy3 .cta3 .rel{margin-top:28px;font-size:14px;color:rgba(255,255,255,.82)}
.sfy3 .cta3 .rel a{color:#fff;text-decoration:underline;text-underline-offset:3px}
@media(max-width:940px){
  .sfy3 .hero-in{grid-template-columns:1fr;gap:38px;padding:20px 0 54px}
  .sfy3 .split{grid-template-columns:1fr;gap:28px}.sfy3 .slabel{position:static}
  .sfy3 .row{grid-template-columns:44px 1fr;gap:6px 14px}.sfy3 .row .rt{display:none}
  .sfy3 .cmp{grid-template-columns:1fr}.sfy3 .st3{grid-template-columns:64px 1fr;gap:16px}
}
@media(max-width:560px){.sfy3 .band{padding:64px 0}.sfy3 .hero h1{font-size:42px}.sfy3 .hero-figs{flex-wrap:wrap;gap:20px}.sfy3 .fstage{max-width:100%!important}}
</style>
"""
print("v3 framework loaded")



# ---------------- hero + section renderers ----------------
def hero(eyebrow, loc, h1, lead, art, figs, cta1="Start a project", cta2="See the work", center=False):
    figs_html = "".join(f'<div class="f"><b>{b}</b><span>{s}</span></div>' for b, s in figs)
    ccls = " center" if center else ""
    return f'''
<section class="hero"><div class="wrap">
  <div class="hero-top"><span class="ey">{eyebrow}</span><span class="loc">{loc}</span></div>
  <div class="hero-in{ccls}">
    <div class="reveal">
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <div class="hero-cta"><a class="btn b-mag" href="{SITE}/contact/">{cta1} <span class="ar">&#8599;</span></a>
        <a class="btn b-ld" href="#s01">{cta2}</a></div>
      <div class="hero-figs">{figs_html}</div>
    </div>
    <div class="reveal" style="animation-delay:.12s">{art}</div>
  </div>
</div></section>'''

def ticker(items):
    row = "".join(f'<span>{i} <b>&middot;</b></span>' for i in items)
    return f'<div class="rule"><div class="tk">{row}{row}</div></div>'

def slab(num, label, title=None, sub=None, ink=False):
    t = f'<h2>{title}</h2>' if title else ''
    s = f'<p>{sub}</p>' if sub else ''
    return f'<div class="slabel"><div class="n">{num} &mdash; {label}</div>{t}{s}</div>'

def sec(anchor, num, label, title, sub, inner, cls="paper"):
    return f'''<section class="band {cls}" id="{anchor}"><div class="wrap split">
      {slab(num,label,title,sub,ink=(cls=="ink"))}<div>{inner}</div></div></section>'''

def index_rows(rows):
    out = '<div class="idx">'
    for n, t, tag, d in rows:
        out += (f'<div class="row"><span class="rn">{n}</span><h3>{t}</h3>'
                f'<span class="rt">{tag}</span><p class="rd">{d}</p></div>')
    return out + '</div>'

def proof(num, label, statement):
    return f'''<section class="band ink"><div class="wrap split">
      {slab(num,label,ink=True)}<p class="state">{statement}</p></div></section>'''

def strip(anchor, num, label, sub, cards, cls="ink"):
    c = ""
    for grad, k, h in cards:
        c += f'<div class="scard"><div class="im {grad}"><span class="pl"></span></div><div class="cap"><div class="k">{k}</div><h4>{h}</h4></div></div>'
    return f'''<section class="band {cls}" id="{anchor}"><div class="wrap split">
      {slab(num,label,sub=sub,ink=(cls=="ink"))}<div class="strip-h">{c}</div></div></section>'''

def compare(num, label, title, sub, win_t, lose_t, win_items, lose_items):
    wi = "".join(f'<div class="ci"><span class="mk yes">&#10003;</span><span>{x}</span></div>' for x in win_items)
    li = "".join(f'<div class="ci"><span class="mk no">&times;</span><span>{x}</span></div>' for x in lose_items)
    inner = (f'<div class="cmp"><div class="col win"><div class="ct"><span class="pn" style="width:10px;height:10px;border-radius:50%;background:var(--mag);display:inline-block"></span>{win_t}</div>{wi}</div>'
             f'<div class="col"><div class="ct">{lose_t}</div>{li}</div></div>')
    return sec("s"+num, num, label, title, sub, inner, "paper")

def funnel(num, label, title, sub, stages):
    fs = "".join(f'<div class="fstage s{i+1}"><b>{t}</b><span>{v}</span></div>' for i, (t, v) in enumerate(stages))
    return sec("s"+num, num, label, title, sub, f'<div class="funnel">{fs}</div>', "paper")

def clusters(num, label, title, sub, pillar, chips):
    ch = "".join(f'<span class="chip">{c}</span>' for c in chips)
    inner = f'<div class="clus"><div class="pillar">{pillar}</div><div class="cline"></div><div class="chips">{ch}</div></div>'
    return sec("s"+num, num, label, title, sub, inner, "paper")

def coverage(num, label, title, sub, areas):
    a = "".join(f'<div class="area"><span class="pn"></span>{x}</div>' for x in areas)
    return sec("s"+num, num, label, title, sub, f'<div class="cov">{a}</div>', "paper")

def process(num, label, title, steps, cls="ink"):
    st = ""
    for i, (t, d) in enumerate(steps, 1):
        st += f'<div class="st3"><div class="bn">0{i}</div><div><h4>{t}</h4><p>{d}</p></div></div>'
    return sec("s"+num, num, label, title, None, f'<div class="steps3">{st}</div>', cls)

def faq(num, faqs):
    q = '<div class="faq3">'
    for it in faqs:
        q += (f'<details class="q3"><summary>{it["q"]}<span class="pm"></span></summary>'
              f'<div class="a3">{it["a"]}</div></details>')
    return sec("s"+num, num, "FAQ", "Questions, answered.", None, q + '</div>', "paper")

def cta(h2, sub, related):
    rel = " &middot; ".join(f'<a href="{u}">{t}</a>' for t, u in related)
    return f'''<section class="cta3"><div class="wrap cta3-in reveal">
      <h2>{h2}</h2><p>{sub}</p>
      <div class="hero-cta"><a class="btn b-dark" href="{SITE}/contact/">Get a free proposal <span class="ar">&#8599;</span></a>
        <a class="btn b-ld" href="{SITE}/sanctify-facility/">View all services</a></div>
      <p class="rel">Related: {rel}</p></div></section>'''

def schema(d, url):
    g = [
     {"@type":"Service","@id":url+"#service","name":d["schema_name"],"serviceType":d["schema_name"],
      "url":url,"areaServed":{"@type":"Place","name":d.get("area","Goa, India")},
      "provider":{"@type":"Organization","name":"Sanctify","url":SITE+"/","areaServed":"Goa, India"},
      "description":d["meta_desc"]},
     {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q["q"],
      "acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',q["a"])}} for q in d["faq"]]},
     {"@type":"BreadcrumbList","@id":url+"#bc","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
      {"@type":"ListItem","position":2,"name":"Facility","item":SITE+"/sanctify-facility/"},
      {"@type":"ListItem","position":3,"name":d["title"],"item":url}]}]
    return '<script type="application/ld+json">\n%s\n</script>' % json.dumps(
        {"@context":"https://schema.org","@graph":g}, indent=2, ensure_ascii=False)

# ---------------- hero visuals ----------------
def art_feed():
    return '''<div class="feed">
      <div class="tileF g1 tall"><span class="pl"></span></div>
      <div class="tileF g3"><span class="pl"></span></div>
      <div class="tileF g2"><span class="pl"></span></div>
      <div class="tileF g4 wide"><span class="pl"></span></div>
      <div class="tileF g5"><span class="pl"></span></div>
      <span class="chipF" style="top:-14px;right:8px"><span class="d"></span>+312 leads / mo</span>
      <span class="chipF" style="bottom:-12px;left:-16px"><span class="d"></span>45k reach</span>
    </div>'''

def art_map(cap, rows):
    r = ""
    for i, (nm, meta, top) in enumerate(rows, 1):
        r += f'<div class="prow{" top" if top else ""}"><span class="prk">{i}</span><span><span class="nm">{nm}</span><br><span class="rt2">{meta}</span></span></div>'
    return f'''<div class="card"><div class="mp"><span class="rd0 rdA"></span><span class="rd0 rdB"></span>
      <span class="pin0"></span><span class="pin0 s p2"></span><span class="pin0 s p3"></span></div>
      <div class="pack"><h5>{cap}</h5>{r}</div></div>'''

def art_dash():
    bars = "".join(f'<i style="height:{h}%"></i>' for h in [34,44,40,58,66,76,90])
    return f'''<div class="card dash">
      <div class="dbig"><b>6.8x</b><span>&#9650; ROAS</span></div>
      <div class="dcap">Return on ad spend &mdash; last 90 days</div>
      <div class="bars">{bars}</div>
      <div class="dstats"><div class="dstat"><b>&#8377;19</b><span>Avg. cost / lead</span></div>
        <div class="dstat"><b>143%</b><span>Conversions &#9650;</span></div></div></div>'''

def art_serp():
    return '''<div class="card serp">
      <div class="srow win"><span class="srk">1</span><span style="flex:1"><span class="stt">Your brand &mdash; the answer Google shows first</span><span class="sl"></span><span class="sl s2"></span></span></div>
      <div class="srow"><span class="srk">2</span><span style="flex:1"><span class="stt">competitor-a.in</span><span class="sl"></span></span></div>
      <div class="srow"><span class="srk">3</span><span style="flex:1"><span class="stt">competitor-b.com</span><span class="sl"></span></span></div>
      <div class="spk"><div class="lb"><span>Organic traffic</span><b>&#9650; 218%</b></div>
        <svg viewBox="0 0 300 60" style="width:100%;height:52px"><defs><linearGradient id="s3g" x1="0" x2="1"><stop offset="0" stop-color="#ff0066"/><stop offset="1" stop-color="#7b2ff7"/></linearGradient></defs>
        <path d="M0 50 C40 46 60 34 100 32 S170 20 210 15 260 6 300 5" fill="none" stroke="url(#s3g)" stroke-width="3"/></svg></div></div>'''
print("v3 renderers loaded")



# ---------------- page meta (title / SEO / faq / related) ----------------
F = "/sanctify-facility/"
L = {  # internal links
 "smm":SITE+F+"social-media-marketing-agency-goa/","local":SITE+F+"local-seo-services-goa/",
 "ppc":SITE+F+"ppc-google-ads-agency-goa/","content":SITE+F+"content-marketing-agency-goa/",
 "seo":SITE+F+"search-engine-optimization-seo-company-in-goa-india/","infl":SITE+F+"influencer-marketing-agency-goa/",
 "north":SITE+"/digital-marketing-agency-north-goa/","south":SITE+"/digital-marketing-agency-south-goa/",
 "hub":SITE+"/digital-marketing-agency-goa/"}

PAGES = {}
PAGES["social-media-marketing-agency-goa"] = dict(id=6977, url_path=F+"social-media-marketing-agency-goa/",
 title="Social Media Marketing Agency in Goa",
 meta_title="Social Media Marketing Agency in Goa | Instagram &amp; Meta Ads | Sanctify",
 meta_desc="Sanctify is a social media marketing agency in Goa - strategy, reels, paid social and community management on Instagram, Facebook, YouTube & LinkedIn. Built for Goa brands, measured on results.",
 schema_name="Social Media Marketing", area="Goa, India",
 faq=[
  {"q":"How much does social media marketing cost in Goa?","a":"Pricing depends on platforms, content volume and ad spend. We offer flexible monthly retainers scaled to your goals and budget &mdash; ask us for a proposal built around your business."},
  {"q":"Which platforms are best for my business?","a":"For most Goa businesses Instagram and Facebook drive the strongest results, with LinkedIn for B2B and YouTube for video. We recommend the mix based on your audience."},
  {"q":"Do you create the content too?","a":"Yes &mdash; reels, posts, stories, graphics and captions are handled end-to-end by our in-house creative team."},
  {"q":"How soon will I see results?","a":"Engagement and reach improve within the first few weeks; paid campaigns can drive leads almost immediately, while organic growth compounds over months."},
  {"q":"Do you run influencer campaigns in Goa?","a":f"We do &mdash; through our <a href='{L['infl']}'>influencer marketing</a> service we match you with vetted Goa creators and manage the whole collaboration."}],
 related=[("Influencer Marketing",L["infl"]),("PPC &amp; Google Ads",L["ppc"]),("Content Marketing",L["content"])])

PAGES["local-seo-services-goa"] = dict(id=6978, url_path=F+"local-seo-services-goa/",
 title="Local SEO Services in Goa",
 meta_title="Local SEO Services in Goa | Google Business Profile &amp; Map Pack | Sanctify",
 meta_desc="Local SEO services in Goa that win the Google Map Pack and 'near me' searches - Google Business Profile, citations, reviews and location pages that drive calls, visits and bookings.",
 schema_name="Local SEO Services", area="Goa, India",
 faq=[
  {"q":"How long does local SEO take?","a":"Google Business Profile improvements can show within weeks; competitive Map Pack rankings typically build over three to six months of consistent work."},
  {"q":"Do you manage reviews and GBP posts?","a":"Yes &mdash; we optimise the profile, publish regular posts and set up a review-generation flow while helping you respond professionally."},
  {"q":"Can you help a multi-location business?","a":"Absolutely &mdash; we create individual optimised profiles and location pages for each branch across Goa."},
  {"q":"Is local SEO different from regular SEO?","a":f"It overlaps with our <a href='{L['seo']}'>SEO services</a>, but local SEO adds Google Business Profile, map ranking, citations and reviews to win &lsquo;near me&rsquo; searches specifically."}],
 related=[("North Goa",L["north"]),("South Goa",L["south"]),("SEO Services",L["seo"])])

PAGES["ppc-google-ads-agency-goa"] = dict(id=6979, url_path=F+"ppc-google-ads-agency-goa/",
 title="PPC &amp; Google Ads Agency in Goa",
 meta_title="PPC &amp; Google Ads Agency in Goa | Search, Shopping &amp; Meta Ads | Sanctify",
 meta_desc="A PPC & Google Ads agency in Goa that turns ad spend into calls, bookings and sales. Search, Shopping, Performance Max and Meta Ads managed by a certified in-house team, measured on ROAS.",
 schema_name="PPC &amp; Google Ads Management", area="Goa, India",
 faq=[
  {"q":"What&rsquo;s the minimum ad budget to start?","a":"It depends on your industry and goals, but we work with a wide range of Goa budgets and will tell you honestly what a realistic starting spend looks like for your market."},
  {"q":"Is the ad spend separate from your fee?","a":"Yes &mdash; ad spend is paid directly to Google or Meta. Our management fee is separate and scaled to the work and budget involved."},
  {"q":"How soon will I see leads?","a":"Search campaigns can generate enquiries within days of launch because they target people actively searching. We then optimise to bring the cost-per-lead down."},
  {"q":"Do you handle both Google and social ads?","a":f"We do &mdash; and they work best together. We often pair Google Ads with <a href='{L['smm']}'>social media marketing</a> for full-funnel coverage."}],
 related=[("Social Media Marketing",L["smm"]),("Local SEO",L["local"]),("Content Marketing",L["content"])])

PAGES["content-marketing-agency-goa"] = dict(id=6980, url_path=F+"content-marketing-agency-goa/",
 title="Content Marketing Agency in Goa",
 meta_title="Content Marketing Agency in Goa | SEO Content &amp; Strategy | Sanctify",
 meta_desc="A content marketing agency in Goa that builds topical authority - SEO blogs, website copy, video and content strategy that rank, earn trust and turn readers into customers.",
 schema_name="Content Marketing", area="Goa, India",
 faq=[
  {"q":"How is content marketing different from just blogging?","a":"Blogging is one tactic; content marketing is a strategy. We map topics to search demand and buyer journeys, then interlink everything to build authority that compounds."},
  {"q":"Do you write the content or just plan it?","a":"Both &mdash; strategy, writing, editing and publishing are handled by our in-house team. All content is original and written for humans and search engines."},
  {"q":"How does content help my rankings?","a":f"Well-structured content clusters signal topical authority to Google, support your <a href='{L['seo']}'>SEO</a> and earn links and trust &mdash; which lifts rankings across the site."},
  {"q":"When will I see results?","a":"Content is a compounding asset. Early pieces can rank within weeks for low-competition terms, while authority and traffic build meaningfully over three to six months."}],
 related=[("SEO Services",L["seo"]),("Local SEO",L["local"]),("Social Media Marketing",L["smm"])])

def city_meta(pid, slug, region, other, other_url, places):
    return dict(id=pid, url_path="/"+slug+"/", title=f"Digital Marketing Agency in {region}",
     meta_title=f"Digital Marketing Agency in {region} | SEO, Ads &amp; Social | Sanctify",
     meta_desc=f"Sanctify is a digital marketing agency serving {region}, Goa - SEO, Google Ads, social media, web design and content for businesses in {places[0]}, {places[1]} and across {region}.",
     schema_name=f"Digital Marketing Agency in {region}", area=f"{region}, Goa, India",
     faq=[
      {"q":f"Do you work with small businesses in {region}?","a":f"Yes &mdash; from single-location shops and clinics to hotels and multi-branch brands across {region}. We scale the plan to your goals and budget."},
      {"q":"Which services should I start with?","a":f"Most {region} businesses start with <a href='{L['local']}'>local SEO</a> and <a href='{L['ppc']}'>Google Ads</a> for fast, high-intent leads, then add social and content."},
      {"q":f"Do you also serve {other}?","a":f"We do &mdash; we work across all of Goa. See our <a href='{other_url}'>{other}</a> page, or our main <a href='{L['hub']}'>Goa digital marketing</a> hub."},
      {"q":"How do we get started?","a":"Get in touch for a free consultation. We&rsquo;ll audit your current presence and show you the fastest route to more enquiries."}],
     related=[(other,other_url),("SEO Services",L["seo"]),("Local SEO",L["local"])])

PAGES["digital-marketing-agency-north-goa"] = city_meta(6981,"digital-marketing-agency-north-goa","North Goa","South Goa",L["south"],["Panjim","Calangute"])
PAGES["digital-marketing-agency-south-goa"] = city_meta(6982,"digital-marketing-agency-south-goa","South Goa","North Goa",L["north"],["Margao","Vasco da Gama"])

# ---------------- per-page BODIES (distinct structures) ----------------
def body_smm(d):
    rows=[("01","Paid Social Advertising","Meta &middot; IG","High-ROI Instagram &amp; Facebook campaigns &mdash; precise targeting, creative testing and conversion tracking that turn ad spend into <b>measurable bookings and sales</b>."),
          ("02","Content &amp; Reels","Studio","Scroll-stopping reels, posts, stories and graphics produced end-to-end by our in-house creative team."),
          ("03","Strategy &amp; Audit","Monthly","A data-backed plan tuned to your niche, competitors and the way Goa actually buys."),
          ("04","Community Management","Daily","On-brand engagement, comments and DMs that build loyalty and turn followers into regulars."),
          ("05","Influencer &amp; Creator Collabs","Network","Authentic partnerships with 30+ vetted Goa creators that expand reach and trust fast."),
          ("06","Analytics &amp; Reporting","Always","Clear monthly reporting on the metrics that grow revenue &mdash; not vanity likes.")]
    cards=[("g1","Reel","Launch teaser that hit 45k views"),("g2","Campaign","Festive paid-social, 6.8x ROAS"),
           ("g4","UGC","Creator series for a Goa caf&eacute;"),("g5","Story","Booking-driving story funnel")]
    steps=[("Discover","We audit your presence, competitors and audience, then define clear goals."),
           ("Plan","A monthly content calendar and paid-social roadmap mapped to those goals."),
           ("Create &amp; Launch","Our studio produces the content and launches optimised campaigns."),
           ("Optimise &amp; Scale","We test relentlessly and scale what drives leads, bookings and sales.")]
    return [
     hero("Social Media Marketing","SINCE 2012 &mdash; VASCO &middot; PANJIM, GOA",
      'Make Goa <span class="mag">stop</span><br>scrolling. <span class="thin">Then buy.</span>',
      "We&rsquo;re the in-house social studio for Goa&rsquo;s boldest brands &mdash; strategy, reels, paid social and community that move followers to bookings.",
      art_feed(), [("14","years in Goa"),("500+","campaigns"),("30+","creators")]),
     ticker(["Instagram","Reels &amp; UGC","Meta Ads","Community","Influencer Collabs","Analytics"]),
     sec("s01","01","SERVICES","A full creator studio, in one team.","Everything that grows a Goa brand&rsquo;s social &mdash; under one roof, no outsourcing.", index_rows(rows),"paper"),
     proof("02","PROOF",'Fourteen years. <span class="num">500+</span> campaigns. One studio that never <span class="thin">outsources.</span>'),
     strip("s03","03","WHAT WE MAKE","Scroll the kind of content that fills your feed &mdash; and your calendar.",cards,"ink"),
     process("04","HOW WE WORK","From audit to scale.",steps,"paper"),
     faq("05",d["faq"]),
     cta("Let&rsquo;s make your brand<br>impossible to scroll past.","Book a free strategy call and get a custom social plan for your Goa business.",d["related"])]

def body_local(d):
    rows=[("01","Google Business Profile","GBP","Full setup, optimisation, categories, services and weekly posts that keep you ranking and clickable."),
          ("02","Local Keyword SEO","On-page","Optimisation for local, high-intent &lsquo;near me&rsquo; searches across your service areas."),
          ("03","Citations &amp; NAP","Directories","Consistent name, address and phone across the listings that actually move rankings."),
          ("04","Reviews &amp; Reputation","Trust","Review-generation flows and reputation management that build the stars buyers judge you on."),
          ("05","Location Pages","Pages","Optimised service-area and city landing pages that rank and convert."),
          ("06","Map Pack Tracking","Reporting","Local rank tracking and clear monthly reporting on movement.")]
    steps=[("Audit","We assess your GBP, citations and current local rankings."),
           ("Optimise","Profile, on-page and citation cleanup and build-out."),
           ("Content","Location pages, GBP posts and review generation."),
           ("Track","Map Pack tracking and monthly optimisation.")]
    return [
     hero("Local SEO","GOOGLE BUSINESS PROFILE &middot; MAP PACK &middot; GOA",
      'Own the <span class="mag">Map Pack</span> in every corner of Goa.',
      "Get found in the Google Map Pack and &ldquo;near me&rdquo; searches across North and South Goa &mdash; and turn local intent into calls, visits and bookings.",
      art_map("Dentists near Panjim",[("Your Business","&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 (128) &middot; Open now",True),
        ("A Competitor Clinic","&#9733;&#9733;&#9733;&#9733;&#9734; 4.2 (54)",False),("Another Listing","&#9733;&#9733;&#9733;&#9733;&#9734; 4.0 (31)",False)]),
      [("Map Pack","3-pack visibility"),("500+","projects"),("4.9","avg. rating")]),
     ticker(["Google Business Profile","Map Pack","Citations","Reviews","Location Pages","&lsquo;Near me&rsquo; SEO"]),
     compare("01","HOW YOU SHOW UP","Optimised vs. left alone.","The same business, two very different results in local search.",
       "With Sanctify","A typical un-managed listing",
       ["Ranks in the 3-pack for &lsquo;near me&rsquo; searches","Complete, category-rich Google Business Profile","Steady flow of fresh reviews","Consistent citations across directories","Location pages that rank"],
       ["Buried below the map","Half-filled profile, wrong categories","Reviews stall and go unanswered","Inconsistent name/address/phone","No local landing pages"]),
     sec("s02","02","SERVICES","Everything that fills the map.","A complete local-visibility system engineered for ready-to-buy customers nearby.", index_rows(rows),"paper2"),
     process("03","HOW WE WORK","Our local SEO process.",steps,"ink"),
     faq("04",d["faq"]),
     cta("Own your local market.","Rank in the Map Pack across North and South Goa and turn local searches into customers.",d["related"])]

def body_ppc(d):
    rows=[("01","Google Search &amp; PMax","High intent","Search, Performance Max and Shopping campaigns that capture people actively looking for what you sell."),
          ("02","Meta &amp; Instagram Ads","Demand","Prospecting and retargeting that fills the top of the funnel and brings them back."),
          ("03","Conversion Tracking","GA4","Proper GA4 and pixel setup so every rupee is measured against real leads and sales."),
          ("04","Landing Pages","CRO","Fast, focused pages built to turn ad clicks into enquiries."),
          ("05","Remarketing","Recover","Win back the visitors who didn&rsquo;t convert the first time."),
          ("06","ROAS Reporting","Clarity","Transparent reporting on spend, leads and return &mdash; no black box.")]
    stages=[("Impressions","1.2M / mo"),("Clicks","38k"),("Leads","+312"),("Booked customers","6.8x ROAS")]
    steps=[("Audit &amp; Plan","We review your account, tracking and competitors, then build a plan."),
           ("Build","Campaigns, keywords, creative and landing pages set up properly."),
           ("Launch &amp; Track","Go live with full conversion tracking from day one."),
           ("Optimise","Weekly optimisation to lower cost-per-lead and grow ROAS.")]
    return [
     hero("PPC &amp; Google Ads","CERTIFIED &middot; SEARCH &middot; SHOPPING &middot; META",
      'Ad spend that comes<br>back as <span class="mag">revenue.</span>',
      "Certified Google Ads &amp; Meta management for Goa businesses &mdash; engineered around conversions, cost-per-lead and return on ad spend, not clicks.",
      art_dash(), [("6.8x","avg. ROAS"),("&#8377;19","cost / lead"),("500+","campaigns")]),
     ticker(["Google Search","Performance Max","Shopping","Meta Ads","Remarketing","Conversion Tracking"]),
     funnel("01","THE FUNNEL","Every click, accounted for.","We build and measure the whole path &mdash; from impression to booked customer.",stages),
     sec("s02","02","SERVICES","Full-funnel paid media.","From first click to booked customer &mdash; built, tracked and optimised for return.", index_rows(rows),"paper"),
     proof("03","PROOF",'<span class="num">6.8x</span> average return. <span class="num">&#8377;19</span> cost per lead. Zero <span class="thin">guesswork.</span>'),
     process("04","HOW WE WORK","Our PPC process.",steps,"paper"),
     faq("05",d["faq"]),
     cta("Turn your ad budget<br>into booked customers.","Get a free account audit and a paid-media plan built around your ROAS targets.",d["related"])]

def body_content(d):
    rows=[("01","SEO Blog &amp; Articles","Ranking","Search-optimised articles targeting the questions your customers actually ask &mdash; the foundation of topical authority."),
          ("02","Content Strategy","Roadmap","A topic map and editorial calendar tied to real search demand."),
          ("03","Website &amp; Landing Copy","Convert","Clear, persuasive copy that turns visitors into enquiries."),
          ("04","Video &amp; Scripts","Reach","Short-form scripts and video content that travels."),
          ("05","Topical Authority","Clusters","Interlinked content clusters that make Google trust your site."),
          ("06","Email &amp; Newsletters","Nurture","Sequences that keep leads warm until they&rsquo;re ready.")]
    steps=[("Research","Keyword, intent and competitor research to find the gaps."),
           ("Plan","A topic map and editorial calendar built around demand."),
           ("Create","Original, SEO-optimised content produced and edited in-house."),
           ("Distribute","Publish, interlink, promote and measure what performs.")]
    return [
     hero("Content Marketing","SEO CONTENT &middot; STRATEGY &middot; GOA",
      'Content that <span class="mag">ranks,</span><br>earns trust &amp; sells.',
      "SEO-led content that makes your brand the answer people find in Goa &mdash; strategy, blogs, website copy, video and topical authority.",
      art_serp(), [("218%","avg. traffic lift"),("500+","pieces produced"),("14","years")]),
     ticker(["Content Strategy","SEO Blogs","Website Copy","Topical Authority","Video","Email"]),
     clusters("01","TOPICAL AUTHORITY","We build clusters, not one-off posts.","One pillar, many supporting articles, all interlinked &mdash; so the whole site rises.",
       "Pillar: Digital Marketing in Goa",["Social media tips","Local SEO guide","Google Ads costs","Best time to post","Hiring an agency","Content calendar","Review strategy","Web design basics"]),
     sec("s02","02","SERVICES","Words and stories that build authority.","A content engine that compounds &mdash; every piece supports the next.", index_rows(rows),"paper"),
     process("03","HOW WE WORK","Our content process.",steps,"ink"),
     faq("04",d["faq"]),
     cta("Become the answer<br>Goa searches for.","Get a content strategy session and a topic map built around what your customers search.",d["related"])]

def body_city(d, region, places, areas, pack_cap, pack_rows):
    rows=[("01","SEO &amp; Local SEO","Search",f"Rank on Google and in the Map Pack for {region} &lsquo;near me&rsquo; searches that bring ready-to-buy customers."),
          ("02","Google &amp; Meta Ads","Paid","High-ROI Search, Shopping and social campaigns that drive leads fast."),
          ("03","Social Media","Brand","Content and community that grows your local audience."),
          ("04","Web Design","Convert","Fast, mobile-first websites built to turn visitors into enquiries."),
          ("05","Content Marketing","Authority","SEO content that builds trust and topical authority."),
          ("06","Analytics","Proof","Tracking and reporting tied to leads and revenue.")]
    steps=[("Discover",f"We learn your goals, market and {region} competitors."),
           ("Strategy","A channel plan built around your best opportunities."),
           ("Execute","Search, ads, social, web and content, delivered in-house."),
           ("Optimise","Continuous improvement tied to leads and revenue.")]
    return [
     hero(f"Digital Marketing &middot; {region}","EVERY CHANNEL, ONE TEAM &middot; GOA",
      f'The digital partner<br>{region} <span class="mag">brands trust.</span>',
      f"Full-service digital marketing for businesses across {region} &mdash; from {places[0]} to {places[1]}. SEO, ads, social, web and content, all under one roof.",
      art_map(pack_cap, pack_rows), [("#1",f"for {region} marketing"),("14","years in Goa"),("500+","projects")]),
     ticker(["SEO","Google Ads","Social Media","Web Design","Local SEO","Content"]),
     coverage("01","COVERAGE",f"We work across {region}.",f"On the ground from {places[0]} to {places[1]} &mdash; not a remote agency guessing.",areas),
     sec("s02","02","SERVICES",f"Everything {region} businesses need to grow online.","One team for search, ads, social, web and content &mdash; pulling in the same direction.", index_rows(rows),"paper"),
     proof("03","WHY US",f'Ranked <span class="num">#1</span> in {region}. <span class="num">14</span> years local. One accountable <span class="thin">team.</span>'),
     process("04","HOW WE WORK","How we grow your business.",steps,"paper"),
     faq("05",d["faq"]),
     cta(f"Grow your business<br>across {region}.",f"Book a free consultation and get a plan tailored to your {region} audience.",d["related"])]

BODIES = {
 "social-media-marketing-agency-goa": lambda d: body_smm(d),
 "local-seo-services-goa": lambda d: body_local(d),
 "ppc-google-ads-agency-goa": lambda d: body_ppc(d),
 "content-marketing-agency-goa": lambda d: body_content(d),
 "digital-marketing-agency-north-goa": lambda d: body_city(d,"North Goa",["Panjim","Mapusa"],
   ["Panjim","Calangute","Candolim","Mapusa","Anjuna","Baga","Porvorim","Assagao","Siolim","Vagator","Morjim","Arpora"],
   "Marketing agency in North Goa",[("Your Business","&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 &middot; Panjim",True),
    ("A Competitor","&#9733;&#9733;&#9733;&#9733;&#9734; 4.3 &middot; Mapusa",False),("Another Agency","&#9733;&#9733;&#9733;&#9733;&#9734; 4.1 &middot; Calangute",False)]),
 "digital-marketing-agency-south-goa": lambda d: body_city(d,"South Goa",["Margao","Vasco"],
   ["Margao","Vasco da Gama","Colva","Benaulim","Ponda","Cortalim","Verna","Cansaulim","Betalbatim","Fatorda","Chicalim","Majorda"],
   "Marketing agency in South Goa",[("Your Business","&#9733;&#9733;&#9733;&#9733;&#9733; 4.9 &middot; Vasco",True),
    ("A Competitor","&#9733;&#9733;&#9733;&#9733;&#9734; 4.2 &middot; Margao",False),("Another Agency","&#9733;&#9733;&#9733;&#9733;&#9734; 4.0 &middot; Colva",False)]),
}

PREVIEW_DOC = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} (preview)</title>{fonts}
<style>body{{margin:0;background:#0e0b14;font-family:'Inter',sans-serif}}
.pv-nav{{display:flex;align-items:center;justify-content:space-between;max-width:1200px;margin:0 auto;padding:20px 28px;background:#0e0b14}}
.pv-logo{{font-family:'Space Grotesk';font-weight:700;font-size:22px;letter-spacing:-.02em;color:#fff}}.pv-logo b{{color:#ff0066}}
.pv-menu{{display:flex;gap:24px;font-size:14px;color:#b7b1c4;font-weight:500}}
.pv-foot{{background:#0e0b14;color:#8a8296;text-align:center;padding:40px 20px;font-size:13px}}</style></head>
<body><div class="pv-nav"><div class="pv-logo">SANCT<b>I</b>FY</div>
<div class="pv-menu"><span>Work</span><span>About</span><span>Services</span><span>Journal</span><span>Contact</span></div></div>
{body}<div class="pv-foot">SANCTIFY &middot; Vasco-da-Gama, Goa &middot; &copy; 2012&ndash;2026</div></body></html>"""

def build_content_html(slug, d):
    url = SITE + d["url_path"]
    body = "\n".join(BODIES[slug](d))
    return "\n".join([FONTS, CSS, '<div class="sfy3">', body, '</div>', schema(d, url)])

def main():
    for slug, d in PAGES.items():
        content = build_content_html(slug, d)
        open(os.path.join(BUILD, slug + ".content.html"), "w").write(content)
        json.dump({"content":content,"meta":{"_seopress_titles_title":d["meta_title"],"_seopress_titles_desc":d["meta_desc"]}},
                  open(os.path.join(BUILD, slug + ".payload.json"), "w"))
        open(os.path.join(PREVIEW, slug + ".html"), "w").write(
            PREVIEW_DOC.format(title=re.sub('<[^>]+>','',d["title"]), fonts=FONTS, body=content))
        print(f"  built {slug:38s} id={d['id']} {len(content):6d}B")
    print("done.")

if __name__ == "__main__":
    main()
