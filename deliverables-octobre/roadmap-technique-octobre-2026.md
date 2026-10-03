# Roadmap technique — octobre 2026

Relevé par crawl des **172 URL publiées**, le 01/10/2026. Chaque ligne est
mesurée sur la page servie, pas déduite. Aucune URL en erreur : les 172
répondent 200.

Les tickets T1 à T8 d'août et septembre sont marqués TERMINÉ dans la
roadmap. Trois d'entre eux ont **régressé** : le crawl les retrouve sur
les pages produites depuis. C'est la première chose à traiter, parce
qu'une correction qui revient n'a pas été corrigée à la source.

---

## T9 · Les pages de septembre étaient en noindex — **FAIT**

Trois landings livrées en septembre et marquées INDEXÉ dans la roadmap
sortaient `nofollow, noindex` :

| page | requête cible |
|---|---|
| `/agroalimentaire/fruits-et-legumes/` | erp fruits et légumes |
| `/agroalimentaire/pme-en-croissance/` | erp pme agroalimentaire |
| `/agroalimentaire/produits-de-la-mer/` | erp produits de la mer |
| `/blog/erp-agroalimentaire/` | erp agroalimentaire |

Ce n'était pas l'extrait « pages de test A/B » — ses identifiants sont
d'autres pages. C'était un réglage Rank Math posé page par page.

Corrigé par `rankmath/v1/updateMeta`, vérifié sur la page servie : les
quatre sortent désormais `index, follow`.

**ACCEPTATION** : les 4 URL en `index, follow` au recrawl. ✅

---

## T10 · Le générateur de meta description a de nouveau lâché — **FAIT**

Le ticket T1 d'août portait sur 55 pages dont la description sortait en
CSS brut. Il est marqué TERMINÉ. Le crawl en retrouve **quatre**, et ce
sont exactement les pages créées depuis :

    /agroalimentaire/fruits-et-legumes/
    /agroalimentaire/pme-en-croissance/
    /agroalimentaire/produits-de-la-mer/
    /agroalimentaire/viande/

Plus `/conformite-loi-anti-fraude-tva/`, sans description du tout.

Les cinq descriptions ont été réécrites et posées, toutes entre 516 et
678 px. Mais **la cause n'est pas traitée** : le gabarit continue de
servir du CSS comme description quand le champ est vide. Tant qu'elle
l'est, chaque nouvelle page naîtra avec le défaut.

**ACCEPTATION** : 0 description contenant `{` ou `}` au recrawl ✅ ·
cause corrigée dans le gabarit ❌ **à faire**

---

## T11 · 88 descriptions dépassent 985 px

76 articles et 12 pages. La pire fait **1 552 px**
(`/comparatifs/meilleur-logiciel-facturation-grossiste-negoce-2026/`),
soit plus d'une fois et demie ce que Google affiche.

Le ticket T3 d'août a traité les titles ; les descriptions ne l'ont pas
été, ou ont été réécrites depuis sans contrainte de largeur.

**ACCEPTATION** : toutes les descriptions entre 400 et 985 px.
**Charge** : 4 h — la réécriture se fait par lot, triée par impressions.

---

## T12 · 33 titles en casse anglaise

« ERP Fruits **Et** Légumes », « Prix **De** Revient », « Sortir
**D'**Excel **Sans** Tout Casser ». L'extrait « Casse française des
titles refondus » est actif mais ne couvre pas ces pages.

Un title en casse anglaise se lit comme une traduction automatique dans
la SERP. Sur des requêtes de marque métier, c'est un signal de qualité
qui coûte du clic.

**ACCEPTATION** : aucun title avec une minuscule grammaticale en
majuscule, hors noms propres et sigles. **Charge** : 2 h

---

## T13 · Le balisage structuré est dupliqué sur 133 pages

Le ticket T5 d'août portait sur ce défaut à l'accueil. Il est marqué
TERMINÉ. Il est aujourd'hui sur **133 pages**, et pire qu'avant :

| page | Organization | AggregateRating |
|---|---|---|
| `/comparatifs/meilleur-erp-negoce-distribution-alimentaire-2026/` | **×10** | **×10** |
| `/comparatifs/meilleur-logiciel-facturation-grossiste-negoce-2026/` | **×10** | **×10** |
| 5 pages `/fonctionnalites/` | ×7 | ×2 |

Dix `AggregateRating` sur une page, c'est le cas où Google ignore les
étoiles — et les étoiles sont l'atout de Hello Harel dans la SERP
(5,0 sur 31 avis).

**ACCEPTATION** : une seule entité par type et par page, test des
résultats enrichis sans avertissement de doublon. **Charge** : 3 h

---

## T14 · 207 images encore hors WebP, sur 103 pages

Le ticket T7 d'août a converti la médiathèque. 207 images servies en PNG
ou JPEG sont revenues depuis, réparties sur 103 pages — surtout des
articles de blog.

**ACCEPTATION** : 100 % des images de contenu en WebP, aucune au-dessus
de 200 ko. **Charge** : 2 h

---

## T15 · Deux pages servent 432 ko

`/comparatifs/meilleur-erp-negoce-distribution-alimentaire-2026/` et
`/comparatifs/meilleur-logiciel-facturation-grossiste-negoce-2026/`
servent 432 ko de HTML chacune, pour 354 ko de contenu en base. Elles
rendent correctement leurs 22 sections — le seuil de rendu n'est pas
atteint — mais elles n'ont aucune marge, et ce sont elles qui portent le
balisage dupliqué ×10.

**ACCEPTATION** : moins de 300 ko servis. **Charge** : 2 h

---

## T16 · Cinq pages sans H1, une avec deux

Sans H1 : `/cgu/`, `/mentions-legales/`,
`/politique-de-confidentialite/`, `/conformite-loi-anti-fraude-tva/`.
Deux H1 : `/comparatifs/`.

Les trois premières sont des pages légales, l'enjeu est faible. La
quatrième et `/comparatifs/` sont des pages de contenu.

**ACCEPTATION** : un H1 et un seul par page. **Charge** : 1 h

---

## Ce que le crawl ne montre pas, et qui reste ouvert

- **Deux articles publiés sont inaccessibles** : `/blog/erp-boissons/`
  et `/blog/logiciel-maree-mareyeur/` répondent 301 vers une autre page.
  Les redirections sont dans l'extrait « Redirections 301 », lignes 12
  et 14. Décision à prendre : les rouvrir ou les supprimer pour de bon.
- **Le domaine expéditeur des mails** n'a ni SPF, ni DKIM, ni DMARC, et
  helloharel.com publie deux SPF en conflit. Hors périmètre technique du
  site, mais c'est ce qui décide si une demande arrive.
