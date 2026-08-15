<?php
/**
 * ============================================================================
 * HELLO HAREL — T2 · Canonisation des URL à ancre (#s-*)
 * ----------------------------------------------------------------------------
 * À coller dans : Code Snippets → Add New → « Run snippet everywhere » → Save & Activate.
 *
 * CONSTAT (audit + live 2026-08-15) :
 *   163 URL en #s-* sont indexées séparément = 119 439 impressions / 19 clics / 90 j
 *   (≈ 80 % des impressions du site), /blog/cout-prix-au-kilo/ en disperse 50 241.
 *   Source des fragments : le sommaire d'article rendu en <nav class="hha-toc">…</nav>
 *   (dans <div class="hh-blog-toc">), composé de liens de saut <a href="#s-0">…</a>.
 *   565 fragments #s-* recensés sur 71 pages. Ce sont ces <a href="#s-N"> que Google
 *   découvre et transforme en résultats « aller à » / deep-links fragmentés.
 *
 * DEUX LEVIERS POSÉS PAR CE SNIPPET :
 *   (A) rel=canonical sans fragment, auto-référent, ASSERTÉ sur chaque page single.
 *       Un fragment (#s-N) partage le <head> de sa page mère : il hérite donc déjà de
 *       ce canonical → chaque #s-* pointe vers son URL mère. On force la valeur pour
 *       supprimer tout doute (et neutraliser une éventuelle réécriture tierce).
 *   (B) Neutralisation des liens de saut crawlables : on réécrit, dans le contenu,
 *       les <a href="#s-N"> du sommaire en éléments cliquables SANS href (role="link"
 *       + data-jump). L'UX de défilement est conservée par un petit JS. Google ne voit
 *       plus d'URL fragmentée à indexer.
 *
 * PORTÉE : n'agit que sur le bloc sommaire .hha-toc — le reste du contenu et les
 *   ancres de destination (id="s-N") ne sont pas modifiés. Aucune page protégée
 *   ne change d'URL, de gabarit ni de balisage.
 *
 * ACCEPTATION : plus aucune URL contenant # dans le rapport Pages de la Search
 *   Console à J+30 (après recrawl + éventuelle demande de suppression temporaire
 *   des motifs #s- dans GSC pour accélérer).
 * ============================================================================
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------------------------------------------------------------------
 * (A) Canonical auto-référent sans fragment.
 * ------------------------------------------------------------------------- */
add_filter( 'rank_math/frontend/canonical', function ( $canonical ) {
	if ( is_singular() ) {
		$clean = get_permalink( get_queried_object_id() );
		if ( $clean ) {
			// Supprime tout fragment ou paramètre résiduel.
			$clean = strtok( $clean, '#' );
			return $clean;
		}
	}
	return $canonical;
}, 20 );

/* ---------------------------------------------------------------------------
 * (B) Neutralisation des liens de saut du sommaire (.hha-toc).
 *     On transforme <a href="#s-N">Label</a> en
 *       <a role="link" tabindex="0" class="hha-jump" data-jump="s-N">Label</a>
 *     uniquement à l'intérieur du bloc <nav class="hha-toc"> … </nav>.
 * ------------------------------------------------------------------------- */
add_filter( 'the_content', function ( $content ) {
	if ( is_admin() || strpos( $content, 'hha-toc' ) === false ) {
		return $content;
	}

	// Cible le(s) bloc(s) <nav class="...hha-toc...">…</nav>.
	$content = preg_replace_callback(
		'#(<nav\b[^>]*class="[^"]*hha-toc[^"]*"[^>]*>)(.*?)(</nav>)#is',
		function ( $m ) {
			$inner = $m[2];
			// Remplace chaque href="#s-XXX" par data-jump + attributs a11y, en retirant href.
			$inner = preg_replace_callback(
				'~<a\b([^>]*?)href="\#(s-[a-z0-9\-]+)"([^>]*)>~i',
				function ( $a ) {
					$before = trim( $a[1] );
					$after  = trim( $a[3] );
					$target = $a[2];
					$attrs  = trim( $before . ' ' . $after );
					return '<a ' . ( $attrs ? $attrs . ' ' : '' )
						. 'role="link" tabindex="0" class="hha-jump" data-jump="' . esc_attr( $target ) . '">';
				},
				$inner
			);
			return $m[1] . $inner . $m[3];
		},
		$content
	);

	return $content;
}, 20 );

/* ---------------------------------------------------------------------------
 * (B-bis) JS minimal : rend les .hha-jump fonctionnels (défilement doux) sans
 *          exposer d'URL fragmentée. history.replaceState évite d'écrire le #
 *          dans la barre d'adresse (donc rien à crawler / partager).
 * ------------------------------------------------------------------------- */
add_action( 'wp_footer', function () {
	if ( is_admin() ) { return; }
	?>
<script>
(function () {
  function jump(el) {
    var id = el.getAttribute('data-jump');
    if (!id) return;
    var t = document.getElementById(id);
    if (!t) return;
    t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (window.history && history.replaceState) {
      history.replaceState(null, '', location.pathname + location.search);
    }
  }
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('.hha-jump') : null;
    if (el) { e.preventDefault(); jump(el); }
  });
  document.addEventListener('keydown', function (e) {
    if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('hha-jump')) {
      e.preventDefault(); jump(e.target);
    }
  });
})();
</script>
<style>.hha-jump{cursor:pointer}</style>
	<?php
}, 99 );
