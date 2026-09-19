#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reporting Google Ads — compte HELLO HAREL (8044187703), 30 derniers jours.

Source : API Google Ads via Composio, requêtes GAQL du 18/09/2026.

UNE écriture a été faite, sur accord explicite du 18/09 : les 38 exclusions
sans risque, posées au niveau de la campagne 24061100837. Elles ont d'abord
été validées en validate_only, puis appliquées, puis relues sur le compte :
54 exclusions au total, 16 d'avant plus les 38 nouvelles, toutes ENABLED.
Rien d'autre n'a été touché.

Rappel de cadrage : « Google Ads est hors périmètre » est une règle du dossier.
Elle est levée par la demande du 18/09, et ce document en est la trace.

DA Google Store (client.json : "da": "google-store").

Usage :  python3 reporting_ads.py
"""

import json
import os
import re

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SORTIE = os.path.join(S, "reporting-ads.html")

BLEU, ORANGE = "#1a73e8", "#E37400"
VERT, ROUGE = "#188038", "#c5221f"


def nb(v):
    return "{:,}".format(int(round(v))).replace(",", " ")


def eur(v):
    return ("%.2f" % v).replace(".", ",") + " €"


def virg(v, d=1):
    return (("%." + str(d) + "f") % v).replace(".", ",")


# ═══════════════════════════════════════════════════════ briques
def tuile(valeur, libelle, detail, ton=""):
    return ('<div class="tuile%s"><p class="tuile-v">%s</p><p class="tuile-l">%s</p>'
            '<p class="tuile-d">%s</p></div>'
            % ((" tuile--" + ton) if ton else "", valeur, libelle, detail))


def colonnes(jours):
    """Coût par jour, conversions marquées. Une seule échelle, un seul axe."""
    maxi = max(j["eur"] for j in jours)
    c = ""
    for j in jours:
        h = 100.0 * j["eur"] / maxi
        c += ('<div class="jc" tabindex="0" title="%s — %s dépensés, %d clics, '
              '%s conversion(s)">'
              '<span class="jc-b" style="height:%.1f%%"></span>'
              '%s<span class="jc-l">%s</span></div>'
              % (j["date"], eur(j["eur"]), j["clics"], virg(j["conv"], 0), h,
                 ('<span class="jc-c">%d</span>' % j["conv"]) if j["conv"] else "",
                 j["date"][8:10]))
    return '<div class="jours">%s</div>' % c


def barres(lignes, maxi=None, couleur=BLEU, lib="260px"):
    maxi = maxi or max(v for _, v, _ in lignes)
    out = ['<div class="barres" style="--lib:%s">' % lib]
    for label, v, note in lignes:
        out.append('<div class="barre" tabindex="0" title="%s — %s%s">'
                   '<span class="barre-l">%s</span>'
                   '<span class="barre-p"><i style="width:%.1f%%;background:%s"></i></span>'
                   '<span class="barre-v">%s</span></div>'
                   % (label, eur(v), (" · " + note) if note else "", label,
                      max(1.2, 100.0 * v / maxi), couleur, eur(v)))
    out.append("</div>")
    return "".join(out)


def anneau(part, total, couleur):
    pc = 100.0 * part / total
    c = 2 * 3.14159 * 54
    return ('<svg viewBox="0 0 128 128" class="anneau" role="img" '
            'aria-label="%s %% du coût">'
            '<circle cx="64" cy="64" r="54" fill="none" stroke="#e8eaed" stroke-width="16"/>'
            '<circle cx="64" cy="64" r="54" fill="none" stroke="%s" stroke-width="16" '
            'stroke-linecap="round" stroke-dasharray="%.1f %.1f" '
            'transform="rotate(-90 64 64)"/>'
            '<text x="64" y="70" text-anchor="middle" class="anneau-t">%d %%</text></svg>'
            % (virg(pc, 0), couleur, c * pc / 100, c, round(pc)))


def main():
    d = json.load(open(os.path.join(S, "ads.json"), encoding="utf-8"))
    c = d["campagne"]
    t = d["termes"]

    tuiles = "".join([
        tuile(eur(c["eur"]), "dépensés sur 30 jours",
              "budget %s/jour · %s clics" % (eur(c["budget_jour"]), nb(c["clics"]))),
        tuile(nb(c["conv"]), "conversions",
              "soit %s par conversion" % eur(c["eur"] / c["conv"])),
        tuile(eur(t["perte_eur"]), "sur des requêtes à 0 conversion",
              "%d termes · %d %% du coût analysé"
              % (t["perte_n"], round(100 * t["perte_eur"] / t["eur"])), ton="ko"),
        tuile(eur(d["proposes_eco"]), "récupérables sans risque",
              "%d exclusions, aucune ne touche une conversion" % d["proposes_n"], ton="ok"),
    ])

    b_neg = barres([(m, e, "%d terme%s" % (n, "s" if n > 1 else ""))
                    for m, n, e in d["proposes"] if e >= 0.5], couleur=ORANGE, lib="270px")
    b_arb = "".join(
        '<li><span class="q">%s</span><span class="q-p">%s</span>'
        '<span class="q-i">%d termes</span>'
        '<span class="q-d down">%s conversion%s en jeu</span></li>'
        % (m, eur(e), n, virg(cv, 0), "s" if cv > 1 else "")
        for m, n, e, cv in d["arbitrer"])

    valeurs = dict(
        tuiles=tuiles, jours=colonnes(d["jours"]),
        campagne=c["nom"], budget=eur(c["budget_jour"]),
        imp=nb(c["imp"]), clics=nb(c["clics"]), cpc=eur(c["cpc"]),
        cout=eur(c["eur"]), conv=nb(c["conv"]), cpa=eur(c["eur"] / c["conv"]),
        groupes=len(d["groupes"]),
        liste_groupes=" · ".join(d["groupes"]),
        t_n=nb(t["n"]), t_eur=eur(t["eur"]), t_perte=eur(t["perte_eur"]),
        t_perte_n=t["perte_n"], t_pc=round(100 * t["perte_eur"] / t["eur"]),
        anneau=anneau(t["perte_eur"], t["eur"], ORANGE),
        neg_camp=d["negatifs"]["campagne"], neg_grp=d["negatifs"]["groupe"],
        neg_listes=d["negatifs"]["listes_partagees"],
        b_neg=b_neg, prop_n=d["proposes_n"], prop_eco=eur(d["proposes_eco"]),
        prop_termes=d["proposes_termes"], b_arb=b_arb,
        sitelinks=d["assets"]["sitelinks"], callouts=d["assets"]["callouts"],
    )

    html = GABARIT
    for k, v in valeurs.items():
        html = html.replace("{{%s}}" % k, str(v))
    reste = re.findall(r"\{\{(\w+)\}\}", html)
    if reste:
        raise SystemExit("ARRÊT — jeton non remplacé : %s" % sorted(set(reste)))

    open(SORTIE, "w", encoding="utf-8").write(html)
    print("écrit : %s (%d ko)" % (SORTIE, len(html) // 1024))
    pb = []
    for x in ("section", "div", "svg", "ul", "li"):
        o, f = len(re.findall(r"<%s[\s>]" % x, html)), len(re.findall(r"</%s>" % x, html))
        if o != f:
            pb.append("%s : %d/%d" % (x, o, f))
    if html.count("<h1") != 1:
        pb.append("il faut un seul H1")
    print("contrôles : %s" % ("tout est vert" if not pb else pb))


GABARIT = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Google Ads Hello Harel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{color-scheme:light;
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
 --mono:'Roboto Mono',ui-monospace,SFMono-Regular,Menlo,monospace}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);
 font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:var(--display);letter-spacing:-.01em;margin:0;font-weight:600}
p,ul,figure{margin:0}ul{list-style:none;padding:0}
a{color:var(--action);text-decoration:none}a:hover{color:var(--action-hover)}
:focus-visible{outline:3px solid var(--focus);outline-offset:2px;border-radius:8px}
.wrap{max-width:var(--max);margin-inline:auto;padding-inline:24px}
.sec{padding-block:clamp(32px,5vw,56px)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;
 color:var(--ink-2);margin-bottom:8px}
.sec>.wrap>h2{font-size:clamp(1.35rem,2.6vw,1.9rem);margin-bottom:8px}
.sec>.wrap>h2+p{color:var(--ink-2);margin-bottom:24px;max-width:76ch}
.sec>.wrap>h2+p b{color:var(--ink);font-weight:500}
code{font-family:var(--mono);font-size:.84rem;background:var(--surface-2);padding:2px 7px;
 border-radius:6px}

.hdr{background:linear-gradient(180deg,#f8f9fa,#fff);border-bottom:1px solid var(--line)}
.hdr .wrap{padding-block:40px 32px}
.hdr h1{font-size:clamp(1.7rem,4vw,2.5rem);font-weight:700}
.hdr .sous{color:var(--ink-2);margin-top:8px;max-width:80ch}
.puce{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:.72rem;
 letter-spacing:.1em;text-transform:uppercase;color:#174ea6;background:#e8f0fe;
 padding:6px 14px;border-radius:var(--r-pill);margin-bottom:16px}

.tuiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));gap:16px}
.tuile{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);padding:24px;
 box-shadow:var(--shadow);transition:box-shadow .25s,transform .25s}
.tuile:hover{box-shadow:var(--shadow-h);transform:translateY(-2px)}
.tuile--ok{background:#e6f4ea;border-color:#ceead6}
.tuile--ko{background:#fef7e0;border-color:#feefc3}
.tuile-v{font-family:var(--display);font-size:clamp(1.7rem,3.6vw,2.4rem);font-weight:700;
 line-height:1.08;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.tuile--ok .tuile-v{color:var(--vert)}.tuile--ko .tuile-v{color:#976700}
.tuile-l{font-weight:500;margin-top:4px}
.tuile-d{color:var(--ink-2);font-size:.84rem;margin-top:6px}

.card{background:#fff;border:1px solid var(--line);border-radius:var(--r-card);
 padding:clamp(20px,3vw,32px);box-shadow:var(--shadow)}
.card+.card{margin-top:16px}
.card h3{font-size:1.05rem;margin-bottom:4px}
.card h3+p{color:var(--ink-2);font-size:.88rem;margin-bottom:20px}
.grille2{display:grid;grid-template-columns:1fr;gap:16px}
@media(min-width:900px){.grille2{grid-template-columns:1.3fr .7fr}}

.jours{display:flex;align-items:flex-end;gap:3px;height:190px}
.jc{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;
 height:100%;gap:4px;border-radius:6px 6px 0 0;position:relative}
.jc:hover,.jc:focus-visible{background:var(--surface)}
.jc-b{width:100%;max-width:26px;background:#1a73e8;border-radius:4px 4px 0 0;min-height:3px}
.jc-c{position:absolute;top:0;font-family:var(--mono);font-size:.62rem;font-weight:600;
 color:#fff;background:var(--vert);border-radius:var(--r-pill);padding:1px 6px}
.jc-l{font-family:var(--mono);font-size:.6rem;color:var(--ink-2)}
@media(max-width:700px){.jc-l{display:none}}
.leg{display:flex;flex-wrap:wrap;gap:20px;font-size:.82rem;color:var(--ink-2);margin-top:16px;
 padding-top:16px;border-top:1px solid var(--line)}
.leg i{display:inline-block;width:12px;height:12px;border-radius:4px;margin-right:7px;
 vertical-align:-1px}

.barres{display:grid;gap:9px}
.barre{display:grid;grid-template-columns:var(--lib) 1fr auto;align-items:center;gap:12px;
 font-size:.86rem;border-radius:8px;padding:2px 4px}
.barre:hover,.barre:focus-visible{background:var(--surface)}
.barre-l{font-family:var(--mono);font-size:.78rem;overflow:hidden;text-overflow:ellipsis;
 white-space:nowrap}
.barre-p{background:var(--surface-2);border-radius:var(--r-pill);height:13px;position:relative}
.barre-p i{position:absolute;inset:0 auto 0 0;border-radius:var(--r-pill);display:block}
.barre-v{font-variant-numeric:tabular-nums;font-weight:500;min-width:74px;text-align:right}
@media(max-width:720px){.barre{grid-template-columns:1fr auto;
 grid-template-areas:"l v" "p p"}.barre-l{grid-area:l}.barre-v{grid-area:v}.barre-p{grid-area:p}}

.anneau{width:clamp(126px,20vw,160px);height:auto;display:block;margin:0 auto 14px}
.anneau-t{font-family:var(--display);font-size:26px;font-weight:700;fill:var(--ink)}

.qs li{display:grid;grid-template-columns:1fr auto;gap:2px 14px;padding:13px 0;
 border-bottom:1px solid var(--line)}
.qs li:last-child{border-bottom:0;padding-bottom:0}
.q{font-family:var(--mono);font-size:.86rem;font-weight:500}
.q-p{font-family:var(--mono);font-size:.84rem;text-align:right;font-variant-numeric:tabular-nums;
 font-weight:600}
.q-i{font-size:.76rem;color:var(--ink-2)}
.q-d{font-size:.78rem;text-align:right}
.q-d.down{color:#976700}

.fiche{display:grid;gap:14px}
.fiche-l{display:grid;grid-template-columns:28px 1fr;gap:14px;align-items:start;
 padding:16px 0;border-bottom:1px solid var(--line)}
.fiche-l:last-child{border-bottom:0}
.fiche-l i{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;
 font-family:var(--mono);font-size:.78rem;font-weight:700;font-style:normal;color:#fff}
.fiche-l.ko i{background:var(--rouge)}.fiche-l.ok i{background:var(--vert)}
.fiche-l.att i{background:var(--orange)}
.fiche-l>div>b{display:block;font-family:var(--display);font-size:1rem;font-weight:600;margin-bottom:2px}
.fiche-l p b{font-weight:600;color:var(--ink)}
.fiche-l p{color:var(--ink-2);font-size:.9rem;margin-top:4px}
.fiche-l p+p{margin-top:8px}
.verdict{display:inline-block;font-family:var(--mono);font-size:.68rem;letter-spacing:.08em;
 text-transform:uppercase;padding:3px 10px;border-radius:var(--r-pill);margin-top:8px;
 font-weight:500}
.v-ko{background:#fce8e6;color:#a50e0e}.v-ok{background:#e6f4ea;color:#0d652d}
.v-att{background:#fef7e0;color:#976700}

.note{display:flex;gap:14px;align-items:flex-start;background:#e8f0fe;border:1px solid #d2e3fc;
 border-radius:var(--r-md);padding:18px 22px;font-size:.92rem}
.note svg{flex:0 0 20px;width:20px;height:20px;margin-top:2px;color:var(--action)}
.pied{border-top:1px solid var(--line);background:var(--surface)}
.pied .wrap{padding-block:28px;font-size:.84rem;color:var(--ink-2)}
@media (prefers-reduced-motion:reduce){*{transition-duration:.001ms !important}}
</style></head><body>

<header class="hdr"><div class="wrap">
 <p class="puce">Google Ads · compte 804-418-7703</p>
 <h1>HELLO HAREL — 30 derniers jours</h1>
 <p class="sous">Une campagne active, <b>{{campagne}}</b>, {{groupes}} groupes d'annonces,
 budget {{budget}}/jour. Relevé du 18 septembre 2026 par l'API Google Ads.
 <b>Les 38 exclusions ont été posées</b> après ton accord ; rien d'autre n'a été
 touché.</p>
</div></header>

<main>

<section class="sec"><div class="wrap"><div class="tuiles">{{tuiles}}</div></div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Dépense</p>
 <h2>Jour par jour</h2>
 <p>{{imp}} impressions, {{clics}} clics à {{cpc}} en moyenne, {{cout}} dépensés,
 <b>{{conv}} conversions</b> — soit <b>{{cpa}} par conversion</b>. Le budget plafonne à
 {{budget}} : les journées à 60 € sont des jours où Google a doublé la mise, ce qu'il
 s'autorise sur une moyenne mensuelle.</p>
 <div class="card">
  {{jours}}
  <div class="leg"><span><i style="background:#1a73e8"></i>Coût du jour</span>
  <span><i style="background:#188038"></i>Conversions du jour</span></div>
 </div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Requêtes</p>
 <h2>Où part l'argent</h2>
 <p>Sur les {{t_n}} termes de recherche relevés ({{t_eur}} de coût attribué),
 <b>{{t_perte_n}} termes n'ont produit aucune conversion</b> et coûtent {{t_perte}}.
 Le motif dominant : des requêtes en anglais ou en allemand, et des requêtes
 génériques sans rapport avec l'agroalimentaire.</p>
 <div class="grille2">
  <div class="card">
   <h3>Ce que coûtent les exclusions proposées</h3>
   <p>Mesuré sur 30 jours · seules les lignes ≥ 0,50 € sont affichées</p>
   {{b_neg}}
  </div>
  <div class="card">
   <h3>Part du coût sans conversion</h3>
   <p>Sur les termes relevés</p>
   {{anneau}}
   <div class="note" style="margin-top:8px">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round"><path d="M12 16v-4m0-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
    <span>Le compte n'a <b>aucune liste d'exclusion partagée</b> : {{neg_camp}} exclusions au
    niveau de la campagne et {{neg_grp}} au niveau des groupes, rien de mutualisé.</span>
   </div>
  </div>
 </div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">À arbitrer</p>
 <h2>Les cinq exclusions que je ne pose pas sans ton accord</h2>
 <p>Elles coupent le plus de dépense, mais elles touchent aussi des conversions.
 Les poser en bloc ferait perdre <b>8 des 12 conversions</b> du relevé de termes.</p>
 <div class="card"><ul class="qs">{{b_arb}}</ul></div>
</div></section>

<section class="sec"><div class="wrap">
 <p class="eyebrow">Tes quatre demandes</p>
 <h2>Ce qui est faisable, et ce qui ne l'est pas</h2>
 <div class="card"><div class="fiche">

  <div class="fiche-l ko"><i>1</i><div>
   <b>Favicon sur les annonces</b>
   <p>Ce n'est pas un réglage : Google affiche le favicon automatiquement, à deux
   conditions — que l'identité de l'annonceur soit <b>vérifiée</b> dans le compte, et qu'il
   trouve une icône sur le domaine. L'API n'expose aucun champ pour l'activer.</p>
   <p>Le site déclare bien ses icônes (<code>hello-harel-favicon-512x512</code>, 32 px et
   192 px), mais <code>/favicon.ico</code> répond en redirection 302 au lieu de servir un
   fichier. Deux actions, aucune dans Ads : servir un vrai <code>/favicon.ico</code> à la
   racine, et vérifier l'annonceur dans le compte.</p>
   <span class="verdict v-ko">Pas faisable par l'API</span>
  </div></div>

  <div class="fiche-l ko"><i>2</i><div>
   <b>Étoiles des avis Google sur les annonces</b>
   <p>Ce sont les <b>évaluations du vendeur</b>. Elles ne s'activent pas non plus : Google
   les affiche quand le domaine réunit <b>au moins 100 avis sur douze mois</b> auprès d'une
   source agréée, et une note d'au moins 3,5.</p>
   <p>Hello Harel affiche <b>31 avis Google</b> — et les avis de la fiche Google Business ne
   comptent pas comme source agréée pour cette extension. Le chemin réaliste passe par
   Google Customer Reviews ou un tiers agréé, et par le franchissement du seuil de 100.</p>
   <span class="verdict v-ko">Seuil non atteint — 31 avis sur 100</span>
  </div></div>

  <div class="fiche-l ok"><i>3</i><div>
   <b>Liste d'exclusion de mots-clés</b>
   <p>Il n'y a <b>rien à mettre à jour</b> : aucune liste partagée n'existe sur le compte.
   J'ai construit la liste à partir des {{t_n}} termes réellement déclenchés.</p>
   <p><b>{{prop_n}} exclusions sans risque</b>, qui ne touchent aucun terme ayant converti :
   {{prop_termes}} termes couverts, <b>{{prop_eco}} de dépense évitée sur 30 jours</b>.</p>
   <p>Validées en <code>validate_only</code>, puis <b>appliquées le 18/09 sur ton accord</b>,
   puis relues sur le compte : la campagne porte désormais <b>54 exclusions</b> — les 16
   d'avant plus les 38 nouvelles, toutes actives.</p>
   <span class="verdict v-ok">Posé le 18/09 · 54 exclusions actives</span>
  </div></div>

  <div class="fiche-l ok"><i>4</i><div>
   <b>Reporting</b>
   <p>C'est ce document, mis à jour après la pose des exclusions. En bonus, deux constats
   qui ne venaient pas de ta liste :
   la campagne ne diffuse que <b>{{sitelinks}} liens annexes</b> et {{callouts}} accroches,
   là où Google en demande quatre minimum pour un affichage complet — et il n'y a
   <b>ni extrait structuré, ni logo, ni extension d'appel</b>.</p>
   <p>Chaque groupe d'annonces ne porte qu'<b>une seule annonce responsive</b>. Sans
   deuxième annonce, Google n'a rien à comparer.</p>
   <span class="verdict v-ok">Livré</span>
  </div></div>

 </div></div>
</div></section>

</main>

<footer class="pied"><div class="wrap">
 <p><b>Source.</b> API Google Ads via Composio, compte HELLO HAREL (804-418-7703), requêtes
 GAQL du 18/09/2026, fenêtre LAST_30_DAYS. Les conversions sont celles déclarées dans le
 compte ; leur qualité n'est pas vérifiable depuis l'API — et les formulaires du site
 n'envoient plus de mail depuis le 10/08, ce qui doit être gardé en tête avant de raisonner
 sur le coût par conversion. Une seule modification a été apportée au compte, sur accord
 explicite : les 38 exclusions du point 3, relues après application. Ni budget, ni
 enchère, ni annonce, ni extension n'ont été touchés.</p>
</div></footer>
</body></html>"""


if __name__ == "__main__":
    main()
