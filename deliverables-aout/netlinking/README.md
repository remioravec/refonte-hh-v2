# Prospection netlinking Hello Harel — livrable AOÛT 2026

Client : **Hello Harel** (helloharel.com), éditeur d'ERP agroalimentaire.
Agence : SEO Monkey (Rémi Oravec). Process : `operationnel-netlinking`.
Relevés DataForSEO datés du **15/08/2026**, location France, langue fr.

> Août = mois de **sourcing / qualification**. **Aucun contact n'est envoyé.**
> Les premières citations partent en **septembre**. Cadence cible : **3 liens / mois**.

---

## 1. Le link gap vs les 4 concurrents

Intersection des domaines référents (`backlinks_domain_intersection`),
Hello Harel exclu, sur **vif.fr, akanea.com, infologic-copilote.fr, archipelia.com**.

| Périmètre | Domaines remontés | Exploitables après filtrage |
|---|---|---|
| Intersection des **4** concurrents | 4 | **0** — 100 % de bruit |
| Paire **akanea + vif** | 31 | 7, **déjà tous dans la BDD des 60** |
| Paire **infologic + archipelia** | 10 | 2 **inédits** qui passent le test |

**L'intersection des 4 est intégralement du bruit** : `craft.co`, `clodura.ai`,
`global-website.pages.dev` (spam 35), `rubypayeur.com` — agrégateurs
automatiques et nofollow, exactement les signatures documentées dans
`references/01-filtrage.md`. Ce résultat **confirme la recommandation de l'audit :
0 € d'achat au démarrage**, on part sur des citations gratuites.

Les seuls domaines thématiques du gap akanea+vif (logiciels.pro, businessman.fr,
gs1.fr, news-eco.com, timcod.fr, voxlog.fr, blogistics.fr) **étaient déjà dans
la liste des 60**. Le gap n'apporte donc **que 2 domaines nets nouveaux**, issus
de la paire infologic+archipelia et validés au test thématique :

| Domaine net nouveau | Source | Test thématique |
|---|---|---|
| **logicielfrance.com** | infologic + archipelia | PASS — pos1 « logiciel francais », **pos4 « erp copilote »** |
| **comparateur-cpgi.fr** | infologic + archipelia | PASS — **pos6 « isagri logiciel »**, pos5 « application et logiciel » |

Rejetés du gap infologic+archipelia : `infopass.fr` (0 kw top10), `themetix.com`
(nofollow image), `whatiscrmdaijiru.blogspot.com` (spam 55), `tntcode.com`
(spam 50), + les agrégateurs communs.

---

## 2. Le test thématique éliminatoire (le cœur du travail)

**Règle Rémi (non négociable) :** un domaine ne qualifie que s'il **ranke top 10**
sur des mots-clés de la thématique Hello Harel (erp / logiciel / agroalimentaire /
un métier de bouche). Vérifié en données (`dataforseo_labs_google_ranked_keywords`,
filtre `rank_group ≤ 10` + regex thématique), **jamais au flair**. Preuve (mot-clé
+ position) consignée pour chaque PASS dans le CSV.

### Bilan sur les 60 sites de la BDD

| | Nombre |
|---|---|
| **PASS** (positionné top 10 sur la thématique) | **26 lignes / 25 domaines** |
| Citations client (clause au contrat, test N/A) — conservés | 2 |
| **REJETÉS** (0 mot-clé thématique en top 10, ou hors-thème / nofollow) | **32** |

*(agro-media.fr apparaît 2 fois dans les 60 — sept. et nov. — d'où 26 lignes pour 25 domaines.)*

**+ 2 domaines nets du link gap** (logicielfrance.com, comparateur-cpgi.fr) qui passent.
→ **CSV final : 30 lignes à activer** (28 domaines uniques + les 2 doublons de plan).

### Les 25 domaines qui PASSENT (preuve datée dans le CSV)

- **Comparateurs / annuaires logiciels** : appvizer.fr (pos9 « logiciel erp »),
  logiciels.pro, capterra.fr (pos1 « erp logiciel gratuit »), getapp.fr,
  tool-advisor.fr (pos1, 449 kw), lebonlogiciel.com (pos1 « erp baan »),
  app-fox.com (pos5 « jlogiciels facturation »), **logicielfrance.com**,
  **comparateur-cpgi.fr** *(2 derniers = link gap)*.
- **Traçabilité / codes-barres** : gs1.fr (**pos3 « code barre », 27 100**), timcod.fr (pos6).
- **Institution / GED** : francenum.gouv.fr (pos1 « GED logiciel »).
- **Presse & médias filière** : agro-media.fr (**pos3 « agroalimentaire », 9 900**),
  processalimentaire.com (pos5 « code des usages de la charcuterie »),
  usinenouvelle.com (**pos1 « agroalimentaire industriel », 3 600**),
  lsa-conso.fr (pos3 « groupe agroalimentaire mondial »),
  voxlog.fr & blogistics.fr (supply chain / logistique).
- **Interpro / fédérations** : fict.fr (**pos4 « charcutiers », 2 400**),
  interfel.com (**pos8 « fruits et légumes », 8 100**),
  ania.net (**pos2 « industries alimentaires », 3 600**).
- **Réseaux régionaux** : area-normandie.fr (pos2), areaoccitanie.com (pos7),
  ariasud.com (pos10, limite), bretagne-supplychain.fr (pos6 « supply chain métiers »).
- **Salons** : cfiaexpo.com (pos1 « salon agroalimentaire rennes »),
  sirha-bakeandsnack.com (pos1 « salon de la boulangerie 2026 »).

### Les 32 REJETS et leur motif (échantillon des cas qui comptent)

| Domaine | Motif de rejet (mesuré le 15/08/2026) |
|---|---|
| **businessman.fr** | Top 10 uniquement sur sa marque + brèves retail locales (popeyes, lidl, carrefour). **0 mot-clé thématique.** (l'audit l'avait retenu — le test le sort) |
| **celge.com** | **0 ranking top 10 en France**, toutes requêtes confondues. *(reste citation engagée au plan sept., cf §4)* |
| **news-eco.com** | Communiqués **nofollow** (filtre #2) ; seul hit « resalys logiciel » = logiciel tourisme, hors filière |
| **sialparis.fr** | Le plus gros salon food, mais **ne ranke pas top 10** sur « agroalimentaire / salon agroalimentaire » (concurrence) — non positionné = rejet |
| **ria-agroalimentaire.com** | 0 mot-clé thématique en top 10 |
| **prodandpack.com** | Positionné mais sur « salon emballage » — **emballage ≠ thématique** (transverse, hors agroalimentaire) |
| **cniel.com** | Seul hit « accord interprofessionnel » (gouvernance laitière), hors thème logiciel/métier |
| Clusters régionaux : vitagora.com, valorial.fr, vegepolys-valley.eu, pole-innovalliance.com, agri-sud-ouest-innovation.com, aria-paysdelaloire.fr, aria-grandest.fr, aria-hautsdefrance.fr, adnouest.org, foodinpaca.com, criticalfood.fr, adepale.org | **Ne rankent que sur leur propre marque.** « Avoir l'air pertinent » ≠ « être positionné » |
| Comparateurs jeunes/étrangers : softwareadviser.ai, erpimplementation.eu, societe-informatique.fr | 0 ranking FR top 10 malgré « erp » dans le nom |
| Standards : edifrance.org | 0 mot-clé thématique top 10 |
| Presse/industrie : industrie-mag.com, production-maintenance.com, emballage-technologies.com | 0 mot-clé thématique top 10 |
| Écoles : adae-oniris.com, groupe-imt.com, ecoledagriculture.fr, agrocampus-ouest.fr, isara.fr | 0 mot-clé thématique top 10 (rankent sur leur nom d'école) |
| Salon : salon-cfia.com | doublon de cfiaexpo.com, 0 top 10 propre |

**Leçon confirmée (mesure du 13/08 dans le skill) :** une liste brute n'est pas
une liste de cibles. Sur 60 « sites à contacter », **~43 % passent réellement**
le test ; livrer les 60 aurait fait perdre une demi-journée à la vérification.

---

## 3. La porte d'entrée de chaque domaine (script `trouver_contact.py`)

Toutes les portes sont dans la colonne **PORTE D'ENTRÉE** du CSV. Synthèse des cas
à traiter à la main :

- **BLOQUE LE ROBOT (vivant, ne pas écarter)** : capterra.fr, getapp.fr,
  usinenouvelle.com, lsa-conso.fr → ouvrir manuellement (portail éditeur Gartner
  pour Capterra/GetApp ; rédaction via LinkedIn pour les deux médias).
- **PAGE ÉDITEUR (meilleur canal, gratuit)** : appvizer.fr (`/referencer-logiciel`),
  celge.com (`/annonceurs/`), agro-media.fr (`/publicite`),
  interfel.com (`/espace/inscription-autre/`), fict.fr (`/inscription/`).
- **INJOIGNABLE au crawl mais domaine connu** : gs1.fr (formulaire adhérent),
  area-normandie.fr (annuaire membres), appvizer.fr / logiciels.pro (fiches éditeur) —
  à ouvrir à la main.
- **Citations client** : jambonsoliveras.fr & primfruit.fr → **clause de citation
  au contrat**, aucun outreach (jambonsoliveras injoignable en ligne, normal).

---

## 4. Préparation des citations de SEPTEMBRE (fiches éditeur)

Les 3 premières citations du plan d'audit partent en septembre. Anchor **imposée
par la plateforme** (= nom de l'éditeur) → comptent en **citation**, hors
répartition d'ancres. Ne PAS acheter un lien pour compenser.

| Plateforme | URL / process de soumission de la fiche éditeur | Coût | Statut test thématique |
|---|---|---|---|
| **appvizer.fr** | Formulaire « Référencer mon logiciel » : **https://www.appvizer.fr/referencer-logiciel** (compte éditeur → création de la fiche produit). | Gratuit (offre de base) | PASS (pos9 « logiciel erp ») |
| **logiciels.pro** | Pas de page publique d'auto-inscription détectée au crawl → passer par **LinkedIn logiciels.pro** / demande de référencement éditeur. | Gratuit | PASS (pos1 « logiciel pro ») |
| **celge.com** | Espace annonceurs / référencement : **https://celge.com/annonceurs/**. | Gratuit (base) | **ÉCHEC** test (0 top10 FR) — citation **maintenue** car engagée au plan d'audit ; faible valeur, à surveiller |

**Note celge.com :** le domaine ne ranke sur aucun mot-clé en France au
15/08/2026. Il reste au plan (engagement audit, fiche gratuite thématique) mais
c'est la citation la plus faible des trois ; si l'inscription demande le moindre
effort payant, la déprioriser au profit de capterra.fr / getapp.fr / tool-advisor.fr
qui passent le test avec de vrais volumes.

**Rappel envoi :** toute la prospection part de `administration@remi-oravec.fr`.
Le skill prépare les brouillons, **Rémi valide et envoie**. Aucun `send_message`
automatique. Contrôle de l'adresse d'envoi à faire en début de campagne (septembre).

---

## 5. Fichiers du livrable

| Fichier | Contenu |
|---|---|
| `prospection-aout.csv` | Roadmap de prospection — 30 lignes qualifiées (MOIS, TYPE, DOMAINE, RECHERCHE, PAGE, ANCRE, PORTE D'ENTRÉE, TEST THÉMATIQUE daté, STATUT) |
| `README.md` | Ce document — link gap, bilan test thématique, prépa citations septembre |
| `templates-outreach.md` | 3 modèles FR (article invité, citation client, blog SEO) + exemples d'ancres semi-optimisées |
