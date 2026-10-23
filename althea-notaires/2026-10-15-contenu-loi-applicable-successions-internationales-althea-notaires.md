# Quelle loi est applicable aux successions internationales ?

Althéa Notaires · roadmap contenu, livraison du 26/10/2026 · page question ·
URL cible `/loi-applicable-successions-internationales/`

---

## 1 · Anti-cannibalisation

Le silo porte déjà `/succession-internationale-notaire-paris/` (page de
service, mère de silo) et trois pages filles livrées en octobre :
`/succession-internationale-avec-un-heritier-a-l-etranger/`,
`/acte-de-notoriete-en-succession-internationale/`,
`/comment-se-passe-une-succession-internationale/`.

La page du jour ne doit donc **pas** raconter le déroulé d'une succession —
c'est le travail de `/comment-se-passe-une-succession-internationale/`, en
ligne depuis le 06/10. Elle traite **une seule question : quelle loi
gouverne**. Verdict : **FAIBLE**, création, à condition de s'en tenir à la
règle de conflit.

## 2 · Analyse SERP — relevé du 15/10/2026, France, français

**Qui rank.** AI Overview en position absolue 1. Puis notaires.fr
(institutionnel), notaires-office.fr (novembre 2022), gestiondepatrimoine.com
(mars 2024), Banque Populaire (octobre 2023), un PDF du CNUE, Allianz,
Citizen Avocats, une vidéo YouTube, un PDF d'étude notariale.

**Trois constats chiffrés.**

1. **Aucune étude notariale parisienne dans le top 10.** Les deux seuls
   résultats notariaux sont un portail institutionnel et un PDF. La place
   d'une étude qui répond clairement est libre.
2. **Quatre des huit pages de texte ont plus de deux ans** (2022, 2023, 2024,
   2015). Sur un sujet où la règle a changé en 2021 — le droit de prélèvement
   compensatoire — l'ancienneté est un défaut exploitable.
3. **Le « People also ask » ne parle pas de la règle mais de l'argent** :
   frais de notaire, pays sans droits de succession, nouveautés 2026 et 2027.
   La demande réelle mélange loi civile et fiscalité, que le règlement
   européen sépare justement.

**Angle tranché — plus rapide.** La réponse en un écran : un arbre de
décision en quatre questions qui donne la loi applicable, puis seulement
après, les trois cas où la règle ne suffit pas.

**Promesse de page.** En quatre questions, vous savez quelle loi gouverne
votre succession — et si la réponse ne suffit pas, vous savez pourquoi.

## 3 · Gabarit

Repris de `/comment-se-passe-une-succession-internationale/`, en ligne le
06/10 : H1 question + angle · H2 d'accroche · H2 d'appel (« Ouvrir votre
dossier ») · H2 par étape · Questions fréquentes · bloc Me Camille Grellet ·
bloc « Althéa Notaires, l'acte de confiance » · appel final.

Balisage de la page sœur : `WebPage`, `Service`, `LegalService`, `FAQPage`,
`BreadcrumbList`. On reprend le même jeu.

## 4 · Maillage

**Sortant** (ancres contiguës, exactes, jamais neutres) :

| Ancre | Vers | Emplacement |
|---|---|---|
| succession internationale notaire Paris | `/succession-internationale-notaire-paris/` | 1er paragraphe |
| acte de notoriété en succession internationale | `/acte-de-notoriete-en-succession-internationale/` | étape 2 |
| règlement européen sur les successions internationales | `/reglement-europeen-successions-internationales/` | étape 1 *(page sœur du 26/10)* |
| succession internationale avec un héritier à l'étranger | `/succession-internationale-avec-un-heritier-a-l-etranger/` | étape 3 |
| délai de règlement d'une succession | `/delai-de-reglement-d-une-succession/` | FAQ |

**Entrant — à poser, c'est le bloc qu'on oublie :**

| Depuis | Ancre | Où |
|---|---|---|
| `/succession-internationale-notaire-paris/` | quelle loi est applicable aux successions internationales | corps, section « loi applicable » |
| `/comment-se-passe-une-succession-internationale/` | la loi applicable à la succession | première étape |
| `/succession-heritage/` | succession internationale : la loi applicable | bloc des cas particuliers |

## 5 · Balisage

- **Title** : `Quelle loi s'applique à une succession internationale ? La règle`
- **Description** : `Dernière résidence habituelle du défunt, sauf choix de votre loi nationale : la règle du règlement européen, les trois cas où elle ne suffit pas, et ce que la fiscalité ne suit pas.`
- **H1** : `Quelle loi est applicable à une succession internationale&nbsp;? La règle, puis les trois exceptions`

## 6 · Les faits datés et leurs sources

| Fait | Source |
|---|---|
| Règlement (UE) n° 650/2012 du 4 juillet 2012, applicable aux successions **ouvertes à compter du 17 août 2015** | EUR-Lex, règlement 650/2012 |
| Critère principal : **dernière résidence habituelle** du défunt (article 21) | idem |
| Exception : liens manifestement plus étroits avec un autre État (article 21 § 2) | idem |
| Choix possible de **la loi de sa nationalité** — *professio juris* (article 22) | idem |
| **Unicité** : une seule loi pour les meubles et les immeubles | idem |
| **25 États membres liés** ; le Danemark et l'Irlande n'y participent pas ; le Royaume-Uni n'est plus un État membre depuis 2020 | idem |
| La **fiscalité est exclue** du règlement (article 1 § 1) ; en France, CGI article 750 ter | EUR-Lex + CGI |
| **Droit de prélèvement compensatoire** : article 913 alinéas 2 et 3 du code civil, issu de la loi du 24 août 2021, pour les successions ouvertes **à compter du 1er novembre 2021** | Légifrance, code civil art. 913 |

---

## 7 · Corps de page — HTML prêt à coller

```html
<h2>La réponse en quatre questions</h2>

<p>Une succession internationale est gouvernée par <strong>une seule loi</strong>, celle de l'État où le défunt avait sa <strong>dernière résidence habituelle</strong>. C'est la règle posée par le règlement européen (UE) n° 650/2012 du 4 juillet 2012, applicable à toutes les successions ouvertes à compter du <strong>17 août 2015</strong>. Elle vaut pour l'ensemble du patrimoine, meubles et immeubles, où qu'ils se trouvent. Si vous ouvrez un dossier à Paris, c'est le point de départ de notre travail de <a href="/succession-internationale-notaire-paris/">succession internationale notaire Paris</a>.</p>

<ol>
  <li><strong>Le défunt est-il décédé le 17 août 2015 ou après&nbsp;?</strong> Si non, les anciennes règles françaises s'appliquent : loi du dernier domicile pour les meubles, loi du lieu de situation pour chaque immeuble.</li>
  <li><strong>Avait-il choisi sa loi nationale par écrit&nbsp;?</strong> Si oui, ce choix l'emporte. C'est la <em>professio juris</em> de l'article 22 : chacun peut désigner, dans un testament ou un acte séparé, la loi de l'État dont il a la nationalité.</li>
  <li><strong>À défaut de choix, où vivait-il réellement au jour du décès&nbsp;?</strong> C'est là que se situe la résidence habituelle — pas l'adresse fiscale, pas la nationalité, pas le lieu des biens.</li>
  <li><strong>Cette loi est-elle celle d'un État lié par le règlement&nbsp;?</strong> Si c'est celle d'un État tiers, il faut vérifier si cet État renvoie à une autre loi.</li>
</ol>

<h2>Ouvrir votre dossier de succession internationale</h2>

<h2>Première exception : le défunt avait choisi sa loi nationale</h2>

<p>L'article 22 du <a href="/reglement-europeen-successions-internationales/">règlement européen sur les successions internationales</a> permet de désigner la loi de sa nationalité. Un Français installé au Portugal peut ainsi soumettre sa succession au droit français&nbsp;; un Italien résidant à Paris peut la soumettre au droit italien.</p>

<p>Ce choix doit être <strong>exprès</strong> et résulter d'une disposition à cause de mort — le plus souvent un testament. Il ne se présume pas. Une personne binationale peut choisir l'une ou l'autre de ses nationalités.</p>

<h2>Deuxième exception : la résidence habituelle n'est pas évidente</h2>

<p>La résidence habituelle n'est définie nulle part par un nombre de jours. Elle se déduit d'un faisceau : durée et régularité de la présence, lieu de vie de la famille, centre des intérêts, intention de s'établir. Un retraité qui passe six mois par an en Espagne et six mois en France oblige à une analyse, pas à un décompte.</p>

<p>Le règlement prévoit lui-même le cas limite : si le défunt présentait des <strong>liens manifestement plus étroits</strong> avec un autre État, c'est la loi de cet État qui s'applique (article 21 § 2). C'est une exception rare, et elle se motive.</p>

<p>C'est à ce stade que se prépare <a href="/acte-de-notoriete-en-succession-internationale/">l'acte de notoriété en succession internationale</a>, qui établit qui hérite au regard de la loi retenue.</p>

<h2>Troisième exception : la loi désignée est celle d'un État tiers</h2>

<p>Trois situations à distinguer, et c'est là que les pages généralistes se trompent le plus souvent&nbsp;:</p>

<table>
  <thead><tr><th>État</th><th>Situation au regard du règlement</th></tr></thead>
  <tbody>
    <tr><td>25 États membres de l'Union</td><td>Liés par le règlement</td></tr>
    <tr><td>Danemark, Irlande</td><td>États membres, mais ne participent pas au règlement</td></tr>
    <tr><td>Royaume-Uni</td><td>N'a jamais participé au règlement, et n'est plus un État membre depuis 2020</td></tr>
    <tr><td>Suisse, États-Unis, Maroc, Canada…</td><td>États tiers</td></tr>
  </tbody>
</table>

<p>Quand la loi désignée est celle d'un État tiers, il faut regarder si les règles de cet État renvoient à une autre loi — le mécanisme du renvoi, prévu à l'article 34. Un immeuble situé dans un pays qui applique la loi du lieu de situation peut ainsi échapper à la loi successorale principale. L'unicité annoncée par le règlement connaît là sa vraie limite.</p>

<h2>Le cas des héritiers réservataires : ce que la loi française protège encore</h2>

<p>Une loi étrangère qui ignore la réserve héréditaire n'est pas, par elle-même, contraire à l'ordre public international français. Mais depuis la loi du 24 août 2021, l'article 913 du code civil ouvre un <strong>droit de prélèvement compensatoire</strong> : lorsque la loi étrangère ne connaît aucun mécanisme réservataire, les enfants peuvent prélever sur les biens situés en France la part que la loi française leur aurait reconnue. Ce droit vaut pour les successions ouvertes <strong>à compter du 1er novembre 2021</strong>, et suppose que le défunt ou l'un de ses enfants soit ressortissant d'un État membre ou y réside.</p>

<p>Si l'un des héritiers vit hors de France, la façon de le faire signer est traitée sur la page <a href="/succession-internationale-avec-un-heritier-a-l-etranger/">succession internationale avec un héritier à l'étranger</a>.</p>

<h2>Ce que la loi applicable ne décide pas : l'impôt</h2>

<p>Le règlement européen règle la dévolution — qui hérite, de quoi, dans quelle proportion. Il <strong>exclut expressément la fiscalité</strong> (article 1 § 1). Les droits de succession restent déterminés par chaque État et, le cas échéant, par les conventions fiscales bilatérales.</p>

<p>En France, l'article 750 ter du code général des impôts retient trois rattachements : le domicile fiscal du défunt, la situation des biens, et le domicile fiscal de l'héritier lorsqu'il a été domicilié en France au moins six ans au cours des dix dernières années. Une succession peut donc être régie par le droit espagnol et imposée en France.</p>

<h2>Questions fréquentes</h2>

<h3>Peut-on choisir la loi du pays où se trouvent les biens&nbsp;?</h3>
<p>Non. Le règlement n'ouvre le choix qu'à la loi de la nationalité du défunt. La loi du lieu de situation des biens ne peut pas être désignée par testament.</p>

<h3>Que se passe-t-il si le défunt avait deux résidences&nbsp;?</h3>
<p>Une seule est la résidence habituelle. Elle se détermine par un faisceau d'indices — durée, régularité, centre des intérêts familiaux et patrimoniaux — et se motive dans l'acte.</p>

<h3>Le choix de loi doit-il être fait devant notaire&nbsp;?</h3>
<p>Il doit figurer dans une disposition à cause de mort valable en la forme. Le testament authentique reçu par notaire est la voie la plus sûre, parce qu'il est conservé, daté et incontestable dans sa forme.</p>

<h3>Combien de temps prend une succession internationale&nbsp;?</h3>
<p>Les délais français courent indépendamment de la loi applicable : la déclaration de succession est due dans les six mois du décès si celui-ci est survenu en France, douze mois sinon. Le détail figure sur la page <a href="/delai-de-reglement-d-une-succession/">délai de règlement d'une succession</a>.</p>

<h3>La loi applicable change-t-elle le montant des droits de succession&nbsp;?</h3>
<p>Non. La loi civile dit qui hérite, la loi fiscale dit ce qui est dû. Les deux peuvent relever de deux États différents.</p>
```

## 8 · JSON-LD FAQPage à ajouter

Reprendre les cinq questions ci-dessus, au même format que
`/comment-se-passe-une-succession-internationale/`. Les réponses doivent être
le texte des `<p>`, sans balise.

## 9 · Contrôle

| Critère | Verdict |
|---|---|
| Exact match dans le title, au plus tôt | oui — « Quelle loi s'applique à une succession internationale » |
| H1 ≠ title | oui |
| P1 = la réponse, requête dans les 60 premiers mots | oui — la réponse est dans la première phrase |
| Fait daté + source dans le premier tiers | oui — 17 août 2015, règlement 650/2012 |
| Définition en une phrase, extractible | oui — première phrase du corps |
| Donnée structurée | oui — tableau des quatre catégories d'États |
| Module au-dessus du 2e écran | oui — l'arbre en quatre questions |
| La suite est dans la page | oui — 5 liens internes contextuels |
| Nom de l'étude absent du title | oui |

**Réserve.** Le relevé SERP du 15/10 a été fait sur la requête exacte. Le
volume n'a pas été mesuré : sur ce silo, la stratégie est la couverture de la
demande, pas le volume.
