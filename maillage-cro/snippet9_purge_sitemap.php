/**
 * T4 — Resynchroniser le sitemap Rank Math (v3)
 *
 * Rejoue le 06/10/2026 : le cache fichier n'avait pas bouge depuis le 11/09.
 * Le sitemap servait encore 10 URL supprimees (pages IA, integrateurs,
 * article Akanea) et ignorait les 3 landings de septembre. Apres purge :
 * 171 URL pour 172 publiees, l'ecart etant /blog/erp-agroalimentaire/, dont
 * la canonique pointe vers /agroalimentaire/ — exclusion normale.
 *
 * LA CAUSE RESTE OUVERTE : le cache ne s'invalide pas tout seul a la
 * publication. Il faudra rejouer cet extrait (marqueur + date) a chaque
 * campagne de publication tant que la cause n'est pas traitee.
 *
 * Le premier essai purgeait les transients et cherchait une table dediee.
 * Le diagnostic a montre que Rank Math met le sitemap en cache DANS DES FICHIERS,
 * suivis par l'option rank_math_sitemap_cache_files. C'est cette voie qu'il faut
 * emprunter, via l'invalidation officielle de la classe Cache.
 *
 * Execute une seule fois, puis se neutralise.
 */
add_action( 'init', function () {

    $marqueur = 'hh_t4_sitemap_flush_v3';
    if ( get_option( $marqueur ) === '2026-10-06' ) {
        return;
    }

    // 1 · invalidation officielle, cote fichiers
    if ( class_exists( '\RankMath\Sitemap\Cache' ) &&
         method_exists( '\RankMath\Sitemap\Cache', 'invalidate_storage' ) ) {
        \RankMath\Sitemap\Cache::invalidate_storage();
    }
    if ( class_exists( '\RankMath\Sitemap\Cache_Watcher' ) &&
         method_exists( '\RankMath\Sitemap\Cache_Watcher', 'invalidate_storage' ) ) {
        \RankMath\Sitemap\Cache_Watcher::invalidate_storage();
    }

    // 2 · le registre des fichiers de cache
    delete_option( 'rank_math_sitemap_cache_files' );

    // 3 · les reliquats Yoast, qui ne servent plus a rien ici
    delete_option( 'wpseo_sitemap_cache_validator_global' );
    delete_option( 'wpseo_sitemap_page_cache_validator' );
    delete_option( 'wpseo_sitemap_post_cache_validator' );
    delete_option( 'wpseo_sitemap_1_cache_validator' );

    // 4 · les transients, par securite
    global $wpdb;
    $wpdb->query(
        "DELETE FROM {$wpdb->options}
         WHERE option_name LIKE '\_transient\_rank\_math\_sitemap%'
            OR option_name LIKE '\_transient\_timeout\_rank\_math\_sitemap%'"
    );

    update_option( $marqueur, '2026-10-06' );
}, 99 );