# Nettoyage des marqueurs de mesure — helloharel.com — 14/11/2026

## Ce qui a été retiré

| Script | Où il vivait | État |
|---|---|---|
| `attributer.js` (318 Ko) | Elementor Custom Code **5249 « Attributer IO »**, `elementor_head` prio 1 | passé en brouillon |
| `tracker.js` (CRM Lovable) | Elementor Custom Code **6072 « Oremi Attribution Tracker »**, `elementor_head` prio 1 | passé en brouillon |
| `tracker.js` (2e copie) | **WPCode Lite → Header & Footer → En-tête**, option `ihaf_insert_header` | **à retirer à la main** |

Attributer ne remplissait aucun champ du formulaire : il vise `channel`,
`channeldrilldown1` à `4`, `landingpage`, aucun n'existe sur le site.
Retrait sans contrepartie, 318 Ko de moins par page.

## Pourquoi le tracker Lovable devait partir

C'est le script de l'incident du 23/10 : `navigator.sendBeacon` avec un Blob
`application/json`, type non inscrit sur la liste sûre CORS, donc préflight
`OPTIONS` abandonné au déchargement de la page. Il était chargé **deux fois**
par page.

La balise Oravec, elle, poste en `fetch` keepalive avec
`Content-Type: text/plain` — type simple, aucun préflight — et garde une file
de rejeu (2 s, 10 s). Le défaut ne peut pas s'y reproduire.

## Ce qui a été posé

### Snippet 18 — pont de consentement CookieYes → marqueur Oravec
CookieYes n'émet aucun signal Google Consent Mode sur ce site : sans pont, le
marqueur restait en mode exempté et ne rapportait jamais la provenance.
Le pont lit le cookie `cookieyes-consent` déjà posé, pose
`window.filConsentement` avant le démarrage du marqueur, et relaie chaque
réponse (événement `cookieyes_consent_update` **et** relecture du cookie toutes
les 1,5 s pendant 10 min — l'événement seul s'est révélé intermittent au test).
Correspondance : `analytics` → mesure, `advertisement` → régies.
Aucun cookie nouveau, aucun appel réseau, GA4 et le formulaire intacts.

Vérifié au navigateur, 3 essais sur 3 : `exempte` → `consenti`,
mesure + régies à vrai, identifiant `_fil` créé, `/fil/visite` reçu par l'outil.
Refus : reste `exempte`, aucun identifiant. Zéro erreur JS sur `/contact/`.

### Snippet 20 — attribution première partie (créé, **pas encore actif**)
Remplit `te_source`, `te_medium`, `te_campaign`, `te_landing`, `workspace_id`,
les cinq champs cachés que le relai serveur du snippet 6 transmet au CRM.
Premier contact gardé en `localStorage`. **Aucun appel réseau.**
À activer avant de retirer la dernière copie du tracker, sinon le CRM perd la
source et le gclid sur chaque nouveau lead.

## Reste à faire

1. Activer le snippet 20 (refusé au classificateur, un clic dans Code Snippets).
2. WPCode Lite → Header & Footer → En-tête : ne garder que la ligne Oravec.
3. Chaîne des demandes contrôlée 4 fois pendant l'opération, toujours
   `{"ok":true,"veille":true,"crm":"200 {\"success\":true}"}`.
