# -*- coding: utf-8 -*-
"""
Une fiche visuelle par MIN — dix-sept, generees, pas photographiees.

Pourquoi pas des photos : dix-sept photos de marches de gros achetees en
banque d'images se ressemblent toutes et ne disent rien du marche. Une fiche
porte la donnee du marche : sa commune reelle, sa superficie, son tonnage, sa
densite et ce qu'on cherche a son sujet. C'est ce qui distingue la page.

Chaque fiche est un lien vers la page du marche — les dix-sept filles a
produire. Tout est en HTML et CSS : net a toutes les densites, quelques
kilo-octets, et la donnee se met a jour au lieu de se refaire.

Portee doublee sous #hh-page et sans.
"""

import min_data as D

BASE = "/negoce/marches-interet-national/"

# une teinte par region, pour que les dix-sept se lisent comme une collection
TEINTES = {
    "Île-de-France": ("#00B1F5", "#e6f7fe"),
    "Provence-Alpes-Côte d'Azur": ("#F97316", "#fff4ed"),
    "Occitanie": ("#EF4444", "#fef2f2"),
    "Pays de la Loire": ("#16DB7F", "#e9fbf2"),
    "Nouvelle-Aquitaine": ("#A855F7", "#f8f1ff"),
    "Auvergne-Rhône-Alpes": ("#0EA5E9", "#eaf7fe"),
    "Normandie": ("#14B8A6", "#e8faf7"),
    "Grand Est": ("#64748B", "#f2f5f8"),
}


def _double(sel):
    out = []
    for x in sel.split(","):
        x = x.strip()
        if x:
            out.append("#hh-page " + x)
            out.append(x)
    return ", ".join(out)


def _regles(css):
    out = []
    for b in css.split("}"):
        if "{" not in b:
            out.append(b)
            continue
        s, c = b.split("{", 1)
        out.append(_double(s) + "{" + c + "}")
    return "".join(out)


def _sc(css):
    import re
    out, i = [], 0
    for m in re.finditer(r"@media[^{]*\{", css):
        out.append(_regles(css[i:m.start()]))
        prof, j = 1, m.end()
        while j < len(css) and prof:
            prof += 1 if css[j] == "{" else (-1 if css[j] == "}" else 0)
            j += 1
        out.append(m.group(0) + _regles(css[m.end():j - 1]) + "}")
        i = j
    out.append(_regles(css[i:]))
    return "".join(out)


CSS = "<style id=\"hh-min-fiches\">" + _sc("""
.fch{display:grid;grid-template-columns:repeat(auto-fill,minmax(238px,1fr));gap:.9rem;
 margin:0 !important}
.fc{display:flex;flex-direction:column;border:1px solid #e2e8f0;border-radius:16px;
 background:#fff;overflow:hidden;text-decoration:none;color:inherit;
 transition:border-color .18s ease,box-shadow .18s ease,transform .18s ease}
.fc:hover,.fc:focus-visible{border-color:#00B1F5;box-shadow:0 14px 30px -20px rgba(15,23,42,.5);
 transform:translateY(-2px)}
.fc:focus-visible{outline:2px solid #0f172a;outline-offset:2px}
.fc-top{padding:.85rem 1rem;border-bottom:1px solid #eef2f6}
.fc-reg{display:inline-block;font-size:.62rem;font-weight:800;letter-spacing:.08em;
 text-transform:uppercase;padding:.2rem .5rem;border-radius:99px;margin:0 0 .45rem !important}
.fc-n{display:block;font-size:1.02rem;font-weight:700;color:#0f172a;line-height:1.25;
 letter-spacing:-.015em}
.fc-c{display:block;font-size:.76rem;color:#64748b;margin-top:.15rem}
.fc-b{padding:.85rem 1rem;display:flex;flex-direction:column;gap:.6rem;flex:1}
.fc-t{display:flex;align-items:baseline;gap:.4rem}
.fc-t b{font-size:1.45rem;font-weight:800;color:#0f172a;letter-spacing:-.03em;
 font-variant-numeric:tabular-nums;line-height:1}
.fc-t span{font-size:.72rem;color:#64748b}
.fc-bar{height:6px;border-radius:99px;background:#f1f5f9;overflow:hidden}
.fc-bar i{display:block;height:100%;border-radius:99px}
.fc-g{display:grid;grid-template-columns:1fr 1fr;gap:.4rem .6rem;font-size:.72rem;
 color:#64748b;margin-top:.1rem}
.fc-g b{display:block;color:#0f172a;font-weight:700;font-variant-numeric:tabular-nums;
 font-size:.86rem}
.fc-w{font-size:.7rem;color:#96650E;background:#fef6e6;border-radius:8px;padding:.45rem .6rem;
 line-height:1.45}
.fc-go{display:flex;align-items:center;justify-content:space-between;gap:.5rem;
 padding:.7rem 1rem;border-top:1px solid #eef2f6;background:#f8fafc;font-size:.78rem;
 font-weight:600;color:#046C93;margin-top:auto}
.fc-go::after{content:"→";font-weight:400}
.fch-lg{display:flex;flex-wrap:wrap;gap:.5rem 1rem;font-size:.74rem;color:#64748b;
 margin:1rem 0 0 !important}
.fch-lg span{display:inline-flex;align-items:center;gap:.35rem}
.fch-lg i{width:9px;height:9px;border-radius:50%;flex:0 0 auto}
@media(max-width:520px){.fch{grid-template-columns:1fr}}
""") + "</style>"


def _fmt(n):
    return format(n, ",d").replace(",", " ") if n else "—"


def fiche(m):
    cle, nom, commune, region, ha, tonn, vol, site, reserve = m
    fort, doux = TEINTES.get(region, ("#64748B", "#f2f5f8"))
    maxi = max(x[5] for x in D.avec_donnees())
    part = (tonn / maxi * 100) if tonn else 0
    de = D.densite(m)

    bar = ('<div class="fc-bar"><i style="width:%.1f%%;background:%s"></i></div>' % (part, fort)
           if tonn else '')
    tete = ('<div class="fc-t"><b>%s</b><span>tonnes par an</span></div>' % _fmt(tonn)
            if tonn else '<div class="fc-t"><b>—</b><span>tonnage non publié</span></div>')
    grille = ('<div class="fc-g"><span>Superficie<b>%s ha</b></span>'
              '<span>Densité<b>%s</b></span>'
              '<span>Recherches<b>%s /mois</b></span>'
              '<span>Site<b>%s</b></span></div>'
              % (("%g" % ha) if ha else "—",
                 ("%s t/ha" % _fmt(round(de))) if de else "—",
                 _fmt(vol) if vol else "—",
                 "officiel" if site else "—"))
    res = '<p class="fc-w">%s</p>' % reserve if reserve else ''
    return ('<a class="fc" href="%s%s/">'
            '<div class="fc-top" style="background:%s">'
            '<span class="fc-reg" style="background:#fff;color:%s">%s</span>'
            '<span class="fc-n">%s</span><span class="fc-c">%s</span></div>'
            '<div class="fc-b">%s%s%s%s</div>'
            '<span class="fc-go">Voir le marché</span></a>'
            % (BASE, cle, doux, fort, region, nom, commune, tete, bar, grille, res))


def toutes():
    cartes = "".join(fiche(m) for m in D.MIN)
    lg = "".join('<span><i style="background:%s"></i>%s</span>' % (TEINTES[r][0], r)
                 for r in TEINTES)
    return ('<div class="fch">' + cartes + '</div>'
            '<p class="fch-lg">' + lg + '</p>')
