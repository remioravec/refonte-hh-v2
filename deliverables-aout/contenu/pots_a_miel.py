#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pots a miel multiples sur les deux formulaires du site.

CE QUE MONTRE LA MESURE DU 16/09/2026
=====================================
Le site a DEUX points d'entree, et c'est la tout le sujet :
  · hh/v1/contact ... envoie le mail ;
  · hh/v1/lead ..... enregistre la demande, appele par un script du pied de
    page, donc uniquement quand un VRAI navigateur execute le JavaScript.

Releve : le magasin de demandes contient 71 entrees et PAS UNE en cyrillique,
alors que la boite mail deborde d'envois en russe. Les deux ne peuvent etre
vrais que si les envois en russe n'executent jamais le JavaScript du site :
ils tapent directement /wp-json/hh/v1/contact.

CONSEQUENCE A DIRE FRANCHEMENT — un pot a miel ne piege que ce qui LIT le
formulaire. Contre un robot qui poste en direct, il ne peut rien : le champ
n'existe pas dans sa requete, donc il est vide, donc il passe. Les pots a miel
poses ici arretent les robots qui remplissent la page ; ils n'arreteront pas
celui-la. Ce qui l'arrete est cote serveur, et c'est livre a part.

CE QUE FAIT CE SCRIPT — cote client, sur les deux formulaires :
  1. trois pots a miel au lieu d'un, aux noms que les robots remplissent le
     plus volontiers : website, url, email_confirm ;
  2. le controle d'envoi refuse si l'un des trois est rempli ;
  3. sur /migration-as400/ : la garde temporelle, qui n'existait pas ;
  4. sur /migration-as400/ : correction d'un defaut reel — la charge envoyee
     contenait « website:"" » en dur. Le pot a miel de ce formulaire etait
     donc neutralise avant meme d'arriver au serveur.

Les champs sont hors du flux, hors de la navigation au clavier, hors de
l'autocompletion, et marques aria-hidden : invisibles pour un humain comme
pour un lecteur d'ecran.

Usage :  python3 pots_a_miel.py            (essai a blanc)
         python3 pots_a_miel.py --live     (ecriture)
"""

import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"

# ============================================================ /contact/ (661)
C_HP_AV = ('                        <input type="text" id="hh-hp-website" name="website" '
           'tabindex="-1" autocomplete="off" value="">\n')
C_HP_AP = (C_HP_AV
           + '                        <label for="hh-hp-url">Laissez ce champ vide '
             '(anti-spam)</label>\n'
             '                        <input type="text" id="hh-hp-url" name="url" '
             'tabindex="-1" autocomplete="off" value="">\n'
             '                        <label for="hh-hp-confirm">Laissez ce champ vide '
             '(anti-spam)</label>\n'
             '                        <input type="email" id="hh-hp-confirm" '
             'name="email_confirm" tabindex="-1" autocomplete="off" value="">\n')

C_CTRL_AV = "  if (v('website')) {"
C_CTRL_AP = "  if (v('website') || v('url') || v('email_confirm')) {"

# ==================================================== /migration-as400/ (11162)
M_HP_AV = ('<input type="text" name="website" tabindex="-1" autocomplete="off" '
           'style="position:absolute;left:-9999px" aria-hidden="true">')
M_HP_AP = ('<div aria-hidden="true" style="position:absolute;left:-9999px;top:-9999px;'
           'width:1px;height:1px;overflow:hidden;opacity:0;pointer-events:none">'
           '<label for="hh-mig-hp1">Laissez ce champ vide (anti-spam)</label>'
           '<input type="text" id="hh-mig-hp1" name="website" tabindex="-1" '
           'autocomplete="off" value="">'
           '<label for="hh-mig-hp2">Laissez ce champ vide (anti-spam)</label>'
           '<input type="text" id="hh-mig-hp2" name="url" tabindex="-1" '
           'autocomplete="off" value="">'
           '<label for="hh-mig-hp3">Laissez ce champ vide (anti-spam)</label>'
           '<input type="email" id="hh-mig-hp3" name="email_confirm" tabindex="-1" '
           'autocomplete="off" value="">'
           '</div>'
           '<input type="hidden" name="loaded_at" id="hh-mig-loaded" value="0">')

M_CTRL_AV = ' if(val("website")){return false;}'
M_CTRL_AP = (' if(val("website")||val("url")||val("email_confirm")){'
             'btn.disabled=true;btn.textContent="Envoyé";return false;}\n'
             ' var migT=parseInt(val("loaded_at")||"0",10);'
             'if(migT>0&&Date.now()-migT<2000){'
             'show("#fee2e2","#991b1b","Merci de prendre un instant pour relire votre '
             'demande avant de l\'envoyer.");return false;}')

M_CHARGE_AV = 'te_landing:fp(),te_source:"migration-as400",website:""};'
M_CHARGE_AP = ('te_landing:fp(),te_source:"migration-as400",'
               'website:val("website"),url:val("url"),email_confirm:val("email_confirm"),'
               'loaded_at:val("loaded_at")};')

M_HORODATE_AV = '</form>'
M_HORODATE_AP = ('</form>\n<script>(function(){var e=document.getElementById("hh-mig-loaded");'
                 'if(e){e.value=Date.now();}})();</script>')


def patcher(page, edits, doivent_survivre):
    p = w.get_raw("pages", page)
    c = p["content"]["raw"]
    el = (p.get("meta", {}).get("_elementor_data") or "").strip()
    if el not in ("", "[]", "[ ]", "null"):
        raise SystemExit("ARRET — page %d : donnees Elementor (%d octets)" % (page, len(el)))

    n, faits, pb = c, [], []
    for quoi, av, ap in edits:
        if n.count(av) != 1:
            pb.append("%s : ancre trouvee %d fois, attendu 1" % (quoi, n.count(av)))
            continue
        n = n.replace(av, ap, 1)
        faits.append(quoi)

    for quoi in doivent_survivre:
        if n.count(quoi) < 1:
            pb.append("perdu au montage : %s" % quoi)
    for quoi in ("<h1", "hero-section", "<form"):
        if n.count(quoi) != c.count(quoi):
            pb.append("structure : %s a change de compte" % quoi)
    if len(n) < len(c):
        pb.append("la page a maigri de %d octets" % (len(c) - len(n)))

    print("\npage %d — %d -> %d octets" % (page, len(c), len(n)))
    for f in faits:
        print("  · %s" % f)
    for x in pb:
        print("  ! %s" % x)
    if pb:
        raise SystemExit("ARRET — rien n'est ecrit tant qu'un controle est rouge")

    open("%s/pots-%d-avant.html" % (S, page), "w", encoding="utf-8").write(c)
    open("%s/pots-%d-apres.html" % (S, page), "w", encoding="utf-8").write(n)
    if not LIVE:
        print("  essai a blanc — rien n'est ecrit")
        return
    w.api("pages/%d" % page, "POST", {"content": n})
    c2 = w.get_raw("pages", page)["content"]["raw"]
    print("  relecture : %s" % ("en place" if 'name="email_confirm"' in c2 else "ECHEC"))


def main():
    patcher(661,
            [("deux pots a miel supplementaires", C_HP_AV, C_HP_AP),
             ("controle etendu aux trois pots", C_CTRL_AV, C_CTRL_AP)],
            ["submitContactForm", "hh/v1/contact", 'name="phone"', "generate_lead",
             'name="website"', 'name="url"', 'name="email_confirm"'])

    patcher(11162,
            [("trois pots a miel et champ d'horodatage", M_HP_AV, M_HP_AP),
             ("controle etendu et garde temporelle", M_CTRL_AV, M_CTRL_AP),
             ("pots a miel reellement transmis au serveur", M_CHARGE_AV, M_CHARGE_AP),
             ("horodatage pose au chargement", M_HORODATE_AV, M_HORODATE_AP)],
            ["hhMigSubmit", "hh/v1/contact", 'id="hh-mig-tel"', 'name="AS400"',
             'name="website"', 'name="url"', 'name="email_confirm"'])

    if LIVE:
        for u in ("/contact/", "/migration-as400/"):
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                                "https://www.helloharel.com" + u],
                               capture_output=True, text=True)
            print("%s -> HTTP %s" % (u, r.stdout.strip()))
    else:
        print("\nessai a blanc termine. Relancer avec --live.")


if __name__ == "__main__":
    main()
