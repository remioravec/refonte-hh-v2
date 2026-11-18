#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
T11, second temps — les 33 descriptions que la règle automatique refusait de
toucher, réécrites à la main.

Ce sont celles qui n'avaient pas de signature de marque en fin de texte :
retirer une phrase entière y aurait fait perdre un argument. Elles sont donc
raccourcies mot à mot, en gardant l'argument et l'expression cible.

Deux exclusions explicites :
  - /blog/erp-boissons/ répond 301, la page n'est pas accessible : décision à
    prendre avant d'y toucher ;
  - /comparatifs/ a déjà été réécrite dans la passe T16.

Un cas de réparation sous Règle 0 : /migration-as400/ servait une description
COUPÉE EN PLEIN MOT (« ...piloté par l'ERP agroaliment »). Ce n'est pas une
optimisation, c'est un défaut : la phrase est refermée, à l'identique pour le
reste.

Le chiffre de clients (« +200 PME », « +200 entreprises », « plus de 100
clients ») est retiré des textes réécrits : trois valeurs différentes
circulent sur le site et la bonne n'est pas tranchée. On ne réaffirme pas un
chiffre qu'on ne sait pas vrai.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

HAUT, BAS = 985, 400
LARGE = set("mwMW—…")


def px(s):
    return round(sum(11.0 if c in LARGE else (8.0 if c.isalnum() else 5.5) for c in s))


D = {
 '/comparatifs/meilleur-logiciel-facturation-grossiste-negoce-2026/':
   "Comparatif 2026 des 9 logiciels de facturation pour grossistes et négoces. "
   "Méthodologie publique, Factur-X, facture depuis le BL.",
 '/blog/logiciel-commande-grande-surface-traiteur/':
   "Logiciel de commande GMS pour traiteurs : EDI, cadenciers, étiquetage INCO, "
   "14 allergènes et EAN-13 GS1. Conformité assurée.",
 '/blog/logiciel-tracabilite-dlc-traiteur/':
   "Logiciel de traçabilité DLC pour traiteurs : suivi des dates courtes, alertes "
   "avant péremption, rappel produit ciblé.",
 '/blog/logiciel-calcul-cout-de-revient-traiteur/':
   "Calculer le coût de revient et la marge nette par plat cuisiné : pertes et "
   "freintes intégrées, hausses fournisseurs propagées.",
 '/blog/logiciel-gestion-recette-multi-niveaux-traiteur/':
   "Gérer des recettes traiteur multi-niveaux : sous-recettes, fiches techniques "
   "coût matière propagé. La fin du tableur.",
 '/blog/logiciel-gestion-calibre-fruits-legumes/':
   "ERP fruits et légumes : calibres CEE, agréage à réception, catégories I, II et "
   "Extra, traçabilité des lots producteur.",
 '/blog/logiciel-prix-du-jour-fruits-legumes/':
   "Logiciel fruits et légumes avec prix du jour : grilles variables, cours RNM et "
   "MIN, télévente, marge recalculée chaque jour.",
 '/comparatifs/meilleur-erp-negoce-distribution-alimentaire-2026/':
   "Comparatif 2026 des 9 ERP de négoce et distribution alimentaire pour PME. "
   "Méthodologie publique sur 10 critères pondérés.",
 '/blog/meilleurs-erp-maraichers-fruits-legumes/':
   "Comparatif des 8 logiciels pour maraîchers et grossistes en fruits et légumes : "
   "poids variable, consignes, traçabilité.",
 '/blog/meilleurs-erp-boulangerie/':
   "Comparatif des ERP pour boulangeries et pâtisseries industrielles : recettes, "
   "coût de revient et traçabilité des lots de farine.",
 '/blog/alternative-sage-erp/':
   "Sage reste un bon outil financier mais limité en négoce alimentaire. Hello Harel "
   "gère poids variable, DLC et marges nativement.",
 '/blog/erp-cloud-saas-vs-on-premise/':
   "Cloud ou serveur local ? Comparatif ERP SaaS et on-premise pour PME "
   "agroalimentaires : coûts, sécurité, mobilité, évolutivité.",
 '/blog/partenariat-toncarton/':
   "Hello Harel s'associe à TonCarton pour la gestion des emballages alimentaires : "
   "commande intégrée, stock en temps réel.",
 '/blog/erp-as400/':
   "Votre AS/400 freine votre croissance ? Migrez vers un ERP SaaS sans perdre vos "
   "données. Guide et reprise d'historique.",
 '/blog/erp-decoupe-viande-poisson/':
   "ERP pour ateliers de découpe viande et poisson : rendements, désassemblage, "
   "poids variable et coût de revient réel par pièce.",
 '/blog/facture-traiteur/':
   "Modèle de facture pour traiteurs : mentions obligatoires, TVA et facturation "
   "événementielle. Conforme à la réglementation 2026.",
 '/blog/erp-viande-volaille/':
   "ERP filière viande et volaille : découpe, désassemblage, rendement matière et "
   "poids variable. Comparatif par profil.",
 '/blog/tracabilite-de-la-viande/':
   "Traçabilité de la viande : numéro de lot, origine, abattoir et atelier de "
   "découpe, du quartier au produit fini. Rappel ciblé.",
 '/blog/alerte-stock-securite/':
   "Configurer des alertes de stock de sécurité : seuils par article, "
   "réapprovisionnement automatique, ruptures évitées.",
 '/blog/logiciel-grossiste-boissons-cave-maitrisez-vos-consignes-et-accises/':
   "Logiciel pour grossistes en boissons et cavistes : consignes, accises, DLC et "
   "traçabilité des lots. SaaS adapté au négoce.",
 '/migration-as400/':
   "Migration AS/400 : audit gratuit et reprise de données garantie. Traçabilité "
   "par lot, coût de revient, poids variable et DLC.",
 '/negoce/':
   "L'ERP négoce alimentaire qui facture au poids réellement pesé, applique la DLC "
   "du lot et l'échéance légale du produit.",
 '/blog/erp-grossiste-distributeur/':
   "ERP pour distributeurs de produits frais : DLC courtes, poids variable, démarque "
   "et traçabilité. Simulateur de démarque.",
 '/blog/gestion-stock-multi-entrepots/':
   "Piloter ses stocks sur plusieurs sites : inventaire consolidé, transferts "
   "inter-dépôts, FEFO multi-sites et alertes par dépôt.",
 '/blog/calculer-le-prix-de-revient-en-boulangerie/':
   "Formule, simulateur gratuit et comparatif 2026 : tableur, logiciel dédié ou ERP. "
   "Le seuil où un logiciel devient rentable.",
 '/agroalimentaire/brasseur/':
   "Logiciel ERP pour brasseurs : traçabilité des matières, planification des "
   "brassins, consignes et coût de revient au litre.",
 '/contact/':
   "Démo gratuite et personnalisée de l'ERP agroalimentaire. Réponse sous 24 h. "
   "Contactez Maxence au 06 18 06 00 18.",
 '/qui-sommes-nous/':
   "Éditeur français d'ERP SaaS fondé en 2014 par un professionnel de la "
   "distribution alimentaire. Équipe et support en France.",
 '/implantation-auvergne-rhone-alpes/':
   "ERP agroalimentaire en Auvergne-Rhône-Alpes : traçabilité par lot, coût de "
   "revient, poids variable et DLC. Démo gratuite.",
 '/agroalimentaire/glacier/':
   "ERP glacier : mix, foisonnement, lot et DLC reliés au coût de revient du litre. "
   "Calculateur de poids au litre inclus.",
 '/agroalimentaire/':
   "ERP SaaS dédié à l'agroalimentaire : stocks, traçabilité, poids variable, DLC "
   "et marges. Démo gratuite en 3 minutes.",
}

EXCLUES = {
 '/blog/erp-boissons/': 'répond 301, décision à prendre avant d\'y toucher',
 '/comparatifs/': 'déjà réécrite dans la passe T16',
}


def resoudre(url):
    seg = [x for x in url.strip('/').split('/') if x]
    slug = seg[-1] if seg else ''
    for base in ('posts', 'pages'):
        d = n.call(f'wp/v2/{base}?slug={slug}&_fields=id,link')
        for p in d:
            if p['link'].replace('https://www.helloharel.com', '').rstrip('/') == url.rstrip('/'):
                return base, p['id']
        if d:
            return base, d[0]['id']
    raise RuntimeError('introuvable : ' + url)


def main(ecrire=False):
    hors = []
    for u, d in D.items():
        d = re.sub(r'\s+', ' ', d).strip()
        p = px(d)
        marque = '' if BAS <= p <= HAUT else '  <-- HORS BORNES'
        print(f'{p:5}{marque}  {u}')
        print(f'      {d}')
        if marque:
            hors.append(u)
            continue
        if ecrire:
            base, pid = resoudre(u)
            n.call('rankmath/v1/updateMeta', 'POST', {
                'objectID': pid, 'objectType': 'post',
                'meta': {'rank_math_description': d}})
    print()
    for u, r in EXCLUES.items():
        print(f'  exclue : {u} — {r}')
    print(f'\n{len(D) - len(hors)} écrites, {len(hors)} hors bornes')
    for u in hors:
        print('   ', u)


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
