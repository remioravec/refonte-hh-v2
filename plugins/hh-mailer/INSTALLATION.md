# hh-mailer — ce qui a change, et les deux gestes qui restent

## Le constat

Le formulaire de contact **atteint bien le serveur** : les demandes sont
enregistrees dans WordPress (menu « Demandes »). Trois vraies demandes y
figurent depuis le 15 septembre. **Aucune n'a ete envoyee par mail a
personne.** Le formulaire ne perd pas les prospects ; il ne previent
personne qu'ils sont arrives.

Trois causes, distinctes, toutes a traiter.

### 1. Deux extensions d'envoi actives en meme temps

`hh-mailer` et `wp-mail-smtp` s'accrochent toutes les deux a l'evenement
`phpmailer_init`. Les extensions se chargent par ordre alphabetique :
`wp-mail-smtp` passe **apres** `hh-mailer` et ecrasait silencieusement
l'hote, l'identifiant et l'expediteur poses par celui-ci.

Corrige dans cette version : `hh-mailer` s'accroche desormais en
priorite maximale et repasse en dernier. Mais deux expediteurs actifs
restent une mauvaise idee — voir le geste 2.

### 2. L'extension etait peut-etre inerte, sans le dire

Sans identifiant ni mot de passe, `hh-mailer` ne prend pas la main : le
site retombe sur sa configuration d'origine. C'est voulu — mieux vaut ne
rien casser. Mais elle le faisait **en silence**, et rien ne distinguait
« active et aux commandes » de « active et inerte ».

Corrige : elle l'ecrit maintenant dans son journal, et une route de
lecture permet de le verifier de l'exterieur :

    GET /wp-json/hh-mailer/v1/etat      (administrateur connecte)

Elle rend l'identifiant, d'ou vient le mot de passe, si l'extension
prend la main, quelles autres extensions d'envoi sont actives, et les
quinze dernieres lignes du journal. **Elle ne rend jamais le mot de
passe.**

### 3. Le domaine porte DEUX enregistrements SPF

Releve le 23/09/2026 sur les resolveurs de Google et de Cloudflare :

    v=spf1 include:_mailcust.gandi.net ?all
    v=spf1 include:_mailcust.gandi.net include:_spf.google.com ?all

La norme (RFC 7208, section 4.5) est explicite : un domaine qui publie
plus d'un enregistrement SPF provoque une erreur permanente. Les
receveurs ne choisissent pas le bon — ils abandonnent la verification.
Il n'y a ni DKIM (`google._domainkey` absent) ni DMARC.

Ce point-la ne se corrige pas dans WordPress.

## Les deux gestes qui restent

### Geste 1 — installer cette version et verifier l'etat

1. Zipper le dossier `hh-mailer/`, puis Extensions → Ajouter →
   Televerser. WordPress remplace la version en place.
2. Ouvrir `https://www.helloharel.com/wp-json/hh-mailer/v1/etat` en etant
   connecte en administrateur.
3. Lire `mot_de_passe` et `prend_la_main`.

   * `mot_de_passe: ABSENT` → l'extension n'a jamais rien envoye. Poser
     le mot de passe d'application, de preference dans `wp-config.php`,
     au-dessus de la ligne `/* That's all, stop editing! */` :

         define('HH_SMTP_USER', 'l-adresse-du-compte@helloharel.com');
         define('HH_SMTP_PASS', 'le-mot-de-passe-d-application');

     Dans `wp-config.php` il reste hors de la base et hors des
     sauvegardes SQL. Le champ de reglage marche aussi, mais il stocke
     le secret en base.

   * `concurrents` non vide → desactiver `wp-mail-smtp`. Deux
     expediteurs, c'est le dernier charge qui gagne, et ce n'est pas
     forcement celui qu'on croit.

4. Reglages → Hello Harel Mailer → « Envoyer un test ». Le journal dit
   `ok` ou donne l'erreur SMTP exacte.

### Geste 2 — le DNS, chez Gandi

1. **Supprimer l'un des deux SPF.** Garder celui-ci, qui couvre Gandi et
   Google :

         v=spf1 include:_mailcust.gandi.net include:_spf.google.com ?all

   Tant qu'il y en a deux, le reste ne sert a rien.

2. **DKIM** : dans la console Google Workspace, Applications → Gmail →
   Authentifier les e-mails → generer la cle, puis publier
   `google._domainkey` chez Gandi.

3. **DMARC**, une fois les deux premiers en place et verifies :

         _dmarc  TXT  "v=DMARC1; p=none; rua=mailto:postmaster@helloharel.com"

   `p=none` observe sans rien rejeter. On durcit plus tard, au vu des
   rapports.

## Un point a trancher

Le formulaire envoie a `maxence@helloharel.com`, avec
`administration@remi-oravec.fr` et `timothy.jollivet@harelsystems.com`
en copie. Il se presente comme `no-reply@helloharel.com`.

Si cette adresse n'est pas un alias autorise du compte qui
s'authentifie, Google refuse l'envoi — et `wp_mail()` rend `false`, ce
qui fait repondre **500** au formulaire : le visiteur voit une erreur
alors que sa demande est bien enregistree.

`hh-mailer` corrige deja cela quand elle a la main : elle repose
l'expediteur sur le compte authentifie. C'est une raison de plus pour
qu'elle soit la seule aux commandes.
