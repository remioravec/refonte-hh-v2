# Outil Hello Harel — les 15 besoins

Vérifié le 20 octobre 2026 contre la base de production, le code du projet et sa
roadmap. Sources : le point hebdomadaire du 10 octobre et les précisions de Rémi
du 20 octobre.

Fait 6 · À faire 5 · En cours 2 · Écarté 2.

## Dans quel ordre

| | Besoin | Pourquoi là | Effort |
|---|---|---|---|
| 1 | Liste de tâches par commercial | Autonome, et c'est la réponse directe au goulot : 47 leads sur 58 jamais touchés. | moyen |
| 2 | Vue Kanban qui est l'entonnoir | Consomme lead_events, déjà alimenté. Rien à créer en base. | moyen |
| 3 | Chaque client maître de ses étapes | Petite migration de champ, débloque la promesse « chaque client son pipeline ». | petit |
| 4 | Connecter le Drive, ou déposer des documents | Dépend d'un choix de stockage à trancher d'abord. | moyen |
| 5 | Connexion au Google Agenda de chacun | Le plus coûteux : un jeton par commercial et son renouvellement. | gros |
| 6 | S'inspirer de Taap.it Conversion et Radar | Le plus ambitieux, et il gagne à venir après le Kanban qu'il prolonge. | gros |

## Le détail

### Liste de tâches par commercial

**En cours** · Rémi, 20/10

Chaque tâche accrochée à un lead. Échéance, statut, réassignation depuis l'outil.

**Ce qui existe.** Table `lead_tasks` créée en production le 20/10 : 10 colonnes, 3 index dont un partiel sur les tâches non faites, trigger `updated_at`, RLS active, 4 politiques calquées sur celles de `leads`.

**Ce qui manque.** La migration drizzle `0010_lead_tasks.sql` qui déclare ce que la base porte déjà, le bloc « Tâches » dans `LeadSheet.tsx`, la page `/taches` avec son entrée de menu, la pastille de retard dans `CRM.tsx`.

> L'agent Lovable s'est arrêté faute de crédits après avoir seulement enregistré le périmètre. La spec est écrite et prête à coller.

### Chaque client maître de ses étapes

**En cours** · Rémi, 20/10

Que le client crée, renomme et réordonne ses étapes lui-même.

**Ce qui existe.** `workspaces.pipeline_stages` existe et est rempli pour HELLOHAREL. L'écran de réglages (`WorkspaceOptionsCard.tsx`) propose des cases à cocher.

**Ce qui manque.** Les 9 étapes sont figées en dur dans `ALL_STAGES`. On active ou on désactive, on ne renomme pas, on ne crée pas, on ne réordonne pas. Il faut passer le champ d'un tableau de clés à des objets `{clé, libellé, ordre, couleur, terminale}`, et adapter `pipelineOptions()`.

> Migration de données à prévoir pour les trois espaces existants, dont deux sont encore sur la valeur par défaut (null).

### Vue Kanban qui est l'entonnoir

**À faire** · Rémi, 20/10

Une seule vue : les colonnes du Kanban sont les étages de l'entonnoir, avec les taux de passage entre étapes.

**Ce qui existe.** Rien côté vue — le CRM est une liste (`CRM.tsx`, `StatusBadge`, `AssigneeSelect`, `BulkActionsBar`). Mais `lead_events` est alimenté depuis des semaines par le trigger `log_lead_changes` : 28 événements horodatés, types `status`, `assigned`, `whatsapp`.

**Ce qui manque.** Les composants de colonnes et d'entonnoir. Les taux se calculent sur `lead_events`, rien à créer en base.

> Maquette interactive livrée le 20/10 sur 58 vrais leads. Elle montre le vrai problème : 16 % seulement passent de « Nouveau » à « Premier contact », alors que la suite de l'entonnoir est saine (33 %, 67 %, 50 %).

### Connexion au Google Agenda de chacun

**À faire** · Rémi, 20/10

Chaque commercial connecte son propre agenda.

**Ce qui existe.** `lib/calendarReminder.ts` fabrique un lien `calendar.google.com/render?action=TEMPLATE`.

**Ce qui manque.** Ce lien n'est qu'un raccourci : il ouvre un formulaire pré-rempli que le commercial valide à la main. Pas d'OAuth, donc rien ne se synchronise et rien ne revient. Il faut un jeton par utilisateur, son renouvellement, et trancher le sens de synchronisation.

> Ma recommandation : la tâche créée dans le CRM pose un événement dans l'agenda, et l'agenda ne réécrit pas dans le CRM. Le bidirectionnel coûte bien plus cher pour un gain que les commerciaux ne demandent pas.

### Connecter le Drive, ou déposer des documents

**À faire** · Rémi, 20/10

Devis, comptes rendus de démo, cahiers des charges, sur le lead ou la tâche.

**Ce qui existe.** Rien en base, rien dans le code.

**Ce qui manque.** Tout. Le choix de stockage conditionne le reste : Supabase Storage, ou OAuth Drive par utilisateur comme pour l'agenda.

### S'inspirer de Taap.it Conversion et Radar

**À faire** · Rémi, 20/10

Le flux d'événements en direct, les compteurs clic → lead → vente avec les taux entre eux, le dashboard partageable par lien, la valeur vie client et le délai jusqu'à la vente.

**Ce qui existe.** La donnée est déjà collectée par le script d'attribution : `leads` porte first_touch et last_touch (source, medium, campagne, landing, date), `ai_sessions` et `gsc_data_cache` complètent.

**Ce qui manque.** La vue, pas la donnée. Transposé en SEO / IA / Ads : impression → clic → lead → vente, avec la requête, le prompt ou le mot-clé porté jusqu'au revenu.

> C'est le même objet que le Kanban-entonnoir : l'entonnoir marketing en haut, l'entonnoir commercial en bas, sur un seul écran.

### Transmettre les liens de connexion à l'équipe

**À faire** · Rémi, point du 10/10

Après finalisation des correctifs.

**Ce qui existe.** Les invitations existent (`pending_invitations`, `InviteMemberDialog`), 18 membres déjà en base.

**Ce qui manque.** Un geste de Rémi, pas du développement.

### Refondre les étapes du pipeline

**Fait** · Timothy, point du 10/10

Supprimer « qualifié », remplacer « négociation » par « offre envoyée », ajouter « premier contact » et « rendez-vous pris / démo ».

**Ce qui existe.** `pipeline_stages` = new, first_contact, meeting, offer_sent, won, lost, wrong_number pour HELLOHAREL. Exactement les étapes décidées.

### Assignation des leads entre commerciaux

**Fait** · Timothy, point du 10/10

Attribuer un lead et tracer qui a fait le premier contact.

**Ce qui existe.** Fiche et liste, filtre, historique, mail et push. `leads.assigned_to` + `AssigneeSelect.tsx`.

### Retirer le téléphone des e-mails de lead

**Fait** · Timothy, point du 10/10

Pour forcer le passage par l'outil. Rémi précise : pour Hello Harel seulement.

**Ce qui existe.** `hide_phone_in_notifications` = true pour HELLOHAREL, false pour 451F et ART ET CONFORT. Lu côté serveur dans chaque générateur d'e-mail et de push, donc non contournable depuis le navigateur.

### Accusé de réception automatique au prospect

**Fait** · Rémi, point du 10/10

**Ce qui existe.** `prospect_confirmation_enabled` = true. Le message ne contient aucun lien de réservation et ne lit jamais `calendar_url`, par décision après incident.

### Notification instantanée à l'assignation

**Fait** · Rémi, point du 10/10

Via l'application mobile.

**Ce qui existe.** Web Push en place. Clés VAPID générées côté serveur et stockées dans `push_config`, accessibles au seul rôle de service.

### Intégrer Hello Harel au tableau de bord consolidé

**Fait** · Rémi, point du 10/10

**Ce qui existe.** Domaine helloharel.com et 8 prompts suivis en place.

### Connecter le CRM à WhatsApp

**Écarté** · Rémi, point du 10/10

Centraliser les communications clients.

**Ce qui existe.** Livré : bouton et historique, événements `whatsapp` dans `lead_events` — le seul type que le client est autorisé à insérer.

> Écarté par Rémi le 20/10 : « pas besoin ». Le code reste en place.

### Suivre les requêtes et prompts IA

**Écarté** · Rémi, point du 10/10

**Ce qui existe.** Livré : section IA, tag IA, 8 prompts suivis, classification côté client depuis `form_data.referrer` et `utm_source`.

> Écarté par Rémi le 20/10 : « pas besoin pour le moment ». Le code reste en place.
