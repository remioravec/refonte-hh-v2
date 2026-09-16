<?php
/**
 * ANTI-SPAM FORMULAIRES — a coller dans un NOUVEL extrait Code Snippets.
 * Nom suggere : « Anti-spam formulaires (Claude) »   ·   Portee : global
 *
 * POURQUOI CET EXTRAIT EST NECESSAIRE
 * ===================================
 * Mesure du 16/09/2026. Le site a deux points d'entree :
 *   · hh/v1/contact ... envoie le mail ;
 *   · hh/v1/lead ..... enregistre la demande, appele par un script du pied de
 *     page, donc SEULEMENT quand un vrai navigateur execute le JavaScript.
 * Le magasin de demandes compte 71 entrees et pas une en cyrillique, alors que
 * la boite mail deborde d'envois en russe. Les deux ne peuvent etre vrais que
 * si ces envois n'executent jamais le JavaScript du site : ils postent
 * directement sur /wp-json/hh/v1/contact.
 *
 * Un pot a miel ne piege que ce qui LIT le formulaire. Contre un robot qui
 * poste en direct, le champ n'existe pas dans sa requete, donc il est vide,
 * donc il passe. Les pots a miel poses dans les pages arretent les robots qui
 * remplissent la page. Celui-la se corrige ici, cote serveur.
 *
 * LE TROU PRINCIPAL — dans l'extrait « HH Contact Form - REST Endpoint » :
 *     if ( $origin && strpos( $origin, 'helloharel.com' ) === false ) { 403 }
 * Si le robot n'envoie AUCUN en-tete Origin, $origin est vide, la condition
 * est fausse, et la requete passe. C'est exactement ce que fait un script.
 *
 * CE QUE FAIT CET EXTRAIT — il s'intercale AVANT la route, en quatre gardes :
 *   1. pots a miel : website, url, email_confirm, _honey ;
 *   2. provenance : refus seulement si NI Origin NI Referer ne portent le
 *      domaine. Un navigateur envoie toujours Origin sur un POST ;
 *   3. garde temporelle, uniquement si le jeton loaded_at est present ;
 *   4. alphabet cyrillique dans les champs libres.
 *
 * CE QU'IL NE FAIT PAS — il ne modifie PAS l'extrait existant. Il est additif.
 * Le desactiver rend exactement le comportement d'aujourd'hui, en une seconde.
 *
 * RIEN N'EST PERDU — une demande ecartee n'est pas jetee : elle est rangee en
 * brouillon dans Demandes, titre « [SPAM] », avec son motif, son IP et son
 * navigateur. Si une vraie demande tombait a tort, elle est la, visible.
 * Le robot, lui, recoit un faux succes : il ne doit pas apprendre ce qui l'a
 * fait tomber, sinon il s'adapte.
 */

add_filter( 'rest_pre_dispatch', function ( $result, $server, $request ) {

    if ( null !== $result ) { return $result; }
    if ( '/hh/v1/contact' !== $request->get_route() ) { return $result; }

    $p = $request->get_json_params();
    if ( ! is_array( $p ) ) { $p = $request->get_params(); }
    if ( ! is_array( $p ) ) { return $result; }

    $motif = '';

    /* 1 — pots a miel ----------------------------------------------------- */
    foreach ( array( 'website', 'url', 'email_confirm', '_honey' ) as $k ) {
        if ( ! empty( $p[ $k ] ) ) { $motif = 'pot a miel rempli : ' . $k; break; }
    }

    /* 2 — provenance ------------------------------------------------------ */
    if ( ! $motif ) {
        $o = (string) $request->get_header( 'origin' );
        $r = (string) $request->get_header( 'referer' );
        $ok_o = ( '' !== $o && false !== strpos( $o, 'helloharel.com' ) );
        $ok_r = ( '' !== $r && false !== strpos( $r, 'helloharel.com' ) );
        if ( ! $ok_o && ! $ok_r ) { $motif = 'ni Origin ni Referer du domaine'; }
    }

    /* 3 — garde temporelle, seulement si le jeton existe ------------------- */
    if ( ! $motif && ! empty( $p['loaded_at'] ) ) {
        $t = (int) $p['loaded_at'];
        if ( $t > 0 && ( round( microtime( true ) * 1000 ) - $t ) < 2000 ) {
            $motif = 'envoye en moins de deux secondes';
        }
    }

    /* 4 — alphabet cyrillique --------------------------------------------- */
    if ( ! $motif ) {
        $texte = '';
        foreach ( array( 'name', 'Nom', 'company', 'Entreprise', 'message', 'Message', 'secteur' ) as $k ) {
            if ( isset( $p[ $k ] ) && is_string( $p[ $k ] ) ) { $texte .= ' ' . $p[ $k ]; }
        }
        if ( '' !== $texte && preg_match( '/\p{Cyrillic}/u', $texte ) ) {
            $motif = 'texte en cyrillique';
        }
    }

    if ( ! $motif ) { return $result; }   // rien a signaler : la route s'execute

    hh_ranger_spam( $p, $motif );

    return new WP_REST_Response( array( 'success' => true, 'message' => 'OK' ), 200 );

}, 10, 3 );


/**
 * Range la demande ecartee en brouillon, pour que rien ne se perde.
 * Best-effort : une erreur ici ne doit jamais remonter.
 */
function hh_ranger_spam( $p, $motif ) {
    try {
        $nom = '';
        foreach ( array( 'name', 'Nom' ) as $k ) {
            if ( ! empty( $p[ $k ] ) && is_string( $p[ $k ] ) ) { $nom = $p[ $k ]; break; }
        }
        $id = wp_insert_post( array(
            'post_type'   => 'hh_lead',
            'post_status' => 'draft',
            'post_title'  => '[SPAM] ' . mb_substr( $nom ? $nom : 'sans nom', 0, 60 )
                             . ' - ' . date_i18n( 'd/m/Y H:i' ),
        ), true );
        if ( ! is_wp_error( $id ) && $id ) {
            update_post_meta( $id, '_hh_spam',  sanitize_text_field( $motif ) );
            update_post_meta( $id, '_hh_email', isset( $p['email'] ) ? sanitize_email( $p['email'] ) : '' );
            update_post_meta( $id, '_hh_name',  sanitize_text_field( $nom ) );
            update_post_meta( $id, '_hh_ip',    isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( $_SERVER['REMOTE_ADDR'] ) : '' );
            update_post_meta( $id, '_hh_ua',    isset( $_SERVER['HTTP_USER_AGENT'] ) ? sanitize_text_field( $_SERVER['HTTP_USER_AGENT'] ) : '' );
            update_post_meta( $id, '_hh_all',   wp_json_encode( $p ) );
        }
    } catch ( \Throwable $e ) { /* silencieux : ne jamais bloquer */ }
}


/* Le motif du rejet, visible dans la liste Demandes. */
add_filter( 'manage_hh_lead_posts_columns', function ( $c ) {
    $c['hh_spam'] = 'Ecarte';
    return $c;
}, 20 );
add_action( 'manage_hh_lead_posts_custom_column', function ( $col, $id ) {
    if ( 'hh_spam' === $col ) {
        $m = get_post_meta( $id, '_hh_spam', true );
        echo $m ? '<span style="color:#b3261e;font-weight:600">' . esc_html( $m ) . '</span>' : '-';
    }
}, 20, 2 );
