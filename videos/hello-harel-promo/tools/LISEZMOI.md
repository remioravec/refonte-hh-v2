# Comment ce film est fabriqué

Tout est régénérable. Aucune étape n'est manuelle.

| Script | Rôle |
|---|---|
| `miroir_site.mjs` | Sert `helloharel.com` en HTTP local. Nécessaire parce que le proxy interne de `hyperframes capture` refuse les IP privées et que Chromium ne lit pas la CA du proxy d'agent. Tout le TLS sortant reste vérifié par Node. |
| `extraire_site.mjs` | Relève sur le DOM réel : jetons de marque, textes, images, et les 11 tableaux de bord `<figure class="ui">` avec une capture de référence chacun. |
| `extraire_css_ui.mjs` | Extrait le CSS du système `.ui` **en respectant les `@media`** — évaluées à 1920 de large. Sans ça, les règles mobiles masquent des onglets de navigation. |
| `completer_voix.py` | Synthétise séquentiellement les répliques manquantes (le palier gratuit ElevenLabs limite la concurrence) et complète `audio_meta.json`. |
| `generer_plans.py` | Génère les 10 sous-compositions et `index.html` depuis une seule table de spécifications. **C'est ici qu'on modifie le film**, jamais dans `compositions/frames/`. |

## Relancer

```bash
node tools/miroir_site.mjs &                 # si on veut re-relever le site
node tools/extraire_site.mjs
node tools/extraire_css_ui.mjs
python3 tools/generer_plans.py               # régénère les 10 plans
npx hyperframes check --at 6,15,24,35,43,53,63,72,82,90
npx hyperframes render --fps 30 --quality delivery
```

## Deux pièges rencontrés, à ne pas refaire

1. **Les dimensions des tableaux de bord relevées sur la page sont déjà mises à l'échelle** par le site (`--k`). Il faut les mesurer hors échelle, sinon tout est sous-dimensionné.
2. **Les hauteurs dépendent des polices du film** (Inter/Urbanist locales), pas de celles du relevé. Mesurer avec les `@font-face` du projet chargées.
