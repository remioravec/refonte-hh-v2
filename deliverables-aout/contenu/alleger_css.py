#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retirer d'une feuille les regles qui ne peignent plus rien.

La page pilier traine cent vingt-huit kilo-octets de style pour onze
sections. Une bonne part vise des blocs retires depuis longtemps.

Le danger est connu : une classe posee par le JavaScript — .revealed,
.open, .scrolled — n'apparait nulle part dans le balisage servi. La
supprimer casserait une animation sans qu'aucun controle statique ne le
voie. On considere donc comme vivante toute chaine citee dans un script
de la page, en plus de ce que porte le balisage.

Regles de prudence, toutes appliquees :
  * une regle n'est retiree que si AUCUN de ses selecteurs ne trouve
    preneur — « .a, .b » survit des que .b existe ;
  * les blocs @media, @font-face, @keyframes et les regles sans classe
    ni identifiant ne sont jamais touches ;
  * le nombre d'accolades ouvrantes et fermantes est verifie avant et
    apres.
"""

import re

GARDE = ("@",)
# Enveloppes de page : presentes partout, elles ne discriminent rien.
ENVELOPPES = {"hh-page", "hh-app", "page", "content", "main"}


def vivants(contenu):
    """Ce que le balisage porte, plus ce que les scripts nomment."""
    mk = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", contenu, flags=re.S)
    cl = set()
    for x in re.findall(r'class="([^"]*)"', mk):
        cl.update(x.split())
    ids = set(re.findall(r'id="([^"]+)"', mk))
    js = set()
    for m in re.finditer(r"<script(?![^>]*src)[^>]*>(.*?)</script>", contenu, re.S):
        js.update(re.findall(r"['\"]([A-Za-z][\w-]{1,40})['\"]", m.group(1)))
        js.update(re.findall(r"[.#]([A-Za-z][\w-]{1,40})", m.group(1)))
    return cl | js, ids | js


def decouper(css):
    """Les regles de premier niveau, accolades equilibrees."""
    out, prof, debut = [], 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            prof += 1
        elif ch == "}":
            prof -= 1
            if prof == 0:
                out.append(css[debut:i + 1])
                debut = i + 1
    if debut < len(css):
        out.append(css[debut:])
    return out


def alleger(contenu, mini=20000):
    """Retire les regles mortes des feuilles d'au moins `mini` octets."""
    cl, ids = vivants(contenu)
    gagne, n = 0, 0
    for m in list(re.finditer(r"<style([^>]*)>(.*?)</style>", contenu, re.S))[::-1]:
        css = m.group(2)
        if len(css) < mini:
            continue
        garde = []
        for r in decouper(css):
            sel = r.split("{", 1)[0]
            if sel.strip().startswith(GARDE):
                garde.append(r)
                continue
            c2 = set(re.findall(r"\.([a-zA-Z][\w-]+)", sel))
            # Le theme prefixe chaque regle de « #hh-page ». Juger sur les
            # identifiants reviendrait a tout garder, cette enveloppe etant
            # toujours presente : des qu'une regle porte des classes, ce
            # sont elles qui decident.
            i2 = set(re.findall(r"#([a-zA-Z][\w-]+)", sel)) - ENVELOPPES
            if c2:
                vivant = bool(c2 & cl)
            elif i2:
                vivant = bool(i2 & ids)
            else:
                vivant = True
            if vivant:
                garde.append(r)
            else:
                gagne += len(r)
                n += 1
        neuve = "".join(garde)
        if neuve.count("{") != neuve.count("}"):
            raise SystemExit("ARRET — accolades desequilibrees apres allegement")
        contenu = contenu[:m.start(2)] + neuve + contenu[m.end(2):]
    return contenu, n, gagne
