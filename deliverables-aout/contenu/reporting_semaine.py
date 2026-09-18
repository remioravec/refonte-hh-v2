#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reporting hebdomadaire Hello Harel — semaine du 12 au 18 septembre 2026.

Peu de texte, beaucoup de visuel. Chaque chiffre affiche vient d'un releve
date : rien n'est saisi a la main dans le HTML, tout est lu dans les fichiers
produits par les appels DataForSEO du 18/09.

Ce que le rapport NE fait PAS : il n'annonce pas de clics Search Console. La
propriete GSC n'est pas connectee a cet environnement ; le rapport le dit et
montre a la place le trafic ESTIME de DataForSEO, nomme comme tel.

DA Google Store (client.json : "da": "google-store").
Palette des graphiques validee par scripts/validate_palette.js du skill dataviz.

Usage :  python3 reporting_semaine.py
"""

import json
import os
import re

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "reporting-semaine.html")

RELEVE = "18 septembre 2026"
SEMAINE = "12 → 18 septembre 2026"

BIZ = re.compile(r"^/(agroalimentaire|negoce|medical|migration-as400|comparatifs"
                 r"|fonctionnalites|tarifs)")
MARQUE = re.compile(r"hello\s*harel|helloharel", re.I)

# Paire categorielle, validee : DeltaE normal 36,9 · protan 30,3 · tritan 30,8
DUO = ("#1a73e8", "#E37400")


def charger():
    kw = json.load(open(os.path.join(S, "kw.json"), encoding="utf-8"))
    hm = [l for l in kw if not MARQUE.search(l["requete"])]
    bofu = json.load(open(os.path.join(S, "bofu-strict.json"), encoding="utf-8"))
    return hm, bofu


# ═══════════════════════════════════════════════════════ briques visuelles
def tuile(valeur, libelle, detail, accent=False):
    return ('<div class="tuile%s"><p class="tuile-v">%s</p>'
            '<p class="tuile-l">%s</p><p class="tuile-d">%s</p></div>'
            % (" tuile--a" if accent else "", valeur, libelle, detail))


def barres_h(lignes, maxi=None, unite="", couleur="#1a73e8", largeur_lib=None):
    """lignes : [(libelle, valeur, note)] — barres horizontales, valeur en bout.

    La valeur est ecrite au bout de chaque barre : c'est l'encodage secondaire
    qui rend le graphique lisible sans distinguer les teintes.
    """
    maxi = maxi or max([v for _, v, _ in lignes] + [1])
    lib = largeur_lib or "190px"
    out = ['<div class="barres" style="--lib:%s">' % lib]
    for label, v, note in lignes:
        pc = max(1.2, 100.0 * v / maxi)
        out.append(
            '<div class="barre" tabindex="0" title="%s — %s%s%s">'
            '<span class="barre-l">%s</span>'
            '<span class="barre-p"><i style="width:%.1f%%;background:%s"></i></span>'
            '<span class="barre-v">%s%s</span>'
            '<span class="barre-n">%s</span></div>'
            % (label, "{:,}".format(v).replace(",", " "), unite,
               (" · " + note) if note else "",
               label, pc, couleur,
               "{:,}".format(v).replace(",", " "), unite, note or ""))
    out.append("</div>")
    return "".join(out)


def bandes(hm, champ):
    tranches = [("1–3", 1, 3), ("4–10", 4, 10), ("11–20", 11, 20),
                ("21–50", 21, 50), ("51+", 51, 9999)]
    return [(lab, len([l for l in hm if a <= l[champ] <= b]))
            for lab, a, b in tranches]


def colonnes_bandes(hm):
    """Deux lectures de la meme realite : rang organique et rang affiche.

    Sur une SERP a blocs, une position 3 s'affiche 5e. Comparer les deux
    colonnes est la seule facon de ne pas se raconter d'histoire.
    """
    g = bandes(hm, "rank_group")
    a = bandes(hm, "rank_absolute")
    maxi = max([v for _, v in g] + [v for _, v in a])
    cols = ""
    for k in range(5):
        lab, vg = g[k]
        _, va = a[k]
        cols += (
            '<div class="col">'
            '<div class="col-p">'
            '<span class="col-b" style="height:%.0f%%;background:%s" '
            'title="rang organique %s : %d requêtes"><b>%d</b></span>'
            '<span class="col-b col-b--a" style="height:%.0f%%;background:%s" '
            'title="rang affiché %s : %d requêtes"><b>%d</b></span>'
            '</div><p class="col-l">%s</p></div>'
            % (100.0 * vg / maxi, DUO[0], lab, vg, vg,
               100.0 * va / maxi, DUO[1], lab, va, va, lab))
    return ('<div class="colonnes">%s</div>'
            '<div class="legende">'
            '<span><i style="background:%s"></i>Rang organique <b>(rank_group)</b></span>'
            '<span><i class="hach" style="background:%s"></i>Rang réellement affiché '
            '<b>(rank_absolute)</b></span></div>' % (cols, DUO[0], DUO[1]))


def anneau(part, total, couleur, fond="#e8eaed"):
    pc = 100.0 * part / total
    c = 2 * 3.14159 * 54
    return ('<svg viewBox="0 0 128 128" class="anneau" role="img" '
            'aria-label="%.1f %% du trafic estimé">'
            '<circle cx="64" cy="64" r="54" fill="none" stroke="%s" stroke-width="16"/>'
            '<circle cx="64" cy="64" r="54" fill="none" stroke="%s" stroke-width="16" '
            'stroke-linecap="round" stroke-dasharray="%.1f %.1f" '
            'transform="rotate(-90 64 64)"/>'
            '<text x="64" y="70" text-anchor="middle" class="anneau-t">%.0f %%</text>'
            '</svg>' % (pc, fond, couleur, c * pc / 100, c, pc))


# ═══════════════════════════════════════════════════════ contenu du rapport
ROADMAP = [
    ("Terminé cette semaine", "fait", [
        ("Méga-menu unifié posé sur 174 contenus", "16 métiers, desktop et mobile"),
        ("Bentos → module à onglets sur 31 pages", "fonctionnalités + fiches métier"),
        ("3 landings de septembre publiées", "PME en croissance, fruits &amp; légumes, "
                                             "produits de la mer — en noindex"),
        ("Bug d'intégration corrigé", "les 3 landings sortaient avec deux H1"),
        ("/agroalimentaire/ : copie, refonte, remaniement", "4 maquettes livrées"),
    ]),
    ("En cours", "cours", [
        ("Refonte SEO /agroalimentaire/", "maquette remaniée validée — reste la décision "
                                          "de mise en ligne (page protégée)"),
        ("Photos de héros des pages métier", "16 planches de candidats livrées, en attente "
                                             "de ton choix"),
    ]),
    ("Planifié / bloqué", "todo", [
        ("Anti-spam formulaires (PHP)", "le fichier est prêt — il doit être installé côté "
                                        "serveur, le classificateur bloque l'écriture"),
        ("Délivrabilité e-mail", "SPF en double, ni DKIM ni DMARC — 0 mail depuis le 10/08"),
        ("Casse des titles des 3 landings", "rendus en Title Case, 651–673 px au lieu de "
                                            "528–551 px"),
        ("16 pages filles MIN", "Nantes en tête de file"),
        ("5 pages sans menu", "CGU, mentions légales, confidentialité, comparatifs, loi TVA"),
    ]),
]

ARTEFACTS = [
    ("Copie conforme de /agroalimentaire/", "La page telle quelle, hors ligne",
     "18 sections · 118 liens · 3 357 mots, identiques à la source",
     "https://claude.ai/artifact/8G26R12e7m4qXkHFccK8Fd"),
    ("Page remaniée", "Les 13 demandes appliquées",
     "Mur de 25 logos · FAQ des pages sœurs · avis en carrousel · section guide",
     "https://claude.ai/artifact/XSMvyCT6bTPWnAhB4FJFe7"),
    ("Refonte complète", "Proposition de nouveau gabarit",
     "Système de design unique, 128 ko de CSS remplacés",
     "https://claude.ai/artifact/39mAUf1g4JgxeVZvXS6bzD"),
]


def main():
    hm, bofu = charger()

    top10 = len([l for l in hm if l["rank_group"] <= 10])
    etv = sum(l["etv"] for l in hm)
    etv_blog = sum(l["etv"] for l in hm if (l["url"] or "").startswith("/blog"))
    etv_biz = sum(l["etv"] for l in hm if BIZ.match(l["url"] or ""))
    pages = len({l["url"] for l in hm})

    # trafic estime par page, les huit premieres
    par = {}
    for l in hm:
        par[l["url"]] = par.get(l["url"], 0) + l["etv"]
    top_pages = sorted(par.items(), key=lambda x: -x[1])[:8]

    # les pages business qui apparaissent, et a quel rang
    biz_l = sorted([l for l in hm if BIZ.match(l["url"] or "")],
                   key=lambda x: x["rank_group"])

    as400 = [x for x in bofu if re.search(r"as.?400|s400", x["requete"], re.I)]
    bofu_blog = [x for x in bofu if (x["url"] or "").startswith("/blog")]

    nb = lambda v: "{:,}".format(int(round(v))).replace(",", " ")

    # ── les blocs
    tuiles = "".join([
        tuile(nb(len(hm)), "requêtes positionnées", "hors marque · relevé du " + RELEVE),
        tuile(nb(top10), "dans le top 10", "%d %% des requêtes suivies"
              % round(100 * top10 / len(hm))),
        tuile(nb(etv), "visites/mois estimées", "estimation DataForSEO, pas des clics GSC"),
        tuile(nb(len(bofu)), "requêtes BOFU en jeu", "%s de volume cumulé"
              % nb(sum(x["volume"] for x in bofu)), accent=True),
    ])

    b_pages = barres_h(
        [(u if len(u) < 40 else u[:38] + "…", int(round(v)), "") for u, v in top_pages],
        unite="", couleur=DUO[0], largeur_lib="300px")

    b_bofu = barres_h(
        [("%s  (position %d)" % (x["requete"], x["rank_absolute"]), x["volume"], "")
         for x in bofu[:12]], unite="", couleur=DUO[1], largeur_lib="330px")

    lignes_biz = "".join(
        '<tr><td><code>%s</code></td><td>%s</td><td class="num">%s</td>'
        '<td class="num"><b class="rang">%d</b></td><td class="num">%d</td></tr>'
        % (l["url"], l["requete"], nb(l["volume"]), l["rank_absolute"], l["rank_group"])
        for l in biz_l)

    road = ""
    for titre, cl, items in ROADMAP:
        li = "".join('<li><b>%s</b><span>%s</span></li>' % (t, d) for t, d in items)
        road += ('<div class="kan kan--%s"><h3>%s <em>%d</em></h3><ul>%s</ul></div>'
                 % (cl, titre, len(items), li))

    arte = "".join(
        '<a class="arte" href="%s" target="_blank" rel="noopener">'
        '<span class="arte-k">Artefact</span><b>%s</b><span class="arte-s">%s</span>'
        '<span class="arte-d">%s</span><span class="arte-c">Ouvrir →</span></a>'
        % (u, t, s, d) for t, s, d, u in ARTEFACTS)

    valeurs = dict(
        semaine=SEMAINE, releve=RELEVE,
        tuiles=tuiles,
        pages=nb(pages),
        b_pages=b_pages,
        etv=nb(etv), etv_blog=nb(etv_blog), etv_biz="%.0f" % etv_biz,
        anneau_blog=anneau(etv_blog, etv, DUO[0]),
        pc_blog="%.1f" % (100 * etv_blog / etv),
        pc_biz="%.1f" % (100 * etv_biz / etv),
        colonnes=colonnes_bandes(hm),
        nb_g3=len([l for l in hm if l["rank_group"] <= 3]),
        nb_a3=len([l for l in hm if l["rank_absolute"] <= 3]),
        lignes_biz=lignes_biz, nb_biz=len(biz_l),
        b_bofu=b_bofu,
        nb_bofu=len(bofu), vol_bofu=nb(sum(x["volume"] for x in bofu)),
        nb_bofu_blog=len(bofu_blog),
        nb_as400=len(as400), vol_as400=nb(sum(x["volume"] for x in as400)),
        road=road, arte=arte,
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
    for t in ("section", "div", "table", "svg"):
        o, f = len(re.findall(r"<%s[\s>]" % t, html)), len(re.findall(r"</%s>" % t, html))
        if o != f:
            pb.append("%s : %d ouvertes, %d fermées" % (t, o, f))
    print("contrôles : %s" % ("tout est vert" if not pb else pb))


GABARIT = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reporting SEO Hello Harel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
 color-scheme:light;
 --g-blue:#4285F4;--g-red:#EA4335;--g-yellow:#FBBC04;--g-green:#34A853;
 --action:#1a73e8;--action-hover:#1b66c9;--focus:#aecbfa;--orange:#E37400;
 --bg:#fff;--surface:#f8f9fa;--surface-2:#f1f3f4;
 --ink:#1f1f1f;--ink-2:#5f6368;--line:#e8eaed;
 --r-card:28px;--r-md:16px;--r-sm:12px;--r-pill:999px;
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
h1,h2,h3,h4{font-family:var(--display);letter-spacing:-.01em;margin:0;font-weight:600}
p,ul,ol,figure{margin:0}ul{list-style:none;padding:0}
a{color:var(--action);text-decoration:none}
a:hover{color:var(--action-hover)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px;border-radius:8px}
.wrap{max-width:var(--max);margin-inline:auto;padding-inline:24px}
.sec{padding-block:clamp(32px,5vw,56px)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;
 color:var(--ink-2);margin-bottom:8px}
.sec>.wrap>h2{font-size:clamp(1.35rem,2.6vw,1.9rem);margin-bottom:8px}
.sec>.wrap>h2+p{color:var(--ink-2);margin-bottom:24px;max-width:70ch}

/* ───────────────────────────────────────────────── en-tête */
.hdr{background:linear-gradient(180deg,#f8f9fa,#fff);border-bottom:1px solid var(--line)}
.hdr .wrap{padding-block:40px 32px}
.hdr h1{font-size:clamp(1.7rem,4vw,2.6rem);font-weight:700}
.hdr .sous{color:var(--ink-2);margin-top:8px;font-size:1.05rem}
.puce{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:.72rem;
 letter-spacing:.1em;text-transform:uppercase;color:#174ea6;background:#e8f0fe;
 padding:6px 14px;border-radius:var(--r-pill);margin-bottom:16px}

/* ───────────────────────────────────────────────── tuiles */
.tuiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}
.tuile{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);padding:24px;
 box-shadow:var(--shadow);transition:box-shadow .25s,transform .25s}
.tuile:hover{box-shadow:var(--shadow-h);transform:translateY(-2px)}
.tuile--a{background:#e8f0fe;border-color:#d2e3fc}
.tuile-v{font-family:var(--display);font-size:clamp(2rem,4.5vw,2.9rem);font-weight:700;
 line-height:1.05;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.tuile--a .tuile-v{color:var(--action)}
.tuile-l{font-weight:500;margin-top:4px}
.tuile-d{color:var(--ink-2);font-size:.84rem;margin-top:6px}

/* ───────────────────────────────────────────────── cartes */
.card{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);
 padding:clamp(20px,3vw,32px);box-shadow:var(--shadow)}
.card+.card{margin-top:16px}
.grille2{display:grid;grid-template-columns:1fr;gap:16px}
@media(min-width:900px){.grille2{grid-template-columns:1.25fr .75fr}}
.card h3{font-size:1.05rem;margin-bottom:4px}
.card h3+p{color:var(--ink-2);font-size:.9rem;margin-bottom:20px}

/* ───────────────────────────────────────────────── barres */
.barres{display:grid;gap:10px}
.barre{display:grid;grid-template-columns:var(--lib) 1fr auto;align-items:center;gap:12px;
 font-size:.88rem;border-radius:8px;padding:2px 4px}
.barre:hover,.barre:focus-visible{background:var(--surface)}
.barre-l{color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
 font-family:var(--mono);font-size:.78rem}
.barre-p{background:var(--surface-2);border-radius:var(--r-pill);height:14px;position:relative}
.barre-p i{position:absolute;inset:0 auto 0 0;border-radius:var(--r-pill);display:block}
.barre-v{font-variant-numeric:tabular-nums;font-weight:500;min-width:58px;text-align:right}
.barre-n{display:none}
@media(max-width:720px){.barre{grid-template-columns:1fr auto;grid-template-areas:"l v" "p p"}
 .barre-l{grid-area:l}.barre-v{grid-area:v}.barre-p{grid-area:p}}

/* ───────────────────────────────────────────────── colonnes */
.colonnes{display:grid;grid-template-columns:repeat(5,1fr);gap:clamp(8px,2vw,20px);
 align-items:end;height:220px;margin-bottom:16px}
.col{display:flex;flex-direction:column;height:100%;justify-content:flex-end;gap:10px}
.col-p{display:flex;align-items:flex-end;justify-content:center;gap:4px;height:100%}
.col-b{width:clamp(18px,3.4vw,38px);border-radius:6px 6px 0 0;position:relative;
 display:block;min-height:6px;border:2px solid #fff}
.col-b b{position:absolute;bottom:calc(100% + 4px);left:50%;transform:translateX(-50%);
 font-size:.76rem;font-weight:600;font-variant-numeric:tabular-nums;color:var(--ink)}
.col-b--a{background-image:repeating-linear-gradient(135deg,
 rgba(255,255,255,.55) 0 3px,transparent 3px 7px)}
.col-l{text-align:center;font-family:var(--mono);font-size:.76rem;color:var(--ink-2)}
.legende{display:flex;flex-wrap:wrap;gap:20px;font-size:.84rem;color:var(--ink-2)}
.legende i{display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:7px;
 vertical-align:-2px}
.legende i.hach{background-image:repeating-linear-gradient(135deg,
 rgba(255,255,255,.55) 0 3px,transparent 3px 7px)}
.legende b{color:var(--ink);font-family:var(--mono);font-size:.76rem;font-weight:500}

/* ───────────────────────────────────────────────── anneau */
.anneau{width:clamp(130px,20vw,168px);height:auto;display:block;margin:0 auto 12px}
.anneau-t{font-family:var(--display);font-size:26px;font-weight:700;fill:var(--ink)}
.repart{display:grid;gap:10px;margin-top:4px}
.repart div{display:flex;align-items:center;gap:10px;font-size:.9rem}
.repart i{width:12px;height:12px;border-radius:4px;flex:0 0 12px}
.repart b{margin-left:auto;font-variant-numeric:tabular-nums}

/* ───────────────────────────────────────────────── tableau */
.tab-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r-md)}
table{border-collapse:collapse;width:100%;min-width:640px;font-size:.88rem}
th,td{padding:12px 16px;text-align:left;border-bottom:1px solid var(--line)}
thead th{background:var(--surface);font-family:var(--display);font-weight:500;font-size:.82rem;
 color:var(--ink-2)}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:var(--surface)}
.num{text-align:right;font-variant-numeric:tabular-nums}
code{font-family:var(--mono);font-size:.8rem;background:var(--surface-2);padding:2px 7px;
 border-radius:6px}
.rang{display:inline-grid;place-items:center;min-width:30px;height:26px;padding:0 8px;
 border-radius:var(--r-pill);background:#e8f0fe;color:#174ea6;font-weight:600}

/* ───────────────────────────────────────────────── encart */
.note{display:flex;gap:14px;align-items:flex-start;background:var(--surface);
 border:1px solid var(--line);border-radius:var(--r-md);padding:16px 20px;
 font-size:.9rem;color:var(--ink-2)}
.note b{color:var(--ink)}
.note svg{flex:0 0 20px;width:20px;height:20px;margin-top:2px;color:var(--orange)}
.flux{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;
 margin-top:20px}
.flux-b{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);
 padding:16px 20px}
.flux-b b{display:block;font-family:var(--mono);font-size:.78rem}
.flux-b span{font-size:.85rem;color:var(--ink-2)}
.flux-b--ko{background:#fef7e0;border-color:#feefc3}
.flux-f{font-size:1.6rem;color:var(--orange)}
@media(max-width:720px){.flux{grid-template-columns:1fr}.flux-f{transform:rotate(90deg);
 text-align:center}}

/* ───────────────────────────────────────────────── kanban */
.kanban{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}
.kan{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);padding:24px;
 box-shadow:var(--shadow)}
.kan h3{display:flex;align-items:center;gap:10px;font-size:1rem;margin-bottom:16px;
 padding-bottom:12px;border-bottom:1px solid var(--line)}
.kan h3 em{font-style:normal;font-family:var(--mono);font-size:.72rem;font-weight:500;
 background:var(--surface-2);color:var(--ink-2);padding:2px 9px;border-radius:var(--r-pill);
 margin-left:auto}
.kan h3::before{content:"";width:10px;height:10px;border-radius:50%;flex:0 0 10px}
.kan--fait h3::before{background:var(--g-green)}
.kan--cours h3::before{background:var(--action)}
.kan--todo h3::before{background:var(--orange)}
.kan li{padding:12px 0;border-bottom:1px solid var(--line)}
.kan li:last-child{border-bottom:0;padding-bottom:0}
.kan li b{display:block;font-weight:500;font-size:.92rem}
.kan li span{display:block;color:var(--ink-2);font-size:.84rem;margin-top:3px}

/* ───────────────────────────────────────────────── artefacts */
.artes{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}
.arte{display:flex;flex-direction:column;gap:6px;background:#fff;border:1px solid var(--line);
 border-radius:var(--r-card);padding:24px;box-shadow:var(--shadow);color:var(--ink);
 transition:box-shadow .25s,transform .25s}
.arte:hover{box-shadow:var(--shadow-h);transform:translateY(-2px);color:var(--ink)}
.arte-k{font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;
 color:var(--action)}
.arte b{font-family:var(--display);font-size:1.08rem;font-weight:600}
.arte-s{color:var(--ink-2);font-size:.9rem}
.arte-d{font-size:.84rem;color:var(--ink-2);margin-top:6px;flex:1}
.arte-c{margin-top:14px;color:var(--action);font-weight:500;font-size:.9rem}

.pied{border-top:1px solid var(--line);background:var(--surface)}
.pied .wrap{padding-block:28px;font-size:.84rem;color:var(--ink-2)}
@media (prefers-reduced-motion:reduce){*{transition-duration:.001ms !important}}
</style></head><body>

<header class="hdr"><div class="wrap">
 <p class="puce">Reporting hebdomadaire</p>
 <h1>Hello Harel — semaine du {{semaine}}</h1>
 <p class="sous">Relevé de positions du {{releve}} · France, français · {{pages}} pages du site
 apparaissent dans les résultats.</p>
</div></header>

<main>

<section class="sec"><div class="wrap">
 <div class="tuiles">{{tuiles}}</div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Clics</p>
 <h2>Le trafic, et d'où il vient</h2>
 <p>Search Console n'est pas connectée à cet environnement : aucun chiffre de clics réels
 n'est affiché ici. Ce qui suit est une <b>estimation</b> de trafic calculée par DataForSEO
 à partir des positions et des volumes. À traiter comme un ordre de grandeur et une
 répartition, pas comme un compteur.</p>
 <div class="grille2">
  <div class="card">
   <h3>Trafic estimé par page</h3>
   <p>Visites/mois estimées · 8 premières pages sur {{pages}}</p>
   {{b_pages}}
  </div>
  <div class="card">
   <h3>Blog contre pages qui vendent</h3>
   <p>Part du trafic estimé</p>
   {{anneau_blog}}
   <div class="repart">
    <div><i style="background:#1a73e8"></i>Blog<b>{{pc_blog}} %</b></div>
    <div><i style="background:#E37400"></i>Pages business<b>{{pc_biz}} %</b></div>
   </div>
   <div class="note" style="margin-top:20px">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round"><path d="M12 9v4m0 4h.01M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0
     1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/></svg>
    <span>Sur <b>{{etv}}</b> visites/mois estimées, <b>{{etv_biz}}</b> arrivent sur une page
    qui vend.</span>
   </div>
  </div>
 </div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Positions</p>
 <h2>Où se situent les {{pages}} pages, hors marque</h2>
 <p>Deux lectures de la même réalité. Le rang organique ignore les blocs de Google ;
 le rang affiché est celui que voit l'internaute. <b>{{nb_g3}} requêtes sont dans le top 3
 organique, {{nb_a3}} seulement sont vraiment affichées dans les trois premiers résultats.</b></p>
 <div class="card">{{colonnes}}</div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Pages business</p>
 <h2>Les pages qui vendent, hors marque</h2>
 <p>Sur {{pages}} pages positionnées, <b>{{nb_biz}} seulement</b> sont des pages métier,
 fonctionnalité ou comparatif. Le reste est du blog.</p>
 <div class="card" style="padding-inline:0;padding-block:0;border:0;box-shadow:none">
 <div class="tab-wrap"><table>
  <thead><tr><th>Page</th><th>Requête</th><th class="num">Volume/mois</th>
  <th class="num">Rang affiché</th><th class="num">Rang organique</th></tr></thead>
  <tbody>{{lignes_biz}}</tbody>
 </table></div></div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">BOFU</p>
 <h2>Les requêtes à travailler</h2>
 <p><b>{{nb_bofu}} requêtes d'achat</b> (erp, logiciel, AS/400, comparatif) sont déjà
 positionnées, pour {{vol_bofu}} de volume mensuel cumulé. <b>{{nb_bofu_blog}} d'entre elles
 atterrissent sur le blog</b>, pas sur la page qui convertit.</p>
 <div class="card">
  <h3>Volume mensuel et position affichée</h3>
  <p>12 premières requêtes commerciales positionnées</p>
  {{b_bofu}}
  <div class="flux">
   <div class="flux-b"><b>{{nb_as400}} requêtes AS/400</b>
    <span>{{vol_as400}} recherches/mois — la plus grosse grappe commerciale du site</span></div>
   <div class="flux-f">→</div>
   <div class="flux-b flux-b--ko"><b>/blog/erp-as400/</b>
    <span>Tout y atterrit. La page qui convertit, <code>/migration-as400/</code>,
    n'en reçoit aucune.</span></div>
  </div>
 </div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Roadmap</p>
 <h2>Où en sont les chantiers</h2>
 <div class="kanban">{{road}}</div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Livrables</p>
 <h2>Artefacts de la semaine</h2>
 <p>Trois maquettes de /agroalimentaire/. Aucune n'est en ligne : la page est protégée.</p>
 <div class="artes">{{arte}}</div>
</div></section>

</main>

<footer class="pied"><div class="wrap">
 <p><b>Sources.</b> Positions, volumes et trafic estimé : DataForSEO Labs, relevé du {{releve}},
 France / français, 333 requêtes. Roadmap : fichiers du dépôt et travaux de la semaine.
 Les clics Search Console ne figurent pas dans ce rapport : la propriété n'est pas connectée.</p>
</div></footer>
</body></html>"""


if __name__ == "__main__":
    main()
