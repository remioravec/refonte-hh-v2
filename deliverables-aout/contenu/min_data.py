# -*- coding: utf-8 -*-
"""
Le jeu de donnees des 17 MIN — la matiere propriétaire de la page.

Personne ne publie les dix-sept marches sur la MEME grille. La federation des
marches de gros de France donne superficie et tonnage, Wikipedia donne les
communes, et le volume de recherche vient de notre propre releve. Mis cote a
cote, ces trois sources donnent une comparaison qui n'existe nulle part
ailleurs — y compris ses defauts, que nous signalons plutot que de les
recopier.

SOURCES, PAR CHAMP
  commune, region ..... liste Wikipedia des MIN, relevee le 11/09/2026,
                        recoupee avec les fiches Google des marches
  superficie, tonnage . Federation des marches de gros de France,
                        marchesdegrosdefrance.net, releve le 11/09/2026
  recherches .......... Google Ads, France, francais, moyenne 12 mois
                        arretee en juillet 2026
  site officiel ....... relevé en SERP le 11/09/2026

TROIS DONNEES PUBLIEES QUE NOUS SIGNALONS COMME DOUTEUSES
  · Agen 29 ha / 320 000 t et Lille 29 ha / 320 000 t : chiffres STRICTEMENT
    identiques sur la page de la federation. L'un des deux est une erreur de
    recopie. Nous affichons la valeur avec une reserve.
  · Angers 140 t pour 11 ha : deux mille fois moins dense que la moyenne des
    seize autres. Il manque trois zeros. Nous n'affichons pas le tonnage.
  Lille n'est plus un MIN — declasse en 2019 — et ne figure donc pas ici.
"""

# cle, nom, commune, region, superficie ha, tonnage t, recherches/mois, site, reserve
MIN = [
    ("rungis", "Rungis", "Rungis et Chevilly-Larue (94)", "Île-de-France",
     234.0, 1862000, 1600, "https://www.rungisinternational.com/", None),
    ("marseille", "Marseille", "Marseille (13)", "Provence-Alpes-Côte d'Azur",
     35.0, 537182, 110, None, None),
    ("lyon", "Lyon — Corbas", "Corbas (69)", "Auvergne-Rhône-Alpes",
     12.0, 305000, 40, None, None),
    ("toulouse", "Toulouse", "Toulouse (31)", "Occitanie",
     18.0, 232000, 260, "http://www.lgm-mintoulouse.com/", None),
    ("nantes", "Nantes", "Rezé (44)", "Pays de la Loire",
     20.0, 200000, 1600, "https://www.minnantes.com/", None),
    ("bordeaux", "Bordeaux — Brienne", "Bordeaux (33)", "Nouvelle-Aquitaine",
     15.0, 180000, 110, "https://min-bordeaux-brienne.fr/", None),
    ("rouen", "Rouen", "Rouen (76)", "Normandie",
     20.0, 130000, 480, "http://www.minderouen.fr/", None),
    ("cavaillon", "Cavaillon", "Cavaillon (84)", "Provence-Alpes-Côte d'Azur",
     27.0, 110000, 170, "https://www.min-cavaillon.fr/", None),
    ("chateaurenard", "Châteaurenard", "Châteaurenard (13)", "Provence-Alpes-Côte d'Azur",
     11.5, 100000, 140, None, None),
    ("nice", "Nice — MIN d'Azur", "Nice (06)", "Provence-Alpes-Côte d'Azur",
     23.0, 97555, 210, None,
     "Le MIN d'Azur réunit le marché alimentaire et le marché aux fleurs."),
    ("avignon", "Avignon", "Avignon (84)", "Provence-Alpes-Côte d'Azur",
     25.5, 86000, 40, None, None),
    ("strasbourg", "Strasbourg", "Strasbourg (67)", "Grand Est",
     15.0, 80000, 50, None, None),
    ("montpellier", "Montpellier — Mercadis", "Montpellier (34)", "Occitanie",
     10.0, 60000, 210, None, None),
    ("agen", "Agen — Boé", "Agen (47)", "Nouvelle-Aquitaine",
     29.0, 320000, 40, "https://www.min-agen-boe.com/",
     "Chiffres strictement identiques à ceux publiés pour Lille : l'un des deux "
     "est une erreur de recopie de la source."),
    ("grenoble", "Grenoble", "Grenoble (38)", "Auvergne-Rhône-Alpes",
     5.0, 20000, 170, "http://www.min-grenoble.fr/", None),
    ("angers", "Angers", "Angers (49)", "Pays de la Loire",
     11.0, None, 40, None,
     "La fédération publie 140 tonnes pour 11 hectares, deux mille fois moins "
     "dense que la moyenne des autres marchés. Tonnage non affiché."),
    ("nice-fleurs", "Nice — fleurs", "Nice (06)", "Provence-Alpes-Côte d'Azur",
     None, None, None, None,
     "Marché aux fleurs, compté dans le MIN d'Azur ci-dessus. Ni superficie ni "
     "tonnage publiés séparément."),
]

SOURCES = {
    "federation": ("Fédération des marchés de gros de France",
                   "https://www.marchesdegrosdefrance.net/fr_FR/nos-marches-partenaires"),
    "rungis": ("Marché International de Rungis", "https://www.rungisinternational.com/"),
    "loi": ("Code de commerce, articles L761-1 à L761-11",
            "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000005634379/"
            "LEGISCTA000006146141/"),
}
RELEVE = "11 septembre 2026"


def avec_donnees():
    """Les marches dont superficie ET tonnage sont exploitables."""
    return [m for m in MIN if m[4] and m[5]]


def totaux():
    d = avec_donnees()
    t = sum(m[5] for m in d)
    s = sum(m[4] for m in d)
    return {"marches": len(MIN), "mesures": len(d), "tonnage": t, "surface": s,
            "densite": t / s}


def densite(m):
    return (m[5] / m[4]) if (m[4] and m[5]) else None
