# Outbound — Salons agroalimentaire (Hello Harel)

Projet de prospection B2B : constituer une base d'**exposants** des salons
agroalimentaires français (= prospects de Hello Harel) avec contacts email,
pour des campagnes outbound conformes.

## ⚖️ Conformité (CNIL / RGPD) — cadre de collecte

La prospection B2B par email est autorisée en France **sans consentement
préalable** si :
1. le destinataire est un **professionnel** et le message **concerne son métier**
   (ERP agroalimentaire ↔ industriel/grossiste/artisan de l'agro) ;
2. un **lien de désinscription (opt-out)** est présent dans chaque email ;
3. la personne est **informée** de l'usage de ses données (mention + politique) ;
4. la **source** de chaque donnée est documentée (traçabilité).

Règles appliquées à la base :
- on privilégie les **emails professionnels** (génériques `contact@`, `commercial@`
  ou nominatifs publiés sur les mentions légales / pages contact) ;
- **minimisation** : on ne stocke que les champs utiles à la prospection pro ;
- chaque ligne porte sa **`source_url`** et sa **`date_collecte`** ;
- pas de données sensibles ; suppression sur simple demande.

## Pipeline (5 phases)

| Phase | Objet | Sortie |
|---|---|---|
| **1. Référentiel salons** | Lister 100 % des salons agro FR + métiers | `salons-agroalimentaire-france.csv` ✅ |
| **2. Exposants** | Scraper les annuaires d'exposants (plusieurs éditions/années) | `exposants-bruts.csv` |
| **3. Emails** | Visiter les sites exposants (mentions légales / contact) → email | `exposants-emails.csv` |
| **4. Nettoyage** | Dédoublonnage, validation syntaxe + MX, exclusion hors-cible | `base-clean.csv` |
| **5. Base finale** | Base enrichie prête campagne (segmentée par métier/salon) | `base-outbound-finale.csv` |

## Schéma de la base finale (cible)

```
salon ; edition_annee ; entreprise ; secteur_metier ; site_web ;
email ; type_email (generique|nominatif) ; nom_contact ; fonction ;
ville ; departement ; telephone ; source_url ; date_collecte ;
statut_validation (valide|risque|invalide) ; segment_ICP
```

## Statut

- ✅ Phase 1 : référentiel des salons (v1, ~28 salons taggés par pertinence ICP).
- ⏳ Phase 2-5 : pipeline de scraping à construire (scripts dédiés, gatés et
  respectueux des robots.txt / CGU de chaque annuaire).

## Note technique

Le scraping s'appuiera sur les annuaires d'exposants en ligne (la plupart des
gros salons en publient un). Volume estimé : plusieurs milliers d'exposants →
collecte par lots, idempotente, avec cache et journalisation.
