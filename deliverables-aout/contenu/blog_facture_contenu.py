# -*- coding: utf-8 -*-
"""
Article « mentions obligatoires d'une facture », en prevision de Factur-X.

4.1 BRIEF
=========
GRAPPE VISEE — 6 530 recherches par mois sur le coeur.
Google Ads, France, francais, moyenne 12 mois arretee en aout 2026 :
  mention obligatoire facture ................. 3 600
  mentions obligatoires facture ............... 1 900
  mentions legales facture .................... 720
  mentions obligatoires facture electronique .. 210
  que doit contenir une facture ............... 90
  facture mentions obligatoires auto entrepreneur 10
Contexte de la grappe, pour le maillage :
  facturation electronique obligatoire ........ 6 600, et 12 100 en juillet
                                                et aout 2026
  factur-x .................................... 1 600, CPC 4,80 €

TENDANCE — « mentions obligatoires facture electronique » passe de 70 en
septembre 2025 a 320 en juin 2026 : multiplie par 4,5 en un an. C'est la
demande qui monte, et c'est elle qui porte l'angle.

ANTI-CANNIBALISATION — verdict FAIBLE. Le site a bien un article Factur-X
(/blog/factur-x-e-facturation-logiciel/, post 7763, publie le 14/04/2026),
mais il ne contient AUCUNE occurrence de « mentions obligatoires » : verifie,
zero. Les deux pages ne se marchent pas dessus :
  · /blog/factur-x-e-facturation-logiciel/ .. le format, le calendrier, l'ERP
  · cet article ............................. la liste des mentions, a jour
Elles se lient. Reserve a signaler : l'article Factur-X date d'avril 2026, son
calendrier est anterieur a l'entree en vigueur — a verifier separement.

SERP « mentions obligatoires facture » RELEVEE LE 11/09/2026 — TROIS CONSTATS
  1. Un AI Overview occupe la POSITION 1 ABSOLUE et repousse le premier
     organique en 2e. Il cite quatre sources, dont DEUX editeurs prives
     (Dext, Fiducial) : un editeur peut etre cite.
  2. Deux editeurs de logiciel sont deja dans le top 5 — Codial 3e, Dext 4e.
     La SERP n'est pas verrouillee par les sites publics.
  3. AUCUNE page du top 10 n'est datee d'apres le 1er septembre 2026, date
     d'entree en vigueur de l'obligation de reception. Les plus recentes
     datent du 1er juillet (Bpifrance) et du 11 mai (Dext). La plus ancienne
     du top 10 date de fevrier 2024.

C'est le trou : l'obligation est en vigueur depuis DIX JOURS et personne n'a
mis a jour. Deux des quatre questions posees portent d'ailleurs sur le
nouveau — « Quelles sont les nouvelles mentions obligatoires sur les factures
en 2026 ? ».

ANGLE TRANCHE — plus a jour et plus demontre : la liste complete arretee au
11 septembre 2026, ce qui est DEJA en vigueur et ce qui ne l'est pas encore,
et une checklist cochable au lieu d'une liste a puces de plus.

PROMESSE — Les mentions obligatoires d'une facture au 11 septembre 2026, les
quatre qui arrivent avec la facture electronique, et ce que coute un oubli.

MODULE NAVBOOST — la SERP montre cinq pages de listes a puces et AUCUN outil.
La requete « que doit contenir une facture » est une liste a verifier : le
module est donc une CHECKLIST COCHABLE, avec compteur de conformite.

SIGNAL GA4 DECLARE — interaction avec la checklist (case cochee).

MAILLAGE — lien mere dans les 100 premiers mots : « logiciel de facturation »
vers /fonctionnalites/facturation/. Puis Factur-X, bon de livraison, bon de
commande, loi anti-fraude TVA, tarifs reporting et EDI.
"""

TITLE = "Mentions Obligatoires d'une Facture : la Liste à Jour 2026"
DESC = ("Les mentions obligatoires d'une facture au 11 septembre 2026, les quatre nouvelles "
        "de la facture électronique, et l'amende encourue par mention manquante.")
H1 = "Mentions obligatoires d'une facture : la liste à jour, et les quatre nouvelles"

SOURCES = {
    "sp_mentions": ("Service-public Entreprendre, mentions obligatoires sur une facture, "
                    "mis à jour le 11 août 2026",
                    "https://entreprendre.service-public.gouv.fr/vosdroits/F31808"),
    "sp_sanctions": ("Service-public Entreprendre, sanctions, mis à jour le 7 août 2026",
                     "https://entreprendre.service-public.gouv.fr/vosdroits/F23208"),
    "loi": ("Code de commerce, article L441-9 et Code général des impôts, annexe II, "
            "article 242 nonies A",
            "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000032227330/"),
}
RELEVE = "11 septembre 2026"

# groupe, libelle, detail
MENTIONS = [
    ("Identification", "Date d'émission de la facture", ""),
    ("Identification", "Numéro de facture unique",
     "Sur une séquence chronologique continue, sans trou."),
    ("Identification", "Date de la vente ou de la prestation",
     "Date de livraison du bien ou de fin d'exécution de la prestation."),
    ("Identification", "Numéro du bon de commande", "S'il a été établi par l'acheteur."),
    ("Vendeur", "Identité complète du vendeur",
     "Nom, prénom et mention EI pour un entrepreneur individuel ; dénomination, "
     "forme juridique, capital et siège social pour une société."),
    ("Vendeur", "Numéro SIREN du vendeur", ""),
    ("Vendeur", "Numéro de TVA intracommunautaire du vendeur",
     "Sauf pour les factures d'un montant inférieur à 150 € hors taxes."),
    ("Client", "Identité du client",
     "Dénomination sociale s'il s'agit d'un professionnel."),
    ("Client", "Adresse de facturation du client", ""),
    ("Client", "Numéro de TVA du client", "S'il est redevable de la TVA."),
    ("Opération", "Désignation précise des produits ou prestations", ""),
    ("Opération", "Décompte détaillé",
     "Quantité, dénomination, prix unitaire hors taxes et taux de TVA pour chaque ligne."),
    ("Opération", "Majorations éventuelles", "Frais de transport, d'emballage."),
    ("Opération", "Réductions acquises", "Rabais, remises et ristournes."),
    ("Opération", "Sommes totales hors taxes et toutes taxes comprises", ""),
    ("Règlement", "Date d'échéance du paiement", ""),
    ("Règlement", "Conditions d'escompte",
     "Ou la mention « escompte pour paiement anticipé : néant »."),
    ("Règlement", "Taux des pénalités de retard", ""),
    ("Règlement", "Indemnité forfaitaire pour frais de recouvrement",
     "40 €, entre professionnels."),
]

# Les quatre mentions ajoutees par la reforme de la facturation electronique.
NOUVELLES = [
    ("Le numéro SIREN du client",
     "Jusqu'ici seul le SIREN du vendeur était exigé. Celui de l'acheteur devient "
     "obligatoire : c'est lui qui permet l'acheminement de la facture sur la plateforme."),
    ("L'adresse de livraison des biens",
     "Uniquement si elle diffère de l'adresse de facturation du client. Pour un grossiste "
     "qui livre sur plusieurs points de vente, c'est la règle et non l'exception."),
    ("La catégorie de l'opération",
     "Livraison de biens, prestation de services, ou les deux à la fois quand la facture "
     "porte une vente et une prestation distincte."),
    ("L'option de paiement de la TVA sur les débits",
     "À porter sur la facture lorsque le vendeur a exercé cette option."),
]

CALENDRIER = [
    ("1ᵉʳ septembre 2026", "Réception",
     "Toutes les entreprises assujetties à la TVA doivent être capables de RECEVOIR une "
     "facture électronique. Sans exception de taille.", True),
    ("1ᵉʳ septembre 2026", "Émission — grandes entreprises et ETI",
     "Les grandes entreprises et les entreprises de taille intermédiaire doivent ÉMETTRE "
     "au format électronique.", True),
    ("1ᵉʳ septembre 2027", "Émission — PME et TPE",
     "Les petites et moyennes entreprises et les microentreprises basculent à leur tour.",
     False),
]

FORMATS = [
    ("Factur-X", "PDF lisible + XML embarqué",
     "Le format hybride : l'œil lit le PDF, la machine lit le XML. Le plus courant en France."),
    ("UBL", "XML seul", "Format international, très répandu dans les échanges européens."),
    ("CII", "XML seul", "Format de la norme européenne EN 16931, utilisé en EDI."),
]

SANCTIONS = [
    ("15 €", "par mention manquante ou inexacte",
     "Plafonné à 25 % du montant de la facture."),
    ("50 %", "du montant des factures",
     "Si l'identité ou l'adresse du client ou du fournisseur a été dissimulée ou modifiée."),
    ("75 000 €", "personne physique, défaut de facturation",
     "Porté à 150 000 € en cas de récidive dans les deux ans."),
    ("375 000 €", "personne morale, défaut de facturation",
     "Porté à 750 000 € en cas de récidive dans les deux ans."),
]

# Les quatre questions posees, reprises MOT POUR MOT dans la SERP du 11/09/2026.
FAQ = [
    ("Quelles sont les nouvelles mentions obligatoires sur les factures en 2026 ?",
     "Quatre s'ajoutent avec la facturation électronique : le <strong>numéro SIREN du "
     "client</strong>, l'<strong>adresse de livraison des biens</strong> si elle diffère de "
     "l'adresse de facturation, la <strong>catégorie de l'opération</strong> — livraison de "
     "biens, prestation de services ou les deux — et la mention de l'<strong>option de "
     "paiement de la TVA sur les débits</strong> lorsqu'elle a été exercée."),
    ("Quels sont les composants obligatoires d'une facture ?",
     "Dix-neuf mentions, réparties en cinq blocs : l'identification de la facture, "
     "l'identité du vendeur, celle du client, le détail de l'opération et les conditions de "
     "règlement. La checklist plus haut les reprend une par une, avec ce qu'il faut y "
     "écrire."),
    ("Quel est l'élément indispensable sur une facture ?",
     "Aucun ne l'est plus qu'un autre : l'amende de 15 € s'applique <strong>par mention "
     "manquante ou inexacte</strong>, quelle qu'elle soit. En pratique, le numéro unique et "
     "la séquence chronologique continue sont les plus surveillés, parce qu'un trou dans la "
     "numérotation est la première chose qu'un contrôle regarde."),
    ("La facturation électronique est-elle déjà obligatoire ?",
     "Oui, en réception. Depuis le <strong>1ᵉʳ septembre 2026</strong>, toute entreprise "
     "assujettie à la TVA doit être capable de recevoir une facture électronique, quelle que "
     "soit sa taille. L'obligation d'émettre suit : elle s'applique déjà aux grandes "
     "entreprises et aux ETI, et s'étendra aux PME et TPE le 1ᵉʳ septembre 2027."),
]
