#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le formulaire ne partait pas : son piege a robots attrapait les humains.

Le journal de l'extension est formel. Un test envoye depuis l'extension
passe a 08:51:25. Une demande deposee par le formulaire a 08:52:41 est
enregistree dans WordPress — et le journal n'en porte aucune trace. Le
message n'a donc jamais atteint wp_mail() : quelque chose l'a arrete
avant.

Ce quelque chose est le piege a robots. Il posait trois champs caches :

    <input type="text"  name="website">
    <input type="text"  name="url">
    <input type="email" name="email_confirm">     <-- celui-la

Le troisieme est declare en type « email ». Les navigateurs remplissent
ces champs-la tout seuls, et ils le font meme avec autocomplete="off" —
la consigne est traitee comme une suggestion depuis longtemps. Le
visiteur remplit son adresse en haut du formulaire, le navigateur la
recopie dans le champ cache, et le script conclut qu'il a affaire a un
robot.

Le pire est ce qu'il fait ensuite : il affiche « Merci ! Notre equipe
vous recontactera sous 24h » et n'envoie rien. C'est le comportement
voulu face a un robot — ne pas lui dire qu'il est repere. Face a un
client, c'est une demande perdue sans que personne le sache.

On retire les deux champs que les navigateurs convoitent — « email_confirm »
et « url » — et on garde « website », que le serveur controle de son cote
et qu'aucun navigateur ne remplit d'une adresse. Il passe en
autocomplete="new-password", la seule valeur que les navigateurs
respectent vraiment.

Usage :  python3 reparer_piege.py           (blanc)
         python3 reparer_piege.py --poser   (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

# Les deux pages qui portent un formulaire, et le meme piege.
# /migration-as400/ est sous Regle 0 : on ne la touche que pour reparer un
# defaut, et un formulaire qui perd les demandes en est un.
PAGES = ((661, "/contact/"), (11162, "/migration-as400/"))
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/piege-avant")

# Le source est indente et va a la ligne : on vise chaque element, pas un
# bloc litteral recopie a l'espace pres.
A_RETIRER = (
    (r'<label for="hh-[\w-]*hp[\w-]*\d?">[^<]*</label>\s*'
     r'<input[^>]*name="url"[^>]*>\s*', "piege « url »"),
    (r'<label for="hh-[\w-]*hp[\w-]*\d?">[^<]*</label>\s*'
     r'<input[^>]*name="email_confirm"[^>]*>\s*', "piege « email_confirm »"),
)
DURCIR = (r'(<input[^>]*name="website"[^>]*)autocomplete="off"',
          r'\1autocomplete="new-password"')

# Les deux formulaires ecrivent le meme controle, avec des noms de fonction
# differents. On vise la condition, pas la ligne entiere.
JS = ((r"v\('website'\) \|\| v\('url'\) \|\| v\('email_confirm'\)", "v('website')"),
      (r'val\("website"\)\|\|val\("url"\)\|\|val\("email_confirm"\)', 'val("website")'))
# Le formulaire de migration recopie aussi les trois pieges dans ce qu'il
# envoie au serveur. Les deux retires n'ont plus de champ : on retire les
# cles plutot que de laisser des references a des champs disparus.
CHARGE = (r',url:val\("url"\),email_confirm:val\("email_confirm"\)', "")


def traiter(PID, URL, poser):
    c = w.get_raw("pages", PID)["content"]["raw"]
    depart = c
    notes = []

    if "email_confirm" not in c:
        print("%-46s deja repare" % URL[:46])
        return
    for motif, quoi in A_RETIRER:
        c, n = re.subn(motif, "", c, flags=re.S)
        if n != 1:
            raise SystemExit("ARRET — %d occurrence(s) du %s" % (n, quoi))
        notes.append(quoi + " retire")
    c, n = re.subn(DURCIR[0], DURCIR[1], c)
    if n != 1:
        raise SystemExit("ARRET — %d champ « website » a durcir" % n)
    notes.append("website en autocomplete=new-password")
    c, _ = re.subn(CHARGE[0], CHARGE[1], c)
    total = 0
    for motif, apres in JS:
        c, n = re.subn(motif, apres, c)
        total += n
    if total != 1:
        raise SystemExit("ARRET — %d controle(s) JavaScript trouve(s)" % total)
    notes.append("controle JavaScript resserre")

    # ── controles ────────────────────────────────────────────────────────
    for mort in ('name="email_confirm"', 'name="url"', "email_confirm"):
        if mort in c:
            raise SystemExit("ARRET — « %s » est encore la" % mort)
    if 'name="website"' not in c:
        raise SystemExit("ARRET — le piege a disparu en entier")
    # L'enveloppe n'a pas le meme nom d'un formulaire a l'autre : on
    # verifie qu'il reste exactement un piege, et qu'il est toujours cache.
    if len(re.findall(r'name="website"', c)) != 1:
        raise SystemExit("ARRET — %d piege(s) « website » au lieu d'un"
                         % len(re.findall(r'name="website"', c)))
    m2 = re.search(r'<div[^>]*>(?:(?!</div>).)*?name="website"', c, re.S)
    if not m2 or "-9999px" not in m2.group(0):
        raise SystemExit("ARRET — le piege n'est plus hors champ")
    for garde in ('name="loaded_at"', "wp-json/hh/v1/contact", "<form"):
        if garde not in c:
            raise SystemExit("ARRET — %s a disparu" % garde)
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge")
    if D.liens(c) != D.liens(depart):
        raise SystemExit("ARRET — les liens bougent")
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge")
    avant_champs = len(re.findall(r"<(?:input|select|textarea)\b", depart))
    apres_champs = len(re.findall(r"<(?:input|select|textarea)\b", c))
    if apres_champs != avant_champs - 2:
        raise SystemExit("ARRET — %d champs au lieu de %d"
                         % (apres_champs, avant_champs - 2))

    print("%s  %d -> %d o" % (URL, len(depart), len(c)))
    print("   %s" % " · ".join(notes))
    print("   champs : %d -> %d (les deux pieges que le navigateur remplissait)"
          % (avant_champs, apres_champs))
    print("   reste le piege « website », que le serveur controle aussi")
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % PID), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", PID, c, live=True)
        print("   pose.")


def main():
    poser = "--poser" in sys.argv
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for pid, url in PAGES:
        try:
            traiter(pid, url, poser)
        except SystemExit as e:
            print("%-46s %s" % (url[:46], e))
        print()
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
