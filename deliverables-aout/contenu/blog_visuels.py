#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Des images sous les H2, et un appel a l'action qui parle au lecteur.

LES IMAGES viennent de la mediatheque, jamais d'ailleurs. Elles sont
choisies par le sujet du H2 : un titre qui parle de tracabilite recoit la
photo de palettes codes-barres, un titre qui parle de dates recoit la
capture du tableau de bord FEFO. Le texte alternatif est celui de la
mediatheque, ecrit par l'equipe — on ne le reinvente pas.

Une image n'est posee que si le titre correspond a un theme connu. Aucune
illustration par defaut : une photo de hasard sous un titre est pire que
pas de photo.

L'APPEL A L'ACTION suit ce que Remi demande : le client doit se
reconnaitre. Une image, le probleme tel qu'il le vit, la reponse ensuite.
Le probleme n'est pas invente : il est tire de ce que l'article decrit
lui-meme.
"""

BASE = "https://www.helloharel.com/wp-content/uploads/"

# theme -> (fichier, texte alternatif, legende)
VISUELS = {
 "tracabilite": ("2026/08/erp-negoce-tracabilite-lots.webp",
   "Palettes identifiées par codes-barres dans un entrepôt alimentaire",
   "Chaque palette porte son identifiant : c'est ce qui rend un lot retrouvable."),
 "dates": ("2026/09/hh-erp-stock-fefo-peremption.webp",
   "Tableau de bord Stock de Hello Harel : suivi des dates de péremption",
   "Les lots proches de leur date remontent d'eux-mêmes, avant la perte."),
 "stock": ("2026/08/erp-negoce-stocks-multi-depots.webp",
   "Magasinier scannant les références dans un entrepôt",
   "Un stock se tient à la référence et au lot, pas au ressenti."),
 "erp": ("2025/03/Hello-Harel-Gestion-des-stocks.png",
   "Interface de gestion des stocks de Hello Harel",
   "L'écran de gestion des stocks de Hello Harel."),
 "production": ("2026/09/erp-pme-agroalimentaire-atelier-operatrices.webp",
   "Deux opératrices en charlotte et blouse dans un atelier agroalimentaire",
   "En atelier, ce qui n'est pas enregistré au moment même est perdu."),
 "reception": ("2026/08/erp-import-export-quai-reception.webp",
   "Chariot élévateur déchargeant un camion sur un quai de réception",
   "La réception est le premier maillon : c'est là que le lot entre dans la chaîne."),
 "vente": ("2026/08/erp-negoce-alimentaire-televente.webp",
   "Télévendeur avec casque prenant une commande",
   "La prise de commande décide de ce que l'atelier devra produire."),
 "cout": ("2026/09/hh-erp-catalogue-tarifs-marge.webp",
   "Catalogue tarifaire Hello Harel avec les marges par référence",
   "La marge se lit par référence, pas sur une moyenne."),
 "achat": ("2026/08/erp-negoce-achats-approvisionnements.webp",
   "Opérateur logistique vérifiant une commande fournisseur",
   "Un approvisionnement se déclenche sur un seuil, pas sur une rupture."),
 "gms": ("2026/09/erp-negoce-alimentaire-marche-de-gros.webp",
   "Déchargement de cagettes depuis un camion sur un marché de gros",
   "Les enseignes imposent leurs délais : la DLC résiduelle se joue ici."),
 "qualite": ("2026/09/erp-conserverie-ligne-conditionnement.webp",
   "Opératrices en tenue sur une ligne de conditionnement",
   "Les contrôles se consignent au fil de la ligne, pas après coup."),
}

# les mots qui rattachent un titre a un theme, du plus precis au plus large
THEMES = [
 ("dates", ["dlc", "ddm", "dluo", "peremption", "fefo", "fifo", "rotation",
            "date limite", "durabilite"]),
 ("tracabilite", ["tracabilite", "tracer", "lot", "rappel", "origine",
                  "ascendante", "descendante"]),
 ("gms", ["gms", "grande distribution", "enseigne", "distributeur",
          "cahier des charges"]),
 ("qualite", ["haccp", "qualite", "controle", "conformite", "sanitaire",
              "inco", "etiquetage", "allergene"]),
 ("cout", ["cout", "marge", "prix de revient", "rentabilite", "tarif",
           "facturation", "perte"]),
 ("stock", ["stock", "entrepot", "inventaire", "depot", "reassort", "seuil"]),
 ("production", ["production", "fabrication", "atelier", "recette",
                 "nomenclature", "planification", "ordonnancement"]),
 ("achat", ["achat", "fournisseur", "approvisionnement", "commande fournisseur"]),
 ("vente", ["vente", "commande", "client", "televente", "devis", "crm"]),
 ("reception", ["reception", "livraison", "quai", "logistique", "expedition",
                "transport"]),
 ("erp", ["erp", "logiciel", "solution", "module", "outil", "hello harel"]),
]


def sans_accent(t):
    for a, b in zip("éèêëàâäçôöûüùîïÿ", "eeeeaaacoouuuiiy"):
        t = t.replace(a, b)
    return t.lower()


def themes_du_titre(titre):
    """Tous les themes qu'un titre evoque, du plus precis au plus large."""
    t = sans_accent(titre)
    return [nom for nom, mots in THEMES if any(m in t for m in mots)]


def theme_du_titre(titre):
    L = themes_du_titre(titre)
    return L[0] if L else None


def repartir(titres, maxi=4):
    """Attribue une image par titre, SANS jamais repeter la meme.

    Sur un article de tracabilite, « DLC » apparait dans presque tous les
    H2 : sans cette regle, les sept sections recevraient la meme photo, ce
    qui revient a tapisser plutot qu'a illustrer. Un titre dont tous les
    themes sont deja pris ne recoit pas d'image — mieux vaut aucune image
    qu'une image de hasard.
    """
    pris, sortie = set(), []
    for t in titres:
        choisi = None
        if len(pris) < maxi:
            for th in themes_du_titre(t):
                if th not in pris:
                    choisi = th
                    pris.add(th)
                    break
        sortie.append(choisi)
    return sortie


def figure(theme, cote=""):
    f, alt, leg = VISUELS[theme]
    return ('<figure class="hhb-img%s">'
            '<img src="%s%s" alt="%s" loading="lazy" decoding="async" '
            'width="1200" height="630">'
            '<figcaption>%s</figcaption></figure>' % (cote, BASE, f, alt, leg))


# ══════════════════════════════════════════════════════ l'appel a l'action
#
# « Le client doit se reconnaitre. Image. Probleme, solution. »
# Le probleme est celui que l'article decrit ; on ne lui en invente pas un.

ACCROCHES = {
 "tracabilite": (
   "2026/09/erp-pme-agroalimentaire-atelier-operatrices.webp",
   "Deux opératrices en charlotte et blouse dans un atelier agroalimentaire",
   "Le contrôleur est là. Il demande où est parti le lot 2409-114.",
   "Vous ouvrez trois classeurs, vous rappelez un fournisseur, vous recoupez "
   "des bons de livraison. Pendant ce temps, l'horloge tourne.",
   "Avec Hello Harel, la chaîne complète d'un lot — d'où il vient, où il est "
   "parti, qui a été livré — se sort à l'écran. Le dossier est prêt avant que "
   "la question suivante arrive."),
 "dates": (
   "2026/08/erp-negoce-entrepot-cagettes-hd.webp",
   "Cagettes de produits frais rangées en entrepôt",
   "Vous découvrez la palette périmée le jour où vous la cherchez.",
   "Les dates vivent dans un tableur que personne n'ouvre le matin. Ce qui "
   "devait partir en promotion part à la benne.",
   "Hello Harel fait remonter les lots proches de leur date avant qu'il soit "
   "trop tard, et sert les stocks dans l'ordre des péremptions."),
 "stock": (
   "2026/09/erp-negoce-magasinier-entrepot-alimentaire.webp",
   "Magasinier conduisant un transpalette en entrepôt alimentaire",
   "Le stock du logiciel dit une chose, l'entrepôt en dit une autre.",
   "On recompte, on corrige à la main, on recommence le mois suivant. Et on "
   "commande ce qu'on avait déjà.",
   "Hello Harel tient le stock à la référence, au lot et à l'emplacement, "
   "mis à jour à chaque réception et à chaque sortie."),
 "cout": (
   "2026/08/erp-negoce-ventes-devis-commandes.webp",
   "Tablette affichant un tableau de bord commercial",
   "Vous connaissez votre chiffre. Votre marge, beaucoup moins.",
   "Le prix de revient est calculé une fois par an dans un classeur, et les "
   "cours ont bougé depuis. Certaines références se vendent à perte sans "
   "qu'on le sache.",
   "Hello Harel recalcule le prix de revient à chaque réception et affiche la "
   "marge référence par référence."),
 "production": (
   "2026/09/erp-pme-agroalimentaire-atelier-operatrices.webp",
   "Deux opératrices en charlotte et blouse dans un atelier agroalimentaire",
   "Le planning de l'atelier tient sur un tableau blanc.",
   "Une commande urgente arrive, tout est à refaire à la main. Les besoins "
   "matière se découvrent le matin même.",
   "Hello Harel calcule les besoins depuis le plan de production et affiche "
   "la charge de l'atelier avant de lancer."),
 "defaut": (
   "2026/09/erp-pme-agroalimentaire-atelier-operatrices.webp",
   "Deux opératrices en charlotte et blouse dans un atelier agroalimentaire",
   "Votre gestion tient dans des fichiers que vous êtes seul à comprendre.",
   "Chaque question demande une recherche, chaque contrôle une reconstitution. "
   "Le temps passé là n'est pas passé à produire.",
   "Hello Harel réunit stocks, lots, production et marges au même endroit, "
   "pour les PME de l'agroalimentaire."),
}


def bloc_accroche(theme, lien_demo, lien_contact):
    img, alt, pb_t, pb_d, sol = ACCROCHES.get(theme, ACCROCHES["defaut"])
    return (
     '<section class="hhb-acc">'
     '<div class="hhb-acc-img"><img src="%s%s" alt="%s" loading="lazy" '
     'decoding="async" width="1200" height="800"></div>'
     '<div class="hhb-acc-txt">'
     '<p class="hhb-acc-eti">Le problème</p>'
     '<p class="hhb-acc-pb">%s</p>'
     '<p class="hhb-acc-d">%s</p>'
     '<p class="hhb-acc-eti hhb-acc-eti2">La réponse</p>'
     '<p class="hhb-acc-sol">%s</p>'
     '<div class="hhb-acc-b">'
     '<a class="hhb-b" href="%s">Voir Hello Harel sur vos données →</a>'
     '<a class="hhb-b hhb-b2" href="%s">Poser une question →</a>'
     '</div></div></section>' % (BASE, img, alt, pb_t, pb_d, sol,
                                 lien_demo, lien_contact))


# ══════════════════════════════════════════════════════ la feuille
CSS = """<style id="hh-blog-visuels">
/* ── les images sous les H2 ─────────────────────────────────────────── */
.hhb-img,#hh-page .hhb-img{margin:0 0 1.6rem !important;padding:0 !important;
 max-width:var(--mes,68ch) !important}
.hhb-img img,#hh-page .hhb-img img{display:block !important;width:100% !important;
 height:auto !important;aspect-ratio:16/8 !important;object-fit:cover !important;
 border-radius:16px !important;margin:0 !important;background:#EEF2F7 !important}
.hhb-img figcaption,#hh-page .hhb-img figcaption{margin:.6rem 0 0 !important;
 padding:0 0 0 .8rem !important;border-left:3px solid #BAE6FD !important;
 color:#64748b !important;font-size:.86rem !important;line-height:1.55 !important;
 font-style:normal !important}

/* ── l'accroche : image a gauche, probleme puis reponse a droite ─────── */
.hhb-acc,#hh-page .hhb-acc{margin:2.8rem auto 0 !important;
 max-width:var(--mes,68ch) !important;
 display:grid !important;grid-template-columns:1fr !important;gap:0 !important;
 background:#fff !important;border:1px solid #e2e8f0 !important;
 border-radius:22px !important;overflow:hidden !important;
 box-shadow:0 18px 44px -34px rgba(15,23,42,.6) !important}
@media (min-width:760px){
 .hhb-acc,#hh-page .hhb-acc{grid-template-columns:minmax(0,38%) minmax(0,1fr) !important}}
.hhb-acc-img,#hh-page .hhb-acc-img{margin:0 !important;min-height:190px !important;
 background:#EEF2F7 !important}
.hhb-acc-img img,#hh-page .hhb-acc-img img{display:block !important;
 width:100% !important;height:100% !important;min-height:190px !important;
 object-fit:cover !important;margin:0 !important;border-radius:0 !important}
.hhb-acc-txt,#hh-page .hhb-acc-txt{padding:1.6rem 1.5rem 1.5rem !important}
.hhb-acc .hhb-acc-eti,#hh-page .hhb-acc .hhb-acc-eti{margin:0 0 .35rem !important;
 font-size:.72rem !important;font-weight:800 !important;letter-spacing:.11em !important;
 text-transform:uppercase !important;color:#BE123C !important}
.hhb-acc .hhb-acc-eti2,#hh-page .hhb-acc .hhb-acc-eti2{color:#15803D !important;
 margin-top:1.3rem !important}
.hhb-acc .hhb-acc-pb,#hh-page .hhb-acc .hhb-acc-pb{margin:0 0 .5rem !important;
 font-size:1.16rem !important;font-weight:800 !important;line-height:1.32 !important;
 color:#0f172a !important}
.hhb-acc .hhb-acc-d,#hh-page .hhb-acc .hhb-acc-d{margin:0 !important;color:#475569 !important;
 font-size:.97rem !important;line-height:1.66 !important}
.hhb-acc .hhb-acc-sol,#hh-page .hhb-acc .hhb-acc-sol{margin:0 !important;color:#334155 !important;
 font-size:1rem !important;line-height:1.68 !important}
.hhb-acc-b,#hh-page .hhb-acc-b{display:flex !important;flex-wrap:wrap !important;
 gap:.6rem !important;margin-top:1.35rem !important}
.hhb-acc .hhb-b,#hh-page .hhb-acc .hhb-b{display:inline-flex !important;
 align-items:center !important;padding:.72rem 1.3rem !important;
 border-radius:999px !important;background:#0369A1 !important;color:#fff !important;
 font-weight:700 !important;font-size:.93rem !important;
 text-decoration:none !important;margin:0 !important}
.hhb-acc .hhb-b2,#hh-page .hhb-acc .hhb-b2{background:#fff !important;
 color:#0369A1 !important;border:1.5px solid #0369A1 !important}
@media (max-width:760px){
 .hhb-acc-txt,#hh-page .hhb-acc-txt{padding:1.35rem 1.2rem 1.3rem !important}
 .hhb-acc .hhb-acc-pb,#hh-page .hhb-acc .hhb-acc-pb{font-size:1.1rem !important}
 .hhb-acc .hhb-b,#hh-page .hhb-acc .hhb-b{width:100% !important;
  justify-content:center !important}}
</style>"""
