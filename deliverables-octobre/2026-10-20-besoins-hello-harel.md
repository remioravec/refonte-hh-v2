# Besoins Hello Harel — inventaire complet

État arrêté le 20 octobre 2026. Sources : le point hebdomadaire du 10 octobre,
la discussion WhatsApp de Maxence du 17 octobre, les demandes de Rémi du 20 octobre,
et les défauts relevés en vérifiant le site, la base et le code.

**38 besoins** — Bloqué 3 · En cours 2 · À faire 16 · Fait 13 · Écarté 4

Version consultable et filtrable : artefact « Besoins Hello Harel ».

---

## Le site helloharel.com

### Une page d'accès client, ou une redirection

**À faire** · demandé par Claude · Relevé 15/10

/vente/ sort en position 1 sur « hello harel connexion » et « helloharel » — 445 impressions de marque pour 1 clic. Des clients existants atterrissent sur une page commerciale au lieu de leur espace.

> Défaut d'expérience et signal gâché. À arbitrer : page d'accès ou redirection.

### Alléger les 46 pages de plus de 300 ko

**À faire** · demandé par Claude · Audit

> Ticket T15, ouvert.

### Élaguer les 17 questions de FAQ

**À faire** · demandé par Claude · Relevé 15/10

/fonctionnalites/planification-production-erp/ porte 17 questions de FAQ.

### Retirer « intégration, formation et support compris »

**Fait** · demandé par Maxence · WhatsApp 17/10

La page tarifs annonçait ces trois prestations comme comprises alors qu'elles sont vendues à part via Harel Formation. Un client l'a relevé.

> Corrigé le 20/10 sur /tarifs/, deux occurrences. Vérifié en ligne.

### Appeler ça des licences, pas des plans

**Fait** · demandé par Maxence · WhatsApp 17/10

> Hero, H2 de grille et sous-titre repris le 20/10.

### Passer le badge « Populaire » de Garden à Forest

**Fait** · demandé par Maxence · WhatsApp 17/10

> Fait le 20/10. Forest est seule mise en avant, vérifié en ligne.

### Corriger le comparatif facturation

**Fait** · demandé par Claude · Relevé 20/10

La page annonçait « Starter 99 € — Pro 199 €, déploiement et formation inclus » pour Hello Harel. Les licences réelles sont 49 / 79 / 99, et rien n'est inclus. Le comparatif plaçait Hello Harel plus cher qu'il n'est, face à Pennylane et Sellsy à 30-100 €.

> Sept corrections le 20/10. Les 9 blocs JSON-LD vérifiés intacts.

### Renommer le champ honeypot du formulaire

**Fait** · demandé par Claude · Relevé 20/10

Le champ piège s'appelait « website », un nom que les navigateurs remplissent automatiquement. Trois pièges étaient posés dessus : le JS de la page, /hh/v1/contact et /hh/v1/lead. Quand il se déclenchait, le visiteur voyait « Merci », aucun mail ne partait et le lead n'était écrit nulle part.

> Renommé en « hh_zc7 » le 20/10, trois scénarios testés en ligne. Combien de demandes ont été perdues reste inconnu : rien n'était journalisé.

### Retirer « sans intégrateur »

**Écarté** · demandé par Maxence · WhatsApp 17/10

Maxence est devenu intégrateur à son compte (Integralia Systems) et demande le retrait de la mention.

> Rémi arbitre de le conserver : c'est le différenciant du site face aux ERP classiques. Relevé disponible : 83 occurrences sur 56 pages, mais 3 formulations seulement, donc 3 remplacements si la décision change.

### Revoir le statut de Maxence dans le bloc équipe

**Écarté** · demandé par Maxence · WhatsApp 17/10

Affiché « Resp. Commercial » sur /tarifs/, /qui-sommes-nous/ et le widget de contact de l'accueil, alors qu'il est passé à son compte.

> Rémi arbitre de laisser en l'état. À reprendre quand Timothy et lui auront calé le statut.


## L'outil d'attribution et le CRM

### Chaque client maître de ses étapes

**En cours** · demandé par Rémi · 20/10

Que le client crée, renomme et réordonne ses étapes lui-même, sans passer par Rémi.

> À moitié : l'écran de réglages propose des cases à cocher sur 9 étapes figées dans le code. On active ou désactive, on ne renomme pas, on ne crée pas, on ne réordonne pas. Il faut passer pipeline_stages d'un tableau de clés à des objets {clé, libellé, ordre, couleur, terminale}.

### Liste de tâches par commercial

**En cours** · demandé par Rémi · 20/10

Chaque tâche accrochée à un lead ; échéance, statut, réassignation depuis l'outil.

> Table lead_tasks créée en production le 20/10 avec RLS et index. Reste la migration drizzle, le bloc dans la fiche du lead, la page /taches et la pastille de retard. L'agent Lovable s'est arrêté faute de crédits.

### Transmettre les liens de connexion à l'équipe

**À faire** · demandé par Rémi · Point Gemini 10/10

Après finalisation des correctifs.

> À la main de Rémi.

### Vue Kanban qui est l'entonnoir

**À faire** · demandé par Rémi · 20/10

Une seule vue : colonnes Kanban et entonnoir horizontal avec les taux de conversion entre étapes.

> N'existe pas, le CRM est une liste. Maquette interactive livrée le 20/10 sur 58 vrais leads. Les taux sont calculables dès maintenant : lead_events est alimenté par un trigger depuis des semaines.

### Connexion au Google Agenda de chacun

**À faire** · demandé par Rémi · 20/10

Chaque commercial connecte son propre agenda.

> Aujourd'hui il n'y a qu'un lien « template » pré-rempli que le commercial doit valider à la main. Pas d'OAuth, donc rien ne se synchronise et rien ne revient. C'est le lot le plus coûteux : un jeton par commercial, son renouvellement, et le sens de synchronisation à trancher.

### Connecter le Drive, ou déposer des documents

**À faire** · demandé par Rémi · 20/10

Devis, comptes rendus de démo, cahiers des charges, sur le lead ou la tâche.

> Rien en base, rien dans le code.

### S'inspirer de Taap.it Conversion et Radar

**À faire** · demandé par Rémi · 20/10

Le flux d'événements en direct, les compteurs clic → lead → vente avec les taux entre eux, le dashboard partageable par lien, la valeur vie client et le délai jusqu'à la vente.

> Transposé en SEO / IA / Ads : impression → clic → lead → vente, avec la requête, le prompt ou le mot-clé porté jusqu'au revenu. La donnée est déjà collectée par le script d'attribution ; ce qui manque, c'est la vue.

### Refondre les étapes du pipeline

**Fait** · demandé par Timothy · Point Gemini 10/10

Supprimer « qualifié », remplacer « négociation » par « offre envoyée », ajouter « premier contact » et « rendez-vous pris / démo ».

> En base : pipeline_stages = new, first_contact, meeting, offer_sent, won, lost, wrong_number pour HELLOHAREL.

### Assignation des leads entre commerciaux

**Fait** · demandé par Timothy · Point Gemini 10/10

Attribuer un lead à Nicolas ou Maxence et tracer qui a fait le premier contact.

> Fait : fiche + liste, filtre, historique, mail et push.

### Retirer le téléphone des e-mails de lead

**Fait** · demandé par Timothy · Point Gemini 10/10

Pour forcer les équipes à passer par l'outil au lieu d'appeler directement. Rémi précise : pour Hello Harel seulement.

> hide_phone_in_notifications = true pour HELLOHAREL, false pour 451F et ART ET CONFORT. Lu côté serveur, non contournable.

### Accusé de réception automatique au prospect

**Fait** · demandé par Rémi · Point Gemini 10/10

> prospect_confirmation_enabled = true. Le message ne contient aucun lien de réservation, par décision après incident.

### Notification instantanée à l'assignation

**Fait** · demandé par Rémi · Point Gemini 10/10

Via l'application mobile.

> Web Push en place, clés VAPID côté serveur.

### Intégrer Hello Harel au tableau de bord consolidé

**Fait** · demandé par Rémi · Point Gemini 10/10

> Domaine helloharel.com et prompts suivis en place.

### Connecter le CRM à WhatsApp

**Écarté** · demandé par Rémi · Point Gemini 10/10

Centraliser les communications clients.

> Livré (bouton + historique), puis écarté par Rémi le 20/10 : « pas besoin ».

### Suivre les requêtes et prompts IA

**Écarté** · demandé par Rémi · Point Gemini 10/10

> Livré (section IA, tag IA, 8 prompts suivis), puis écarté par Rémi le 20/10 : « pas besoin pour le moment ».


## Google Ads

### Arbitrer le compteur de conversions

**Bloqué** · demandé par Claude · Relevé 20/10

Google Ads déclare 63 conversions sur juillet-octobre 2026. Sur la même période, 64 demandes sont réellement arrivées, dont 4 seulement attribuées à Ads.

> Ads s'attribue la quasi-totalité des soumissions du site. Le coût par conversion affiché est divisé par 16 environ, et « maximiser les conversions » optimise sur un signal qui vient à 94 % du SEO. La baisse de coût par lead présentée au point du 10/10 repose sur ce compteur.

### Importer la pause des 56 mots-clés larges

**À faire** · demandé par Rémi · Point Gemini 10/10

99 % de la dépense partait sur les partenaires de recherche, qualité 1 à 4.

> Fichier d'import prêt. L'API refuse cette opération, c'est à faire dans Ads Editor ou à la main.

### Rééquilibrer les budgets de groupes d'annonces

**À faire** · demandé par Rémi · Point Gemini 10/10

> Même restriction d'API.

### Régler les objectifs de conversion au niveau campagne

**À faire** · demandé par Rémi · Relevé 06/10

Ne garder que « Demande de démo - Page Contact ».

> Cinq actions de conversion sont immuables par API (Google-hosted, smart campaign, Universal Analytics). À faire dans l'interface.


## Le produit ERP — côté Harel Systems

### Import en masse des produits

**Bloqué** · demandé par Maxence · Point Gemini 10/10

Produits, catégories, prix et codes-barres, saisis un par un aujourd'hui.

> C'est ce qui bloque le démarrage du client de Maxence depuis le 10/10. Côté Harel Systems, pas Rémi.

### Fonctionnalité de découpe

**À faire** · demandé par Maxence · Point Gemini 10/10

Projet initialement prévu pour septembre, repoussé.

> Lancement espéré en novembre. Côté Harel Systems.

### Dossier Monoprix : RFI et MDA avant démo

**À faire** · demandé par Timothy · Point Gemini 10/10

Documents administratifs et techniques à envoyer avant toute démonstration, comme pour Biocentre Loire.

> Côté Harel Systems.


## Données et technique

### Récupérer les téléphones manquants

**Bloqué** · demandé par Rémi · Brief

89 leads de 2026 sans numéro : le formulaire a cessé de les transmettre à la base en janvier 2026.

> Bloqué sur le choix d'accès WordPress : A snippet lecture seule temporaire, B MySQL par variables d'environnement, C plugin d'export.

### Décocher « Capitaliser les titles » dans Rank Math

**À faire** · demandé par Rémi · Audit

Le réglage force une casse que les titles refondus ne veulent pas.

> 29 titles sont épinglés dans l'extrait 12 pour compenser. Ce rustine disparaît quand le réglage est décoché.

### Vérifier l'exposition publique des leads WordPress

**À faire** · demandé par Claude · Relevé

Le type hh_lead est lisible en REST. 103 enregistrements.

> À confirmer : la lecture anonyme est-elle ouverte, et le tableau de bord s'en sert-il ?

### Poser SPF, DKIM et DMARC sur remi-oravec.fr

**À faire** · demandé par Claude · Audit

> Fiabilise la remise des notifications de lead.

### Sortir 100 % des leads sur trois ans

**Fait** · demandé par Rémi · 20/10

> 511 demandes uniques du 18/08/2023 au 14/10/2026, aucun mois vide. Reconstruit depuis les soumissions Elementor et la base d'attribution, dédoublonné, 24 entrées parasites retirées.

### Horodater les changements d'étape

**Fait** · demandé par Claude · Relevé 20/10

Sans historique, l'entonnoir montre une photo et non une conversion.

> Déjà en place : lead_events, écrit par le trigger log_lead_changes, 28 événements. Le client ne peut insérer que des événements whatsapp.

