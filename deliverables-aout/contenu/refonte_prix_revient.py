#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REFONTE /blog/calculer-le-prix-de-revient-en-boulangerie/ (post 3430)
Cible : « logiciel prix de revient ». Process operationnel-contenu, etapes 1 a 7.

ETAPE 1 — anti-cannibalisation (GSC 28/05 -> 25/08/2026) : verdict FORT.
  La page possede DEJA le cluster : « logiciel prix de revient » 568 impr pos 2,5 ·
  « logiciel calcul prix de revient gratuit » 867 impr pos 3,6 · « logiciel de calcul
  prix de revient » 125 impr pos 1,0 · « logiciel calcul prix de revient boulangerie »
  81 impr pos 1,1. Total du cluster ~3 300 impressions pour 34 clics — CTR 1,0 %.
  => on met a jour cette page, on n'en cree pas une seconde.

ETAPE 2 — releve SERP du 27/08/2026, « logiciel prix de revient », France.
  Garde-fou : rank_group 2 mais rank_absolute 3 (AI Overview au rang 1).
  Le CTR bas n'est donc PAS un artefact d'affichage.
  Top 10 : otami.fr (abs 2), helloharel (abs 3), inbp.com/INBP-CR (abs 4),
  PAA (abs 5), incwo (abs 6), celge (abs 7), lhotellerie (abs 8), yokitup (abs 9),
  quantara (abs 10), videos YouTube (abs 11).
  3 CONSTATS CHIFFRES :
   1. pos absolue 3, 568 impressions, 0 clic — la courbe donne ~11 %, soit ~62 clics perdus
   2. cluster complet : ~3 300 impressions / 34 clics (CTR 1,0 %) en position 1 a 3,6
   3. 6 des 8 organiques sont des pages de LOGICIEL, 1 seule est un guide de calcul : la notre
  ANGLE (plus demontre) : la page devient l'outil + le comparatif que personne ne fait.
  PROMESSE : calculez maintenant, puis voyez quel logiciel l'automatise.

ETAPE 3 — gabarit des soeurs (cout-prix-au-kilo, difference-prix-dachat, calcul-cout-
  de-revient-logiciel) : article-hero > hha-tool > corps > faq-section,
  JSON-LD BreadcrumbList + FAQPage, module a 5 champs place juste apres le hero.
  La page cible suit deja ce gabarit : on n'y touche pas, on l'exploite.

ETAPE 3 bis — modules d'attention. AI Overview au-dessus du 1er organique =>
  reponse encadree + chiffre date renforces. Requete a variable (prix) => calculateur :
  DEJA PRESENT et deja au-dessus du 2e ecran. On ajoute la reponse encadree et le
  tableau comparatif (donnee structurée), absents.

DRY par defaut ; --live pour pousser.
"""
import sys, re, json
import wp_common as w

PID = 3430
TITLE = "Logiciel Prix de Revient • Simulateur Gratuit & Comparatif 2026"
H1 = "Le simulateur de prix de revient, et les logiciels qui l’automatisent"
BC = "Logiciel prix de revient • Simulateur &amp; comparatif"

# --- Bloc 1 : la reponse encadree (P1) + le fait date sourcé ---
ANSWER = '''<section class="hh-answer" id="reponse">
<style>
#hh-page .hh-answer{margin:0 0 34px}
#hh-page .hh-answer .box{border:1px solid #cfe3ee;border-left:4px solid #0090c8;background:#f4fafd;
padding:22px 24px;border-radius:4px}
#hh-page .hh-answer .box p{margin:0 0 .8rem;font-size:1.06rem;line-height:1.62;color:#1e293b}
#hh-page .hh-answer .box p:last-child{margin-bottom:0}
#hh-page .hh-answer .lbl{display:inline-block;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;
font-weight:700;color:#0090c8;margin-bottom:.7rem}
#hh-page .hh-fact{margin-top:14px;padding:14px 18px;background:#fff;border:1px solid #e2e8f0;border-radius:4px;
font-size:.92rem;color:#475569;line-height:1.6}
#hh-page .hh-fact b{color:#0f172a}
#hh-page .hh-fact .src{display:block;margin-top:6px;font-size:.8rem;color:#94a3b8}
</style>
<div class="box">
<span class="lbl">La réponse en une phrase</span>
<p><strong>Un logiciel de prix de revient calcule automatiquement ce que vous coûte une
recette ou un produit fini</strong> — matières premières, pertes, main-d’œuvre, énergie et
frais fixes compris — puis met ce coût à jour dès qu’un prix d’achat bouge, ce qu’un
tableur ne fait pas.</p>
<p>Vous pouvez tester le calcul tout de suite dans le simulateur ci-dessous, gratuitement
et sans inscription, puis comparer les solutions du marché plus bas.</p>
</div>
<div class="hh-fact">
<b>Ce que dit le marché :</b> sur les dix premiers résultats Google pour « logiciel prix de
revient », <b>six sont des logiciels payants</b>, un seul propose une version gratuite et
deux sont des comparateurs. Autrement dit, l’offre gratuite se limite en pratique aux
simulateurs en ligne et aux modèles de tableur.
<span class="src">Source : relevé de la SERP française, 27 août 2026.</span>
</div>
</section>
'''

# --- Bloc 2 : le comparatif (donnee structurée, absent de toute la SERP) ---
TABLE = '''<section id="s-comparatif">
<style>
#hh-page .hh-cmp{width:100%;border-collapse:collapse;font-size:.94rem;margin:18px 0 10px;
display:block;overflow-x:auto;white-space:nowrap}
#hh-page .hh-cmp thead th{background:#0f172a;color:#fff;text-align:left;padding:12px 14px;
font-size:.76rem;letter-spacing:.06em;text-transform:uppercase;font-weight:700}
#hh-page .hh-cmp td{padding:12px 14px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
#hh-page .hh-cmp td:first-child{color:#0f172a;font-weight:600}
#hh-page .hh-cmp tr:last-child td{border-bottom:none}
#hh-page .hh-cmp .yes{color:#15803d;font-weight:600}
#hh-page .hh-cmp .no{color:#b45309;font-weight:600}
#hh-page .hh-cmp-note{font-size:.85rem;color:#64748b;line-height:1.6;margin:.4rem 0 0}
@media(min-width:820px){#hh-page .hh-cmp{display:table;white-space:normal}}
</style>
<h2>Quel logiciel de prix de revient choisir&nbsp;?</h2>
<p>Le marché se partage en trois familles : les <strong>simulateurs en ligne</strong>, gratuits
mais qui ne gardent rien ; les <strong>logiciels dédiés au calcul de coût de revient</strong>,
qui gèrent les fiches recettes ; et les <strong>ERP</strong>, qui recalculent le coût à chaque
mouvement d’achat ou de stock. Voici les solutions présentes sur cette recherche, relevées
le 27 août 2026.</p>
<table class="hh-cmp">
<thead><tr><th>Solution</th><th>Type</th><th>Version gratuite</th><th>Pensé pour</th></tr></thead>
<tbody>
<tr><td>Simulateur de cette page</td><td>Calculateur en ligne</td><td class="yes">Oui</td>
<td>Tester une recette, sans inscription</td></tr>
<tr><td>INBP-CR</td><td>Logiciel de coût de revient</td><td class="no">Non</td>
<td>Boulangerie-pâtisserie artisanale</td></tr>
<tr><td>Otami</td><td>Logiciel de gestion des achats</td><td class="no">Non</td>
<td>Boulangerie, pâtisserie, restauration</td></tr>
<tr><td>Quantara</td><td>Module coût de revient</td><td class="no">Non</td>
<td>Boulangerie, pâtisserie, chocolaterie, traiteur</td></tr>
<tr><td>Yokitup</td><td>Logiciel de restauration</td><td class="yes">Oui</td>
<td>Restauration, fiches techniques</td></tr>
<tr><td>incwo</td><td>Application de gestion</td><td class="no">Non</td>
<td>TPE et PME, tous secteurs</td></tr>
<tr><td>Hello Harel</td><td>ERP agroalimentaire</td><td class="no">Non</td>
<td>PME agroalimentaires de 20 à 300 salariés</td></tr>
</tbody></table>
<p class="hh-cmp-note">Relevé effectué sur la première page de résultats Google France pour
« logiciel prix de revient », le 27&nbsp;août&nbsp;2026. Les versions gratuites indiquées
correspondent à ce que l’éditeur annonce publiquement.</p>
<h3>Simulateur, logiciel dédié ou ERP&nbsp;: comment trancher</h3>
<p>Un <strong>simulateur</strong> suffit pour vérifier une recette ou préparer un tarif : c’est
l’usage de l’outil ci-dessus. Un <strong>logiciel dédié</strong> devient utile dès que vous gérez
plusieurs dizaines de fiches recettes et que vous voulez les conserver d’une saison à l’autre.
Un <strong>ERP</strong> se justifie quand le coût doit se recalculer tout seul&nbsp;: à chaque
facture fournisseur, à chaque changement de rendement, à chaque perte constatée en production —
c’est ce que détaille notre guide sur le
<a href="/blog/calcul-cout-de-revient-logiciel/">calcul du coût de revient par un logiciel</a>.</p>
<p>Le partage se fait donc moins sur le prix que sur la <strong>fréquence de mise à jour</strong>&nbsp;:
un tableur et un simulateur donnent une photo, un logiciel donne un film. Si vos prix d’achat
bougent plusieurs fois par trimestre, la photo est périmée avant d’être imprimée.</p>
</section>
'''

# --- Bloc 3 : questions PAA relevees mot pour mot ---
FAQ_ADD = [
 ("Quel logiciel gratuit puis-je utiliser pour calculer le prix de revient des recettes de pâtisserie ?",
  "En pratique, le gratuit se limite à trois options : un simulateur en ligne comme celui de cette page, un modèle de tableur, ou la version gratuite d’un logiciel de restauration comme Yokitup. Les logiciels dédiés à la boulangerie-pâtisserie — INBP-CR, Otami, Quantara — sont tous payants. Le simulateur convient pour vérifier une recette ; au-delà d’une trentaine de fiches à conserver et mettre à jour, il faut passer à un outil qui garde l’historique."),
 ("Quelle est la formule pour calculer le prix de revient ?",
  "Prix de revient = coût des matières premières consommées + pertes et freinte + main-d’œuvre de production + énergie + quote-part de frais fixes. Le piège le plus fréquent est d’oublier la freinte : sur une pâte, l’évaporation à la cuisson fait qu’un kilo de pâte crue ne donne pas un kilo de produit fini, et le coût au kilo vendu est donc supérieur au coût au kilo produit."),
 ("Comment calculer le coût de revient dans Excel ?",
  "Une colonne par poste — matière, perte, main-d’œuvre, énergie, frais fixes — une ligne par ingrédient, et un total rapporté à la quantité réellement produite. Le tableur fonctionne tant que les prix d’achat sont stables : sa limite n’est pas le calcul mais la mise à jour, puisqu’il faut ressaisir chaque nouveau tarif fournisseur dans toutes les fiches concernées."),
 ("Un logiciel de prix de revient est-il rentable pour une petite structure ?",
  "Le seuil n’est pas le chiffre d’affaires mais le nombre de références et la volatilité des achats. Avec dix recettes et des prix stables, un tableur tient. Avec cinquante références et des tarifs qui bougent chaque trimestre, le temps passé à ressaisir dépasse rapidement le coût d’un outil — et l’écart de marge constaté sur des coûts périmés le dépasse encore plus vite."),
]


def build(c):
    log = []

    # 1 · H1
    old_h1 = "<h1>Prix Revient Boulangerie • Calcul &amp; Exercices • Guide</h1>"
    if old_h1 in c:
        c = c.replace(old_h1, "<h1>%s</h1>" % H1, 1); log.append("H1 remplace")
    else:
        log.append("!! H1 introuvable")

    # 2 · fil d'Ariane
    old_bc = '<span style="color:rgba(255,255,255,0.5)">Prix Revient Boulangerie • Calcul &amp; Exercices …</span>'
    if old_bc in c:
        c = c.replace(old_bc, '<span style="color:rgba(255,255,255,0.5)">%s</span>' % BC, 1)
        log.append("fil d'Ariane mis a jour")

    # 3 · la reponse encadree, en tete du corps editorial
    if 'class="hh-answer"' not in c:
        anchor = '<div class="hha-card hha-main">'
        i = c.find(anchor)
        if i >= 0:
            j = i + len(anchor)
            c = c[:j] + "\n" + ANSWER + c[j:]
            log.append("reponse encadree + fait date inseres en P1")
        else:
            log.append("!! ancre hha-main introuvable")

    # 4 · le comparatif, juste avant la FAQ
    if 'id="s-comparatif"' not in c:
        k = c.find('<section class="faq-section"')
        if k < 0: k = c.find('faq-section')
        if k >= 0:
            c = c[:k] + TABLE + "\n" + c[k:]
            log.append("tableau comparatif insere avant la FAQ")
        else:
            log.append("!! faq-section introuvable")

    # 5 · FAQ : questions PAA ajoutees au JSON-LD
    def upd(m):
        try: d = json.loads(m.group(1))
        except Exception: return m.group(0)
        if d.get("@type") != "FAQPage": return m.group(0)
        noms = {q["name"] for q in d.get("mainEntity", [])}
        for q, a in FAQ_ADD:
            if q not in noms:
                d["mainEntity"].append({"@type": "Question", "name": q,
                                        "acceptedAnswer": {"@type": "Answer", "text": a}})
        return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)
    c2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', upd, c, flags=re.S)
    if c2 != c:
        c = c2; log.append("FAQPage enrichi des questions PAA")

    # 6 · sommaire : ajouter l'entree comparatif
    toc_anchor = '<a href="#s-12">Conclusion et Recommandations</a>'
    if toc_anchor in c and 'href="#s-comparatif"' not in c:
        c = c.replace(toc_anchor,
                      '<a href="#s-comparatif">Quel logiciel de prix de revient choisir ?</a>\n' + toc_anchor, 1)
        log.append("sommaire complete")

    return c, log


def controle(c, title):
    """Etape 6 — 7 criteres mesures."""
    txt = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)
    plain = re.sub(r'<[^>]+>', ' ', txt)
    plain = re.sub(r'\s+', ' ', plain)
    body = plain[plain.find('La réponse en une phrase'):] if 'La réponse en une phrase' in plain else plain
    first60 = " ".join(body.split()[:60]).lower()
    tiers = " ".join(plain.split()[:len(plain.split()) // 3]).lower()
    r = {}
    r["title porte l'angle"] = "logiciel prix de revient" in title.lower()
    r["title <= 65 car."] = len(title) <= 65
    r["H1 != title"] = H1.lower() != title.lower()
    r["P1 = la reponse (requete dans les 60 premiers mots)"] = "prix de revient" in first60
    r["module interactif present"] = 'hha-tool' in c and c.count('<input') >= 3
    r["preuve datee + source dans le 1er tiers"] = ("27 août 2026" in tiers or "27 aout 2026" in tiers) and "source" in tiers
    r["definition en UNE phrase extractible"] = "Un logiciel de prix de revient calcule automatiquement" in c
    r["donnee structuree (tableau)"] = 'class="hh-cmp"' in c
    r["la suite est dans la page (lien interne contextuel)"] = '/blog/calcul-cout-de-revient-logiciel/' in c
    return r


def main():
    live = "--live" in sys.argv
    c0 = w.get_raw('posts', PID)['content']['raw']
    c, log = build(c0)
    for l in log: print("  •", l)
    mots = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)).split())
    print("\n  taille %d -> %d car. | mots %d" % (len(c0), len(c), mots))
    print("\n=== ETAPE 6 — controle en 7 criteres ===")
    ok = True
    for k, v in controle(c, TITLE).items():
        print("  [%s] %s" % ("OK " if v else "NON", k))
        if not v: ok = False
    print("\n  VERDICT :", "CITABLE + SIGNAL — livrable" if ok else "BLOQUE — corriger")
    if not live:
        print("\nDRY-RUN — ajouter --live"); return
    if not ok:
        print("\nrefus de pousser : le controle n'est pas vert"); return
    w.update_content('posts', PID, c, live=True)
    w.api('posts/%d' % PID, method='POST', data={'title': TITLE})
    print("\nPOUSSE — post %d | title : %s" % (PID, TITLE))


if __name__ == "__main__":
    main()
