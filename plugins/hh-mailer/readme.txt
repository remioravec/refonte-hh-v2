=== Hello Harel — Mailer ===
Version: 1.0.0

Envoi SMTP par Google Workspace, mise en page Hello Harel des demandes de
demo, garde-fou anti-doublon et journal des envois.

INSTALLATION
1. Extensions > Ajouter > Televerser une extension > hh-mailer.zip > Installer
2. Activer
3. Reglages > HH Mailer
4. Compte expediteur : administration@remi-oravec.fr
5. Mot de passe d'application : celui genere sur
   https://myaccount.google.com/apppasswords (les espaces sont retires seuls)
6. Enregistrer, puis « Envoyer le test »

PLUS SUR — le mot de passe hors base de donnees
Plutot que le champ de l'ecran, poser dans wp-config.php, avant la ligne
/* That's all, stop editing! */ :

    define( 'HH_SMTP_USER', 'administration@remi-oravec.fr' );
    define( 'HH_SMTP_PASS', 'le-mot-de-passe-sans-espaces' );

Les constantes priment sur l'ecran de reglages. Le secret reste alors hors
de la base et hors des sauvegardes SQL.

CE QUE L'EXTENSION NE TOUCHE PAS
Le snippet du formulaire (hh/v1/contact), l'enregistrement des demandes
(hh/v1/lead) et le script d'attribution restent inchanges. Tout passe par
des filtres WordPress, et chaque intervention est enveloppee : en cas de
pepin, on retombe sur le comportement d'origine plutot que de casser
l'envoi.

CE QU'ELLE CORRIGE
Le formulaire envoyait depuis no-reply@helloharel.com, une adresse que le
site ne peut pas authentifier. Sans SMTP, WordPress tombe sur mail() de
PHP ; le SPF du domaine est en erreur et les destinataires sont sur Google
Workspace, qui refuse. wp_mail() renvoyait false — et l'endpoint repond 500
dans ce cas, si bien que le visiteur voyait une erreur alors que sa demande
etait bien enregistree. Corriger l'envoi repare les deux.

A FAIRE EN PLUS, COTE DNS (independant de l'extension)
- SPF : un seul enregistrement, pas deux. Deux = permerror, et tout echoue.
    v=spf1 include:_mailcust.gandi.net include:_spf.google.com ~all
- DKIM : a activer dans la console Google Workspace, puis publier la cle.
- DMARC : _dmarc en p=none pour commencer, le temps d'observer.
