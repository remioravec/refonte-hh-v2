<?php
/**
 * ============================================================================
 * HELLO HAREL — T5 · Dédoublonnage du JSON-LD
 * ----------------------------------------------------------------------------
 * À coller dans : Code Snippets → Add New → « Run snippet everywhere » → Save & Activate.
 *
 * ÉTAT MESURÉ EN LIVE (2026-08-15) — 3 générateurs cohabitent :
 *
 *  BLOC 0 (Rank Math, auto)  — sur toutes les pages
 *     @graph propre : Organization + WebSite + WebPage + SearchAction (+ ImageObject).
 *     >>> À CONSERVER. C'est la source unique et correcte d'Organization et WebSite.
 *
 *  BLOC A (snippet custom « SoftwareApplication », ~1 395 car.) — sur TOUTES les pages
 *     SoftwareApplication + aggregateRating (5.0 / 31) + Offer + creator:Organization + Thing.
 *     C'est lui qui affiche les étoiles dans la SERP (5,0/31 sur le comparatif charcuterie).
 *     >>> À CONSERVER, mais il devient l'UNIQUE porteur de la note (voir ci-dessous).
 *
 *  BLOC B (snippet custom « LocalBusiness », ~4 559 car.) — sur l'ACCUEIL uniquement
 *     LocalBusiness + 2e AggregateRating (5/31) + 2e SoftwareApplication + Person +
 *     OfferCatalog + plusieurs Organization + 2 WebSite + BreadcrumbList.
 *     >>> C'EST LE COUPABLE. Il crée à lui seul, sur l'accueil :
 *         2e AggregateRating, 2e SoftwareApplication, +2 WebSite, +3 Organization.
 *         => 5 Organization, 3 WebSite, 2 SoftwareApplication, 2 AggregateRating.
 *     Le DOUBLE AggregateRating est le risque n°1 : Google peut ignorer les étoiles.
 *
 *  BLOC LocalBusiness court (~433 car.) — sur les gabarits métier/comparatif
 *     LocalBusiness + PostalAddress (NAP, sans note). Inoffensif pour les étoiles.
 *     >>> Peut rester ; il ne crée aucun doublon de note. (Voir option ci-dessous.)
 *
 * ----------------------------------------------------------------------------
 * ACTION DEMANDÉE AU CLIENT (manuelle, 5 min — NON scriptable à distance) :
 *   1. Aller dans Code Snippets (et/ou Elementor « Custom Code » / en-tête du thème).
 *   2. Repérer le snippet qui émet le BLOC B. Signatures faciles à rechercher :
 *        "OpeningHoursSpecification", "GeoCoordinates", "OfferCatalog",
 *        "Timothy Jollivet", "Belgium", "Mauritius".
 *   3. DÉSACTIVER ce snippet (BLOC B). NE PAS toucher au BLOC A ni à Rank Math.
 *   >>> À lui seul, cela ramène l'accueil à 1 Organization, 1 WebSite,
 *       1 SoftwareApplication, 1 AggregateRating.
 *
 * Ce fichier PHP fait DEUX choses complémentaires :
 *   - Il garde une seule entité SoftwareApplication + AggregateRating propre,
 *     émise partout (les étoiles restent). Si tu préfères conserver le BLOC A
 *     existant tel quel, laisse la section (1) commentée.
 *   - Il retire, par sécurité, tout 2e AggregateRating résiduel qui traînerait
 *     encore dans le <head> si le client n'a pas pu désactiver le BLOC B (section 2).
 *
 * ACCEPTATION : test des résultats enrichis (Rich Results Test) sans avertissement
 *   de doublon sur les 3 gabarits (accueil, métier, comparatif), étoiles conservées.
 * ============================================================================
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ===========================================================================
 * (1) SOURCE UNIQUE de SoftwareApplication + AggregateRating.
 *     >>> N'active cette section QUE si tu as désactivé À LA FOIS le BLOC A et le
 *         BLOC B côté admin, et que tu veux que ce snippet devienne l'émetteur
 *         unique et versionné de la note produit. Sinon, garde le BLOC A existant
 *         (ne rien décommenter) — il fait déjà le travail proprement.
 *     Décommente le bloc ci-dessous pour l'activer.
 * ------------------------------------------------------------------------- */
/*
add_action( 'wp_head', function () {
	if ( is_admin() ) { return; }
	$node = array(
		'@context'            => 'https://schema.org',
		'@type'               => 'SoftwareApplication',
		'name'                => 'Hello Harel',
		'operatingSystem'     => 'All',
		'applicationCategory' => 'BusinessApplication',
		'applicationSubCategory' => 'ERP',
		'url'                 => 'https://www.helloharel.com',
		'offers'              => array(
			'@type'         => 'Offer',
			'price'         => '99',
			'priceCurrency' => 'EUR',
		),
		'aggregateRating'     => array(
			'@type'       => 'AggregateRating',
			'ratingValue' => '5.0',
			'reviewCount' => '31',
			'bestRating'  => '5',
			'worstRating' => '1',
		),
		'creator'             => array(
			'@type' => 'Organization',
			'name'  => 'HAREL SYSTEMS',
			'url'   => 'https://www.helloharel.com',
		),
	);
	echo "\n" . '<script type="application/ld+json">'
		. wp_json_encode( $node, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE )
		. '</script>' . "\n";
}, 5 );
*/

/* ===========================================================================
 * (2) FILET DE SÉCURITÉ — supprime tout 2e AggregateRating dans le <head>
 *     au cas où le BLOC B n'aurait pas été désactivé côté admin.
 *     Il garde le PREMIER bloc JSON-LD qui contient une AggregateRating (le BLOC A,
 *     émis tôt) et retire l'AggregateRating de tous les blocs JSON-LD suivants.
 *     Ne touche à aucun autre type ni au rendu visible.
 * ------------------------------------------------------------------------- */
add_action( 'template_redirect', function () {
	if ( is_admin() ) { return; }
	ob_start( 'hh_dedupe_aggregaterating' );
}, 1 );

function hh_dedupe_aggregaterating( $html ) {
	if ( stripos( $html, 'AggregateRating' ) === false ) {
		return $html;
	}
	$seen = 0;
	return preg_replace_callback(
		'#<script[^>]*type=(["\'])application/ld\+json\1[^>]*>(.*?)</script>#is',
		function ( $m ) use ( &$seen ) {
			if ( stripos( $m[0], 'AggregateRating' ) === false ) {
				return $m[0]; // bloc sans note : inchangé.
			}
			$seen++;
			if ( $seen === 1 ) {
				return $m[0]; // 1re note (BLOC A) : on la garde, c'est elle qui donne les étoiles.
			}
			// Blocs suivants : on retire proprement le noeud aggregateRating (JSON).
			$decoded = json_decode( $m[2], true );
			if ( is_array( $decoded ) ) {
				$decoded = hh_strip_key_recursive( $decoded, 'aggregateRating' );
				$decoded = hh_strip_type_recursive( $decoded, 'AggregateRating' );
				$json    = wp_json_encode( $decoded, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );
				return '<script type="application/ld+json">' . $json . '</script>';
			}
			// Repli si JSON non décodable : neutralise la clé par regex.
			$cleaned = preg_replace( '#,?\s*"aggregateRating"\s*:\s*\{[^{}]*\}#s', '', $m[2] );
			return '<script type="application/ld+json">' . $cleaned . '</script>';
		},
		$html
	);
}

/** Retire récursivement une clé (ex. "aggregateRating") d'un tableau JSON décodé. */
function hh_strip_key_recursive( $data, $key ) {
	if ( ! is_array( $data ) ) { return $data; }
	unset( $data[ $key ] );
	foreach ( $data as $k => $v ) {
		if ( is_array( $v ) ) {
			$data[ $k ] = hh_strip_key_recursive( $v, $key );
		}
	}
	return $data;
}

/** Retire récursivement tout noeud dont @type == $type (ex. items d'un tableau). */
function hh_strip_type_recursive( $data, $type ) {
	if ( ! is_array( $data ) ) { return $data; }
	foreach ( $data as $k => $v ) {
		if ( is_array( $v ) && isset( $v['@type'] ) && $v['@type'] === $type ) {
			unset( $data[ $k ] );
			continue;
		}
		if ( is_array( $v ) ) {
			$data[ $k ] = hh_strip_type_recursive( $v, $type );
		}
	}
	return is_array( $data ) ? array_values_preserve( $data ) : $data;
}

/** Réindexe uniquement les listes (clés 0..n), préserve les objets associatifs. */
function array_values_preserve( $data ) {
	$keys = array_keys( $data );
	$is_list = $keys === range( 0, count( $data ) - 1 );
	return $is_list ? array_values( $data ) : $data;
}
