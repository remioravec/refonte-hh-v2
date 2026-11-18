---
name: production
description: "La production hebdomadaire d'Oravec pour un ou plusieurs cabinets clients, en deux pistes qui se rejoignent au QCM de Rémi — Contenu (4 contenus de la semaine pris dans la Roadmap de l'outil : brief, rédaction en pyramide inversée avec infographies interactives, NavBoost, CTA et EEAT, quatre contrôles, brouillon dans le CMS, maillage aux seuils de l'audit 3.3) et Technique (les tickets de la semaine, P1 d'abord) — puis publication, vérification et mise à jour de la Roadmap. Utiliser quand Rémi dit « production », « lance la production », « produis la semaine », « passe les tickets techniques » ou « reprends les brouillons »."
---

# La production de la semaine

Pour chaque cabinet choisi : **les 4 contenus** de la semaine et **tous les tickets techniques** que
la Roadmap de l'outil place sur cette semaine. Deux pistes, Contenu et Technique, préparées en
brouillon, qui se rejoignent au QCM de Rémi ; puis mise en ligne, vérification, Roadmap à jour.

Les règles viennent de la spec 14 § 3 du dépôt `oravec` (elle fait foi ; ce skill en porte la copie
parce qu'il tourne sur le compte claude.ai de Rémi). Construites avec Rémi au QCM du 05/11/2026 ;
version visuelle, règle par règle (A1 à H1) : https://claude.ai/artifact/WsfMhRvsMJJtDexJRm4dZb

## Les règles qui ne se discutent pas

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
   coordonnée ; ils inspirent le texte, jamais cités avec un détail qui identifierait quelqu'un.
3. **La déontologie de chaque profession est dans `deontologie/`** (`avocats.md`, `notaires.md`,
   `experts-comptables.md`, validées par Rémi le 05/11) : la lire avant le premier brief de la
   profession, l'appliquer au contrôle 1. Points durs : avocats — jamais de nom de client ni de
   témoignage élogieux, « spécialiste » réservé au certificat, pas de photo en robe, **les avis
   Google en badge (note et nombre), sans texte d'avis ni lien, avec l'accord écrit du cabinet** ;
   notaires — **aucun référencement payant**, une information utile et retenue, les tarifs
   affichés ; experts-comptables — aucun élément comparatif, aucune information sur un client.
   Simulateurs et quiz : **jamais de promesse de résultat**.
4. **Rien n'est mis en ligne sans le « Publier » de Rémi** : ni page, ni lien, ni balise, ni
   correction technique.
5. **Jamais de mot de passe ni de clé dans la conversation.** Le CMS du cabinet passe par le
   connecteur que Rémi a branché (WordPress, Webflow, ou le site refait par Oravec). Pas de
   connecteur : rien n'est déposé, la ligne est sautée (A5).
6. **Seuls ces outils** : le connecteur Oravec, Légifrance, DataForSEO, la lecture des pages
   publiques, le connecteur du CMS du cabinet, le connecteur Search Console s'il est branché, le
   Drive d'administration@remi-oravec.fr. Aucun outil, aucune donnée, aucun client d'une autre
   structure que celle de Rémi.
7. **Le cabinet ne voit que sa Roadmap** (et le Loom) : le brief, les contrôles et les fiches restent
   internes.

## A · Lancer

1. Appeler `espaces`. Rien ne répond, `401` ou « jeton d'agent refusé » : le connecteur Oravec n'est
   pas branché ; s'arrêter et le dire.
2. **Un QCM** : quel cabinet (un, plusieurs, ou « tous » en premier). Ensuite, **plus aucune
   question** jusqu'au QCM de validation (F).
3. **Lire la Roadmap de l'outil** (`lire_roadmap`) : les lignes de la semaine, roadmap contenu et
   roadmap technique, avec leur page, leur priorité et le lien vers l'annexe de l'audit.
   *Aucune roadmap déposée* (« Aucune roadmap déposée pour cet espace ») : ne rien lire ailleurs ;
   dire à Rémi de la déposer (fin de l'audit, ou reprise d'un ancien classeur), et passer au
   cabinet suivant.
4. **D'abord les brouillons « à reprendre »** de la semaine d'avant, avec la remarque de Rémi ;
   ils comptent dans les 4. Puis **les contenus en haut de la roadmap contenu, jusqu'à 4** (16 par
   mois), et **tous les tickets techniques de la semaine**.
5. **Une ligne bloque** (pas de connecteur CMS, fait impossible à sourcer, cannibalisation,
   règles de profession absentes) : **passer à la ligne suivante** pour tenir le quota, et la
   lister en H.
6. Le netlinking et la fiche Google **ne passent pas par la production**.

## Piste Contenu

### B · Le brief (interne, jamais livré au cabinet)

1. **Le mot-clé, son lot et le dossier visé** : la requête principale, ses requêtes proches
   (`mots_cles`, `positions_mots_cles`), et le type de dossier que la page doit faire signer
   (valeur, situation vécue). On part du dossier.
2. **La cannibalisation** : aucune autre page ne porte la requête ni son lot (`positions_mots_cles`
   donne les pages qui se partagent ses impressions) **et le sitemap du cabinet ne contient aucune
   page sur le sujet** (une page en ligne sans impressions n'apparaît pas dans les positions : lire
   le sitemap XML et les titres des URL proches) ; sinon, ne pas écrire : proposer au QCM une
   seule page (fusion ou recentrage).
3. **La SERP et le top 3** : le top 10 et ses encarts du dernier relevé (aperçu IA et ses sources,
   pack local, autres questions, extrait, vidéos) ; à défaut DataForSEO
   (`serp_organic_live_advanced`, France, langue française). Puis **lire les 3 premières pages** :
   ce qu'elles couvrent, ce qui leur manque, leur ossature.
4. **La cartographie MOFU et les pages sœurs** : le lot de questions avant achat de la requête
   (`lire_strategie`, `besoins_leads`) ; le gabarit des pages sœurs qui signent déjà (`pages`).
5. **Le plan de la page** : la pyramide inversée, la structure, une infographie interactive par section H2, les
   éléments NavBoost, les CTA, l'EEAT, le maillage prévu.

### C · Rédiger

1. **La pyramide inversée** : tout en haut, **la réponse à la question du client en 2 à 3
   phrases**, dans les limites déontologiques, écrite pour être reprise par l'extrait optimisé et
   l'aperçu IA ; puis l'appel ; puis le détail.
2. **La structure** : l'ossature des pages sœurs — **H1 = la requête principale**, formulée comme la
   question ou la situation du client · **H2 = les questions du lot MOFU** · **H3 = les requêtes
   secondaires**, sous leur H2 — **complétée de ce que couvre le top 3 et qui manque**.
3. **Un gabarit par niveau du cocon** : **mère** = la page d'offre (preuve, CTA forts, liens vers ses
   filles) · **fille** = l'offre précisée (un métier, une ville) · **petite-fille** = la réponse
   MOFU de longue traîne, écrite pour les IA.
4. **La longueur** : ce que demandent les questions, **aucune cible de mots**. Chaque question a sa
   réponse complète, rien de plus.
5. **Une infographie entre chaque section (chaque H2)**, en **schéma HTML interactif** dans la DA
   du site (frise de délais, étapes d'une procédure, comparatif) : un bloc de la page, lisible par
   Google et les IA, jamais une image fixe. **Aucun H2 sans son schéma.** Le but : un contenu
   extrêmement qualitatif, agréable à lire, qui retient le visiteur (NavBoost).
6. **NavBoost** (le signal des clics et de l'engagement des visiteurs, décrit au procès DOJ contre
   Google en 2023) : **un simulateur ou calculateur** (coût, délai, sans promesse de résultat),
   **un sommaire cliquable** en haut, **une FAQ dépliable** (les questions MOFU, balisées en FAQ),
   **un quiz « votre situation »** (2 à 4 questions qui orientent vers la bonne page ou le bon
   rendez-vous). **Les quatre modules sur chaque page, quel que soit son niveau du cocon,
   petite-fille comprise.**
7. **Les CTA** : **3 niveaux** — appeler, prendre rendez-vous, poser sa question —, le premier selon
   l'intention de la page, **en haut et en bas**, en boutons.
8. **L'EEAT** : **la carte auteur** (le professionnel qui signe ou relit : photo, barreau ou ordre,
   spécialité, date de mise à jour) · **le badge d'avis Google** (règle 3) · **les sources
   officielles citées en clair, sans lien** (« article 1240 du Code civil »), vérifiées par
   Légifrance.
9. **Le title, la description et les données structurées** (le cabinet, la FAQ, le fil d'Ariane)
   s'écrivent en même temps que le texte.

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

### E · Mettre en brouillon et mailler

1. **Le brouillon dans le CMS** du cabinet, dans le gabarit de son niveau, avec ses balises et ses
   données structurées.
2. **Les seuils de l'audit 3.3** : page **mère 11 liens entrants et 11 ancres différentes**, **fille 11
   et 11**, **petite-fille 5 et 5** ; **3 clics au plus** depuis l'accueil ; **aucune orpheline** ;
   **aucune ancre cannibale** (une ancre ne vise jamais deux pages, vérifier avec `maillage`). Le site
   n'a pas assez de pages pour tenir 11/11 : **ne pas baisser le seuil** — proposer les pages
   manquantes à créer (`proposer_pages`), elles entrent dans la roadmap contenu.
3. **Le « surfer raisonnable »** (brevet Google : un lien dans le contenu, visible et pertinent,
   pèse plus qu'un lien de pied de page) : **les liens dans le texte**, le plus important **tôt**,
   dans les premiers paragraphes ; **des ancres semi-optimisées, toutes différentes** (jamais
   d'exact match systématique) ; **la mère vers ses filles**, chaque fille vers sa mère, les sœurs
   entre elles ; **un seul lien d'une page vers une même page**. **Aucun lien sortant.**
4. Les liens entrants sont **préparés en brouillon sur leurs pages de départ** et proposés à l'outil
   (`proposer_liens`, avec l'ancre et la raison) ; la page nouvelle aussi (`proposer_pages`).

## Piste Technique

### T · Les tickets de la semaine

1. **Les tickets de la semaine**, dans l'ordre de la roadmap technique : **P1** (ce qui empêche
   Google de voir la page) → **P2** (ce qui la prive de sa force) → **P3** (ce qui l'empêche de la
   comprendre) → **P4** (les contrôles). Chacun avec **son annexe de l'audit**.
2. **Ce que l'agent prépare lui-même dans le CMS** :
   - **erreurs et redirections** : 404 → redirection 301 vers la bonne page, chaînes de redirection
     raccourcies, noindex retiré d'une page utile, canoniques fausses ou absentes ;
   - **balises et données structurées** : title, description, H1, Schema (cabinet, FAQ, fil
     d'Ariane), page par page selon l'annexe ;
   - **le plan de maillage** : les liens de l'annexe (URL source → URL destination, ancre), les
     orphelines reliées, les pages trop profondes remontées, aux règles de E2 et E3 ;
   - **le menu, le pied de page, le fil d'Ariane** de l'audit 3.3, et **les maquettes intégrées**
     dans le gabarit.
3. **Ce qu'il ne peut pas faire seul** (vitesse, développement, hébergeur, CMS sans connecteur) :
   **une fiche d'intégration** pour le webmaster du cabinet — avant / après, où, comment, comment
   vérifier — ; le ticket passe **« bloqué »** dans la Roadmap jusqu'à la pose.
4. **Contrôler** : chaque correction montrée **avant / après** (les pages touchées, la valeur avant
   et après) ; aucune correction ne casse une page qui signe (`pages`), ni ne crée d'orpheline ou
   d'ancre cannibale.

## F · Le QCM de Rémi

Pour chaque cabinet, **les contenus d'abord, puis les tickets**, au plus 4 par question, autant de
questions que nécessaire :

- un contenu : son lien d'aperçu du brouillon, le dossier visé, la requête, les contrôles passés ou
  le passage retiré, les liens entrants préparés ;
- un ticket : sa priorité, les pages touchées, **avant / après** ;
- réponses **« Publier »**, **« À reprendre »**, **« Plus tard »**. « À reprendre » : demander ce qui
  ne va pas en une phrase ; il sera réécrit avec cette remarque au lancement suivant.

Les liens entrants et les balises suivent le choix de leur contenu. Reporter les choix dans l'outil
(`statuer_production` : les pages et les liens passent « validés » ou « refusés »).

## G · Publier, vérifier, mettre à jour

1. **Mise en ligne tout de suite** après le « Publier » : la page, ses liens entrants, ses balises,
   les corrections techniques.
2. **Vérifier**, sur la page en ligne :
   - elle **répond et est indexable** : code 200, pas de noindex, canonique sur elle-même, présente
     dans le sitemap ;
   - **Search Console** : l'inspection d'URL (découverte, explorée, indexée) par le connecteur
     Search Console s'il est branché ; sinon, la relire au reporting suivant, et le dire ;
   - **la mesure et les liens** : le formulaire et le numéro suivis par l'outil, les liens entrants
     en ligne avec leur ancre ;
   - **le ticket corrigé** : la 404 redirige, la balise a changé, le lien est posé.
3. **La Roadmap de l'outil** (`statuer_roadmap`) : chaque ligne passe **« en ligne »** avec son
   adresse, ou **« bloquée »** avec sa raison ; un ticket corrigé passe **« terminé »**.
4. `marquer_pose` (page « en ligne » avec son adresse, liens « posés ») ; la page « en ligne » dans
   le cocon (`regler_cocon`) ; son lot de mots-clés « en test ». Le reporting suivant les mesure.

## H · Rendre la main

Pour chaque cabinet, en quelques lignes : ce qui est en ligne (avec les adresses) · ce qui attend
(« à reprendre », « plus tard », « bloqué » et pourquoi) · les lignes sautées et la raison · ce qui
manquait (connecteur, règles de profession, chiffres du cabinet) · les liens entrants posés par page.

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
