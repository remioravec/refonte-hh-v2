#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La page de demande de demo : retirer le selecteur, poser la preuve.

Trois choses, dans cet ordre.

1. Le selecteur « Secteur d'activite » s'en va. Un champ de plus entre le
   visiteur et l'envoi, et sa liste proposait encore dispositifs
   medicaux, laboratoire, materiel dentaire — le site ne parle plus que
   d'agroalimentaire. Le script d'envoi lit ce champ pour l'etiquette
   d'un evenement GA4 et retombe deja sur « demo » quand il est vide :
   rien a changer de ce cote.

2. Les avis Google arrivent. La section est reprise telle quelle des
   pages metiers — meme composant, memes logos Google, meme note. Elle
   est autonome : trois feuilles de style internes, aucun script.

3. L'ordre de la page change. La bande de logos etait posee APRES les
   coordonnees, loin du formulaire. Preuve et formulaire se lisent
   ensemble ou ne servent a rien :

       formulaire · logos · avis · coordonnees · appel a l'action

Usage :  python3 contact_preuve.py           (blanc)
         python3 contact_preuve.py --poser   (ecrit)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import pilier_gabarit as P       # noqa: E402

PID, URL = 661, "/contact/"
DONNEUSE = 3309                  # /agroalimentaire/boulanger/
ORDRE = ["contact-hero", "logos-section", "reviews-section",
         "contact-section", "cta-banner"]
SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/contact-avant")


def section(c, nom):
    i = c.find('<section class="%s"' % nom)
    if i < 0:
        return None, None
    return i, P.bornes(c, i)


def main():
    poser = "--poser" in sys.argv
    d = w.get_raw("pages", PID)
    el = (d.get("meta") or {}).get("_elementor_data")
    if el not in (None, "", "[]"):
        raise SystemExit("ARRET — _elementor_data non vide")
    c = d["content"]["raw"]
    depart = c
    notes = []

    # ── 1. le selecteur ──────────────────────────────────────────────────
    m = re.search(r'<div class="form-group"><label>Secteur[^<]*</label>'
                  r'<select name="secteur">.*?</select></div>', c, re.S)
    if not m:
        raise SystemExit("ARRET — champ « secteur » introuvable")
    n_champs = len(re.findall(r"<(?:input|select|textarea)\b", c))
    c = c[:m.start()] + c[m.end():]
    notes.append("selecteur d'activite retire (%d o)" % (m.end() - m.start()))

    # ── 2. les avis ──────────────────────────────────────────────────────
    b = w.get_raw("pages", DONNEUSE)["content"]["raw"]
    i, j = section(b, "reviews-section")
    if i is None:
        raise SystemExit("ARRET — section des avis introuvable sur la donneuse")
    avis = b[i:j]
    if D.solde(avis) != 0:
        raise SystemExit("ARRET — la section des avis n'est pas close")
    if "<script" in avis:
        raise SystemExit("ARRET — la section des avis embarque un script")
    # La feuille de style de la page decrit deja « reviews-section » —
    # c'est le balisage qui manque, pas le CSS. On cherche donc la section,
    # pas le mot.
    if '<section class="reviews-section"' in c:
        raise SystemExit("ARRET — la page porte deja des avis")

    # ── 3. l'ordre ───────────────────────────────────────────────────────
    il, jl = section(c, "logos-section")
    if il is None:
        raise SystemExit("ARRET — bande de logos introuvable")
    logos = c[il:jl]
    c = c[:il] + c[jl:]
    ih, jh = section(c, "contact-hero")
    if ih is None:
        raise SystemExit("ARRET — hero introuvable")
    c = c[:jh] + logos + avis + c[jh:]
    notes.append("avis Google poses (%d o)" % len(avis))
    notes.append("logos remontes sous le formulaire")

    # ── controles ────────────────────────────────────────────────────────
    vus = [m2.group(1).split()[0] for m2 in re.finditer(r'<section class="([^"]+)"', c)]
    if vus != ORDRE:
        raise SystemExit("ARRET — ordre obtenu : %s" % vus)
    if D.solde(c) != D.solde(depart):
        raise SystemExit("ARRET — le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    reste = len(re.findall(r"<(?:input|select|textarea)\b", c))
    if reste != n_champs - 1:
        raise SystemExit("ARRET — %d champs au lieu de %d" % (reste, n_champs - 1))
    for champ in ('name="name"', 'name="email"', 'name="company"',
                  'name="phone"', 'name="message"', 'id="hh-contact-form"',
                  "submitContactForm"):
        if champ not in c:
            raise SystemExit("ARRET — %s a disparu du formulaire" % champ)
    if 'name="secteur"' in c:
        raise SystemExit("ARRET — le selecteur est encore la")
    perdus = sorted(set(D.liens(depart)) - set(D.liens(c)))
    if perdus:
        raise SystemExit("ARRET — lien(s) perdu(s) : %s" % perdus[:3])
    if len(c) > D.PLAFOND:
        raise SystemExit("ARRET — %d o, au-dela du seuil de rendu" % len(c))

    print("%s  %d -> %d o" % (URL, len(depart), len(c)))
    print("   %s" % "\n   ".join(notes))
    print("   ordre : %s" % " > ".join(vus))
    print("   champs du formulaire : %d -> %d" % (n_champs, reste))
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
