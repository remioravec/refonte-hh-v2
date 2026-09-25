#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le contenu de la section fonctionnalites en defilement, pour les trois pages.

Trois regles d'ecriture, tenues ligne par ligne :

1. Le titre dit ce que l'ecran montre. Plusieurs paires etaient fausses
   avant : sur le torrefacteur, « Origines & tracabilite » affichait l'ecran
   des allergenes ; sur le brasseur, « Brassins & fermentation » affichait la
   preparation de commandes. Les titres sont realignes sur l'ecran reel
   plutot que de laisser le lecteur constater le decalage.

2. Les puces decrivent ce qu'on voit a l'ecran, pas des promesses. Chaque
   puce renvoie a un element present dans la capture : une colonne, un
   indicateur, un seuil.

3. Sur telephone, les puces longues laissent la place a trois pastilles
   courtes : la meme information, compressee, jamais une affirmation
   nouvelle. Le tableau de bord passe au-dessus du texte — c'est lui qu'on
   vient voir.

4. AUCUN avis n'est invente. Les trois seuls avis places sont des avis
   Google reels, deja affiches sur le site, poses la ou ils parlent
   vraiment de la fonctionnalite. Les autres etapes n'en portent pas.
   Un avis client fabrique est une fausse allegation, pas un element de
   design.
"""

# Les avis reels du site. La cle sert a les rattacher a une fonctionnalite.
AVIS = {
    "marges": ("Philippe D.", "PD",
               "Le suivi des marges nous a permis d'identifier des pertes "
               "qu'on ne voyait pas."),
    "dlc": ("Julien B.", "JB",
            "La gestion des fiches techniques et des DLC est un vrai gain de "
            "temps au quotidien."),
    "sites": ("Sophie L.", "SL",
              "On gère 3 sites avec des stocks consolidés en temps réel."),
}

# page -> [(titre H2, [puces], cle d'avis ou None)], dans l'ordre des ecrans
CONTENU = {
    "torrefacteur": [
        ("Le coût de revient d'un café torréfié, décomposé au kilo",
         ["La décomposition matière, main-d'œuvre et frais, en pourcentage du coût",
          "La freinte de torréfaction intégrée au rendement, pas estimée à part",
          "Le prix de revient recalculé dès qu'un cours du café vert bouge",
          "La marge par référence : origine, assemblage, mouture"],
         "marges",
         ["Coût au kilo", "Freinte incluse", "Marge par origine"]),
        ("Chaque lot de café vert suivi jusqu'au paquet livré",
         ["La traçabilité aval : quel client a reçu quel lot, sur quel bon de livraison",
          "La traçabilité amont : de quel lot vert et de quel importateur il provient",
          "Les quantités sorties par produit fini et par destination",
          "Un rappel produit reconstitué sans rouvrir un classeur"],
         None,
         ["Lot → client", "Lot → importateur", "Rappel reconstitué"]),
        ("Allergènes et étiquetage INCO, remontés depuis les matières",
         ["La déclaration d'allergènes remontée automatiquement des matières premières",
          "L'origine de chaque composant, lot par lot",
          "La distinction entre ingrédient déclaré et trace possible",
          "L'étiquette générée conforme, sans ressaisie"],
         None,
         ["Allergènes auto", "Traces distinguées", "Étiquette INCO"]),
        ("Des emplacements sous contrainte, surveillés en continu",
         ["Chaque emplacement avec sa consigne de température",
          "Le relevé courant comparé à la consigne, écart visible",
          "Les alertes déclenchées au dépassement, pas au constat",
          "Les DDM du café vert et du torréfié suivies par emplacement"],
         "dlc",
         ["Température suivie", "Alerte au seuil", "DDM par emplacement"]),
        ("Un stock consolidé sur tous vos points de vente",
         ["Le stock des quatre sites vu d'un seul écran",
          "Les références à réassortir, sous le seuil, remontées seules",
          "Les transferts entre entrepôt, dépôts et boutique",
          "Boutique, e-commerce, CHR et B2B dans le même compteur"],
         "sites",
         ["4 sites, 1 écran", "Seuil de réassort", "Transferts suivis"]),
    ],
    "brasseur": [
        ("Le coût de revient d'un brassin, décomposé poste par poste",
         ["La décomposition matière, main-d'œuvre et frais, en pourcentage du coût",
          "Les pertes de garde et de soutirage intégrées au rendement",
          "Le coût recalculé dès qu'un prix de malt ou de houblon bouge",
          "La marge par format : fût, bouteille, canette"],
         "marges",
         ["Coût par brassin", "Pertes incluses", "Marge par format"]),
        ("Des commandes préparées ligne à ligne, lot par lot",
         ["Chaque ligne de commande rattachée au lot réellement prélevé",
          "Le commandé et le pesé côte à côte, écart visible",
          "Le colisage constitué au fur et à mesure de la préparation",
          "Un brassin retrouvé depuis n'importe quelle expédition"],
         None,
         ["Ligne ↔ lot", "Commandé vs pesé", "Colisage suivi"]),
        ("Malt et houblon stockés sous contrainte, alertés au seuil",
         ["Chaque emplacement avec sa consigne de température",
          "Le relevé courant comparé à la consigne, écart visible",
          "Les DDM des matières suivies par emplacement",
          "Le réapprovisionnement déclenché au seuil, pas à la rupture"],
         "dlc",
         ["Température suivie", "Alerte au seuil", "DDM par emplacement"]),
        ("Vos clients CHR et cavistes, encours et retards compris",
         ["L'ancienneté de la relation et le facturé sur douze mois glissants",
          "Les retards de règlement affichés sur la fiche, pas dans un tableur",
          "Les opportunités et les relances rattachées au client",
          "Les consignes de fûts suivies par client"],
         None,
         ["Encours client", "Retards visibles", "Consignes de fûts"]),
        ("Chaque brassin tracé, de la matière au client livré",
         ["La traçabilité aval : quel client a reçu quel lot, sur quel bon de livraison",
          "La traçabilité amont : de quelles matières le brassin provient",
          "Les quantités sorties par produit fini et par destination",
          "Les contrôles et non-conformités consignés au même endroit"],
         None,
         ["Lot → client", "Lot → matières", "Contrôles consignés"]),
    ],
    "chocolatier": [
        ("Le coût matière d'une ganache, décomposé au gramme",
         ["La décomposition matière, main-d'œuvre et frais, en pourcentage du coût",
          "Les pertes de tempérage et d'enrobage intégrées au rendement",
          "Le coût recalculé dès qu'un cours du cacao bouge",
          "La marge par référence : bonbon, tablette, coffret"],
         "marges",
         ["Coût au gramme", "Pertes incluses", "Marge par référence"]),
        ("Un plan de production qui tient la charge de l'atelier",
         ["Les ordres du jour, dont ceux en série longue",
          "Le taux de charge de l'atelier affiché avant lancement",
          "Les besoins matière calculés depuis le plan, pas après",
          "Les pics de Pâques et de Noël lissés sur les semaines"],
         None,
         ["Charge d'atelier", "Besoins matière", "Pics lissés"]),
        ("Couvertures et pralinés sous contrainte, surveillés en continu",
         ["Chaque emplacement avec sa consigne de température",
          "Le relevé courant comparé à la consigne, écart visible",
          "Les alertes déclenchées au dépassement, pas au constat",
          "Les DLC des matières fragiles suivies par emplacement"],
         "dlc",
         ["Température suivie", "Alerte au seuil", "DLC par emplacement"]),
        ("Atelier, boutiques et corners sur un seul stock",
         ["Le stock des quatre sites vu d'un seul écran",
          "Les références à réassortir, sous le seuil, remontées seules",
          "Les transferts entre atelier, boutiques et corners",
          "Les ventes de chaque point de vente dans le même compteur"],
         "sites",
         ["4 sites, 1 écran", "Seuil de réassort", "Transferts suivis"]),
        ("Allergènes propagés jusqu'à l'étiquette, sans ressaisie",
         ["La déclaration d'allergènes remontée automatiquement des matières premières",
          "L'origine de chaque composant, lot par lot",
          "La distinction entre ingrédient déclaré et trace possible",
          "L'étiquette INCO générée conforme depuis la recette"],
         None,
         ["Allergènes auto", "Traces distinguées", "Étiquette INCO"]),
    ],
}


def controler():
    """Le contenu doit couvrir exactement cinq etapes par page."""
    pb = []
    for cle, blocs in CONTENU.items():
        if len(blocs) != 5:
            pb.append("%s : %d etapes au lieu de 5" % (cle, len(blocs)))
        for k, (h2, pts, avis, ch) in enumerate(blocs, 1):
            if not 3 <= len(pts) <= 4:
                pb.append("%s %d : %d puces (3 ou 4 attendues)" % (cle, k, len(pts)))
            if avis and avis not in AVIS:
                pb.append("%s %d : avis inconnu %r" % (cle, k, avis))
            if len(ch) != 3:
                pb.append("%s %d : %d pastilles au lieu de 3" % (cle, k, len(ch)))
            for x in ch:
                if len(x) > 22:
                    pb.append("%s %d : pastille trop longue %r" % (cle, k, x))
            if len(h2) > 72:
                pb.append("%s %d : titre de %d caracteres" % (cle, k, len(h2)))
    return pb


if __name__ == "__main__":
    pb = controler()
    for x in pb:
        print("   !", x)
    n = sum(len(b) for b in CONTENU.values())
    a = sum(1 for b in CONTENU.values() for x in b if x[2])
    print("%d etapes, %d portant un avis reel, %d avis distincts disponibles"
          % (n, a, len(AVIS)))
    print("controles :", "tout est vert" if not pb else "%d ecart(s)" % len(pb))
