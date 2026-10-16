# Négoce — variante B du test A/B — 29/08/2026

Objet : produire la variante B avec **le contenu de la variante A**, **notre DA** et
**l'UX de la page d'accueil Skello** transmise en référence.

Page : `11495` — `[TEST B] ERP Import Export Alimentaire • Frais d'Approche & Lots`, **brouillon**.

---

## Une correction de conception du test, à valider

Les deux variantes en place ne testaient pas la même chose : A portait l'angle « frais
d'approche » et B un guide d'achat. Deux contenus **et** deux UX différents : quel que soit
le résultat, on n'aurait pas su ce qui l'a produit.

B a donc été reconstruite sur **le contenu de A, sans réécriture**. Les valeurs du calcul, le
tableau comparatif, les huit fonctions, les cinq modules et les huit questions sont repris
mot pour mot. Les seules transformations sont des mises en puces de paragraphes déjà présents
dans A, imposées par la grille Skello. **Une seule variable change : l'UX.**

L'ancien contenu de B (guide d'achat) n'est pas perdu : il reste dans l'historique des
révisions WordPress de la page 11495.

---

## L'UX Skello, transposée dans la DA Hello Harel

Aucune classe, aucune couleur, aucune police de Skello n'a été reprise : seulement la
**structure de page** et les **mécaniques d'interaction**. Le rendu est en Inter, bleu
`#00B1F5`, CTA vert `#22C55E`, cartes à 24 px — la DA des landings du site.

| Bloc Skello | Ce qu'il devient sur B |
|---|---|
| Hero à deux colonnes, 4 lignes à coche, 2 CTA, ligne de réassurance | H1 de A animé mot à mot, les 4 axes en coches, « Voir sur mes opérations » + « Le module import export », « Édité en France depuis 2014 » |
| Bande de logos défilante + note | Les 14 logos clients réels du site en défilement continu, + 5,0/5 sur 31 avis, + les 4 chiffres du hero de A en cartes |
| **Onglets de fonctionnalités** (le bloc signature) | Les 8 « terrains de vérité » de A regroupés en 4 onglets — Coût de revient · Stock et douane · Marchandise alimentaire · Marge — chacun avec son visuel |
| Sections alternées texte / image | § 01 le calcul (texte + carte chiffrée) et § 03 le terrain (image + texte) |
| Grille de cartes secteurs | Les 5 briques du négoce, image + numéro + description + « En savoir plus » |
| Bandeau CTA final | « Voyez-le sur vos propres conteneurs. » sur fond encre |
| FAQ en accordéon +/− | Les 8 questions de A, ouverture douce, `aria-expanded` tenu |
| Animations au défilement, rotation auto des onglets | Réimplémentées en JavaScript natif — ni jQuery, ni GSAP, ni Webflow |

Le tableau comparatif TMS / ERP généraliste / Hello Harel n'a pas d'équivalent chez Skello.
Il est conservé : c'est un des contenus les plus décisifs de A.

**Rotation des onglets** : toutes les 15 secondes, démarrée à l'entrée en vue, **arrêtée
définitivement au premier clic**. Navigation au clavier par flèches gauche/droite, rôles
ARIA `tablist` / `tab` / `tabpanel` posés.

---

## Images

11 visuels cherchés via l'**API Pexels**, redimensionnés, convertis en **WebP**, déposés dans
la médiathèque avec leur texte alternatif et le crédit photo :
terminal à conteneurs (hero), liasse documentaire, allée d'entrepôt, cagettes de légumes en
camion, analyse de marge, quai de réception, et les 5 visuels de cartes modules.

Le plus lourd pèse **197 ko**, tous les autres sont sous 110 ko — la règle du ticket T7 est
tenue. Les 25 URL d'images de la page ont été testées : **25 en 200**, aucune image morte.
Le mapping est versionné dans `images-negoce-b.json`.

---

## Un défaut corrigé au passage — et c'est un récidiviste

Au premier rendu, la photo du hero restait **invisible en mobile** : le bloc portait
`opacity:0` en attendant son observateur de défilement. C'est exactement le défaut
`scroll-reveal` déjà rencontré sur le site en 07/2026 et inscrit en vigilance dans le
`client.json`.

Corrigé à la racine, par inversion de la logique :

- l'état masqué **n'existe plus par défaut**. Il est écrit sous `.anim-on`, une classe que le
  script pose lui-même. Sans JavaScript, avec un JavaScript en erreur, ou sans
  `IntersectionObserver`, **tout le contenu est visible** ;
- un filet à 4 secondes révèle d'office tout bloc qu'un observateur n'aurait pas déclenché ;
- `prefers-reduced-motion` neutralise l'ensemble.

Vérifié en navigateur réel : **0 bloc invisible** en desktop, en mobile et **JavaScript coupé**.

---

## Contrôles passés

Automatiques, à la publication : équilibre de toutes les balises, 25 images **toutes** issues
de la médiathèque du site et **toutes** pourvues d'un `alt`, aucun lien vers une page protégée
(Règle 0), présence des valeurs du calcul de A (`38 390 €`, `× 1,20`), des 8 questions et des
5 liens de modules, rôles ARIA des onglets et `aria-expanded` de la FAQ.

En navigateur (Chromium, rendu réel) : aucune erreur JavaScript, **aucun défilement
horizontal** en 1440 px comme en 390 px, onglets et accordéon fonctionnels au clic et au
clavier.

---

## Ce qui est en ligne

| Élément | État |
|---|---|
| Page 11495 — variante B | **brouillon**, 404 en anonyme |
| Page 11493 — variante A | **brouillon**, inchangée |
| Extrait 13 — « Noindex sur les pages de test A/B » | **actif** |

L'extrait noindex n'avait **jamais été déposé** : le fichier existait dans le dépôt depuis le
22/08 mais aucun extrait ne le portait sur le site. Il l'est maintenant, **en amont** — filtre
Rank Math, secours `wp_head`, en-tête `X-Robots-Tag` et exclusion du sitemap sur les deux ID.
Aucune publication du test ne peut plus partir sans noindex.

---

## Ce qui reste à trancher avant de lancer le test

1. **Le chrome du site.** Ni A ni B ne portent l'en-tête et le pied de page du site : elles
   sont autonomes, comme A l'était déjà. Pour un test vu par de vrais visiteurs, il faut les
   ajouter **aux deux**, sinon la parité tombe.
2. **Ce qu'on mesure.** Un test A/B a besoin d'un objectif unique et d'un volume. Sur
   `/negoce/`, la demande CRM est le seul événement de conversion — et sa valeur n'est
   toujours pas renseignée (29 demandes à 0 €). Sans elle, le test départagera deux taux de
   clic, pas deux revenus.
3. **L'outil de répartition.** Rien n'est en place pour servir 50/50 et mesurer. À décider :
   un test côté serveur, ou un outil tiers.
4. **La requête cible.** DataForSEO est de nouveau accessible dans cette session : je peux
   mesurer la SERP réelle sur « erp négoce alimentaire » et « erp import export » avant
   publication, ce qui manquait quand A et B ont été construites.
