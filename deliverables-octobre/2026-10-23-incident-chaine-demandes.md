# Incident — les demandes de démo n'arrivaient plus dans le CRM

**23 octobre 2026** · helloharel.com · corrigé et vérifié en production

---

## Ce qui se passait

Le client signale deux choses : il ne reçoit plus les mails de demande de démo, et les
demandes n'arrivent plus dans le CRM. Exemple donné : un prospect ivoirien
(Ivoiretransforme) a bien envoyé une demande, absente du CRM.

**Aucune demande n'a été perdue.** WordPress les enregistre toutes, dans un type de
contenu dédié (`hh_lead`, menu « Demandes »), depuis le 5 août 2026 : 117 fiches au
moment du diagnostic, dont celle du prospect ivoirien, horodatée 21/10 12:51.

La rupture était entre WordPress et le CRM.

## La cause

Le traceur du navigateur (`tracker.js`, servi depuis le stockage Supabase) envoyait la
fiche au CRM avec :

```js
const blob = new Blob([JSON.stringify(payload)], { type: 'application/json' });
navigator.sendBeacon(WEBHOOK_URL, blob);
```

`application/json` n'est pas sur la liste blanche CORS. Le navigateur doit donc envoyer
une pré-requête `OPTIONS` avant le `POST` — deux allers-retours — au moment précis où la
page se décharge après l'envoi du formulaire. Chrome abandonne la pré-requête et
journalise `blocked by CORS policy`.

Deux preuves que le problème était bien là, et pas côté serveur :

1. En `curl`, la fonction `webhook-lead` répond **HTTP 200 `{"success":true}`** et insère
   la fiche, avec ou sans en-tête `Authorization`, en-têtes CORS corrects. Le serveur
   n'a jamais été en cause.
2. La même technique (`sendBeacon` + Blob `application/json`) fonctionne pour la capture
   WordPress, **parce qu'elle est same-origin** : pas de CORS, pas de pré-requête. Même
   code, résultat inverse selon le domaine visé. C'est la signature de la panne.

Ce n'était pas une panne franche mais une perte intermittente : la pré-requête passe ou
ne passe pas selon la vitesse de déchargement de la page. D'où des demandes qui
remontent et d'autres non.

## Les demandes perdues, et ce qui en a été fait

Cinq demandes réelles présentes dans WordPress et absentes du CRM, sur la période
14/09 → 21/10/2026 :

| Date | Nom | Société | Source | Page d'entrée |
|---|---|---|---|---|
| 14/09 20:05 | Florian Coubrun | Femme | Google Ads | /negoce/ |
| 14/09 20:31 | Siby | — | Google Ads | /contact/ |
| 15/09 01:01 | baba maiga | nouradun91862996 | SEO | /blog/prix-dachat-definition/ |
| 16/09 03:53 | Abdellatif Haddaj | — | Google Ads | /negoce/ |
| **21/10 12:51** | **SÉRAPHIN GUEU** | **Ivoiretransforme** | **SEO** | **/blog/numeros-de-lot/** |

Les quatre de septembre portent un `gclid` dans leur URL d'entrée : ce sont des clics
Ads, que le CRM aurait classés en SEO faute de transmission du `gclid`. Elles sont
réinjectées avec la bonne attribution.

- **Réinjectées dans le CRM** avec leur date d'origine, leur message et leur page
  d'entrée, pas la date du rattrapage.
- **Renvoyées par mail** aux destinataires habituels (ndecerner@gmail.com, Rémi,
  Timothy), objet préfixé `(RATTRAPAGE du …)`, corps ouvrant sur un avertissement
  explicite : la demande date de telle date et le prospect attend un rappel depuis.
  Les cinq envois ont répondu `Mail envoye` en HTTP 200.

Écartés : 4 sollicitations commerciales allemandes du 23/10 (roboteruni.com,
field-sales.de), 2 tests de pénétration, et les fiches de Rémi lui-même.

## Le correctif

Le relai ne part plus du navigateur mais du serveur. Dans le snippet 6
« HH Contact Form - REST Endpoint », une fonction `hh_relay_crm()` est appelée par
`hh_store_lead()` **après** l'enregistrement WordPress, et poste la demande au webhook du
CRM en `wp_remote_post`. Pas de navigateur, pas de CORS, pas de course avec le
déchargement de la page.

Trois précautions :

- **Le handler de mail n'est pas touché.** Une demande ne peut pas être bloquée par le
  CRM : tout le relai est dans un `try/catch` silencieux, et il s'exécute après l'envoi.
- **Appel bloquant, mais sans coût pour le visiteur** : `/hh/v1/lead` est appelé en
  `sendBeacon` same-origin, la page n'attend pas la réponse. Attendre celle du CRM permet
  de journaliser l'issue dans la fiche (`_hh_crm`, visible dans une nouvelle colonne
  « CRM » de la liste des Demandes).
- **Pas de doublon** si le traceur navigateur réussit aussi : le CRM dédoublonne sur
  l'email dans les deux minutes, et le relai part dans la même seconde.

Le `gclid` est désormais extrait de l'URL de la page d'entrée et transmis au CRM :
l'attribution Ads cesse d'être perdue.

**Vérifié en production** : une demande postée sur `/hh/v1/lead` arrive dans
`public.leads` en 4 secondes, avec son message, sa page d'entrée et sa source.

## L'agent de veille quotidien

Tâche planifiée tous les jours à 07:43 (Europe/Paris), silencieuse si tout va bien,
notification poussée en cas d'échec.

Une seule commande, **aucun effet de bord** : une demande portant l'adresse
`veille@hh-chaine.invalid` et un champ `honeypot` traverse toute la chaîne. WordPress la
reconnaît et ne l'enregistre pas dans la liste des Demandes ; le CRM la rejette sur le
honeypot, sans créer de fiche et sans notifier personne. Et la réponse HTTP porte le
verdict du CRM :

```
{"ok":true,"veille":true,"crm":"200 {\"success\":true}"}
```

Trois pannes distinguées par la seule lecture de cette réponse : le CRM ne répond plus
(`crm` vide ou en échec), le snippet 6 a été réécrit et le relai a disparu (plus de champ
`veille` — c'est la panne du 23/10 qui revient), la route ou le site ne répond plus
(HTTP non 200).

**Ce que la veille ne couvre pas**, et qui reste à contrôler à la main : l'écriture en
base du CRM, et la livraison effective des mails chez le client.

## Reste ouvert

- **La moitié « mails » de la plainte n'est pas tranchée.** L'envoi réussit côté serveur
  (`{"success":true,"message":"Mail envoye"}` sur les cinq rattrapages), mais la
  livraison n'est pas vérifiable d'ici : la boîte connectée est `orvcremi@gmail.com`,
  alors que Rémi reçoit les notifications sur `administration@remi-oravec.fr`. À
  confirmer auprès de Nicolas et de Timothy : les cinq mails de rattrapage sont-ils
  arrivés, et dans quel dossier.
- **La dette SPF / DKIM / DMARC sur le domaine expéditeur reste la piste première** si
  les mails n'arrivent pas : helloharel.com publie deux SPF en conflit, et l'accusé de
  réception au prospect est désactivé pour cette raison (`HH_ACCUSE_RECEPTION`).
- `tracker.js` continue de tourner et d'échouer silencieusement sur les envois
  cross-origin. Ce n'est plus bloquant — le serveur fait le travail — mais le fichier
  gagnerait à passer en `fetch(..., {keepalive:true})` avec un `Content-Type` de la liste
  blanche. Nécessite un déploiement Lovable, donc des crédits.
