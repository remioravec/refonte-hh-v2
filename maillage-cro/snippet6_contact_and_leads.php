
/**
 * Endpoint REST custom pour le formulaire de contact /contact/.
 * Reçoit un POST JSON, valide, envoie un mail via wp_mail() (SMTP du site).
 */
add_action('rest_api_init', function() {
    register_rest_route('hh/v1', '/contact', [
        'methods'             => 'POST',
        'callback'            => 'hh_handle_contact_form',
        'permission_callback' => '__return_true',
    ]);
});

function hh_handle_contact_form( $request ) {
    $params = $request->get_json_params();
    if ( ! is_array( $params ) ) {
        $params = $request->get_params();
    }

    // ===== Origin check : seulement helloharel.com =====
    $origin = $request->get_header( 'origin' );
    if ( $origin && strpos( $origin, 'helloharel.com' ) === false ) {
        return new WP_REST_Response( [ 'success' => false, 'message' => 'Origin non autorisee' ], 403 );
    }

    // ===== Honeypot serveur (immuun au bypass JS) =====
    if ( ! empty( $params['website'] ) ) {
        // Faux succes pour ne pas alerter le bot
        return new WP_REST_Response( [ 'success' => true, 'message' => 'OK' ], 200 );
    }

    // ===== Validation =====
    $name    = isset( $params['name'] )    ? sanitize_text_field( $params['name'] )    : '';
    $email   = isset( $params['email'] )   ? sanitize_email( $params['email'] )        : '';
    $company = isset( $params['company'] ) ? sanitize_text_field( $params['company'] ) : '';
    $phone   = isset( $params['phone'] )   ? sanitize_text_field( $params['phone'] )   : '';
    $secteur = isset( $params['secteur'] ) ? sanitize_text_field( $params['secteur'] ) : '';
    $message = isset( $params['message'] ) ? sanitize_textarea_field( $params['message'] ) : '';

    if ( empty( $name ) || empty( $email ) || empty( $company ) || ! is_email( $email ) ) {
        return new WP_REST_Response( [ 'success' => false, 'message' => 'Champs requis manquants ou email invalide.' ], 400 );
    }

    // ===== Rate limit basique : 1 envoi / IP / 30s =====
    $ip = isset( $_SERVER['REMOTE_ADDR'] ) ? $_SERVER['REMOTE_ADDR'] : '';
    if ( $ip ) {
        $key = 'hh_contact_throttle_' . md5( $ip );
        if ( get_transient( $key ) ) {
            return new WP_REST_Response( [ 'success' => false, 'message' => 'Veuillez patienter quelques secondes avant un nouvel envoi.' ], 429 );
        }
        set_transient( $key, 1, 30 );
    }

    // ===== Composition du mail =====
    $to       = 'maxence@helloharel.com';
    $cc_addrs = [
        'administration@remi-oravec.fr',
        'timothy.jollivet@harelsystems.com',
    ];

    $subject = sprintf(
        'Demande de demo - %s%s',
        $company ? $company : $name,
        $secteur ? ' (' . $secteur . ')' : ''
    );

    $te_source   = isset( $params['te_source'] )   ? sanitize_text_field( $params['te_source'] )   : '';
    $te_medium   = isset( $params['te_medium'] )   ? sanitize_text_field( $params['te_medium'] )   : '';
    $te_campaign = isset( $params['te_campaign'] ) ? sanitize_text_field( $params['te_campaign'] ) : '';
    $te_landing  = isset( $params['te_landing'] )  ? esc_url_raw( $params['te_landing'] )           : '';

    $body_lines = [
        'Bonjour,',
        '',
        'Nouvelle demande depuis helloharel.com/contact/ :',
        '',
        '- Nom : ' . $name,
        '- Email : ' . $email,
        '- Societe : ' . $company,
        '- Telephone : ' . ( $phone ? $phone : '(non renseigne)' ),
        '- Secteur : ' . ( $secteur ? $secteur : '(non precise)' ),
        '',
        '- Message :',
        ( $message ? $message : '(aucun)' ),
        '',
        '- - - - - - -',
        'Attribution :',
        '  source : ' . ( $te_source ? $te_source : 'n/a' ),
        '  medium : ' . ( $te_medium ? $te_medium : 'n/a' ),
        '  campaign : ' . ( $te_campaign ? $te_campaign : 'n/a' ),
        '  landing : ' . ( $te_landing ? $te_landing : 'n/a' ),
        '  IP : ' . ( $ip ? $ip : 'n/a' ),
        '',
        '- - - - - - -',
        'Cordialement,',
        'Formulaire helloharel.com',
    ];
    $body = implode( "\n", $body_lines );

    $from_email = 'no-reply@helloharel.com';
    $headers    = [
        'From: Hello Harel <' . $from_email . '>',
        'Reply-To: ' . $name . ' <' . $email . '>',
        'Content-Type: text/plain; charset=UTF-8',
    ];
    foreach ( $cc_addrs as $cc ) {
        $headers[] = 'Cc: ' . $cc;
    }

    $sent = wp_mail( $to, $subject, $body, $headers );

    if ( ! $sent ) {
        return new WP_REST_Response( [ 'success' => false, 'message' => 'Envoi echoue cote serveur' ], 500 );
    }

    return new WP_REST_Response( [ 'success' => true, 'message' => 'Mail envoye' ], 200 );
}


/* ===================================================================
   HH Demandes — enregistrement des leads (100% decouple de l'email)
   Aucune modification du handler d'envoi ci-dessus. Best-effort.
   =================================================================== */
add_action('init', function () {
    register_post_type('hh_lead', array(
        'labels' => array('name' => 'Demandes', 'singular_name' => 'Demande', 'menu_name' => 'Demandes'),
        'public' => false, 'show_ui' => true, 'show_in_menu' => true, 'show_in_rest' => true,
        'rest_base' => 'hh_lead', 'menu_icon' => 'dashicons-email-alt', 'menu_position' => 26,
        'supports' => array('title'), 'capability_type' => 'post', 'map_meta_cap' => true,
    ));
});

add_action('rest_api_init', function () {
    register_rest_route('hh/v1', '/lead', array(
        'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'hh_store_lead',
    ));
});

function hh_store_lead($request) {
    try {
        $p = $request->get_json_params();
        if (!is_array($p)) { $p = $request->get_params(); }
        if (!empty($p['website']) || !empty($p['_honey'])) { return new WP_REST_Response(array('ok'=>true), 200); }
        $g = function($keys) use ($p) { foreach ((array)$keys as $k) { if (isset($p[$k]) && $p[$k] !== '') return $p[$k]; } return ''; };
        $email = sanitize_email($g(array('email','Email')));
        $name  = sanitize_text_field($g(array('name','Nom')));
        if (!$email && !$name) { return new WP_REST_Response(array('ok'=>true), 200); }
        $id = wp_insert_post(array(
            'post_type' => 'hh_lead', 'post_status' => 'publish',
            'post_title' => ($name ? $name : $email) . ' - ' . date_i18n('d/m/Y H:i'),
        ), true);
        if (!is_wp_error($id) && $id) {
            update_post_meta($id, '_hh_email', $email);
            update_post_meta($id, '_hh_name', $name);
            update_post_meta($id, '_hh_company', sanitize_text_field($g(array('company','Entreprise'))));
            update_post_meta($id, '_hh_message', sanitize_textarea_field($g(array('message','Message'))));
            update_post_meta($id, '_hh_first_page', esc_url_raw($g(array('first_page','te_landing'))));
            update_post_meta($id, '_hh_form_page', esc_url_raw($g(array('form_page'))));
            update_post_meta($id, '_hh_ip', isset($_SERVER['REMOTE_ADDR']) ? sanitize_text_field($_SERVER['REMOTE_ADDR']) : '');
            update_post_meta($id, '_hh_all', wp_json_encode($p));
        }
    } catch (\Throwable $e) { /* silencieux : ne jamais bloquer */ }
    return new WP_REST_Response(array('ok'=>true), 200);
}

add_filter('manage_hh_lead_posts_columns', function ($c) {
    return array('cb'=>isset($c['cb'])?$c['cb']:'', 'title'=>'Demande', 'hh_email'=>'Email', 'hh_company'=>'Societe', 'hh_first'=>'Page 1er clic', 'hh_form'=>'Page du formulaire', 'date'=>'Date');
});
add_action('manage_hh_lead_posts_custom_column', function ($col, $id) {
    if ($col === 'hh_email')   { echo esc_html(get_post_meta($id, '_hh_email', true)); }
    if ($col === 'hh_company') { echo esc_html(get_post_meta($id, '_hh_company', true)); }
    if ($col === 'hh_first')   { $u = get_post_meta($id, '_hh_first_page', true); echo $u ? '<a href="'.esc_url($u).'" target="_blank">'.esc_html(str_replace('https://www.helloharel.com','',$u)).'</a>' : '-'; }
    if ($col === 'hh_form')    { $u = get_post_meta($id, '_hh_form_page', true); echo $u ? esc_html(str_replace('https://www.helloharel.com','',$u)) : '-'; }
}, 10, 2);

add_action('wp_footer', function () {
    $endpoint = esc_url_raw( rest_url('hh/v1/lead') );
    echo '<script>(function(){try{if(!document.cookie.match(/(?:^|;\\s*)hh_first_page=/)){document.cookie="hh_first_page="+encodeURIComponent(location.href)+";path=/;max-age="+(60*60*24*90)+";SameSite=Lax";}function fp(){var m=document.cookie.match(/(?:^|;\\s*)hh_first_page=([^;]+)/);return m?decodeURIComponent(m[1]):location.href;}document.addEventListener("submit",function(ev){try{var f=ev.target;if(!f||f.tagName!=="FORM")return;var fd=new FormData(f);var o={};fd.forEach(function(v,k){if(typeof v==="string")o[k]=v;});o.first_page=fp();o.form_page=location.href;if(navigator.sendBeacon){navigator.sendBeacon("'.$endpoint.'",new Blob([JSON.stringify(o)],{type:"application/json"}));}}catch(e){}},true);}catch(e){}})();</script>';
}, 99);
