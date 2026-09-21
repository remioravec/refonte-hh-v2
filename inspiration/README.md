# Stock de sites d'inspiration

Références captées pour la refonte helloharel.com. Un dossier par site :
le DOM rendu, la version contenu quand le site l'expose, et une fiche `NOTES.md`
(design system relevé, patterns d'interface, SEO).

| Site | Secteur | Ce qu'on y prend | Fiche |
|---|---|---|---|
| [Allô](https://www.withallo.com/fr) | SaaS téléphonie IA | Monochrome + 1 accent, nav 2 étages, FAQ par objection, JSON-LD `@graph` + version `.md` pour les LLM | [`withallo/NOTES.md`](withallo/NOTES.md) |

## Capter un nouveau site

```bash
mkdir -p inspiration/<nom>
curl -sSL -A "Mozilla/5.0" "<url>" -o inspiration/<nom>/<nom>-home.html
```
