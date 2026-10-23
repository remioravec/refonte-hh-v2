#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose le gabarit des trois pages pilotes sur les pages metier et
fonctionnalites qui portent la meme structure.

CE QUI EST POSE, et dans cet ordre :
  1. reparation  — la carte orpheline hors section, et le solde des <div>
  2. FAQ         — le tiroir devient des accordeons natifs
  3. avis        — la grille devient un carrousel continu, marque Google
  4. equipe      — les quinze cartes deviennent trois vraies + silhouettes
  5. metiers      — icones remplacees par la photo de la page ouverte,
                    puis carte reduite au nom et a une fleche
  6. fonctionnalites — les onglets deviennent le defilement colle
  7. Hero        — description en liste, badge de reassurance, Maxence

CE QUI N'EST PAS POSE, et pourquoi :
  · les H2 explicatifs et les pastilles courtes des trois pages pilotes ont
    ete ecrits a la main, ecran par ecran. Ailleurs on garde les titres et
    les puces de la page. Le gabarit se deploie, le contenu se relit.
  · les avis dans les fonctionnalites : leur rattachement a une
    fonctionnalite a ete decide a la main. Sans cette lecture, aucun avis.

TROIS VERROUS :
  · les cinq pages de la regle 0 sont refusees ;
  · une page dont _elementor_data n'est pas vide est refusee ;
  · au-dela de 275 ko de contenu, le site cesse de rendre la page : toute
    page qui depasserait ce seuil apres travaux est refusee, pas posee.

Usage :  python3 deployer_gabarit.py                 (blanc, toutes)
         python3 deployer_gabarit.py --poser         (ecrit)
         python3 deployer_gabarit.py --page 3309     (une seule)
"""

import os
import re
import sys
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import scroll_sticky as SY       # noqa: E402
import remanier_agro as RA       # noqa: E402
import avatars as AV             # noqa: E402
import faq_accordeon as FA       # noqa: E402
import avis_pages as AP          # noqa: E402
import equipe_pages as EQ        # noqa: E402
import metiers_photos as MP      # noqa: E402
import metiers_sobre as MS       # noqa: E402
import hero_v2 as HV             # noqa: E402
import hero_maxence as HM        # noqa: E402

S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
SAUV = os.path.join(S, "gabarit-avant")
PROTEGEES = {1726, 2818, 2839, 5477, 11162}
PILOTES = {10935, 10896, 10894}
PLAFOND = 275_000


def solde(t):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", lambda m: " " * len(m.group(0)), t, flags=re.S)
    return len(re.findall(r"<div\b", t)) - len(re.findall(r"</div>", t))


def sans_code(t):
    return re.sub(r"<(style|script)[^>]*>.*?</\1>", "", t, flags=re.S)


def liens(t):
    return sorted(re.findall(r'href="([^"]+)"', sans_code(t)))


# ══════════════════════════════════════════════════════ les etapes

def etape_reparer(c, notes):
    """Retire TOUTES les cartes bento posees hors section, pas seulement la
    premiere : sur glacier, une grille legitime en precedait une orpheline,
    et s'arreter a la premiere laissait la seconde en place."""
    perdus, retirees, gardees = [], 0, 0
    while True:
        bouge = False
        for m in re.finditer(r'<div class="bento-card[^"]*"', c):
            fin = RA.div_complet(c, m.start())
            carte = c[m.start():fin]
            if solde(carte) != 0:
                raise SystemExit("une carte bento n'est pas un bloc clos")
            if c.rfind("<section", 0, m.start()) > c.rfind("</section>", 0, m.start()):
                continue          # dans une section : c'est sa place
            perdus += re.findall(r'href="([^"]+)"', carte)
            c = c[:m.start()] + c[fin:]
            retirees += 1
            bouge = True
            break
        if not bouge:
            break
    gardees = len(re.findall(r'<div class="bento-card', c))
    if retirees:
        notes.append("%d carte(s) orpheline(s) retiree(s)%s"
                     % (retirees, (" · %d gardee(s) en section" % gardees) if gardees else ""))
    elif gardees:
        notes.append("%d carte(s) bento en section, laissees" % gardees)
    return c, perdus


def etape_faq(c, notes):
    if 'id="faqDrawerOverlay"' not in c:
        notes.append("FAQ : pas de tiroir")
        return c
    i = c.find('<section class="faq-section"')
    j = c.find("</section>", i) + len("</section>")
    if i >= 0 and "<details" in c[i:j]:
        # La FAQ est deja depliable : il ne reste qu'un tiroir sans cartes
        # pour l'ouvrir, poids mort dans la page.
        k = c.find('id="faqDrawerOverlay"')
        k = c.rfind("<div", 0, k)
        fin = c.find("<script", k)
        dans = re.findall(r'href="([^"]+)"', sans_code(c[k:fin]))
        if dans:
            # Il porte des liens : ce n'est pas du poids mort, c'est du
            # maillage. On n'y touche pas sans l'avoir relu.
            notes.append("FAQ : deja en accordeon, tiroir laisse (%d lien(s) dedans)"
                         % len(dans))
            return c
        neuf = c[:k] + c[fin:]
        for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", neuf, re.S))[::-1]:
            if "openFaqDrawer" in m.group(1) or "faqDrawerOverlay" in m.group(1):
                neuf = neuf[:m.start()] + neuf[m.end():]
        if 'id="faqDrawerOverlay"' in neuf:
            raise SystemExit("le tiroir orphelin survit")
        notes.append("FAQ : deja en accordeon, tiroir orphelin retire (%d o)"
                     % (len(c) - len(neuf)))
        return neuf
    avant_faq = re.findall(r'href="([^"]+)"',
                           sans_code(c[c.find('<section class="faq-section"'):
                                       c.find("<script", c.find('id="faqDrawerOverlay"'))]))
    (i, j, k, fin), entete, paires, pied = FA.lire(c)
    if not (j <= k):
        raise SystemExit("le tiroir n'est pas apres la section")
    neuf = c[:k] + c[fin:]
    neuf = neuf[:i] + FA.section(entete, paires, pied) + neuf[j:]
    for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", neuf, re.S))[::-1]:
        if "openFaqDrawer" in m.group(1) or "faqDrawerOverlay" in m.group(1):
            neuf = neuf[:m.start()] + neuf[m.end():]
    # le balisage FAQPage n'est pas ajoute : les reponses de ces pages n'ont
    # pas ete relues, et on ne declare pas a Google un texte non verifie.
    neuf = re.sub(r'<script type="application/ld\+json">(?:(?!</script>).)*?'
                  r'FAQPage(?:(?!</script>).)*?</script>', "", neuf, flags=re.S)
    neuf = re.sub(r'\sitem(?:scope|prop|type)(?:="[^"]*")?', "", neuf)
    neuf = neuf.replace("<details open ", "<details ").replace("<details open>", "<details>")
    for x in ("faqDrawerOverlay", "faq-drawer", "openFaqDrawer", "faq-card"):
        if x in sans_code(neuf):
            raise SystemExit("il reste %s dans le corps" % x)
    i2 = neuf.find('<section class="faq-section"')
    j2 = neuf.find("</section>", i2) + len("</section>")
    apres_faq = re.findall(r'href="([^"]+)"', sans_code(neuf[i2:j2]))
    partis = list(avant_faq)
    for x in apres_faq:
        if x in partis:
            partis.remove(x)
    # Les libelles de cartes portaient parfois un lien que la question du
    # tiroir n'a pas. On le dit, on ne le cache pas dans un total.
    notes.append("FAQ : %d accordeons%s"
                 % (len(paires),
                    (" · lien(s) de libelle perdu(s) : " + ", ".join(sorted(set(partis))))
                    if partis else ""))
    return neuf, partis


def etape_avis(c, notes):
    i = c.find('<section class="reviews-section"')
    if i < 0 or 'class="avis-file"' in c:
        notes.append("avis : rien a faire")
        return c
    j = c.find("</section>", i) + len("</section>")
    sec = c[i:j]
    cartes = AP.cartes(sec)
    if len(cartes) < 3:
        notes.append("avis : %d carte(s), laissees" % len(cartes))
        return c
    neuves, noms = [], []
    for k in cartes:
        n, nom = AP.poser_tete(k)
        if not nom:
            raise SystemExit("carte d'avis sans nom")
        neuves.append(n.replace('class="hh-tete ' + AV.cle(nom) + '"',
                                'class="hh-tete hh-tete-g"'))
        noms.append(nom)
    g = sec.find('<div class="reviews-grid">')
    gf = RA.div_complet(sec, g)
    neuve = (sec[:g] + AV.feuille_google("hh-avis-tetes") + AP.CSS_TETE
             + RA.avis_carrousel(neuves) + sec[gf:])
    av = re.findall(r'<p class="review-text">(.*?)</p>', sec, re.S)
    ap = re.findall(r'<p class="review-text">(.*?)</p>', neuve, re.S)
    if sorted(set(av)) != sorted(set(ap)) or len(ap) != 2 * len(av):
        raise SystemExit("un texte d'avis a change")
    notes.append("avis : %d en carrousel" % len(cartes))
    return c[:i] + neuve + c[j:]


def etape_equipe(c, notes):
    i = c.find('<section class="team-section"')
    if i < 0 or 'class="eq-rail"' in c:
        notes.append("equipe : rien a faire")
        return c
    j = c.find("</section>", i) + len("</section>")
    sec = c[i:j]
    ent = re.search(r'<div class="section-header">.*?</div>\s*(?=<div class="team-grid")', sec, re.S)
    if not ent:
        notes.append("equipe : en-tete introuvable, laissee")
        return c
    vrais, faux = EQ.lire(sec)
    if len(vrais) != 3:
        notes.append("equipe : %d personne(s) reelle(s), laissee" % len(vrais))
        return c
    notes.append("equipe : 3 en rail, %d fabriquees retirees" % faux)
    return c[:i] + EQ.section(ent.group(0), vrais) + c[j:]


def etape_metiers(c, notes):
    i = c.find('<section class="metiers-section"')
    if i < 0:
        notes.append("metiers : pas de section")
        return c
    j = c.find("</section>", i) + len("</section>")
    sec = c[i:j]
    if 'class="mt-f"' in sec:
        notes.append("metiers : deja fait")
        return c
    cartes = re.findall(r'(<a href="([^"]+)" class="metier-slide[^"]*">)(.*?)(</a>)', sec, re.S)
    if not cartes:
        notes.append("metiers : aucune carte")
        return c
    neuve, poses, sans = sec, 0, []
    for ouvre, cible, corps, ferme in cartes:
        nom = re.search(r"<h3>([^<]+)</h3>", corps)
        if not nom:
            raise SystemExit("carte metier sans nom")
        img = MP.hero_de(cible)
        bloc = re.search(r'<div class="tilted-icon">.*?</div>\s*(?=<h3>)', corps, re.S)
        vis = re.search(r'<span class="mt-v">.*?</span>', corps, re.S)
        if img and bloc:
            vis_html = ('<span class="mt-v"><img src="%s" alt="" aria-hidden="true" '
                        'loading="lazy" decoding="async"></span>' % img)
            poses += 1
        elif vis:
            vis_html = vis.group(0)
        elif bloc:
            # Pas de Hero a la destination — un article de blog, par
            # exemple. L'icone reste : mieux vaut une carte sans photo
            # qu'une carte sans visuel.
            vis_html = bloc.group(0)
            sans.append(nom.group(1).strip())
        else:
            raise SystemExit("carte metier sans visuel possible (%s)" % cible)
        sobre = vis_html + "<h3><span>%s</span>%s</h3>" % (nom.group(1).strip(), MS.FLECHE)
        neuve = neuve.replace(ouvre + corps + ferme, ouvre + sobre + ferme, 1)
    neuve = MP.CSS + MS.CSS + neuve
    if len(re.findall(r'class="metier-slide', neuve)) != len(cartes):
        raise SystemExit("carte metier perdue")
    notes.append("metiers : %d cartes, %d photos%s"
                 % (len(cartes), poses,
                    (" (icone gardee : " + ", ".join(sans) + ")") if sans else ""))
    return c[:i] + neuve + c[j:]


def etape_fonctionnalites(c, notes):
    i = c.find('<section class="features-section"')
    if i < 0:
        notes.append("fonctionnalites : pas de section")
        return c
    j = c.find("</section>", i) + len("</section>")
    if "<section" in c[i + 10:j]:
        raise SystemExit("section fonctionnalites imbriquee")
    if 'class="sy-ecrans"' in c:
        notes.append("fonctionnalites : deja converti")
        return c
    if 'class="hhf-bar"' not in c[i:j]:
        notes.append("fonctionnalites : module inconnu, laissee")
        return c
    avant_liens = re.findall(r'href="([^"]+)"', sans_code(c[i:j]))
    entete, blocs = SY.extraire(c)
    ecrans = [b[2] for b in blocs]
    lg = [m for b in blocs for m in re.findall(r'(<a class="hhf-lien".*?</a>)', b[1], re.S)]
    contenu = []
    for titre, corps, _ in blocs:
        puces = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
                 for x in re.findall(r"<li>(.*?)</li>", corps, re.S)]
        puces = [x for x in puces if x]
        contenu.append((re.sub(r"<[^>]+>", "", titre).strip(), puces, None, []))
    neuf = c[:i] + SY.section(entete, ecrans, lg, contenu) + c[j:]
    for motif in (r'<style id="hh-scrollytelling">.*?</style>',
                  r'<script(?![^>]*\ssrc)[^>]*>(?:(?!</script>).)*?'
                  r'querySelectorAll\("\.sy-ecrans(?:(?!</script>).)*?</script>'):
        t = list(re.finditer(motif, neuf, re.S))
        for m in t[:-1][::-1]:
            neuf = neuf[:m.start()] + neuf[m.end():]
    i2 = neuf.find('<section class="features-section"')
    j2 = neuf.find("</section>", i2) + len("</section>")
    apres_liens = re.findall(r'href="([^"]+)"', sans_code(neuf[i2:j2]))
    partis = list(avant_liens)
    for x in apres_liens:
        if x in partis:
            partis.remove(x)
    notes.append("fonctionnalites : %d etapes en defilement, %d lien(s) de section retire(s)"
                 % (len(ecrans), len(partis)))
    return neuf, partis


def decouper_hero(texte):
    """Amorce + enumeration, tirees de la phrase elle-meme."""
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", texte)).strip()
    if ":" not in t:
        return None
    a, b = t.split(":", 1)
    a, b = a.strip(), b.strip().rstrip(".")
    # la moitie qui enumere est celle qui porte le plus de virgules
    if a.count(",") >= b.count(","):
        liste_txt, amorce = a, b
    else:
        liste_txt, amorce = b, a
    items = [x.strip() for x in re.split(r",| et ", liste_txt) if x.strip()]
    if len(items) < 3 or len(items) > 8:
        return None
    if any(len(x) > 46 for x in items):
        return None
    amorce = amorce[0].upper() + amorce[1:] if amorce else amorce
    return amorce, items


def etape_hero(c, notes):
    i = c.find('<section class="hero-section"')
    if i < 0:
        notes.append("Hero : pas de section")
        return c
    j = c.find("</section>", i)
    hero = c[i:j]
    neuf = c

    # 1. la description en liste, sans perdre un mot
    m = re.search(r'<p class="hero-description">(.*?)</p>', hero, re.S)
    if m and 'class="hh-hl"' not in hero:
        d = decouper_hero(m.group(1))
        if d:
            amorce, items = d
            lis = "".join("<li>%s%s</li>" % (HV.COCHE, x) for x in items)
            neuve = ('<p class="hero-description">%s :</p><ul class="hh-hl">%s</ul>'
                     % (amorce, lis))
            LIBRE = {"et"}
            av = [x for x in HV.mots(m.group(1)) if x not in LIBRE]
            ap = [x for x in HV.mots(neuve) if x not in LIBRE]
            if av == ap:
                neuf = neuf[:i + m.start()] + neuve + neuf[i + m.end():]
                notes.append("Hero : %d puces" % len(items))
            else:
                notes.append("Hero : liste ecartee (le texte aurait bouge)")
        else:
            notes.append("Hero : phrase non decoupable, laissee")

    # 2. le badge de reassurance
    if 'class="hh-conf"' not in neuf:
        note = re.search(r'class="rating-text">([^<]+)<', neuf)
        sub = re.search(r'<p class="hero-cta-sub">.*?</p>', neuf, re.S)
        i2 = neuf.find('<section class="hero-section"')
        j2 = neuf.find("</section>", i2)
        if note and sub and i2 < sub.start() < j2:
            neuf = neuf[:sub.end()] + HV.badge(note.group(1).strip()) + neuf[sub.end():]
            notes.append("Hero : badge")
        else:
            notes.append("Hero : badge ecarte (note ou pied absent)")

    # 3. la feuille du Hero et Maxence
    if '<style id="hh-hero-v2">' not in neuf:
        neuf += HV.CSS
    if 'class="hh-max"' not in neuf:
        neuf += HV.css_maxence() + HM.widget() + HM.JS
        notes.append("Maxence")
    return neuf


# ══════════════════════════════════════════════════════ l'orchestration

def cibles():
    out, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/pages?per_page=100&page=%d&status=publish&_fields=id,link" % p)
        if not lot:
            break
        out += lot
        if len(lot) < 100:
            break
        p += 1
    res = []
    for x in out:
        u = x["link"].replace("https://www.helloharel.com", "")
        interessante = (u.startswith("/agroalimentaire/")
                        or u.startswith("/fonctionnalites/")
                        or u in ("/", ""))
        if interessante and x["id"] not in PROTEGEES and x["id"] not in PILOTES:
            res.append((x["id"], u or "/"))
    return sorted(res, key=lambda t: t[1])


def traiter(pid, url, poser):
    d = w.get_raw("pages", pid)
    c = d["content"]["raw"]
    el = (d.get("meta") or {}).get("_elementor_data")
    if el not in (None, "", "[]"):
        print("%-46s REFUSEE — _elementor_data non vide" % url[:46])
        return
    depart = c
    notes, tolere = [], []

    c, p1 = etape_reparer(c, notes); tolere += p1
    rf = etape_faq(c, notes)
    if isinstance(rf, tuple):
        c, pf = rf; tolere += pf
    else:
        c = rf
    c = etape_avis(c, notes)
    c = etape_equipe(c, notes)
    c = etape_metiers(c, notes)
    r = etape_fonctionnalites(c, notes)
    if isinstance(r, tuple):
        c, p2 = r; tolere += p2
    else:
        c = r
    c = etape_hero(c, notes)

    if solde(c) != solde(depart):
        print("%-46s REFUSEE — le solde des <div> bouge (%+d -> %+d)"
              % (url[:46], solde(depart), solde(c)))
        return
    if len(c) > PLAFOND:
        print("%-46s REFUSEE — %d ko, au-dela du seuil de rendu" % (url[:46], len(c) // 1024))
        return
    if c.count("<section class=") != depart.count("<section class="):
        print("%-46s REFUSEE — %d sections au lieu de %d"
              % (url[:46], c.count("<section class="), depart.count("<section class=")))
        return
    # Les seuls liens autorises a bouger : ceux qu'une etape retire
    # sciemment, et le /contact/ que le widget de Maxence ajoute.
    reste = liens(depart)
    for x in tolere:
        if x in reste:
            reste.remove(x)
    apres = liens(c)
    if 'class="hh-max"' in c and '/contact/' in apres:
        apres.remove("/contact/")
    if reste != apres:
        manque = sorted(set(reste) - set(apres))
        ajout = sorted(set(apres) - set(reste))
        print("%-46s REFUSEE — liens : -%s +%s"
              % (url[:46], manque[:3] or "0", ajout[:3] or "0"))
        return

    print("%-46s %3d -> %3d ko · %s" % (url[:46], len(depart) // 1024, len(c) // 1024,
                                        " · ".join(notes)))
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % pid), "w", encoding="utf-8").write(depart)
        w.update_content("pages", pid, c, live=True)
        print("%-46s   pose" % "")


def main():
    poser = "--poser" in sys.argv
    une = None
    if "--page" in sys.argv:
        une = int(sys.argv[sys.argv.index("--page") + 1])
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    for pid, url in cibles():
        if une and pid != une:
            continue
        try:
            traiter(pid, url, poser)
        except SystemExit as e:
            print("%-46s ARRET — %s" % (url[:46], e))
        except Exception as e:
            print("%-46s ERREUR — %s: %s" % (url[:46], type(e).__name__, str(e)[:70]))
    if not poser:
        print("\n(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
