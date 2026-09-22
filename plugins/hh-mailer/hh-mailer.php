<?php
/**
 * Plugin Name: Hello Harel — Mailer
 * Description: Envoi SMTP via Google Workspace, mise en page Hello Harel des demandes de demo, garde-fou anti-doublon et journal des envois. Ne touche ni au formulaire, ni a l'enregistrement des leads, ni au tracking.
 * Version:     1.0.0
 * Author:      Hello Harel
 * License:     GPL-2.0-or-later
 *
 * POURQUOI CE PLUGIN
 * ------------------
 * Le formulaire de /contact/ envoyait depuis no-reply@helloharel.com, une
 * adresse que le site ne peut pas authentifier. Sans SMTP, WordPress tombe
 * sur la fonction mail() de PHP ; le SPF du domaine est en erreur et le
 * destinataire est sur Google Workspace, qui refuse. wp_mail() renvoyait
 * donc false — et l'endpoint du formulaire repond 500 dans ce cas, si bien
 * que le visiteur voyait une erreur alors que sa demande etait bien
 * enregistree. Corriger l'envoi repare les deux d'un coup.
 *
 * CE QU'IL NE FAIT PAS
 * --------------------
 * Il ne touche pas au snippet du formulaire, ni a l'endpoint hh/v1/lead qui
 * enregistre les demandes, ni au script d'attribution. Le tracking continue
 * de fonctionner exactement comme avant. Toutes les interventions passent
 * par des filtres WordPress et sont enveloppees : en cas de pepin, on
 * retombe sur le comportement d'origine plutot que de casser l'envoi.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

final class HH_Mailer {

	const OPT       = 'hh_mailer_options';
	const JOURNAL   = 'hh_mailer_journal';
	const JOURNAL_N = 40;

	/** Fenetre anti-doublon : deux fois le meme message en 10 min = une fois. */
	const DOUBLON_S = 600;

	private static $instance = null;

	public static function boot() {
		if ( null === self::$instance ) { self::$instance = new self(); }
		return self::$instance;
	}

	private function __construct() {
		add_action( 'phpmailer_init', array( $this, 'configurer_smtp' ) );
		add_filter( 'wp_mail_from', array( $this, 'expediteur' ), 99 );
		add_filter( 'wp_mail_from_name', array( $this, 'nom_expediteur' ), 99 );
		add_filter( 'wp_mail', array( $this, 'mettre_en_page' ), 99 );
		add_filter( 'pre_wp_mail', array( $this, 'ecarter_doublon' ), 99, 2 );
		add_action( 'wp_mail_succeeded', array( $this, 'noter_succes' ) );
		add_action( 'wp_mail_failed', array( $this, 'noter_echec' ) );
		add_action( 'admin_menu', array( $this, 'menu' ) );
		add_action( 'admin_init', array( $this, 'reglages' ) );
		add_action( 'admin_post_hh_mailer_test', array( $this, 'envoyer_un_test' ) );
	}

	/* ---------------------------------------------------------------- */
	/*  Reglages                                                         */
	/* ---------------------------------------------------------------- */

	public function opt( $cle, $defaut = '' ) {
		$o = get_option( self::OPT, array() );
		return ( is_array( $o ) && isset( $o[ $cle ] ) && '' !== $o[ $cle ] ) ? $o[ $cle ] : $defaut;
	}

	/**
	 * Le mot de passe d'application. Une constante de wp-config.php prime sur
	 * le reglage : c'est l'endroit le plus sur pour un secret, hors base de
	 * donnees et hors sauvegarde SQL.
	 */
	public function mot_de_passe() {
		if ( defined( 'HH_SMTP_PASS' ) && HH_SMTP_PASS ) { return HH_SMTP_PASS; }
		return $this->opt( 'pass' );
	}

	public function utilisateur() {
		if ( defined( 'HH_SMTP_USER' ) && HH_SMTP_USER ) { return HH_SMTP_USER; }
		return $this->opt( 'user' );
	}

	/* ---------------------------------------------------------------- */
	/*  SMTP                                                             */
	/* ---------------------------------------------------------------- */

	public function configurer_smtp( $phpmailer ) {
		try {
			$user = $this->utilisateur();
			$pass = $this->mot_de_passe();
			// Sans identifiants, on ne touche a rien : le site retombe sur son
			// comportement d'origine au lieu de partir en erreur.
			if ( ! $user || ! $pass ) { return; }

			$phpmailer->isSMTP();
			$phpmailer->Host        = $this->opt( 'host', 'smtp.gmail.com' );
			$phpmailer->Port        = (int) $this->opt( 'port', 587 );
			$phpmailer->SMTPAuth    = true;
			$phpmailer->SMTPSecure  = $this->opt( 'chiffrement', 'tls' );
			$phpmailer->Username    = $user;
			$phpmailer->Password    = $pass;
			$phpmailer->SMTPAutoTLS = true;
			$phpmailer->Timeout     = 20;
			$phpmailer->CharSet     = 'UTF-8';

			// Google reecrit l'expediteur s'il ne correspond pas au compte
			// authentifie. On le pose donc nous-memes, sinon le message part
			// avec une adresse qui ne passera pas les controles.
			$phpmailer->setFrom( $user, $this->opt( 'nom', 'Hello Harel — Site' ), false );
			$phpmailer->Sender = $user;   // enveloppe, pour le SPF
		} catch ( \Throwable $e ) {
			$this->journal( 'erreur', 'Configuration SMTP : ' . $e->getMessage() );
		}
	}

	public function expediteur( $courant ) {
		$user = $this->utilisateur();
		return ( $user && $this->mot_de_passe() ) ? $user : $courant;
	}

	public function nom_expediteur( $courant ) {
		return ( $this->utilisateur() && $this->mot_de_passe() )
			? $this->opt( 'nom', 'Hello Harel — Site' ) : $courant;
	}

	/* ---------------------------------------------------------------- */
	/*  Anti-doublon                                                     */
	/* ---------------------------------------------------------------- */

	/**
	 * Deux fois le meme message vers les memes destinataires en dix minutes :
	 * on n'envoie qu'une fois. On renvoie true et NON false — false ferait
	 * repondre 500 a l'endpoint du formulaire, et le visiteur verrait une
	 * erreur alors que sa demande est bien partie.
	 */
	public function ecarter_doublon( $court_circuit, $atts ) {
		if ( null !== $court_circuit ) { return $court_circuit; }
		try {
			$to   = isset( $atts['to'] ) ? $atts['to'] : '';
			$sujet = isset( $atts['subject'] ) ? $atts['subject'] : '';
			$corps = isset( $atts['message'] ) ? $atts['message'] : '';
			$cle  = 'hh_mail_' . md5( wp_json_encode( array( $to, $sujet, $corps ) ) );
			if ( get_transient( $cle ) ) {
				$this->journal( 'doublon', $sujet . ' — ecarte (deja envoye il y a moins de '
					. ( self::DOUBLON_S / 60 ) . ' min)' );
				return true;
			}
			set_transient( $cle, 1, self::DOUBLON_S );
		} catch ( \Throwable $e ) {
			$this->journal( 'erreur', 'Anti-doublon : ' . $e->getMessage() );
		}
		return $court_circuit;
	}

	/* ---------------------------------------------------------------- */
	/*  Mise en page                                                     */
	/* ---------------------------------------------------------------- */

	/**
	 * Les demandes de demo partent en texte brut depuis le snippet du
	 * formulaire. On les relit et on les remet en page aux couleurs Hello
	 * Harel, sans toucher au snippet. Si la lecture echoue, on laisse le
	 * message d'origine passer tel quel : mieux vaut un mail moche qu'un
	 * mail perdu.
	 */
	public function mettre_en_page( $atts ) {
		try {
			$sujet = isset( $atts['subject'] ) ? $atts['subject'] : '';
			if ( false === stripos( $sujet, 'demande de demo' ) ) { return $atts; }

			$entetes = isset( $atts['headers'] ) ? (array) $atts['headers'] : array();
			foreach ( $entetes as $h ) {
				if ( is_string( $h ) && false !== stripos( $h, 'text/html' ) ) { return $atts; }
			}

			$champs = $this->lire_corps( (string) $atts['message'] );
			if ( empty( $champs['lignes'] ) ) { return $atts; }

			$atts['message'] = $this->gabarit( $champs, $sujet );

			$garde = array();
			foreach ( $entetes as $h ) {
				if ( is_string( $h ) && 0 === stripos( ltrim( $h ), 'content-type:' ) ) { continue; }
				$garde[] = $h;
			}
			$garde[]          = 'Content-Type: text/html; charset=UTF-8';
			$atts['headers']  = $garde;
		} catch ( \Throwable $e ) {
			$this->journal( 'erreur', 'Mise en page : ' . $e->getMessage() );
		}
		return $atts;
	}

	/** Relit le corps « - Etiquette : valeur » produit par le formulaire. */
	private function lire_corps( $corps ) {
		$lignes  = array();
		$message = '';
		$attr    = array();
		$zone    = 'champs';
		foreach ( preg_split( "/\r\n|\n|\r/", $corps ) as $l ) {
			$t = trim( $l );
			if ( '' === $t ) { continue; }
			if ( 0 === strpos( $t, '- - - -' ) ) { $zone = 'fin'; continue; }
			if ( 'Attribution :' === $t ) { $zone = 'attr'; continue; }
			if ( '- Message :' === $t ) { $zone = 'message'; continue; }

			if ( 'champs' === $zone && preg_match( '/^-\s*([^:]+?)\s*:\s*(.*)$/u', $t, $m ) ) {
				$lignes[ trim( $m[1] ) ] = trim( $m[2] );
			} elseif ( 'message' === $zone ) {
				if ( preg_match( '/^-\s*([^:]+?)\s*:\s*(.*)$/u', $t, $m ) ) {
					$lignes[ trim( $m[1] ) ] = trim( $m[2] ); $zone = 'champs'; continue;
				}
				$message .= ( $message ? "\n" : '' ) . $t;
			} elseif ( 'attr' === $zone && preg_match( '/^([a-z]+)\s*:\s*(.*)$/i', $t, $m ) ) {
				$attr[ trim( $m[1] ) ] = trim( $m[2] );
			}
		}
		return array( 'lignes' => $lignes, 'message' => $message, 'attribution' => $attr );
	}

	private function gabarit( $c, $sujet ) {
		$BLEU = '#00B1F5'; $ENCRE = '#0f172a'; $GRIS = '#475569'; $BORD = '#e2e8f0';
		$e = function ( $v ) { return esc_html( $v ); };

		// Le formulaire ecrit ses etiquettes sans accents. Elles arrivent a
		// l'ecran d'un humain : on les lui rend.
		$accents = array(
			'Societe'   => 'Société',
			'Telephone' => 'Téléphone',
			'Email'     => 'E-mail',
		);

		$rangs = '';
		foreach ( $c['lignes'] as $cle => $val ) {
			if ( '' === $val ) { continue; }
			$etiquette = isset( $accents[ $cle ] ) ? $accents[ $cle ] : $cle;
			$v = $e( $val );
			if ( 0 === strcasecmp( $cle, 'Email' ) ) {
				$v = '<a href="mailto:' . esc_attr( $val ) . '" style="color:#0369A1;">' . $v . '</a>';
			} elseif ( 0 === strcasecmp( $cle, 'Telephone' ) && '(non renseigne)' !== $val ) {
				$v = '<a href="tel:' . esc_attr( preg_replace( '/[^0-9+]/', '', $val ) )
					. '" style="color:#0369A1;">' . $v . '</a>';
			}
			$rangs .= '<tr>'
				. '<td style="padding:11px 0;border-bottom:1px solid ' . $BORD . ';color:' . $GRIS
				. ';font-size:13px;width:34%;vertical-align:top;">' . $e( $etiquette ) . '</td>'
				. '<td style="padding:11px 0;border-bottom:1px solid ' . $BORD . ';color:' . $ENCRE
				. ';font-size:15px;font-weight:600;vertical-align:top;">' . $v . '</td></tr>';
		}

		$bloc_message = '';
		if ( '' !== $c['message'] && '(aucun)' !== $c['message'] ) {
			$bloc_message = '<div style="margin:22px 0 0;padding:16px 18px;background:#F8FAFC;'
				. 'border-left:3px solid ' . $BLEU . ';border-radius:0 10px 10px 0;">'
				. '<div style="color:' . $GRIS . ';font-size:12px;text-transform:uppercase;'
				. 'letter-spacing:.09em;font-weight:700;margin-bottom:7px;">Message</div>'
				. '<div style="color:' . $ENCRE . ';font-size:15px;line-height:1.65;">'
				. nl2br( $e( $c['message'] ) ) . '</div></div>';
		}

		$bloc_attr = '';
		if ( ! empty( $c['attribution'] ) ) {
			$li = '';
			foreach ( $c['attribution'] as $k => $v ) {
				if ( '' === $v || 'n/a' === $v ) { continue; }
				$li .= '<tr><td style="padding:4px 14px 4px 0;color:#94a3b8;font-size:12px;">'
					. $e( $k ) . '</td><td style="padding:4px 0;color:' . $GRIS
					. ';font-size:12px;word-break:break-all;">' . $e( $v ) . '</td></tr>';
			}
			if ( $li ) {
				$bloc_attr = '<div style="margin:22px 0 0;padding-top:16px;border-top:1px solid '
					. $BORD . ';"><div style="color:#94a3b8;font-size:11px;text-transform:uppercase;'
					. 'letter-spacing:.09em;font-weight:700;margin-bottom:8px;">D\'où vient cette demande</div>'
					. '<table cellpadding="0" cellspacing="0" border="0" style="width:100%;">'
					. $li . '</table></div>';
			}
		}

		$titre = isset( $c['lignes']['Societe'] ) && $c['lignes']['Societe']
			? $c['lignes']['Societe']
			: ( isset( $c['lignes']['Nom'] ) ? $c['lignes']['Nom'] : 'Nouvelle demande' );

		return '<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">'
			. '<meta name="viewport" content="width=device-width,initial-scale=1">'
			. '<title>' . $e( $sujet ) . '</title></head>'
			. '<body style="margin:0;padding:0;background:#EEF2F7;">'
			. '<div style="display:none;max-height:0;overflow:hidden;opacity:0;">'
			. $e( $titre ) . ' vient de demander une démo depuis helloharel.com</div>'
			. '<table cellpadding="0" cellspacing="0" border="0" style="width:100%;background:#EEF2F7;">'
			. '<tr><td align="center" style="padding:26px 14px;">'
			. '<table cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:580px;'
			. 'background:#ffffff;border-radius:16px;overflow:hidden;'
			. 'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;'
			. 'box-shadow:0 18px 40px -30px rgba(15,23,42,.55);">'
			// bandeau
			. '<tr><td style="background:' . $BLEU . ';padding:20px 26px;">'
			. '<div style="color:#ffffff;font-size:12px;letter-spacing:.14em;text-transform:uppercase;'
			. 'font-weight:700;opacity:.92;">Hello Harel</div>'
			. '<div style="color:#ffffff;font-size:20px;font-weight:800;margin-top:4px;">'
			. 'Nouvelle demande de démo</div></td></tr>'
			// corps
			. '<tr><td style="padding:24px 26px 28px;">'
			. '<div style="color:' . $ENCRE . ';font-size:18px;font-weight:800;margin:0 0 4px;">'
			. $e( $titre ) . '</div>'
			. '<div style="color:#94a3b8;font-size:13px;margin:0 0 18px;">Reçue le '
			. $e( date_i18n( 'd/m/Y \a H\hi' ) ) . '</div>'
			. '<table cellpadding="0" cellspacing="0" border="0" style="width:100%;">' . $rangs . '</table>'
			. $bloc_message . $bloc_attr
			. ( isset( $c['lignes']['Email'] ) && $c['lignes']['Email']
				? '<div style="margin:26px 0 0;"><a href="mailto:'
					. esc_attr( $c['lignes']['Email'] ) . '" style="display:inline-block;'
					. 'background:#0369A1;color:#ffffff;text-decoration:none;font-weight:700;'
					. 'font-size:15px;padding:13px 26px;border-radius:999px;">Répondre à '
					. $e( isset( $c['lignes']['Nom'] ) ? $c['lignes']['Nom'] : 'la demande' )
					. '</a></div>'
				: '' )
			. '</td></tr>'
			// pied
			. '<tr><td style="padding:16px 26px 22px;border-top:1px solid ' . $BORD . ';'
			. 'color:#94a3b8;font-size:12px;line-height:1.6;">'
			. 'Message automatique du formulaire de <a href="https://www.helloharel.com/contact/" '
			. 'style="color:#0369A1;text-decoration:none;">helloharel.com/contact/</a>. '
			. 'Répondre à ce mail écrit directement au prospect.'
			. '</td></tr></table></td></tr></table></body></html>';
	}

	/* ---------------------------------------------------------------- */
	/*  Journal                                                          */
	/* ---------------------------------------------------------------- */

	public function journal( $etat, $texte ) {
		try {
			$j = get_option( self::JOURNAL, array() );
			if ( ! is_array( $j ) ) { $j = array(); }
			array_unshift( $j, array(
				'quand' => current_time( 'mysql' ),
				'etat'  => $etat,
				'texte' => (string) $texte,
			) );
			update_option( self::JOURNAL, array_slice( $j, 0, self::JOURNAL_N ), false );
		} catch ( \Throwable $e ) { /* le journal ne doit jamais faire echouer un envoi */ }
	}

	public function noter_succes( $atts ) {
		$to = isset( $atts['to'] ) ? ( is_array( $atts['to'] ) ? implode( ', ', $atts['to'] ) : $atts['to'] ) : '?';
		$this->journal( 'ok', ( isset( $atts['subject'] ) ? $atts['subject'] : '(sans objet)' ) . ' -> ' . $to );
	}

	public function noter_echec( $erreur ) {
		$msg = is_wp_error( $erreur ) ? $erreur->get_error_message() : 'echec inconnu';
		$this->journal( 'echec', $msg );
	}

	/* ---------------------------------------------------------------- */
	/*  Ecran d'administration                                           */
	/* ---------------------------------------------------------------- */

	public function menu() {
		add_submenu_page( 'options-general.php', 'Hello Harel — Mailer', 'HH Mailer',
			'manage_options', 'hh-mailer', array( $this, 'ecran' ) );
	}

	public function reglages() {
		register_setting( 'hh_mailer', self::OPT, array( 'sanitize_callback' => array( $this, 'nettoyer' ) ) );
	}

	public function nettoyer( $v ) {
		$a   = get_option( self::OPT, array() );
		if ( ! is_array( $a ) ) { $a = array(); }
		$out = array(
			'host'        => isset( $v['host'] ) ? sanitize_text_field( $v['host'] ) : 'smtp.gmail.com',
			'port'        => isset( $v['port'] ) ? (int) $v['port'] : 587,
			'chiffrement' => ( isset( $v['chiffrement'] ) && 'ssl' === $v['chiffrement'] ) ? 'ssl' : 'tls',
			'user'        => isset( $v['user'] ) ? sanitize_email( $v['user'] ) : '',
			'nom'         => isset( $v['nom'] ) ? sanitize_text_field( $v['nom'] ) : 'Hello Harel — Site',
		);
		// Un champ laisse vide ne remplace pas le mot de passe deja en place.
		$nouveau = isset( $v['pass'] ) ? trim( (string) $v['pass'] ) : '';
		$out['pass'] = ( '' !== $nouveau ) ? str_replace( ' ', '', $nouveau )
			: ( isset( $a['pass'] ) ? $a['pass'] : '' );
		return $out;
	}

	public function envoyer_un_test() {
		if ( ! current_user_can( 'manage_options' ) ) { wp_die( 'Acces refuse' ); }
		check_admin_referer( 'hh_mailer_test' );
		$a = isset( $_POST['dest'] ) ? sanitize_email( wp_unslash( $_POST['dest'] ) ) : '';
		if ( ! is_email( $a ) ) { $a = get_option( 'admin_email' ); }
		$ok = wp_mail( $a, 'Demande de demo - Test Hello Harel',
			implode( "\n", array(
				'Bonjour,', '', 'Nouvelle demande depuis helloharel.com/contact/ :', '',
				'- Nom : Essai de configuration',
				'- Email : ' . $a,
				'- Societe : Hello Harel',
				'- Telephone : (non renseigne)',
				'- Secteur : Test',
				'', '- Message :',
				"Si vous lisez ceci, l'envoi SMTP fonctionne.",
				'', '- - - - - - -', 'Attribution :',
				'  source : test', '  medium : admin', '  campaign : n/a', '  landing : n/a',
			) ),
			array( 'Content-Type: text/plain; charset=UTF-8' ) );
		wp_safe_redirect( add_query_arg( array( 'page' => 'hh-mailer', 'test' => $ok ? 'ok' : 'ko' ),
			admin_url( 'options-general.php' ) ) );
		exit;
	}

	public function ecran() {
		$par_constante = defined( 'HH_SMTP_PASS' ) && HH_SMTP_PASS;
		$pret          = $this->utilisateur() && $this->mot_de_passe();
		?>
		<div class="wrap">
			<h1>Hello Harel — Mailer</h1>

			<?php if ( isset( $_GET['test'] ) ) : ?>
				<div class="notice notice-<?php echo 'ok' === $_GET['test'] ? 'success' : 'error'; ?>"><p>
					<?php echo 'ok' === $_GET['test']
						? 'Test parti. Regardez la boite de reception — et le journal ci-dessous.'
						: 'Le test a echoue. Le motif exact est dans le journal, en bas.'; ?>
				</p></div>
			<?php endif; ?>

			<div class="notice notice-<?php echo $pret ? 'success' : 'warning'; ?> inline"><p>
				<?php echo $pret
					? '<strong>SMTP actif.</strong> Les mails partent par le serveur configure ci-dessous.'
					: '<strong>SMTP inactif.</strong> Tant qu\'il manque l\'identifiant ou le mot de passe, le site envoie comme avant — et les mails continuent de ne pas arriver.'; ?>
			</p></div>

			<form method="post" action="options.php">
				<?php settings_fields( 'hh_mailer' ); $o = get_option( self::OPT, array() ); ?>
				<table class="form-table" role="presentation">
					<tr><th scope="row"><label for="u">Compte expediteur</label></th>
						<td><input name="<?php echo self::OPT; ?>[user]" id="u" type="email" class="regular-text"
							value="<?php echo esc_attr( isset( $o['user'] ) ? $o['user'] : '' ); ?>"
							placeholder="administration@remi-oravec.fr">
						<p class="description">Le compte Google Workspace qui envoie. C'est aussi l'adresse qui s'affichera : Google reecrit toute autre valeur.</p></td></tr>

					<tr><th scope="row"><label for="p">Mot de passe d'application</label></th>
						<td>
						<?php if ( $par_constante ) : ?>
							<p><code>HH_SMTP_PASS</code> est definie dans <code>wp-config.php</code> — c'est elle qui sert, et ce champ est ignore.</p>
						<?php else : ?>
							<input name="<?php echo self::OPT; ?>[pass]" id="p" type="password" class="regular-text"
								value="" autocomplete="new-password"
								placeholder="<?php echo $this->opt( 'pass' ) ? '•••••••• (enregistre)' : 'xxxx xxxx xxxx xxxx'; ?>">
							<p class="description">
								Genere sur <a href="https://myaccount.google.com/apppasswords" target="_blank" rel="noopener">myaccount.google.com/apppasswords</a>.
								Les espaces sont retires automatiquement. Laisser vide conserve le mot de passe deja enregistre.<br>
								Plus sur : le poser dans <code>wp-config.php</code> avec
								<code>define('HH_SMTP_PASS', '...');</code> — il reste alors hors de la base et hors des sauvegardes SQL.
							</p>
						<?php endif; ?>
						</td></tr>

					<tr><th scope="row"><label for="n">Nom affiche</label></th>
						<td><input name="<?php echo self::OPT; ?>[nom]" id="n" type="text" class="regular-text"
							value="<?php echo esc_attr( $this->opt( 'nom', 'Hello Harel — Site' ) ); ?>"></td></tr>

					<tr><th scope="row">Serveur</th><td>
						<input name="<?php echo self::OPT; ?>[host]" type="text"
							value="<?php echo esc_attr( $this->opt( 'host', 'smtp.gmail.com' ) ); ?>" size="24">
						port <input name="<?php echo self::OPT; ?>[port]" type="number"
							value="<?php echo esc_attr( $this->opt( 'port', 587 ) ); ?>" size="5" style="width:6em">
						<select name="<?php echo self::OPT; ?>[chiffrement]">
							<option value="tls" <?php selected( $this->opt( 'chiffrement', 'tls' ), 'tls' ); ?>>TLS (587)</option>
							<option value="ssl" <?php selected( $this->opt( 'chiffrement', 'tls' ), 'ssl' ); ?>>SSL (465)</option>
						</select></td></tr>
				</table>
				<?php submit_button( 'Enregistrer' ); ?>
			</form>

			<hr>
			<h2>Envoyer un test</h2>
			<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
				<input type="hidden" name="action" value="hh_mailer_test">
				<?php wp_nonce_field( 'hh_mailer_test' ); ?>
				<input type="email" name="dest" class="regular-text"
					value="<?php echo esc_attr( get_option( 'admin_email' ) ); ?>">
				<?php submit_button( 'Envoyer le test', 'secondary', 'submit', false ); ?>
				<p class="description">Le test emprunte exactement le chemin d'une vraie demande, mise en page comprise.</p>
			</form>

			<hr>
			<h2>Journal des <?php echo (int) self::JOURNAL_N; ?> derniers evenements</h2>
			<?php $j = get_option( self::JOURNAL, array() ); if ( empty( $j ) ) : ?>
				<p>Rien pour l'instant.</p>
			<?php else : ?>
				<table class="widefat striped"><thead><tr>
					<th style="width:160px">Quand</th><th style="width:90px">Etat</th><th>Detail</th>
				</tr></thead><tbody>
				<?php foreach ( $j as $l ) :
					$c = array( 'ok' => '#15803d', 'echec' => '#b91c1c',
						'doublon' => '#b45309', 'erreur' => '#b91c1c' );
					$couleur = isset( $c[ $l['etat'] ] ) ? $c[ $l['etat'] ] : '#475569'; ?>
					<tr><td><?php echo esc_html( $l['quand'] ); ?></td>
						<td><strong style="color:<?php echo esc_attr( $couleur ); ?>">
							<?php echo esc_html( $l['etat'] ); ?></strong></td>
						<td><?php echo esc_html( $l['texte'] ); ?></td></tr>
				<?php endforeach; ?>
				</tbody></table>
			<?php endif; ?>
		</div>
		<?php
	}
}

HH_Mailer::boot();
