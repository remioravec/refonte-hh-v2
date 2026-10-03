#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le formulaire de /migration-as400/ n'a jamais rien envoye.

Son script contient deux esperluettes doubles. WordPress en transforme
une a la sortie :

    if(d&&d.success)      devient      if(d&#038;&#038;d.success)

Ce n'est plus du JavaScript. Le bloc entier echoue au chargement, la
fonction hhMigSubmit n'existe jamais, et le bouton du formulaire appelle
une fonction absente. Verifie dans un navigateur : « Invalid or
unexpected token », puis « hhMigSubmit is not defined ».

C'est le meme piege qui avait casse le defilement des trois pages
pilotes le 22 septembre. La regle qui en est sortie : aucune esperluette
nue dans un script pose en contenu. On applique la regle plutot que de
compter sur l'humeur du filtre.

    if(migT>0&&Date.now()-migT<2000){...}   ->   deux if imbriques
    if(d&&d.success){...}else{...}          ->   un ternaire, sans « & »

La page est sous Regle 0. Reparer un formulaire qui perd les demandes
n'est pas l'optimiser.

Usage :  python3 reparer_as400.py           (blanc)
         python3 reparer_as400.py --poser   (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402

PID, URL = 11162, "/migration-as400/"
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/as400-avant")

REMPLACEMENTS = (
    ('if(migT>0&&Date.now()-migT<2000){',
     'if(migT>0){if(Date.now()-migT<2000){'),
    ('pour relire votre demande avant de l\'envoyer.");return false;}',
     'pour relire votre demande avant de l\'envoyer.");return false;}}'),
    ('.then(function(d){if(d&&d.success){',
     '.then(function(d){if(d?d.success:false){'),
)


def main():
    poser = "--poser" in sys.argv
    c = w.get_raw("pages", PID)["content"]["raw"]
    depart = c

    for avant, apres in REMPLACEMENTS:
        n = c.count(avant)
        if n != 1:
            raise SystemExit("ARRET — %d occurrence(s) de : %s" % (n, avant[:60]))
        c = c.replace(avant, apres)

    # ── controles ────────────────────────────────────────────────────────
    for m in re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S):
        if "&" in m.group(1):
            k = m.group(1).find("&")
            raise SystemExit("ARRET — esperluette restante : ...%s..."
                             % m.group(1)[max(0, k - 50):k + 40])
    # accolades du script du formulaire
    i = c.find("function hhMigSubmit")
    sc = c.rfind("<script", 0, i)
    fin = c.find("</script>", i)
    bloc = c[sc:fin]
    if bloc.count("{") != bloc.count("}"):
        raise SystemExit("ARRET — accolades desequilibrees : %d / %d"
                         % (bloc.count("{"), bloc.count("}")))
    if bloc.count("(") != bloc.count(")"):
        raise SystemExit("ARRET — parentheses desequilibrees")
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge")
    if D.liens(c) != D.liens(depart):
        raise SystemExit("ARRET — les liens bougent")
    if c.count("<section class=") != depart.count("<section class="):
        raise SystemExit("ARRET — le nombre de sections bouge")
    if len(re.findall(r"<(?:input|select|textarea)\b", c)) \
            != len(re.findall(r"<(?:input|select|textarea)\b", depart)):
        raise SystemExit("ARRET — le nombre de champs bouge")

    print("%s  %d -> %d o" % (URL, len(depart), len(c)))
    print("   3 reecritures, plus une seule esperluette dans les scripts")
    print("   script du formulaire : %d accolades appairees" % bloc.count("{"))
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % PID), "w",
             encoding="utf-8").write(depart)
        w.update_content("pages", PID, c, live=True)
        print("\n   pose.")
    else:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
