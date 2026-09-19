# Audit univers /agroalimentaire/ — 3 juillet 2026

Périmètre : hub `/agroalimentaire/` + 12 pages métier. Données GSC réelles (avril-juin 2026) + crawl live.

## 1. Maillage interne
**Constat :** les 3 nouvelles pages (chocolatier, glacier, brasseur) étaient **orphelines** (0 lien entrant) ; les 9 autres à in-degree 12.
**✅ Action réalisée :** ajout des 3 liens au méga-menu des **13 pages** → in-degree **12** pour chaque nouvelle page. Plus aucune orpheline.

## 2. Cannibalisation (24 requêtes captées par ≥2 pages)
**Constats :**
- **Cannibalisation générique** : des requêtes comme « erp gestion recettes multi-sites », « logiciel préparation produits finis GMS », « erp approvisionnement restauration collective » sont captées par **3-4 pages métier à la fois** (positions 34-78). Cause = **contenu quasi-dupliqué** issu du clonage de template → les pages se concurrencent, aucune ne perce.
- **« erp patissier »** capté par **boulanger** (pos 15,4), pas par la page patissier dédiée.
- Le **hub** capte en doublon plusieurs requêtes métier (erp traiteur, logiciel industrie laitière…) — normal mais à surveiller.

**Actions :**
- ✅ Quick win (via maillage) : chaque page reçoit désormais des liens internes (dont boulanger → patissier).
- ⚠️ **À faire (projet contenu)** : **différencier le corps** des pages clonées (sections + FAQ réellement spécifiques par métier) pour lever la cannibalisation générique. Le clonage donne le bon design mais un contenu trop proche.
- Positionnement : garder le **hub** comme cible des requêtes génériques (« erp agroalimentaire »), les pages métier pour les requêtes métier.

## 3. CRO
**Constats :**
- ✅ CTAs présents (« Demander une démo », « Ventes & Devis ») + **22 signaux de réassurance**.
- ⚠️ **CTA above-the-fold faible** : le hero propose « Découvrir l'ERP… » ; le vrai CTA « Demander une démo » n'apparaît qu'à ~42 % de la page.
- ⚠️ **Pas de formulaire on-page** (conversion via modale / page contact).

**Actions recommandées (à valider avant application prod) :**
- Renforcer le **CTA hero** : « Demander une démo » visible dès le premier écran.
- Ajouter un **mini-formulaire** ou un lien démo direct au-dessus de la ligne de flottaison.
- A/B tester l'accroche hero (bénéfice chiffré vs générique).

## Priorités
1. ✅ Maillage (fait).
2. Différenciation contenu des pages métier (anti-cannibalisation) — page par page.
3. CRO hero (CTA démo above-the-fold) — sur validation.
