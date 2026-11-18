# Tâches commerciales — spécification du lot 1

Projet : Rémi Oravec Attribution (`c881fc77-70b4-458b-b4e0-2085fbc9d192`)
Écrit le 20/10/2026 · périmètre : les tâches seules. Agenda OAuth et documents hors lot.

---

## Pourquoi ce lot d'abord

Sur les 58 leads travaillés depuis août 2026, **47 sont encore au stade « Nouveau »** :
16 % de passage de « Nouveau » à « Premier contact ». Quand un lead est contacté, il
avance normalement (33 %, puis 67 %, puis 50 %). **Le goulot est au premier geste.**

Une liste de tâches accrochée au lead est la réponse directe à ce goulot. C'est aussi
le seul chantier entièrement neuf : tout le reste du pipeline existe déjà.

## Ce qui existe déjà et qu'on ne refait pas

| Brique | Où |
|---|---|
| Étapes par client | `workspaces.pipeline_stages`, lues par `pipelineOptions()` |
| Historique des changements | `lead_events`, écrit par le trigger `log_lead_changes` |
| Assignation | `leads.assigned_to` + `AssigneeSelect.tsx` |
| Lien Google Agenda | `lib/calendarReminder.ts` → `buildReminderUrl()` |
| Masquage du téléphone | `workspaces.hide_phone_in_notifications`, lu côté serveur |

## Base

```sql
create table public.lead_tasks (
  id           uuid primary key default gen_random_uuid(),
  workspace_id uuid not null references public.workspaces(id) on delete cascade,
  lead_id      uuid not null references public.leads(id)      on delete cascade,
  title        text not null check (char_length(title) between 1 and 300),
  due_at       timestamptz,
  done_at      timestamptz,
  assigned_to  uuid references auth.users(id) on delete set null,
  created_by   uuid references auth.users(id) on delete set null,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

create index lead_tasks_a_faire_idx
  on public.lead_tasks (workspace_id, assigned_to, due_at)
  where done_at is null;
create index lead_tasks_lead_idx on public.lead_tasks (lead_id);
```

**RLS** : exactement la politique de `leads` — un membre de l'espace lit et écrit les
tâches de son espace, rien d'autre. `workspace_id` est vérifié côté serveur, jamais
pris depuis le client.

**Migration** : `drizzle/migrations/0010_lead_tasks.sql`, plus l'entrée de journal et
le snapshot qui vont avec.

## Interface

**1 · Dans la fiche du lead** (`LeadSheet.tsx`) — un bloc « Tâches » :
liste triée par échéance, les faites en bas et barrées ; ajout en une ligne
(titre, échéance facultative, assigné — par défaut le commercial du lead) ;
case à cocher qui écrit `done_at` ; suppression. Chaque tâche qui porte une
échéance affiche le lien Google Agenda construit par `buildReminderUrl()`.

**2 · Une page « Mes tâches »** (`/taches`, entrée de menu) :
les tâches de l'utilisateur connecté, groupées **En retard · Aujourd'hui ·
Cette semaine · Plus tard · Sans échéance**. Chaque ligne nomme son lead et
ouvre sa fiche. Un commutateur « toutes les tâches de l'espace » pour les admins.

**3 · Dans la liste du CRM** (`CRM.tsx`) : une pastille d'alerte sur le lead qui
porte au moins une tâche en retard. Pas de colonne supplémentaire.

## Contraintes à tenir

- **Ne jamais écrire dans `lead_events` depuis le navigateur.** L'historique est au
  trigger. Si une tâche doit laisser une trace, c'est un trigger `lead_tasks` qui
  l'écrit, pas le client.
- **Passer par `pipelineOptions()`** partout où une étape est affichée.
- **Aucune référence à « seo-monkey »**, sous aucune forme.
- Les notifications de tâche (mail, push, rappel d'échéance) **ne sont pas dans ce lot**.
- `updated_at` tenu par un trigger, pas par le client.

## Ce qu'on vérifie avant de dire que c'est fini

1. Une tâche créée depuis la fiche d'un lead apparaît dans « Mes tâches ».
2. Une tâche en retard pose bien la pastille sur la ligne du CRM.
3. Un membre d'un autre espace ne voit aucune de ces tâches (contrôle RLS).
4. Supprimer un lead supprime ses tâches, et ne casse rien d'autre.
5. Le lien Google Agenda ouvre un événement pré-rempli au nom du lead.

## Après ce lot

| Suite | Pourquoi dans cet ordre |
|---|---|
| Vue Kanban + entonnoir | consomme `lead_events`, déjà alimenté — rien à créer en base |
| Étapes vraiment éditables | `pipeline_stages` est aujourd'hui un tableau de clés figées dans `ALL_STAGES` ; il faut des objets `{clé, libellé, ordre, couleur, terminale}` pour renommer, réordonner et créer |
| Google Agenda en OAuth | le plus coûteux : un jeton par commercial, son renouvellement, le sens de synchronisation |
| Documents / Drive | dépend du choix de stockage |

---

## Ce qui a été posé le 20/10/2026

La table `lead_tasks` est **créée en production** : 10 colonnes, 3 index, le trigger
`updated_at`, RLS active et 4 politiques calquées à l'identique sur celles de `leads`
(`is_workspace_member(workspace_id)`). Table vide, aucune donnée existante touchée.

L'agent Lovable a enregistré le périmètre en mémoire (`mem://features/lead-tasks-scope`)
et inscrit la ligne dans `roadmap.md`, puis **l'espace Lovable est tombé à court de
crédits** avant d'écrire la moindre interface. Il reste donc à faire :

- la migration drizzle `0010_lead_tasks.sql` qui déclare formellement ce que la base
  porte déjà (sans quoi le schéma versionné et la production divergent) ;
- le bloc « Tâches » dans `LeadSheet.tsx` ;
- la page `/taches` et son entrée de menu ;
- la pastille de retard dans `CRM.tsx`.

Pour annuler ce qui a été posé : `drop table public.lead_tasks cascade;` — rien d'autre
n'en dépend.
