#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VARIANTE A de /negoce/ — page produit import-export alimentaire. BROUILLON NOINDEX.

Fonde sur le releve SERP du 21/08/2026 sur « logiciel import export » :
  #1 akanea.com   — glossaire/definition, 1617 mots, 6 H2 en questions, peu de visuel
  #2 dashdoc.com  — blog comparatif, 2592 mots, 9 H2 + 26 H3, FAQ
  #3 trade-easy.fr— PAGE PRODUIT, 1786 mots, 8 cartes fonction en prose longue,
                    icones couleur, fiche produit a telecharger, bandeau demo photo

  Ce que la SERP recompense : structure en questions + definition + comparatif + FAQ.
  Le format d'une page produit qui tient : les cartes en PROSE, pas en puces.

  L'ANGLE : la SERP est saturee de TMS et de transport (Akanea TMS, Dashdoc) et
  d'import de donnees (Teogest, MyClic). PERSONNE ne traite l'import-export
  ALIMENTAIRE — ou le cout de revient doit integrer les frais d'approche ET le
  poids variable ET la DLC. C'est le coin ou l'on entre.

Images : uniquement des visuels reels de la mediatheque, verifies un par un.
Reserve : aucun visuel de conteneur, de port ou de douane n'existe en mediatheque.
DRY par defaut ; --live pour publier.
"""
import sys, json
import wp_common as w

SLUG = "negoce-test-a-import-export"
TITLE = "[TEST A] ERP Import Export Alimentaire • Frais d'Approche & Lots"

U = "https://www.helloharel.com/wp-content/uploads/"
IMG = {
    "hero":    U + "2026/08/ERP-logiciel-pour-les-grossistes-en-lait.webp",   # entrepot, palettes
    "produit": U + "2025/06/Hello-Harel-Gestion-de-la-logistique.png",        # capture UI reelle
    "t1":      U + "2026/08/Logiciel-de-grossistes-alimentaire-1.webp",       # magasinier rayonnages
    "t2":      U + "2026/08/Logiciel-de-grossistes-alimentaire-2.webp",       # controle tablette
    "t3":      U + "2026/08/Logiciel-de-grossistes-alimentaire-4.webp",       # preparation commandes
    "demo":    U + "2026/08/Logiciel-pour-grossiste-industriel.webp",         # responsable, ligne prod
}

def ico(p):
    return ('<span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.9" aria-hidden="true"><path stroke-linecap="round" '
            'stroke-linejoin="round" d="%s"/></svg></span>') % p

# 8 cartes en PROSE LONGUE — le format qui tient chez trade-easy
CARTES = [
("M12 8c-1.7 0-3 .9-3 2s1.3 2 3 2 3 .9 3 2-1.3 2-3 2m0-8V4m0 12v2",
 "Frais d’approche et coût de revient réel",
 "Le prix payé au fournisseur n’est jamais votre coût. Il faut y ajouter le fret, l’assurance, "
 "les droits de douane, les frais de dossier et le transitaire, puis répartir l’ensemble sur "
 "chaque référence du conteneur — au poids, à la valeur ou au volume selon ce qui est juste pour "
 "la marchandise. Hello Harel applique ce coefficient automatiquement à la réception : le coût de "
 "revient au kilo est connu le jour où la marchandise entre, pas au moment du bilan. C’est ce "
 "calcul qui décide si une opération était rentable, et c’est celui que la plupart des entreprises "
 "font encore dans un tableur, plusieurs semaines après."),

("M3 3h18v4H3zM5 7v12a1 1 0 001 1h12a1 1 0 001-1V7M10 11h4",
 "Multi-devises et écart de change",
 "Une commande passée en dollars et réglée trois mois plus tard n’a pas le même coût qu’à la "
 "signature. Chaque opération porte son taux à la date de l’événement, et l’écart constaté au "
 "règlement est enregistré séparément, au lieu d’être noyé dans la marge. Vous savez donc ce qui "
 "relève de votre négociation d’achat et ce qui relève du change — deux sujets qu’on confond "
 "souvent, et qui n’appellent pas les mêmes décisions."),

("M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10",
 "Stock en transit, sous douane et disponible",
 "Trois états, trois réalités. La marchandise partie du fournisseur mais pas encore arrivée est "
 "un engagement, pas du stock. Celle qui est arrivée mais pas dédouanée ne peut pas être vendue. "
 "Celle qui est disponible peut l’être. Confondre les trois, c’est vendre ce qu’on n’a pas ou "
 "racheter ce qu’on possède déjà. Hello Harel les suit séparément et affiche la date d’arrivée "
 "prévue, ce qui permet d’engager une vente sur une marchandise en route en connaissance de cause."),

("M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6l7-3z",
 "Traçabilité du lot et de l’origine",
 "À l’import alimentaire, la traçabilité ne s’arrête pas au fournisseur : il faut le lot d’origine, "
 "le pays de provenance, le numéro d’agrément de l’établissement expéditeur et les certificats "
 "sanitaires ou phytosanitaires qui accompagnent la marchandise. Tout est attaché au lot et "
 "remonte jusqu’au client livré. En cas de contrôle ou de rappel, la liste des clients concernés "
 "s’obtient en quelques minutes, sans rouvrir de classeur."),

("M8 7V3m8 4V3M3 11h18M5 21h14a2 2 0 002-2V7H3v12a2 2 0 002 2z",
 "DLC courtes et rotation FEFO",
 "C’est le point où un logiciel d’import généraliste s’arrête. Une marchandise alimentaire "
 "importée arrive avec une DLC déjà entamée par le transport : ce qui reste de durée de vie "
 "conditionne à qui on peut la vendre et à quel prix. La rotation se fait en premier périmé, "
 "premier sorti, avec des alertes avant péremption et la possibilité de déclencher une remise "
 "ciblée sur les lots qui approchent — plutôt que de constater la perte."),

("M4 7h16M4 12h16M4 17h10",
 "Poids variable, de la réception à la facture",
 "On commande vingt cartons, on en reçoit vingt qui ne pèsent pas le poids annoncé. Si la "
 "facturation se fait au poids commandé, il faut ensuite émettre un avoir ; si elle se fait au "
 "poids réellement pesé, le problème n’existe pas. Le poids variable est natif dans Hello Harel : "
 "bon de pesée, étiquette et facture sortent de la même donnée, et disent donc la même chose."),

("M9 12l2 2 4-4M7.8 4.7a3.3 3.3 0 004.6-1.1 3.3 3.3 0 013.8 0 3.3 3.3 0 004.6 1.1",
 "Liasse documentaire et formalités",
 "Facture commerciale, packing list, connaissement, certificat d’origine, document sanitaire "
 "commun d’entrée : chaque opération traîne une liasse qui doit être complète au bon moment, "
 "sous peine d’immobilisation. Les documents sont rattachés à l’opération et leur présence est "
 "contrôlée à chaque étape, ce qui évite de découvrir la pièce manquante quand le conteneur est "
 "déjà à quai."),

("M3 3v18h18M7 15l4-4 3 3 5-6",
 "Marge par opération, par client et par référence",
 "La question utile n’est pas « quel est mon chiffre d’affaires » mais « quelles opérations "
 "gagnent de l’argent ». Une fois le coût de revient réel calculé, la marge se lit par conteneur, "
 "par référence, par client et par commercial. C’est ce qui permet d’arrêter une ligne de produits "
 "qui coûte plus qu’elle ne rapporte — un arbitrage impossible tant que le coût reste estimé."),
]

# Comparatif a 3 colonnes : la SERP est pleine de TMS, il faut se situer
COMPARATIF = [
 ("Ce que vous cherchez", "TMS / transitaire", "ERP généraliste", "Hello Harel"),
 ("Suivre l’acheminement", "oui, c’est son métier", "non", "oui, dates et statuts"),
 ("Répartir les frais d’approche", "non", "développement spécifique", "natif, à la réception"),
 ("Stock sous douane vs vendable", "partiel", "non", "trois états distincts"),
 ("Poids variable", "non", "développement spécifique", "natif"),
 ("DLC et rotation FEFO", "non", "non", "natif, avec alertes"),
 ("Lot d’origine et certificats", "documents seulement", "non", "attaché au lot"),
 ("Facturation et marge réelle", "non", "oui, sur coût estimé", "sur coût de revient réel"),
]

FILLES = [
 ("/negoce/achats-approvisionnements/", "gérer les achats et approvisionnements",
  "Cadenciers fournisseurs, contrats d’achat, engagements et suivi des arrivages."),
 ("/negoce/stocks-multi-depots/", "stocks multi-dépôts",
  "Plusieurs entrepôts, transit, sous douane et marchandise réservée."),
 ("/negoce/tracabilite-lots/", "traçabilité des lots",
  "Lot d’origine, provenance, certificats et rappel produit."),
 ("/negoce/ventes-devis-commandes/", "ventes, devis et commandes",
  "Télévente, devis multi-devises, commandes et bons de livraison."),
 ("/negoce/tarifs-reporting-edi/", "tarifs, reporting et EDI",
  "Grilles par client, échanges EDI et reporting de marge."),
]

FAQ = [
 ("Qu’est-ce qu’un logiciel import export ?",
  "Un logiciel import export pilote les flux de marchandises entre plusieurs pays : achats en devises, incoterms, acheminement, formalités douanières, stock en transit et facturation multi-devises. Appliqué à l’alimentaire, il ajoute trois exigences que les outils généralistes ne portent pas : le poids variable, les DLC et la traçabilité du lot d’origine."),
 ("Quelle différence avec un TMS ?",
  "Un TMS pilote le transport — l’acheminement, les documents de transport, la relation avec les transitaires. Il ne calcule ni votre coût de revient, ni votre marge, ni votre stock vendable. Les deux outils sont complémentaires : le TMS sait où est la marchandise, l’ERP sait ce qu’elle vous coûte et ce qu’elle vous rapporte."),
 ("Comment sont calculés les frais d’approche ?",
  "Le fret, l’assurance, les droits de douane et les frais de dossier sont saisis sur l’opération puis répartis sur chaque référence du conteneur, au poids, à la valeur ou au volume. Le coefficient obtenu s’applique automatiquement au prix d’achat pour donner le coût de revient réel, disponible dès la réception."),
 ("Le logiciel gère-t-il les incoterms ?",
  "Oui. L’incoterm est porté par la ligne d’achat : il détermine à quel moment la marchandise entre dans votre stock et dans votre coût, et quelles charges vous incombent. C’est aussi ce qui conditionne le transfert de risque, donc la couverture d’assurance."),
 ("Peut-on vendre une marchandise encore en transit ?",
  "Oui, et c’est courant en négoce alimentaire. La marchandise en route est visible avec sa date d’arrivée prévue, ce qui permet d’engager une vente en connaissance de cause — la distinction avec le stock disponible reste explicite pour éviter de promettre ce qui n’est pas encore là."),
 ("Comment est gérée la DLC d’une marchandise importée ?",
  "La DLC est portée par le lot, pas par la référence : deux lots du même produit n’ont pas la même date. La rotation se fait en FEFO, avec des alertes avant péremption et la possibilité de déclencher une remise ciblée sur les lots concernés."),
 ("Combien de temps dure le déploiement ?",
  "Comptez 4 à 8 semaines entre le cadrage et la bascule, reprise des données comprise. Le délai tient parce que les processus de la filière sont préconfigurés : le poids variable, le multi-devises et les DLC n’ont pas à être modélisés."),
 ("Hello Harel est-il un logiciel français ?",
  "Oui, édité en France depuis 2014 et proposé en SaaS : pas de serveur à administrer, mises à jour incluses, accès depuis le bureau comme depuis l’entrepôt. Plus de 200 entreprises agroalimentaires l’utilisent, avec une note de 5,0 sur 5."),
]

CSS = """
<style id="hh-vA">
#hva{--c:#0090c8;--c2:#00B1F5;--ink:#0f172a;--gr:#475569;--gl:#64748b;--bd:#e2e8f0;--bg:#f8fafc;
font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--ink);line-height:1.68}
#hva *{box-sizing:border-box}
#hva .w{max-width:1120px;margin:0 auto;padding:0 24px}
#hva section{padding:clamp(46px,6vw,80px) 0}
#hva .alt{background:var(--bg)}
#hva h1{font-size:clamp(1.9rem,4vw,3rem);line-height:1.12;font-weight:800;letter-spacing:-.022em;margin:.75rem 0 .9rem}
#hva h2{font-size:clamp(1.45rem,3vw,2.15rem);line-height:1.18;font-weight:800;margin:0 0 .55rem;letter-spacing:-.014em}
#hva h3{font-size:1.06rem;font-weight:700;margin:0 0 .45rem;line-height:1.3}
#hva p{color:var(--gr);margin:0 0 .9rem}
#hva .eyebrow{display:inline-block;background:#e0f2fe;color:var(--c);font-weight:700;font-size:.72rem;
letter-spacing:.08em;text-transform:uppercase;padding:.42rem .9rem;border-radius:999px}
#hva .lead{font-size:1.13rem;max-width:640px}
#hva .sub{max-width:780px;margin-bottom:1.9rem}
#hva .btn{display:inline-flex;align-items:center;gap:9px;background:linear-gradient(135deg,var(--c),var(--c2));
color:#fff!important;font-weight:800;font-size:1.05rem;padding:16px 30px;border-radius:14px;text-decoration:none;
box-shadow:0 12px 28px rgba(0,144,200,.3)}
#hva .btn.ghost{background:transparent;color:var(--c)!important;border:2px solid var(--c);box-shadow:none}
#hva .btns{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
/* HERO photo */
#hva .hero{position:relative;border-radius:26px;overflow:hidden;min-height:460px;display:flex;align-items:center}
#hva .hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
#hva .hero .veil{position:absolute;inset:0;background:linear-gradient(100deg,rgba(4,32,48,.93) 0%,rgba(4,32,48,.78) 46%,rgba(4,32,48,.30) 100%)}
#hva .hero .in{position:relative;padding:clamp(30px,4vw,54px);max-width:660px}
#hva .hero h1,#hva .hero p{color:#fff}
#hva .hero .lead{color:rgba(255,255,255,.94)}
#hva .proof{display:flex;flex-wrap:wrap;gap:9px;margin-top:1.5rem}
#hva .proof span{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.26);color:#fff;
border-radius:999px;padding:7px 14px;font-size:.85rem;font-weight:600}
/* bloc calcul — l'angle */
#hva .calc{display:grid;grid-template-columns:1.05fr .95fr;gap:30px;align-items:center}
#hva .tab{width:100%;border-collapse:collapse;background:#fff;border-radius:16px;overflow:hidden;
box-shadow:0 10px 30px rgba(15,23,42,.07);font-size:.94rem}
#hva .tab td{padding:11px 16px;border-bottom:1px solid var(--bd);color:var(--gr)}
#hva .tab tr:last-child td{border-bottom:none}
#hva .tab td:last-child{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink);font-weight:600;white-space:nowrap}
#hva .tab .tot td{background:#e0f2fe;color:var(--ink);font-weight:800;font-size:1rem}
#hva .tab .head td{background:#0f172a;color:#fff;font-weight:700;font-size:.8rem;
text-transform:uppercase;letter-spacing:.05em}
/* cartes fonction — prose longue */
#hva .cards{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:1.6rem}
#hva .card{background:#fff;border:1px solid var(--bd);border-radius:20px;padding:26px 24px}
#hva .card p{font-size:.95rem;margin:0;color:var(--gl);line-height:1.62}
#hva .ic{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:13px;
background:linear-gradient(135deg,var(--c),var(--c2));color:#fff;margin-bottom:14px}
#hva .ic svg{width:23px;height:23px}
/* capture produit */
#hva .shot{display:grid;grid-template-columns:.95fr 1.05fr;gap:34px;align-items:center}
#hva .shot img{width:100%;border-radius:18px;border:1px solid var(--bd);box-shadow:0 18px 44px rgba(15,23,42,.12);display:block}
#hva .cap{font-size:.85rem;color:var(--gl);margin-top:.7rem}
/* comparatif */
#hva .cmpwrap{overflow-x:auto;margin-top:1.5rem;border-radius:16px;box-shadow:0 10px 30px rgba(15,23,42,.07)}
#hva table.cmp{width:100%;border-collapse:collapse;background:#fff;font-size:.93rem;min-width:640px}
#hva table.cmp th{background:#0f172a;color:#fff;text-align:left;padding:14px 16px;font-size:.78rem;
text-transform:uppercase;letter-spacing:.05em;font-weight:700}
#hva table.cmp th:last-child{background:var(--c)}
#hva table.cmp td{padding:12px 16px;border-bottom:1px solid var(--bd);color:var(--gr)}
#hva table.cmp td:first-child{color:var(--ink);font-weight:600}
#hva table.cmp td:last-child{background:#f0f9ff;color:var(--ink);font-weight:600}
#hva table.cmp tr:last-child td{border-bottom:none}
/* silo */
#hva .silo{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-top:1.5rem}
#hva .silo a{display:block;background:#fff;border:1px solid var(--bd);border-radius:16px;padding:20px;
text-decoration:none;transition:border-color .15s,transform .15s}
#hva .silo a:hover{border-color:var(--c);transform:translateY(-2px)}
#hva .silo h3{color:var(--c);font-size:1rem}
#hva .silo p{font-size:.9rem;margin:0;color:var(--gl)}
/* faq */
#hva details{background:#fff;border:1px solid var(--bd);border-radius:14px;padding:16px 20px;margin:0 0 10px}
#hva summary{font-weight:700;cursor:pointer;list-style:none}
#hva summary::-webkit-details-marker{display:none}
#hva summary:after{content:"+";float:right;color:var(--c);font-weight:800;font-size:1.15rem;line-height:1}
#hva details[open] summary:after{content:"\\2013"}
#hva details p{margin:.75rem 0 0;font-size:.95rem}
/* bandeau demo */
#hva .demo{position:relative;border-radius:26px;overflow:hidden;display:grid;
grid-template-columns:1.15fr .85fr;align-items:stretch;min-height:320px}
#hva .demo .txt{background:linear-gradient(135deg,#0090c8,#00B1F5);color:#fff;padding:clamp(28px,3.6vw,46px);
display:flex;flex-direction:column;justify-content:center}
#hva .demo .txt h2,#hva .demo .txt p{color:#fff}
#hva .demo .txt p{color:rgba(255,255,255,.94)}
#hva .demo img{width:100%;height:100%;object-fit:cover;display:block}
#hva .demo .btn{background:#fff;color:var(--c)!important;align-self:flex-start;box-shadow:0 10px 24px rgba(2,32,54,.2)}
#hva .trip{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:1.6rem}
#hva .trip figure{margin:0}
#hva .trip img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;display:block;
border:1px solid var(--bd)}
#hva .trip figcaption{font-size:.9rem;color:var(--gl);margin-top:.6rem;line-height:1.5}
#hva .trip b{color:var(--ink)}
#hva .note{background:#fffbeb;border:1px solid #fde68a;color:#92400e;border-radius:12px;padding:14px 18px;font-size:.9rem;margin:0}
@media(max-width:900px){
 #hva .cards,#hva .calc,#hva .shot,#hva .demo{grid-template-columns:1fr}
 #hva .silo,#hva .trip{grid-template-columns:1fr}
 #hva .demo img{max-height:240px}
}
</style>
"""

def build():
    cards = "".join('<div class="card">%s<h3>%s</h3><p>%s</p></div>' % (ico(p), t, d)
                    for p, t, d in CARTES)
    silo = "".join('<a href="%s"><h3>%s →</h3><p>%s</p></a>' % (u, a, d) for u, a, d in FILLES)
    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQ)
    head = COMPARATIF[0]
    rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in COMPARATIF[1:])
    cmp_tbl = ('<table class="cmp"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>'
               % ("".join("<th>%s</th>" % c for c in head), rows))
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    body = (
'<div id="hva">'
'<section class="w" style="padding-bottom:0"><p class="note"><b>Variante A — test A/B, brouillon non indexé.</b> '
'Page produit reciblée sur l’import-export alimentaire. Ne pas publier sans avoir posé le noindex.</p></section>'

# 1 · HERO photo
'<section style="padding-top:24px"><div class="w"><div class="hero">'
'<img src="%(hero)s" alt="Entrepôt de négoce alimentaire, palettes et préparation de commandes" loading="eager">'
'<div class="veil"></div><div class="in">'
'<span class="eyebrow">Import-export alimentaire</span>'
'<h1>L’ERP import export qui calcule votre coût de revient réel</h1>'
'<p class="lead">Frais d’approche répartis au conteneur, multi-devises, stock sous douane, '
'poids variable et DLC : tout ce qu’un TMS ne fait pas et qu’un ERP généraliste facture en '
'développement spécifique.</p>'
'<div class="btns"><a class="btn" href="/contact/">Voir l’ERP sur mes opérations →</a></div>'
'<div class="proof"><span>+200 entreprises agroalimentaires</span><span>Noté 5,0/5 sur 31 avis</span>'
'<span>Édité en France depuis 2014</span><span>Déploiement en 4 à 8 semaines</span></div>'
'</div></div></div></section>'

# 2 · L'ANGLE : le calcul des frais d'approche, chiffre
'<section class="alt"><div class="w">'
'<h2>Le calcul que personne ne vous montre</h2>'
'<p class="sub">Sur un conteneur, l’écart entre le prix payé au fournisseur et le coût réel de la '
'marchandise dépasse couramment 20 %%. Tant que ce calcul se fait dans un tableur, après coup, '
'la marge affichée sur vos factures est une estimation.</p>'
'<div class="calc"><div>'
'<table class="tab"><tbody>'
'<tr class="head"><td>Conteneur 20 pieds — exemple</td><td>Montant</td></tr>'
'<tr><td>Marchandise, prix fournisseur</td><td>32 000 €</td></tr>'
'<tr><td>Fret maritime</td><td>2 400 €</td></tr>'
'<tr><td>Assurance transport</td><td>310 €</td></tr>'
'<tr><td>Droits de douane</td><td>2 560 €</td></tr>'
'<tr><td>Transitaire et frais de dossier</td><td>640 €</td></tr>'
'<tr><td>Écart de change au règlement</td><td>480 €</td></tr>'
'<tr class="tot"><td>Coût de revient réel</td><td>38 390 €</td></tr>'
'<tr class="tot"><td>Coefficient appliqué</td><td>× 1,20</td></tr>'
'</tbody></table>'
'<p class="cap">Exemple illustratif de répartition. Les postes et la clé de répartition — au poids, '
'à la valeur ou au volume — se paramètrent par type d’opération.</p>'
'</div><div>'
'<h3 style="font-size:1.15rem">Ce que ça change concrètement</h3>'
'<p>Vendre à <b>+15 %%</b> du prix fournisseur, c’est vendre <b>à perte</b> sur cet exemple. '
'C’est l’erreur la plus fréquente en négoce à l’import, et elle ne se voit pas ligne à ligne : '
'elle se voit à la fin du trimestre, quand la marge globale ne correspond pas aux marges affichées.</p>'
'<p>Hello Harel applique le coefficient <b>à la réception</b>, référence par référence. Le coût de '
'revient au kilo est disponible avant la première vente, et la marge se lit ensuite par conteneur, '
'par client et par référence.</p>'
'</div></div></div></section>'

# 3 · 8 CARTES FONCTION en prose
'<section><div class="w">'
'<h2>Huit fonctions écrites pour le négoce alimentaire à l’international</h2>'
'<p class="sub">Ce ne sont pas des options : ce sont les points sur lesquels les outils '
'généralistes et les TMS s’arrêtent.</p>'
'<div class="cards">%(cards)s</div>'
'</div></section>'

# 4 · CAPTURE PRODUIT reelle
'<section class="alt"><div class="w"><div class="shot"><div>'
'<img src="%(produit)s" alt="Interface Hello Harel : ordres de fabrication, gestion des tournées et livraisons">'
'<p class="cap">Interface Hello Harel — pilotage des opérations, des tournées et des livraisons.</p>'
'</div><div>'
'<h2>Un seul outil, du conteneur au client</h2>'
'<p>L’achat, la réception, le stock, la préparation, la livraison et la facturation vivent dans la '
'même base. Ce n’est pas un confort d’usage : c’est ce qui garantit que le bon de pesée, '
'l’étiquette, le bon de livraison et la facture disent tous la même chose.</p>'
'<p>Les équipes de l’entrepôt travaillent sur terminal mobile — réception, pesée, préparation, '
'inventaire — et l’information remonte immédiatement, sans ressaisie le soir.</p>'
'<div class="btns"><a class="btn ghost" href="/fonctionnalites/import-export/">Le module import export →</a></div>'
'</div></div></div></section>'

# 4bis · TRIPTYQUE terrain
'<section><div class="w">'
'<h2>Ce que ça donne sur le terrain</h2>'
'<p class="sub">L\'outil ne vit pas dans un bureau : il vit à la réception, au contrôle et à la '
'préparation. C\'est là qu\'il fait gagner du temps, ou qu\'il en fait perdre.</p>'
'<div class="trip">'
'<figure><img src="%(t1)s" alt="Réception de marchandise en entrepôt de négoce alimentaire" loading="lazy">'
'<figcaption><b>À la réception.</b> Pesée, contrôle de température et affectation du lot dès le quai, '
'sur terminal mobile.</figcaption></figure>'
'<figure><img src="%(t2)s" alt="Contrôle qualité et agréage sur palettes" loading="lazy">'
'<figcaption><b>Au contrôle.</b> Agréage, écarts constatés et photos rattachées au lot, opposables '
'au fournisseur.</figcaption></figure>'
'<figure><img src="%(t3)s" alt="Préparation de commandes et expédition" loading="lazy">'
'<figcaption><b>À la préparation.</b> Picking en FEFO, poids réel saisi à la pesée, bon de livraison '
'édité dans la foulée.</figcaption></figure>'
'</div></div></section>'

# 5 · COMPARATIF a 3 colonnes — se situer face aux TMS
'<section class="alt"><div class="w">'
'<h2>TMS, ERP généraliste ou ERP métier : lequel fait quoi</h2>'
'<p class="sub">La confusion est fréquente parce que les trois parlent d’import-export. '
'Ils ne résolvent pourtant pas le même problème.</p>'
'<div class="cmpwrap">%(cmp)s</div>'
'<p class="cap">Un TMS et un ERP métier ne s’opposent pas : le TMS sait où est la marchandise, '
'l’ERP sait ce qu’elle coûte et ce qu’elle rapporte.</p>'
'</div></section>'

# 6 · SILO — maillage exact-match
'<section><div class="w">'
'<h2>Par où entrer, selon ce que vous voulez régler</h2>'
'<p class="sub">Chaque brique du négoce a sa page dédiée.</p>'
'<div class="silo">%(silo)s</div>'
'</div></section>'

# 7 · FAQ
'<section><div class="w" style="max-width:860px">'
'<h2>Les réponses à vos questions</h2>'
'<div style="margin-top:1.4rem">%(faq)s</div>'
'</div></section>'

# 8 · DEMO photo
'<section class="alt"><div class="w"><div class="demo">'
'<div class="txt"><h2>Voyez-le sur vos propres conteneurs</h2>'
'<p>30 minutes, sans engagement, avec quelqu’un qui connaît les incoterms, les frais d’approche '
'et les contraintes de la marchandise alimentaire. On part de vos opérations réelles, pas d’un '
'jeu de données de démonstration.</p>'
'<a class="btn" href="/contact/">Réserver ma démonstration →</a></div>'
'<img src="%(demo)s" alt="Responsable d\'exploitation en site agroalimentaire">'
'</div></div></section>'
'</div>'
'<script type="application/ld+json">%(ld)s</script>'
) % {"hero": IMG["hero"], "produit": IMG["produit"], "demo": IMG["demo"],
     "t1": IMG["t1"], "t2": IMG["t2"], "t3": IMG["t3"],
     "cards": cards, "silo": silo, "faq": faq, "cmp": cmp_tbl,
     "ld": json.dumps(ld_faq, ensure_ascii=False)}
    return CSS + body


def main():
    live = "--live" in sys.argv
    c = build()
    import re
    mots = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)).split())
    print("taille : %d car. | mots : %d" % (len(c), mots))
    print("images  : %d" % len(re.findall(r'<img ', c)))
    print("cartes  : %d | lignes comparatif : %d | FAQ : %d" %
          (c.count('class="card"'), len(COMPARATIF) - 1, len(FAQ)))
    ex = w.api("pages?slug=%s&status=any&_fields=id,status" % SLUG)
    if not live:
        print("DRY-RUN — ajouter --live"); return
    if ex:
        w.update_content("pages", ex[0]["id"], c, live=True)
        w.api("pages/%d" % ex[0]["id"], method="POST", data={"title": TITLE})
        print("MISE A JOUR id=%s (%s)" % (ex[0]["id"], ex[0]["status"]))
    else:
        r = w.api("pages", method="POST", data={"title": TITLE, "slug": SLUG, "status": "draft",
                                                "content": c, "template": "elementor_canvas"})
        print("CREEE id=%s" % r.get("id"))


if __name__ == "__main__":
    main()
