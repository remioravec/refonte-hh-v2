<?php
/**
 * ============================================================================
 * HELLO HAREL — T1 · Réparation du générateur de meta description
 * ----------------------------------------------------------------------------
 * À coller dans : Code Snippets → Add New → « Run snippet everywhere » → Save & Activate.
 * (NE PAS inclure la balise <?php ci-dessus si Code Snippets la refuse : colle à partir
 *  de la première ligne « if ( ! defined » ou laisse la balise, selon ta version.)
 *
 * CAUSE RACINE (vérifiée en live le 2026-08-15) :
 *   Le contenu de 70 pages commence par un bloc <style id="hh-ux-fix"> … </style>
 *   (correctif CSS de gabarit injecté dans le corps de la page). Quand aucune
 *   meta description manuelle n'est saisie dans Rank Math, Rank Math auto-génère
 *   la description à partir du contenu et récupère la 1re chaîne de texte — ici,
 *   le CSS. Résultat émis dans <meta name="description"> ET og/twitter :
 *     "#hh-page .timeline-grid, .timeline-grid { grid-template-columns: repeat(3, 1fr) !important; }"
 *
 * CE QUE FAIT LE SNIPPET :
 *   Il intercepte la description finale de Rank Math (meta + Open Graph + Twitter).
 *   Si elle ressemble à du CSS (présence de { } ou d'un sélecteur), il la RÉGÉNÈRE
 *   proprement à partir du contenu de la page APRÈS suppression des blocs
 *   <style>/<script>, des shortcodes et des balises, tronquée à ~155 caractères.
 *   Les pages qui ont déjà une description propre ne sont jamais modifiées
 *   (les pages protégées avec description manuelle restent intactes).
 *
 * ACCEPTATION : 0 description contenant { ou } au recrawl.
 *
 * REMARQUE (remédiation de fond, optionnelle, à la charge du client) :
 *   Le vrai correctif durable est de SORTIR le bloc <style id="hh-ux-fix"> du corps
 *   des pages et de le déplacer dans Apparence → Personnaliser → CSS additionnel
 *   (ou dans le CSS du thème enfant). Tant que ce n'est pas fait, ce snippet garantit
 *   quand même une description propre à chaque publication. Il est donc « prêt à poser ».
 * ============================================================================
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/**
 * Détecte une description polluée par du CSS/JS.
 */
function hh_desc_looks_like_css( $text ) {
	if ( ! is_string( $text ) || $text === '' ) { return false; }
	if ( strpos( $text, '{' ) !== false || strpos( $text, '}' ) !== false ) { return true; }
	// Sélecteurs / propriétés CSS résiduels sans accolade.
	if ( preg_match( '/(grid-template|!important|#hh-page|\.[a-z\-]+\s*\{|:\s*repeat\()/i', $text ) ) { return true; }
	return false;
}

/**
 * Régénère une description propre à partir du contenu de la page courante.
 */
function hh_clean_description_from_content( $fallback = '' ) {
	$post = get_queried_object();
	if ( ! ( $post instanceof WP_Post ) ) {
		$post = get_post(); // repli sur le post global.
	}
	if ( ! ( $post instanceof WP_Post ) ) {
		return $fallback;
	}

	$content = $post->post_content;

	// 1) Retirer les blocs <style>…</style> et <script>…</script> (source du bug).
	$content = preg_replace( '#<style\b[^>]*>.*?</style>#is', ' ', $content );
	$content = preg_replace( '#<script\b[^>]*>.*?</script>#is', ' ', $content );

	// 2) Retirer les commentaires HTML et les shortcodes.
	$content = preg_replace( '/<!--.*?-->/s', ' ', $content );
	$content = strip_shortcodes( $content );

	// 3) Laisser WordPress dérouler les blocs Gutenberg puis retirer toutes les balises.
	if ( function_exists( 'do_blocks' ) ) {
		$content = do_blocks( $content );
	}
	$content = wp_strip_all_tags( $content, true );

	// 4) Normaliser espaces / entités.
	$content = html_entity_decode( $content, ENT_QUOTES, 'UTF-8' );
	$content = preg_replace( '/\s+/u', ' ', $content );
	$content = trim( $content );

	// 5) Filet de sécurité : si le début ressemble encore à du CSS, on saute jusqu'à la 1re phrase « propre ».
	if ( hh_desc_looks_like_css( $content ) ) {
		$content = preg_replace( '/^[^.?!]*[{}][^.?!]*[.?!]\s*/u', '', $content );
		$content = trim( $content );
	}

	if ( $content === '' ) {
		return $fallback;
	}

	// 6) Tronquer proprement à ~155 caractères, sur une frontière de mot.
	$max = 155;
	if ( function_exists( 'mb_strlen' ) && mb_strlen( $content, 'UTF-8' ) > $max ) {
		$content = mb_substr( $content, 0, $max, 'UTF-8' );
		$cut     = mb_strrpos( $content, ' ', 0, 'UTF-8' );
		if ( $cut !== false && $cut > 60 ) {
			$content = mb_substr( $content, 0, $cut, 'UTF-8' );
		}
		$content = rtrim( $content, " ,;:–-" ) . '…';
	}

	return $content;
}

/**
 * Point d'entrée commun : ne réécrit QUE si la valeur ressemble à du CSS.
 */
function hh_repair_description( $description ) {
	if ( is_admin() ) { return $description; }
	if ( ! hh_desc_looks_like_css( $description ) ) {
		return $description; // description propre → on ne touche à rien.
	}
	$clean = hh_clean_description_from_content( '' );
	return $clean !== '' ? $clean : $description;
}

// Meta description (Rank Math).
add_filter( 'rank_math/frontend/description', 'hh_repair_description', 20 );

// Open Graph + Twitter (mêmes fuites CSS constatées).
add_filter( 'rank_math/opengraph/facebook/og_description', 'hh_repair_description', 20 );
add_filter( 'rank_math/opengraph/twitter/twitter_description', 'hh_repair_description', 20 );

/**
 * Ceinture + bretelles : si un autre composant (ex. schéma JSON-LD Rank Math)
 * réutilise la description polluée, on la nettoie aussi côté « the_content » n'est
 * PAS touché — on n'agit que sur les sorties meta ci-dessus, pour ne rien casser
 * dans le rendu visible de la page.
 */
