#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le gabarit est-il vraiment en ligne ? Non pas dans la base : dans la page.

Une page peut etre parfaite en base et servie vide. C'est arrive : au-dela
d'environ 275 ko de contenu, le site rend un document complet — en-tete,
pied, balises fermees — et sans aucune de ses sections. Un controle qui
lit la base ne voit rien de tout cela.

On mesure donc ce que le visiteur recoit :
  * les neuf sections du gabarit, dans l'ordre ;
  * le script du defilement, octet pour octet — WordPress l'a deja casse
    en transformant deux esperluettes en entites ;
  * les questions de la FAQ, ouvertes dans le HTML et non au clic ;
  * le nom, l'adresse et le telephone au pied ;
  * l'absence de calculateur, de simulateur et de quiz ;
  * la marge qui reste avant le plafond de rendu.
"""

import os
import re
import sys
import time
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import deployer_gabarit as D     # noqa: E402
import scroll_sticky as SY       # noqa: E402

ATTENDU = ["hero-section", "logos-section", "features-section", "about-card-section",
           "process-section", "metiers-section", "team-section", "faq-section",
           "reviews-section"]
# La page pilier garde son composant de FAQ, a la demande : « ajuste au
# gabarit sans toucher a la FAQ ».
EQUIVALENTS = {"hh2-faq-section": "faq-section"}
PLAFOND = 275_000
TEL = "06 18 06 00 18"
ADRESSE = "6 avenue de Rueil"
INTRUS = re.compile(r"calculateur|calculette|simulateur|quiz|hh-roi|hhq-", re.I)


def pages():
    return D.cibles() + [(10935, "/agroalimentaire/torrefacteur/"),
                         (10896, "/agroalimentaire/brasseur/"),
                         (10894, "/agroalimentaire/chocolatier/")]


def lire_page(url):
    """La page servie, en entier. Le transfert est parfois coupe en route."""
    for essai in range(4):
        try:
            h = urllib.request.urlopen(urllib.request.Request(
                "https://www.helloharel.com" + url + "?v=%d" % time.time(),
                headers={"User-Agent": "Mozilla/5.0"}), timeout=120
            ).read().decode("utf-8", "replace")
            if "</html>" in h:
                return h
        except Exception:                      # noqa: BLE001
            pass
        time.sleep(2 * (essai + 1))
    return None


def corps(h):
    """Le contenu de la page, sans l'en-tete ni le pied du theme."""
    i = h.find('<div id="hh-page"')
    if i < 0:
        i = h.find("<main")
    j = h.rfind("<footer")
    return h[i:j if j > i else len(h)]



def enfants_li(bloc, classe):
    """Les <li> de premier niveau d'une liste. Compter les occurrences d'une
    classe ou d'un attribut donne de faux comptes : les listes du gabarit
    sont imbriquees, et le script cite les memes noms."""
    k = bloc.find('<ul class="%s">' % classe)
    if k < 0:
        return None
    prof, fin = 0, len(bloc)
    for m in re.finditer(r"<(/?)ul\b", bloc[k:]):
        prof += 1 if not m.group(1) else -1
        if prof == 0:
            fin = k + m.end()
            break
    n, d = 0, 0
    for m in re.finditer(r"<(/?)li\b", bloc[k:fin]):
        if m.group(1):
            d -= 1
        else:
            if d == 0:
                n += 1
            d += 1
    return n


def examiner(pid, url):
    stock = w.get_raw("pages", pid)["content"]["raw"]
    h = lire_page(url)
    if h is None:
        return url, len(stock), None, ["page illisible en entier apres 4 essais"]

    b = corps(h)
    maux = []

    # 1. les sections, et leur ordre
    vus = [EQUIVALENTS.get(m.group(1).split()[0], m.group(1).split()[0])
           for m in re.finditer(r'<section class="([^"]+)"', b)]
    manque = [x for x in ATTENDU if x not in vus]
    rang = [ATTENDU.index(x) for x in vus if x in ATTENDU]
    if not vus:
        maux.append("AUCUNE section servie — la page est rendue vide")
    if manque:
        maux.append("sections absentes : " + ",".join(x.replace("-section", "") for x in manque))
    if rang != sorted(rang):
        maux.append("sections dans le desordre")

    # 2. le script du defilement, octet pour octet
    if 'id="hh-scrollytelling-js"' in stock:
        m = re.search(r'<script id="hh-scrollytelling-js">(.*?)</script>', h, re.S)
        attendu = re.search(r'<script id="hh-scrollytelling-js">(.*?)</script>', SY.JS, re.S)
        if not m:
            maux.append("script de defilement absent de la page servie")
        elif attendu and m.group(1) != attendu.group(1):
            maux.append("script de defilement altere (%d o servis contre %d)"
                        % (len(m.group(1)), len(attendu.group(1))))

    # 3. les etapes du defilement et leurs ecrans
    n_pas = enfants_li(b, "sy-pas")
    n_ecr = enfants_li(b, "sy-ecrans")
    if n_pas is None:
        if "features-section" in b:
            maux.append("section fonctionnalites sans defilement")
        n_pas = 0
    else:
        if n_pas < 4:
            maux.append("defilement a %d etape(s) servies" % n_pas)
        if n_ecr != n_pas:
            maux.append("%s etape(s) pour %s ecran(s)" % (n_pas, n_ecr))

    # 4. la FAQ, ouverte dans le HTML
    #
    # Deux composants coexistent : l'accordeon <details> du gabarit, et
    # celui de la page pilier, qui ouvre ses reponses par un <button>. Les
    # deux portent leurs reponses dans le HTML — c'est ce qui compte.
    i = b.find('<section class="faq-section"')
    if i >= 0:
        nq = b[i:b.find("</section>", i)].count("<details")
    else:
        i = b.find('<section class="hh2-faq-section')
        nq = (b[i:b.find("</section>", i)].count('class="hh2-faq-item"')
              if i >= 0 else 0)
    if nq < 5:
        maux.append("FAQ a %d question(s) servies" % nq)

    # 5. le pied de page
    if TEL not in h and TEL.replace(" ", "") not in h:
        maux.append("telephone absent")
    if ADRESSE.lower() not in h.lower():
        maux.append("adresse absente")

    # 6. les intrus
    n_int = len(INTRUS.findall(b))
    if n_int:
        maux.append("%d mention(s) de calculateur/simulateur" % n_int)

    # 7. la marge qui reste avant le plafond de rendu
    #
    # Le plafond n'est pas une regle du moteur, c'est une mesure : a environ
    # 280 ko de contenu, le site a servi trois pages completes et vides de
    # toutes leurs sections. PLAFOND est la marge de securite qu'on s'est
    # donnee en dessous. Une page qui la depasse n'est pas cassee — elle n'a
    # plus de place pour la prochaine modification.
    reste = PLAFOND - len(stock)
    if reste < 0:
        maux.append("marge de rendu epuisee : %d o de trop, aucune "
                    "modification possible sans alleger" % -reste)
    elif reste < 8000:
        maux.append("marge de rendu mince : %d o avant le seuil" % reste)

    return url, len(stock), (len(vus), n_pas, nq), maux


def main():
    lignes = []
    for pid, url in sorted(pages(), key=lambda t: t[1]):
        lignes.append(examiner(pid, url))

    print("%-46s %4s %3s %3s %3s  %s"
          % ("url", "ko", "sec", "pas", "FAQ", "etat"))
    print("-" * 126)
    bons = 0
    for url, taille, mes, maux in lignes:
        s, p, q = mes if mes else ("?", "?", "?")
        if not maux:
            bons += 1
        print("%-46s %4d %3s %3s %3s  %s"
              % (url[:46], taille // 1024, s, p, q,
                 " · ".join(maux) if maux else "servi conforme"))
    print("\n%d page(s) sur %d servies conformes" % (bons, len(lignes)))


if __name__ == "__main__":
    main()
