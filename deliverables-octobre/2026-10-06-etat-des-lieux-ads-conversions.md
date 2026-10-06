# État des lieux — Google Ads et conversions

Hello Harel · 6 octobre 2026 · mesuré sur Google Ads, GA4, Search Console et la
base WordPress

---

## La réponse courte

**Non, ce n'est pas normal.** Et ce n'est pas un problème de mesure : trois
systèmes indépendants disent la même chose.

| Source | 15 → 25 sept. | 26 sept. → 6 oct. |
|---|---|---|
| Conversions Google Ads | **24** | **4** |
| Événements clés GA4 | 24 | 5 |
| Demandes en base WordPress | ~14 réelles | **1, et c'est un spam** |

Le trafic, lui, n'a pas bougé : **32 clics par jour** contre 43 avant, et
**~100 sessions par jour** en continu. Ce n'est pas le robinet qui s'est fermé,
c'est le taux de conversion qui est passé de **5,6 % à 1,1 %**.

Coût par conversion : **29,59 €** sur 22/09–05/10, **83 €** sur les 11 derniers
jours.

---

## La cause, en un chiffre

Répartition du trafic de la seule campagne active, `HH | Search | ERP x Metiers`,
du 22/09 au 05/10 :

| Réseau | Impressions | Clics | Coût | Conversions |
|---|---|---|---|---|
| **Google Search** (google.com) | 181 | **2** | 5,79 € | 0 |
| **Partenaires du Réseau de Recherche** | 2 285 | **548** | **556,39 €** | 19 |

**99 % du budget part chez les partenaires de recherche, pas sur Google.**
Deux clics en deux semaines sur google.com.

Le lead Yannick Pederiva de ce matin vient de `syndicatedsearch.goog` — un
partenaire, précisément.

### Pourquoi le budget part là-bas

Ce n'est pas un réglage volontaire, c'est une conséquence :

| Mesure | Valeur |
|---|---|
| Taux d'impressions obtenu sur le Réseau de Recherche | **9,99 %** |
| Impressions perdues **à cause du classement** | **69,06 %** |
| Impressions perdues à cause du budget | 27,27 % |

Les annonces **n'arrivent pas à gagner les enchères sur google.com**. Le budget
ne reste pas inutilisé : il se déverse sur les partenaires, où la concurrence
est nulle et l'intention aussi.

Et le classement est bas parce que le niveau de qualité l'est :

| Mot-clé | Correspondance | Niveau de qualité | Coût | Conv. |
|---|---|---|---|---|
| erp negoce | large | **3** | 235,43 € | 7 |
| logiciel negoce | large | – | 137,00 € | 3 |
| logiciel gestion des lots | large | – | 88,08 € | 8 |
| logiciel négoce | large | 4 | 31,69 € | 0 |
| erp grossiste | large | 4 | 29,12 € | 1 |
| logiciel boulangerie | large | **1** | 12,57 € | 0 |
| erp traiteur | **exact** | **7** | 4,84 € | 0 |

Le seul mot-clé en **exact** est aussi le seul qui a un bon niveau de qualité.

### La correspondance large n'a jamais été corrigée

| Type | Mots-clés | Dépense |
|---|---|---|
| Large | 47 | **556,39 € (99 %)** |
| Expression | 12 | 0,95 € |
| Exact | 1 | 4,84 € |

Le fichier `hh-expression-et-exact.csv` préparé fin septembre **n'a jamais été
importé**. La campagne tourne toujours à 99 % en large.

### Ce que le large achète

Termes de recherche réellement payés du 26/09 au 06/10 :

| Terme | Clics | Coût | Conversions |
|---|---|---|---|
| logiciels commerciaux | **64** | **41,72 €** | **0** |
| logiciels gestion entreprise | 9 | 9,71 € | 0 |
| automatisation des commandes | 2 | 7,18 € | 0 |
| digitalisation des entreprises | 7 | 5,16 € | 0 |
| logiciel gestion intégré | 9 | 8,40 € | 0 |
| pastel invoicing · cin7 shopify · xero retail · erp codecanyon · isitrack | 11 | ~7,70 € | 0 |
| how artificial intelligence helps businesses | 1 | 1,08 € | 0 |

**Pas une seule conversion sur toute cette liste.** Pendant ce temps,
`traçabilité produit alimentaire` et `erp traiteur` reçoivent un clic chacun.

Le mécanisme est une boucle : large + Maximiser les conversions + peu de signal
de conversion → Google élargit → on bloque un paquet de requêtes génériques avec
des négatifs → il en trouve un autre. Les 158 négatifs déjà en place le
montrent : `logiciel gestion entreprise` y figurait déjà, et
`logiciels gestion entreprise` au pluriel est passé quand même (un négatif ne
bloque pas les variantes proches).

---

## Le deuxième problème : les mails de leads n'arrivent pas

**Zéro mail de demande de démo dans ta boîte sur 30 jours.** Les seuls objets
« Demande de demo » retrouvés sont ton propre test du 23/09 et ton transfert de
mon test du 03/10.

Or la chaîne fonctionne : j'ai renvoyé à l'instant le lead Yannick Pederiva par
l'endpoint normal, et le mail est parti et arrivé — mis en page par le plugin,
avec le bouton tableau de bord, à Nicolas, toi et Timothy en copie.

Donc l'envoi marche **quand l'endpoint est appelé**. Pour les vraies
soumissions, il ne l'est pas, ou il échoue sans bruit. Les deux routes sont
découplées :

- `wp-json/hh/v1/contact` → envoie le mail
- `wp-json/hh/v1/lead` → crée la fiche

La fiche peut exister sans que le mail parte. C'est exactement ce qu'on observe.
**Il faut un journal d'envoi côté serveur pour trancher** — je ne veux pas
deviner sur ce point.

### Au passage, les fiches sont dupliquées

93 fiches en base, mais : « Yves grard » ×7 en une minute, « Abdellatif Haddaj »
×3, « Yannick Pederiva » ×2. L'endpoint `/lead` est ouvert, sans
déduplication et sans authentification. Le compte réel de demandes est bien plus
bas que 93.

---

## Ce que j'ai fait aujourd'hui

**17 négatifs posés** sur la campagne, en **expression** (pas en large : un
négatif large ne bloque pas les pluriels) — uniquement des termes qui ont coûté
de l'argent pour zéro conversion, ou des marques de produits étrangers :

`logiciels commerciaux` · `logiciel commercial` · `digitalisation` ·
`logiciel pour entreprise` · `logiciels pour entreprises` ·
`logiciel gestion intégré` (+ sans accent) · `solutions logicielles` ·
`outils de gestion` · `pastel invoicing` · `cin7` · `xero` · `codecanyon` ·
`dext` · `isitrack` · `coupa` · `ciel gestion`

**Je n'ai pas touché** à `application pour professionnel` : générique, mais il a
produit **8 conversions pour 193 €** à la mi-septembre. On ne le coupe pas.

**Le lead Yannick Pederiva a été renvoyé** à Nicolas, toi et Timothy en copie.

---

## Les trois décisions qui t'attendent

### 1. Couper les partenaires du Réseau de Recherche

Une case à décocher. **C'est ma recommandation**, avec un avertissement net :
les 19 conversions des deux dernières semaines viennent **toutes** des
partenaires. Couper, c'est accepter que le volume tombe très bas le temps que le
niveau de qualité remonte sur google.com.

Le contre-argument : sur les 11 derniers jours, ces partenaires ont produit
4 conversions pour 332 €, et achètent `xero retail` et `erp codecanyon`. On paie
déjà cher pour du vide.

### 2. Passer en expression et exact

Le fichier est prêt depuis fin septembre. C'est la seule correction qui agit sur
la cause : tant que 47 mots-clés sont en large, chaque négatif posé sera
contourné la semaine suivante. Je ne peux pas changer un type de correspondance
par l'API — c'est un import manuel dans l'interface.

### 3. Nettoyer les actions de conversion

7 actions sont marquées **principales** et n'enregistrent rien :
« Actions locales – Itinéraire », « Appels directs via Google Maps »,
« Appels Directs », deux actions de campagnes intelligentes toutes supprimées,
et « Création de compte », qui est un objectif **Universal Analytics** — un outil
arrêté depuis 2023.

La stratégie « Maximiser les conversions » optimise sur ce panier. Il faut ne
laisser principale que **« Demande de demo - Page Contact »**, la seule qui
porte les 19 conversions. Aucun risque : les autres sont à zéro.
**Je le fais sur un mot de ta part.**

---

## Deux leviers gratuits en plus

**Le remarketing est en pause.** `HH | Display | RMK Metiers+Contact`, 3 €/jour,
statut PAUSED. Ce sont des gens qui ont déjà vu le site.

**Le budget est mal réparti entre les groupes d'annonces :**

| Groupe | Clics | Coût | Conv. | Coût / conversion |
|---|---|---|---|---|
| ERP Négoce & Grossiste | 427 | 433,23 € | 11 | **39,38 €** |
| Traçabilité & Lots | 104 | 102,00 € | 8 | **12,75 €** |
| Boulangerie (surveillé) | 13 | 12,57 € | 0 | – |
| Traiteur & Plats cuisinés | 2 | 8,57 € | 0 | – |
| ERP Agroalimentaire | 4 | 5,81 € | 0 | – |

« Traçabilité & Lots » convertit **trois fois moins cher** et reçoit **un quart**
du budget de « Négoce ».

---

## Ce que je ne recommande pas

**Augmenter le budget.** 27 % des impressions sont perdues sur le budget, mais
69 % le sont sur le classement. Mettre plus d'argent aujourd'hui, c'est acheter
plus de clics chez les partenaires sur `logiciels commerciaux`. Le budget est le
dernier levier à toucher, pas le premier.
