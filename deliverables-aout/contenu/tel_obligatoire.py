#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telephone obligatoire et valide sur le formulaire de contact.

ETAT DES LIEUX — 179 contenus passes en revue le 12/09/2026 (76 pages et 103
articles, contenu brut ET rendu HTML en ligne). Le site ne porte que DEUX
formulaires :

  · /contact/ (page 661) ........... le formulaire de demande de demo, avec un
    champ telephone ;
  · /migration-as400/ (page 11162) . le formulaire d'audit de migration, SANS
    champ telephone — et la page est protegee par la regle 0.

Aucun formulaire n'est injecte par le theme, le pied de page ou une modale :
les boutons « Demandez une demo » des 177 autres pages sont des liens vers
/contact/. Corriger /contact/ couvre donc tout le parcours de demande.

LE DEFAUT — le champ telephone porte bien un attribut « required », mais le
formulaire porte « novalidate » : la validation native du navigateur est
desactivee, et submitContactForm() ne verifie que le nom, l'email et la
societe. Le telephone part donc vide, ou avec trois chiffres.

CE QUE FAIT CE SCRIPT — cote CLIENT uniquement :
  1. l'etiquette passe a « Telephone * », comme les autres champs requis ;
  2. le champ recoit inputmode, autocomplete et un emplacement de message ;
  3. submitContactForm() refuse l'envoi si le numero ne fait pas dix chiffres,
     avec un message sous le champ et dans le bandeau deja existant.

CE QU'IL NE TOUCHE PAS — l'endpoint hh/v1/contact. Aucune regle serveur n'est
ajoutee : si la validation client passe, le mail part exactement comme avant.
C'est la garantie que rien ne peut bloquer l'envoi.

LE FORMAT ACCEPTE — la norme francaise : dix chiffres commencant par 0, avec
ou sans espaces, points ou tirets. « +33 » et « 0033 » sont ramenes a « 0 ».
  06 12 34 56 78 · 06.12.34.56.78 · 0612345678 · +33 6 12 34 56 78

Usage :  python3 tel_obligatoire.py            (essai a blanc)
         python3 tel_obligatoire.py --live     (ecriture)
"""

import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w                       # noqa: E402

LIVE = "--live" in sys.argv
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PAGE = 661
PROTEGEES = {1726, 2818, 2839, 5477, 11162}

# ---------------------------------------------------------------- 1. l'etiquette
LABEL_AV = ('<div class="form-group"><label>Téléphone</label>'
            '<input type="tel" name="phone" id="form-field-phone" required '
            'placeholder="06 00 00 00 00" '
            'oninput="document.getElementById(\'form-field-tel\').value=this.value;"></div>')
LABEL_AP = ('<div class="form-group"><label for="form-field-phone">Téléphone *</label>'
            '<input type="tel" name="phone" id="form-field-phone" required '
            'inputmode="tel" autocomplete="tel" aria-describedby="form-field-phone-err" '
            'placeholder="06 12 34 56 78" '
            'oninput="document.getElementById(\'form-field-tel\').value=this.value;">'
            '<span class="hh-err" id="form-field-phone-err" hidden></span></div>')

# ------------------------------------------------- 2. l'effacement du message
MIROIR_AV = ("document.getElementById('form-field-tel').value=this.value;"
             "document.getElementById('form-field-telephone').value=this.value;");
MIROIR_AP = (MIROIR_AV
             + "var e=document.getElementById('form-field-phone-err');"
               "if(e){e.hidden=true;}"
               "this.removeAttribute('aria-invalid');"
               "this.classList.remove('hh-invalide');")

# ----------------------------------------------------------- 3. la validation
ANCRE = """  if (!nameVal || !emailVal || !companyVal) {
    show('#fef2f2', '#b91c1c', '#fecaca', "Merci de renseigner votre nom, votre email et le nom de votre société.");
    return false;
  }"""

GARDE = ANCRE + """

  // Telephone obligatoire, au format francais a dix chiffres. On accepte les
  // espaces, points et tirets, ainsi que les prefixes +33 et 0033.
  var phoneRaw = (v('phone') || '').trim();
  var phoneNum = phoneRaw.replace(/[\\s.\\-()\\/]/g, '')
                         .replace(/^\\+33/, '0')
                         .replace(/^0033/, '0');
  var phoneEl  = document.getElementById('form-field-phone');
  var phoneErr = document.getElementById('form-field-phone-err');
  if (!/^0[1-9][0-9]{8}$/.test(phoneNum)) {
    if (phoneErr) {
      phoneErr.hidden = false;
      phoneErr.textContent = phoneRaw
        ? 'Ce numéro ne fait pas dix chiffres. Exemple : 06 12 34 56 78.'
        : 'Merci d\\'indiquer votre numéro de téléphone.';
    }
    if (phoneEl) {
      phoneEl.setAttribute('aria-invalid', 'true');
      phoneEl.classList.add('hh-invalide');
      try { phoneEl.focus({preventScroll: true}); } catch (err) {}
    }
    show('#fef2f2', '#b91c1c', '#fecaca',
         "Merci d'indiquer un numéro de téléphone à dix chiffres, par exemple 06 12 34 56 78.");
    return false;
  }
  if (phoneErr) { phoneErr.hidden = true; }
  if (phoneEl) {
    phoneEl.removeAttribute('aria-invalid');
    phoneEl.classList.remove('hh-invalide');
  }"""

# ------------------------------------------------------------------ 4. le style
STYLE = """<style id="hh-tel-obligatoire">
#hh-page .hh-err,.hh-err{display:block;margin:.4rem 0 0 !important;padding:0 !important;
 color:#B3261E;font-size:.82rem;line-height:1.4;font-weight:600}
#hh-page .hh-err[hidden],.hh-err[hidden]{display:none !important}
#hh-page input.hh-invalide,input.hh-invalide{border-color:#B3261E !important;
 box-shadow:0 0 0 3px rgba(179,38,30,.12) !important}
</style>"""


def main():
    if PAGE in PROTEGEES:
        raise SystemExit("ARRET — page protegee")

    p = w.get_raw("pages", PAGE)
    c = p["content"]["raw"]
    el = (p.get("meta", {}).get("_elementor_data") or "").strip()
    if el not in ("", "[]", "[ ]", "null"):
        raise SystemExit("ARRET — la page porte des donnees Elementor (%d octets)" % len(el))

    faits, pb = [], []
    n = c

    for quoi, av, ap in (("etiquette et champ", LABEL_AV, LABEL_AP),
                         ("effacement du message a la saisie", MIROIR_AV, MIROIR_AP),
                         ("garde sur le numero", ANCRE, GARDE)):
        if n.count(av) != 1:
            pb.append("%s : ancre trouvee %d fois, attendu 1" % (quoi, n.count(av)))
            continue
        n = n.replace(av, ap, 1)
        faits.append(quoi)

    if "hh-tel-obligatoire" not in n:
        n += STYLE
        faits.append("feuille de style du message d'erreur")

    # --------------------------------------------------------------- controles
    for quoi, attendu in (("submitContactForm", 1), ("hh/v1/contact", 1),
                          ('id="hh-contact-form"', 1), ('name="phone"', 1),
                          ("generate_lead", 1)):
        if n.count(quoi) < attendu:
            pb.append("perdu au montage : %s" % quoi)
    if len(n) < len(c):
        pb.append("la page a maigri de %d octets" % (len(c) - len(n)))

    print("page %d /contact/ — %d octets -> %d" % (PAGE, len(c), len(n)))
    for f in faits:
        print("  · %s" % f)
    for x in pb:
        print("  ! %s" % x)
    if pb:
        raise SystemExit("ARRET — rien n'est ecrit tant qu'un controle est rouge")

    open("%s/contact-661-avant.html" % S, "w", encoding="utf-8").write(c)
    open("%s/contact-661-apres.html" % S, "w", encoding="utf-8").write(n)
    print("  sauvegardes : contact-661-avant.html / contact-661-apres.html")

    if not LIVE:
        print("\nessai a blanc — rien n'est ecrit. Relancer avec --live.")
        return

    w.api("pages/%d" % PAGE, "POST", {"content": n})
    c2 = w.get_raw("pages", PAGE)["content"]["raw"]
    ok = ("hh-tel-obligatoire" in c2 and "form-field-phone-err" in c2
          and "0[1-9][0-9]{8}" in c2 and "submitContactForm" in c2)
    print("  relecture : %s" % ("en place" if ok else "ECHEC"))
    r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                        "https://www.helloharel.com/contact/"], capture_output=True, text=True)
    print("  /contact/ -> HTTP %s" % r.stdout.strip())


if __name__ == "__main__":
    main()
