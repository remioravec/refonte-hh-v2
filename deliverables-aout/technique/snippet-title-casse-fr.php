<?php
/**
 * ============================================================================
 * HELLO HAREL — Casse française des titles refondus
 * ----------------------------------------------------------------------------
 * CONSTAT 27/08/2026 : le site capitalise chaque mot du title rendu. Le title
 * posé « Logiciel Prix de Revient… » ressort « Logiciel Prix De Revient… » :
 * le « de » de l'expression exacte est capitalisé, ce qui n'est pas de la
 * typographie française.
 *
 * DIAGNOSTIC : la capitalisation s'applique APRÈS le filtre
 * rank_math/frontend/title (vérifié en direct). Le seul point de sortie qui
 * la précède est pre_get_document_title, qui court-circuite toute la chaîne.
 *
 * POURQUOI UN FILTRE CIBLÉ ET NON UN RÉGLAGE GLOBAL : couper la capitalisation
 * dans les réglages changerait le title des 5 pages protégées.
 * Règle 0 — aucune modification de leur balisage. On ne corrige donc que les
 * deux pages dont le title a été refondu.
 *
 * PORTÉE : posts 3430 et 5269, pages 10895, 10934 et 5957. Les meta descriptions ne subissent pas la
 * capitalisation : elles restent gérées dans l'onglet Rank Math.
 * ============================================================================
 */

function hh_titles_refondus() {
	return array(
		3430 => 'Logiciel Prix de Revient • Simulateur Gratuit et Comparatif 2026',
		5269 => 'ERP pour Distributeurs de Produits Frais • Comparatif 2026',
		10895 => 'ERP Glacier • Foisonnement, Lots et Coût de Revient au Litre',
		10934 => 'ERP Négoce Alimentaire • Poids Réel, DLC et Marge Grossiste',
		5957  => 'ERP Négoce • Achats, Stocks, Ventes et Tarifs',
	);
}

function hh_title_refondu() {
	if ( ! is_singular() ) {
		return null;
	}
	$titres = hh_titles_refondus();
	$id     = get_queried_object_id();
	return isset( $titres[ $id ] ) ? $titres[ $id ] : null;
}

/* Sortie réelle de la balise <title> — court-circuite la capitalisation. */
add_filter( 'pre_get_document_title', function ( $title ) {
	$t = hh_title_refondu();
	return ( null !== $t ) ? $t : $title;
}, PHP_INT_MAX );

/* Cohérence des titres sociaux (Open Graph / Twitter). */
foreach ( array( 'rank_math/opengraph/facebook/og_title', 'rank_math/opengraph/twitter/twitter_title' ) as $hh_hook ) {
	add_filter( $hh_hook, function ( $title ) {
		$t = hh_title_refondu();
		return ( null !== $t ) ? $t : $title;
	}, PHP_INT_MAX );
}
unset( $hh_hook );
