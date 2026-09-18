#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reporting hebdomadaire Hello Harel — requêtes métier, évolution des positions.

Source unique : Google Search Console, propriété https://www.helloharel.com/,
lue via Composio. Aucune estimation, aucun chiffre de tiers.

Périmètre : les requêtes qui portent A LA FOIS un métier (agroalimentaire,
fruits et légumes, boulangerie, négoce, traiteur, viande, laitier, marée…) ET
une intention d'outil (erp, logiciel, progiciel, solution, crm). C'est ce que
cherche quelqu'un qui va acheter, pas quelqu'un qui révise un calcul de prix.

Comparaison : 28 jours (19/08 → 15/09) contre les 28 jours précédents
(22/07 → 18/08). La position est la moyenne pondérée par les impressions —
une moyenne simple donnerait le même poids à une requête vue 1 117 fois et à
une requête vue 3 fois.

DA Google Store (client.json : "da": "google-store").
Palette validée par scripts/validate_palette.js du skill dataviz.

Usage :  python3 reporting_semaine.py
"""

import json
import os
import re

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "reporting-semaine.html")

PERIODE = "19 août → 15 septembre 2026"
PRECEDENT = "22 juillet → 18 août 2026"

# Paire catégorielle validée : ΔE normal 36,9 · protan 30,3 · tritan 30,8
BLEU, ORANGE = "#1a73e8", "#E37400"
VERT, ROUGE = "#188038", "#c5221f"


def nb(v):
    return "{:,}".format(int(round(v))).replace(",", " ")


def virg(v):
    return ("%.1f" % v).replace(".", ",")


def signe(v):
    return ("+" if v > 0 else "−") + virg(abs(v))


# ═══════════════════════════════════════════════════════ briques visuelles
def tuile(valeur, libelle, detail, ton=""):
    return ('<div class="tuile%s"><p class="tuile-v">%s</p>'
            '<p class="tuile-l">%s</p><p class="tuile-d">%s</p></div>'
            % ((" tuile--" + ton) if ton else "", valeur, libelle, detail))


def courbe(semaines):
    """La position dans le temps. L'axe est INVERSÉ : la 1re place est en haut.

    Une courbe de position tracée à l'endroit se lit à l'envers — « ça monte »
    voudrait dire « ça se dégrade ». On inverse l'axe, et on le dit sous le titre.
    """
    L, H = 980.0, 260.0
    mg, mh, md, mb = 48, 20, 16, 34
    pos = [s["pos"] for s in semaines]
    hi, lo = max(1.0, min(pos) - 3), max(pos) + 3
    x = lambda i: mg + i * (L - mg - md) / max(1, len(semaines) - 1)
    y = lambda p: mh + (p - hi) * (H - mh - mb) / (lo - hi)

    grille = etiq = ""
    for p in range(5, int(lo) + 5, 5):
        if not (hi <= p <= lo):
            continue
        grille += ('<line x1="%.0f" y1="%.1f" x2="%.0f" y2="%.1f" class="g"/>'
                   % (mg, y(p), L - md, y(p)))
        etiq += ('<text x="%.0f" y="%.1f" class="ax ax--y">%d<tspan class="e">e</tspan>'
                 '</text>' % (mg - 10, y(p) + 4, p))

    d = " ".join(("M" if i == 0 else "L") + "%.1f %.1f" % (x(i), y(s["pos"]))
                 for i, s in enumerate(semaines))
    aire = d + " L%.1f %.1f L%.1f %.1f Z" % (x(len(semaines) - 1), H - mb, x(0), H - mb)

    pts = xs = ""
    for i, s in enumerate(semaines):
        der = i == len(semaines) - 1
        pts += ('<circle cx="%.1f" cy="%.1f" r="%d" class="pt%s">'
                '<title>Semaine du %s — position moyenne %s, %s impressions%s</title>'
                '</circle>'
                % (x(i), y(s["pos"]), 6 if der else 5, " pt--part" if der else "",
                   s["semaine"], virg(s["pos"]), nb(s["imp"]),
                   " (semaine incomplète)" if der else ""))
        if i % 2 == 0 or der:
            xs += ('<text x="%.1f" y="%.0f" class="ax">%s</text>'
                   % (x(i), H - 10, s["semaine"][8:10] + "/" + s["semaine"][5:7]))

    # On n'étiquette que le début, le pire et la fin : jamais tous les points.
    pire = max(range(len(semaines)), key=lambda i: semaines[i]["pos"])
    lab = ""
    for i in sorted({0, pire, len(semaines) - 1}):
        ancre = "start" if i == 0 else ("end" if i == len(semaines) - 1 else "middle")
        dx = 8 if i == 0 else (-8 if i == len(semaines) - 1 else 0)
        lab += ('<text x="%.1f" y="%.1f" class="val" text-anchor="%s">%s</text>'
                % (x(i) + dx, y(semaines[i]["pos"]) - 13, ancre, virg(semaines[i]["pos"])))

    return ('<svg viewBox="0 0 %d %d" class="graph" role="img" '
            'aria-label="Position moyenne par semaine sur les requêtes métier, '
            'de la semaine du %s à celle du %s">'
            '<defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s" stop-opacity=".16"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient></defs>'
            '%s<path d="%s" fill="url(#ga)"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="2.5" '
            'stroke-linejoin="round" stroke-linecap="round"/>%s%s%s%s</svg>'
            % (int(L), int(H), semaines[0]["semaine"], semaines[-1]["semaine"],
               BLEU, BLEU, grille, aire, d, BLEU, pts, etiq, xs, lab))


def barres_imp(semaines):
    maxi = max(s["imp"] for s in semaines)
    b = ""
    for i, s in enumerate(semaines):
        der = i == len(semaines) - 1
        b += ('<span class="imp-b%s" style="height:%.0f%%" tabindex="0" '
              'title="Semaine du %s — %s impressions%s"></span>'
              % (" imp-b--part" if der else "", 100.0 * s["imp"] / maxi,
                 s["semaine"], nb(s["imp"]), " (semaine incomplète)" if der else ""))
    return '<div class="imp">%s</div>' % b


def haltere(metiers):
    """Avant / après sur le même axe : la distance EST la variation."""
    maxi = max(max(m["pos"], m["pos0"]) for m in metiers) + 4
    li = ""
    for m in metiers:
        a, b = m["pos0"], m["pos"]
        mieux = b < a
        x1, x2 = 100.0 * min(a, b) / maxi, 100.0 * max(a, b) / maxi
        li += (
            '<div class="halt" tabindex="0" title="%s — %s : %s puis %s">'
            '<span class="halt-l">%s <em>%d requêtes · %s impr.</em></span>'
            '<span class="halt-p">'
            '<i class="halt-t" style="left:%.1f%%;width:%.1f%%;background:%s"></i>'
            '<i class="halt-a" style="left:%.1f%%"><b>%s</b></i>'
            '<i class="halt-b" style="left:%.1f%%;background:%s"><b>%s</b></i>'
            '</span><span class="halt-d %s">%s</span></div>'
            % (m["metier"], "progresse" if mieux else "recule", virg(a), virg(b),
               m["metier"], m["n"], nb(m["imp"]),
               x1, max(0.6, x2 - x1), VERT if mieux else ROUGE,
               100.0 * a / maxi, virg(a),
               100.0 * b / maxi, VERT if mieux else ROUGE, virg(b),
               "up" if mieux else "down", signe(m["delta"])))
    return ('<div class="halteres">%s</div>'
            '<div class="legende">'
            '<span><i class="rond" style="background:#9aa0a6"></i>Position sur %s</span>'
            '<span><i class="rond" style="background:%s"></i>Aujourd\'hui — progression</span>'
            '<span><i class="rond" style="background:%s"></i>Aujourd\'hui — recul</span>'
            '</div>' % (li, PRECEDENT, VERT, ROUGE))


def liste_q(items, sens):
    li = ""
    for x in items:
        li += ('<li><span class="q">%s</span>'
               '<span class="q-p"><b>%s</b> <em>← %s</em></span>'
               '<span class="q-i">%s impressions</span>'
               '<span class="q-d %s">%s</span></li>'
               % (x["q"], virg(x["pos"]), virg(x["pos0"]), nb(x["imp"]), sens,
                  signe(x["delta"])))
    return '<ul class="qs">%s</ul>' % li


# ═══════════════════════════════════════════════════════ contenu éditorial
ROADMAP = [
    ("Terminé cette semaine", "fait", [
        ("Méga-menu unifié sur 174 contenus", "16 métiers, desktop et mobile"),
        ("Bentos → module à onglets sur 31 pages", "fonctionnalités + fiches métier"),
        ("3 landings de septembre publiées", "PME en croissance, fruits &amp; légumes, "
                                             "produits de la mer — en noindex"),
        ("/agroalimentaire/ : copie, refonte, remaniement", "4 maquettes livrées"),
    ]),
    ("En cours", "cours", [
        ("Refonte /agroalimentaire/", "maquette remaniée validée — reste la décision de "
                                      "mise en ligne (page protégée)"),
        ("Photos de héros des pages métier", "planches livrées, en attente de ton choix"),
    ]),
    ("À traiter, par ordre d'impact", "todo", [
        ("« erp agroalimentaire » : 15,6 → 20,0", "1 117 impressions, 2 clics — la requête "
                                                  "n° 1 décroche, c'est la priorité"),
        ("Anti-spam formulaires (PHP)", "fichier prêt, installation serveur à faire"),
        ("Délivrabilité e-mail", "SPF en double, ni DKIM ni DMARC — 0 mail depuis le 10/08"),
        ("16 pages filles MIN", "Nantes en tête de file"),
    ]),
]

ARTEFACTS = [
    ("Image héros", "Photos des pages métier",
     "L'image actuelle de chaque page métier et ses remplaçantes proposées, libres de "
     "droit — en attente de ton choix.",
     "https://claude.ai/artifact/SM5JQeFuzGp1NhbNRB4LCY"),
    ("Refonte ERP agroalimentaire", "/agroalimentaire/ remaniée",
     "Les treize demandes appliquées : mur de 25 logos, FAQ des pages sœurs, avis en "
     "carrousel continu, section guide vers le hub.",
     "https://claude.ai/artifact/XSMvyCT6bTPWnAhB4FJFe7"),
]


def main():
    d = json.load(open(os.path.join(S, "gsc-metier.json"), encoding="utf-8"))
    sem = json.load(open(os.path.join(S, "gsc-semaines.json"), encoding="utf-8"))
    g = d["global"]

    tuiles = "".join([
        tuile(nb(g["n"]), "requêtes métier suivies",
              "%s impressions, contre %s" % (nb(g["imp"]), nb(g["imp0"]))),
        tuile(virg(g["pos"]), "position moyenne",
              "%s — elle était à %s" % (signe(g["delta"]), virg(g["pos0"])),
              ton="ko" if g["delta"] < 0 else "ok"),
        tuile(nb(g["top10"]), "requêtes en page 1",
              "+%d — elles étaient %d" % (g["top10"] - g["top10_0"], g["top10_0"]), ton="ok"),
        tuile("%d / %d" % (g["progressent"], g["reculent"]), "progressent / reculent",
              "sur %d requêtes suivies · %d nouvelles" % (g["suivies"], g["nouvelles"])),
    ])

    valeurs = dict(
        periode=PERIODE, precedent=PRECEDENT, tuiles=tuiles,
        courbe=courbe(sem), imp=barres_imp(sem),
        pos_debut=virg(sem[0]["pos"]), pos_fin=virg(sem[-2]["pos"]),
        pos_pire=virg(max(s["pos"] for s in sem)),
        haltere=haltere(d["metiers"]),
        gagne=liste_q(d["gagne"][:6], "up"), perd=liste_q(d["perd"][:6], "down"),
        nb_q=nb(g["n"]), imp_tot=nb(g["imp"]), clics=g["clics"], clics0=g["clics0"],
        road="".join(
            '<div class="kan kan--%s"><h3>%s <em>%d</em></h3><ul>%s</ul></div>'
            % (cl, t, len(it), "".join('<li><b>%s</b><span>%s</span></li>' % (a, b)
                                       for a, b in it))
            for t, cl, it in ROADMAP),
        arte="".join(
            '<a class="arte" href="%s" target="_blank" rel="noopener">'
            '<span class="arte-k">Artefact</span><b>%s</b><span class="arte-s">%s</span>'
            '<span class="arte-d">%s</span><span class="arte-c">Ouvrir →</span></a>'
            % (u, t, s, x) for t, s, x, u in ARTEFACTS),
    )

    html = GABARIT
    for cle, val in valeurs.items():
        html = html.replace("{{%s}}" % cle, str(val))
    reste = re.findall(r"\{\{(\w+)\}\}", html)
    if reste:
        raise SystemExit("ARRÊT — jeton non remplacé : %s" % sorted(set(reste)))

    open(SORTIE, "w", encoding="utf-8").write(html)
    print("écrit : %s (%d ko)" % (SORTIE, len(html) // 1024))

    pb = []
    if re.search(r'<img[^>]+src="https?://', html):
        pb.append("image distante")
    for t in ("section", "div", "svg", "ul", "li"):
        o, f = len(re.findall(r"<%s[\s>]" % t, html)), len(re.findall(r"</%s>" % t, html))
        if o != f:
            pb.append("%s : %d ouvertes, %d fermées" % (t, o, f))
    if html.count("<h1") != 1:
        pb.append("il faut un seul H1")
    print("contrôles : %s" % ("tout est vert" if not pb else pb))


GABARIT = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Positions métier Hello Harel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
 color-scheme:light;
 --action:#1a73e8;--action-hover:#1b66c9;--focus:#aecbfa;--orange:#E37400;
 --vert:#188038;--rouge:#c5221f;
 --bg:#fff;--surface:#f8f9fa;--surface-2:#f1f3f4;
 --ink:#1f1f1f;--ink-2:#5f6368;--line:#e8eaed;
 --r-card:28px;--r-md:16px;--r-pill:999px;
 --shadow:0 1px 2px rgba(60,64,67,.08),0 1px 3px rgba(60,64,67,.06);
 --shadow-h:0 6px 18px rgba(60,64,67,.12),0 2px 6px rgba(60,64,67,.08);
 --max:1180px;
 --display:'Google Sans Flex','Google Sans','Product Sans','Roboto',system-ui,sans-serif;
 --body:'Roboto',system-ui,'Segoe UI',Arial,sans-serif;
 --mono:'Roboto Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);
 font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--display);letter-spacing:-.01em;margin:0;font-weight:600}
p,ul,figure{margin:0}ul{list-style:none;padding:0}
a{color:var(--action);text-decoration:none}a:hover{color:var(--action-hover)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px;border-radius:8px}
sup{font-size:.62em}
.wrap{max-width:var(--max);margin-inline:auto;padding-inline:24px}
.sec{padding-block:clamp(32px,5vw,56px)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;
 color:var(--ink-2);margin-bottom:8px}
.sec>.wrap>h2{font-size:clamp(1.35rem,2.6vw,1.9rem);margin-bottom:8px}
.sec>.wrap>h2+p{color:var(--ink-2);margin-bottom:24px;max-width:74ch}
.sec>.wrap>h2+p b{color:var(--ink);font-weight:500}

.hdr{background:linear-gradient(180deg,#f8f9fa,#fff);border-bottom:1px solid var(--line)}
.hdr .wrap{padding-block:40px 32px}
.hdr h1{font-size:clamp(1.7rem,4vw,2.5rem);font-weight:700}
.hdr .sous{color:var(--ink-2);margin-top:8px;max-width:78ch}
.puce{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:.72rem;
 letter-spacing:.1em;text-transform:uppercase;color:#174ea6;background:#e8f0fe;
 padding:6px 14px;border-radius:var(--r-pill);margin-bottom:16px}

.tuiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:16px}
.tuile{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);padding:24px;
 box-shadow:var(--shadow);transition:box-shadow .25s,transform .25s}
.tuile:hover{box-shadow:var(--shadow-h);transform:translateY(-2px)}
.tuile--ok{background:#e6f4ea;border-color:#ceead6}
.tuile--ko{background:#fce8e6;border-color:#fad2cf}
.tuile-v{font-family:var(--display);font-size:clamp(2rem,4.5vw,2.9rem);font-weight:700;
 line-height:1.05;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.tuile--ok .tuile-v{color:var(--vert)}.tuile--ko .tuile-v{color:var(--rouge)}
.tuile-l{font-weight:500;margin-top:4px}
.tuile-d{color:var(--ink-2);font-size:.84rem;margin-top:6px}

.card{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);
 padding:clamp(20px,3vw,32px);box-shadow:var(--shadow)}
.card h3{font-size:1.05rem;margin-bottom:4px}
.card h3+p{color:var(--ink-2);font-size:.88rem;margin-bottom:20px}

.graph{width:100%;height:auto;display:block;overflow:visible}
.graph .g{stroke:var(--line);stroke-width:1}
.graph .ax{font-family:var(--mono);font-size:11px;fill:var(--ink-2);text-anchor:middle}
.graph .ax--y{text-anchor:end}
.graph .e{font-size:8px;baseline-shift:super}
.graph .val{font-family:var(--display);font-size:14px;font-weight:600;fill:var(--ink)}
.graph .pt{fill:#fff;stroke:#1a73e8;stroke-width:2.5}
.graph .pt:hover{fill:#1a73e8}
.graph .pt--part{stroke-dasharray:3 2}
.axe-note{font-family:var(--mono);font-size:.7rem;color:var(--ink-2);margin-top:20px;
 padding-top:16px;border-top:1px solid var(--line)}
.imp{display:flex;align-items:flex-end;gap:5px;height:54px;margin-top:8px}
.imp-b{flex:1;background:#d2e3fc;border-radius:4px 4px 0 0;min-height:4px}
.imp-b:hover{background:#8ab4f8}
.imp-b--part{background:repeating-linear-gradient(135deg,#d2e3fc 0 4px,#fff 4px 8px)}

.halteres{display:grid;gap:18px}
.halt{display:grid;grid-template-columns:250px 1fr 66px;align-items:center;gap:16px;
 padding:8px 4px;border-radius:10px}
.halt:hover,.halt:focus-visible{background:var(--surface)}
.halt-l{font-size:.92rem;font-weight:500;line-height:1.3}
.halt-l em{display:block;font-style:normal;font-family:var(--mono);font-size:.7rem;
 color:var(--ink-2);margin-top:2px}
.halt-p{position:relative;height:36px}
.halt-t{position:absolute;top:16px;height:4px;border-radius:2px;opacity:.55}
.halt-a,.halt-b{position:absolute;top:11px;width:14px;height:14px;border-radius:50%;
 transform:translateX(-7px);border:2px solid #fff}
.halt-a{background:#9aa0a6}
.halt-a b,.halt-b b{position:absolute;left:50%;transform:translateX(-50%);
 font-family:var(--mono);font-size:.68rem;font-weight:500;white-space:nowrap}
.halt-a b{top:-18px;color:var(--ink-2)}
.halt-b b{top:17px;color:var(--ink);font-weight:600}
.halt-d{text-align:right;font-family:var(--mono);font-size:.86rem;font-weight:500;
 font-variant-numeric:tabular-nums}
.halt-d.up{color:var(--vert)}.halt-d.down{color:var(--rouge)}
@media(max-width:760px){.halt{grid-template-columns:1fr 62px;
 grid-template-areas:"l d" "p p"}.halt-l{grid-area:l}.halt-d{grid-area:d}
 .halt-p{grid-area:p;margin-top:10px}}
.legende{display:flex;flex-wrap:wrap;gap:20px;font-size:.82rem;color:var(--ink-2);
 margin-top:28px;padding-top:16px;border-top:1px solid var(--line)}
.legende i.rond{display:inline-block;width:12px;height:12px;border-radius:50%;
 margin-right:7px;vertical-align:-1px}

.duo{display:grid;grid-template-columns:1fr;gap:16px}
@media(min-width:900px){.duo{grid-template-columns:1fr 1fr}}
.qs li{display:grid;grid-template-columns:1fr auto;gap:2px 14px;padding:13px 0;
 border-bottom:1px solid var(--line)}
.qs li:last-child{border-bottom:0;padding-bottom:0}
.q{font-size:.92rem;font-weight:500}
.q-p{font-family:var(--mono);font-size:.82rem;text-align:right;
 font-variant-numeric:tabular-nums}
.q-p b{font-weight:600}.q-p em{font-style:normal;color:var(--ink-2)}
.q-i{font-size:.76rem;color:var(--ink-2)}
.q-d{font-family:var(--mono);font-size:.78rem;font-weight:500;text-align:right}
.q-d.up{color:var(--vert)}.q-d.down{color:var(--rouge)}

.note{display:flex;gap:14px;align-items:flex-start;background:#fef7e0;
 border:1px solid #feefc3;border-radius:var(--r-md);padding:18px 22px;font-size:.92rem}
.note svg{flex:0 0 20px;width:20px;height:20px;margin-top:2px;color:var(--orange)}
.note b{font-weight:600}
.note code{font-family:var(--mono);font-size:.82rem;background:#fff;padding:2px 7px;
 border-radius:6px}

.kanban{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}
.kan{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);padding:24px;
 box-shadow:var(--shadow)}
.kan h3{display:flex;align-items:center;gap:10px;font-size:1rem;margin-bottom:16px;
 padding-bottom:12px;border-bottom:1px solid var(--line)}
.kan h3 em{font-style:normal;font-family:var(--mono);font-size:.72rem;font-weight:500;
 background:var(--surface-2);color:var(--ink-2);padding:2px 9px;border-radius:var(--r-pill);
 margin-left:auto}
.kan h3::before{content:"";width:10px;height:10px;border-radius:50%;flex:0 0 10px}
.kan--fait h3::before{background:var(--vert)}
.kan--cours h3::before{background:var(--action)}
.kan--todo h3::before{background:var(--orange)}
.kan li{padding:12px 0;border-bottom:1px solid var(--line)}
.kan li:last-child{border-bottom:0;padding-bottom:0}
.kan li b{display:block;font-weight:500;font-size:.92rem}
.kan li span{display:block;color:var(--ink-2);font-size:.84rem;margin-top:3px}

.artes{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.arte{display:flex;flex-direction:column;gap:6px;background:#fff;border:1px solid var(--line);
 border-radius:var(--r-card);padding:28px;box-shadow:var(--shadow);color:var(--ink);
 transition:box-shadow .25s,transform .25s}
.arte:hover{box-shadow:var(--shadow-h);transform:translateY(-2px);color:var(--ink)}
.arte-k{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;
 color:#174ea6}
.arte b{font-family:var(--display);font-size:1.15rem;font-weight:600}
.arte-s{color:var(--ink-2);font-size:.9rem}
.arte-d{font-size:.86rem;color:var(--ink-2);margin-top:8px;flex:1}
.arte-c{margin-top:16px;color:var(--action);font-weight:500;font-size:.9rem}

.pied{border-top:1px solid var(--line);background:var(--surface)}
.pied .wrap{padding-block:28px;font-size:.84rem;color:var(--ink-2)}
@media (prefers-reduced-motion:reduce){*{transition-duration:.001ms !important}}
</style></head><body>

<header class="hdr"><div class="wrap">
 <p class="puce">Requêtes métier · Search Console</p>
 <h1>Évolution des positions</h1>
 <p class="sous">{{periode}}, comparé à {{precedent}} · {{nb_q}} requêtes qui associent un
 métier et une intention d'outil · {{imp_tot}} impressions.</p>
</div></header>

<main>

<section class="sec"><div class="wrap"><div class="tuiles">{{tuiles}}</div></div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Évolution</p>
 <h2>La position moyenne, semaine après semaine</h2>
 <p>Le site est passé de la <b>{{pos_debut}}<sup>e</sup></b> place fin juin à un creux de
 <b>{{pos_pire}}<sup>e</sup></b> mi-août, puis remonte à <b>{{pos_fin}}<sup>e</sup></b>.
 Sur la même période les impressions montent : le site apparaît sur <b>plus</b> de
 requêtes, mais <b>plus bas</b>.</p>
 <div class="card">
  <h3>Position moyenne pondérée par les impressions</h3>
  <p>Axe inversé : la 1<sup>re</sup> place est en haut. Dernier point = semaine incomplète.</p>
  {{courbe}}
  <p class="axe-note">Impressions par semaine</p>
  {{imp}}
 </div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Par métier</p>
 <h2>Qui monte, qui descend</h2>
 <p>Chaque ligne relie la position d'avant à celle d'aujourd'hui. <b>Le négoce et la
 boulangerie gagnent plus de dix places</b> ; l'agroalimentaire générique et la viande
 reculent.</p>
 <div class="card">{{haltere}}</div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Détail</p>
 <h2>Les six plus gros mouvements, dans chaque sens</h2>
 <div class="duo">
  <div class="card"><h3>Ce qui progresse</h3><p>Position aujourd'hui ← position d'avant</p>
  {{gagne}}</div>
  <div class="card"><h3>Ce qui recule</h3><p>Position aujourd'hui ← position d'avant</p>
  {{perd}}</div>
 </div>
 <div class="note" style="margin-top:20px">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
   stroke-linecap="round"><path d="M12 9v4m0 4h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0
   1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
  <span><b>La priorité tient en une requête.</b> <code>erp agroalimentaire</code> pèse
  1 117 impressions à elle seule — un quart du total métier — et passe de la
  15,6<sup>e</sup> à la 20<sup>e</sup> place. Elle a rapporté <b>2 clics</b> en 28 jours.
  Tant qu'elle reste en page 2, les gains ailleurs ne compensent pas : sur l'ensemble,
  {{clics}} clics contre {{clics0}}.</span>
 </div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Roadmap</p>
 <h2>Où en sont les chantiers</h2>
 <div class="kanban">{{road}}</div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Livrables</p>
 <h2>Artefacts</h2>
 <div class="artes">{{arte}}</div>
</div></section>

</main>

<footer class="pied"><div class="wrap">
 <p><b>Source.</b> Google Search Console, propriété https://www.helloharel.com/, recherche
 web, données finales. Période {{periode}} comparée à {{precedent}}. La position est la
 moyenne pondérée par les impressions. Périmètre : les requêtes portant à la fois un métier
 et une intention d'outil (erp, logiciel, progiciel, solution, crm) — {{nb_q}} requêtes,
 {{imp_tot}} impressions. Les données GSC accusent deux à trois jours de retard : la
 dernière semaine est incomplète et signalée comme telle.</p>
</div></footer>
</body></html>"""


if __name__ == "__main__":
    main()
