#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Champ telephone obligatoire sur le formulaire de /migration-as400/.

PAGE PROTEGEE — 11162 fait partie des cinq pages de la regle 0. Ajouter un
champ est une modification de structure. Le client a donne son feu vert
explicite le 12/09/2026 : « oui je veux de la meme facon ». Rien d'autre n'est
touche — ni l'URL, ni le gabarit, ni le title, ni le reste de la structure.
La portee est strictement : un champ, sa validation, son envoi.

CE QUI EST POSE — exactement le meme dispositif que sur /contact/ :
  1. un champ telephone requis, apres l'email, dans le style du formulaire ;
  2. la garde a dix chiffres dans hhMigSubmit(), avec message sous le champ
     et dans le bandeau deja existant ;
  3. le numero ENTRE DANS LA CHARGE envoyee — sans cela il serait saisi puis
     jete, et le mail afficherait « Telephone : (non renseigne) », puisque
     l'endpoint hh/v1/contact lit la cle « phone ».

CE QUI N'EST PAS TOUCHE — l'endpoint hh/v1/contact. Aucune regle serveur
ajoutee : si la validation client passe, le mail part comme avant.

Usage :  python3 tel_migration_as400.py            (essai a blanc)
         python3 tel_migration_as400.py --live     (ecriture)
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
PAGE = 11162
STYLE_CHAMP = ("padding:13px 15px;border:1px solid #cbd5e1;border-radius:10px;font-size:1rem")

# ------------------------------------------------------------- 1. le champ
CHAMP_AV = ('<input type="email" name="Email" required placeholder="Email professionnel *" '
            'style="%s">' % STYLE_CHAMP)
CHAMP_AP = (CHAMP_AV
            + '\n<input type="tel" name="Telephone" id="hh-mig-tel" required inputmode="tel" '
              'autocomplete="tel" aria-label="Téléphone" aria-describedby="hh-mig-tel-err" '
              'placeholder="Téléphone * — 06 12 34 56 78" '
              'oninput="var e=document.getElementById(\'hh-mig-tel-err\');if(e){e.hidden=true;}'
              'this.removeAttribute(\'aria-invalid\');this.classList.remove(\'hh-invalide\');" '
              'style="%s">'
              '\n<span class="hh-err" id="hh-mig-tel-err" hidden></span>' % STYLE_CHAMP)

# --------------------------------------------------------- 2. la validation
GARDE_AV = (' if(!val("Nom")||!val("Email")){show("#fee2e2","#991b1b",'
            '"Merci de renseigner votre nom et votre email.");return false;}')
GARDE_AP = (GARDE_AV
            + '\n var telBrut=val("Telephone");'
              '\n var telNum=telBrut.replace(/[\\s.\\-()\\/]/g,"").replace(/^\\+33/,"0")'
              '.replace(/^0033/,"0");'
              '\n var telEl=document.getElementById("hh-mig-tel"),'
              'telErr=document.getElementById("hh-mig-tel-err");'
              '\n if(!/^0[1-9][0-9]{8}$/.test(telNum)){'
              'if(telErr){telErr.hidden=false;telErr.textContent=telBrut?'
              '"Ce numéro ne fait pas dix chiffres. Exemple : 06 12 34 56 78.":'
              '"Merci d\'indiquer votre numéro de téléphone.";}'
              'if(telEl){telEl.setAttribute("aria-invalid","true");'
              'telEl.classList.add("hh-invalide");'
              'try{telEl.focus({preventScroll:true});}catch(err){}}'
              'show("#fee2e2","#991b1b","Merci d\'indiquer un numéro de téléphone à dix '
              'chiffres, par exemple 06 12 34 56 78.");return false;}'
              '\n if(telErr){telErr.hidden=true;}'
              '\n if(telEl){telEl.removeAttribute("aria-invalid");'
              'telEl.classList.remove("hh-invalide");}')

# ------------------------------------------------------------ 3. la charge
CHARGE_AV = 'var payload={name:val("Nom"),email:val("Email"),company:val("Entreprise"),'
CHARGE_AP = ('var payload={name:val("Nom"),email:val("Email"),company:val("Entreprise"),'
             'phone:val("Telephone"),')

# ------------------------------------------------------------- 4. le style
STYLE = """<style id="hh-tel-obligatoire">
#hh-page .hh-err,.hh-err{display:block;margin:.1rem 0 0 !important;padding:0 !important;
 color:#B3261E;font-size:.82rem;line-height:1.4;font-weight:600}
#hh-page .hh-err[hidden],.hh-err[hidden]{display:none !important}
#hh-page input.hh-invalide,input.hh-invalide{border-color:#B3261E !important;
 box-shadow:0 0 0 3px rgba(179,38,30,.12) !important}
</style>"""


def main():
    p = w.get_raw("pages", PAGE)
    c = p["content"]["raw"]
    el = (p.get("meta", {}).get("_elementor_data") or "").strip()
    if el not in ("", "[]", "[ ]", "null"):
        raise SystemExit("ARRET — la page porte des donnees Elementor (%d octets)" % len(el))

    faits, pb = [], []
    n = c
    for quoi, av, ap in (("champ telephone requis", CHAMP_AV, CHAMP_AP),
                         ("garde a dix chiffres", GARDE_AV, GARDE_AP),
                         ("numero ajoute a la charge envoyee", CHARGE_AV, CHARGE_AP)):
        if n.count(av) != 1:
            pb.append("%s : ancre trouvee %d fois, attendu 1" % (quoi, n.count(av)))
            continue
        n = n.replace(av, ap, 1)
        faits.append(quoi)
    if "hh-tel-obligatoire" not in n:
        n += STYLE
        faits.append("feuille de style du message d'erreur")

    # ------------------------------------------------- ce qui doit survivre
    for quoi in ('id="hh-mig-form"', "hhMigSubmit", "hh/v1/contact", 'name="Nom"',
                 'name="Email"', 'name="AS400"', 'name="Users"', 'name="Message"',
                 'name="website"', "hh-mig-btn", "hh-mig-msg"):
        if n.count(quoi) < c.count(quoi) or n.count(quoi) == 0:
            pb.append("perdu au montage : %s" % quoi)
    # la regle 0 : rien d'autre que le formulaire ne bouge
    for quoi in ("<h1", "<title", "hero-section"):
        if n.count(quoi) != c.count(quoi):
            pb.append("regle 0 : %s a change de compte" % quoi)
    if len(n) < len(c):
        pb.append("la page a maigri de %d octets" % (len(c) - len(n)))

    print("page %d /migration-as400/ (PROTEGEE, feu vert du client) — %d -> %d octets"
          % (PAGE, len(c), len(n)))
    for f in faits:
        print("  · %s" % f)
    for x in pb:
        print("  ! %s" % x)
    if pb:
        raise SystemExit("ARRET — rien n'est ecrit tant qu'un controle est rouge")

    open("%s/migration-11162-avant.html" % S, "w", encoding="utf-8").write(c)
    open("%s/migration-11162-apres.html" % S, "w", encoding="utf-8").write(n)
    print("  sauvegardes : migration-11162-avant.html / migration-11162-apres.html")

    if not LIVE:
        print("\nessai a blanc — rien n'est ecrit. Relancer avec --live.")
        return

    w.api("pages/%d" % PAGE, "POST", {"content": n})
    c2 = w.get_raw("pages", PAGE)["content"]["raw"]
    ok = all(x in c2 for x in ('id="hh-mig-tel"', '0[1-9][0-9]{8}',
                               'phone:val("Telephone")', "hh-tel-obligatoire"))
    print("  relecture : %s" % ("en place" if ok else "ECHEC"))
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                        "https://www.helloharel.com/migration-as400/"],
                       capture_output=True, text=True)
    print("  /migration-as400/ -> HTTP %s" % r.stdout.strip())


if __name__ == "__main__":
    main()
