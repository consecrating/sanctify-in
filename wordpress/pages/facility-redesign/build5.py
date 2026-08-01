#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build4 — rebuild 6 Sanctify facility/landing pages NATIVELY in the site's own
sf-* design system (magenta/violet, Poppins), matching about-sanctify + sanctify-facility.
Self-contained: each page inlines the full sf CSS + a scoped reveal/counter/parallax JS
+ <noscript> fallback so it NEVER renders blank (the live parent has that bug).
Honest brand-level stats only (no fabricated performance metrics)."""
import json, os, html

SITE = "https://www.sanctify.in"
WA   = "https://wa.me/919923352923"
TEL  = "tel:+919923352923"
CONTACT = SITE + "/contact/"
FACILITY = SITE + "/sanctify-facility/"
BG_ABSTRACT = SITE + "/wp-content/uploads/2026/07/sanctify-about-abstract-bg.png"

os.makedirs("build5", exist_ok=True)
os.makedirs("preview5", exist_ok=True)

# ---------- icons (stroke, 24x24) ----------
IC = {
 "chart":'<path d="M3 3v18h18"/><path d="M7 14l3-3 3 3 5-6"/>',
 "search":'<circle cx="11" cy="11" r="7"/><path d="M21 21l-4-4"/>',
 "pin":'<path d="M12 21s-7-6.5-7-11a7 7 0 1114 0c0 4.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/>',
 "star":'<path d="M12 2l2.2 6.3L21 10.5l-5.6 4.1L17 21l-5-3.6L7 21l1.6-6.4L3 10.5l6.8-2.2z"/>',
 "users":'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
 "reel":'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M10 9l5 3-5 3z"/>',
 "mega":'<path d="M3 10v4h4l5 5V5L7 10z"/><path d="M16 8a5 5 0 010 8"/>',
 "pen":'<path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18z"/>',
 "doc":'<path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9z"/><path d="M14 3v6h6"/>',
 "target":'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
 "cursor":'<path d="M4 3l7 18 2-8 8-2z"/>',
 "mail":'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
 "shield":'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "compass":'<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
 "cart":'<path d="M6 6h15l-1.6 9H7z"/><circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M6 6L5 3H2"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 "cal":'<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/>',
 "layout":'<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 9h20M9 9v11"/>',
 "spark":'<path d="M12 2v6M12 16v6M2 12h6M16 12h6M5 5l3 3M16 16l3 3M19 5l-3 3M8 16l-3 3"/>',
 "link":'<path d="M10 14a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1"/><path d="M14 10a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/>',
 "grid":'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
}
ARW = '<svg class="sf-arw" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" style="width:14px;height:14px"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def svg(ic):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">'+IC[ic]+'</svg>')

def e(s): return html.escape(s, quote=True)

# ---------- component renderers ----------
def eyebrow(txt, light=False):
    c = " sf-eyebrow-lt" if light else ""
    return f'<span class="sf-eyebrow{c}">{e(txt)}</span>'

def hero_light(d):
    stats = "".join(f'<div><b>{e(b)}</b><span>{e(s)}</span></div>' for b,s in d["hero_stats"])
    return f'''<section class="sf-hero sf-hero-anim">
 <div class="sf-hero-inner">
  <div class="sf-hero-text">
   {eyebrow(d["eyebrow"])}
   <h1 class="sf-h1">{d["h1"]}</h1>
   <p class="sf-lead">{d["lead"]}</p>
   <div class="sf-hero-cta">
    <a class="sf-btn sf-btn-p" href="{CONTACT}">Get a Free Consultation {ARW}</a>
    <a class="sf-btn sf-btn-g" href="{WA}" target="_blank" rel="noopener">WhatsApp Us</a>
   </div>
   <div class="sf-stats">{stats}</div>
  </div>
  <div class="sf-hero-media"><span class="sf-glow"></span><img src="{d["img"]}" alt="{e(d["img_alt"])}" loading="eager" width="1024" height="1024"></div>
 </div>
</section>'''

def hero_dark(d):
    return f'''<section class="sf-px sf-px-hero" data-px>
 <div class="sf-px-bg" style="background-image:url('{d["img"]}')"></div>
 <canvas id="sf-smoke" class="sf-smoke" aria-hidden="true"></canvas>
 <div class="sf-px-ov"></div>
 <div class="sf-px-inner">
  {eyebrow(d["eyebrow"], light=True)}
  <h1 class="sf-px-h1">{d["h1"]}</h1>
  <p class="sf-px-sub">{d["lead"]}</p>
  <div class="sf-hero-cta" style="justify-content:center;margin-top:26px">
   <a class="sf-btn sf-btn-w" href="{CONTACT}">Get a Free Consultation {ARW}</a>
   <a class="sf-btn sf-btn-go" href="{WA}" target="_blank" rel="noopener">WhatsApp Us</a>
  </div>
 </div>
</section>'''

def sec_head(eb, h2, p):
    return f'''<div class="sf-sec-head sf-reveal">
  {eyebrow(eb)}
  <h2 class="sf-h2">{h2}</h2>
  <p>{p}</p>
 </div>'''

def two(eb, h2, paras, quote, by):
    ps = "".join(f"<p>{x}</p>" for x in paras)
    return f'''<section class="sf-two">
 <div class="sf-two-l sf-reveal">
  {eyebrow(eb)}
  <h2 class="sf-h2">{h2}</h2>
  {ps}
 </div>
 <aside class="sf-quote sf-reveal" style="--d:120ms">
  <span class="sf-qmark">&ldquo;</span>
  <p>{quote}</p>
  <span class="sf-qby">{e(by)}</span>
 </aside>
</section>'''

def grid(cards, cols=3):
    out = []
    for i,(ic,h3,p,href) in enumerate(cards):
        d = (i % cols) * 70
        tag_o = f'<a class="sf-card sf-reveal" style="--d:{d}ms" href="{href}">' if href else f'<div class="sf-card sf-reveal" style="--d:{d}ms">'
        tag_c = "</a>" if href else "</div>"
        more = f'<span class="sf-more">Learn more {ARW}</span>' if href else ""
        out.append(f'{tag_o}<span class="sf-ic">{svg(ic)}</span><span class="sf-card-b"><h3>{e(h3)}</h3><p>{e(p)}</p>{more}</span>{tag_c}')
    return f'<div class="sf-grid">{"".join(out)}</div>'

def dark_services(eb, h2, p, cards):
    out = []
    for i,(ic,h3,txt,href) in enumerate(cards):
        d = (i % 3) * 90
        tag_o = f'<a class="sf-dcard sf-reveal" style="--d:{d}ms" href="{href}">' if href else f'<div class="sf-dcard sf-reveal" style="--d:{d}ms">'
        tag_c = "</a>" if href else "</div>"
        out.append(
            f'{tag_o}<span class="sf-dcard-fx"></span>'
            f'<span class="sf-dic">{svg(ic)}</span>'
            f'<span class="sf-dhead"><span class="sf-dline"></span><h3>{e(h3)}</h3><span class="sf-dline"></span></span>'
            f'<p>{e(txt)}</p>{tag_c}')
    return f'''<section class="sf-dark">
 <div class="sf-dark-bg"></div>
 <canvas id="sf-smoke2" class="sf-smoke" aria-hidden="true"></canvas>
 <div class="sf-dark-in">
  <div class="sf-sec-head sf-reveal sf-sec-head-lt">
   <span class="sf-eyebrow sf-eyebrow-lt">{e(eb)}</span>
   <h2 class="sf-h2">{h2}</h2>
   <p>{p}</p>
  </div>
  <div class="sf-dgrid">{"".join(out)}</div>
 </div>
</section>'''

def steps(items):
    out = []
    for i,(ic,h3,p) in enumerate(items):
        out.append(f'<div class="sf-step sf-reveal" style="--d:{i*90}ms" tabindex="0"><span class="sf-step-no">{i+1:02d}</span><span class="sf-ic">{svg(ic)}</span><h3>{e(h3)}</h3><p>{e(p)}</p></div>')
    return f'<div class="sf-steps">{"".join(out)}</div>'

def chips(items):
    out = "".join(f'<span class="sf-chip sf-reveal" style="--d:{i*45}ms">{e(x)}</span>' for i,x in enumerate(items))
    return f'<div class="sf-chips">{out}</div>'

def band(stats):
    inner = "".join(f'<div><b data-count="{n}" data-suf="{suf}">0</b><span>{e(lbl)}</span></div>' for n,suf,lbl in stats)
    return f'''<section class="sf-px sf-px-band" data-px>
 <div class="sf-px-bg" style="background-image:url('{BG_ABSTRACT}')"></div>
 <div class="sf-px-ov sf-px-ov-d"></div>
 <div class="sf-px-inner"><div class="sf-stats sf-stats-lt">{inner}</div></div>
</section>'''

def faq(items):
    rows = "".join(f'<details><summary>{e(q)}</summary><div class="sf-faq-a">{e(a)}</div></details>' for q,a in items)
    return f'<div class="sf-faq">{rows}</div>'

def cta(h2, p):
    return f'''<section class="sf-cta sf-reveal">
 <div class="sf-cta-in">
  <h2>{e(h2)}</h2>
  <p>{e(p)}</p>
  <div class="sf-hero-cta">
   <a class="sf-btn sf-btn-w" href="{CONTACT}">Start a Project {ARW}</a>
   <a class="sf-btn sf-btn-go" href="{TEL}">Call +91 99233 52923</a>
  </div>
 </div>
</section>'''

def services_section(eb, h2, p, body):
    return f'<section class="sf-services">\n {sec_head(eb,h2,p)}\n {body}\n</section>'

BRAND_BAND = [("14","+","Years of excellence"),("500","+","Projects delivered"),
              ("18","","Services in-house"),("6","+","Industries served")]
HERO_STATS = [("14+","Years"),("18","Services"),("500+","Projects"),("100%","In-house")]

# service card set reused for city pages
def city_services():
    return [
     ("search","Search Engine Optimization","Rank higher on Google with technical, on-page and content SEO.", SITE+"/sanctify-facility/best-search-engine-optimization-seo-company-in-goa-india/"),
     ("reel","Social Media Marketing","Instagram, Facebook & reels content that grows and engages your audience.", SITE+"/sanctify-facility/social-media-marketing-agency-goa/"),
     ("target","Google & Meta Ads","Search, Performance Max & social ads managed for qualified enquiries.", SITE+"/sanctify-facility/ppc-google-ads-agency-goa/"),
     ("layout","Web Design & Development","Fast, responsive, conversion-focused websites that sell around the clock.", SITE+"/sanctify-facility/web-designing-company-in-goa-india/"),
     ("pin","Local SEO & Map Pack","Google Business Profile and local rankings that bring nearby customers.", SITE+"/sanctify-facility/local-seo-services-goa/"),
     ("pen","Content & Branding","Strategy-led content and visual identity that build authority.", SITE+"/sanctify-facility/content-marketing-agency-goa/"),
    ]

# ---------- per-page content ----------
PAGES = {
 6977: dict(
  slug="social-media-marketing-agency-goa", hero="dark", img_id=7011,
  eyebrow="Social Media Marketing · Goa",
  h1='Social media that <span>builds brands, not just posts</span>',
  lead="We plan, create and manage scroll-stopping social content and paid campaigns for Goa businesses - turning followers into customers.",
  img_alt="Social media marketing agency in Goa - Sanctify",
  title="Social Media Marketing Agency in Goa | Instagram & Meta | Sanctify",
  desc="Sanctify is a social media marketing agency in Goa managing Instagram, Facebook & paid social. Content, reels, ads & influencer campaigns that grow your brand.",
  two=("Why social","Social media built for measurable growth",
     ["A polished feed is not the goal - <strong>business results</strong> are. We combine brand storytelling with performance advertising so every post, reel and campaign moves someone closer to becoming a customer.",
      "From boutique hotels to restaurants, salons and retail across Goa, we run social accounts that stay consistent, on-brand and genuinely engaging - backed by our <a href=\""+SITE+"/sanctify-facility/ppc-google-ads-agency-goa/\">paid ads</a> and <a href=\""+SITE+"/sanctify-facility/content-marketing-agency-goa/\">content</a> teams."],
     "We treat your social growth as our own - no vanity metrics, just brand and business results.","The Sanctify Philosophy"),
  grid_head=("What we do","A complete social media service","Everything needed to plan, produce and grow your social presence - handled by one in-house team."),
  grid=[("reel","Instagram & Facebook Management","Day-to-day management, posting and growth across your core social channels.",None),
        ("spark","Content & Reels Production","Photo, short-form video and reels crafted to stop the scroll and get shared.",None),
        ("target","Paid Social Advertising","Meta ads that put your brand in front of the right Goa audience and drive enquiries.",None),
        ("users","Influencer Collaborations","Creator partnerships in Goa that turn authentic reach into real bookings.",None),
        ("mail","Community Management","Comments, DMs and reviews handled promptly to build trust and loyalty.",None),
        ("chart","Reporting & Insights","Clear monthly reporting on what worked, what grew and what is next.",None)],
  chips_head=("Platforms","Where we grow your brand","We manage and advertise across every platform that matters for Goa businesses."),
  chips=["Instagram","Facebook","YouTube","LinkedIn","Google Business","WhatsApp"],
  steps_head=("How we work","From strategy to results","A clear, repeatable process that keeps your social presence consistent and effective."),
  steps=[("compass","Audit & Strategy","We review your brand, audience and competitors to set a clear direction."),
         ("cal","Content Calendar","A month of planned posts, reels and campaigns aligned to your goals."),
         ("reel","Publish & Engage","We publish consistently and actively engage your growing community."),
         ("chart","Measure & Optimise","Monthly insights guide the next cycle so results compound over time.")],
  faq=[("Which social media platforms do you manage?","We manage Instagram, Facebook, YouTube, LinkedIn, Google Business Profile and WhatsApp, focusing on the platforms where your customers actually spend time."),
       ("Do you create the content or do we?","Our in-house team handles it end to end - strategy, photography, short-form video, reels and captions - though we love collaborating with brands that have their own assets too."),
       ("Do you also run paid social ads?","Yes. Alongside organic management we plan and manage Meta (Instagram & Facebook) ad campaigns designed to drive enquiries, not just reach."),
       ("How soon will we see results?","Organic growth is a steady build over weeks and months; paid campaigns can drive enquiries much faster. We report clearly every month so you always see progress.")],
  cta=("Ready to grow your social presence?","Let's turn your social channels into a real growth engine for your Goa business."),
 ),
 6978: dict(
  slug="local-seo-services-goa", hero="light", img_id=7012,
  eyebrow="Local SEO · Google Business Profile",
  h1='Get found first in <span>local Goa searches</span>',
  lead="We optimise your Google Business Profile, map pack presence and local rankings so nearby customers discover and choose you first.",
  img_alt="Local SEO services in Goa - Google Business Profile and map pack - Sanctify",
  title="Local SEO Services in Goa | Google Business Profile & Map Pack | Sanctify",
  desc="Local SEO services in Goa by Sanctify - Google Business Profile optimisation, map pack rankings, citations and reviews that bring nearby customers to your door.",
  two=("Why local SEO","When customers search nearby, you should be first",
     ["Most people looking for a service in Goa search on Google and pick from the top few local results. If your business is not in that <strong>map pack</strong>, those customers go to a competitor instead.",
      "We make sure your Google Business Profile, local citations and website all point in the same direction - so you show up when it matters. It pairs perfectly with our <a href=\""+SITE+"/sanctify-facility/best-search-engine-optimization-seo-company-in-goa-india/\">SEO</a> and <a href=\""+SITE+"/sanctify-facility/content-marketing-agency-goa/\">content</a> work."],
     "Being visible to nearby customers at the exact moment they are ready to buy is the highest-intent marketing there is.","The Sanctify Philosophy"),
  grid_head=("What we do","A complete local SEO service","Everything needed to dominate local search and the Google map pack across Goa."),
  grid=[("pin","Google Business Profile Optimisation","Complete setup and optimisation of your profile for maximum local visibility.",None),
        ("search","Local Keyword & Map Rankings","Targeting the searches nearby customers actually use to find your services.",None),
        ("link","Citations & Directory Listings","Consistent business listings across the directories Google trusts.",None),
        ("star","Review Generation & Management","Systems to earn more genuine reviews and respond to them professionally.",None),
        ("doc","Localised On-Page SEO","Location-focused pages and content that help you rank in your area.",None),
        ("globe","Local Link Building","Relevant local links and mentions that build authority and trust.",None)],
  chips_head=("Areas we serve","Local SEO across Goa","We help businesses get found in their town and neighbourhood, right across the state."),
  chips=["Panaji","Margao","Vasco","Mapusa","Ponda","Calangute","Candolim","Porvorim"],
  steps_head=("How we work","A clear path to the map pack","A structured process that steadily lifts your local visibility and rankings."),
  steps=[("compass","Local Audit","We assess your profile, listings, reviews and current local rankings."),
         ("shield","Optimise & Fix","We correct inconsistencies and fully optimise your profile and pages."),
         ("link","Build Authority","Citations, reviews and local links strengthen your local presence."),
         ("chart","Track & Report","We track map and local rankings and report progress every month.")],
  faq=[("What is the Google map pack?","It's the block of three local businesses shown with a map at the top of Google for local searches. Ranking there dramatically increases calls, direction requests and visits."),
       ("How is local SEO different from regular SEO?","Local SEO focuses on being found by nearby customers - your Google Business Profile, map rankings, reviews and location pages - while general SEO targets broader organic rankings. They work best together."),
       ("Do reviews really affect local rankings?","Yes. The quantity, quality and recency of genuine reviews are an important local ranking factor and strongly influence whether customers choose you."),
       ("How long does local SEO take?","Profile optimisations can show results within weeks, while competitive local rankings build over a few months. We report visible progress throughout.")],
  cta=("Want to be the first business customers find?","Let's get your business into the Goa map pack and in front of nearby, ready-to-buy customers."),
 ),
 6979: dict(
  slug="ppc-google-ads-agency-goa", hero="dark", img_id=7013,
  eyebrow="PPC · Google Ads Management",
  h1='Google Ads that <span>work as hard as you do</span>',
  lead="Search, Shopping and Performance Max campaigns managed end-to-end - built to bring qualified enquiries and sales, not just clicks.",
  img_alt="PPC and Google Ads agency in Goa - Sanctify",
  title="PPC & Google Ads Agency in Goa | Search & Performance Max | Sanctify",
  desc="PPC & Google Ads agency in Goa. Sanctify manages Search, Shopping, Performance Max & remarketing campaigns end-to-end to drive qualified leads and sales.",
  two=("Why PPC","Show up the moment someone is ready to buy",
     ["Paid search puts your business at the very top of Google exactly when someone is looking for what you offer. Done well, it is one of the fastest ways to generate <strong>qualified enquiries</strong>.",
      "We build, manage and continually refine your campaigns - keywords, ad copy, bids and landing page alignment - so your budget works harder every month. It complements your <a href=\""+SITE+"/sanctify-facility/best-search-engine-optimization-seo-company-in-goa-india/\">organic SEO</a> perfectly."],
     "Every rupee of ad spend should be accountable. We optimise relentlessly so your investment keeps working harder.","The Sanctify Philosophy"),
  grid_head=("What we do","Full-service Google Ads management","Every campaign type you need, planned and managed by an experienced in-house team."),
  grid=[("search","Search Ads","Text ads that appear when customers search for your products or services.",None),
        ("spark","Performance Max","Google's AI-driven campaigns spanning Search, Display, YouTube and more.",None),
        ("cart","Google Shopping","Product listings that put your catalogue in front of ready buyers.",None),
        ("target","Display & Remarketing","Re-engage past visitors and stay visible across the web.",None),
        ("reel","YouTube Ads","Video campaigns that build awareness and drive action at scale.",None),
        ("layout","Landing Page Alignment","We align ads with focused landing pages to lift conversions.",None)],
  chips_head=("Platforms","Where we run your ads","We manage paid campaigns across Google's and Meta's advertising networks."),
  chips=["Google Search","Performance Max","Google Shopping","YouTube","Display Network","Meta Ads"],
  steps_head=("How we work","A disciplined PPC process","A structured approach to setup, optimisation and scaling - with clear reporting throughout."),
  steps=[("compass","Account & Goal Setup","We define goals, conversion tracking and account structure the right way."),
         ("target","Campaign Build","Keywords, audiences, ad copy and landing page alignment are built out."),
         ("chart","Bids & Optimisation","Ongoing optimisation of bids, budgets and creatives to improve efficiency."),
         ("spark","Reporting & Scaling","Transparent reporting, then scaling what works to grow results.")],
  faq=[("What budget do I need for Google Ads?","It depends on your industry and goals. We help you start at a sensible level, prove what works, then scale spend as the campaigns deliver a return."),
       ("Do you manage the ad spend or do we pay Google directly?","You pay Google directly for the ad spend and retain full ownership of your account. We manage strategy, setup and ongoing optimisation."),
       ("Which campaign types will you run?","We select from Search, Performance Max, Shopping, Display, remarketing and YouTube based on your goals, audience and budget."),
       ("How do you measure success?","We set up proper conversion tracking and report on the metrics that matter to your business - enquiries, calls and sales - not just clicks.")],
  cta=("Ready to turn clicks into customers?","Let's build Google Ads campaigns that bring qualified enquiries to your Goa business."),
 ),
 6980: dict(
  slug="content-marketing-agency-goa", hero="light", img_id=7014,
  eyebrow="Content Marketing · SEO Content",
  h1='Content that <span>ranks, resonates and converts</span>',
  lead="Strategy-led blogs, website copy and social content that build authority, earn trust and pull the right audience toward your brand.",
  img_alt="Content marketing agency in Goa - Sanctify",
  title="Content Marketing Agency in Goa | SEO Content & Blogs | Sanctify",
  desc="Content marketing agency in Goa. Sanctify creates strategy-led SEO blogs, website copy and social content that build authority and convert readers into customers.",
  two=("Why content","Content is how modern brands earn attention",
     ["Great content answers the questions your customers are already asking - building trust long before they ever enquire. It is also what powers strong <strong>SEO</strong> and gives your social channels something worth sharing.",
      "We plan content around real search demand and your business goals, then produce it to a genuinely high standard. It feeds directly into our <a href=\""+SITE+"/sanctify-facility/best-search-engine-optimization-seo-company-in-goa-india/\">SEO</a> and <a href=\""+SITE+"/sanctify-facility/social-media-marketing-agency-goa/\">social</a> work."],
     "Publish content that is genuinely useful, and both your audience and Google will reward you for it.","The Sanctify Philosophy"),
  grid_head=("What we do","A complete content service","From strategy to production and promotion - a full content engine for your brand."),
  grid=[("compass","Content Strategy & Planning","A clear plan built around search demand, your audience and business goals.",None),
        ("doc","SEO Blog Writing","Well-researched, optimised articles that rank and answer real questions.",None),
        ("pen","Website & Landing Copy","Persuasive, on-brand copy that guides visitors toward taking action.",None),
        ("reel","Social & Short-form Content","Captions, carousels and scripts that keep your channels active.",None),
        ("mail","Email & Newsletters","Nurture campaigns that keep your brand front of mind and drive repeat business.",None),
        ("spark","Content Refresh & Optimisation","Updating existing content to recover and grow its search performance.",None)],
  chips_head=("Content types","What we produce","A versatile mix of formats to reach your audience wherever they are."),
  chips=["Blogs & Articles","Landing Pages","Case Studies","Social Posts","Newsletters","Video Scripts"],
  steps_head=("How we work","A research-first content process","A repeatable process that turns strategy into content that performs."),
  steps=[("search","Research & Topics","We find the topics and keywords your audience is actually searching for."),
         ("cal","Editorial Plan","A prioritised content calendar aligned to your goals and seasons."),
         ("pen","Create & Optimise","We produce and optimise each piece to a high editorial and SEO standard."),
         ("chart","Publish & Promote","We publish, distribute and track performance to guide what comes next.")],
  faq=[("What kind of content do you produce?","Blogs and articles, website and landing page copy, case studies, social content, newsletters and video scripts - all planned around your goals."),
       ("Is the content optimised for SEO?","Yes. Every piece is researched around real search demand and optimised so it can rank, while still reading naturally for people."),
       ("Do you write specifically for Goa businesses?","Absolutely. We craft content that speaks to your local audience and market while meeting national quality standards."),
       ("How often should we publish?","It depends on your goals and capacity. We recommend a sustainable, consistent cadence and build a calendar around it.")],
  cta=("Ready to build authority with content?","Let's create content that ranks, earns trust and turns readers into customers."),
 ),
 6981: dict(
  slug="digital-marketing-agency-north-goa", hero="light", img_id=7015,
  eyebrow="Digital Marketing · North Goa",
  h1='Digital marketing for <span>North Goa brands</span>',
  lead="From Calangute to Mapusa, we help North Goa businesses grow their visibility, leads and sales online - all under one roof.",
  img_alt="Digital marketing agency in North Goa - Sanctify",
  title="Digital Marketing Agency in North Goa | SEO, Ads & Social | Sanctify",
  desc="Digital marketing agency serving North Goa - Calangute, Baga, Anjuna, Candolim, Mapusa & Panaji. SEO, social media, Google Ads, web design & branding by Sanctify.",
  two=("North Goa","Marketing built for the North Goa market",
     ["North Goa moves fast - hospitality, cafes, retail, real estate and events all competing for the same attention. Standing out takes more than a nice logo; it takes a <strong>coordinated digital strategy</strong>.",
      "As an award-winning Goa agency since 2012, we bring SEO, social, ads, web and branding together so North Goa brands grow with one clear plan. Explore our full <a href=\""+FACILITY+"\">services</a> or our <a href=\""+SITE+"/sanctify-facility/digital-marketing-agency-south-goa/\">South Goa</a> page."],
     "Local insight paired with national standards is what helps a North Goa brand truly stand out.","The Sanctify Philosophy"),
  grid_head=("What we do","Everything your brand needs, under one roof","A complete digital marketing suite tailored to North Goa businesses."),
  grid=city_services(),
  chips_head=("Areas we serve","Across North Goa","We work with businesses right across the North Goa belt."),
  chips=["Calangute","Baga","Anjuna","Candolim","Mapusa","Panaji","Porvorim","Assagao"],
  steps_head=("How we work","A simple, proven process","From first conversation to compounding results - a clear path to growth."),
  steps=[("compass","Discover","We learn your brand, market and goals across the North Goa landscape."),
         ("target","Strategy","We build a focused plan across the channels that will move the needle."),
         ("spark","Execute","Our in-house team delivers design, content, SEO, ads and social."),
         ("chart","Optimise","We measure, refine and scale what works - month after month.")],
  faq=[("Which North Goa areas do you cover?","We work with businesses across North Goa including Calangute, Baga, Anjuna, Candolim, Mapusa, Panaji, Porvorim and Assagao."),
       ("Do you work with hospitality and restaurant brands?","Yes - hospitality, cafes, restaurants, retail, real estate and events are among the North Goa sectors we regularly serve."),
       ("Can you handle everything in-house?","Yes. SEO, social, ads, web design, content and branding are all delivered by our own in-house team - no fragmented hand-offs."),
       ("Do you also serve South Goa?","We do. See our dedicated South Goa page, or talk to us about statewide campaigns.")],
  cta=("Ready to grow your North Goa brand?","Let's build a digital strategy that gets your business noticed across North Goa."),
 ),
 6982: dict(
  slug="digital-marketing-agency-south-goa", hero="dark", img_id=7016,
  eyebrow="Digital Marketing · South Goa",
  h1='Digital marketing for <span>South Goa brands</span>',
  lead="From Margao to Palolem, we help South Goa businesses turn online visibility into real bookings, enquiries and sales.",
  img_alt="Digital marketing agency in South Goa - Sanctify",
  title="Digital Marketing Agency in South Goa | SEO, Ads & Social | Sanctify",
  desc="Digital marketing agency serving South Goa - Margao, Vasco, Colva, Benaulim, Ponda & Palolem. SEO, social media, Google Ads, web design & branding by Sanctify.",
  two=("South Goa","Marketing that fits the South Goa market",
     ["South Goa blends established local businesses with a fast-growing hospitality and lifestyle scene. Reaching the right customers here takes a <strong>coordinated digital strategy</strong>, not scattered efforts.",
      "As an award-winning Goa agency since 2012, we unite SEO, social, ads, web and branding so South Goa brands grow with one clear plan. Explore our full <a href=\""+FACILITY+"\">services</a> or our <a href=\""+SITE+"/sanctify-facility/digital-marketing-agency-north-goa/\">North Goa</a> page."],
     "The brands that win in South Goa are the ones that show up consistently, everywhere their customers look.","The Sanctify Philosophy"),
  grid_head=("What we do","Everything your brand needs, under one roof","A complete digital marketing suite tailored to South Goa businesses."),
  grid=city_services(),
  chips_head=("Areas we serve","Across South Goa","We work with businesses right across the South Goa region."),
  chips=["Margao","Vasco","Colva","Benaulim","Ponda","Cuncolim","Canacona","Palolem"],
  steps_head=("How we work","A simple, proven process","From first conversation to compounding results - a clear path to growth."),
  steps=[("compass","Discover","We learn your brand, market and goals across the South Goa landscape."),
         ("target","Strategy","We build a focused plan across the channels that will move the needle."),
         ("spark","Execute","Our in-house team delivers design, content, SEO, ads and social."),
         ("chart","Optimise","We measure, refine and scale what works - month after month.")],
  faq=[("Which South Goa areas do you cover?","We work with businesses across South Goa including Margao, Vasco, Colva, Benaulim, Ponda, Cuncolim, Canacona and Palolem."),
       ("What types of businesses do you help?","Retail, hospitality, real estate, professional services and lifestyle brands are among the South Goa sectors we regularly serve."),
       ("Is everything handled in-house?","Yes. SEO, social, ads, web design, content and branding are delivered by our own in-house team."),
       ("Do you also serve North Goa?","We do. See our dedicated North Goa page, or talk to us about statewide campaigns.")],
  cta=("Ready to grow your South Goa brand?","Let's build a digital strategy that gets your business noticed across South Goa."),
 ),
}

# ---------- CSS (merged native sf-* system) ----------
CSS = r"""<style id="sf-facility-css">
.sf-page{font-family:'Poppins',-apple-system,Segoe UI,Roboto,sans-serif;color:#241c2b;max-width:1200px;margin:0 auto;padding:0 20px 10px;overflow:hidden;}
.sf-page *{box-sizing:border-box;}
.sf-eyebrow{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#c20b58;background:linear-gradient(135deg,#ffe3ef,#f4e0ff);padding:7px 14px;border-radius:999px;margin-bottom:16px;}
.sf-eyebrow-lt{color:#fff;background:rgba(255,255,255,.16);backdrop-filter:blur(4px);}
.sf-h2{font-size:34px;font-weight:800;margin:8px 0 12px;letter-spacing:-.01em;color:#1f1526;line-height:1.12;}
.sf-sec-head{text-align:center;max-width:660px;margin:0 auto 36px;}
.sf-sec-head p{color:#7a6e83;font-size:15px;line-height:1.65;font-weight:300;margin:0;}
.sf-btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:14px;padding:13px 24px;border-radius:999px;text-decoration:none;transition:transform .2s,box-shadow .2s,opacity .2s;cursor:pointer;}
.sf-btn .sf-arw{transition:transform .2s;}.sf-btn:hover .sf-arw{transform:translateX(4px);}
.sf-btn-p{background:linear-gradient(135deg,#c20b58,#7a00df);color:#fff !important;box-shadow:0 14px 30px -12px rgba(122,0,223,.6);}
.sf-btn-g{background:#fff;color:#c20b58 !important;border:1.5px solid #f0d4e3;}
.sf-btn-w{background:#fff;color:#c20b58 !important;}
.sf-btn-go{background:rgba(255,255,255,.14);color:#fff !important;border:1.5px solid rgba(255,255,255,.4);}
.sf-btn-p:hover,.sf-btn-g:hover,.sf-btn-w:hover,.sf-btn-go:hover{transform:translateY(-2px);}
/* LIGHT HERO */
.sf-hero{position:relative;margin:22px 0 10px;padding:40px;border-radius:26px;background:radial-gradient(120% 140% at 100% 0,#fdeef6 0,#f7edff 42%,#ffffff 100%);border:1px solid #f2e4ee;}
.sf-hero-inner{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center;}
.sf-h1{font-size:44px;line-height:1.08;font-weight:800;margin:0 0 16px;letter-spacing:-.01em;color:#1f1526;}
.sf-h1 span{background:linear-gradient(120deg,#c20b58,#7a00df);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}
.sf-lead{font-size:16px;line-height:1.7;color:#5c5064;font-weight:300;margin:0 0 26px;}
.sf-lead strong{font-weight:600;color:#3a2f42;}
.sf-hero-cta{display:flex;flex-wrap:wrap;gap:12px;}
.sf-hero .sf-stats,.sf-hero-text .sf-stats{display:flex;gap:26px;margin-top:30px;flex-wrap:wrap;}
.sf-hero-text .sf-stats div{display:flex;flex-direction:column;}
.sf-hero-text .sf-stats b{font-size:26px;font-weight:800;background:linear-gradient(120deg,#c20b58,#7a00df);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;line-height:1;}
.sf-hero-text .sf-stats span{font-size:12px;color:#8a7c92;font-weight:500;margin-top:4px;text-transform:uppercase;letter-spacing:.05em;}
.sf-hero-media{position:relative;}
.sf-hero-media img{width:100%;border-radius:20px;display:block;box-shadow:0 40px 70px -30px rgba(60,10,45,.5);position:relative;z-index:1;}
.sf-glow{position:absolute;inset:-10% -6% -14% -6%;background:radial-gradient(closest-side,rgba(194,11,88,.4),transparent 70%),radial-gradient(closest-side,rgba(122,0,223,.35),transparent 70%);filter:blur(28px);z-index:0;}
/* DARK PARALLAX HERO + BAND */
.sf-px{position:relative;overflow:hidden;border-radius:26px;margin:22px 0;display:grid;place-items:center;text-align:center;}
.sf-px-hero{min-height:60vh;}
.sf-px-band{min-height:320px;margin:52px 0;}
.sf-px-bg{position:absolute;left:0;right:0;top:-16%;height:132%;background-size:cover;background-position:center;will-change:transform;z-index:0;}
.sf-px-ov{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(18,4,22,.5),rgba(18,4,22,.34) 42%,rgba(70,6,50,.58));}
.sf-px-ov-d{background:linear-gradient(120deg,rgba(120,0,90,.72),rgba(60,0,120,.68));}
.sf-px-inner{position:relative;z-index:3;padding:56px 26px;max-width:820px;}
.sf-px-h1{font-size:50px;font-weight:800;color:#fff;margin:0 0 14px;letter-spacing:-.02em;line-height:1.06;text-shadow:0 4px 26px rgba(0,0,0,.3);}
.sf-px-h1 span{background:linear-gradient(110deg,#ff8fc0,#c79bff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}
.sf-px-sub{color:rgba(255,255,255,.94);font-size:17px;line-height:1.6;font-weight:300;margin:0 auto;max-width:620px;text-shadow:0 2px 14px rgba(0,0,0,.32);}
.sf-stats-lt{display:flex;gap:26px;flex-wrap:wrap;justify-content:center;}
.sf-stats-lt div{display:flex;flex-direction:column;align-items:center;min-width:120px;}
.sf-stats-lt b{font-size:40px;font-weight:800;line-height:1;color:#fff;text-shadow:0 3px 18px rgba(0,0,0,.3);}
.sf-stats-lt span{color:rgba(255,255,255,.9);font-size:13px;margin-top:8px;font-weight:400;letter-spacing:.03em;}
/* TWO COLUMN */
.sf-two{display:grid;grid-template-columns:1.45fr .9fr;gap:40px;align-items:center;margin:56px 0;}
.sf-two-l p{color:#5c5064;font-size:15px;line-height:1.75;font-weight:300;margin:0 0 15px;}
.sf-two-l p strong{color:#3a2f42;font-weight:600;}
.sf-two-l a{color:#c20b58;font-weight:600;text-decoration:none;border-bottom:1px solid rgba(194,11,88,.3);}
.sf-quote{position:relative;background:linear-gradient(150deg,#fdeef6,#f4ecff);border:1px solid #f0e0ec;border-radius:20px;padding:34px 28px 30px;}
.sf-quote:before{content:"";position:absolute;left:0;top:24px;bottom:24px;width:4px;border-radius:4px;background:linear-gradient(#c20b58,#7a00df);}
.sf-qmark{font-size:70px;line-height:.7;color:#e39bc4;font-family:Georgia,serif;display:block;height:34px;}
.sf-quote p{font-size:19px;font-weight:700;font-style:italic;color:#3a2340;line-height:1.42;margin:6px 0 14px;}
.sf-qby{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#c20b58;}
/* SECTIONS */
.sf-services{margin:58px 0;}
.sf-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;}
.sf-card{display:flex;flex-direction:column;gap:14px;background:#fff;border:1px solid #eee3ec;border-radius:18px;padding:24px 22px;text-decoration:none;color:inherit;position:relative;transition:transform .28s cubic-bezier(.4,0,.2,1),box-shadow .28s,border-color .28s;overflow:hidden;}
.sf-card:before{content:"";position:absolute;left:0;top:0;height:3px;width:100%;background:linear-gradient(90deg,#c20b58,#7a00df);transform:scaleX(0);transform-origin:left;transition:transform .3s;}
.sf-card:hover{transform:translateY(-6px);box-shadow:0 30px 50px -26px rgba(90,10,60,.4);border-color:#f0cfe1;}
.sf-card:hover:before{transform:scaleX(1);}
.sf-ic{flex:0 0 52px;width:52px;height:52px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,#ffe3ef,#f4e0ff);color:#c20b58;transition:.28s;}
.sf-ic svg{width:25px;height:25px;}
.sf-card:hover .sf-ic,.sf-step:hover .sf-ic{background:linear-gradient(135deg,#c20b58,#7a00df);color:#fff;transform:rotate(-6deg) scale(1.06);}
.sf-card h3{font-size:17.5px;font-weight:700;margin:0 0 6px;color:#241c2b;line-height:1.25;}
.sf-card p{font-size:13.4px;line-height:1.6;color:#7d7188;margin:0;font-weight:300;}
.sf-more{display:inline-flex;align-items:center;gap:6px;margin-top:auto;padding-top:10px;font-size:13px;font-weight:700;color:#c20b58;}
.sf-more .sf-arw{transition:transform .22s;}.sf-card:hover .sf-more .sf-arw{transform:translateX(5px);}
/* STEPS */
.sf-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;}
.sf-step{position:relative;background:#fff;border:1px solid #eee3ec;border-radius:18px;padding:26px 20px 22px;transition:transform .28s,box-shadow .28s,border-color .28s;outline:none;}
.sf-step:hover,.sf-step:focus{transform:translateY(-6px);box-shadow:0 28px 46px -26px rgba(90,10,60,.42);border-color:#f0cfe1;}
.sf-step .sf-ic{margin-bottom:14px;}
.sf-step-no{position:absolute;top:16px;right:18px;font-size:30px;font-weight:800;color:#f3e3ee;letter-spacing:-.02em;transition:.28s;}
.sf-step:hover .sf-step-no{color:#f3cfe2;}
.sf-step h3{font-size:16.5px;font-weight:700;margin:0 0 7px;color:#241c2b;}
.sf-step p{font-size:13px;line-height:1.6;color:#7d7188;margin:0;font-weight:300;}
/* CHIPS */
.sf-chips{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;}
.sf-chip{font-size:14px;font-weight:600;color:#3a2f42;background:#fff;border:1.5px solid #f0dfea;padding:11px 20px;border-radius:999px;transition:.22s;}
.sf-chip:hover{background:linear-gradient(135deg,#c20b58,#7a00df);color:#fff;border-color:transparent;transform:translateY(-3px);box-shadow:0 14px 26px -14px rgba(122,0,223,.6);}
/* FAQ */
.sf-faq{max-width:820px;margin:0 auto;}
.sf-faq details{background:#fff;border:1px solid #eee3ec;border-radius:14px;margin-bottom:12px;overflow:hidden;transition:.2s;}
.sf-faq details[open]{border-color:#f0cfe1;box-shadow:0 20px 40px -28px rgba(90,10,60,.4);}
.sf-faq summary{list-style:none;cursor:pointer;padding:18px 22px;font-weight:700;font-size:15.5px;color:#241c2b;display:flex;justify-content:space-between;align-items:center;gap:14px;}
.sf-faq summary::-webkit-details-marker{display:none;}
.sf-faq summary:after{content:"+";font-size:24px;font-weight:400;color:#c20b58;transition:.25s;line-height:1;}
.sf-faq details[open] summary:after{transform:rotate(45deg);}
.sf-faq .sf-faq-a{padding:0 22px 20px;color:#6a5f74;font-size:14px;line-height:1.72;font-weight:300;}
/* CTA */
.sf-cta{margin:52px 0 26px;border-radius:26px;background:linear-gradient(135deg,#c20b58,#7a00df);padding:52px 30px;text-align:center;position:relative;overflow:hidden;}
.sf-cta:before,.sf-cta:after{content:"";position:absolute;border-radius:50%;background:rgba(255,255,255,.1);}
.sf-cta:before{width:220px;height:220px;top:-90px;right:-60px;}.sf-cta:after{width:160px;height:160px;bottom:-70px;left:-40px;}
.sf-cta-in{position:relative;z-index:1;}
.sf-cta h2{color:#fff;font-size:31px;font-weight:800;margin:0 0 10px;}
.sf-cta p{color:rgba(255,255,255,.92);font-size:15px;margin:0 0 24px;font-weight:300;}
.sf-cta .sf-hero-cta{justify-content:center;}
/* REVEAL + HERO ANIM */
.sf-reveal{opacity:0;transform:translateY(26px);transition:opacity .6s ease,transform .6s cubic-bezier(.2,.7,.2,1);transition-delay:var(--d,0ms);}
.sf-reveal.sf-in{opacity:1;transform:none;}
@keyframes sfUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:none}}
@keyframes sfPop{from{opacity:0;transform:translateY(30px) scale(.97)}to{opacity:1;transform:none}}
@keyframes sfFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-14px)}}
@keyframes sfPulse{0%,100%{opacity:.7;transform:scale(1)}50%{opacity:1;transform:scale(1.08)}}
.sf-hero-anim .sf-eyebrow{animation:sfUp .7s .05s both cubic-bezier(.2,.7,.2,1);}
.sf-hero-anim .sf-h1{animation:sfUp .75s .16s both cubic-bezier(.2,.7,.2,1);}
.sf-hero-anim .sf-lead{animation:sfUp .75s .3s both cubic-bezier(.2,.7,.2,1);}
.sf-hero-anim .sf-hero-cta{animation:sfUp .75s .44s both cubic-bezier(.2,.7,.2,1);}
.sf-hero-anim .sf-hero-text .sf-stats{animation:sfUp .75s .58s both cubic-bezier(.2,.7,.2,1);}
.sf-hero-anim .sf-hero-media{animation:sfPop .9s .26s both cubic-bezier(.2,.7,.2,1);}
.sf-hero-anim .sf-hero-media img{animation:sfPop .9s .26s both cubic-bezier(.2,.7,.2,1),sfFloat 6.5s 1.2s ease-in-out infinite;}
.sf-glow{animation:sfPulse 5.5s ease-in-out infinite;}
/* one H1 per page: hide theme title bar (loads only on these pages) */
.title{display:none !important;}
@media(prefers-reduced-motion:reduce){.sf-hero-anim *,.sf-glow,.sf-hero-media img{animation:none !important;}.sf-reveal{opacity:1 !important;transform:none !important;}.sf-px-bg{transform:none !important;}}
@media(max-width:960px){
 .sf-hero{padding:28px;}.sf-hero-inner{grid-template-columns:1fr;gap:26px;}.sf-hero-media{order:-1;}
 .sf-h1{font-size:32px;}.sf-px-h1{font-size:36px;}.sf-h2{font-size:27px;}
 .sf-two{grid-template-columns:1fr;gap:26px;}
 .sf-steps{grid-template-columns:repeat(2,1fr);}
 .sf-grid{grid-template-columns:repeat(2,1fr);gap:14px;}
 .sf-px-hero{min-height:52vh;}
}
@media(max-width:560px){
 .sf-page{padding:0 14px;}
 .sf-hero{padding:22px 18px;border-radius:20px;}.sf-px{border-radius:18px;}
 .sf-h1{font-size:27px;}.sf-px-h1{font-size:29px;}.sf-px-sub,.sf-lead{font-size:15px;}
 .sf-grid,.sf-steps{grid-template-columns:1fr;}
 .sf-stats-lt{gap:22px 30px;}.sf-stats-lt b{font-size:32px;}
 .sf-cta{padding:38px 20px;}.sf-cta h2{font-size:24px;}
 .sf-btn{width:100%;justify-content:center;}
 .sf-px-band{min-height:280px;}
 .sf-dgrid{grid-template-columns:1fr !important;}
 .sf-dark{padding:46px 18px !important;}
}
/* SMOKE: header = site WebGL mouse-fluid (magenta, unchanged) via screen blend; section 2 = natural white ambient */
.sf-smoke{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;}
.sf-px-hero .sf-smoke{z-index:2;mix-blend-mode:screen;}
.sf-dark .sf-smoke{z-index:1;mix-blend-mode:screen;}
@property --sfa{syntax:"<angle>";inherits:false;initial-value:0deg;}
/* DARK GLOW-CARD SERVICES (new layout) */
.sf-dark{position:relative;overflow:hidden;border-radius:26px;margin:56px 0;padding:62px 40px;}
.sf-dark-bg{position:absolute;inset:0;z-index:0;background:radial-gradient(125% 130% at 18% 0%,#5a1e6e 0%,#43206f 50%,#2f1656 100%);}
.sf-dark-in{position:relative;z-index:3;}
.sf-sec-head-lt h2{color:#fff;}
.sf-sec-head-lt p{color:rgba(255,255,255,.72);}
.sf-dgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;}
.sf-dcard{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:20px;padding:34px 26px 30px;text-decoration:none;color:inherit;overflow:hidden;transition:transform .3s cubic-bezier(.4,0,.2,1),background .3s;}
.sf-dcard:hover{transform:translateY(-6px);background:rgba(255,255,255,.055);}
.sf-dcard-fx{position:absolute;inset:0;border-radius:20px;padding:2px;pointer-events:none;z-index:1;background:conic-gradient(from var(--sfa),transparent 0deg,transparent 225deg,#c20b58 280deg,#ff2ea6 315deg,#ffffff 338deg,#ff2ea6 352deg,#c79bff 360deg);-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);mask-composite:exclude;filter:drop-shadow(0 0 5px rgba(255,70,165,.65));animation:sf-beam 4.2s linear infinite;}
.sf-dcard-fx:after{content:"";position:absolute;inset:0;border-radius:20px;border:1px solid rgba(255,255,255,.1);}
@keyframes sf-beam{to{--sfa:360deg;}}
.sf-dcard>*{position:relative;z-index:2;}
.sf-dic{width:66px;height:66px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(140deg,#c20b58,#7a00df);color:#fff;box-shadow:0 12px 30px -10px rgba(194,11,88,.7);margin-bottom:12px;transition:transform .3s;}
.sf-dic svg{width:28px;height:28px;}
.sf-dcard:hover .sf-dic{transform:scale(1.08) rotate(-5deg);}
.sf-dhead{display:flex;align-items:center;justify-content:center;gap:12px;margin:2px 0 8px;}
.sf-dline{height:2px;width:26px;border-radius:2px;background:linear-gradient(90deg,transparent,#c20b58);opacity:.5;transition:.3s;}
.sf-dhead .sf-dline:last-child{background:linear-gradient(90deg,#7a00df,transparent);}
.sf-dcard:hover .sf-dline{width:34px;opacity:1;}
.sf-dcard h3{font-size:19px;font-weight:700;margin:0;color:#fff;font-family:Georgia,serif;letter-spacing:.01em;}
.sf-dcard p{font-size:13.6px;line-height:1.66;color:rgba(255,255,255,.66);font-weight:300;margin:0;}
@media(prefers-reduced-motion:reduce){.sf-dcard-fx{animation:none !important;}.sf-smoke{display:none !important;}}
@media(max-width:960px){.sf-dgrid{grid-template-columns:repeat(2,1fr);}}
</style>"""

# ---------- scoped JS (reveal + counters + parallax) ----------
JS = r"""<script>
(function(){
 function ready(fn){if(document.readyState!=='loading'){fn();}else{document.addEventListener('DOMContentLoaded',fn);}}
 ready(function(){
  var root=document.querySelector('.sf-facility');if(!root)return;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  function countTo(b,tgt,suf){if(reduce){b.textContent=tgt+suf;return;}var st=null;function step(ts){if(!st)st=ts;var p=Math.min((ts-st)/1200,1);b.textContent=Math.floor(p*tgt)+suf;if(p<1)requestAnimationFrame(step);}requestAnimationFrame(step);}
  var io=('IntersectionObserver' in window)?new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('sf-in');io.unobserve(x.target);}});},{threshold:.14,rootMargin:'0px 0px -6% 0px'}):null;
  var rev=root.querySelectorAll('.sf-reveal');
  if(io){rev.forEach(function(el){io.observe(el);});}else{rev.forEach(function(el){el.classList.add('sf-in');});}
  var band=root.querySelector('.sf-px-band');
  if(band){
   if('IntersectionObserver' in window){var io2=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.querySelectorAll('b[data-count]').forEach(function(b){countTo(b,+b.getAttribute('data-count'),b.getAttribute('data-suf')||'');});io2.unobserve(x.target);}});},{threshold:.3});io2.observe(band);}
   else{band.querySelectorAll('b[data-count]').forEach(function(b){b.textContent=b.getAttribute('data-count')+(b.getAttribute('data-suf')||'');});}
  }
  if(!reduce){
   var pxs=[].slice.call(root.querySelectorAll('[data-px] .sf-px-bg'));
   var ticking=false;
   function upd(){ticking=false;var vh=window.innerHeight;pxs.forEach(function(bg){var s=bg.parentNode.getBoundingClientRect();var center=s.top+s.height/2;var off=((vh/2)-center)*0.18;bg.style.transform='translate3d(0,'+off.toFixed(1)+'px,0)';});}
   function onScroll(){if(!ticking){ticking=true;requestAnimationFrame(upd);}}
   window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll);upd();
  }
 });
})();
</script>"""

NOSCRIPT = "<noscript><style>.sf-facility .sf-reveal{opacity:1 !important;transform:none !important;}</style></noscript>"
# Site's WebGL mouse-fluid smoke (mu-plugin) - not auto-enqueued on these pages, so load it explicitly.
# It self-initializes on #sf-smoke / #sf-smoke2 and binds pointer splats to document.body.
SMOKE_SCRIPT = '<script src="https://www.sanctify.in/wp-content/mu-plugins/sanctify-smoke.js" defer></script>'

def schema(d, pid):
    url = f"{SITE}/sanctify-facility/{d['slug']}/" if d['slug'] not in ("digital-marketing-agency-north-goa","digital-marketing-agency-south-goa") else f"{SITE}/{d['slug']}/"
    faqld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d["faq"]]}
    svc = {"@context":"https://schema.org","@type":"Service","name":d["title"].split(" | ")[0],
           "provider":{"@type":"Organization","name":"Sanctify","url":SITE},
           "areaServed":{"@type":"Place","name":"Goa, India"},"url":url,"description":d["desc"]}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":"Facility","item":FACILITY},
        {"@type":"ListItem","position":3,"name":d["title"].split(" | ")[0],"item":url}]}
    out=""
    for obj in (svc,faqld,crumb):
        out += '<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False)+'</script>\n'
    return out

def render(pid, d):
    d["img"] = f"{SITE}/wp-content/uploads/2026/08/sanctify-{d['slug']}-hero.jpg"
    d["hero_stats"] = HERO_STATS
    hero = hero_dark(d) if d["hero"]=="dark" else hero_light(d)
    parts = [f'<div class="sf-page sf-facility">', hero]
    # order sections for variety
    parts.append(two(*d["two"]))
    parts.append(dark_services(*d["grid_head"], d["grid"]))
    parts.append(services_section(*d["chips_head"], chips(d["chips"])))
    parts.append(band(BRAND_BAND))
    parts.append(services_section(*d["steps_head"], steps(d["steps"])))
    parts.append(services_section("FAQ","Frequently asked questions","Answers to the questions Goa businesses ask us most.", faq(d["faq"])))
    parts.append(cta(*d["cta"]))
    parts.append('</div>')
    body = "\n".join(parts)
    content = CSS + "\n" + body + "\n" + NOSCRIPT + "\n" + JS + "\n" + SMOKE_SCRIPT + "\n" + schema(d, pid)
    return content

for pid, d in PAGES.items():
    content = render(pid, d)
    img = f"{SITE}/wp-content/uploads/2026/08/sanctify-{d['slug']}-hero.jpg"
    payload = {"content":content,"template":"full_width.php","meta":{
        "_seopress_titles_title": d["title"],
        "_seopress_titles_desc": d["desc"],
        "_seopress_social_fb_img": img,
        "_seopress_social_twitter_img": img,
    }}
    open(f"build5/{d['slug']}.content.html","w").write(content)
    json.dump(payload, open(f"build5/{d['slug']}.payload.json","w"), ensure_ascii=False)
    prev = ("<!doctype html><html lang=en><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>"
            "<link href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap' rel=stylesheet>"
            "<style>body{margin:0;background:#fff;}</style></head><body>"+content+"</body></html>")
    open(f"preview5/{d['slug']}.html","w").write(prev)
    print(f"built {pid} {d['slug']} | hero={d['hero']} | content {len(content)} chars")
print("ALL BUILT")
