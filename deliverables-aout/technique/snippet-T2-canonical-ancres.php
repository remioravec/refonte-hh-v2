<?php
/**
 * ============================================================================
 * HELLO HAREL — T2 · Canonisation des URL à ancre (#s-*)
 * ----------------------------------------------------------------------------
 * Déposé par REST (Code Snippets), « Run snippet everywhere ».
 *
 * RELEVÉ LIVE 27/08/2026 (71 pages porteuses, toutes sous /blog/) :
 *   1 147 liens de saut <a href="#s-N"> · 567 fragments uniques
 *   Le sommaire <nav class="hha-toc"> est rendu DEUX fois par page
 *   (carte mobile en tête + carte latérale desktop) : d'où 1 147 pour 567 cibles.
 *   Aucune des 5 pages protégées n'est concernée.
 *
 * CE QUE CE SNIPPET NE FAIT PAS — et pourquoi :
 *   Poser un rel=canonical « par fragment » n'est pas implémentable : le
 *   fragment n'est jamais transmis au serveur, une URL #s-N partage donc le
 *   <head> de sa page mère. Elle hérite déjà de son canonical. Vérifié le
 *   27/08 sur les 71 pages : 70 portent un canonical auto-référent sans
 *   fragment ; la 71e (/blog/erp-agroalimentaire/) n'en porte pas parce
 *   qu'elle est en noindex — comportement normal de Rank Math.
 *   Aucun filtre n'est donc posé sur le canonical : le balisage existant est
 *   correct, et y toucher modifierait le <head> des pages protégées.
 *
 * CE QUE CE SNIPPET FAIT :
 *   Il retire les liens de saut crawlables du sommaire. <a href="#s-N">Label</a>
 *   devient <a class="hha-jump" data-jump="s-N" role="link" tabindex="0">Label</a>.
 *   Google ne découvre plus d'URL fragmentée à afficher en lien de section ;
 *   l'utilisateur garde le défilement (JS délégué ci-dessous) et le clavier.
 *
 * PORTÉE : uniquement l'intérieur de <nav class="hha-toc"> et <div class="som">. Les titres cibles
 *   (id="s-N"), le reste du contenu, le CSS (.hha-toc a) et le scroll-spy
 *   (indexé sur la position, pas sur le href) sont inchangés.
 *
 * DÉGRADATION SANS JS : le sommaire reste lisible (il annonce le plan) mais le
 *   saut ne fonctionne plus — le lecteur fait défiler. Contenu intégralement
 *   présent dans la page, aucune information n'est perdue.
 *
 * RÉVERSIBLE : désactiver l'extrait restaure les href à la requête suivante
 *   (aucune écriture en base, le post_content n'est pas modifié).
 *
 * ACCEPTATION : plus aucune URL contenant # dans le rapport Pages de la Search
 *   Console à J+30.
 * ============================================================================
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------------------------------------------------------------------
 * Neutralisation des liens de saut des deux sommaires du blog :
 *   - <nav class="hha-toc">      : gabarit historique, rendu deux fois par page
 *   - <div class="som">          : gabarit validé (prix de revient / distributeurs)
 * ------------------------------------------------------------------------- */
add_filter( 'the_content', function ( $content ) {

	if ( is_admin() || is_feed() || ! is_singular() ) {
		return $content;
	}
	if ( strpos( $content, 'href="#s-' ) === false ) {
		return $content;
	}

	$touche = 0;

	// Réécrit les <a href="#s-N"> d'un bloc sommaire, et lui seul.
	$reecrire = function ( $inner ) use ( &$touche ) {
		return preg_replace_callback(
			'~<a\b([^>]*?)\shref="\#(s-[0-9a-z\-]+)"([^>]*)>~i',
			function ( $a ) use ( &$touche ) {
				$touche++;
				$attrs = trim( trim( $a[1] ) . ' ' . trim( $a[3] ) );
				return '<a ' . ( $attrs ? $attrs . ' ' : '' )
					. 'class="hha-jump" role="link" tabindex="0" data-jump="'
					. esc_attr( $a[2] ) . '">';
			},
			$inner
		);
	};

	$conteneurs = array(
		'#(<nav\b[^>]*class="[^"]*hha-toc[^"]*"[^>]*>)(.*?)(</nav>)#is',
		'#(<div\b[^>]*class="som"[^>]*>)(.*?)(</div>)#is',
	);

	foreach ( $conteneurs as $motif ) {
		$content = preg_replace_callback(
			$motif,
			function ( $m ) use ( $reecrire ) {
				return $m[1] . $reecrire( $m[2] ) . $m[3];
			},
			$content
		);
	}

	if ( $touche > 0 ) {
		$GLOBALS['hh_t2_jump'] = true;
	}

	return $content;
}, 20 );

/* ---------------------------------------------------------------------------
 * Défilement doux + clavier, uniquement si un sommaire a été neutralisé.
 * Aucun # n'est écrit dans la barre d'adresse : rien de nouveau à crawler.
 * ------------------------------------------------------------------------- */
add_action( 'wp_footer', function () {

	if ( empty( $GLOBALS['hh_t2_jump'] ) ) { return; }
	?>
<style>.hha-jump{cursor:pointer}</style>
<script>
(function () {
  function sauter(el) {
    var id = el.getAttribute('data-jump');
    if (!id) { return; }
    var cible = document.getElementById(id);
    if (!cible) { return; }
    cible.scrollIntoView({ behavior: 'smooth', block: 'start' });
    if (!cible.hasAttribute('tabindex')) { cible.setAttribute('tabindex', '-1'); }
    cible.focus({ preventScroll: true });
  }
  document.addEventListener('click', function (e) {
    var el = e.target && e.target.closest ? e.target.closest('.hha-jump') : null;
    if (el) { e.preventDefault(); sauter(el); }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') { return; }
    var el = e.target && e.target.closest ? e.target.closest('.hha-jump') : null;
    if (el) { e.preventDefault(); sauter(el); }
  });
})();
</script>
	<?php
}, 99 );
