# Séquence mail outbound — Hello Harel (ERP agroalimentaire)

Séquence cold email **4 touches**, calibrée sur les benchmarks 2025 du cold email B2B.
Cible : décideurs de PME agroalimentaires (exposants des salons → base `base-outbound`).

---

## 1. Ce que disent les études (et comment la séquence s'y aligne)

| Levier | Donnée benchmark 2025 | Décision appliquée |
|---|---|---|
| **Taux d'ouverture** | Moyenne cold email ~**27–42 %** (gonflé par Apple Mail Privacy → le *reply rate* est le vrai indicateur) | Objets courts (< 50 car.), sans spam-words ; on pilote au **taux de réponse**, pas à l'ouverture |
| **Taux de réponse** | Moyenne **3–9 %** ; > 5 % = bon, **10 %+ = excellent**, top quartile **15–25 %** | Objectif réaliste **8–12 %** grâce à l'hyper-ciblage (exposants = ICP pur) |
| **Relances** | Cadence Day 0/3/10/17 → **93 % des réponses arrivent ≤ J10** ; la 1ʳᵉ relance capte une large part des réponses | 4 emails sur **17 jours** ; ne jamais s'arrêter au 1ᵉʳ envoi |
| **Personnalisation** | Objet personnalisé : **3 % → 7 %** de réponse (**+133 %**) ; perso **au-delà du prénom : +340 %** | 1ʳᵉ ligne référençant le **salon + métier + ville** de chaque prospect |
| **Longueur** | Les emails < 120 mots répondent mieux ; 1 seul CTA | Corps de 50–110 mots, **un seul** appel à l'action |
| **Multicanal** | Email + LinkedIn augmente la conversion | Touche 3 = LinkedIn optionnel (cf. note) |

*Sources : Belkins 2025, Instantly, Martal, thedigitalbloom, Built For B2B (10 000 campagnes).*
Les chiffres sont **indicatifs** (variables selon secteur/qualité de la base) — à recalibrer sur vos propres stats après 200–300 envois.

**Variables** (depuis `base-outbound`) : `{{prenom}}`, `{{nom_entreprise}}`, `{{secteur_metier}}`,
`{{ville}}`, `{{salon}}`, `{{lien_demo}}`, `{{prenom_commercial}}`.
Repli si champ vide : `{{prenom}}`→"Bonjour", `{{ville}}`→"votre région".

---

## 2. La séquence (4 touches sur 17 jours)

### ✉️ Email 1 — J0 · Accroche (référence salon)
**Objet :** `{{nom_entreprise}} — vu au salon {{salon}}`
**Objet alt (A/B) :** `traçabilité + marges chez {{nom_entreprise}}`

> Bonjour {{prenom}},
>
> J'ai repéré {{nom_entreprise}} parmi les exposants de {{salon}}. On accompagne des PME {{secteur_metier}} (souvent autour de {{ville}}) sur le même point de friction : la traçabilité, le coût de revient réel et les étiquettes INCO gérés dans des fichiers Excel séparés.
>
> Hello Harel réunit tout ça dans un seul ERP **pensé pour l'alimentaire** — poids variable, rendements, FEFO, allergènes propagés.
>
> Ça vaut 15 min d'échange pour voir ce que ça donnerait sur vos produits ?
>
> {{prenom_commercial}} — Hello Harel

---

### ✉️ Email 2 — J3 · Valeur / preuve (relance n°1)
**Objet :** `Re: {{nom_entreprise}} — vu au salon {{salon}}` *(garder le même fil)*

> Bonjour {{prenom}},
>
> Un repère concret : les PME {{secteur_metier}} qui passent d'une gestion manuelle à un ERP spécialisé ramènent leurs pertes sur DLC de 3–5 % à **moins de 1,5 % du CA**, et regagnent **2 à 5 points de marge** en pilotant leur PRI en temps réel.
>
> J'ai préparé une page qui résume ce que ça donnerait pour {{nom_entreprise}} : {{lien_demo}}
>
> Utile d'en discuter cette semaine ?
>
> {{prenom_commercial}}

---

### ✉️ Email 3 — J10 · Angle conformité (relance n°2)
**Objet :** `audit IFS / INCO chez {{nom_entreprise}} ?`

> Bonjour {{prenom}},
>
> Question rapide : aujourd'hui, combien de temps vous faut-il pour être « audit-ready » (HACCP, IFS, INCO, EGALIM) si la DDPP ou un client GMS débarque ?
>
> Avec Hello Harel, les enregistrements qualité, les allergènes et les certificats sont centralisés → dossier sorti en quelques clics au lieu de 3 jours.
>
> Je vous montre sur un de vos produits ? {{lien_demo}}
>
> {{prenom_commercial}}
>
> *(Touche multicanal optionnelle : un message LinkedIn court le même jour double souvent le taux de réponse.)*

---

### ✉️ Email 4 — J17 · Clôture (break-up)
**Objet :** `je referme le dossier {{nom_entreprise}} ?`

> Bonjour {{prenom}},
>
> Pas de retour de votre côté — c'est sûrement que ce n'est pas le moment, et c'est ok.
>
> Je clos le suivi pour ne pas encombrer votre boîte. Si la traçabilité ou les marges deviennent un sujet chez {{nom_entreprise}}, ma porte reste ouverte : {{lien_demo}}
>
> Belle continuation,
> {{prenom_commercial}} — Hello Harel

---

## 3. Bonnes pratiques d'envoi (délivrabilité = précision de la base)

- **Base déjà MX-vérifiée** (`verify_emails.py`) → bounces réduits, réputation protégée.
- Segmenter par **statut** : envoyer d'abord aux `valide`, traiter les `a_verifier` à la main.
- **Warm-up** du domaine d'envoi + ≤ ~40–50 cold emails/jour/boîte au départ.
- Envois **mardi–jeudi, 8 h–10 h** ; 1 seul CTA ; signature avec lien de désinscription.
- Mesurer **réponses** (pas ouvertures) ; recalibrer objets/accroches après ~250 envois.
- Personnaliser la 1ʳᵉ ligne : c'est le levier n°1 (+340 % au-delà du prénom).

## 4. Projection (base actuelle : 581 emails délivrables)

| Hypothèse réponse | Réponses attendues | RDV (≈30 % des réponses) |
|---|---|---|
| 5 % (prudent) | ~29 | ~9 |
| 8 % (ciblage ICP) | ~46 | ~14 |
| 12 % (séquence + perso optimales) | ~70 | ~21 |
