#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose le gabarit d'article sur tout le parc.

CE QUI EST POSE :
  1. la mise en lecture — 17/18 px, une respiration entre les blocs, une
     hierarchie coloree, des tableaux qui deviennent des fiches lisibles
     sur telephone ;
  2. des images sous les H2, choisies par le sujet du titre, jamais deux
     fois la meme dans un article ;
  3. l'appel a l'action « probleme puis reponse », avec une photo du
     quotidien du lecteur ;
  4. les accents des titres.

  5. les vraies questions que le blog cachait dans son JavaScript. Deux
     cent quarante-sept reponses, deja ecrites, n'etaient injectees dans
     la page qu'au clic : aucun moteur ne les a jamais lues. Elles
     deviennent des accordeons HTML, avec leur balisage FAQPage. Huit
     blocs de sources officielles sortent de la meme cachette.

La fausse FAQ — deux cartes de rendez-vous presentees comme des questions,
y compris dans le balisage envoye a Google — est retiree partout, et ses
deux liens passent dans l'appel a l'action.

CE QUI N'EST PAS POSE. Les trente-neuf articles dont le tiroir ne
contenait que les deux cartes n'ont aucune question a montrer. En ecrire
six cents, cela se redige et se relit ; cela ne se genere pas.

Usage :  python3 deployer_blog.py                 (blanc)
         python3 deployer_blog.py --poser         (ecrit)
         python3 deployer_blog.py --un 7761       (un seul)
"""

import os
import re
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
sys.path.insert(0, ICI)
import wp_common as w            # noqa: E402
import ns_api                    # noqa: E402
import deployer_gabarit as D     # noqa: E402
import remanier_agro as RA       # noqa: E402
import blog_lecture as BL        # noqa: E402
import blog_visuels as BV        # noqa: E402
import blog_gabarit as BG        # noqa: E402
import blog_faq_cachee as FC  # noqa: E402
import faq_accordeon as FA    # noqa: E402

SAUV = ("/tmp/claude-0/-home-user-refonte-hh-v2/"
        "b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/blog-parc-avant")
PLAFOND = 275_000


def liens_rdv(c):
    """Les deux liens des cartes de rendez-vous, ou None. On les reconnait
    a leur cible — /demo/ et /contact/ — et non a leur rang : plusieurs
    articles rangeaient des sources officielles avant elles."""
    return FC.extraire(c)[2]


REFERENCE = ("/blog/erp-grossiste-distributeur/",
             "/blog/calculer-le-prix-de-revient-en-boulangerie/")


def _vider_tiroir(c):
    """Le tiroir lateral, son fond noir et son script n'ont plus d'objet."""
    for ident in ('id="faqOverlay"', 'id="faqDrawer"'):
        k = c.find(ident)
        while k >= 0:
            d0 = c.rfind("<div", 0, k)
            if d0 < 0:
                break
            fin = RA.div_complet(c, d0)
            if D.solde(c[d0:fin]) != 0:
                raise SystemExit("bloc de tiroir non clos")
            c = c[:d0] + c[fin:]
            k = c.find(ident)
    for m in list(re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", c, re.S))[::-1]:
        if "faqData" in m.group(1) or "openFaqDrawer" in m.group(1):
            c = c[:m.start()] + c[m.end():]
    return c


def faqpage(paires):
    """Le balisage FAQPage, bati sur de vraies questions."""
    import json as _j
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer",
                            "text": re.sub(r"\s+", " ",
                                           re.sub(r"<[^>]+>", " ", r)).strip()}}
        for q, r in paires]}
    return ('<script type="application/ld+json">%s</script>'
            % _j.dumps(ld, ensure_ascii=False))


def remplacer_faq(c, url, notes):
    """La fausse FAQ s'en va ; les vraies questions prennent sa place.

    Le tiroir contenait trois natures de choses melangees : de vraies
    questions deja redigees, un bloc de sources officielles, et deux cartes
    de rendez-vous que le balisage presentait a Google comme des questions.
    On separe les trois, et chacune part ou elle doit."""
    questions, sources, liens = FC.extraire(c)
    i = c.find('<section class="faq-section"')
    if i < 0:
        return c, liens
    j = c.find("</section>", i) + len("</section>")
    c = c[:i] + c[j:]
    c = _vider_tiroir(c)
    # Le balisage en place decrivait une FAQ que la page ne montrait pas —
    # et, sur cinquante articles, presentait deux cartes de rendez-vous
    # comme des questions. Il s'en va en entier ; un seul le remplacera,
    # adosse a des reponses reellement presentes dans le HTML.
    n = 0
    for m in list(re.finditer(
            r'<script type="application/ld\+json">(?:(?!</script>).)*?</script>',
            c, re.S))[::-1]:
        if "FAQPage" in m.group(0):
            c = c[:m.start()] + c[m.end():]
            n += 1
    if n:
        notes.append("balisage FAQPage sans reponse visible retire")

    if url in REFERENCE:
        # Ces deux-la portent le gabarit valide, avec leur propre FAQ
        # visible. On ne leur en ajoute pas une seconde : on leur rend
        # seulement le balisage que la fausse FAQ leur avait pris.
        k = c.find('<h2 id="s-faq"')
        fin = c.find("<h2", k + 10)
        bloc = c[k:fin if fin > 0 else len(c)]
        vis = [(re.sub(r"<[^>]+>", "", q).strip(), r)
               for q, r in re.findall(r"<h3[^>]*>(.*?)</h3>(.*?)(?=<h3|$)", bloc, re.S)]
        if vis:
            c = c[:fin] + faqpage(vis) + c[fin:]
            notes.append("balisage FAQPage refait sur %d question(s) visibles" % len(vis))
        return c, liens

    ajout = ""
    if questions:
        ajout += BG.bloc_faq(FC.ENTETE % FC.chapeau(url), questions, FA.CSS)
        notes.append("%d question(s) sorties du JavaScript" % len(questions))
    if sources:
        ajout += FC.bloc_sources(sources)
        notes.append("bloc de sources rendu visible")
    if ajout:
        c = c[:i] + ajout + c[i:]
    if liens:
        notes.append("fausse FAQ retiree")
    return c, liens


def lire(pid):
    """Le proxy tronque un transfert de temps en temps. On redemande."""
    dernier = None
    for _ in range(4):
        try:
            return w.get_raw("posts", pid)["content"]["raw"]
        except Exception as e:          # noqa: BLE001
            dernier = e
            time.sleep(3)
    raise dernier


def traiter(pid, url, poser):
    c = lire(pid)
    depart = c
    notes = []

    deja_faq = "<details" in c
    if "var faqData" in c:
        c, L = remplacer_faq(c, url, notes)
    else:
        m = re.search(r'<section class="hhb-acc">.*?</section>', c, re.S)
        L = re.findall(r'href="([^"]+)"', m.group(0))[:2] if m else None
        if m:
            c = c[:m.start()] + c[m.end():]
    if not L or len(L) < 2:
        L = ["/demo/", "/contact/"]
        notes.append("liens de rendez-vous par defaut")

    if url in REFERENCE:
        # Le gabarit « prix de revient », valide par ailleurs, porte deja sa
        # mise en lecture, ses visuels et sa FAQ. On ne lui superpose rien.
        controler(depart, c, [], deja_faq)
        rendre(pid, url, depart, c, notes, poser)
        return

    # ── les images sous les H2 ───────────────────────────────────────────
    i = c.find('<article class="hha-art"')
    j = c.find("</article>", i)
    if i < 0 or j < 0:
        raise SystemExit("corps d'article introuvable")
    corps = c[i:j]
    corps = re.sub(r'<figure class="hhb-img">.*?</figure>', "", corps, flags=re.S)
    h2 = list(re.finditer(r"<h2[^>]*>(.*?)</h2>", corps, re.S))
    titres = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() for m in h2]
    themes = BV.repartir(titres)
    n_img = 0
    for m, th in list(zip(h2, themes))[::-1]:
        if not th:
            continue
        corps = corps[:m.end()] + BV.figure(th) + corps[m.end():]
        n_img += 1
    c = c[:i] + corps + c[j:]
    notes.append("%d image(s)" % n_img)

    # ── l'appel a l'action ───────────────────────────────────────────────
    theme = BV.theme_du_titre(" ".join(titres[:2])) or "defaut"
    fin_art = c.find("</article>", c.find('<article class="hha-art"')) + len("</article>")
    c = c[:fin_art] + BV.bloc_accroche(theme, L[0], L[1]) + c[fin_art:]
    notes.append("accroche « %s »" % theme)

    # ── tableaux, accents, feuilles ──────────────────────────────────────
    c, n_tab = BL.etiqueter_tableaux(c)
    c, n_acc = BV.__dict__.get("accentuer_titres", BG.accentuer_titres)(c)
    if n_tab:
        notes.append("%d tableau(x)" % n_tab)
    if n_acc:
        notes.append("%d titre(s) reaccentue(s)" % n_acc)
    for ident, feuille in (("hh-blog-lecture", BL.CSS), ("hh-blog-visuels", BV.CSS)):
        if '<style id="%s">' % ident in c:
            c = re.sub(r'<style id="%s">.*?</style>' % ident, feuille, c, flags=re.S)
        else:
            k = c.find('<article class="hha-art"')
            c = c[:k] + feuille + c[k:]

    controler(depart, c, L, deja_faq)
    rendre(pid, url, depart, c, notes, poser)


def controler(depart, c, L, deja_faq):
    if D.solde(c) != D.solde(depart):
        raise SystemExit("le solde des <div> bouge (%+d -> %+d)"
                         % (D.solde(depart), D.solde(c)))
    perdus = [x for x in D.liens(depart) if x not in D.liens(c)]
    perdus = [x for x in perdus if x not in L]
    if perdus:
        raise SystemExit("lien(s) perdu(s) : %s" % perdus[:3])
    for x in L:
        if x not in D.liens(c):
            raise SystemExit("lien de rendez-vous perdu : %s" % x)
    if len(c) > PLAFOND:
        raise SystemExit("%d ko, au-dela du seuil de rendu" % (len(c) // 1024))
    if "hha-tool" in depart and "hha-tool" not in c:
        raise SystemExit("le simulateur a disparu")
    if deja_faq and c.count("<details") < depart.count("<details"):
        raise SystemExit("la vraie FAQ a bouge")
    n_ld = len(re.findall(r'"@type": ?"FAQPage"', c))
    if n_ld > 1:
        raise SystemExit("%d balisages FAQPage sur la meme page" % n_ld)


def rendre(pid, url, depart, c, notes, poser):
    print("%-52s %3d -> %3d ko · %s" % (url[:52], len(depart) // 1024,
                                        len(c) // 1024, " · ".join(notes)))
    if poser:
        os.makedirs(SAUV, exist_ok=True)
        open(os.path.join(SAUV, "avant-%d.html" % pid), "w",
             encoding="utf-8").write(depart)
        w.update_content("posts", pid, c, live=True)


def main():
    poser = "--poser" in sys.argv
    un = int(sys.argv[sys.argv.index("--un") + 1]) if "--un" in sys.argv else None
    print("mode :", "POSE REELLE" if poser else "blanc (aucune ecriture)", "\n")
    arts, p = [], 1
    while True:
        lot = ns_api.call("wp/v2/posts?per_page=100&page=%d&status=publish&_fields=id,link" % p)
        if not lot:
            break
        arts += lot
        if len(lot) < 100:
            break
        p += 1
    ok = ko = 0
    for a in sorted(arts, key=lambda x: x["link"]):
        u = a["link"].replace("https://www.helloharel.com", "")
        if un and a["id"] != un:
            continue
        try:
            traiter(a["id"], u, poser)
            ok += 1
        except SystemExit as e:
            print("%-52s ARRET — %s" % (u[:52], e)); ko += 1
        except Exception as e:
            print("%-52s ERREUR — %s: %s" % (u[:52], type(e).__name__, str(e)[:60])); ko += 1
    print("\n%d article(s) traite(s), %d en defaut" % (ok, ko))
    if not poser:
        print("(blanc — rien n'a ete ecrit)")


if __name__ == "__main__":
    main()
