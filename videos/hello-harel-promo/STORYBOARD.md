---
format: 1920x1080
duration: 92.5s
message: "Une journée de production agroalimentaire coûte en lots perdus, en marge invisible et en coups de téléphone — Hello Harel la remet en ordre, écran par écran"
arc: 6h30 l'accroche → la galère de chaque heure, suivie de son écran → 18h00 la marge enfin lisible → preuve et demande de démo
audience: "dirigeants et responsables production / qualité / achats de PME agroalimentaires françaises"
mode: autonomous
music: calm-building-corporate
---

## Frame 1 — 6h30, le camion est à quai

- scene: Horloge 6h30 en gros chiffres, quai de réception en aplats, le titre tombe
- duration: 8s
- poster: 5.0s
- transition_in: cut
- status: animated
- voiceover: "Six heures trente. Le camion est à quai. À partir de maintenant, tout ce que vous ne mesurez pas vous coûte quelque chose."
- src: compositions/frames/01-0630-quai.html
- blueprint: kinetic-title
- assets: horloge de journée (6h30), aplats cyan #00B1F5 sur encre #0F172A

L'accroche. Pas de promesse, pas de logo : une heure, un quai, une menace. On
installe l'horloge de la journée, qui restera à l'écran jusqu'à la fin et qui
porte tout le récit. Le film ne dit pas encore qui parle.

## Frame 2 — Le contrôle à réception se fait sur un carnet

- scene: Carnet / stylo en silhouette, une ligne « DLC restante 5 jours » surlignée, puis l'écran Contrôle à réception se substitue au carnet et passe la ligne hors tolérance au rouge
- duration: 10s
- poster: 6.2s
- transition_in: crossfade
- status: animated
- voiceover: "Le contrôle à réception, vous le faites sur un carnet. Huit jours de DLC exigés, cinq jours livrés : personne ne le verra avant la cuisson."
- src: compositions/frames/02-reception.html
- blueprint: before-after-swap
- assets: dashboard #0 Contrôle à réception (549×312, HTML natif), capture/screenshots/negoce-ui-0-*.png
- dashboard_native: true

Première galère, et la plus chère : la non-conformité qui entre dans le stock.
L'écran réel du produit pose les trois points de contrôle et fait passer le
troisième hors tolérance — la donnée affichée est celle du site (DLC restante à
réception, ≥ 8 jours exigés, 5 jours constatés). Rien n'est inventé.

## Frame 3 — Personne ne sait ce qu'il y a, ni où

- scene: Quatre lieux en pastilles dispersées (entrepôt, deux dépôts, carreau), les quantités clignotent sans se réconcilier ; l'écran Stock consolidé les rassemble en une colonne
- duration: 8.5s
- poster: 5.3s
- transition_in: cut
- status: animated
- voiceover: "Huit heures quinze. L'entrepôt, deux dépôts, le carreau. Quatre endroits, quatre vérités, et un seul client qui attend sa palette."
- src: compositions/frames/03-stock-eclate.html
- blueprint: scatter-to-grid
- assets: dashboard #1 Stock consolidé (446×870, HTML natif)
- dashboard_native: true

La galère multi-sites. Le mouvement dit tout : du dispersé vers le consolidé.
Le dashboard entre par la droite et absorbe les pastilles.

## Frame 4 — La DLC, on la découvre en prenant le bac

- scene: Deux écrans côte à côte sous le titre — Dates limites (FEFO / FIFO) à gauche, Emplacements à droite avec une chambre hors consigne
- duration: 11s
- poster: 6.8s
- transition_in: crossfade
- status: animated
- voiceover: "Dix heures. La date limite, vous la découvrez en prenant le bac. Au plus près de la DLC d'abord : c'est une règle, pas une habitude — et elle se tient toute seule."
- src: compositions/frames/04-dlc-fefo.html
- blueprint: stacked-reveal
- assets: dashboard #5 Dates limites (541×521), dashboard #7 Emplacements (541×585), tous deux HTML natifs
- dashboard_native: true

Le cœur métier. FEFO / FIFO sont les mots du site, pas du marketing. Emplacements ajoute la température : trois chambres suivies, une hors consigne.
Deux écrans de même hauteur, centrés sous le titre — l'incrustation initiale
masquait la table « À prélever en priorité » de l'écran principal.

## Frame 5 — Le client appelle pour un prix

- scene: Un combiné, trois onglets de messagerie qui s'ouvrent en vain, puis la Fiche client qui pose historique, encours et tarif en un seul plan
- duration: 8s
- poster: 5.0s
- transition_in: cut
- status: animated
- voiceover: "Onze heures trente. Un grossiste veut son prix. Vous cherchez dans vos mails ce que votre ERP devrait afficher en une ligne."
- src: compositions/frames/05-fiche-client.html
- blueprint: search-to-answer
- assets: dashboard #8 Fiche client (541×653, HTML natif)
- dashboard_native: true

La galère commerciale. Elle est moins spectaculaire que le rappel mais elle
arrive tous les jours. Le contraste visuel : trois fenêtres qui se ferment,
un écran qui reste.

## Frame 6 — Le rappel. Trois heures de classeurs.

- scene: Pic du film. Un lot de terrine au centre ; des classeurs s'empilent et noircissent le cadre, puis l'arbre de traçabilité se déploie — trois matières premières en amont, trois clients en aval, en une seconde
- duration: 11.5s
- poster: 7.1s
- transition_in: wipe
- status: animated
- voiceover: "Quatorze heures. Un rappel. Il faut remonter un lot de terrine à ses matières premières et redescendre à ses clients. Au classeur, c'est l'après-midi. Ici, c'est quelques secondes."
- src: compositions/frames/06-tracabilite-rappel.html
- blueprint: tree-expand
- assets: dashboard #4 Traçabilité (392×871, HTML natif) — lot de terrine, 3 matières premières amont, 3 clients aval
- dashboard_native: true

Le sommet du film, et le seul endroit où l'on tient douze secondes. « Rappel
produit en quelques secondes » est la formulation du site ; on la montre au lieu
de l'écrire. L'arbre se déploie amont puis aval, avec une pause entre les deux.

## Frame 7 — La commande arrive, on la retape

- scene: Un bon de commande scanné, un curseur qui retape ligne à ligne ; l'écran Flux EDI prend sa place, les messages défilent, une anomalie se signale et se résout
- duration: 9.5s
- poster: 5.9s
- transition_in: crossfade
- status: animated
- voiceover: "Quinze heures trente. La commande du partenaire arrive, et quelqu'un la retape. Chaque ressaisie est une erreur qui attend son tour."
- src: compositions/frames/07-edi.html
- blueprint: pipeline-flow
- assets: dashboard #3 Flux EDI (438×871, HTML natif)
- dashboard_native: true

La galère invisible, celle que personne ne chiffre. Le mouvement est un flux :
de gauche à droite, sans rupture.

## Frame 8 — Facturé au poids commandé, pas au poids livré

- scene: Deux colonnes côte à côte — poids commandé / poids pesé — l'écart se surligne, puis l'écran Facture pose quatre lignes au poids réellement livré et le total
- duration: 9s
- poster: 5.6s
- transition_in: cut
- status: animated
- voiceover: "Seize heures trente. Un ERP généraliste facture le poids commandé. Vous avez livré autre chose. L'écart, vous le payez sans jamais le voir."
- src: compositions/frames/08-facture-poids.html
- blueprint: comparison-columns
- assets: dashboard #9 Facture (541×307, HTML natif) — quatre lignes au poids réellement livré
- dashboard_native: true

L'argument différenciant du site, repris mot pour mot dans l'esprit : « un ERP
qui facture au poids réellement pesé, là où un ERP généraliste facture au poids
commandé ». C'est le poids variable, la signature du secteur.

## Frame 9 — 18h00. La marge, enfin lisible.

- scene: L'horloge atteint 18h00 ; l'écran Coût de revient décompose le coût au kilo en quatre postes, puis l'écran Marge glisse à côté et le taux s'inscrit
- duration: 9s
- poster: 5.6s
- transition_in: crossfade
- status: animated
- voiceover: "Dix-huit heures. Le coût de revient au centime, poste par poste. Et la marge du jour, aujourd'hui — pas le mois prochain."
- src: compositions/frames/09-cout-marge.html
- blueprint: metric-reveal
- assets: dashboard #6 Coût de revient (541×492), dashboard #2 Marge (444×871), tous deux HTML natifs
- dashboard_native: true

La résolution. « Coût de revient au centime près » est la formule du site. Les
deux écrans cohabitent : la décomposition à gauche, le taux à droite. C'est le
seul moment du film où l'on respire.

## Frame 10 — 200 PME, et votre atelier

- scene: Plan sur fond encre, en miroir de l'ouverture. Le logo Hello Harel se pose, le compteur monte jusqu'à 200+, puis « Demander une démo » et helloharel.com
- duration: 8s
- poster: 5.0s
- transition_in: wipe
- status: animated
- voiceover: "Plus de deux cents PME agroalimentaires françaises travaillent déjà comme ça. Hello Harel. Demandez une démo."
- src: compositions/frames/10-preuve-cta.html
- blueprint: logo-sting
- assets: assets/img/logo.svg (logo Hello Harel, blanc d'origine), compteur 0 → 200+
- dashboard_native: false

La seule revendication chiffrée du film, et elle vient du title de l'accueil
(« 200+ PME »). Pas de pourcentage de gain, pas de ROI promis : le site n'en
porte pas, le film n'en inventera pas.

Le fond est encre parce que **le logo que le site expose est entièrement blanc** :
il est fait pour un bandeau sombre. Le poser sur blanc l'aurait rendu invisible ;
le recolorer aurait été une décision de marque qui ne m'appartient pas. Le plan
sombre règle les deux, et referme le film sur l'image qui l'a ouvert.


---

## Video direction

**Le principe.** Une seule idée tient tout le film : *la galère d'abord, l'écran
ensuite*. Jamais l'inverse, jamais un bénéfice annoncé sans la douleur qui le
précède. Le spectateur doit reconnaître sa journée avant de voir un produit.

**L'horloge est le fil.** Une pastille en haut à gauche donne l'heure à chaque
plan (06:30 → 18:00) et une barre de progression de la journée court en bas du
cadre, de 0 % à 100 %. Elle avance *pendant* chaque plan, jamais entre deux :
c'est le seul mouvement continu du film, et il dit que la journée passe.

**La grille.** Colonne de gauche pour le texte (690 px), colonne de droite pour
l'écran produit, centré verticalement dans sa bande. Deux plans dérogent — le 4
et le 9 — parce qu'ils portent deux écrans : le titre passe centré au-dessus,
les deux écrans sont mis à la même hauteur et centrés dans la largeur.

**Le mouvement.** Quatre gestes, pas un de plus :

| Geste | Où | Durée |
|---|---|---|
| Montée du texte, en cascade | eyebrow → titre → accroche → pavé galère | 0,5 à 0,75 s, `power3.out` |
| Entrée de l'écran par la droite | le tableau de bord, avec un léger `scale` | 0,95 s |
| Révélation interne | tuiles KPI, puis lignes de tableau en cascade de 90 ms | 0,34 à 0,45 s |
| Battement d'alerte | la ligne hors tolérance, en liseré rouge, aller-retour | 0,5 s, une fois |

Puis la pastille verte de réponse, en `back.out`, au dernier tiers du plan.
Rien d'autre ne bouge. Le film est sobre parce que la cible l'est.

**Les écrans sont réels.** Les 11 tableaux de bord sont le HTML et le CSS du
site de production, pas des captures : leurs lignes, leurs chiffres et leurs
alertes s'animent de l'intérieur. La mention « écran réel du produit » figure en
bas de chaque plan concerné — c'est une promesse qu'on peut tenir.

**Les couleurs.** Le cyan de marque `#00B1F5` porte les aplats, les pastilles et
la barre de journée. Le texte, lui, est en `#0079B8` — qui est la couleur de
l'interface du produit elle-même (`--c`) et qui, elle, passe le contraste AA sur
blanc. Le cyan pur ne le passe pas (2,44:1) : l'utiliser en texte aurait été une
faute de lisibilité, pas une fidélité à la marque.

**Les deux plans sombres** — l'ouverture et la clôture — encadrent le film. Entre
les deux, tout est blanc : c'est la journée.
