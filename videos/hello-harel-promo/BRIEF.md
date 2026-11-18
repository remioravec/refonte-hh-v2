---
workflow: product-launch-video
flow: automation
storyboard: no
message: "Une journée de production agroalimentaire sans Hello Harel coûte en lots perdus, en marge invisible et en coups de téléphone — l'ERP la remet en ordre, écran par écran"
destination: site-web
aspect: 1920x1080
language: fr
audience: "dirigeants et responsables production / qualité / achats de PME agroalimentaires françaises : charcuterie-traiteur, négoce fruits et légumes, transformation, marée"
length: 90s
angle: "journée type — la galère réelle à chaque heure, puis l'écran Hello Harel qui la règle"
style_preset: blue-professional
voice: cjVigY5qzO86Huf0OWal
---

## Intent

Vidéo motion design de promotion pour Hello Harel, éditeur d'ERP agroalimentaire
français (200+ PME équipées). Le film suit **une journée type d'atelier** : à
chaque heure, la galère que vivent réellement les PME du secteur — le camion à
quai sans contrôle à réception, le planning d'ordonnancement sur Excel, la DLC
qu'on découvre trop tard, le client au téléphone pour un prix, le lot à retracer
en urgence, le coût de revient qu'on calcule le mois suivant — et, en réponse
immédiate, **le tableau de bord Hello Harel** qui la règle.

Registre : sobre, industriel, crédible. Pas de clinquant, pas d'humour. La cible
est un dirigeant de PME qui a déjà entendu dix promesses d'éditeur ; ce qui le
convainc, c'est de voir son propre quotidien à l'écran, puis l'outil qui y
répond. La preuve, ici, c'est l'interface.

## Assets

- capture/extracted/dashboards.json — **les 11 tableaux de bord réels du site, en HTML/CSS natif** (`<figure class="ui">`). C'est la matière première du film : ils s'animent image par image, sans capture d'écran.
- capture/dashboards/ui-*.css — les règles CSS qui les stylent, relevées sur le site de production.
- capture/screenshots/*-ui-*.png — une capture de référence par tableau de bord, pour le cadrage.
- capture/screenshots/full-page.png — plaque pleine page de l'accueil, 1920 de large.
- capture/assets/ — 25 images du site (logo, visuels sectoriels, photos atelier).

## Customizations

- Les tableaux de bord sont **repris nativement** (HTML/CSS du site), pas sous forme de captures : chaque écran doit pouvoir s'animer de l'intérieur — ligne qui apparaît, valeur qui monte, alerte qui passe au rouge.
- Horloge de la journée visible en permanence (6h30 → 18h00) : c'est elle qui tient le récit.
- Chaque galère est montrée avant sa solution — jamais de bénéfice annoncé sans la douleur qui le précède.

## Notes

- Police d'affichage **Urbanist**, corps **Inter** — relevées sur le DOM du site, pas supposées.
- Couleur de marque **#00B1F5**, appui **#005F88**, encre **#0F172A**, succès **#22C55E**.
- Aucune promesse chiffrée de performance qui ne vienne pas du site : « 200+ PME » est la seule revendication reprise, elle figure dans le title de l'accueil.
- Pas de visage, pas de signature auteur dans le film.
- Capture réalisée via un miroir HTTP local du site de production : le proxy interne de `hyperframes capture` refuse par conception les IP privées et le HTTP, donc le relevé a été fait avec Playwright sur le DOM réel, puis écrit dans `capture/extracted/`.
