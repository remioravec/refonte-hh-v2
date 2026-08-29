# -*- coding: utf-8 -*-
"""
Contenu de la variante B — repris de la variante A (page 11493) sans reecriture.

Regle du test : une seule variable change entre A et B, l'UX. Le fond reste
identique, mot pour mot partout ou la mise en page le permet ; les seules
transformations sont des mises en puces de paragraphes deja presents dans A.
"""

BADGE = "Import Export Alimentaire"

H1_MOTS = ["Le", "prix", "payé", "au", "fournisseur", "n'est", "jamais", "<em>votre&nbsp;coût.</em>"]

HERO_TICKS = [
    "Répartissez le <b>fret, la douane, l'assurance et le change</b> sur chaque référence",
    "Distinguez le stock <b>en transit, sous douane et disponible</b>",
    "Gérez le <b>poids variable, les DLC et le lot d'origine</b>",
    "Lisez la <b>marge par conteneur, par client et par référence</b>",
]

HERO_REASSURE = "Édité en France depuis 2014. Démonstration de 30 minutes, sans engagement."

PREUVE = ("Rejoignez les <b>+200 entreprises agroalimentaires</b> qui pilotent leurs "
          "opérations avec Hello Harel")

STATS = [
    ("200+",     "entreprises agroalimentaires équipées"),
    ("5,0/5",    "sur 31 avis clients"),
    ("2014",     "édité en France depuis"),
    ("4–8 sem.", "du cadrage à la bascule"),
]

# --------------------------------------------------------------------- onglets
# Chaque onglet condense en puces les paragraphes du § 02 de la variante A.
ICONES = {
 "euro": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8V7m0 1v8m0 0v1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
 "boite": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>',
 "feuille": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>',
 "graph": '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m4 10v-6m4 6V9M5 21h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v14a2 2 0 002 2z"/>',
}

ONGLETS = [
    {
        "cle": "cout", "onglet": "Coût de revient", "icone": "euro", "img": "cout",
        "h2": "Le coût de revient réel, calculé à la réception",
        "ticks": [
            "Fret, assurance, droits de douane, frais de dossier et transitaire "
            "<b>répartis sur chaque référence du conteneur</b>",
            "Répartition <b>au poids, à la valeur ou au volume</b>, selon ce qui est juste "
            "pour la marchandise",
            "Multi-devises : chaque opération porte <b>son taux à la date de l'événement</b>",
            "L'écart de change constaté au règlement est <b>enregistré séparément</b>, "
            "au lieu d'être noyé dans la marge",
        ],
        "lien": ("/fonctionnalites/import-export/", "Voir le module import export"),
    },
    {
        "cle": "stock", "onglet": "Stock et douane", "icone": "boite", "img": "stock",
        "h2": "Trois états, trois réalités",
        "ticks": [
            "<b>En transit</b> : partie du fournisseur, pas encore arrivée — un engagement, "
            "pas du stock, avec sa date d'arrivée prévue",
            "<b>Sous douane</b> : arrivée mais pas dédouanée, donc pas vendable",
            "<b>Disponible</b> : ce que vous pouvez réellement engager",
            "Liasse documentaire <b>contrôlée à chaque étape</b>, avant de découvrir la pièce "
            "manquante quand le conteneur est déjà à quai",
        ],
        "lien": ("/negoce/stocks-multi-depots/", "Découvrir les stocks multi-dépôts"),
    },
    {
        "cle": "alim", "onglet": "Marchandise alimentaire", "icone": "feuille", "img": "alim",
        "h2": "Ce sur quoi un logiciel d'import généraliste s'arrête",
        "ticks": [
            "Lot d'origine, pays de provenance, <b>numéro d'agrément</b> et certificats "
            "sanitaires attachés au lot",
            "DLC portée par le lot : rotation <b>FEFO</b>, alertes avant péremption et remise "
            "ciblée sur les lots qui approchent",
            "<b>Poids variable natif</b> : bon de pesée, étiquette et facture sortent de la "
            "même donnée",
            "En cas de rappel, la liste des clients concernés s'obtient <b>en quelques "
            "minutes</b>, sans rouvrir de classeur",
        ],
        "lien": ("/negoce/tracabilite-lots/", "Découvrir la traçabilité des lots"),
    },
    {
        "cle": "marge", "onglet": "Marge", "icone": "graph", "img": "marge",
        "h2": "Quelles opérations gagnent de l'argent",
        "ticks": [
            "Marge lue <b>par conteneur, par référence, par client et par commercial</b>",
            "Calculée sur le <b>coût de revient réel</b>, pas sur un coût estimé",
            "Arrêter une ligne de produits qui coûte plus qu'elle ne rapporte redevient "
            "<b>un arbitrage possible</b>",
        ],
        "lien": ("/negoce/tarifs-reporting-edi/", "Voir les tarifs, reporting et EDI"),
    },
]

# --------------------------------------------------------------------- calcul
CALC_TITRE = "Sur un conteneur, l'écart dépasse 20 %."
CALC_INTRO = ("Tant que la répartition des frais d'approche se fait dans un tableur, après "
              "coup, la marge inscrite sur vos factures est une estimation. Voici le calcul, "
              "poste par poste.")
CALC_CARTE = "Conteneur 20 pieds — exemple"
CALC_LIGNES = [
    ("Marchandise, prix fournisseur", "32 000 €"),
    ("Fret maritime", "2 400 €"),
    ("Assurance transport", "310 €"),
    ("Droits de douane", "2 560 €"),
    ("Transitaire, frais de dossier", "640 €"),
    ("Écart de change au règlement", "480 €"),
]
CALC_TOTAL = ("Coût de revient réel", "38 390 €")
CALC_COEF = ("Coefficient appliqué", "× 1,20")
CALC_NOTE = ("Exemple illustratif. Les postes et la clé de répartition — au poids, à la valeur "
             "ou au volume — se paramètrent par type d'opération.")
CALC_WARN = [
    "Vendre à <b>+15 % du prix fournisseur</b>, sur cet exemple, c'est vendre <b>à perte</b>. "
    "C'est l'erreur la plus fréquente du négoce à l'import, et elle ne se voit pas ligne à "
    "ligne : elle se voit à la fin du trimestre, quand la marge globale ne correspond plus aux "
    "marges affichées.",
    "Hello Harel applique le coefficient <b>à la réception</b>, référence par référence. La "
    "marge se lit ensuite par conteneur, par client et par référence — pas seulement en cumul.",
]

# --------------------------------------------------------------------- terrain
TERRAIN_TITRE = "L'outil ne vit pas dans un bureau."
TERRAIN_INTRO = ("Il vit sur le quai, au contrôle et à la préparation. C'est là qu'il fait "
                 "gagner du temps — ou qu'il en fait perdre.")
TERRAIN = [
    ("À la réception", "Pesée, contrôle de température et affectation du lot dès le quai, "
                       "sur terminal mobile."),
    ("Au contrôle", "Agréage, écarts constatés et photos rattachés au lot, opposables au "
                    "fournisseur."),
    ("À la préparation", "Picking en FEFO, poids réel saisi à la pesée, bon de livraison "
                         "édité dans la foulée."),
]

# --------------------------------------------------------------------- comparatif
CMP_TITRE = "Trois outils, trois problèmes différents."
CMP_INTRO = ("La confusion est fréquente parce que les trois parlent d'import-export. Un TMS "
             "sait où est la marchandise ; un ERP métier sait ce qu'elle coûte et ce qu'elle "
             "rapporte.")
CMP_COLS = ["Ce que vous cherchez", "TMS / transitaire", "ERP généraliste", "Hello Harel"]
CMP_LIGNES = [
    ("Suivre l'acheminement", "oui, c'est son métier", "non", "oui, dates et statuts"),
    ("Répartir les frais d'approche", "non", "développement spécifique", "natif, à la réception"),
    ("Stock sous douane vs vendable", "partiel", "non", "trois états distincts"),
    ("Poids variable", "non", "développement spécifique", "natif"),
    ("DLC et rotation FEFO", "non", "non", "natif, avec alertes"),
    ("Lot d'origine et certificats", "documents seulement", "non", "attaché au lot"),
    ("Facturation et marge réelle", "non", "oui, sur coût estimé", "sur coût de revient réel"),
]

# --------------------------------------------------------------------- modules
MOD_TITRE = "Chaque brique du négoce a sa page."
MODULES = [
    ("01", "m-achats", "/negoce/achats-approvisionnements/", "gérer les achats et approvisionnements",
     "Cadenciers fournisseurs, contrats d'achat, engagements et suivi des arrivages."),
    ("02", "m-stocks", "/negoce/stocks-multi-depots/", "stocks multi-dépôts",
     "Plusieurs entrepôts, transit, sous douane et marchandise réservée."),
    ("03", "m-trace", "/negoce/tracabilite-lots/", "traçabilité des lots",
     "Lot d'origine, provenance, certificats et rappel produit."),
    ("04", "m-ventes", "/negoce/ventes-devis-commandes/", "ventes, devis et commandes",
     "Télévente, devis multi-devises, commandes et bons de livraison."),
    ("05", "m-edi", "/negoce/tarifs-reporting-edi/", "tarifs, reporting et EDI",
     "Grilles par client, échanges EDI et reporting de marge."),
]

# --------------------------------------------------------------------- CTA final
CTA_TITRE = "Voyez-le sur vos propres conteneurs."
CTA_INTRO = ("30 minutes, sans engagement, avec quelqu'un qui connaît les incoterms, les frais "
             "d'approche et les contraintes de la marchandise alimentaire. On part de vos "
             "opérations réelles.")

# --------------------------------------------------------------------- FAQ
FAQ_TITRE = "Ce qu'on nous demande avant de choisir."
FAQ = [
 ("Qu'est-ce qu'un logiciel import export ?",
  "Un logiciel import export pilote les flux de marchandises entre plusieurs pays : achats en "
  "devises, incoterms, acheminement, formalités douanières, stock en transit et facturation "
  "multi-devises. Appliqué à l'alimentaire, il ajoute trois exigences que les outils "
  "généralistes ne portent pas : le poids variable, les DLC et la traçabilité du lot d'origine."),
 ("Quelle différence avec un TMS ?",
  "Un TMS pilote le transport — l'acheminement, les documents de transport, la relation avec "
  "les transitaires. Il ne calcule ni votre coût de revient, ni votre marge, ni votre stock "
  "vendable. Les deux outils sont complémentaires : le TMS sait où est la marchandise, l'ERP "
  "sait ce qu'elle vous coûte et ce qu'elle vous rapporte."),
 ("Comment sont calculés les frais d'approche ?",
  "Le fret, l'assurance, les droits de douane et les frais de dossier sont saisis sur "
  "l'opération puis répartis sur chaque référence du conteneur, au poids, à la valeur ou au "
  "volume. Le coefficient obtenu s'applique automatiquement au prix d'achat pour donner le coût "
  "de revient réel, disponible dès la réception."),
 ("Le logiciel gère-t-il les incoterms ?",
  "Oui. L'incoterm est porté par la ligne d'achat : il détermine à quel moment la marchandise "
  "entre dans votre stock et dans votre coût, et quelles charges vous incombent. C'est aussi ce "
  "qui conditionne le transfert de risque, donc la couverture d'assurance."),
 ("Peut-on vendre une marchandise encore en transit ?",
  "Oui, et c'est courant en négoce alimentaire. La marchandise en route est visible avec sa "
  "date d'arrivée prévue, ce qui permet d'engager une vente en connaissance de cause — la "
  "distinction avec le stock disponible reste explicite pour éviter de promettre ce qui n'est "
  "pas encore là."),
 ("Comment est gérée la DLC d'une marchandise importée ?",
  "La DLC est portée par le lot, pas par la référence : deux lots du même produit n'ont pas la "
  "même date. La rotation se fait en FEFO, avec des alertes avant péremption et la possibilité "
  "de déclencher une remise ciblée sur les lots concernés."),
 ("Combien de temps dure le déploiement ?",
  "Comptez 4 à 8 semaines entre le cadrage et la bascule, reprise des données comprise. Le "
  "délai tient parce que les processus de la filière sont préconfigurés : le poids variable, le "
  "multi-devises et les DLC n'ont pas à être modélisés."),
 ("Hello Harel est-il un logiciel français ?",
  "Oui, édité en France depuis 2014 et proposé en SaaS : pas de serveur à administrer, mises à "
  "jour incluses, accès depuis le bureau comme depuis l'entrepôt. Plus de 200 entreprises "
  "agroalimentaires l'utilisent, avec une note de 5,0 sur 5."),
]

LOGOS = [
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Logo_Pro-inter_Magasins_Orientaux.webp", "Pro-Inter"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/1.webp", "Leclerc"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.14.24-300x64-1.webp", "Corseprim"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.12.46.webp", "Les Primeurs"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.10.42-300x226-1.webp", "HPS"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.08.48-300x86-1.webp", "Kore"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.07.48-300x165-1.webp", "Poujauran"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.06.38-300x131-1.webp", "Eatmotion"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.03.06-300x170-1.webp", "Ciao Gusto"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.04.34-300x103-1.webp", "Chef Cheffe"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.01.39-300x163-1.webp", "Savary"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-15.00.01-300x218-1.webp", "Karine & Jeff"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-14.57.18-300x122-1.webp", "Chrono Primeurs"),
 ("https://www.helloharel.com/wp-content/uploads/2026/08/Capture-decran-2026-01-13-a-14.56.24-300x154-1.webp", "Maison Aléna"),
]
