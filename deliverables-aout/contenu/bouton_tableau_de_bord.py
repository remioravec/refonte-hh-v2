#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correction d'une bêtise de ma part, et pose du bouton « tableau de bord ».

CE QUE J'AVAIS CASSÉ. La mise en page du mail de lead existait déjà, dans le
plugin hh-mailer : mettre_en_page() relit le corps « - Étiquette : valeur » et
le rend avec le gabarit maison (bandeau cyan, tableau des champs, bloc
« D'où vient cette demande », bouton « Répondre à »). Ce gabarit se désactive
tout seul si les en-têtes déclarent déjà text/html — et c'est exactement ce que
ma version précédente faisait. Elle remplaçait donc un gabarit déjà fait, et
mieux fait, par le mien.

CE QUE FAIT CE SCRIPT :
  1. l'extrait 6 reprend le corps en texte, dans la forme que hh-mailer sait
     relire — le gabarit du plugin redevient maître de la mise en page ;
  2. le mode test et l'accusé de réception désactivé sont conservés ;
  3. le bouton « Ouvrir la demande dans le tableau de bord » est injecté DANS
     le gabarit du plugin, par un filtre wp_mail en priorité 100, donc après la
     mise en page (priorité 99). Le plugin n'est pas modifié : il n'y a pas
     d'écriture de fichier possible depuis l'API, et deux gabarits
     concurrents, c'est ce qu'on vient de corriger.

Le lien pointe vers l'écran « Demandes » de wp-admin filtré sur le nom du
demandeur. Les deux routes du formulaire sont découplées : au moment de
l'envoi, la fiche peut ne pas encore exister. Une liste filtrée la retrouve
dès qu'elle arrive ; un lien vers un identifiant pas encore attribué, non.

GARDE-FOU : si l'ancre du gabarit n'est pas trouvée, le filtre ne touche à
rien et le mail part tel quel.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

SNIPPET = 6
ORIGINE = os.environ.get('HH_ORIGINE', '/tmp/t/avant-snippet6.php')
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-bouton.php')

VIEUX_TO = "    $to       = 'maxence@helloharel.com';"
NEUF_TO = """    /* Mode test : tout part chez Rémi, et seulement chez lui. Repasser la
       constante à false pour la diffusion décidée au point du 03/10/2026. */
    if ( ! defined( 'HH_LEADS_TEST' ) ) { define( 'HH_LEADS_TEST', true ); }

    if ( HH_LEADS_TEST ) {
        $to       = 'administration@remi-oravec.fr';
    } else {
        /* Maxence sort de la diffusion, Nicolas la reçoit. Rémi et Timothy
           restent en copie : si l'adresse de Nicolas est la mauvaise, la
           demande arrive quand même. */
        $to       = 'ndecerner@gmail.com';
    }"""

VIEUX_CC = """    $cc_addrs = [
        'administration@remi-oravec.fr',
        'timothy.jollivet@harelsystems.com',
    ];"""
NEUF_CC = """    $cc_addrs = HH_LEADS_TEST ? array() : array(
        'administration@remi-oravec.fr',
        'timothy.jollivet@harelsystems.com',
    );"""

FIN = """    return new WP_REST_Response( [ 'success' => true, 'message' => 'Mail envoye' ], 200 );
}"""

NEUF_FIN = r"""    /* Accusé de réception au demandeur. Point du 03/10/2026.
       DÉSACTIVÉ tant que le domaine expéditeur n'a pas SPF, DKIM et DMARC, et
       tant que helloharel.com publie deux SPF en conflit : sans eux, ces mails
       partent en spam et dégradent la réputation qui fait arriver la
       notification. L'échec est volontairement ignoré : une demande ne peut
       pas être perdue parce que le mail de courtoisie n'est pas parti. */
    if ( defined( 'HH_ACCUSE_RECEPTION' ) && HH_ACCUSE_RECEPTION ) {
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
        @wp_mail( $email, 'Votre demande de démonstration — Hello Harel', $ar_corps, array(
            'From: Hello Harel <' . $from_email . '>',
            'Reply-To: ' . $to,
            'Content-Type: text/plain; charset=UTF-8',
        ) );
    }

    return new WP_REST_Response( [ 'success' => true, 'message' => 'Mail envoye' ], 200 );
}

/**
 * Bouton « tableau de bord » ajouté au gabarit de hh-mailer.
 *
 * Priorité 100 : hh-mailer met en page en 99, on intervient juste après, sur
 * son HTML. Le plugin n'est pas touché — un seul gabarit, un seul endroit où
 * la mise en page se décide.
 *
 * L'ancre est le bloc du bouton « Répondre à » ; le nôtre se place juste
 * avant. Ancre absente, on ne touche à rien.
 */
add_filter( 'wp_mail', function ( $atts ) {
    try {
        $sujet = isset( $atts['subject'] ) ? (string) $atts['subject'] : '';
        if ( false === stripos( $sujet, 'demande de demo' ) ) { return $atts; }
        $html = isset( $atts['message'] ) ? (string) $atts['message'] : '';
        $ancre = '<div style="margin:26px 0 0;">';
        if ( false === strpos( $html, $ancre ) ) { return $atts; }

        /* Le nom du demandeur, relu dans le titre du gabarit. */
        $nom = '';
        if ( preg_match( '/Répondre à ([^<]+)</u', $html, $m ) ) {
            $nom = trim( html_entity_decode( $m[1], ENT_QUOTES, 'UTF-8' ) );
        }
        $lien = ( defined( 'HH_CRM_LEAD_URL' ) && HH_CRM_LEAD_URL )
            ? HH_CRM_LEAD_URL
            : admin_url( 'edit.php?post_type=hh_lead' . ( $nom ? '&s=' . rawurlencode( $nom ) : '' ) );

        $bouton = '<div style="margin:24px 0 0;">'
            . '<a href="' . esc_url( $lien ) . '" style="display:inline-block;background:#0f172a;'
            . 'color:#ffffff;text-decoration:none;font-weight:700;font-size:15px;'
            . 'padding:13px 26px;border-radius:999px;">Ouvrir la demande dans le tableau de bord</a>'
            . '</div>';

        $atts['message'] = substr_replace( $html, $bouton, strpos( $html, $ancre ), 0 );
    } catch ( \Throwable $e ) { /* jamais bloquer un envoi */ }
    return $atts;
}, 100 );"""


def main(ecrire=False):
    vivant = n.call(f'code-snippets/v1/snippets/{SNIPPET}')['code']
    open(SAUVE, 'w').write(vivant)
    c = open(ORIGINE, encoding='utf-8').read()
    print(f'repart de la version d\'origine : {len(c)} o '
          f'(la version en ligne, {len(vivant)} o, est sauvegardée)')

    for a in (VIEUX_TO, VIEUX_CC, FIN):
        if c.count(a) != 1:
            raise RuntimeError('ancre absente ou en double : ' + a[:60])

    c2 = c.replace(VIEUX_TO, NEUF_TO).replace(VIEUX_CC, NEUF_CC).replace(FIN, NEUF_FIN)

    assert 'maxence@helloharel.com' not in c2
    assert 'text/html' not in c2.split('add_filter( \'wp_mail\'')[0], \
        "l'envoi ne doit plus declarer text/html, sinon le gabarit du plugin se desactive"
    assert "'- Nom : ' . $name" in c2, 'le corps texte attendu par hh-mailer a disparu'
    assert c2.count('{') == c2.count('}')
    assert c2.count('(') == c2.count(')')
    assert "register_post_type('hh_lead'" in c2
    print(f'nouveau : {len(c2)} o')
    print('corps   : texte, relu et mis en page par hh-mailer')
    print('bouton  : injecté dans le gabarit du plugin, filtre wp_mail prio 100')
    print('mode    : HH_LEADS_TEST = true -> administration@remi-oravec.fr seul')
    if ecrire:
        r = n.call(f'code-snippets/v1/snippets/{SNIPPET}', 'POST', {'code': c2})
        print('erreur PHP :', r.get('code_error'), '| actif :', r.get('active'))


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
