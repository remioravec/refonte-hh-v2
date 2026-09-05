<?php
/**
 * Hello Harel — title & meta description de /blog/calculer-le-prix-de-revient-en-boulangerie/
 *
 * POURQUOI : Rank Math stocke son title dans une meta qui n'est pas exposee par
 * l'API REST. Le post_title a bien ete change, mais Rank Math l'ecrase au rendu.
 * Deux options : saisir les valeurs a la main dans l'onglet Rank Math du post
 * (le plus simple), OU coller ce snippet dans Code Snippets.
 *
 * DIAGNOSTIC : la page est en position absolue 3 sur « logiciel prix de revient »
 * avec 568 impressions et 0 clic. Son title promet un guide d'exercices de
 * boulangerie dans une SERP ou 6 resultats sur 8 sont des pages de logiciel.
 */

define( 'HH_PRI_POST_ID', 3430 );

add_filter( 'rank_math/frontend/title', function ( $title ) {
    if ( is_singular() && get_queried_object_id() === HH_PRI_POST_ID ) {
        return 'Logiciel Prix de Revient • Simulateur Gratuit & Comparatif 2026';
    }
    return $title;
} );

add_filter( 'rank_math/frontend/description', function ( $desc ) {
    if ( is_singular() && get_queried_object_id() === HH_PRI_POST_ID ) {
        return 'Calculez votre prix de revient dans le simulateur gratuit, puis comparez '
             . 'les logiciels du marché : INBP-CR, Otami, Quantara, ERP. Relevé du 27/08/2026.';
    }
    return $desc;
} );
