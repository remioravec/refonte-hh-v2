#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roadmap contenu — semaine du 12/10/2026.

Trois lignes etaient au programme :

  1. « logiciel import export agroalimentaire »        -> /fonctionnalites/import-export/        (mise a jour)
  2. « logiciel de gestion commerciale import export » -> page a creer                           (creation)
  3. « logiciel devis commande bon de livraison »      -> /fonctionnalites/logiciel-devis-...-/  (mise a jour)

La ligne 2 ne donne pas lieu a une creation. Mesure Search Console sur
90 jours : la requete est deja captee par DEUX pages du site —
/blog/meilleurs-erp-import-export/ en position 9,7 avec 134 impressions, et
/fonctionnalites/import-export/ en position 34,3 avec 21 impressions. Creer
une troisieme page partagerait la meme requete entre trois URL. Le verdict
d'anti-cannibalisation est FORT : on renforce la page qui capte deja, on n'en
cree pas une seconde. La ligne est donc servie par une mise a jour de
/blog/meilleurs-erp-import-export/ — balisage a l'exact match et quatre liens
entrants contextuels, la ou la page n'en recevait que trois.

Ce que le script pose :

  4813  /fonctionnalites/import-export/
        badge, H1 a l'exact match, accroche, signature datee,
        reponse encadree + fait date source, calculateur de frais d'approche,
        deux questions de FAQ, FAQPage JSON-LD, bloc sources officielles,
        liens sortants contextuels, title et description.

  7911  /fonctionnalites/logiciel-devis-commande-bon-livraison/
        H1 a l'exact match naturel (il disait « devis-commande-BL »),
        module « du devis au bon de livraison, a poids variable »,
        fait date source.

  5640  /blog/meilleurs-erp-import-export/
        title et description portant « logiciel de gestion commerciale import
        export », plus les liens entrants poses depuis quatre pages, a ancres
        tournantes.

GARDE-FOUS
  - sauvegarde du contenu avant ecriture ;
  - refus si _elementor_data n'est pas vide ;
  - refus si un « & » nu entre dans un <script> (WordPress le transforme en
    &#038; et casse le JSON comme le JavaScript) ;
  - refus si le contenu depasse le plafond de rendu ;
  - verification du nombre de H1 et de l'unicite des points d'insertion.

Usage :  python3 maj_import_export.py            (blanc, aucune ecriture)
         python3 maj_import_export.py --ecrire
"""

import html
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import ns_api as n                                       # noqa: E402

PLAFOND = 275_000
SAUVE = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
         "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-sem41")

# --------------------------------------------------------------------------
# Largeur en pixels — meme approximation que le tableau de balisage
# --------------------------------------------------------------------------
LARGE = set("mwMW—…")
MOYEN = set("ABCDEFGHJKLNOPQRSTUVXYZabcdeghknopqsuvxyz0123456789")


def px(t):
    return round(sum(11.0 if c in LARGE else (8.0 if c in MOYEN else 5.5)
                     for c in t))


# --------------------------------------------------------------------------
# Lecture equilibree des blocs imbriques
# --------------------------------------------------------------------------

def bornes_section(c, classe):
    m = re.search(r'<section[^>]*class="[^"]*' + re.escape(classe)
                  + r'[^"]*"[^>]*>', c)
    if not m:
        return None
    i, p = m.start(), 0
    for t in re.finditer(r"<section\b|</section>", c[i:]):
        p += 1 if t.group(0) != "</section>" else -1
        if p == 0:
            return (i, i + t.end())
    return None


def details(bloc):
    out = []
    for m in re.finditer(r"<details\b[^>]*>", bloc):
        i, p, d = m.start(), 0, None
        for t in re.finditer(r"<details\b|</details>", bloc[i:]):
            p += 1 if t.group(0) != "</details>" else -1
            if p == 0:
                d = bloc[i:i + t.end()]
                break
        if d is None:
            continue
        q = re.search(r"(?is)<summary[^>]*>(.*?)</summary>", d)
        if not q:
            continue
        out.append((html.unescape(re.sub(r"<[^>]+>", "", q.group(1))).strip(),
                    re.sub(r"(?is)</details>\s*$", "", d[q.end():])))
    return out


def texte(h):
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", h)
    t = re.sub(r"(?is)</(p|li|h[1-6]|div)>", " ", t)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t))).strip()


def resume(h, maxi=320):
    t = re.sub(r"\s+", " ", texte(h).replace("&", " et ")).strip()
    if len(t) > maxi:
        coupe = t[:maxi]
        for sep in (". ", " : ", "; "):
            j = coupe.rfind(sep)
            if j > 140:
                t = coupe[:j + 1].strip()
                break
        else:
            t = coupe.rsplit(" ", 1)[0].rstrip(",;") + "."
    if t and t[-1] not in ".!?…":
        t += "."
    return t


def reparer_amp_nus(c, notes):
    """Neutralise les « & » nus que WordPress transformerait en &#038;.

    Deux cas rencontrés, tous deux antérieurs à ce script :
      - un <script> de l'outil ROI retiré en septembre, resté orphelin : il
        sort immédiatement (« if (!i1) return; ») puisque son premier élément
        n'existe plus dans la page. On le retire ;
      - un « & » littéral dans un bloc ld+json (« Fondateur & CEO ») : on
        l'écrit \\u0026, l'échappement JSON, qui survit à l'enregistrement.
    """
    morceaux, fin = [], 0
    for m in re.finditer(r"(?is)<script\b([^>]*)>(.*?)</script>", c):
        attrs, corps = m.group(1), m.group(2)
        nus = [a.start() for a in re.finditer(r"&", corps)
               if not re.match(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);",
                               corps[a.start():a.start() + 10])]
        if not nus:
            continue
        if 'getElementById("roiI1")' in corps and 'id="roiI1"' not in c:
            morceaux.append((m.start(), m.end(), ""))
            notes.append("script ROI orphelin retiré (%d o)" % len(m.group(0)))
            fin += 1
            continue
        if "ld+json" in attrs:
            neuf = corps
            for i in sorted(nus, reverse=True):
                neuf = neuf[:i] + "\\u0026" + neuf[i + 1:]
            json.loads(neuf)          # le bloc doit rester du JSON valide
            morceaux.append((m.start(), m.end(),
                             "<script" + attrs + ">" + neuf + "</script>"))
            notes.append("%d « & » échappés en \\u0026 dans un ld+json" % len(nus))
            fin += 1
            continue
        raise RuntimeError("« & » nu dans un <script> non reconnu : %r"
                           % corps[max(0, nus[0] - 60):nus[0] + 60])
    for a, b, neuf in sorted(morceaux, reverse=True):
        c = c[:a] + neuf + c[b:]
    return c


def sans_amp_nu_dans_scripts(c):
    for m in re.finditer(r"(?is)<script\b[^>]*>(.*?)</script>", c):
        corps = m.group(1)
        for a in re.finditer(r"&", corps):
            if not re.match(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);",
                            corps[a.start():a.start() + 10]):
                return False
    return True


# --------------------------------------------------------------------------
# Signature — identique a celle posee sur les pages soeurs
# --------------------------------------------------------------------------
BYLINE_CSS = """<style id="hh-byline-css">
.eeat-byline{display:flex;flex-wrap:wrap;align-items:center;gap:1.25rem;margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
#hh-page .eeat-byline{display:flex;flex-wrap:wrap;align-items:center;gap:1.25rem;margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
.eeat-byline img,#hh-page .eeat-byline img{width:48px;height:48px;border-radius:50%;border:2px solid #16DB7F;object-fit:cover}
.eeat-byline-author,#hh-page .eeat-byline-author{color:#fff;font-size:.9375rem}
.eeat-byline-author strong,#hh-page .eeat-byline-author strong{color:#16DB7F;display:block;font-size:1rem;margin-bottom:.15rem}
.eeat-byline-meta,#hh-page .eeat-byline-meta{color:rgba(255,255,255,.85);font-size:.8125rem;display:flex;flex-wrap:wrap;gap:.75rem;margin-top:.25rem}
.eeat-byline-meta span,#hh-page .eeat-byline-meta span{display:inline-flex;align-items:center;gap:.35rem}
</style>
"""

BYLINE = """<div class="eeat-byline">
<img loading="lazy" src="https://ui-avatars.com/api/?name=Timothy+Jollivet&amp;background=16DB7F&amp;color=fff&amp;size=96" alt="Timothy Jollivet, fondateur de Hello Harel">
<div class="eeat-byline-author"><strong>Timothy Jollivet</strong>Fondateur de Hello Harel, éditeur d'ERP agroalimentaire
<div class="eeat-byline-meta"><span>Publié le 1er avril 2026</span><span>Mis à jour le 6 octobre 2026</span><span>{LECTURE} min de lecture</span></div>
</div></div>"""


# --------------------------------------------------------------------------
# Feuille de style des deux modules — chaque regle doublee en #hh-page,
# le theme prefixant ses propres regles de cet identifiant.
# --------------------------------------------------------------------------
MODULES_CSS = """<style id="hh-modules-sem41-css">
.hhm-wrap,#hh-page .hhm-wrap{background:#0b1b2b;padding:3.5rem 0}
.hhm-wrap .container,#hh-page .hhm-wrap .container{max-width:1180px;margin:0 auto;padding:0 1rem}
.hhm-rep,#hh-page .hhm-rep{background:rgba(22,219,127,.08);border:1px solid rgba(22,219,127,.35);border-left:4px solid #16DB7F;border-radius:14px;padding:1.5rem 1.5rem;margin:0 0 2rem}
.hhm-rep p,#hh-page .hhm-rep p{color:#e8f2ff;font-size:1.0625rem;line-height:1.65;margin:0 0 .85rem}
.hhm-rep p:last-child,#hh-page .hhm-rep p:last-child{margin-bottom:0}
.hhm-rep b,#hh-page .hhm-rep b{color:#16DB7F}
.hhm-rep a,#hh-page .hhm-rep a{color:#8fd8ff;text-decoration:underline}
.hhm-h,#hh-page .hhm-h{margin:0 0 1.75rem;text-align:center}
.hhm-h p.hhm-over,#hh-page .hhm-h p.hhm-over{color:#16DB7F;text-transform:uppercase;letter-spacing:.08em;font-size:.8125rem;font-weight:700;margin:0 0 .5rem}
.hhm-h h2,#hh-page .hhm-h h2{color:#fff;font-size:1.75rem;line-height:1.3;margin:0 0 .6rem}
.hhm-h p.hhm-sub,#hh-page .hhm-h p.hhm-sub{color:rgba(255,255,255,.8);font-size:1rem;margin:0;line-height:1.6}
.hhm-grid,#hh-page .hhm-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start}
@media (max-width:900px){.hhm-grid,#hh-page .hhm-grid{grid-template-columns:1fr}}
.hhm-card,#hh-page .hhm-card{background:#fff;border-radius:16px;padding:1.5rem;box-shadow:0 10px 30px rgba(0,0,0,.18)}
.hhm-card h3,#hh-page .hhm-card h3{margin:0 0 1.1rem;font-size:1.0625rem;color:#0b1b2b}
.hhm-f,#hh-page .hhm-f{display:block;margin:0 0 1rem}
.hhm-f label,#hh-page .hhm-f label{display:block;font-size:.875rem;color:#334155;margin:0 0 .35rem;font-weight:600}
.hhm-f input,#hh-page .hhm-f input{width:100%;box-sizing:border-box;min-height:44px;padding:.6rem .75rem;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem;color:#0b1b2b;background:#f8fafc}
.hhm-f input:focus,#hh-page .hhm-f input:focus{outline:3px solid #16DB7F;outline-offset:1px;border-color:#16DB7F}
.hhm-f small,#hh-page .hhm-f small{display:block;color:#64748b;font-size:.78125rem;margin:.3rem 0 0;line-height:1.45}
.hhm-tab,#hh-page .hhm-tab{width:100%;border-collapse:collapse;font-size:.9375rem}
.hhm-tab th,#hh-page .hhm-tab th{text-align:left;color:#475569;font-weight:600;padding:.6rem .5rem;border-bottom:1px solid #e2e8f0}
.hhm-tab td,#hh-page .hhm-tab td{padding:.6rem .5rem;border-bottom:1px solid #f1f5f9;color:#0b1b2b;font-variant-numeric:tabular-nums;text-align:right}
.hhm-tab td:first-child,#hh-page .hhm-tab td:first-child{text-align:left;color:#475569}
.hhm-tab tr.hhm-fort td,#hh-page .hhm-tab tr.hhm-fort td{font-weight:700;color:#0b1b2b;background:rgba(22,219,127,.12);border-bottom:none}
.hhm-note,#hh-page .hhm-note{color:rgba(255,255,255,.72);font-size:.84375rem;line-height:1.6;margin:1.25rem 0 0;text-align:center}
.hhm-note a,#hh-page .hhm-note a{color:#8fd8ff;text-decoration:underline}
.eeat-sources,#hh-page .eeat-sources{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:14px;padding:1.5rem}
.eeat-sources h3,#hh-page .eeat-sources h3{color:#fff;margin:0 0 .9rem;font-size:1.0625rem}
.eeat-sources ul,#hh-page .eeat-sources ul{margin:0;padding:0 0 0 1.1rem}
.eeat-sources li,#hh-page .eeat-sources li{color:rgba(255,255,255,.85);margin:0 0 .5rem;line-height:1.55}
.eeat-sources a,#hh-page .eeat-sources a{color:#8fd8ff;text-decoration:underline}
.eeat-sources .src-domain,#hh-page .eeat-sources .src-domain{color:rgba(255,255,255,.55);font-size:.8125rem}
</style>
"""


# --------------------------------------------------------------------------
# 4813 — reponse encadree, fait date, calculateur de frais d'approche
# --------------------------------------------------------------------------
BLOC_4813 = """<section class="hhm-wrap" id="frais-approche" aria-labelledby="hhm-t-fa">
<div class="container">
<div class="hhm-rep">
<p><b>En une phrase.</b> Un logiciel import export agroalimentaire est un ERP qui calcule la valeur en douane d'un lot alimentaire, en déduit le coût au kilo réellement débarqué, et rattache à ce lot son certificat sanitaire et sa date limite de consommation.</p>
<p>Le repère réglementaire : à l'importation, la valeur en douane part de la valeur transactionnelle — le prix effectivement payé au fournisseur — majorée des frais de transport et d'assurance jusqu'au point d'entrée dans l'Union. C'est la règle du code des douanes de l'Union, règlement (UE) n° 952/2013, applicable depuis le 1er mai 2016 (<a href="https://www.douane.gouv.fr/fiche/valeur-en-douane-de-votre-marchandise-limportation" target="_blank" rel="noopener nofollow">valeur en douane à l'importation, douane.gouv.fr</a>). Tout ce qui s'ajoute ensuite — droits, inspection, manutention — constitue les frais d'approche.</p>
</div>
<div class="hhm-h">
<p class="hhm-over">Calculateur</p>
<h2 id="hhm-t-fa">Combien coûte vraiment votre lot importé, au kilo débarqué ?</h2>
<p class="hhm-sub">Le prix d'achat départ n'est pas le prix de revient. Ajoutez le fret, l'assurance, les droits et la freinte : l'écart se lit en coefficient d'approche.</p>
</div>
<div class="hhm-grid">
<div class="hhm-card">
<h3>Les données de votre lot</h3>
<form id="hhfa-form" novalidate>
<div class="hhm-f"><label for="hhfa-fob">Prix d'achat départ, en euros par kilo</label><input type="number" id="hhfa-fob" value="4.20" min="0" step="0.01" inputmode="decimal"></div>
<div class="hhm-f"><label for="hhfa-poids">Poids commandé, en kilos</label><input type="number" id="hhfa-poids" value="20000" min="0" step="1" inputmode="decimal"></div>
<div class="hhm-f"><label for="hhfa-fret">Fret et assurance jusqu'au point d'entrée, en euros</label><input type="number" id="hhfa-fret" value="3400" min="0" step="1" inputmode="decimal"><small>Selon l'Incoterm retenu, ces frais sont déjà dans le prix du fournisseur ou restent à votre charge.</small></div>
<div class="hhm-f"><label for="hhfa-taux">Taux de droit de douane, en pourcentage</label><input type="number" id="hhfa-taux" value="6" min="0" max="100" step="0.1" inputmode="decimal"><small>À lire dans le tarif douanier, à la position tarifaire de votre produit.</small></div>
<div class="hhm-f"><label for="hhfa-freinte">Freinte et écart de pesée constatés, en pourcentage</label><input type="number" id="hhfa-freinte" value="1.5" min="0" max="99" step="0.1" inputmode="decimal"><small>Ce que le quai pèse en moins de ce que le connaissement annonce.</small></div>
</form>
</div>
<div class="hhm-card">
<h3>Votre coefficient d'approche</h3>
<table class="hhm-tab">
<thead><tr><th scope="col">Poste</th><th scope="col">Montant</th></tr></thead>
<tbody>
<tr><td>Valeur en douane</td><td id="hhfa-vd">87 400 €</td></tr>
<tr><td>Droits de douane</td><td id="hhfa-dr">5 244 €</td></tr>
<tr><td>Coût total débarqué</td><td id="hhfa-tot">92 644 €</td></tr>
<tr><td>Poids réellement reçu</td><td id="hhfa-net">19 700 kg</td></tr>
<tr class="hhm-fort"><td>Coût au kilo débarqué</td><td id="hhfa-kg">4,703 €/kg</td></tr>
<tr class="hhm-fort"><td>Coefficient d'approche</td><td id="hhfa-coef">1,120</td></tr>
</tbody>
</table>
</div>
</div>
<p class="hhm-note">Les valeurs affichées au chargement sont un exemple chiffré : un conteneur de 20 tonnes acheté 4,20 € le kilo, 3 400 € de fret et d'assurance, 6 % de droits, 1,5 % de freinte au quai. Le lot revient à 4,703 € le kilo débarqué, soit un coefficient de 1,120 sur le prix d'achat. Modifiez les cinq champs pour vos propres lots.</p>
</div>
</section>
<script>
(function () {
  var form = document.getElementById('hhfa-form');
  if (!form) { return; }
  var champs = ['fob', 'poids', 'fret', 'taux', 'freinte'];
  function val(id) {
    var e = document.getElementById('hhfa-' + id);
    if (!e) { return 0; }
    var v = parseFloat(String(e.value).replace(',', '.'));
    if (isNaN(v)) { return 0; }
    return v;
  }
  function pose(id, t) {
    var e = document.getElementById('hhfa-' + id);
    if (e) { e.textContent = t; }
  }
  function fmt(n, d) {
    return n.toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function calc() {
    var fob = Math.max(val('fob'), 0);
    var poids = Math.max(val('poids'), 0);
    var fret = Math.max(val('fret'), 0);
    var taux = Math.min(Math.max(val('taux'), 0), 100);
    var freinte = Math.min(Math.max(val('freinte'), 0), 99);
    var vd = fob * poids + fret;
    var dr = vd * taux / 100;
    var tot = vd + dr;
    var net = poids * (1 - freinte / 100);
    var kg = net === 0 ? 0 : tot / net;
    var coef = fob === 0 ? 0 : kg / fob;
    pose('vd', fmt(vd, 0) + ' €');
    pose('dr', fmt(dr, 0) + ' €');
    pose('tot', fmt(tot, 0) + ' €');
    pose('net', fmt(net, 0) + ' kg');
    pose('kg', fmt(kg, 3) + ' €/kg');
    pose('coef', fmt(coef, 3));
  }
  champs.forEach(function (id) {
    var e = document.getElementById('hhfa-' + id);
    if (e) { e.addEventListener('input', calc); }
  });
  form.addEventListener('submit', function (ev) { ev.preventDefault(); calc(); });
  calc();
})();
</script>
"""

SOURCES_4813 = """<section class="hhm-wrap" id="sources">
<div class="container">
<div class="eeat-sources">
<h3>Sources et références officielles</h3>
<ul>
<li><a href="https://www.douane.gouv.fr/fiche/valeur-en-douane-de-votre-marchandise-limportation" target="_blank" rel="noopener nofollow">Valeur en douane de votre marchandise à l'importation <span class="src-domain">douane.gouv.fr</span></a></li>
<li><a href="https://www.douane.gouv.fr/demarche/importer-des-marchandises-soumises-reglementation-veterinaire" target="_blank" rel="noopener nofollow">Importer des marchandises soumises à réglementation vétérinaire <span class="src-domain">douane.gouv.fr</span></a></li>
<li><a href="https://www.franceagrimer.fr/international/traces-nt" target="_blank" rel="noopener nofollow">Certificats sanitaires et démarches dans TRACES NT <span class="src-domain">franceagrimer.fr</span></a></li>
<li><a href="https://webgate.ec.europa.eu/tracesnt/" target="_blank" rel="noopener nofollow">TRACES NT, le portail de la Commission européenne <span class="src-domain">ec.europa.eu</span></a></li>
<li><a href="https://iccwbo.org/business-solutions/incoterms-rules/" target="_blank" rel="noopener nofollow">Les règles Incoterms 2020 de la Chambre de commerce internationale <span class="src-domain">iccwbo.org</span></a></li>
</ul>
</div>
</div>
</section>
"""

# Les deux questions ajoutees a la FAQ de 4813, au format <details> de la page.
FAQ_4813 = [
    ("Comment calcule-t-on les frais d'approche d'un lot importé ?",
     "<p>On part de la valeur en douane : le prix effectivement payé au "
     "fournisseur, majoré du transport et de l'assurance jusqu'au point "
     "d'entrée dans l'Union. On y ajoute les droits de douane, calculés au "
     "taux de la position tarifaire du produit, puis les frais d'inspection, "
     "de manutention et de stockage sous douane. Le total est divisé non pas "
     "par le poids commandé mais par le poids réellement débarqué, freinte et "
     "écart de pesée déduits. Le rapport entre ce coût au kilo et le prix "
     "d'achat départ est le coefficient d'approche : c'est lui qui sert de "
     "base au tarif de vente, et c'est lui que le calculateur de cette page "
     "restitue.</p>"),
    ("Faut-il un document sanitaire pour importer un produit d'origine animale ?",
     "<p>Oui. Tout lot d'origine animale entrant dans l'Union européenne est "
     "présenté à un poste de contrôle frontalier et accompagné d'un document "
     "sanitaire commun d'entrée, le DSCE, déposé dans TRACES NT, le système "
     "d'information de la Commission européenne. En France, c'est le SIVEP "
     "qui réalise le contrôle et délivre ce document. Un ERP import-export "
     "rattache la pièce au lot : le numéro de DSCE, le certificat d'origine "
     "et la date limite de consommation suivent le lot jusqu'au bon de "
     "livraison du client, sans ressaisie.</p>"),
]


# --------------------------------------------------------------------------
# 7911 — du devis au bon de livraison, a poids variable
# --------------------------------------------------------------------------
BLOC_7911 = """<section class="hhm-wrap" id="poids-variable" aria-labelledby="hhm-t-pv">
<div class="container">
<div class="hhm-rep">
<p><b>En une phrase.</b> En agroalimentaire, la quantité change entre le devis et le bon de livraison : le devis annonce des pièces à un tarif au kilo, le bon de livraison porte le poids pesé à l'expédition, et c'est ce poids-là que la facture doit reprendre.</p>
<p>Le repère réglementaire : l'article L441-9 du code de commerce impose que la facture mentionne la quantité des produits effectivement livrés. Sur un produit vendu au kilo, c'est donc le poids pesé au quai qui fait foi, pas celui qui figurait au devis. Un cycle commercial qui recopie la quantité du devis jusqu'à la facture produit mécaniquement un écart à régulariser en avoir.</p>
</div>
<div class="hhm-h">
<p class="hhm-over">Du devis au bon de livraison</p>
<h2 id="hhm-t-pv">Ce que le poids variable change entre le devis et la facture</h2>
<p class="hhm-sub">Saisissez une ligne de commande en pièces, puis le poids réellement pesé : l'écart entre le devis et le bon de livraison apparaît en euros.</p>
</div>
<div class="hhm-grid">
<div class="hhm-card">
<h3>Votre ligne de commande</h3>
<form id="hhpv-form" novalidate>
<div class="hhm-f"><label for="hhpv-pieces">Nombre de pièces commandées</label><input type="number" id="hhpv-pieces" value="48" min="0" step="1" inputmode="decimal"></div>
<div class="hhm-f"><label for="hhpv-theo">Poids théorique par pièce, en kilos</label><input type="number" id="hhpv-theo" value="2.5" min="0" step="0.001" inputmode="decimal"><small>Le poids de catalogue, celui qui chiffre le devis.</small></div>
<div class="hhm-f"><label for="hhpv-pese">Poids total pesé à l'expédition, en kilos</label><input type="number" id="hhpv-pese" value="117.4" min="0" step="0.001" inputmode="decimal"><small>Ce que la bascule affiche au moment de charger.</small></div>
<div class="hhm-f"><label for="hhpv-prix">Tarif négocié, en euros par kilo</label><input type="number" id="hhpv-prix" value="14.90" min="0" step="0.01" inputmode="decimal"></div>
</form>
</div>
<div class="hhm-card">
<h3>Devis, bon de livraison, facture</h3>
<table class="hhm-tab">
<thead><tr><th scope="col">Document</th><th scope="col">Quantité</th><th scope="col">Montant</th></tr></thead>
<tbody>
<tr><td>Devis, au poids théorique</td><td id="hhpv-qtheo">120,000 kg</td><td id="hhpv-mtheo">1 788,00 €</td></tr>
<tr><td>Bon de livraison, au poids pesé</td><td id="hhpv-qpese">117,400 kg</td><td id="hhpv-mpese">1 749,26 €</td></tr>
<tr class="hhm-fort"><td>Écart à facturer</td><td id="hhpv-qecart">-2,600 kg</td><td id="hhpv-mecart">-38,74 €</td></tr>
<tr class="hhm-fort"><td>Écart en pourcentage</td><td id="hhpv-pct">-2,17 %</td><td id="hhpv-vide"></td></tr>
</tbody>
</table>
</div>
</div>
<p class="hhm-note">Les valeurs affichées au chargement sont un exemple chiffré : 48 pièces annoncées à 2,500 kg, 117,400 kg réellement pesés, 14,90 € le kilo. Le devis disait 1 788,00 €, le bon de livraison dit 1 749,26 € : 38,74 € d'écart sur une seule ligne, soit 2,17 %. Facturée au devis, cette ligne part en avoir.</p>
</div>
</section>
<script>
(function () {
  var form = document.getElementById('hhpv-form');
  if (!form) { return; }
  var champs = ['pieces', 'theo', 'pese', 'prix'];
  function val(id) {
    var e = document.getElementById('hhpv-' + id);
    if (!e) { return 0; }
    var v = parseFloat(String(e.value).replace(',', '.'));
    if (isNaN(v)) { return 0; }
    return Math.max(v, 0);
  }
  function pose(id, t) {
    var e = document.getElementById('hhpv-' + id);
    if (e) { e.textContent = t; }
  }
  function fmt(n, d) {
    return n.toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
  }
  function calc() {
    var pieces = val('pieces'), theo = val('theo'), pese = val('pese'), prix = val('prix');
    var qtheo = pieces * theo;
    var mtheo = qtheo * prix;
    var mpese = pese * prix;
    var qecart = pese - qtheo;
    var mecart = mpese - mtheo;
    var pct = mtheo === 0 ? 0 : mecart / mtheo * 100;
    pose('qtheo', fmt(qtheo, 3) + ' kg');
    pose('mtheo', fmt(mtheo, 2) + ' €');
    pose('qpese', fmt(pese, 3) + ' kg');
    pose('mpese', fmt(mpese, 2) + ' €');
    pose('qecart', fmt(qecart, 3) + ' kg');
    pose('mecart', fmt(mecart, 2) + ' €');
    pose('pct', fmt(pct, 2) + ' %');
  }
  champs.forEach(function (id) {
    var e = document.getElementById('hhpv-' + id);
    if (e) { e.addEventListener('input', calc); }
  });
  form.addEventListener('submit', function (ev) { ev.preventDefault(); calc(); });
  calc();
})();
</script>
"""


# --------------------------------------------------------------------------
# Balisage
# --------------------------------------------------------------------------
BALISAGE = {
    4813: dict(
        title="Logiciel import export agroalimentaire • Douane et frais d'approche",
        desc="Logiciel import export agroalimentaire : valeur en douane, droits "
             "et frais d'approche au kilo débarqué, DLC par lot. Démo gratuite.",
    ),
    5640: dict(
        title="Logiciel import export et gestion commerciale • Comparatif 2026",
        desc="Comparatif 2026 des logiciels de gestion commerciale import export : "
             "frais d'approche, droits de douane, Incoterms et multi-devises.",
    ),
}

# Liens entrants poses vers /blog/meilleurs-erp-import-export/ : ancres
# tournantes, contigues, jamais neutres, posees dans le corps de la page.
ENTRANTS_5640 = [
    # (id, type, texte d'ancrage a trouver dans le contenu, phrase a inserer)
    (4813, "pages",
     "Tout ce qui s'ajoute ensuite — droits, inspection, manutention — constitue les frais d'approche.</p>",
     " <p>Pour situer Hello Harel face aux autres éditeurs, le "
     "<a href=\"/blog/meilleurs-erp-import-export/\">logiciel de gestion commerciale import export</a> "
     "est comparé module par module dans notre dossier comparatif.</p>"),
]


# --------------------------------------------------------------------------
# Transformations
# --------------------------------------------------------------------------

def remplacer_h1(c, debut, accent):
    m = re.search(r'(?is)(<h1[^>]*class="[^"]*hero-title[^"]*"[^>]*>)(.*?)(</h1>)', c)
    if not m:
        raise RuntimeError("h1.hero-title introuvable")
    coul = re.search(r'class="accent"[^>]*style="color:([^";]+)', m.group(2))
    coul = coul.group(1) if coul else "#60a5fa"
    neuf = (m.group(1) + debut
            + '<span class="accent" style="color:' + coul + '">' + accent
            + "</span>" + m.group(3))
    return c[:m.start()] + neuf + c[m.end():]


def remplacer_accroche(c, t):
    m = re.search(r'(?is)(<p class="hero-description">)(.*?)(</p>)', c)
    if not m:
        raise RuntimeError("p.hero-description introuvable")
    return c[:m.start()] + m.group(1) + t + m.group(3) + c[m.end():]


def remplacer_badge(c, badge):
    m = re.search(r'(?is)(<div class="hero-badge">\s*<span class="dot"></span>)(.*?)(</div>)', c)
    if not m:
        raise RuntimeError("div.hero-badge introuvable")
    return c[:m.start()] + m.group(1) + badge + m.group(3) + c[m.end():]


def poser_byline(c, lecture):
    if "eeat-byline" in c:
        return c
    m = re.search(r'(?is)<p class="hero-cta-sub">.*?</p>', c)
    if not m:
        raise RuntimeError("p.hero-cta-sub introuvable")
    c = c[:m.end()] + BYLINE.replace("{LECTURE}", str(lecture)) + c[m.end():]
    s = re.search(r'<section[^>]*class="[^"]*hero-section', c)
    return c[:s.start()] + BYLINE_CSS + c[s.start():]


def poser_apres_hero(c, bloc):
    """Insere juste avant la section des logos, donc en haut du 2e ecran."""
    cle = '<section class="logos-section">'
    if c.count(cle) != 1:
        raise RuntimeError("point d'insertion ambigu : %d logos-section"
                           % c.count(cle))
    i = c.index(cle)
    return c[:i] + bloc + c[i:]


def ajouter_questions(c, questions):
    """Ajoute des <details> a la fin de la FAQ, au gabarit de la page."""
    b = bornes_section(c, "faq-section")
    if not b:
        raise RuntimeError("faq-section introuvable")
    bloc = c[b[0]:b[1]]
    dern = None
    for m in re.finditer(r"</details>", bloc):
        dern = m
    if dern is None:
        raise RuntimeError("aucun <details> dans la FAQ")
    # on reprend les attributs du dernier <details> et de son <summary>
    ouvr = re.findall(r"<details\b[^>]*>", bloc)[-1]
    summ = re.findall(r"<summary\b[^>]*>", bloc)[-1]
    ajout = ""
    for q, r in questions:
        if q in bloc:
            continue
        ajout += ouvr + summ + q + "</summary>" + r + "</details>"
    if not ajout:
        return c
    pos = b[0] + dern.end()
    return c[:pos] + ajout + c[pos:]


def faq_jsonld(c):
    b = bornes_section(c, "faq-section")
    qs = details(c[b[0]:b[1]])
    if len(qs) < 3:
        raise RuntimeError("moins de 3 questions dans la FAQ")
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer",
                                               "text": resume(r)}}
                           for q, r in qs]}
    return ('\n<script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False) + "</script>\n")


# --------------------------------------------------------------------------

def lire(pid, kind="pages"):
    d = n.call("wp/v2/%s/%d?context=edit&_fields=id,slug,link,content,meta"
               % (kind, pid))
    el = d["meta"].get("_elementor_data")
    if el not in ("", "[]", None):
        raise RuntimeError("%d : _elementor_data non vide, on ne touche pas" % pid)
    return d


def ecrire(pid, contenu, kind="pages"):
    n.call("wp/v2/%s/%d" % (kind, pid), "POST", {"content": contenu})


def rankmath(pid, title, desc):
    n.call("rankmath/v1/updateMeta", "POST",
           {"objectID": pid, "objectType": "post",
            "meta": {"rank_math_title": title, "rank_math_description": desc}})


def verifier(pid, c, avant):
    assert len(c) < max(PLAFOND, avant), \
        "%d : %d o au-dessus du plafond de rendu" % (pid, len(c))
    assert sans_amp_nu_dans_scripts(c), "%d : un & nu dans un <script>" % pid
    assert c.count("<h1") == 1, "%d : %d H1" % (pid, c.count("<h1"))


# --------------------------------------------------------------------------

def main(poser=False):
    os.makedirs(SAUVE, exist_ok=True)
    print("mode :", "ECRITURE REELLE" if poser else "blanc (aucune écriture)", "\n")
    rapport = []

    # ---- 4813 : /fonctionnalites/import-export/
    d = lire(4813)
    c = d["content"]["raw"]
    open(os.path.join(SAUVE, "4813.html"), "w").write(c)
    avant = len(c)
    c = remplacer_badge(c, "Logiciel import export agroalimentaire")
    c = remplacer_h1(c, "Le logiciel import export agroalimentaire qui ",
                     "calcule vos frais d'approche au kilo débarqué")
    c = remplacer_accroche(
        c,
        "Un logiciel import export agroalimentaire reconstitue le coût réel "
        "d'un lot importé : prix d'achat départ, fret, assurance, droits de "
        "douane et frais d'inspection ramenés au kilo réellement débarqué, "
        "freinte déduite. Le lot entre en stock avec son certificat sanitaire "
        "et sa date limite de consommation déjà rattachés.")
    c = poser_byline(c, 8)
    if "hh-modules-sem41-css" not in c:
        s = re.search(r'<section[^>]*class="[^"]*hero-section', c)
        c = c[:s.start()] + MODULES_CSS + c[s.start():]
    c = poser_apres_hero(c, BLOC_4813)
    c = ajouter_questions(c, FAQ_4813)
    # lien sortant contextuel vers le comparatif, pose dans la reponse encadree
    for pid, kind, ancre, phrase in ENTRANTS_5640:
        if pid == 4813:
            if ancre not in c:
                raise RuntimeError("4813 : point d'ancrage du lien introuvable")
            c = c.replace(ancre, ancre + phrase, 1)
    assert "FAQPage" not in c, "4813 : un FAQPage existe déjà"
    c = c + faq_jsonld(c) + SOURCES_4813
    verifier(4813, c, avant)
    rapport.append(("4813 /fonctionnalites/import-export/", avant, len(c)))
    if poser:
        ecrire(4813, c)
        rankmath(4813, BALISAGE[4813]["title"], BALISAGE[4813]["desc"])

    # ---- 7911 : /fonctionnalites/logiciel-devis-commande-bon-livraison/
    d = lire(7911)
    c = d["content"]["raw"]
    open(os.path.join(SAUVE, "7911.html"), "w").write(c)
    avant = len(c)
    notes = []
    c = reparer_amp_nus(c, notes)
    for x in notes:
        print("  7911 — réparation :", x)
    c = remplacer_h1(c, "Le logiciel devis, commande et bon de livraison qui ",
                     "facture le poids réellement pesé, pas celui du devis")
    if "hh-modules-sem41-css" not in c:
        s = re.search(r'<section[^>]*class="[^"]*hero-section', c)
        c = c[:s.start()] + MODULES_CSS + c[s.start():]
    c = poser_apres_hero(c, BLOC_7911)
    verifier(7911, c, avant)
    rapport.append(("7911 /fonctionnalites/logiciel-devis-commande-bon-livraison/",
                    avant, len(c)))
    if poser:
        ecrire(7911, c)

    # ---- 5640 : /blog/meilleurs-erp-import-export/ — balisage seul
    if poser:
        rankmath(5640, BALISAGE[5640]["title"], BALISAGE[5640]["desc"])
    rapport.append(("5640 /blog/meilleurs-erp-import-export/ (balisage)", "-", "-"))

    print("%-62s %>9s %>9s" % ("page", "avant", "apres") if False else
          "%-62s %9s %9s" % ("page", "avant", "après"))
    for u, a, b in rapport:
        print("%-62s %9s %9s" % (u[:62], a, b))
    print("\nbalisage :")
    for pid, v in BALISAGE.items():
        t, de = px(v["title"]), px(v["desc"])
        al = "" if (200 <= t <= 561 and 400 <= de <= 985) else "   <-- HORS BORNES"
        print("  %-6d title %4d px   desc %4d px%s" % (pid, t, de, al))


if __name__ == "__main__":
    main(poser="--ecrire" in sys.argv)
