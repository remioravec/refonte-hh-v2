# Quel est le règlement européen sur les successions internationales ?

Althéa Notaires · roadmap contenu, livraison du 26/10/2026 · page question ·
URL cible `/reglement-europeen-successions-internationales/`

---

## 1 · Anti-cannibalisation

Page sœur de `/loi-applicable-successions-internationales/`, livrée le même
jour. Le risque de recouvrement est réel et il est traité par une coupe
nette :

| Page | Ce qu'elle traite | Ce qu'elle ne traite pas |
|---|---|---|
| `/loi-applicable-…/` | **la règle de conflit** : quelle loi gouverne, et les exceptions | le texte lui-même, son champ, le certificat |
| **cette page** | **le texte** : ce qu'il couvre, qui il lie, ce qu'il crée | le détail du raisonnement sur la résidence habituelle |

Chacune ouvre sur l'autre par un lien contextuel. Verdict : **FAIBLE** à
condition de tenir cette coupe.

## 2 · Analyse SERP — relevé du 15/10/2026, France, français

**Qui rank.** AI Overview en position absolue 1. Puis un support pédagogique
BTS (crcf-edu.fr), un **PDF** d'un cabinet italien, Omega Avocats (nov. 2025),
deux pages du CNUE dont un **PDF**, le rapport du 115e Congrès des notaires
(2019), un **PDF** d'avocat.fr, Avocats Picovschi (juin 2021), un cabinet
suisse (2015).

**Trois constats chiffrés.**

1. **Quatre des neuf résultats sont des PDF.** Un PDF se lit mal sur
   téléphone, ne porte pas de maillage et n'offre aucune suite. Une page HTML
   claire prend l'avantage d'emblée.
2. **Le deuxième résultat organique est factuellement périmé** : il écrit que
   le règlement a été signé par tous les pays de l'Union « à l'exception du
   Danemark, du Royaume-Uni et de l'Irlande ». Le Royaume-Uni n'est plus un
   État membre depuis 2020 — la phrase induit en erreur. Plusieurs autres
   pages du top 10 datent de 2015, 2019, 2020 et 2021.
3. **Aucune page du top 10 ne sépare clairement ce que le règlement règle de
   ce qu'il ne règle pas.** C'est pourtant la confusion la plus coûteuse pour
   un client : il croit que le texte règle aussi l'impôt.

**Angle tranché — plus rapide, et à jour.** Un tableau « ce que le règlement
règle / ce qu'il ne règle pas » dès le premier écran, et une liste des États
exacte au 15/10/2026, là où le top 10 cite encore le Royaume-Uni.

**Promesse de page.** En un tableau, ce que le règlement européen décide pour
vous — et les trois choses qu'il laisse à d'autres textes.

## 3 · Gabarit

Identique à `/comment-se-passe-une-succession-internationale/` : H1 question +
angle · H2 d'accroche · H2 d'appel · H2 thématiques · Questions fréquentes ·
bloc Me Camille Grellet · bloc confiance · appel final. Balisage `WebPage`,
`Service`, `LegalService`, `FAQPage`, `BreadcrumbList`.

## 4 · Maillage

**Sortant :**

| Ancre | Vers |
|---|---|
| quelle loi est applicable aux successions internationales | `/loi-applicable-successions-internationales/` |
| succession internationale notaire Paris | `/succession-internationale-notaire-paris/` |
| acte de notoriété en succession internationale | `/acte-de-notoriete-en-succession-internationale/` |
| comment se passe une succession internationale | `/comment-se-passe-une-succession-internationale/` |

**Entrant — à poser :**

| Depuis | Ancre |
|---|---|
| `/succession-internationale-notaire-paris/` | le règlement européen sur les successions |
| `/loi-applicable-successions-internationales/` | règlement européen sur les successions internationales |
| `/acte-de-notoriete-en-succession-internationale/` | certificat successoral européen |

## 5 · Balisage

- **Title** : `Règlement européen sur les successions : ce qu'il couvre, et pas`
- **Description** : `Règlement (UE) n° 650/2012, applicable depuis le 17 août 2015 : une seule loi pour toute la succession, le certificat successoral européen, les 25 États liés — et ce que le texte laisse à la fiscalité.`
- **H1** : `Le règlement européen sur les successions internationales&nbsp;: ce qu'il décide, et ce qu'il laisse de côté`

## 6 · Les faits datés et leurs sources

| Fait | Source |
|---|---|
| Règlement (UE) n° 650/2012 du Parlement européen et du Conseil du **4 juillet 2012** | EUR-Lex |
| Applicable aux successions **ouvertes à compter du 17 août 2015** | idem, article 83 |
| **25 États membres liés** ; le Danemark et l'Irlande ne participent pas ; le Royaume-Uni n'a jamais participé et n'est plus État membre depuis 2020 | idem |
| **Certificat successoral européen** créé par les articles 62 et suivants | idem |
| La **copie certifiée conforme** du certificat est valable **six mois**, renouvelable (article 70 § 3) | idem |
| **Fiscalité exclue** du champ (article 1 § 1) | idem |
| Sont aussi exclus : régimes matrimoniaux, libéralités entre vifs hors succession, trusts, nature des droits réels | idem, article 1 § 2 |

---

## 7 · Corps de page — HTML prêt à coller

```html
<h2>Ce que le règlement décide, et ce qu'il laisse de côté</h2>

<p>Le règlement européen sur les successions internationales est le <strong>règlement (UE) n° 650/2012 du 4 juillet 2012</strong>. Il s'applique à toutes les successions ouvertes <strong>à compter du 17 août 2015</strong> et pose un principe simple : une seule loi gouverne l'ensemble de la succession, meubles et immeubles réunis, quel que soit le pays où ils se trouvent.</p>

<table>
  <thead><tr><th>Le règlement règle</th><th>Le règlement ne règle pas</th></tr></thead>
  <tbody>
    <tr><td>Quelle loi s'applique à la succession</td><td>Les droits de succession à payer</td></tr>
    <tr><td>Quel tribunal ou notaire est compétent</td><td>Le régime matrimonial des époux</td></tr>
    <tr><td>La reconnaissance des décisions entre États liés</td><td>Les donations faites du vivant, hors rapport successoral</td></tr>
    <tr><td>Le certificat successoral européen</td><td>La nature des droits réels sur les biens</td></tr>
  </tbody>
</table>

<p>Cette colonne de droite est la source de la plupart des malentendus. Une succession peut parfaitement être régie par le droit allemand et imposée en France. Le détail de la règle de conflit est traité sur la page <a href="/loi-applicable-successions-internationales/">quelle loi est applicable aux successions internationales</a>.</p>

<h2>Ouvrir votre dossier de succession internationale</h2>

<h2>Quels pays sont liés par le règlement&nbsp;?</h2>

<p>C'est le point sur lequel beaucoup de pages en ligne sont restées en arrière. Au 15 octobre 2026&nbsp;:</p>

<table>
  <thead><tr><th>Catégorie</th><th>Conséquence</th></tr></thead>
  <tbody>
    <tr><td><strong>25 États membres de l'Union</strong></td><td>Appliquent le règlement</td></tr>
    <tr><td><strong>Danemark et Irlande</strong></td><td>États membres, mais ne participent pas à ce règlement</td></tr>
    <tr><td><strong>Royaume-Uni</strong></td><td>N'y a jamais participé, et n'est plus un État membre depuis 2020</td></tr>
    <tr><td><strong>États tiers</strong> (Suisse, États-Unis, Maroc…)</td><td>Hors règlement&nbsp;: leurs propres règles s'appliquent</td></tr>
  </tbody>
</table>

<p>Attention à une confusion fréquente : le règlement s'applique <strong>devant les autorités des 25 États liés</strong>, même lorsque la loi désignée est celle d'un État tiers. Un notaire français saisi d'une succession dont le défunt vivait au Canada applique bien le règlement pour désigner la loi — et cette loi sera canadienne.</p>

<h2>Le certificat successoral européen, la vraie nouveauté</h2>

<p>Les articles 62 et suivants créent un document unique, le <strong>certificat successoral européen</strong>. Il prouve, dans tous les États liés et sans formalité supplémentaire, la qualité d'héritier, les droits de chacun et les pouvoirs de l'exécuteur ou de l'administrateur.</p>

<p>Concrètement : une banque italienne, un conservateur des hypothèques espagnol ou un notaire belge doivent l'accepter sans redemander d'acte local. En France, il est délivré par le notaire chargé de la succession.</p>

<p>Trois points pratiques à connaître&nbsp;:</p>

<ul>
  <li>Son usage n'est <strong>pas obligatoire</strong> : il ne remplace pas les documents internes, il s'y ajoute.</li>
  <li>La <strong>copie certifiée conforme est valable six mois</strong>, renouvelable — une durée courte, qui suppose de caler les démarches à l'étranger sur sa délivrance.</li>
  <li>Il ne vaut <strong>pas</strong> dans les États tiers, ni au Danemark ni en Irlande.</li>
</ul>

<p>Dans ces cas-là, c'est <a href="/acte-de-notoriete-en-succession-internationale/">l'acte de notoriété en succession internationale</a> qui prend le relais.</p>

<h2>Quel notaire, quel tribunal&nbsp;?</h2>

<p>Le règlement retient le même rattachement pour la compétence que pour la loi : les autorités de l'État de la <strong>dernière résidence habituelle</strong> du défunt sont compétentes pour l'ensemble de la succession. Un principe de concentration, qui évite d'ouvrir une procédure par pays.</p>

<p>Quand le défunt résidait dans un État tiers mais laisse des biens dans un État lié, des règles subsidiaires rouvrent la compétence — notamment sur les biens situés dans cet État. C'est l'une des situations où un dossier parisien se justifie même pour une résidence lointaine.</p>

<h2>Et avant le 17 août 2015&nbsp;?</h2>

<p>Les successions ouvertes avant cette date restent soumises aux anciennes règles françaises, dites scissionnistes : la loi du dernier domicile pour les biens meubles, la loi du lieu de situation pour chaque immeuble. Une même succession pouvait donc relever de trois ou quatre lois. C'est cette dispersion que le règlement a voulu supprimer.</p>

<p>Pour le déroulé complet d'un dossier, acte par acte, voir <a href="/comment-se-passe-une-succession-internationale/">comment se passe une succession internationale</a>.</p>

<h2>Questions fréquentes</h2>

<h3>Le règlement européen s'applique-t-il aux non-Européens&nbsp;?</h3>
<p>Oui. Il ne tient pas compte de la nationalité du défunt mais du lieu de sa dernière résidence habituelle. Un ressortissant américain décédé alors qu'il vivait à Paris relève du règlement.</p>

<h3>Le certificat successoral européen est-il obligatoire&nbsp;?</h3>
<p>Non. Il est facultatif et ne remplace pas les documents nationaux. Il est utile dès qu'un bien, un compte ou un héritier se trouve dans un autre État lié.</p>

<h3>Combien de temps le certificat est-il valable&nbsp;?</h3>
<p>La copie certifiée conforme est valable six mois, renouvelable. Le certificat lui-même reste au dossier du notaire qui l'a délivré.</p>

<h3>Le règlement règle-t-il les droits de succession&nbsp;?</h3>
<p>Non, la fiscalité est expressément exclue de son champ. Les droits restent fixés par chaque État et par les conventions fiscales bilatérales.</p>

<h3>Le Royaume-Uni est-il concerné&nbsp;?</h3>
<p>Non, à double titre : il n'a jamais participé à ce règlement, et il n'est plus un État membre depuis 2020. Une succession comportant des biens britanniques suppose donc un traitement distinct.</p>
```

## 8 · JSON-LD FAQPage

Même format que la page sœur, sur les cinq questions ci-dessus.

## 9 · Contrôle

| Critère | Verdict |
|---|---|
| Exact match dans le title, au plus tôt | oui — « Règlement européen sur les successions » |
| H1 ≠ title | oui |
| P1 = la réponse | oui — numéro, date et principe dans la première phrase |
| Fait daté + source dans le premier tiers | oui — 650/2012, 4 juillet 2012, 17 août 2015 |
| Définition en une phrase | oui |
| Donnée structurée | oui — deux tableaux |
| Module au-dessus du 2e écran | oui — le tableau « règle / ne règle pas » |
| La suite est dans la page | oui — 4 liens internes contextuels |
| Nom de l'étude absent du title | oui |

**Point d'attention.** Le chiffre de 25 États liés doit être revérifié à
chaque révision annuelle de la page : il bouge avec les élargissements.
