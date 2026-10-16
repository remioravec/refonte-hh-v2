# -*- coding: utf-8 -*-
"""Genere les 10 sous-compositions du film Hello Harel + index.html."""
import json, os, textwrap

P = "/home/user/refonte-hh-v2/videos/hello-harel-promo"
UI = open(f"{P}/assets/ui.css").read()
FONTFACE = """@font-face{font-family:'Urbanist';font-style:normal;font-weight:400;font-display:block;src:url('../../assets/fonts/urbanist-400.woff2') format('woff2')}
@font-face{font-family:'Urbanist';font-style:normal;font-weight:600;font-display:block;src:url('../../assets/fonts/urbanist-600.woff2') format('woff2')}
@font-face{font-family:'Urbanist';font-style:normal;font-weight:700;font-display:block;src:url('../../assets/fonts/urbanist-700.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:400;font-display:block;src:url('../../assets/fonts/inter-400.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:500;font-display:block;src:url('../../assets/fonts/inter-500.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:600;font-display:block;src:url('../../assets/fonts/inter-600.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:700;font-display:block;src:url('../../assets/fonts/inter-700.woff2') format('woff2')}"""
FONTFACE_ROOT = """@font-face{font-family:'Urbanist';font-style:normal;font-weight:400;font-display:block;src:url('assets/fonts/urbanist-400.woff2') format('woff2')}
@font-face{font-family:'Urbanist';font-style:normal;font-weight:600;font-display:block;src:url('assets/fonts/urbanist-600.woff2') format('woff2')}
@font-face{font-family:'Urbanist';font-style:normal;font-weight:700;font-display:block;src:url('assets/fonts/urbanist-700.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:400;font-display:block;src:url('assets/fonts/inter-400.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:500;font-display:block;src:url('assets/fonts/inter-500.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:600;font-display:block;src:url('assets/fonts/inter-600.woff2') format('woff2')}
@font-face{font-family:'Inter';font-style:normal;font-weight:700;font-display:block;src:url('assets/fonts/inter-700.woff2') format('woff2')}"""
DASH = {e["n"]: e for e in json.load(open(f"{P}/assets/dashboards/index.json"))}
VO = {v["frame"]: v for v in json.load(open(f"{P}/audio_meta.json"))["voices"]}

def dash_html(n):
    return open(f"{P}/{DASH[n]['file']}").read()

BASE = """
#root{position:absolute;inset:0;width:1920px;height:1080px;background:#FFFFFF;
  overflow:hidden;font-family:Inter,ui-sans-serif,sans-serif;color:#0F172A;
  -webkit-font-smoothing:antialiased}
#root *{box-sizing:border-box}
.stage{position:absolute;inset:0;padding:86px 104px 104px}
.col-l{position:absolute;left:104px;top:214px;width:690px}
.col-r{position:absolute;right:104px;top:150px}
.clock{position:absolute;left:104px;top:82px;display:inline-flex;align-items:center;gap:14px;
  padding:13px 30px 13px 24px;border-radius:100px;background:rgba(0,177,245,.08);
  border:1.5px solid rgba(0,177,245,.2);font-family:Urbanist,sans-serif;font-weight:700;
  font-size:34px;letter-spacing:-.01em;color:#0079B8}
.clock i{width:12px;height:12px;border-radius:50%;background:#00B1F5;display:block}
.eyebrow{font-weight:600;font-size:18px;letter-spacing:.09em;text-transform:uppercase;
  color:#0079B8;margin-bottom:22px}
h2.t{font-family:Urbanist,sans-serif;font-weight:600;font-size:60px;line-height:1.08;
  letter-spacing:-.025em;color:#0F172A;margin:0 0 26px}
h2.t em{font-style:normal;color:#0096D6}
p.sub{font-size:25px;line-height:1.58;color:#64748B;margin:0}
.pain{margin-top:34px;padding:24px 28px;border-radius:14px;background:rgba(0,177,245,.04);
  border:1.5px solid rgba(0,177,245,.2)}
.pain div{display:flex;align-items:flex-start;gap:14px;font-size:21px;line-height:1.5;
  color:#334155;padding:9px 0}
.pain div s{text-decoration:none;color:#dc2626;font-weight:700;flex:none;width:20px}
.answer{margin-top:30px;display:inline-flex;align-items:center;gap:12px;padding:12px 26px;
  border-radius:100px;background:rgba(34,197,94,.1);border:1.5px solid rgba(34,197,94,.35);
  color:#15803d;font-weight:600;font-size:21px}
.dash{position:relative;transform-origin:top right;overflow:hidden;border-radius:16px;border:1.5px solid #E2E8F0}
.dash-in{transform-origin:top left}
.inset{position:absolute;transform-origin:bottom right;z-index:3}
.daybar{position:absolute;left:0;right:0;bottom:0;height:6px;background:#E2E8F0}
.daybar i{position:absolute;left:0;top:0;bottom:0;background:#00B1F5;display:block;width:0}
.stamp{position:absolute;right:104px;bottom:52px;font-size:17px;letter-spacing:.06em;
  text-transform:uppercase;color:#64748B;font-weight:500}
"""

FRAMES = [
 dict(n=1, id="f01", slug="01-0630-quai", dur=8.0, clock=None, bar=(0.0, 0.03)),
 dict(n=2, id="f02", slug="02-reception", dur=10.0, clock="06:50", bar=(0.03, 0.06),
      eyebrow="Réception", dash=0, box=(952, 780),
      title="Le contrôle à réception<br>tient sur un <em>carnet</em>.",
      sub="Huit jours de DLC exigés. Cinq jours livrés. Personne ne le verra avant la cuisson.",
      pain=[("✕","La non-conformité entre quand même en stock"),
            ("✕","Le relevé n'est ni daté, ni nominatif"),
            ("✕","Le fournisseur n'est prévenu de rien")],
      answer="Le lot est bloqué à l'arrivée"),
 dict(n=3, id="f03", slug="03-stock-eclate", dur=8.5, clock="08:15", bar=(0.06, 0.16),
      eyebrow="Multi-sites", dash=1, box=(952, 850),
      title="Quatre endroits,<br><em>quatre vérités</em>.",
      sub="L'entrepôt, deux dépôts, le carreau — et un seul client qui attend sa palette.",
      pain=[("✕","Le total semble suffisant, le site ne l'est pas"),
            ("✕","On transfère au jugé, on livre en retard")],
      answer="Un stock, quatre sites, une ligne"),
 dict(n=4, id="f04", slug="04-dlc-fefo", dur=11.0, clock="10:00", bar=(0.16, 0.31),
      eyebrow="DLC · FEFO", dash=5, box=(560, 480), side=(7, 1.0667), row_y=430,
      title="Vous découvrez la DLC<br>en <em>prenant le bac</em>.",
      sub="Au plus près de la DLC d'abord : c'est une règle, pas une habitude. Et la chambre qui dérive se voit avant l'inventaire, pas après.",
      answer="FEFO appliqué, dérive signalée à temps"),
 dict(n=5, id="f05", slug="05-fiche-client", dur=8.0, clock="11:30", bar=(0.31, 0.44),
      eyebrow="Relation client", dash=8, box=(952, 790),
      title="Un grossiste<br>veut <em>son prix</em>.",
      sub="Vous cherchez dans vos mails ce que votre ERP devrait afficher en une ligne.",
      pain=[("✕","Historique, encours et remise dans trois outils"),
            ("✕","Le délai négocié, personne ne le retrouve")],
      answer="Tout le client sur un écran"),
 dict(n=6, id="f06", slug="06-tracabilite-rappel", dur=11.5, clock="14:00", bar=(0.44, 0.66),
      eyebrow="Rappel produit", dash=4, box=(952, 800),
      title="Remonter un lot.<br>Redescendre à ses<br><em>clients livrés</em>.",
      sub="Au classeur, c'est l'après-midi. Ici, c'est quelques secondes.",
      pain=[("✕","Trois matières premières à retrouver en amont"),
            ("✕","Trois clients à prévenir en aval"),
            ("✕","Et l'horloge qui tourne")],
      answer="Amont et aval, d'un seul lot"),
 dict(n=7, id="f07", slug="07-edi", dur=9.5, clock="15:30", bar=(0.66, 0.79),
      eyebrow="Flux EDI", dash=3, box=(952, 850),
      title="La commande arrive,<br>et quelqu'un la <em>retape</em>.",
      sub="Chaque ressaisie est une erreur qui attend son tour.",
      pain=[("✕","Référence fausse, quantité fausse, litige"),
            ("✕","Personne ne compte le temps passé")],
      answer="146 messages reçus, 138 intégrés seuls"),
 dict(n=8, id="f08", slug="08-facture-poids", dur=9.0, clock="16:30", bar=(0.79, 0.88),
      eyebrow="Poids variable", dash=9, box=(952, 850),
      title="Facturé au poids<br><em>commandé</em>.",
      sub="Vous avez livré autre chose. L'écart, vous le payez sans jamais le voir.",
      pain=[("✕","12 000 kg commandés, 12 340 kg livrés"),
            ("✕","L'écart se répète sur chaque ligne, chaque jour")],
      answer="Facturé au poids réellement pesé"),
 dict(n=9, id="f09", slug="09-cout-marge", dur=9.0, clock="18:00", bar=(0.88, 1.0),
      eyebrow="Coût de revient · marge", dash=6, box=(700, 512), side=(2, 0.845),
      title="La marge du jour,<br><em>aujourd'hui</em>.",
      sub="Le coût de revient au centime, poste par poste. Pas le mois prochain.",
      answer="26,5 % de marge, lot par lot"),
 dict(n=10, id="f10", slug="10-preuve-cta", dur=8.0, clock=None, bar=(1.0, 1.0)),
]

def frame_file(f):
    css = FONTFACE + "\n" + BASE + "\n" + UI
    n, fid = f["n"], f["id"]
    vo = VO[n]["duration_s"]

    # ---------- plan 1 : accroche ----------
    if n == 1:
        body = f"""
    <div class="stage hook">
      <img id="ph" src="../../assets/img/hook.webp" alt="">
      <div id="veil"></div>
      <div class="hookw">
        <div id="hk-clock">06:30</div>
        <h1 id="hk-t">Le camion est à quai.</h1>
        <p id="hk-s">À partir de maintenant, tout ce que vous ne mesurez pas<br>vous coûte quelque chose.</p>
      </div>
      <div class="daybar"><i id="bar"></i></div>
    </div>"""
        css += """
#root{background:#0F172A}
.hook img{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}
#veil{position:absolute;inset:0;background:linear-gradient(100deg,rgba(15,23,42,.96) 0%,rgba(15,23,42,.88) 48%,rgba(15,23,42,.62) 100%)}
.hookw{position:absolute;left:140px;top:300px;width:1180px}
#hk-clock{font-family:Urbanist,sans-serif;font-weight:700;font-size:150px;line-height:1;
  letter-spacing:-.035em;color:#00B1F5;margin-bottom:34px}
#hk-t{font-family:Urbanist,sans-serif;font-weight:600;font-size:92px;line-height:1.05;
  letter-spacing:-.03em;color:#FFFFFF;margin:0 0 30px}
#hk-s{font-size:31px;line-height:1.55;color:#CBD5E1;margin:0}
.daybar{background:rgba(255,255,255,.14)}
"""
        js = f"""
      tl.fromTo("#ph",{{scale:1.1,opacity:0}},{{scale:1.03,opacity:1,duration:2.4,ease:"power2.out"}},0);
      tl.to("#ph",{{scale:1.0,duration:{f['dur']-2.4:.2f},ease:"none"}},2.4);
      tl.fromTo("#hk-clock",{{opacity:0,y:48}},{{opacity:1,y:0,duration:.9,ease:"power3.out"}},.35);
      tl.fromTo("#hk-t",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.8,ease:"power3.out"}},1.25);
      tl.fromTo("#hk-s",{{opacity:0,y:28}},{{opacity:1,y:0,duration:.8,ease:"power3.out"}},2.45);
      tl.fromTo("#bar",{{width:"0%"}},{{width:"3%",duration:{f['dur']:.2f},ease:"none"}},0);"""

    # ---------- plan 10 : preuve + appel a l'action ----------
    elif n == 10:
        body = """
    <div class="stage cta">
      <div class="ctaw">
        <img id="lg" src="../../assets/img/logo.svg" alt="Hello Harel">
        <div id="cnt-wrap"><span id="cnt">0</span><span id="plus">+</span></div>
        <p id="cta-l">PME agroalimentaires françaises équipées</p>
        <div id="cta-b">Demander une démo</div>
        <p id="cta-u">helloharel.com</p>
      </div>
      <div class="daybar"><i id="bar"></i></div>
    </div>"""
        css += """
.cta{display:grid;place-items:center}
#root{background:#0F172A}
.ctaw{text-align:center;width:1100px}
#lg{width:430px;height:auto;display:block;margin:0 auto 60px}
#cnt-wrap{font-family:Urbanist,sans-serif;font-weight:700;font-size:188px;line-height:1;
  letter-spacing:-.04em;color:#00B1F5}
#plus{font-size:120px;vertical-align:super;margin-left:6px}
#cta-l{font-size:30px;color:#CBD5E1;margin:22px 0 0}
#cta-b{display:inline-block;margin-top:56px;padding:24px 62px;border-radius:100px;
  background:#00B1F5;color:#0F172A;font-weight:700;font-size:29px;letter-spacing:-.01em}
#cta-u{font-size:24px;color:#94A3B8;margin:30px 0 0;letter-spacing:.04em}
.daybar{background:rgba(255,255,255,.14)}
.daybar i{width:100%}
"""
        js = """
      tl.fromTo("#lg",{opacity:0,y:34},{opacity:1,y:0,duration:.8,ease:"power3.out"},.2);
      const c={v:0};
      tl.fromTo("#cnt-wrap",{opacity:0,scale:.92},{opacity:1,scale:1,duration:.6,ease:"power3.out"},.9);
      tl.to(c,{v:200,duration:2.0,ease:"power2.out",
        onUpdate:()=>{document.getElementById("cnt").textContent=Math.round(c.v);}},1.0);
      tl.fromTo("#cta-l",{opacity:0},{opacity:1,duration:.6},2.6);
      tl.fromTo("#cta-b",{opacity:0,y:26},{opacity:1,y:0,duration:.7,ease:"power3.out"},3.3);
      tl.fromTo("#cta-u",{opacity:0},{opacity:1,duration:.6},4.0);"""

    # ---------- plans 2 a 9 : galere + tableau de bord ----------
    else:
        d = DASH[f["dash"]]
        boxw, boxh = f.get("box", (952, 850))
        s = round(min(boxw / d["w"], boxh / d["h"]), 4)
        w, h = round(d["w"] * s), round(d["h"] * s)
        rtop = max(150, round(150 + (850 - h) / 2))
        inner = dash_html(f["dash"])
        extra_css, extra_html, extra_js = "", "", ""

        if f.get("inset"):
            dn, ds = f["inset"]
            di = DASH[dn]
            extra_html = (f'<div class="inset" id="inset" data-layout-allow-overlap '
                          f'style="width:{round(di["w"]*ds)}px;height:{round(di["h"]*ds)}px">'
                          f'<div class="dash-in" style="transform:scale({ds});width:{di["w"]}px">'
                          f'<div id="hh-page"><div class="hhf">{dash_html(dn)}</div></div></div></div>')
            extra_css = ("#inset{position:absolute;left:-196px;bottom:-78px;overflow:hidden;"
                         "border-radius:16px;border:1.5px solid #E2E8F0;"
                         "box-shadow:0 30px 64px -28px rgba(15,23,42,.45)}")
            extra_js = ('tl.fromTo("#inset",{opacity:0,y:40,scale:.94},'
                        '{opacity:1,y:0,scale:1,duration:.8,ease:"power3.out"},3.1);')
        if f.get("side"):
            dn, ds = f["side"]
            di = DASH[dn]
            sw, sh = round(di["w"] * ds), round(di["h"] * ds)
            extra_html = (f'<div class="side" id="side" style="width:{sw}px;height:{sh}px">'
                          f'<div class="dash-in" style="transform:scale({ds});width:{di["w"]}px">'
                          f'<div id="hh-page"><div class="hhf">{dash_html(dn)}</div></div></div></div>')
            GAP = 56
            COLR_X = round((1920 - (w + GAP + sw)) / 2)
            SIDE_X = COLR_X + w + GAP
            ROW_Y = f.get("row_y", 368)
            extra_css = (
              "#root .col-l{left:0;right:0;top:126px;width:auto;padding:0 200px;text-align:center}"
              "#root .eyebrow{margin-bottom:16px}"
              "#root h2.t{font-size:50px;margin-bottom:18px}"
              "#root p.sub{font-size:23px}"
              "#root .col-r{left:" + str(COLR_X) + "px;right:auto;top:" + str(ROW_Y) + "px!important}"
              "#root .side{position:absolute;left:" + str(SIDE_X) + "px;top:" + str(ROW_Y) + "px;overflow:hidden;"
              "border-radius:16px;border:1.5px solid #E2E8F0;z-index:2}"
              "#root .answer{position:absolute;left:50%;top:" + str(ROW_Y + max(h, sh) + 30) + "px;transform:translateX(-50%);margin:0}"
              "#root .stamp{bottom:28px}")
            extra_js = ('tl.fromTo("#side",{opacity:0,y:40},'
                        '{opacity:1,y:0,duration:.85,ease:"power3.out"},1.15);')

        pain = ""
        if f.get("pain"):
            pain = '<div class="pain" id="pain">' + "".join(
                f'<div><s>{m}</s><span>{t}</span></div>' for m, t in f["pain"]) + "</div>"
        answer = f'<div class="answer" id="answer">✓&nbsp;&nbsp;{f["answer"]}</div>' if f.get("answer") else ""

        body = f"""
    <div class="stage">
      <div class="clock" id="clock"><i></i>{f['clock']}</div>
      <div class="col-l">
        <p class="eyebrow" id="eb">{f['eyebrow']}</p>
        <h2 class="t" id="ttl">{f['title']}</h2>
        <p class="sub" id="sb">{f['sub']}</p>
        {pain}
        {answer}
      </div>
      <div class="col-r" style="top:{rtop}px">
        <div class="dash" id="dash" style="width:{w}px;height:{h}px">
          <div class="dash-in" style="transform:scale({s});width:{d['w']}px">
            <div id="hh-page"><div class="hhf">{inner}</div></div>
          </div>
        </div>
      </div>
      {extra_html}
      <p class="stamp">Hello&nbsp;Harel — écran réel du produit</p>
      <div class="daybar"><i id="bar"></i></div>
    </div>"""
        css += extra_css
        b0, b1 = f["bar"]
        js = f"""
      tl.fromTo("#clock",{{opacity:0,x:-26}},{{opacity:1,x:0,duration:.6,ease:"power3.out"}},0);
      tl.fromTo("#eb",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},.18);
      tl.fromTo("#ttl",{{opacity:0,y:34}},{{opacity:1,y:0,duration:.75,ease:"power3.out"}},.32);
      tl.fromTo("#sb",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.65,ease:"power3.out"}},.72);
      tl.fromTo("#dash",{{opacity:0,x:{0 if f.get("side") else 64},scale:.965}},{{opacity:1,x:0,scale:1,duration:.95,ease:"power3.out"}},.55);
      {extra_js}
      const root=document.querySelector('#root');
      const boxes=root.querySelectorAll('#dash .ui-box');
      if(boxes.length) tl.fromTo(boxes,{{opacity:0,y:16,scale:.94}},
        {{opacity:1,y:0,scale:1,duration:.45,stagger:.1,ease:"power2.out"}},1.25);
      const rows=root.querySelectorAll('#dash .ui-tab tbody tr');
      if(rows.length) tl.fromTo(rows,{{opacity:0,y:12}},
        {{opacity:1,y:0,duration:.34,stagger:.09,ease:"power2.out"}},1.55);
      const cards=root.querySelectorAll('#dash .ui-card');
      if(cards.length>1) tl.fromTo(cards,{{opacity:0,y:18}},
        {{opacity:1,y:0,duration:.45,stagger:.16,ease:"power2.out"}},1.1);
      const flag=root.querySelector('#dash .alert, #dash .ui-warn, #dash tr.pr');
      if(flag) tl.fromTo(flag,{{boxShadow:"inset 0 0 0 0 rgba(220,38,38,0)"}},
        {{boxShadow:"inset 0 0 0 2px rgba(220,38,38,.85)",duration:.5,
          repeat:1,yoyo:true,ease:"power2.inOut"}},2.7);
      {f'tl.fromTo("#pain",{{opacity:0,y:22}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},1.35);' if pain else ''}
      {f'tl.fromTo("#answer",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.6,ease:"back.out(1.4)"}},{max(2.6, f["dur"]-3.4):.2f});' if answer else ''}
      tl.fromTo("#bar",{{width:"{b0*100:.1f}%"}},{{width:"{b1*100:.1f}%",duration:{f['dur']:.2f},ease:"none"}},0);"""

    html = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <title>Hello Harel — plan {n:02d} — {f['slug']}</title>
  </head>
  <body>
    <template>
      <style>{css}</style>
      <div id="root" data-composition-id="{fid}" data-width="1920" data-height="1080" data-duration="{f['dur']}">
{body}
      </div>
      <script>
        const tl = gsap.timeline({{ paused: true }});
{js}
        window.__timelines["{fid}"] = tl;
      </script>
    </template>
  </body>
</html>
"""
    out = f"{P}/compositions/frames/{f['slug']}.html"
    open(out, "w").write(html)
    return out, len(html), vo

total = 0.0
rows_host, rows_audio = [], []
for f in FRAMES:
    out, size, vo = frame_file(f)
    rows_host.append(
        f'      <div class="clip" id="plan-{f["n"]:02d}" data-composition-id="{f["id"]}"\n'
        f'           data-composition-src="compositions/frames/{f["slug"]}.html"\n'
        f'           data-start="{total:g}" data-duration="{f["dur"]:g}"\n'
        f'           data-track-index="0" data-width="1920" data-height="1080"></div>')
    rows_audio.append(
        f'      <audio id="vo{f["n"]:02d}" src="assets/voice/{f["n"]:02d}.wav"\n'
        f'             data-start="{total + 0.25:g}" data-duration="{vo:g}" data-track-index="4"></audio>')
    print(f"plan {f['n']:02d} {f['slug']:<24} {f['dur']:>5}s  VO {vo:>6.2f}s  {size//1024} ko")
    total += f["dur"]

index = f"""<!doctype html>
<html lang="fr">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Hello Harel — une journée dans un atelier agroalimentaire</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
{FONTFACE_ROOT}
      *{{margin:0;padding:0;box-sizing:border-box}}
      html,body{{width:1920px;height:1080px;overflow:hidden;background:#FFFFFF}}
      #root{{position:relative;width:1920px;height:1080px;background:#FFFFFF}}
      .clip{{position:absolute;inset:0}}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0"
         data-duration="{total:g}" data-width="1920" data-height="1080">
{chr(10).join(rows_host)}

{chr(10).join(rows_audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
open(f"{P}/index.html", "w").write(index)
print(f"\nindex.html ecrit — {total:g}s au total, {len(FRAMES)} plans")
