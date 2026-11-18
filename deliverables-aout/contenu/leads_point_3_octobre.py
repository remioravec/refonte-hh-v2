#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Point hebdomadaire du 03/10/2026 — ce qui se règle dans l'extrait « HH Contact
Form - REST Endpoint » (snippet 6).

Trois demandes du compte rendu touchent ce fichier :

  1. « Retirer Maxence de la liste de diffusion et ajouter Nicolas. »
     $to passe de maxence@helloharel.com à l'adresse de Nicolas. Les deux
     adresses en copie — Rémi et Timothy — ne bougent pas : si l'adresse de
     Nicolas est la mauvaise, aucune demande n'est perdue pour autant.

  2. « Ajouter un bouton voir le lead dans le corps des notifications. »
     Le lien est construit depuis la constante HH_CRM_LEAD_URL. Tant qu'elle
     est vide, AUCUNE ligne n'est ajoutée au mail : on ne met pas un lien mort
     dans une notification. Le jour où le format d'URL du CRM est connu, une
     seule ligne à renseigner.

  3. « Mettre en place un e-mail de confirmation automatique pour chaque
     demande de démonstration. »
     Il est écrit, et il est DÉSACTIVÉ (HH_ACCUSE_RECEPTION = false). Raison :
     le domaine expéditeur n'a ni SPF, ni DKIM, ni DMARC, et helloharel.com
     publie deux SPF en conflit, ce qui les invalide tous les deux. Envoyer
     d'un coup des accusés de réception à des adresses externes depuis ce
     domaine, c'est partir en spam et abîmer la réputation qui fait aujourd'hui
     arriver les notifications de leads. On l'allume après les enregistrements
     DNS, en passant la constante à true.

GARDE-FOU DE FOND : l'accusé de réception est envoyé APRÈS la notification et
son échec est ignoré. Une demande ne peut pas être perdue parce que le mail de
courtoisie n'est pas parti.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

SNIPPET = 6
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-snippet6.php')
NICOLAS = os.environ.get('HH_NICOLAS', 'ndecerner@gmail.com')

VIEUX_TO = "    $to       = 'maxence@helloharel.com';"
NEUF_TO = """    /* Point du 03/10/2026 : Maxence sort de la diffusion, Nicolas la reçoit.
       Rémi et Timothy restent en copie ci-dessous : si cette adresse est la
       mauvaise, la demande arrive quand même. */
    $to       = '""" + NICOLAS + "';"

ANCRE_LIEN = """        '- - - - - - -',
        'Cordialement,',
        'Formulaire helloharel.com',
    ];"""
NEUF_LIEN = """        '- - - - - - -',
        'Cordialement,',
        'Formulaire helloharel.com',
    ];

    /* Bouton « voir le lead ». Tant que l'URL du CRM n'est pas renseignée,
       on n'ajoute rien : un lien mort dans une notification est pire que pas
       de lien. Renseigner HH_CRM_LEAD_URL avec %s à la place de l'identifiant,
       par exemple https://crm.example.com/leads/%s */
    if ( defined( 'HH_CRM_LEAD_URL' ) && HH_CRM_LEAD_URL ) {
        $ref = isset( $params['lead_id'] ) ? sanitize_text_field( $params['lead_id'] ) : '';
        $url = $ref ? sprintf( HH_CRM_LEAD_URL, rawurlencode( $ref ) ) : HH_CRM_LEAD_URL;
        array_splice( $body_lines, -3, 0, array( 'Voir le lead dans le CRM : ' . $url, '' ) );
    }"""

ANCRE_FIN = """    if ( ! $sent ) {
        return new WP_REST_Response( [ 'success' => false, 'message' => 'Envoi echoue cote serveur' ], 500 );
    }

    return new WP_REST_Response( [ 'success' => true, 'message' => 'Mail envoye' ], 200 );
}"""
NEUF_FIN = """    if ( ! $sent ) {
        return new WP_REST_Response( [ 'success' => false, 'message' => 'Envoi echoue cote serveur' ], 500 );
    }

    /* Accusé de réception au demandeur. Point du 03/10/2026.
       DÉSACTIVÉ tant que le domaine expéditeur n'a pas SPF, DKIM et DMARC, et
       tant que helloharel.com publie deux SPF en conflit : sans eux, ces mails
       partent en spam et dégradent la réputation qui fait arriver la
       notification ci-dessus. Passer la constante à true une fois le DNS en
       place. L'échec est volontairement ignoré : il ne doit jamais empêcher
       une demande d'être prise en compte. */
    if ( defined( 'HH_ACCUSE_RECEPTION' ) && HH_ACCUSE_RECEPTION ) {
        $ar_sujet = 'Votre demande de démonstration — Hello Harel';
        $ar_corps = implode( "\\n", array(
            'Bonjour ' . $name . ',',
            '',
            'Nous avons bien reçu votre demande de démonstration pour ' . $company . '.',
            'Un membre de l\\'équipe vous rappelle pour convenir d\\'un créneau.',
            '',
            'Si vous souhaitez ajouter une précision, répondez simplement à ce message.',
            '',
            'Bien à vous,',
            'L\\'équipe Hello Harel',
            'https://www.helloharel.com/',
        ) );
        $ar_entetes = array(
            'From: Hello Harel <' . $from_email . '>',
            'Reply-To: ' . $to,
            'Content-Type: text/plain; charset=UTF-8',
        );
        @wp_mail( $email, $ar_sujet, $ar_corps, $ar_entetes );
    }

    return new WP_REST_Response( [ 'success' => true, 'message' => 'Mail envoye' ], 200 );
}"""


def main(ecrire=False):
    c = n.call(f'code-snippets/v1/snippets/{SNIPPET}')['code']
    open(SAUVE, 'w').write(c)
    print(f'sauvegarde : {SAUVE} ({len(c)} o)')

    for ancre in (VIEUX_TO, ANCRE_LIEN, ANCRE_FIN):
        if c.count(ancre) != 1:
            raise RuntimeError('ancre absente ou en double :\n' + ancre[:80])

    c2 = c.replace(VIEUX_TO, NEUF_TO)
    c2 = c2.replace(ANCRE_LIEN, NEUF_LIEN)
    c2 = c2.replace(ANCRE_FIN, NEUF_FIN)

    assert 'maxence@helloharel.com' not in c2, 'Maxence est encore destinataire'
    assert NICOLAS in c2
    assert c2.count("administration@remi-oravec.fr") == c.count("administration@remi-oravec.fr")
    assert c2.count("timothy.jollivet@harelsystems.com") == c.count("timothy.jollivet@harelsystems.com")
    assert c2.count('wp_mail(') == c.count('wp_mail(') + 1
    assert c2.count('{') == c2.count('}'), 'accolades déséquilibrées'
    print(f'après       : {len(c2)} o  (+{len(c2) - len(c)})')
    print(f'destinataire : {NICOLAS}')
    print('copies       : administration@remi-oravec.fr, timothy.jollivet@harelsystems.com')
    print('bouton lead  : actif seulement si HH_CRM_LEAD_URL est définie')
    print('accusé récep.: écrit, DÉSACTIVÉ (HH_ACCUSE_RECEPTION)')

    if ecrire:
        r = n.call(f'code-snippets/v1/snippets/{SNIPPET}', 'POST', {'code': c2})
        print('\nerreur PHP :', r.get('code_error'), '| actif :', r.get('active'))


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
