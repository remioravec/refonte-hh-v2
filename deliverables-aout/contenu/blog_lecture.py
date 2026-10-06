#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
La mise en lecture du corps d'article. Mesuree avant d'etre ecrite.

CE QUI A ETE CONSTATE sur telephone, chiffres a l'appui :
  · les paragraphes ont une marge basse de 0 px. Ils se touchent. C'est
    le mur de texte dont Remi parle ;
  · un tableau de six colonnes dans 296 px coupe les mots en morceaux :
    « Carrefo ur », « dereference ment », « minimu m », « souven t » ;
  · les infographies s'enroulent, et les fleches se retrouvent en bout de
    ligne a pointer vers le vide ;
  · le bloc d'appel a l'action est entierement souligne, sans couleur ni
    bouton, parce que la carte entiere est un lien ;
  · zero image sur 30 000 px de defilement.

CE QUE FAIT CETTE FEUILLE. Elle ne touche pas au texte. Elle lui donne un
rythme : une respiration entre les blocs, une mesure de ligne tenue, une
hierarchie coloree, des tableaux lisibles et des etapes qui descendent au
lieu de s'enrouler.

Elle porte un !important sur chaque declaration : le theme en pose partout,
et une regle sans poids ne s'applique tout simplement pas. Lecon du 22/09.
"""

# ── le code couleur, un seul jeu pour tout le corps ───────────────────────
ENCRE = "#0f172a"      # les titres
TEXTE = "#334155"      # le corps
DOUX = "#64748b"       # les mentions secondaires
ACCENT = "#0369A1"     # le bleu qui structure
VIF = "#00B1F5"        # le bleu qui signale
BORD = "#e2e8f0"
FOND = "#F8FAFC"

CSS = """<style id="hh-blog-lecture">
/* ═══ 1. LE RYTHME DE LECTURE ═══════════════════════════════════════════
   Le defaut mesure : 11,8 px de police et 0 px de marge entre paragraphes.
   On remonte a 17 px et on rend aux blocs l'air qui leur manquait. */
.hha-art{--mes:68ch;color:%(TEXTE)s !important;
 font-size:17px !important;line-height:1.72 !important}
.hha-art p{margin:0 0 1.15em !important;max-width:var(--mes) !important;
 font-size:inherit !important;line-height:inherit !important;color:inherit !important}
.hha-art p:last-child{margin-bottom:0 !important}
.hha-art strong,.hha-art b{color:%(ENCRE)s !important;font-weight:650 !important}
.hha-art em{font-style:italic !important}

/* ═══ 2. LA HIERARCHIE ══════════════════════════════════════════════════
   Un H2 se voit de loin : un filet de couleur a gauche, et de l'air
   au-dessus. Un H3 se distingue par la couleur, pas par la taille seule. */
.hha-art h2{position:relative !important;margin:2.9rem 0 1rem !important;
 padding:0 0 0 .95rem !important;font-size:1.48rem !important;
 line-height:1.28 !important;font-weight:800 !important;
 color:%(ENCRE)s !important;letter-spacing:-.015em !important;
 max-width:var(--mes) !important}
.hha-art h2::before{content:"";position:absolute;left:0;top:.16em;bottom:.16em;
 width:4px;border-radius:4px;background:%(VIF)s}
.hha-art h2:first-child{margin-top:0 !important}
.hha-art h3{margin:2rem 0 .6rem !important;font-size:1.13rem !important;
 line-height:1.35 !important;font-weight:700 !important;
 color:%(ACCENT)s !important;max-width:var(--mes) !important}
.hha-art h4{margin:1.5rem 0 .5rem !important;font-size:1.02rem !important;
 font-weight:700 !important;color:%(ENCRE)s !important}

/* ═══ 3. LES LISTES ═════════════════════════════════════════════════════ */
.hha-art ul,.hha-art ol{margin:0 0 1.3em !important;padding:0 0 0 .2rem !important;
 max-width:var(--mes) !important;list-style:none !important}
.hha-art ul>li,.hha-art ol>li{position:relative !important;
 margin:0 0 .65em !important;padding:0 0 0 1.55rem !important;
 line-height:1.68 !important;color:inherit !important}
.hha-art ul>li::before{content:"";position:absolute;left:.25rem;top:.62em;
 width:7px;height:7px;border-radius:50%;background:%(VIF)s}
.hha-art ol{counter-reset:hhli}
.hha-art ol>li{counter-increment:hhli}
.hha-art ol>li::before{content:counter(hhli);position:absolute;left:0;top:.1em;
 display:grid;place-items:center;width:1.15rem;height:1.15rem;
 border-radius:50%;background:#E0F2FE;color:%(ACCENT)s;
 font-size:.72rem;font-weight:800}

/* ═══ 4. LES LIENS DANS LE TEXTE ════════════════════════════════════════ */
.hha-art p a,.hha-art li a{color:%(ACCENT)s !important;font-weight:600 !important;
 text-decoration:underline !important;text-underline-offset:3px !important;
 text-decoration-thickness:1px !important;
 text-decoration-color:rgba(3,105,161,.35) !important}
.hha-art p a:hover,.hha-art li a:hover{
 text-decoration-color:%(ACCENT)s !important}

/* ═══ 5. LES TABLEAUX ═══════════════════════════════════════════════════
   Six colonnes dans 296 px coupaient les mots lettre par lettre. Sur
   telephone chaque ligne devient une fiche, avec l'intitule de colonne
   en face de sa valeur. L'ordinateur garde le tableau. */
.hha-tab{margin:0 0 1.5em !important;max-width:100% !important}
.hha-art table{width:100% !important;border-collapse:collapse !important;
 font-size:.95rem !important;margin:0 !important}
.hha-art th{background:%(ENCRE)s !important;color:#fff !important;
 font-weight:700 !important;text-align:left !important;
 padding:.7rem .85rem !important;font-size:.88rem !important;
 line-height:1.35 !important}
.hha-art td{padding:.7rem .85rem !important;border-bottom:1px solid %(BORD)s !important;
 color:%(TEXTE)s !important;line-height:1.55 !important;vertical-align:top !important}
.hha-art tbody tr:nth-child(even) td{background:%(FOND)s !important}
@media (max-width:760px){
 .hha-art table,.hha-art thead,.hha-art tbody,.hha-art tr,
 .hha-art th,.hha-art td{display:block !important}
 .hha-art thead{position:absolute !important;width:1px !important;height:1px !important;
  overflow:hidden !important;clip:rect(0 0 0 0) !important}
 .hha-art tbody tr{margin:0 0 .85rem !important;background:#fff !important;
  border:1px solid %(BORD)s !important;border-radius:14px !important;
  overflow:hidden !important}
 .hha-art tbody tr:nth-child(even) td{background:transparent !important}
 .hha-art td{display:grid !important;grid-template-columns:minmax(0,1fr) !important;
  gap:.15rem !important;padding:.7rem .9rem !important;
  border-bottom:1px solid #EEF2F7 !important}
 .hha-art td:last-child{border-bottom:0 !important}
 .hha-art td::before{content:attr(data-l);display:block !important;
  font-size:.72rem !important;font-weight:800 !important;
  letter-spacing:.07em !important;text-transform:uppercase !important;
  color:%(DOUX)s !important}
 .hha-art td:first-child{background:%(FOND)s !important}
 .hha-art td:first-child::before{color:%(ACCENT)s !important}
}

/* ═══ 6. LES ETAPES ═════════════════════════════════════════════════════
   Les pastilles s'enroulaient et les fleches pointaient vers le vide en
   bout de ligne. Sur telephone elles descendent, reliees par un trait. */
@media (max-width:760px){
 .hha-cycle{display:grid !important;grid-template-columns:1fr !important;
  gap:0 !important;justify-items:stretch !important}
 .hha-cycle>*{margin:0 !important}
 .hha-cycle>*:not(:last-child){position:relative !important;
  margin-bottom:1.6rem !important}
 .hha-cycle>*:not(:last-child)::after{content:"";position:absolute;
  left:50%;transform:translateX(-50%);bottom:-1.25rem;
  width:2px;height:.9rem;background:#BAE6FD;border-radius:2px}
 .hha-cycle svg{display:none !important}
}

/* ═══ 7. L'APPEL A L'ACTION ═════════════════════════════════════════════
   L'ancien etait souligne de part en part, sans couleur ni bouton, parce
   que la carte entiere etait un lien. Celui-ci a un bouton. */
.hhb-cta{max-width:var(--mes) !important;margin:2.6rem auto 0 !important;
 display:grid !important;grid-template-columns:1fr !important;
 gap:.9rem !important;padding:0 !important;list-style:none !important}
@media (min-width:720px){.hhb-cta{grid-template-columns:1fr 1fr !important}}
.hhb-cta li{margin:0 !important;padding:0 !important}
.hhb-cta li::before{display:none !important}
.hhb-cta .hhb-c{display:flex !important;flex-direction:column !important;
 height:100% !important;padding:1.35rem 1.4rem 1.25rem !important;
 background:#fff !important;border:1px solid %(BORD)s !important;
 border-radius:18px !important;text-decoration:none !important;
 box-shadow:0 12px 30px -26px rgba(15,23,42,.5) !important;
 transition:border-color .18s,box-shadow .18s,transform .18s !important}
.hhb-cta .hhb-c:hover{border-color:%(VIF)s !important;
 transform:translateY(-2px) !important;
 box-shadow:0 20px 40px -28px rgba(15,23,42,.6) !important}
.hhb-cta b{display:block !important;color:%(ENCRE)s !important;
 font-size:1.06rem !important;font-weight:800 !important;
 line-height:1.3 !important;margin:0 0 .4rem !important;
 text-decoration:none !important}
.hhb-cta span{display:block !important;color:%(TEXTE)s !important;
 font-size:.94rem !important;line-height:1.6 !important;
 margin:0 0 1rem !important;text-decoration:none !important}
.hhb-cta .hhb-b{display:inline-flex !important;align-items:center !important;
 gap:.45rem !important;margin-top:auto !important;align-self:flex-start !important;
 padding:.68rem 1.25rem !important;border-radius:999px !important;
 background:%(ACCENT)s !important;color:#fff !important;
 font-style:normal !important;font-weight:700 !important;font-size:.92rem !important;
 text-decoration:none !important}
.hhb-cta .hhb-b2{background:#fff !important;color:%(ACCENT)s !important;
 border:1.5px solid %(ACCENT)s !important}
.hhb-cta-t{max-width:var(--mes) !important;margin:3rem auto .3rem !important;
 font-size:1.42rem !important;font-weight:800 !important;
 color:%(ENCRE)s !important;padding:0 !important}
.hhb-cta-t::before{display:none !important}

/* ═══ 8. L'AIR AUTOUR DU CORPS, SUR TELEPHONE ═══════════════════════════ */
@media (max-width:760px){
 .hha-art{font-size:17px !important;padding:0 2px !important}
 .hha-art h2{font-size:1.34rem !important;margin-top:2.4rem !important}
 .hha-art h3{font-size:1.08rem !important;margin-top:1.75rem !important}
 .hha-art p,.hha-art li{max-width:none !important}
}
@media (min-width:980px){
 .hha-art{font-size:18px !important}
 .hha-art h2{font-size:1.62rem !important}
}
@media (prefers-reduced-motion:reduce){
 .hhb-cta .hhb-c{transition:none !important}
 .hhb-cta .hhb-c:hover{transform:none !important}
}
</style>"""

# Pas de formatage par % sur une feuille de style : elle est pleine de %
# — 50 %, 100 % — et melanger les deux est le piege dans lequel on tombe a
# chaque fois. On remplace des jetons, et une garde refuse le resultat s'il
# en reste un.
for _jeton, _valeur in (("%(ENCRE)s", ENCRE), ("%(TEXTE)s", TEXTE),
                        ("%(DOUX)s", DOUX), ("%(ACCENT)s", ACCENT),
                        ("%(VIF)s", VIF), ("%(BORD)s", BORD), ("%(FOND)s", FOND)):
    CSS = CSS.replace(_jeton, _valeur)
if "%(" in CSS:
    import re as _r
    raise SystemExit("ARRET — jeton non remplace : %s"
                     % _r.findall(r"%\([a-zA-Z]+\)s", CSS)[:3])


# Le theme pose ses marges avec un selecteur porte par #hh-page, qui l'emporte
# sur une classe seule. Chaque regle est donc doublee : une version simple, et
# une version prefixee par #hh-page qui gagne a coup sur. Constate au rendu —
# la police passait bien a 17 px, mais la marge des paragraphes restait a zero.
def _doubler(feuille):
    sortie = []
    for bloc in feuille.split("\n"):
        t = bloc.strip()
        if (t.startswith(("/*", "*", "@", "}")) or not t or "{" not in t
                or t.startswith("<style") or t.startswith("</style")):
            sortie.append(bloc)
            continue
        sel, reste = bloc.split("{", 1)
        if "#hh-page" in sel:
            sortie.append(bloc)
            continue
        parts = [x.strip() for x in sel.split(",") if x.strip()]
        double = ", ".join(parts + ["#hh-page " + x for x in parts])
        sortie.append(double + "{" + reste)
    return "\n".join(sortie)


CSS = _doubler(CSS)



def etiqueter_tableaux(c):
    """Donne a chaque cellule l'intitule de sa colonne.

    Sans cela, une ligne repliee en fiche sur telephone n'est qu'une pile
    de valeurs sans nom. L'intitule vient de l'en-tete du tableau, il n'est
    pas invente.
    """
    import re as _re
    n = [0]

    def par_tableau(m):
        t = m.group(0)
        entetes = [_re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", "", x)).strip()
                   for x in _re.findall(r"<th[^>]*>(.*?)</th>", t, _re.S)]
        if not entetes:
            return t
        def par_ligne(mm):
            ligne, k = mm.group(0), [0]
            def par_cellule(mc):
                i = k[0]; k[0] += 1
                if i >= len(entetes) or 'data-l=' in mc.group(1):
                    return mc.group(0)
                return "<td%s data-l=\"%s\">" % (mc.group(1), entetes[i].replace('"', "'"))
            return _re.sub(r"<td([^>]*)>", par_cellule, ligne)
        t2 = _re.sub(r"<tr[^>]*>.*?</tr>", par_ligne, t, flags=_re.S)
        if t2 != t:
            n[0] += 1
        return '<div class="hha-tab">%s</div>' % t2

    c = _re.sub(r"<table[^>]*>.*?</table>", par_tableau, c, flags=_re.S)
    return c, n[0]
