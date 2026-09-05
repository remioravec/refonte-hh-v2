#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
/blog/erp-grossiste-distributeur/ (post 5269) — cible « erp pour distributeurs
de produits frais ». Applique le GABARIT BLOG valide le 27/08/2026.

RESERVE METHODOLOGIQUE — a lever des reconnexion des outils :
  Les etapes 1 (anti-cannibalisation GSC) et 2 (releve SERP date) n'ont PAS pu
  etre executees : les connecteurs Search Console et DataForSEO sont deconnectes
  de la session. Le choix des modules est donc HERITE du gabarit valide, il n'est
  pas derive de la SERP du jour. Aucune statistique de marche n'est affirmee :
  le chiffre mis en avant est un CALCUL, date, dont la methode et les variables
  sont exposees dans le simulateur — il est donc verifiable par le lecteur.
  A refaire des que GSC et DataForSEO repondent : releve de la SERP, questions
  du PAA mot pour mot, et verdict de cannibalisation.

DRY par defaut ; --live pour pousser.
"""
import sys, os, re, json
_G = "/home/user/refonte-hh-v2/deliverables-aout/contenu/gabarit"
sys.path.insert(0, _G if os.path.isdir(_G) else
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "gabarit"))
import gabarit_blog as G
import wp_common as w

PID = 5269
TITLE = "ERP pour Distributeurs de Produits Frais • DLC & Démarque"
H1 = "Ce que la démarque vous coûte vraiment, et comment un ERP la réduit"
DATE = "27 août 2026"

# ---------- valeurs de reference du calculateur (rendu sans JS deja juste) ----------
CA, DEM, MARGE = 100000.0, 8.0, 22.0
_pm = CA * DEM / 100
_pa = _pm * 12
_comp = _pa / (MARGE / 100)
def _g(x): return max(0.0, CA * (DEM - x) / 100 * 12)

CHAMPS = [
 ("frs-ca",    "CA mensuel en produits frais (€)", "%.0f" % CA, "100"),
 ("frs-dem",   "Taux de démarque (%)",             "%.1f" % DEM, "0.1"),
 ("frs-marge", "Taux de marge brute (%)",          "%.1f" % MARGE, "0.5"),
]

CALC = G.calculateur(
 titre="Calculateur du coût de la démarque",
 sous_titre="Produits périmés, invendus et casse, ramenés à l’année",
 champs=CHAMPS,
 unite="€ perdus par an",
 ref={"id": "frs-out", "label": "Perte annuelle sur produits frais",
      "valeur": G._fr(_pa, 0).replace(",", " "),
      "detail": [("frs-o-mois", "Perte mensuelle", G._fr(_pm, 0).replace(",", " ") + " €"),
                 ("frs-o-an", "Perte annuelle", G._fr(_pa, 0).replace(",", " ") + " €"),
                 ("frs-o-comp", "CA à réaliser pour la compenser",
                  G._fr(_comp, 0).replace(",", " ") + " €")]},
 note="Les valeurs affichées sont un exemple modifiable. Sans JavaScript, le calcul de "
      "référence reste lisible ci-dessus.",
 grille_titre="Gain annuel si la démarque tombe à",
 grille=[("frs-g6", G._fr(_g(6), 0).replace(",", " ") + " €", "6 %"),
         ("frs-g4", G._fr(_g(4), 0).replace(",", " ") + " €", "4 %"),
         ("frs-g2", G._fr(_g(2), 0).replace(",", " ") + " €", "2 %")])

# ---------- tableau : les familles d'outils, au niveau categorie ----------
OUI = '<span class="y">Oui</span>'; NON = '<span class="n">Non</span>'
PART = '<span class="n">Partiel</span>'
TABLE = G.tableau(
 colonnes=[("Type d’outil", True), ("DLC et rotation FEFO", True), ("Poids variable", True),
           ("Traçabilité par lot", True), ("Tournées et livraison", False), ("Pensé pour", False)],
 lignes=[
  ("0", ["Tableur", NON, NON, NON, NON, "Quelques références, produits secs"]),
  ("0", ["Gestion commerciale généraliste", NON, NON, PART, NON, "Négoce de produits stables"]),
  ("0", ["Logiciel de caisse / point de vente", NON, PART, NON, NON, "Vente au comptoir"]),
  ("1", ["WMS (gestion d’entrepôt)", OUI, PART, OUI, NON, "Logistique pure, sans facturation"]),
  ("1", ["ERP agroalimentaire", OUI, OUI, OUI, OUI, "Distributeurs de produits frais"]),
 ],
 filtres=[("all", "Tous"), ("1", "Adaptés au frais"), ("0", "Non adaptés")],
 tid="frs-tab")

# ---------- corps ----------
SECTIONS = [
 '<h2 id="s-frais">Ce que le frais change, et que les autres outils ignorent</h2>'
 '<p>Un distributeur de produits secs gère des références. Un distributeur de produits frais '
 'gère des <strong>lots qui perdent de la valeur chaque jour</strong>. C’est une différence de '
 'nature, pas de degré.</p>'
 '<p>Trois contraintes en découlent, et aucune n’est une option :</p>'
 '<h3>La date, portée par le lot et non par la référence</h3>'
 '<p>Deux palettes du même produit n’ont pas la même DLC. Un outil qui raisonne à la référence '
 'ne sait pas laquelle sortir en premier — et c’est exactement ce qui crée la démarque. La '
 'rotation doit se faire en <strong>FEFO</strong>, premier périmé premier sorti, pas en FIFO.</p>'
 '<h3>Le poids variable, de la réception à la facture</h3>'
 '<p>On commande vingt colis, on en reçoit vingt qui ne pèsent pas le poids annoncé. Si la '
 'facturation se fait au poids commandé, il faut émettre un avoir derrière. Si elle se fait au '
 '<strong>poids réellement pesé</strong>, le problème n’existe pas.</p>'
 '<h3>La traçabilité, exigible sans préavis</h3>'
 '<p>La question posée en contrôle est toujours la même : ce lot est parti où, et qu’y a-t-il '
 'dedans. Si la réponse suppose de rouvrir des bons papier, le périmètre du rappel s’élargit par '
 'précaution — et c’est ce qui coûte cher.</p>',

 '<h2 id="s-outils">Quel type d’outil pour un distributeur de produits frais</h2>'
 '<p>Le marché se partage en cinq familles. Elles ne se distinguent pas par leur prix mais par '
 'ce qu’elles savent modéliser : la date, le poids et le lot.</p>'
 + TABLE +
 '<p class="cap">Comparaison au niveau des familles d’outils, pas des éditeurs. Un « Partiel » '
 'signifie que la fonction existe mais suppose un développement spécifique ou un module '
 'complémentaire.</p>'
 '<p>Le partage utile n’est donc pas « logiciel gratuit ou payant » mais <strong>l’outil '
 'modélise-t-il la date et le poids, ou faut-il les rattraper à la main</strong>. Tout ce qui se '
 'rattrape à la main finit dans un tableur parallèle, et le tableau parallèle finit périmé.</p>',

 '<h2 id="s-seuil">Le seuil : à partir de quand un ERP se justifie</h2>'
 '<p>La rentabilité ne se calcule pas sur le prix de la licence mais sur la démarque évitée.</p>'
 '<div class="seuil">'
 '<div><b>Démarque sous 3 %</b><p>Rotation déjà maîtrisée, peu de références sensibles : un '
 'outil de gestion commerciale et une discipline d’inventaire suffisent.</p></div>'
 '<div><b>Démarque de 3 à 8 %</b><p>C’est la zone où l’ERP se rembourse le plus vite : chaque '
 'point de démarque récupéré vaut, sur l’exemple ci-dessus, douze mille euros par an.</p></div>'
 '<div><b>Démarque au-dessus de 8 %</b><p>Le problème n’est plus seulement l’outil : il faut '
 'aussi revoir les quantités d’achat et les fréquences de livraison. L’ERP rend le sujet '
 'mesurable, il ne le règle pas seul.</p></div>'
 '</div>'
 '<p>Le calcul complet est dans le simulateur : à 8 % de démarque sur 100 000 € de chiffre '
 'd’affaires mensuel, il faut réaliser <strong>plus de 430 000 € de ventes supplémentaires</strong> '
 'chaque année, à 22 % de marge, uniquement pour compenser la marchandise perdue.</p>'
 '<p>C’est ce rapport-là qui décide, pas le montant de l’abonnement. Le même raisonnement '
 's’applique au calcul du prix de revient, détaillé dans notre '
 '<a href="/blog/calculer-le-prix-de-revient-en-boulangerie/">guide du logiciel de prix de '
 'revient</a>.</p>',

 '<h2 id="s-erreurs">Les quatre erreurs qui coûtent le plus en produits frais</h2>'
 '<h3>1. Faire tourner le stock en FIFO plutôt qu’en FEFO</h3>'
 '<p>Premier entré premier sorti paraît logique, mais deux lots entrés le même jour n’ont pas la '
 'même date limite. C’est la première cause de démarque évitable.</p>'
 '<h3>2. Facturer au poids commandé</h3>'
 '<p>Chaque écart se rattrape ensuite en avoir, en litige, ou en marge silencieusement perdue '
 'parce que personne ne l’a repris.</p>'
 '<h3>3. Suivre la démarque en fin de mois</h3>'
 '<p>Un lot qui approche de sa date se vend encore — quinze jours plus tard, il se jette. La '
 'valeur de l’alerte tient entièrement à son avance.</p>'
 '<h3>4. Acheter sur l’historique plutôt que sur la rotation réelle</h3>'
 '<p>Commander la même quantité chaque semaine sur un produit dont la rotation a changé, c’est '
 'programmer l’invendu. La donnée existe déjà dans les sorties de stock : encore faut-il que '
 'l’outil la restitue.</p>',
]

FAQ = [
 ("Qu’est-ce qu’un ERP pour distributeurs de produits frais ?",
  "C’est un logiciel de gestion qui pilote l’achat, le stock, la préparation, la livraison et la facturation en modélisant nativement trois contraintes du frais : la DLC portée par le lot, le poids variable et la traçabilité de l’origine. Un ERP généraliste sait faire le reste, mais rattrape ces trois-là par développement spécifique."),
 ("Comment un ERP réduit-il la démarque ?",
  "Par trois mécanismes cumulés : la rotation en FEFO qui sort d’abord le lot le plus proche de sa date, l’alerte avant péremption qui laisse le temps d’écouler ou de déclasser, et la remise ciblée sur les lots concernés plutôt que sur la référence entière. Le simulateur ci-dessus chiffre ce que vaut chaque point de démarque récupéré."),
 ("Quelle différence entre FIFO et FEFO ?",
  "FIFO sort le lot entré en premier, FEFO sort celui qui périme en premier. Sur des produits stables les deux se confondent ; sur du frais, deux lots reçus le même jour peuvent avoir plusieurs jours d’écart de DLC. C’est précisément cet écart qui devient de la démarque quand la rotation est faite en FIFO."),
 ("Le poids variable est-il vraiment un sujet en distribution ?",
  "Oui, dès que vous vendez de la viande, du poisson, de la crémerie à la coupe ou des fruits et légumes en vrac. Le bon de pesée, l’étiquette et la facture doivent sortir de la même donnée, sinon les trois documents divergent et les avoirs s’accumulent."),
 ("Faut-il un WMS ou un ERP ?",
  "Un WMS optimise l’entrepôt : emplacements, préparation, inventaire. Il ne facture pas, ne calcule pas la marge et ne gère pas l’achat. Pour un distributeur, les deux sujets sont liés — c’est pourquoi un ERP métier qui embarque la logistique évite l’interface entre deux outils."),
 ("Combien de temps dure la mise en place ?",
  "Comptez 4 à 8 semaines entre le cadrage et la bascule, reprise des données comprise, sur un périmètre de distribution alimentaire. Le facteur qui allonge un projet n’est presque jamais le logiciel mais la disponibilité des données de départ : catalogue, tarifs clients et encours."),
 ("Peut-on démarrer sur une partie du périmètre ?",
  "Oui, et c’est souvent le bon choix : démarrer sur la réception et le stock, là où se crée la démarque, puis brancher la vente et la facturation une fois les données propres."),
]

CFG = {
 "cible": "distributeurs de produits frais",
 "cible_courte": "produits frais",
 "title": TITLE,
 "date_courte": "27 août 2026",
 "champs": CHAMPS,
 "reponse": "<strong>Un ERP pour distributeurs de produits frais pilote la marchandise par le "
            "lot et par la date</strong>, pas seulement par la référence : rotation en premier "
            "périmé premier sorti, poids réellement pesé, et traçabilité de l’origine jusqu’au "
            "client livré.",
 "promesse": "Chiffrez ce que votre démarque vous coûte réellement dans le simulateur ci-dessous, "
             "puis comparez les familles d’outils du marché.",
 "fait_chiffre": "96 000 €",
 "fait_texte": "Sur 100 000 € de chiffre d’affaires mensuel en produits frais, une démarque de "
               "8 % représente <strong>96 000 € de marchandise perdue par an</strong> — et il faut "
               "réaliser plus de 430 000 € de ventes supplémentaires, à 22 % de marge, uniquement "
               "pour la compenser.",
 "fait_source": "Source : calcul du 27 août 2026, méthode et variables exposées dans le "
                "simulateur ci-dessous — le résultat est reproductible avec vos propres chiffres.",
 "calc_id": "s-calcul",
 "calc_h2": "Chiffrez votre démarque",
 "calc_intro": "Renseignez vos trois chiffres : la perte annuelle et le chiffre d’affaires "
               "nécessaire pour la compenser se recalculent à chaque frappe. Aucune donnée n’est "
               "envoyée ni enregistrée.",
 "calc_html": CALC,
 "sommaire": [("s-calcul", "Chiffrez votre démarque"),
              ("s-frais", "Ce que le frais change"),
              ("s-outils", "Quel type d’outil choisir"),
              ("s-seuil", "Le seuil de rentabilité"),
              ("s-erreurs", "Les quatre erreurs qui coûtent le plus"),
              ("s-faq", "Les questions fréquentes")],
 "sections": SECTIONS,
 "faq": FAQ,
 "suite": [
  ("/blog/logiciel-grossiste-alimentaire/", "Logiciel grossiste alimentaire",
   "Le panorama complet des fonctions attendues par un grossiste."),
  ("/fonctionnalites/gestion-de-stock/", "La gestion de stock multi-dépôts",
   "Transit, réservé, disponible : les trois états du stock."),
  ("/fonctionnalites/tracabilite-alimentaire/", "La traçabilité alimentaire par lot",
   "Remonter et redescendre la chaîne en quelques minutes."),
  ("/blog/calculer-le-prix-de-revient-en-boulangerie/", "Le logiciel de prix de revient",
   "Le simulateur et le comparatif des solutions du marché."),
 ],
 "js": """
<script>
(function(){
  var ids=['frs-ca','frs-dem','frs-marge'], el={};
  for(var i=0;i<ids.length;i++){el[ids[i]]=document.getElementById(ids[i]);}
  if(!el['frs-ca']) return;
  function f(n){return Math.round(n).toLocaleString('fr-FR');}
  function set(id,v){var e=document.getElementById(id); if(e) e.innerHTML=v;}
  function calc(){
    var ca=parseFloat(el['frs-ca'].value)||0,
        d =parseFloat(el['frs-dem'].value)||0,
        m =parseFloat(el['frs-marge'].value)||0;
    if(d>100) d=100; if(m<=0) m=1; if(m>100) m=100;
    var pm=ca*d/100, pa=pm*12, comp=pa/(m/100);
    set('frs-o-mois',f(pm)+' €'); set('frs-o-an',f(pa)+' €'); set('frs-o-comp',f(comp)+' €');
    set('frs-out',f(pa)+'&nbsp;<small>€ perdus par an</small>');
    [[6,'frs-g6'],[4,'frs-g4'],[2,'frs-g2']].forEach(function(p){
      var g=Math.max(0, ca*(d-p[0])/100*12); set(p[1], f(g)+' €');
    });
  }
  for(var k in el){ if(el[k]) el[k].addEventListener('input',calc); }
  calc();
  var tab=document.getElementById('frs-tab'); if(!tab) return;
  var tb=tab.querySelector('tbody');
  tab.querySelectorAll('thead th button').forEach(function(b){
    b.addEventListener('click',function(){
      var c=+b.dataset.c, th=b.parentNode, asc=th.getAttribute('aria-sort')!=='ascending';
      tab.querySelectorAll('thead th').forEach(function(x){x.setAttribute('aria-sort','none');});
      th.setAttribute('aria-sort',asc?'ascending':'descending');
      var rows=[].slice.call(tb.querySelectorAll('tr'));
      rows.sort(function(x,y){
        var a=x.children[c].textContent.trim().toLowerCase(), d2=y.children[c].textContent.trim().toLowerCase();
        return (a<d2?-1:a>d2?1:0)*(asc?1:-1);
      });
      rows.forEach(function(r){tb.appendChild(r);});
    });
  });
  document.querySelectorAll('.pri .chip').forEach(function(c){
    c.addEventListener('click',function(){
      document.querySelectorAll('.pri .chip').forEach(function(x){x.setAttribute('aria-pressed','false');});
      c.setAttribute('aria-pressed','true');
      var v=c.dataset.f;
      tb.querySelectorAll('tr').forEach(function(r){ r.style.display=(v==='all'||r.dataset.g===v)?'':'none'; });
    });
  });
})();
</script>""",
}


def remplacer_corps(c, inner):
    open_tag = '<div class="hha-card hha-main">'
    i = c.find(open_tag); j = c.find('<section class="faq-section"')
    if i < 0 or j < 0 or j <= i: raise SystemExit("bornes du corps introuvables")
    sl = c[i:j]
    o, f = len(re.findall(r'<div[\s>]', sl)), len(re.findall(r'</div>', sl))
    delta = o - f
    # Dans ce gabarit, hha-main enveloppe AUSSI la faq-section : la tranche doit
    # donc laisser exactement 1 div ouvert. delta==0 signale un </div> orphelin
    # (defaut rencontre sur le post 3430) — on le corrige en passant.
    if delta not in (0, 1):
        raise SystemExit("tranche inattendue : %d ouvrants / %d fermants" % (o, f))
    if delta == 0:
        print("  note : un </div> orphelin etait present, il est corrige")
    return c[:i] + open_tag + "\n" + inner + "\n\n" + c[j:], len(sl)


def main():
    live = "--live" in sys.argv
    html = G.rendre(CFG)
    c0 = w.get_raw('posts', PID)['content']['raw']
    c, removed = remplacer_corps(c0, html)
    # sommaires lateraux
    NEW = "\n" + "".join('<a href="#%s">%s</a>\n' % (i, t) for i, t in CFG["sommaire"])
    c = re.sub(r'(<nav class="hha-toc">).*?(</nav>)', lambda m: m.group(1) + NEW + m.group(2), c, flags=re.S)
    mots = len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', '', c, flags=re.S)).split())
    print("corps : %d car. retires, %d poses | page %d -> %d | mots %d"
          % (removed, len(html), len(c0), len(c), mots))
    d = 0
    for m in re.finditer(r'<div[\s>]|</div>', c): d += -1 if m.group(0).startswith('</') else 1
    print("profondeur div finale : %d %s" % (d, "OK" if d == 0 else "<-- DESEQUILIBRE"))
    orph = re.findall(r'href="#s-\d+"', c)
    print("ancres orphelines :", len(orph))
    print("\n=== controle (7 criteres du skill) ===")
    ok = True
    for k, v in G.controle(html, CFG).items():
        print("  [%s] %s" % ("OK " if v else "NON", k)); ok = ok and v
    print("\n  VERDICT :", "livrable" if ok else "BLOQUE")
    if not live: print("\nDRY-RUN — ajouter --live"); return
    if not ok or d != 0: print("refus de pousser"); return
    w.update_content('posts', PID, c, live=True)
    w.api('posts/%d' % PID, method='POST', data={'title': TITLE})
    print("\nPOUSSE — post %d | title : %s" % (PID, TITLE))


if __name__ == "__main__":
    main()
