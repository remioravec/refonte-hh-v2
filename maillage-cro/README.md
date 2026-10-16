# maillage-cro/ — Toolkit maillage interne + CRO

Outils Python (stdlib uniquement) pour planifier, **en DRY-RUN**, un maillage
interne « au petit oignon » (diversification d'ancres + surfeur raisonnable) et
un template CRO d'article, sur `helloharel.com` via l'API REST WordPress.

## Prérequis

```bash
export WP_USER="administration@remi-oravec.fr"
export WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"   # WP Application Password
# (jamais commité — lu uniquement à l'exécution)
```

## Pipeline

```bash
python3 inventory.py      # 1. inventaire live (lecture seule) -> inventory.json
python3 maillage.py       # 2. plan de maillage -> MAILLAGE-DRY-RUN.md + .json
python3 cro_article.py    # 3. plan CRO + previews -> CRO-PLAN.md + preview/*.html
```

Aucune de ces commandes n'écrit sur WordPress. L'étape d'application live sera un
script séparé, gaté par `--live`, ajouté une fois les plans validés.

## Fichiers

| Fichier | Rôle |
|---|---|
| `wp_common.py` | Accès REST (creds en env, écriture gatée `live=True`) |
| `inventory.py` | Inventaire : structure, mots, H2, liens **contextuels** vs boilerplate |
| `anchors.py` | Pools d'ancres (amorcés GSC) + sélecteur anti-cannibalisation |
| `clusters.py` | Carte du cocon (L1/L2/L3) + affinités pages money |
| `maillage.py` | Moteur de planification du maillage (dry-run) + rapports |
| `cro_tools.py` | Outils interactifs, visuels inter-H2, échelle de CTA |
| `cro_article.py` | Assemblage previews + plan CRO |
| `STRATEGIE-MAILLAGE-CRO.md` | Stratégie complète |

## Sécurité

Purger les anciens identifiants en clair dans `../fix-links.py` et
`../faq-template.py`, puis régénérer le mot de passe d'application.
