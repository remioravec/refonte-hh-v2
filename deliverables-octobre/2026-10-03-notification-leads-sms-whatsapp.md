# Notifier les nouveaux leads par SMS ou WhatsApp — faisabilité et coût

Demande du point hebdomadaire du 03/10/2026 : « Vérifier la faisabilité
technique et le coût d'une automatisation pour envoyer les nouveaux leads par
SMS ou WhatsApp. » Prix relevés le 03/10/2026.

## Le volume dont on parle

24 leads en septembre, soit **moins d'un par jour**. Les destinataires sont
Nicolas et Timothy, pas les prospects. C'est ce qui décide : on alerte deux
personnes de l'équipe, on ne fait pas de la diffusion.

## SMS

| | Twilio | Brevo |
|---|---|---|
| Prix par SMS vers la France | **0,0798 $** | **≈ 0,049 €** |
| Numéro expéditeur | à partir de 1,15 $/mois | compris |
| Paiement | à l'usage | crédits prépayés, sans expiration |

Pour 24 leads et deux destinataires : **environ 2 à 4 € par mois**, numéro
compris. Le coût n'est pas un sujet.

Côté technique, c'est une requête HTTP de plus dans l'extrait qui traite déjà
le formulaire, juste après l'envoi du mail, en « best effort » — son échec ne
doit jamais empêcher la prise en compte d'une demande, comme pour l'accusé de
réception. Une demi-journée avec les tests.

## WhatsApp

La WhatsApp Business Platform facture **au message délivré**, par catégorie :
marketing, utilitaire, authentification, service. Les messages de **service**
ne sont pas facturés, et tout ce qui part dans les 24 h suivant un message
entrant de l'utilisateur ne l'est pas non plus.

Le prix n'est donc pas le problème. Ce qui coûte, c'est l'entrée :

- un compte Meta Business **vérifié** (pièces justificatives de l'entreprise) ;
- un numéro dédié, qui ne peut plus servir dans l'application WhatsApp normale ;
- chaque message sortant hors fenêtre de 24 h passe par un **modèle validé par
  Meta** — on ne peut pas envoyer un texte libre ;
- soit un fournisseur intermédiaire (Twilio, 360dialog, Brevo), soit
  l'intégration directe de l'API Cloud.

Pour prévenir deux personnes de l'équipe moins d'une fois par jour, c'est
disproportionné.

## Ce que je recommande

**SMS, chez Brevo** : facturé en euros, crédits sans expiration, et le compte
peut servir aussi au transactionnel si le sujet revient. Twilio est plus cher
au message et facture le numéro, pour un gain nul à ce volume.

**WhatsApp, seulement si** l'équipe veut à terme répondre aux prospects dans
WhatsApp — là, la vérification Meta se justifie par l'usage commercial, pas
par l'alerte interne.

## Avant d'allumer quoi que ce soit

Le domaine expéditeur n'a ni SPF, ni DKIM, ni DMARC, et helloharel.com publie
**deux SPF en conflit**, ce qui les invalide tous les deux. Ça ne touche pas le
SMS, mais ça touche l'accusé de réception automatique demandé au même point :
il est écrit et **désactivé** tant que le DNS n'est pas en ordre.

## Sources

- [Twilio — tarifs SMS France](https://www.twilio.com/en-us/sms/pricing/fr)
- [WhatsApp Business Platform — tarification](https://whatsappbusiness.com/products/platform-pricing/)
- [Brevo — pays et tarifs SMS](https://help.brevo.com/hc/en-us/articles/208717449-Supported-countries-and-pricing-for-SMS-messages)
