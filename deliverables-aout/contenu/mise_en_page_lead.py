#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mise en page de la notification de lead, et lien vers le tableau de bord.

CE QUI EXISTE DÉJÀ, et qu'il faut avoir en tête :
  - /hh/v1/contact  reçoit le formulaire et envoie le mail ;
  - /hh/v1/lead     est appelé en parallèle par sendBeacon et crée un post
                    « hh_lead » avec ses métadonnées ;
  - l'écran « Demandes » de wp-admin liste ces posts avec e-mail, société,
    page du premier clic et page du formulaire. C'EST le tableau de bord.

Les deux routes sont découplées exprès : au moment où le mail part, le post
peut ne pas encore exister. Le bouton ne peut donc pas pointer vers un
identifiant. Il pointe vers la liste « Demandes » filtrée sur le nom du
demandeur — le titre du post est « Nom - date », donc la recherche le trouve
dès qu'il arrive, même quelques secondes plus tard. Un lien qui marche
toujours vaut mieux qu'un lien exact qui marche une fois sur deux.

Si HH_CRM_LEAD_URL est définie un jour (CRM externe), c'est elle qui prime.

MODE TEST. HH_LEADS_TEST à true envoie tout, et uniquement, à Rémi : pas de
destinataire métier, pas de copie. C'est l'état livré pour la relecture de la
mise en page. Repasser la constante à false rend la diffusion décidée au point
du 03/10 : Nicolas destinataire, Rémi et Timothy en copie.

Le mail part en HTML avec une version texte en repli, posée sur AltBody : un
mail sans partie texte est pénalisé par les filtres, et la délivrabilité est
déjà le point faible du domaine.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

SNIPPET = 6
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-miseenpage.php')

DEBUT = "    // ===== Composition du mail ====="
FIN = "    return new WP_REST_Response( [ 'success' => true, 'message' => 'Mail envoye' ], 200 );\n}"

NOUVEAU = r"""    // ===== Composition du mail =====

    /* Mode test : tout part chez Rémi, et seulement chez lui. Repasser à false
       pour la diffusion décidée au point du 03/10/2026. */
    if ( ! defined( 'HH_LEADS_TEST' ) ) { define( 'HH_LEADS_TEST', true ); }

    if ( HH_LEADS_TEST ) {
        $to       = 'administration@remi-oravec.fr';
        $cc_addrs = array();
    } else {
        /* Maxence sort de la diffusion, Nicolas la reçoit. Rémi et Timothy
           restent en copie : si l'adresse de Nicolas est la mauvaise, la
           demande arrive quand même. */
        $to       = 'ndecerner@gmail.com';
        $cc_addrs = array(
            'administration@remi-oravec.fr',
            'timothy.jollivet@harelsystems.com',
        );
    }

    $subject = sprintf(
        'Demande de demo - %s%s',
        $company ? $company : $name,
        $secteur ? ' (' . $secteur . ')' : ''
    );

    $te_source   = isset( $params['te_source'] )   ? sanitize_text_field( $params['te_source'] )   : '';
    $te_medium   = isset( $params['te_medium'] )   ? sanitize_text_field( $params['te_medium'] )   : '';
    $te_campaign = isset( $params['te_campaign'] ) ? sanitize_text_field( $params['te_campaign'] ) : '';
    $te_landing  = isset( $params['te_landing'] )  ? esc_url_raw( $params['te_landing'] )           : '';
    $form_page   = isset( $params['form_page'] )   ? esc_url_raw( $params['form_page'] )            : '';

    /* Le bouton du tableau de bord. La liste « Demandes » filtrée sur le nom
       retrouve la demande dès que /hh/v1/lead l'a enregistrée, même après
       l'envoi du mail. Un CRM externe, s'il est déclaré, prend le dessus. */
    if ( defined( 'HH_CRM_LEAD_URL' ) && HH_CRM_LEAD_URL ) {
        $lien_lead = HH_CRM_LEAD_URL;
    } else {
        $lien_lead = admin_url( 'edit.php?post_type=hh_lead&s=' . rawurlencode( $name ) );
    }
    $lien_liste = admin_url( 'edit.php?post_type=hh_lead' );

    /* ---- version texte, pour le repli et les filtres anti-spam ---- */
    $body_lines = array(
        'Nouvelle demande de demonstration depuis helloharel.com',
        '',
        'Societe : ' . $company,
        'Nom : ' . $name,
        'Email : ' . $email,
        'Telephone : ' . ( $phone ? $phone : '(non renseigne)' ),
        'Secteur : ' . ( $secteur ? $secteur : '(non precise)' ),
        '',
        'Message :',
        ( $message ? $message : '(aucun)' ),
        '',
        'Voir la demande : ' . $lien_lead,
        '',
        '- - - - - - -',
        'Attribution',
        '  source : ' . ( $te_source ? $te_source : 'n/a' ),
        '  medium : ' . ( $te_medium ? $te_medium : 'n/a' ),
        '  campagne : ' . ( $te_campaign ? $te_campaign : 'n/a' ),
        '  page d-arrivee : ' . ( $te_landing ? $te_landing : 'n/a' ),
        '  page du formulaire : ' . ( $form_page ? $form_page : 'n/a' ),
        '  IP : ' . ( $ip ? $ip : 'n/a' ),
    );
    $body_texte = implode( "\n", $body_lines );

    /* ---- version HTML ---- */
    $ligne = function ( $libelle, $valeur, $lien = '' ) {
        if ( $valeur === '' || $valeur === null ) { $valeur = '—'; }
        $v = $lien
            ? '<a href="' . esc_url( $lien ) . '" style="color:#0369A1;text-decoration:none">' . esc_html( $valeur ) . '</a>'
            : esc_html( $valeur );
        return '<tr>'
            . '<td style="padding:10px 16px;border-bottom:1px solid #E2E8F0;color:#64748B;'
            . 'font:400 13px/1.4 Arial,Helvetica,sans-serif;white-space:nowrap;vertical-align:top">'
            . esc_html( $libelle ) . '</td>'
            . '<td style="padding:10px 16px;border-bottom:1px solid #E2E8F0;color:#0F172A;'
            . 'font:700 14px/1.5 Arial,Helvetica,sans-serif">' . $v . '</td>'
            . '</tr>';
    };

    $attribution = array(
        'Source'     => $te_source,
        'Support'    => $te_medium,
        'Campagne'   => $te_campaign,
        'Page d\'arrivée' => $te_landing,
        'Page du formulaire' => $form_page,
        'IP'         => $ip,
    );
    $attr_html = '';
    foreach ( $attribution as $k => $v ) {
        $attr_html .= '<tr>'
            . '<td style="padding:4px 16px;color:#94A3B8;font:400 12px/1.5 Arial,Helvetica,sans-serif;'
            . 'white-space:nowrap;vertical-align:top">' . esc_html( $k ) . '</td>'
            . '<td style="padding:4px 16px;color:#64748B;font:400 12px/1.5 Arial,Helvetica,sans-serif;'
            . 'word-break:break-all">' . esc_html( $v ? $v : '—' ) . '</td></tr>';
    }

    $body_html =
      '<!doctype html><html lang="fr"><body style="margin:0;padding:0;background:#F1F5F9">'
    . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F1F5F9;padding:24px 12px">'
    . '<tr><td align="center">'
    . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#FFFFFF;border-radius:14px;overflow:hidden;border:1px solid #E2E8F0">'

    . '<tr><td style="background:#0F172A;padding:20px 24px">'
    . '<div style="color:#38BDF8;font:700 11px/1.2 Arial,Helvetica,sans-serif;letter-spacing:.12em;text-transform:uppercase">Nouvelle demande de démo</div>'
    . '<div style="color:#FFFFFF;font:700 21px/1.3 Arial,Helvetica,sans-serif;margin-top:6px">' . esc_html( $company ? $company : $name ) . '</div>'
    . ( $secteur ? '<div style="color:#94A3B8;font:400 13px/1.4 Arial,Helvetica,sans-serif;margin-top:4px">' . esc_html( $secteur ) . '</div>' : '' )
    . '</td></tr>'

    . '<tr><td style="padding:20px 24px 4px">'
    . '<a href="' . esc_url( $lien_lead ) . '" style="display:block;background:#0369A1;color:#FFFFFF;'
    . 'font:700 15px/1.2 Arial,Helvetica,sans-serif;text-align:center;text-decoration:none;'
    . 'padding:14px 20px;border-radius:10px">Ouvrir la demande dans le tableau de bord</a>'
    . '<div style="text-align:center;margin-top:8px"><a href="' . esc_url( $lien_liste ) . '" '
    . 'style="color:#64748B;font:400 12px/1.4 Arial,Helvetica,sans-serif">Voir toutes les demandes</a></div>'
    . '</td></tr>'

    . '<tr><td style="padding:12px 8px 0">'
    . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0">'
    . $ligne( 'Nom', $name )
    . $ligne( 'E-mail', $email, 'mailto:' . $email )
    . ( $phone ? $ligne( 'Téléphone', $phone, 'tel:' . preg_replace( '/[^0-9+]/', '', $phone ) ) : $ligne( 'Téléphone', '' ) )
    . $ligne( 'Société', $company )
    . '</table></td></tr>'

    . '<tr><td style="padding:16px 24px 0">'
    . '<div style="color:#64748B;font:400 13px/1.4 Arial,Helvetica,sans-serif;margin-bottom:6px">Message</div>'
    . '<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:14px 16px;'
    . 'color:#0F172A;font:400 14px/1.6 Arial,Helvetica,sans-serif;white-space:pre-wrap">'
    . esc_html( $message ? $message : 'Aucun message.' ) . '</div></td></tr>'

    . '<tr><td style="padding:18px 8px 20px">'
    . '<div style="color:#94A3B8;font:700 11px/1.2 Arial,Helvetica,sans-serif;letter-spacing:.1em;'
    . 'text-transform:uppercase;padding:0 16px 6px">Attribution</div>'
    . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0">' . $attr_html . '</table>'
    . '</td></tr>'

    . '</table>'
    . '<div style="color:#94A3B8;font:400 11px/1.5 Arial,Helvetica,sans-serif;margin-top:14px;text-align:center">'
    . 'Formulaire helloharel.com — répondre à ce message écrit directement au demandeur.</div>'
    . '</td></tr></table></body></html>';

    $from_email = 'no-reply@helloharel.com';
    $headers    = array(
        'From: Hello Harel <' . $from_email . '>',
        'Reply-To: ' . $name . ' <' . $email . '>',
        'Content-Type: text/html; charset=UTF-8',
    );
    foreach ( $cc_addrs as $cc ) {
        $headers[] = 'Cc: ' . $cc;
    }

    /* Partie texte du multipart : un mail HTML sans repli texte est pénalisé
       par les filtres, et la délivrabilité du domaine est déjà fragile. */
    $GLOBALS['hh_alt_body'] = $body_texte;

    $sent = wp_mail( $to, $subject, $body_html, $headers );

    unset( $GLOBALS['hh_alt_body'] );

    if ( ! $sent ) {
        return new WP_REST_Response( [ 'success' => false, 'message' => 'Envoi echoue cote serveur' ], 500 );
    }

    /* Accusé de réception au demandeur. Point du 03/10/2026.
       DÉSACTIVÉ tant que le domaine expéditeur n'a pas SPF, DKIM et DMARC, et
       tant que helloharel.com publie deux SPF en conflit : sans eux, ces mails
       partent en spam et dégradent la réputation qui fait arriver la
       notification ci-dessus. L'échec est volontairement ignoré. */
    if ( defined( 'HH_ACCUSE_RECEPTION' ) && HH_ACCUSE_RECEPTION ) {
        $ar_sujet = 'Votre demande de démonstration — Hello Harel';
        $ar_corps = implode( "\n", array(
            'Bonjour ' . $name . ',',
            '',
            'Nous avons bien reçu votre demande de démonstration pour ' . $company . '.',
            'Un membre de l\'équipe vous rappelle pour convenir d\'un créneau.',
            '',
            'Si vous souhaitez ajouter une précision, répondez simplement à ce message.',
            '',
            'Bien à vous,',
            'L\'équipe Hello Harel',
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
}

/* Pose la partie texte du mail HTML. Sans elle, le message est mono-part HTML,
   ce que les filtres notent mal. */
add_action( 'phpmailer_init', function ( $phpmailer ) {
    if ( ! empty( $GLOBALS['hh_alt_body'] ) && $phpmailer->ContentType === 'text/html' ) {
        $phpmailer->AltBody = $GLOBALS['hh_alt_body'];
    }
} );"""


def main(ecrire=False):
    c = n.call(f'code-snippets/v1/snippets/{SNIPPET}')['code']
    open(SAUVE, 'w').write(c)
    i = c.find(DEBUT)
    j = c.find(FIN)
    if i < 0 or j < 0:
        raise RuntimeError(f'bornes introuvables (debut {i}, fin {j})')
    c2 = c[:i] + NOUVEAU + c[j + len(FIN):]

    assert c2.count('{') == c2.count('}'), 'accolades déséquilibrées'
    assert c2.count('(') == c2.count(')'), 'parenthèses déséquilibrées'
    assert 'maxence@helloharel.com' not in c2
    assert "hh_store_lead" in c2 and "register_post_type('hh_lead'" in c2, 'la partie Demandes a sauté'
    # 3 occurrences : la mention dans le commentaire d'en-tete, l'envoi de la
    # notification, et l'accuse de reception desactive.
    assert c2.count('wp_mail(') == 3, c2.count('wp_mail(')
    assert 'HH_LEADS_TEST' in c2
    print(f'{len(c)} o -> {len(c2)} o')
    print('mode test : destinataire unique administration@remi-oravec.fr')
    print('bouton    : liste Demandes filtrée sur le nom')
    if ecrire:
        r = n.call(f'code-snippets/v1/snippets/{SNIPPET}', 'POST', {'code': c2})
        print('erreur PHP :', r.get('code_error'), '| actif :', r.get('active'))


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
