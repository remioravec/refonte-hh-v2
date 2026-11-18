# Mise à jour du skill `production` — 18/11/2026

Tirée de la production de `/agroalimentaire/` (ligne 1 de la roadmap du 16/11).
Maquette de référence : https://claude.ai/artifact/CJ8eHttAAiupvF2Qmx52bu

## Où ça doit être reporté

Le skill dit lui-même que **la spec 14 § 3 du dépôt `oravec` fait foi** et que le fichier du skill
n'en est qu'une copie. Les trois blocs ci-dessous sont donc à reporter **dans la spec**, puis dans
le skill publié sur claude.ai. La copie locale de la session a été patchée pour prendre effet tout
de suite, mais elle est dans `skills/synced/` : **elle sera écrasée à la prochaine synchronisation.**

## Ce qui change, en une ligne chacun

1. Règle 1 — chercher dans le site avant d'écrire « à compléter par le cabinet ».
2. Nouveau temps **C bis · La preuve et la conversion**, entre la rédaction et les contrôles.
3. Les contrôles passent de quatre à **cinq** (le cinquième porte la preuve et la lecture rapide).
4. Nouvelle **annexe · Le rendu de la page**.

---

## 1 · Règle 1, complétée

```markdown
1. **Aucun chiffre inventé**, ni sur le cabinet (avis, dossiers, années), ni sur le droit (délais,
   montants, articles). Chaque fait porte sa source publique datée ; **chaque article de loi ou de
   règlement est vérifié dans sa version en vigueur par le connecteur Légifrance**. Sans ce
   connecteur : le fait est marqué « à vérifier » dans le brouillon, et le dire. Un chiffre du
   cabinet inconnu s'écrit « à compléter par le cabinet », ou le bloc ne s'affiche pas.
   **Avant d'écrire « à compléter », lire le pied de page, la page contact et l'accueil du
   site** : le téléphone, l'adresse, l'ancienneté, la note d'avis, les logos clients et le nom
   de l'interlocuteur commercial y sont presque toujours déjà publiés. Un « à compléter » posé
   sur une donnée qui était à deux clics est une faute, pas une précaution.
2. **Aucune coordonnée de prospect.** Les mots des prospects viennent de `besoins_leads`, sans
```

## 2 · Nouveau temps C bis

```markdown
### C bis · La preuve et la conversion

**Rien de ce temps ne se pose sans la fiche de la profession** (règle 3). Chez les avocats, pas de
témoignage élogieux ni de nom de client ; chez les experts-comptables, aucun élément comparatif ni
information sur un client ; chez les notaires, pas de référencement payant. Sur ces professions, ce
temps se réduit au badge d'avis autorisé, à l'ancienneté et aux sources officielles. Partout
ailleurs, il s'applique en entier.

1. **La preuve sociale ne s'invente pas, elle se récolte.** Elle est presque toujours déjà publiée
   par le cabinet : avis avec leur texte, logos clients, note et nombre d'avis, année de création,
   nom et photo de l'interlocuteur. On la reprend **mot pour mot**, attribuée comme à la source.
   Une parole de client reste une parole de client : « en 3 jours nous étions opérationnels » se
   cite entre guillemets avec son auteur, et **ne devient jamais une promesse du cabinet**.
2. **Elle se place aux moments de décision, pas en bas de page.** Un avis répond à l'objection qui
   vient de se poser : le témoignage sur les délais après le bloc des délais, celui sur les marges
   après le calculateur. Un bloc d'avis relégué en pied de page ne convertit personne.
3. **Une relance en plein texte après chaque preuve.** Deux lignes qui nomment ce qu'on propose et
   ce que ça coûte en temps, un bouton, et le numéro. Le moment le plus chaud de la page est
   l'instant qui suit le simulateur : c'est là que la relance est obligatoire.
4. **Lever le risque à côté de chaque bouton**, en une ligne de faits vérifiables : durée du
   rendez-vous, absence d'engagement, ce qu'il n'y a pas à installer, ce qui est préparé à l'avance.
5. **Un visage et un numéro réels au pied de page.** Qui prend l'appel, avec sa photo et sa
   fonction. Un pied de page de conversion sans personne nommée se lit comme un formulaire.
6. **Les chiffres contradictoires ne se tranchent pas tout seuls.** Si le site annonce deux nombres
   de clients différents, aucun des deux ne sort : la question part au QCM.

```

## 3 · D · Contrôler, cinq contrôles

```markdown
### D · Contrôler

Cinq contrôles sur chaque contenu :

1. **Déontologie et faits sourcés** : la fiche de la profession ; chaque article vérifié en vigueur.
2. **SEO de la page** : la requête et son lot, les Hn, le title et la description, les données
   structurées, aucune cannibalisation, la réponse en tête.
3. **Ton et intention de dossier** : le ton du cabinet fixé à l'onboarding ; la page mène à un type
   de dossier précis.
4. **Mesure et rendu** : le formulaire et le numéro de la page sont suivis par l'outil ; une capture
   téléphone et ordinateur du brouillon, sans défaut d'affichage ; **chaque schéma et chaque module
   (simulateur, quiz, FAQ, sommaire) testé au clic sur téléphone** ; aucun débordement horizontal,
   aucune erreur de console, et chaque module reste lisible **sans JavaScript**.
5. **Preuve et lecture rapide** : chaque élément de preuve porte sa source ; le surlignage compte
   **10 à 14 phrases**, pas davantage, aucune dans un avertissement ou une mention ; une relance
   suit le simulateur ; le numéro affiché est le vrai.

Un contrôle raté : **corriger et repasser, deux fois au plus** ; s'il échoue encore, retirer le
passage et le signaler en tête du brouillon.

```

## 4 · Annexe · Le rendu de la page

```markdown
---

## Annexe · Le rendu de la page

La forme n'est pas un habillage : c'est elle qui fait qu'une page se lit en six secondes. Elle suit
la DA du cabinet, et à l'intérieur de cette DA, ces règles valent pour tous.

### Ce qui doit être visible sans lire

- **Un pictogramme par H2**, au même gabarit, repris à l'identique dans le sommaire : le lecteur
  retrouve la section où il va.
- **Une image par grand moment**, prise **chez le cabinet** et nulle part ailleurs, avec une légende
  qui argumente au lieu de décrire. Pas d'image générée, pas de banque d'images.
- **Les schémas se dessinent.** Une chaîne de traçabilité est une chaîne avec ses maillons, pas une
  rangée de boutons. Un calcul a sa barre qui bouge quand on change les valeurs.
- **Le surlignage, à deux niveaux** : le fond marqueur pour ce qu'il faut retenir, et un second
  niveau — un soulignement — pour les **quatre phrases qui décident**. Les phrases surlignées
  reprennent **les mots de la cible** : ceux des demandes reçues (`besoins_leads`), ceux des avis
  publiés, les mots-clés de la roadmap. Jamais un surlignage par goût.
- **La couleur est rare.** Dans une DA monochrome, elle ne sert qu'au moment fonctionnel : la valeur
  qui alerte, la part qui compte dans un graphique, le lien qu'il faut suivre.

### Le bandeau de brouillon

Tout brouillon livré à Rémi porte en tête un bandeau interne, qui ne part jamais en ligne :

- la ligne de roadmap d'où il vient (page, niveau, mot-clé) ;
- les cinq contrôles et leur état, ceux qui restent ouverts en évidence ;
- **le title et la description avec leur largeur mesurée** et les bornes ;
- le compte des liens sortants et des ancres, face au seuil du niveau ;
- une **bascule pour masquer le surlignage**, afin de relire la page comme la lira un visiteur.

### Les quatre modules, dans leur forme

| Module | Forme attendue |
|---|---|
| Sommaire | en pilules cliquables, avec le pictogramme de chaque section |
| Simulateur | des champs réels, un résultat chiffré **et sa visualisation qui bouge** |
| FAQ | dépliable, balisée, les questions dans les mots des demandes reçues |
| Quiz | 2 à 4 questions, une sortie nommée, **et un bouton de rendez-vous dans la sortie** |

### Ce qui disqualifie un brouillon

Un chiffre sans source. Un « à compléter » posé sans avoir lu le pied de page du site. Un H2 sans
son schéma. Un avis inventé ou reformulé. Une promesse de résultat dans un simulateur. Un
surlignage sur un avertissement. Une page qui explique sans jamais demander le rendez-vous.
```
