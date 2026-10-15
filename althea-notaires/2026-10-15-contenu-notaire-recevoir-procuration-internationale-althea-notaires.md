# Comment un notaire peut-il recevoir une procuration internationale ?

Althéa Notaires · roadmap contenu, livraison du 26/10/2026 · page question ·
URL cible `/notaire-recevoir-procuration-internationale/`

---

## 1 · Anti-cannibalisation

`/succession-internationale-avec-un-heritier-a-l-etranger/` (en ligne le
06/10) traite **la situation** : un héritier vit hors de France, que
fait-on&nbsp;? La page du jour traite **l'acte** : par quelles formes une
procuration venue de l'étranger devient utilisable par un notaire français.
Verdict : **FAIBLE**, à condition que la page reste sur la forme de l'acte et
renvoie la situation à sa page mère.

## 2 · Analyse SERP

**Relevé non réalisé.** Deux tentatives sur `procuration internationale
notaire succession` et `procuration notaire étranger succession apostille`
ont échoué le 15/10/2026 (erreur 40101 du fournisseur de données). **L'angle
ci-dessous repose donc sur les deux relevés voisins du même jour et sur la
structure du silo, pas sur un relevé propre.**

À refaire avant publication — c'est la seule réserve de ce lot, et elle est
levable en une requête.

Ce que les deux relevés voisins indiquent malgré tout : sur ce silo, les
premières places sont tenues par des portails institutionnels et des PDF, et
aucune étude parisienne n'apparaît. Il n'y a pas de raison que cette requête,
plus technique encore, échappe à la règle.

**Angle provisoire — plus démontré.** Les trois voies concrètes, avec pour
chacune ce qu'il faut fournir et ce qui bloque. Là où les pages concurrentes
parlent de « procuration légalisée » en une ligne, on donne le mode d'emploi.

**Promesse de page.** Trois façons de signer depuis l'étranger, et laquelle
choisir selon le pays où vous êtes.

## 3 · Gabarit

Identique aux deux pages sœurs.

## 4 · Maillage

**Sortant :**

| Ancre | Vers |
|---|---|
| succession internationale avec un héritier à l'étranger | `/succession-internationale-avec-un-heritier-a-l-etranger/` |
| acte de notoriété en succession internationale | `/acte-de-notoriete-en-succession-internationale/` |
| succession internationale notaire Paris | `/succession-internationale-notaire-paris/` |
| délai de règlement d'une succession | `/delai-de-reglement-d-une-succession/` |

**Entrant — à poser :**

| Depuis | Ancre |
|---|---|
| `/succession-internationale-avec-un-heritier-a-l-etranger/` | procuration internationale reçue par le notaire |
| `/comment-se-passe-une-succession-internationale/` | signer à distance depuis l'étranger |
| `/reglement-succession-etapes/` | procuration pour une succession |

## 5 · Balisage

- **Title** : `Procuration internationale chez le notaire : les 3 formes admises`
- **Description** : `Signer une succession depuis l'étranger : procuration devant notaire local avec apostille, devant le consulat de France, ou comparution à distance par acte authentique électronique.`
- **H1** : `Comment un notaire peut-il recevoir une procuration internationale&nbsp;? Les trois voies`

## 6 · Les faits datés et leurs sources

| Fait | Source |
|---|---|
| **Convention de La Haye du 5 octobre 1961** supprimant l'exigence de légalisation des actes publics étrangers — l'apostille | HCCH, convention Apostille |
| **Acte authentique électronique à distance** : comparution à distance devant notaire, généralisée par le décret n° 2020-1422 du **20 novembre 2020** | Légifrance |
| La procuration portant sur un acte authentique doit en principe revêtir **la même forme** que l'acte auquel elle se rapporte | code civil et décret n° 71-941 |
| Un acte rédigé en langue étrangère doit être accompagné d'une **traduction** pour être annexé à un acte français | pratique notariale, décret n° 71-941 |

**Réserve de rédaction.** Les règles de légalisation varient par pays
(apostille, légalisation consulaire, ou dispense par convention bilatérale).
La page donne la méthode et renvoie à l'étude pour le cas particulier — elle
n'établit pas de liste pays par pays, qui serait périmée en six mois.

---

## 7 · Corps de page — HTML prêt à coller

```html
<h2>Trois voies, selon le pays où vous vous trouvez</h2>

<p>Un notaire français peut recevoir une procuration internationale de trois façons : signée devant un notaire local puis apostillée ou légalisée, signée devant le consulat de France, ou signée à distance par comparution électronique devant le notaire français lui-même. Le choix dépend du pays où se trouve le signataire et du délai dont vous disposez.</p>

<table>
  <thead><tr><th>Voie</th><th>Où elle marche</th><th>Ce qu'il faut prévoir</th></tr></thead>
  <tbody>
    <tr><td>Notaire local + apostille</td><td>Pays liés par la convention de La Haye de 1961</td><td>Déplacement, apostille, traduction si besoin</td></tr>
    <tr><td>Notaire local + légalisation</td><td>Pays non liés par la convention</td><td>Passage par les autorités locales puis le consulat</td></tr>
    <tr><td>Consulat de France</td><td>Partout où la France a un poste compétent</td><td>Rendez-vous, parfois long</td></tr>
    <tr><td>Comparution à distance</td><td>Partout, si la connexion le permet</td><td>Pièce d'identité, visioconférence, signature électronique</td></tr>
  </tbody>
</table>

<p>Si vous cherchez d'abord à comprendre votre situation plutôt que la forme de l'acte, commencez par <a href="/succession-internationale-avec-un-heritier-a-l-etranger/">succession internationale avec un héritier à l'étranger</a>.</p>

<h2>Ouvrir votre dossier de succession internationale</h2>

<h2>Première voie : devant un notaire local, puis apostille</h2>

<p>C'est la voie la plus courante. L'héritier signe la procuration devant un notaire du pays où il réside. Pour que l'acte produise effet en France, il faut ensuite en faire certifier l'origine.</p>

<p>Dans les pays liés par la <strong>convention de La Haye du 5 octobre 1961</strong>, cette certification prend la forme d'une <strong>apostille</strong> : un cachet apposé par une autorité désignée du pays d'origine, qui dispense de toute autre formalité. C'est rapide et standardisé.</p>

<p>Dans les pays non liés par la convention, il faut passer par la <strong>légalisation</strong> : authentification par les autorités locales, puis par le consulat de France sur place. Comptez nettement plus de temps.</p>

<p>Deux points qui bloquent souvent&nbsp;:</p>

<ul>
  <li><strong>La langue.</strong> Une procuration rédigée en langue étrangère doit être traduite pour être annexée à l'acte français. Mieux vaut faire établir la procuration en français dès l'origine, ou en version bilingue.</li>
  <li><strong>La forme.</strong> Une procuration destinée à un acte authentique doit, en principe, revêtir la même forme. Une simple signature légalisée au bas d'un texte sous seing privé ne suffit pas toujours&nbsp;: dites-le au notaire local avant le rendez-vous.</li>
</ul>

<h2>Deuxième voie : devant le consulat de France</h2>

<p>Les postes consulaires français exercent certaines attributions notariales. Un Français résidant à l'étranger peut y signer une procuration qui sera directement utilisable en France, sans apostille ni légalisation — l'acte est français.</p>

<p>L'avantage est la simplicité. La limite est pratique : tous les postes n'exercent pas ces attributions, et les délais de rendez-vous sont parfois longs. Vérifiez auprès du poste avant de compter dessus.</p>

<h2>Troisième voie : la comparution à distance devant votre notaire français</h2>

<p>Depuis le décret du <strong>20 novembre 2020</strong>, un notaire français peut recevoir un acte authentique électronique avec comparution à distance : le signataire se connecte en visioconférence sur un système agréé par le Conseil supérieur du notariat, présente sa pièce d'identité, et signe électroniquement. L'acte est reçu par le notaire français, en France.</p>

<p>C'est souvent la voie la plus rapide, et elle supprime d'un coup l'apostille, la traduction et le déplacement. Trois conditions tout de même&nbsp;:</p>

<ul>
  <li>une <strong>pièce d'identité en cours de validité</strong>, présentée en vidéo&nbsp;;</li>
  <li>une <strong>connexion stable</strong>, l'échange devant être continu&nbsp;;</li>
  <li>un <strong>rendez-vous</strong> calé sur le décalage horaire, l'acte se signant en direct avec l'étude.</li>
</ul>

<p>C'est la voie que nous privilégions quand un héritier vit hors d'Europe et que le dossier n'attend pas.</p>

<h2>Ce que la procuration doit contenir</h2>

<p>Une procuration successorale trop vague fait perdre un mois. Pour éviter un second aller-retour, elle doit désigner précisément&nbsp;:</p>

<ul>
  <li>le <strong>défunt</strong> : nom, date et lieu du décès&nbsp;;</li>
  <li>le <strong>mandant</strong> et sa qualité d'héritier&nbsp;;</li>
  <li>le <strong>mandataire</strong> — souvent un clerc de l'étude&nbsp;;</li>
  <li>les <strong>actes couverts</strong> : acceptation de la succession, signature de l'acte de notoriété, de l'attestation de propriété immobilière, de la déclaration de succession, du partage&nbsp;;</li>
  <li>la <strong>faculté ou non de se substituer</strong>.</li>
</ul>

<p>Une procuration qui ne vise que « la succession » sans énumérer les actes oblige à en redemander une au moment du partage. C'est au stade de <a href="/acte-de-notoriete-en-succession-internationale/">l'acte de notoriété en succession internationale</a> que le défaut se révèle en général.</p>

<h2>Combien de temps prévoir&nbsp;?</h2>

<p>La forme choisie pèse directement sur le calendrier du dossier, et les délais fiscaux français, eux, ne s'arrêtent pas : six mois après un décès survenu en France, douze mois sinon. Le détail figure sur <a href="/delai-de-reglement-d-une-succession/">délai de règlement d'une succession</a>. Autrement dit, la voie la plus lente peut coûter des pénalités — c'est le vrai critère de choix.</p>

<h2>Questions fréquentes</h2>

<h3>Une procuration sous seing privé suffit-elle&nbsp;?</h3>
<p>Rarement. Une procuration destinée à un acte authentique doit en principe revêtir la même forme. Demandez-le à l'étude avant de signer quoi que ce soit à l'étranger.</p>

<h3>Faut-il faire traduire la procuration&nbsp;?</h3>
<p>Oui, si elle est rédigée en langue étrangère et doit être annexée à un acte français. Le plus simple est de la faire établir directement en français ou en version bilingue.</p>

<h3>L'apostille est-elle toujours nécessaire&nbsp;?</h3>
<p>Non. Elle concerne les pays liés par la convention de La Haye de 1961. Ailleurs, c'est la légalisation. Et si vous signez au consulat de France ou à distance devant le notaire français, aucune des deux n'est requise.</p>

<h3>Peut-on signer depuis n'importe quel pays en visioconférence&nbsp;?</h3>
<p>Techniquement oui, dès lors que la liaison est stable et la pièce d'identité valable. En pratique, le décalage horaire est la seule vraie contrainte.</p>

<h3>Qui peut être désigné comme mandataire&nbsp;?</h3>
<p>Toute personne majeure capable, y compris un collaborateur de l'étude. Un cohéritier peut l'être aussi, mais c'est déconseillé lorsque les intérêts peuvent diverger.</p>
```

## 8 · JSON-LD FAQPage

Même format que les pages sœurs.

## 9 · Contrôle

| Critère | Verdict |
|---|---|
| Exact match dans le title | oui — « Procuration internationale chez le notaire » |
| H1 ≠ title | oui |
| P1 = la réponse | oui — les trois voies dans la première phrase |
| Fait daté + source dans le premier tiers | oui — convention de La Haye du 5 octobre 1961 |
| Définition en une phrase | oui |
| Donnée structurée | oui — tableau des quatre voies |
| Module au-dessus du 2e écran | oui — le tableau comparatif |
| La suite est dans la page | oui — 4 liens internes contextuels |
| Nom de l'étude absent du title | oui |
| **Relevé SERP** | **NON FAIT — à refaire avant publication** |

**Verdict de contrôle : BLOQUÉ en l'état**, non pas sur le texte mais sur
l'étape 2 de la méthode. Le relevé manquant doit être fait, l'angle
confirmé ou corrigé, avant mise en ligne.
