<?php
/**
 * NAP dans le pied de page du theme.
 *
 * Cinq pages n'embarquent pas leur propre pied et utilisent celui du
 * theme : /cgu/, /comparatifs/, /conformite-loi-anti-fraude-tva/,
 * /mentions-legales/ et /politique-de-confidentialite/. Le bloc NAP pose
 * dans le contenu des 69 autres pages ne les atteint pas.
 *
 * Ce snippet l'ajoute au pied du theme, en n'affichant rien si la page
 * porte deja le bloc — pour ne jamais l'avoir en double.
 *
 * Les valeurs sont celles des mentions legales de la societe.
 * A coller dans Code Snippets, en « Executer partout ».
 */

add_action( 'wp_footer', function () {

	// Les pages qui portent deja le bloc dans leur contenu n'en veulent pas
	// un second : on ne l'ajoute que si le contenu ne le contient pas.
	if ( is_singular() ) {
		$post = get_post();
		if ( $post && false !== strpos( (string) $post->post_content, 'class="hh-nap"' ) ) {
			return;
		}
	}

	?>
	<style id="hh-nap-theme">
	.hh-nap-theme{max-width:1180px;margin:0 auto;padding:1.1rem 22px 1.6rem;
	 font-size:.82rem;line-height:1.65;color:#64748b;font-style:normal}
	.hh-nap-theme b{display:block;color:#0f172a;font-weight:700;font-size:.88rem;
	 margin-bottom:.15rem}
	.hh-nap-theme a{color:#0369A1;text-decoration:none;font-weight:600}
	.hh-nap-theme a:hover{text-decoration:underline}
	.hh-nap-theme span{display:block}
	.hh-nap-theme .hh-nap-id{margin-top:.45rem;font-size:.74rem;color:#94a3b8}
	</style>
	<address class="hh-nap hh-nap-theme">
		<b>Harel Systems SAS</b>
		<span>6 avenue de Rueil</span>
		<span>92420 Vaucresson, France</span>
		<span>Tél. <a href="tel:+33618060018">06 18 06 00 18</a></span>
		<span class="hh-nap-id">SIREN 799992102 · TVA FR87799992102</span>
	</address>
	<?php
}, 99 );
