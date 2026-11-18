# Mettre les 56 mots-clés larges en pause — mode d'emploi

6 octobre 2026 · campagne `HH | Search | ERP x Metiers` (ID 24061100837)

---

## Pourquoi

Les 56 mots-clés en correspondance **large** ont tous déjà leur jumeau en
**exact** ou en **expression** dans le même groupe d'annonces. Vérifié : zéro
orphelin. Tant que les deux coexistent, c'est le large qui rafle les
impressions — et c'est lui qui est allé acheter `logiciels commerciaux`
(64 clics, 41,72 €, zéro conversion), `xero retail` ou `erp codecanyon`.

Les mettre en pause **ne retire aucune requête de la couverture**. Cela retire
seulement le droit de Google d'élargir.

---

## Méthode 1 — dans l'interface, sans fichier (le plus simple, 2 minutes)

C'est la méthode que je te recommande : pas de téléchargement, pas d'import,
et tu vois ce que tu fais.

1. Ouvre la campagne **HH | Search | ERP x Metiers**
2. Menu de gauche → **Audiences, mots clés et contenus** → **Mots clés de recherche**
3. Clique sur **Ajouter un filtre** → **Type de correspondance** → coche
   **Requête large** uniquement → Appliquer
4. Tu dois voir **56 lignes**. Coche la case en haut du tableau pour **tout
   sélectionner**
5. Barre d'actions en haut → **Modifier** → **Suspendre**
6. Retire le filtre et vérifie : il reste **57 mots clés actifs**, tous en
   exact ou en expression

**Point de contrôle :** si l'étape 4 te montre un nombre très différent de 56,
arrête-toi et dis-le-moi — cela voudrait dire que la structure a bougé depuis
ma lecture de cet après-midi.

---

## Méthode 2 — par import, avec le fichier

Fichier : `2026-10-06-ads-mettre-en-pause-les-larges.csv` (56 lignes)

Colonnes : `Campaign, Ad Group, Keyword, Criterion Type, Status`
Toutes les lignes sont `Broad` → `Paused`. **Aucune création**, que des mises en
pause.

### Avec Google Ads Editor

1. Ouvre **Google Ads Editor** → **Compte** → **Ouvrir** → choisis le compte
   Hello Harel → **Obtenir les modifications récentes** (indispensable, sinon
   l'import ne retrouvera pas les mots-clés)
2. Menu **Compte** → **Importer** → **Coller le texte** (ou *Importer depuis un
   fichier* et sélectionne le CSV)
3. Editor affiche un **aperçu des modifications**. Vérifie : **56 modifications,
   0 ajout, 0 suppression**
4. **Appliquer**, puis **Publier**

### Avec l'import en masse du site web

1. **Outils** → **Importations groupées** → **Importations**
2. Dépose le CSV → **Prévisualiser**
3. Vérifie l'aperçu, puis **Appliquer**

---

## Ce qui a déjà été fait aujourd'hui, de mon côté

| Action | État |
|---|---|
| **Partenaires du Réseau de Recherche coupés** | ✔ vérifié : `target_search_network = false` |
| **Réseau Display de cette campagne coupé** | ✔ `target_content_network = false` |
| **Remarketing Display réactivé** (3 €/j) | ✔ `HH \| Display \| RMK Metiers+Contact` passe en ENABLED |
| **17 négatifs en expression** | ✔ posés cet après-midi |
| Action de conversion « Inscription » passée en secondaire | ✔ |

---

## Ce que je n'ai pas pu faire, et qui te revient

**Cinq actions de conversion restent « principales » alors qu'elles
n'enregistrent rien.** Google refuse de les modifier par l'API —
`MUTATE_NOT_ALLOWED` et `IMMUTABLE_FIELD` : ce sont des actions hébergées par
Google ou héritées de campagnes intelligentes, elles ne sont pas modifiables de
l'extérieur.

| Action | Type |
|---|---|
| Calls from Smart Campaign Ads | campagne intelligente |
| Actions locales – Itinéraire | hébergée par Google |
| Appels Directs | hébergée par Google |
| Appels directs via l'annonce d'une campagne intelligente | campagne intelligente |
| Création de compte (Toutes les données du site Web) | **objectif Universal Analytics** — outil arrêté depuis 2023 |

**Le contournement propre** n'est pas de se battre avec ces actions au niveau du
compte, mais de fixer l'objectif **au niveau de la campagne** :

> Campagne **HH | Search | ERP x Metiers** → **Paramètres** → **Objectifs** →
> **Utiliser des objectifs de conversion spécifiques à cette campagne** → ne
> garder que **« Demande de demo - Page Contact »**

C'est ce réglage qui dit à « Maximiser les conversions » sur quoi optimiser.
Tant qu'il n'est pas posé, la stratégie enchérit sur un panier qui contient
« Itinéraire » et un objectif d'un outil éteint.

**Deuxième chose qui te revient : le budget entre groupes d'annonces.** Les
enchères de groupe me sont bloquées aussi.

| Groupe | Coût / conversion |
|---|---|
| Traçabilité & Lots | **12,75 €** |
| ERP Négoce & Grossiste | 39,38 € |

« Traçabilité » convertit trois fois moins cher et reçoit le quart du budget.

---

## À quoi s'attendre dans les jours qui viennent

Les partenaires représentaient **99 % des clics et 100 % des conversions** des
deux dernières semaines. **Le volume va tomber très bas, c'est attendu et c'est
voulu.** Ce qui compte à partir de maintenant :

- les impressions sur **google.com** doivent remonter (elles étaient à 181 sur
  deux semaines, contre 2 285 chez les partenaires) ;
- le **taux d'impressions** doit sortir de 9,99 % ;
- la part perdue **sur le classement** doit descendre sous les 69 % à mesure que
  les niveaux de qualité remontent — c'est l'exact et l'expression qui font ça.

Je propose de **mesurer dans 7 jours** : impressions Search contre partenaires,
taux d'impressions, part perdue sur le classement, coût par conversion.
