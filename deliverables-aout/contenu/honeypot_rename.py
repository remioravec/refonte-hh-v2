# -*- coding: utf-8 -*-
"""Renomme le champ honeypot « website » — que les navigateurs remplissent tout seuls —
en un nom opaque « hh_zc7 ».

Tant qu'il s'appelait « website », un remplissage automatique du navigateur faisait
repondre un faux succes au visiteur, sans envoyer le mail ni enregistrer le lead.

Le renommage ne peut pas bloquer un envoi : quel que soit l'ordre d'application,
un cote cherche un champ que l'autre n'envoie plus, donc le piege ne se declenche
jamais a tort. Au pire on perd temporairement la protection anti-bot, jamais un lead.

Usage : python3 honeypot_rename.py [serveur|page|test_on|test_off|etat]
"""
import json, os, re, sys, base64, urllib.request

ANCIEN, NOUVEAU = "website", "hh_zc7"
SAUVE = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
TOK = base64.b64encode(
    f"{os.environ['WP_USER']}:{os.environ['WP_PASS']}".encode()).decode()

def req(path, method="GET", data=None):
    r = urllib.request.Request(f"https://www.helloharel.com/wp-json/{path}",
        data=json.dumps(data).encode() if data else None, method=method)
    r.add_header("Authorization", "Basic " + TOK)
    r.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(r, timeout=120).read())

def snippet(code=None):
    if code is None: return req("code-snippets/v1/snippets/6")["code"]
    req("code-snippets/v1/snippets/6", "POST", {"code": code, "active": True})

# --- le serveur : deux pieges, tous deux sur « website »
SRV = [
    ("if ( ! empty( $params['website'] ) ) {",
     "if ( ! empty( $params['%s'] ) ) {" % NOUVEAU, 1),
    ("if (!empty($p['website']) || !empty($p['_honey']))",
     "if (!empty($p['%s']) || !empty($p['_honey']))" % NOUVEAU, 1),
]
# --- la page : champ, label, commentaire, test JS. Le JSON-LD « WebSite » ne bouge pas.
PAGE = [
    ('<label for="hh-hp-website">Laissez ce champ vide (anti-spam)</label>',
     '<label for="hh-hp-%s">Laissez ce champ vide (anti-spam)</label>' % NOUVEAU, 1),
    ('<input type="text" id="hh-hp-website" name="website" tabindex="-1" autocomplete="new-password" value="">',
     '<input type="text" id="hh-hp-%s" name="%s" tabindex="-1" autocomplete="off" '
     'aria-hidden="true" value="">' % (NOUVEAU, NOUVEAU), 1),
    ("if (v('website'))", "if (v('%s'))" % NOUVEAU, 1),
    ('honeypot "website" (non reserve formsubmit). Les bots remplissent ce nom classique, JS bloque l\'envoi.',
     'honeypot "%s" : nom opaque, volontairement hors des listes de remplissage '
     'automatique des navigateurs. Un nom parlant comme "website" etait rempli tout '
     'seul et faisait perdre la demande.' % NOUVEAU, 1),
]

def applique(txte, regles, quoi):
    for vieux, neuf, att in regles:
        n = txte.count(vieux)
        if n != att:
            print(f"ABANDON [{quoi}] — « {vieux[:58]}… » trouve {n} fois, attendu {att}")
            sys.exit(1)
        txte = txte.replace(vieux, neuf)
        print(f"  OK  « {vieux[:62]}… »")
    return txte

def etat():
    c = snippet()
    import wp_common as w
    p = w.api("pages/661?context=edit&_fields=content")["content"]["raw"]
    mode = re.search(r"define\( 'HH_LEADS_TEST', (\w+) \)", c)
    q = chr(34)
    nb_srv = c.count("['website']")
    nb_nom = p.count('name=' + q + 'website' + q)
    nb_new = p.count('name=' + q + NOUVEAU + q)
    nb_js  = p.count("v('website')")
    print("snippet 6 : pieges sur website x%d · %s x%d · mode test = %s"
          % (nb_srv, NOUVEAU, c.count(NOUVEAU), mode.group(1) if mode else "?"))
    print("page 661  : name=website x%d · name=%s x%d · test JS sur website x%d"
          % (nb_nom, NOUVEAU, nb_new, nb_js))

def main():
    quoi = sys.argv[1] if len(sys.argv) > 1 else "etat"
    if quoi == "etat": return etat()

    if quoi in ("test_on", "test_off"):
        c = snippet(); val = "true" if quoi == "test_on" else "false"
        autre = "false" if quoi == "test_on" else "true"
        vieux = f"define( 'HH_LEADS_TEST', {autre} )"
        if vieux not in c:
            print(f"deja en {val} — rien a faire"); return
        snippet(c.replace(vieux, f"define( 'HH_LEADS_TEST', {val} )", 1))
        print(f"mode test -> {val}"
              f"{'  (les mails partent chez Remi seul)' if val=='true' else '  (diffusion normale retablie)'}")
        return

    if quoi == "serveur":
        c = snippet(); open(f"{SAUVE}/snippet6-avant.php", "w").write(c)
        n = applique(c, SRV, "serveur")
        assert "$params['website']" not in n and "$p['website']" not in n
        avant_mode = re.search(r"define\( 'HH_LEADS_TEST', (\w+) \)", c).group(1)
        apres_mode = re.search(r"define\( 'HH_LEADS_TEST', (\w+) \)", n).group(1)
        assert avant_mode == apres_mode, "le mode de diffusion a bouge"
        assert n.count("'ndecerner@gmail.com'") == 1, "le destinataire a bouge"
        snippet(n); print(f"snippet 6 enregistre — {len(c)} -> {len(n)} o")
        return

    if quoi == "page":
        import wp_common as w
        p = w.api("pages/661?context=edit&_fields=content")["content"]["raw"]
        open(f"{SAUVE}/661-avant.html", "w").write(p)
        n = applique(p, PAGE, "page")
        assert 'name="website"' not in n, "le champ porte encore l'ancien nom"
        assert n.count('"@type": "WebSite"') == p.count('"@type": "WebSite"'), "le JSON-LD a bouge"
        assert len(n) < max(400_000, len(p))
        w.api("pages/661", method="POST", data={"content": n})
        print(f"page 661 enregistree — {len(p)} -> {len(n)} o")
        return

    print("usage : serveur | page | test_on | test_off | etat")

if __name__ == "__main__":
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "maillage-cro"))
    main()
