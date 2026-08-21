<?php
/**
 * Hello Harel — noindex sur les pages de test A/B
 *
 * A coller dans Code Snippets, execution « Partout », puis activer.
 *
 * POURQUOI : une page de test A/B ne doit jamais entrer dans l'index. Tant que
 * la page reste en brouillon elle est inaccessible au public, donc non indexable.
 * Des qu'elle est PUBLIEE pour servir le test, il faut un noindex explicite.
 *
 * Rank Math genere la balise robots : on la surcharge par son filtre officiel,
 * et on ajoute une sortie de secours si Rank Math est desactive.
 * On envoie aussi l'en-tete HTTP X-Robots-Tag, respecte meme si le HTML est mis
 * en cache par LiteSpeed.
 */

/** Les IDs des pages de test. Ajouter les nouvelles variantes ici. */
function hh_ab_test_page_ids() {
    return array(
        11493, // [TEST A] ERP Import Export — variante SXO de /negoce/
    );
}

function hh_is_ab_test_page() {
    if ( is_admin() ) {
        return false;
    }
    $id = get_queried_object_id();
    return $id && in_array( (int) $id, hh_ab_test_page_ids(), true );
}

/* 1 · Rank Math — surcharge de la directive robots */
add_filter( 'rank_math/frontend/robots', function ( $robots ) {
    if ( hh_is_ab_test_page() ) {
        return array( 'index' => 'noindex', 'follow' => 'nofollow' );
    }
    return $robots;
} );

/* 2 · Filet de securite si Rank Math n'emet rien */
add_action( 'wp_head', function () {
    if ( hh_is_ab_test_page() && ! class_exists( 'RankMath' ) ) {
        echo '<meta name="robots" content="noindex, nofollow" />' . "\n";
    }
}, 1 );

/* 3 · En-tete HTTP — resiste au cache HTML */
add_action( 'template_redirect', function () {
    if ( hh_is_ab_test_page() ) {
        header( 'X-Robots-Tag: noindex, nofollow', true );
    }
} );

/* 4 · Hors sitemap Rank Math */
add_filter( 'rank_math/sitemap/exclude_post_ids', function ( $ids ) {
    $exclude = hh_ab_test_page_ids();
    if ( is_string( $ids ) ) {
        $ids = array_filter( array_map( 'trim', explode( ',', $ids ) ) );
    }
    if ( ! is_array( $ids ) ) {
        $ids = array();
    }
    return implode( ',', array_unique( array_merge( $ids, $exclude ) ) );
} );
