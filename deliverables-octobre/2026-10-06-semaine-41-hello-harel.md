# Semaine du 12/10/2026 — contenu, technique, sitemap

Hello Harel · 6 octobre 2026 · [roadmap](https://docs.google.com/spreadsheets/d/1SImCHCu7gmSW3aIKTmu_jAhbukPeOv0U3_ONS-96_hM/edit)

---

## Ce qui était au programme

Trois lignes datées du 12/10/2026 dans l'onglet ROADMAP CONTENU :

| Requête | Production prévue | URL prévue |
|---|---|---|
| logiciel import export agroalimentaire | Mise à jour | `/fonctionnalites/import-export/` |
| logiciel de gestion commerciale import export | **Création** | `/fonctionnalites/import-export-gestion-commerciale/` |
| logiciel devis commande bon de livraison | Mise à jour | `/fonctionnalites/logiciel-devis-commande-bon-livraison/` |

---

## La ligne 2 n'a pas donné lieu à une création — et c'est volontaire

Anti-cannibalisation, Search Console sur 90 jours (08/07 → 03/10), requête
`logiciel gestion commerciale import export` :

| Page | Position | Impressions |
|---|---|---|
| `/blog/meilleurs-erp-import-export/` | **9,7** | 134 |
| `/fonctionnalites/import-export/` | 34,3 | 21 |

**Deux pages se partagent déjà la requête.** En créer une troisième l'aurait
partagée entre trois URL, dont celle qui est à une marche du top 5. Verdict
**FORT** : on renforce la page qui capte, on n'en crée pas une seconde.

La ligne est servie par une mise à jour de `/blog/meilleurs-erp-import-export/` :
balisage à l'exact match, et quatre liens entrants éditoriaux là où la page
n'en recevait que trois. L'onglet ROADMAP CONTENU porte la correction —
production « Mise à jour », URL corrigée, statut TERMINE.

Les trois requêtes de la semaine sortent par ailleurs **sans volume mesurable**
dans Google Ads (France, français). Les variantes mesurées existent :
`logiciel import export` 10/mois, `erp import export` 10/mois,
`logiciel bon de livraison` 20/mois. C'est le septième lot de requêtes de
roadmap dans ce cas ; le sujet mérite d'être tranché avant le reste d'octobre.

---

## Ce que dit la SERP, et l'angle retenu

Relevé du 06/10/2026, France, français.

**`logiciel import export agroalimentaire`** — Hello Harel est **absent du
top 10**. Les cinq premiers : un dossier Agro Media, la page ERP agro de
Captivea, deux annuaires Capterra, un billet de 2024 sans rien de spécifique.
**Aucun ne tient l'intersection import-export × agroalimentaire.**

**`logiciel de gestion commerciale import export`** — les positions 1 à 3 sont
Akanea TMS Freight Forwarding, Trade Easy et Dashdoc : du transport, pas un
seul qui sache ce qu'est un lot alimentaire. Hello Harel est 7e organique
(`rank_absolute` 9, AI Overview au-dessus du premier résultat).

**`logiciel devis commande bon de livraison`** — SERP faible : revendeurs EBP,
une fiche produit au format PDF, un billet de 2014, une page de matériel
médical. Personne ne la tient.

**Angle (plus démontré)** — deux contraintes que personne ne couvre :
un lot alimentaire importé arrive avec une DLC déjà lancée et un document
sanitaire attaché, et il se facture au poids débarqué, pas au poids commandé.

---

## Ce qui est en ligne

### `/fonctionnalites/import-export/` — [page](https://www.helloharel.com/fonctionnalites/import-export/)

- **H1** : « Le logiciel import export agroalimentaire qui calcule vos frais
  d'approche au kilo débarqué » (exact match, différent du title)
- **accroche** qui répond dès la première phrase, exact match dans les six
  premiers mots
- **réponse encadrée en une phrase**, extractible hors contexte
- **fait daté et sourcé** : valeur en douane = valeur transactionnelle majorée
  du transport et de l'assurance jusqu'au point d'entrée dans l'Union — code
  des douanes de l'Union, règlement (UE) n° 952/2013, applicable depuis le
  1er mai 2016
- **calculateur de frais d'approche**, en haut du deuxième écran : prix d'achat
  départ, poids commandé, fret et assurance, taux de droit, freinte → valeur en
  douane, droits, coût total, poids reçu, **coût au kilo débarqué** et
  **coefficient d'approche**
- **signature datée**, deux questions de FAQ ajoutées, **FAQPage JSON-LD** sur
  les huit questions (la page n'en avait aucun)
- **bloc sources officielles** : douane.gouv.fr (×2), FranceAgriMer, TRACES NT,
  Incoterms 2020 de la CCI — les cinq URL vérifiées en 200
- title 470 px, description 937 px (mesure du recrawl)

### `/fonctionnalites/logiciel-devis-commande-bon-livraison/` — [page](https://www.helloharel.com/fonctionnalites/logiciel-devis-commande-bon-livraison/)

- **H1** remis à l'exact match naturel : il disait « Logiciel devis-commande-BL »,
  du jargon ; il dit « Le logiciel devis, commande et bon de livraison qui
  facture le poids réellement pesé, pas celui du devis »
- **module « du devis au bon de livraison, à poids variable »** : pièces
  commandées, poids théorique, poids pesé, tarif → montant du devis, montant du
  BL, écart en euros et en pourcentage
- **fait daté et sourcé** : l'article L441-9 du code de commerce impose que la
  facture mentionne la quantité **effectivement livrée**
- réparation au passage : un script mort de 2 189 o retiré, un « & » littéral
  échappé dans le JSON-LD (voir T18)

### `/blog/meilleurs-erp-import-export/` — [page](https://www.helloharel.com/blog/meilleurs-erp-import-export/)

- title « Logiciel import export et gestion commerciale • Comparatif 2026 »
  (448 px), description 969 px
- **quatre liens entrants éditoriaux**, à ancres tournantes, là où elle n'en
  recevait que trois :

| Depuis | Ancre |
|---|---|
| `/fonctionnalites/import-export/` | logiciel de gestion commerciale import export |
| `/negoce/achats-approvisionnements/` | comparatif des logiciels import export |
| `/implantation-maurice/` | logiciel import export |
| `/blog/erp-grossiste-distributeur/` | ERP import export pour le négoce alimentaire |

### Les deux modules

Mesurés au rendu, Chromium 390 px et 1280 px : **zéro débordement horizontal**,
les valeurs affichées sans JavaScript sont exactement celles que le script
recalcule, la saisie recalcule bien. Aucune dépendance externe, `<label for>`
sur chaque champ, `aria-live` sur les résultats, pas de décalage de mise en page.

---

## Technique — ce que le crawl du 06/10 a mesuré (172 URL)

### Réparé

**T17 · Le sitemap avait quatre semaines de retard.** Le cache fichier de
Rank Math n'avait pas bougé depuis le 11/09. Il servait **10 URL supprimées** —
les 5 pages intelligence artificielle, `/integrateurs/`, les 2 pages intégrateur
de ville, `/erp-ia/`, l'article Akanea — et **ignorait les 3 landings de
septembre**, pourtant données INDEXE. Purge rejouée, sitemap resoumis à la
Search Console. Résultat : **171 URL pour 172 publiées**, l'écart étant
`/blog/erp-agroalimentaire/` dont la canonique pointe vers `/agroalimentaire/` —
exclusion normale. *La cause reste ouverte : le cache ne s'invalide pas à la
publication.*

**T18 · Quatre scripts morts, et un piège d'écriture.** Le retrait de l'outil
ROI en septembre avait laissé le `<script>` dans cinq pages `/fonctionnalites/`.
Ils sortent immédiatement — l'élément qu'ils cherchent n'existe plus — mais ils
portaient 3 à 5 « & » nus dans un `<script>`. WordPress les transforme en
`&#038;` au prochain enregistrement : **toute écriture future sur ces pages
aurait cassé la chaîne de requête**. Retirés, et le « & » littéral de la
signature JSON-LD échappé en `&`. Rendu inchangé, vérifié.

**T19 · Trois pages sans title.** `/blog/`, `/medical/` et
`/medical/laboratoires/` servaient le title par défaut du thème — « Blog -
Hello Harel », 122 px, très en dessous du plancher de 200 px. Les trois en ont
un, posé en base et épinglé.

### Toujours ouvert

**T12 · La casse des titles — toujours un clic.** Mesure du jour : les deux
titles posés ce matin **ressortent capitalisés**, et `/blog/bon-de-livraison/`
sert encore « Bon De Livraison ». Le réglage Rank Math est toujours sur ON.
5 titles de plus épinglés dans l'extrait 12, soit **29 en attente**.
→ **Rank Math > Titres & Méta > décocher « Capitaliser les titles »**.

**T20 · Le maillage interne ne tourne pas** (nouveau, mesuré sur le contenu en
base, hors menu et pied de page) :

| Page | Liens entrants | Ancres |
|---|---|---|
| `/fonctionnalites/import-export/` | **517** | 3 ancres répétées 167–168 fois chacune |
| `/fonctionnalites/logiciel-devis-commande-bon-livraison/` | **164** | une seule ancre, 164 fois |
| `/blog/meilleurs-erp-import-export/` | **3** → 7 | la page qui *ranke* |

La règle 2 demande un jeu d'ancres tournant. C'est un bloc de gabarit à faire
varier, pas 500 liens à réécrire à la main. Chiffré 3 h.

**T15 · Les pages lourdes.** 46 pages au-dessus de 300 ko, contre 48 au 01/10.
Les 2 comparatives sont à 440 ko. Ticket de gabarit.

**T16 · Les H1.** Les 4 pages sans H1 sont inchangées : `/cgu/`,
`/mentions-legales/` et `/politique-de-confidentialite/` sont construites dans
Elementor (widget titre, à changer dans l'éditeur),
`/conformite-loi-anti-fraude-tva/` n'a aucun contenu en base.

**T13 · Le balisage structuré.** Re-mesuré entité par entité : **seules les
2 pages comparatives** déclarent deux nœuds notés, et c'est la décision en
attente (4,7 sur 1 avis éditorial contre 5 sur 31). Rien n'a régressé.

### Mesuré, non traité

- **5 pages `/fonctionnalites/` déclarent 7 entités « entreprise » sans `@id`**
  chacune — le plus haut du site. Google ne peut pas les fusionner.
- `2x BreadcrumbList` sur les 10 pages d'implantation, `2x SoftwareApplication`
  sur 5 pages `/negoce/`, `2x WebSite` / `WebPage` / `Organization` sur l'accueil.
- `/blog/erp-agroalimentaire/` — 287 ko d'article qui se déclare canoniquement
  comme un doublon de `/agroalimentaire/`. Il ne rankera jamais pour lui-même.
  Décision éditoriale à prendre.

---

## Décisions qui t'attendent

1. **Rank Math > Titres & Méta > décocher « Capitaliser les titles »** — 29 titles
   épinglés en attendent.
2. **Les requêtes de roadmap sans volume mesurable** — 7 lots sur 8. Faut-il
   re-trier les 350 lignes restantes avant de continuer octobre ?
3. **`wp-json/wp/v2/hh_lead` répond 200 sans authentification** et expose
   91 leads sur 31 pages (nom, prénom, date). Je n'ai pas fermé la route : si le
   tableau de bord Lovable la lit en anonyme, je casserais le dashboard.
   **Est-ce que l'app lit cette route ?**
4. `/blog/erp-agroalimentaire/` : on garde la canonique vers `/agroalimentaire/`,
   ou on lui rend son autonomie ?
