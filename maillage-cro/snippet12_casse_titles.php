/**
 * HELLO HAREL — Casse francaise des titles
 *
 * CAUSE TROUVEE LE 01/10/2026. Ce n'est ni le theme ni un filtre maison : le
 * reglage Rank Math « Capitalize Titles » (titles.capitalize_titles) etait sur
 * ON. Rank Math passe un ucwords() sur le title DANS sa propre composition,
 * donc avant pre_get_document_title et avant les filtres og_title. C'est
 * pourquoi la version du 01/10 au matin, qui se contentait de renvoyer
 * RankMath\Paper\Paper::get()->get_title(), rendait encore « Coût De Revient » :
 * elle renvoyait fidelement une chaine deja capitalisee.
 *
 * ETAT AU 06/10/2026 : le reglage est TOUJOURS SUR ON. Mesure du jour — les
 * deux titles poses ce matin (4813, 5640) ressortent capitalises, et
 * /blog/bon-de-livraison/ sert encore « Bon De Livraison ». Il reste un clic
 * a faire dans Rank Math > Titres & Meta > decocher « Capitaliser les titles ».
 * Tant qu'il n'est pas fait, chaque title neuf doit etre epingle ci-dessous.
 *
 * REGLE 0 — /agroalimentaire/charcutier/ (2818) et /migration-as400/ (11162)
 * ne doivent pas bouger d'un octet. Leur title capitalise est donc fige ici,
 * a l'identique de ce qui etait servi avant la bascule, title et og:title.
 *
 * Les quatre titles rediges a la main restent prioritaires sur le reste.
 */

/** Regle 0 : titles figes, identiques a l'octet pres a l'avant-bascule. */
function hh_titles_intouchables() {
	return array(
		2818  => 'ERP Charcutier • Découpe &amp; Rendements • 99,9% Uptime ☁️',
		11162 => 'Migration AS/400 : Audit Gratuit &amp; Reprise De Données Garantie - Hello Harel',
	);
}

/** Les titles rediges a la main, prioritaires sur tout le reste. */
function hh_titles_refondus() {
	return array(
		3430  => 'Logiciel Prix de Revient • Simulateur Gratuit et Comparatif 2026',
		5269  => 'ERP pour Distributeurs de Produits Frais • Comparatif 2026',
		10895 => 'ERP Glacier • Foisonnement, Lots et Coût de Revient au Litre',
		5957  => 'ERP négoce et distribution alimentaire • Poids réel, DLC, marge',
		/* Roadmap contenu : mises a jour du 21/09, 28/09 et 05/10/2026. */
		4798  => 'Logiciel achat agroalimentaire • Fournisseurs, PMP et seuils',
		4736  => 'CRM agroalimentaire • Cadencier, télévente et tarifs client',
		4778  => 'Logiciel de fabrication agroalimentaire • Recettes et rendements',
		4750  => 'Logiciel de facturation agroalimentaire • Poids réel et tarifs',
		4772  => 'Logiciel de gestion de stock agroalimentaire • FEFO, DLC, lots',
		7905  => 'Facturation automatique depuis bon de livraison • ERP grossiste',
		7912  => 'Consigne bouteille • Logiciel de suivi, retours et soldes client',
		7909  => 'Rendement matière • Logiciel de suivi des pertes et des freintes',
	);
}

/**
 * Les titles dont la valeur en base est juste, et que le reglage Rank Math
 * « Capitalize Titles » capitalise a la sortie. Ils sont rendus tels qu'ils
 * sont stockes, pour que la correction de la casse en base se VOIE.
 *
 * CET ARRAY EST TEMPORAIRE. Le jour ou le reglage est decoche
 * (Rank Math > Titres & Meta > Capitaliser les titles), il devient inutile :
 * chaque title sortira deja dans la bonne casse. On pourra le vider sans
 * rien changer au rendu.
 */
function hh_titles_casse_en_attente() {
	return array(
		2     => 'ERP agroalimentaire • Agile et sur-mesure • 200+ PME',
		608   => 'Tarifs ERP agro • Transparent et sans engagement • 99 €',
		5287  => 'ERP pour PME • Simple et rentable • Guide complet 2026',
		7761  => 'Traçabilité lot et DLC • Logiciel de suivi • Guide 2026',
		7766  => 'Calcul coût de revient • Logiciel agroalimentaire • Guide',
		7769  => 'Remplacer Excel en agroalimentaire • Migration ERP',
		7910  => 'Planification de production ERP • CBN et ordonnancement',
		7911  => 'Logiciel devis, commande et bon de livraison • ERP',
		7944  => 'Logiciel coût de revient traiteur • Marge par plat',
		8112  => 'Calcul freinte charcuterie • Perte de séchage • Logiciel',
		10865 => 'Logiciel et ERP pâtisserie • Prix de revient et marge',
		10868 => 'Logiciel et ERP poissonnerie • Mareyage et poids variable',
		/* Roadmap contenu : semaine du 12/10/2026. */
		4813  => 'Logiciel import export agroalimentaire • Douane et frais d\'approche',
		5640  => 'Logiciel import export et gestion commerciale • Comparatif 2026',
		/* Technique 06/10 : trois pages servaient « Nom - Hello Harel », sous 200 px. */
		141   => 'Blog ERP agroalimentaire • Traçabilité, coûts de revient et marge',
		5958  => 'ERP médical • Traçabilité des lots et conformité réglementaire',
		5960  => 'ERP pour laboratoires • Suivi des lots, analyses et conformité',
		/* Les dix pages d'implantation : noms de region remis d'aplomb. */
		5964  => 'ERP agroalimentaire • Nos implantations en France',
		5965  => 'ERP agroalimentaire à La Réunion',
		5966  => 'ERP agroalimentaire à Maurice',
		5967  => 'ERP agroalimentaire en Belgique',
		5968  => 'ERP agroalimentaire en Île-de-France',
		5969  => 'ERP agroalimentaire en Hauts-de-France',
		5970  => 'ERP agroalimentaire en Auvergne-Rhône-Alpes',
		5971  => 'ERP agroalimentaire en Occitanie',
		5972  => 'ERP agroalimentaire en Nouvelle-Aquitaine',
		5973  => 'ERP agroalimentaire en Bretagne',
	);
}

/** Le title voulu pour un ID, ou '' si on laisse la chaine normale faire. */
function hh_title_voulu( $id ) {
	$id = (int) $id;
	if ( ! $id ) {
		return '';
	}
	$figes = hh_titles_intouchables();
	if ( isset( $figes[ $id ] ) ) {
		return $figes[ $id ];
	}
	$refondus = hh_titles_refondus();
	if ( isset( $refondus[ $id ] ) ) {
		return $refondus[ $id ];
	}
	$attente = hh_titles_casse_en_attente();
	return isset( $attente[ $id ] ) ? $attente[ $id ] : '';
}

/** Sortie reelle de la balise <title>. */
add_filter( 'pre_get_document_title', function ( $title ) {
	if ( ! is_singular() ) {
		return $title;
	}
	$voulu = hh_title_voulu( get_queried_object_id() );
	return '' !== $voulu ? $voulu : $title;
}, PHP_INT_MAX );

/* Coherence des titres sociaux. */
foreach ( array( 'rank_math/opengraph/facebook/og_title', 'rank_math/opengraph/twitter/twitter_title' ) as $hh_hook ) {
	add_filter( $hh_hook, function ( $title ) {
		if ( ! is_singular() ) {
			return $title;
		}
		$voulu = hh_title_voulu( get_queried_object_id() );
		return '' !== $voulu ? $voulu : $title;
	}, PHP_INT_MAX );
}
unset( $hh_hook );
