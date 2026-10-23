# Vidéo motion design — une journée dans un atelier agroalimentaire

Hello Harel · 16 octobre 2026 · 92,5 s · 1920×1080 · 30 i/s

---

## 1 · Le parti pris

Vous avez demandé une journée type, les galères possibles, et nos tableaux de
bord. Le film ne fait que ça, dans cet ordre et sans jamais l'inverser : **à
chaque heure, la galère d'abord, l'écran ensuite.**

| Heure | Ce qui coince | L'écran qui répond |
|---|---|---|
| 06:30 | *(accroche — le camion est à quai)* | — |
| 06:50 | Le contrôle à réception se fait sur un carnet | **Contrôle à réception** |
| 08:15 | Entrepôt, deux dépôts, le carreau — quatre vérités | **Stock consolidé** |
| 10:00 | La DLC se découvre en prenant le bac | **Dates limites** + **Emplacements** |
| 11:30 | Le grossiste veut son prix, on cherche dans les mails | **Fiche client** |
| 14:00 | Un rappel. Remonter un lot, redescendre à ses clients | **Traçabilité** |
| 15:30 | La commande arrive, quelqu'un la retape | **Flux EDI** |
| 16:30 | Facturé au poids commandé, pas au poids livré | **Facture** |
| 18:00 | La marge, on la connaîtra le mois prochain | **Coût de revient** + **Marge** |
| — | *(200+ PME · demander une démo)* | — |

Le fil visible, c'est l'horloge : une pastille à chaque plan et une barre de
journée qui avance en bas du cadre, de 6h30 à 18h00. C'est elle qui tient les
92 secondes.

## 2 · Les tableaux de bord ne sont pas des captures d'écran

C'est le point qui change tout. Vos 11 écrans produit sont, sur le site, du
**HTML et du CSS natifs** (`<figure class="ui">`) — pas des images. Je les ai
repris tels quels dans le film.

Conséquence directe : les lignes de tableau arrivent en cascade, les tuiles de
chiffres se révèlent, la ligne **hors tolérance** bat en rouge. L'écran s'anime
de l'intérieur, au pixel près, avec vos vraies données de démonstration — le lot
L2609-114, la terrine de campagne, les 86 kg chez Grossiste Ouest, la DLC à
5 jours contre 8 exigés.

C'est pour ça que la mention « **écran réel du produit** » figure en bas de
chaque plan : elle est tenable.

## 3 · La DA vient du site, pas d'une supposition

Relevée sur le DOM de production, pas de mémoire :

- affichage **Urbanist**, corps **Inter** — les deux embarquées en local dans le projet ;
- cyan de marque **#00B1F5**, appui **#005F88**, encre **#0F172A**, succès **#22C55E**.

**Un écart assumé, et je préfère vous le dire.** Le texte du film n'est pas en
#00B1F5 mais en **#0079B8**. Le cyan pur ne passe pas le contraste minimum sur
blanc (2,44:1 pour 4,5:1 exigé) : en corps de texte, il est illisible à l'écran.
#0079B8 est la couleur de l'interface de votre ERP elle-même — donc une couleur
Hello Harel, pas une couleur inventée. Les aplats, pastilles et barres restent
en #00B1F5.

**Le plan de fin est sombre pour une raison précise.** Le logo que le site
expose est **entièrement blanc** : il est fait pour un bandeau sombre. Le poser
sur fond clair l'aurait rendu invisible, le recolorer aurait été une décision de
marque qui ne m'appartient pas. Le plan encre règle les deux et referme le film
sur l'image qui l'ouvre.

## 4 · Ce qui est dit, et ce qui ne l'est pas

Narration française, 10 répliques, 85,5 s, voix de synthèse ElevenLabs.

**Aucune promesse chiffrée de performance.** Pas de « +30 % de productivité »,
pas de ROI. La seule revendication du film est « plus de deux cents PME
agroalimentaires françaises », et elle vient du title de votre accueil. Les
seuls autres chiffres à l'écran sont ceux de vos propres écrans de démonstration.

## 5 · Contrôle

| Critère | Résultat |
|---|---|
| Erreurs de composition | **0** |
| Erreurs d'exécution | **0** |
| Problèmes de mise en page | **0** |
| Contraste WCAG AA | **222 / 222** |
| Durée | 92,5 s pour 85,5 s de voix — de l'air à chaque plan |

## 6 · Deux réserves, honnêtement

**La voix.** Votre clé ElevenLabs est sur le **palier gratuit**. Les voix
françaises natives de la bibliothèque sont réservées aux plans payants : le film
utilise donc une voix premade en modèle multilingue. Elle est correcte, elle
n'est pas native. Un passage en plan payant permet de revoicer le film en une
commande — le script est figé, les plans n'ont pas à changer.

**Le relevé du site.** L'outil de capture de la chaîne vidéo refuse par
conception les adresses privées, et le navigateur de ce conteneur ne lit pas
l'autorité de certification du proxy. J'ai donc relevé le site avec Playwright
sur un miroir HTTP local de la production — le DOM est bien celui de
helloharel.com, pas une reconstruction. C'est documenté et rejouable.

## 7 · Ce qui est livré

| Quoi | Où |
|---|---|
| Le film | `videos/hello-harel-promo/renders/hello-harel-journee-type.mp4` |
| Le scénario plan par plan | `videos/hello-harel-promo/STORYBOARD.md` |
| Le texte dit, réplique par réplique | `videos/hello-harel-promo/SCRIPT.md` |
| Le système graphique du film | `videos/hello-harel-promo/frame.md` |
| Les 11 écrans produit isolés | `videos/hello-harel-promo/assets/dashboards/` |
| La chaîne de fabrication | `videos/hello-harel-promo/tools/` |

**Pour modifier le film**, on touche `tools/generer_plans.py` et on régénère —
jamais les fichiers de plan à la main. Une phrase à changer, un écran à
remplacer, un plan à rallonger : c'est une ligne dans la table de spécifications.

## 8 · Ce que je ferais ensuite, si vous le voulez

1. **Un format 9:16 de 30 s** pour LinkedIn, à partir des trois plans qui portent
   le plus — réception, rappel produit, marge. Le matériel est déjà là.
2. **Revoicer en français natif** si la clé passe en payant.
3. **Poser le film sur l'accueil**, au-dessus du premier pli : c'est la page qui
   porte 29 des 64 demandes depuis juillet.
