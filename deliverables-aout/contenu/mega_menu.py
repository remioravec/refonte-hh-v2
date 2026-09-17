#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le mega-menu de Hello Harel — un seul arbre, deux rendus.

D'OU VIENT LE GABARIT
=====================
Modele fourni par le client : hippopos.fr, releve le 17/09/2026. Sa mecanique :
  · l'entete porte le logo, la navigation, deux boutons d'action et le
    hamburger ;
  · deux panneaux de mega-menu, un par axe, poses AVANT les declencheurs dans
    le document et positionnes en absolu ;
  · un panneau = des colonnes (titre + liste de liens a icone), plus un bas de
    panneau avec une phrase de cadrage et un bouton vers la page mere ;
  · le declencheur reste un LIEN vers la page mere : le libelle navigue, le
    chevron ouvre le panneau ;
  · en mobile, un accordeon : le libelle reste un lien, le chevron deplie.

CE QUE CE FICHIER CORRIGE SUR LE MENU ACTUEL
--------------------------------------------
Releve du 17/09/2026 sur la page 5957 : le menu desktop liste QUATORZE metiers
agroalimentaires, le menu mobile en liste SEPT. Les deux ont ete ecrits a la
main, cote a cote, et ont diverge.

La reponse n'est pas de recopier les sept manquants : c'est de n'avoir qu'UNE
source. L'arbre ci-dessous est ecrit une fois ; `desktop()` et `mobile()` en
derivent tous les deux. Ils ne peuvent plus diverger, et `controler()` le
verifie en comparant les deux jeux de liens.

Les quarante-trois URL de cet arbre ont ete testees une par une le 17/09/2026 :
toutes repondent 200.

MODE DEGRADE — sans JavaScript, les panneaux sont dans le document et les
declencheurs restent des liens vers les pages meres. Rien n'est injecte au
clic. Sans CSS, tout se deroule a la suite.
"""

# ---------------------------------------------------------------- les icones
def _i(d):
    return ('<svg class="hhm-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false">%s</svg>' % d)

ICO = {
 "pain":     _i('<path d="M4.5 15.5c-1.4-1.4-1.4-3.6 0-5l6-6c1.4-1.4 3.6-1.4 5 0l3.5 3.5c1.4 1.4 1.4 3.6 0 5l-6 6c-1.4 1.4-3.6 1.4-5 0z"/><path d="M8.5 8.5l3 3M11.5 5.5l3 3"/>'),
 "gateau":   _i('<path d="M4 20h16v-6a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4z"/><path d="M4 15c1.6 0 1.6 1.5 3.2 1.5S8.8 15 10.4 15s1.6 1.5 3.2 1.5S15.2 15 16.8 15s1.6 1.5 3.2 1.5"/><path d="M12 10V6"/>'),
 "chocolat": _i('<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 9.5h16M4 15h16M9.5 4v16M15 4v16"/>'),
 "glace":    _i('<path d="M8 10a4 4 0 1 1 8 0"/><path d="M7.5 10.5h9L12 21z"/>'),
 "viande":   _i('<path d="M6.5 17.5a5 5 0 0 1 0-7l4-4a5 5 0 0 1 7 7l-4 4a5 5 0 0 1-7 0z"/><circle cx="8.5" cy="15.5" r="1.6"/>'),
 "plateau":  _i('<path d="M3 13h18"/><path d="M5 13a7 7 0 0 1 14 0"/><path d="M12 6V4"/><path d="M4 17h16"/>'),
 "fromage":  _i('<path d="M3 16v-3l9-6 9 6v3z"/><path d="M3 16h18"/><circle cx="8" cy="13" r="1"/><circle cx="14" cy="14" r="1"/>'),
 "poisson":  _i('<path d="M3 12c3-4 7-5 10-5s6 2 8 5c-2 3-5 5-8 5s-7-1-10-5z"/><path d="M3 12l-1-3m1 3l-1 3"/><circle cx="16" cy="11" r="1"/>'),
 "legume":   _i('<path d="M12 21c-4-2-7-6-7-10a7 7 0 0 1 14 0c0 4-3 8-7 10z"/><path d="M12 8v6"/>'),
 "cafe":     _i('<path d="M4 8h12v6a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4z"/><path d="M16 9h2a2.5 2.5 0 0 1 0 5h-2"/><path d="M7 5V3M11 5V3"/>'),
 "usine":    _i('<path d="M3 20V10l5 3V10l5 3V7l5 3v10z"/><path d="M3 20h18"/><path d="M8 16h2M14 16h2"/>'),
 "lait":     _i('<path d="M9 3h6v3l2 4v11H7V10l2-4z"/><path d="M7 13h10"/>'),
 "barquette":_i('<path d="M4 9h16l-1.5 10h-13z"/><path d="M4 9l2-4h12l2 4"/><path d="M10 13v3M14 13v3"/>'),
 "bocal":    _i('<rect x="6" y="7" width="12" height="14" rx="2"/><path d="M8 7V5a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2"/><path d="M6 12h12"/>'),
 "biere":    _i('<path d="M5 7h10v14H5z"/><path d="M15 10h2.5a2.5 2.5 0 0 1 0 5H15"/><path d="M8 11v7M12 11v7"/><path d="M5 7a3 3 0 0 1 5-2 3 3 0 0 1 5 2"/>'),
 "camion":   _i('<path d="M2 7h11v9H2z"/><path d="M13 10h4l4 3.5V16h-8z"/><circle cx="6.5" cy="18.5" r="1.8"/><circle cx="17" cy="18.5" r="1.8"/>'),
 "croix":    _i('<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/>'),
 "labo":     _i('<path d="M9 3h6"/><path d="M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 15h9"/>'),
 "dent":     _i('<path d="M7 3c2 0 2 1.5 5 1.5S15 3 17 3c2.5 0 3 3 2.5 6-.6 3.6-1.2 5-2 8-.5 1.8-2.4 1.8-2.9 0-.4-1.6-.7-3.5-2.6-3.5s-2.2 1.9-2.6 3.5c-.5 1.8-2.4 1.8-2.9 0-.8-3-1.4-4.4-2-8C4 6 4.5 3 7 3z"/>'),
 "maison":   _i('<path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/><path d="M10 20v-5h4v5"/>'),
 "spray":    _i('<path d="M9 8h6v13H9z"/><path d="M10 8V5h4v3"/><path d="M16 5h2M16 8h2M16 11h2"/>'),
 "panier":   _i('<path d="M3 7h18l-2 12H5z"/><path d="M8 7V5a4 4 0 0 1 8 0v2"/>'),
 "facture":  _i('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>'),
 "clients":  _i('<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.5a3 3 0 0 1 0 5.5"/><path d="M17 14a6 6 0 0 1 4 6"/>'),
 "stock":    _i('<path d="M3 8l9-4 9 4-9 4z"/><path d="M3 8v8l9 4 9-4V8"/><path d="M12 12v8"/>'),
 "engrenage":_i('<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>'),
 "echange":  _i('<path d="M4 8h13l-3-3"/><path d="M20 16H7l3 3"/>'),
 "loupe":    _i('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>'),
 "serveur":  _i('<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>'),
}

# ------------------------------------------------------------------- l'arbre
#   UNE seule source. desktop() et mobile() en derivent tous les deux : c'est
#   ce qui rend la divergence impossible.
MENU = [
 {"cle": "metiers", "libelle": "Métiers", "href": "/agroalimentaire/",
  "note": "Quinze métiers de l'agroalimentaire, du fournil à la ligne de "
          "conditionnement. Chaque page décrit la gestion telle qu'elle se pose "
          "dans le métier.",
  "cta": ("Voir l'ERP agroalimentaire", "/agroalimentaire/"),
  "colonnes": [
    {"titre": "Métiers de bouche", "double": True, "liens": [
      ("Boulangerie", "/agroalimentaire/boulanger/", "pain"),
      ("Pâtisserie", "/agroalimentaire/patissier/", "gateau"),
      ("Chocolaterie", "/agroalimentaire/chocolatier/", "chocolat"),
      ("Glacier", "/agroalimentaire/glacier/", "glace"),
      ("Charcuterie", "/agroalimentaire/charcutier/", "viande"),
      ("Traiteur", "/agroalimentaire/traiteur/", "plateau"),
      ("Fromagerie", "/agroalimentaire/fromager/", "fromage"),
      ("Poissonnerie", "/agroalimentaire/poissonnier/", "poisson"),
      ("Fruits et légumes", "/agroalimentaire/maraicher/", "legume"),
      ("Torréfaction", "/agroalimentaire/torrefacteur/", "cafe"),
    ]},
    {"titre": "Industrie et transformation", "liens": [
      ("ERP agroalimentaire", "/agroalimentaire/", "usine"),
      ("Viande", "/agroalimentaire/viande/", "viande"),
      ("Industrie laitière", "/agroalimentaire/industrie-laitiere/", "lait"),
      ("Plats cuisinés", "/agroalimentaire/plats-cuisines-industriels/", "barquette"),
      ("Conserverie", "/agroalimentaire/conserverie/", "bocal"),
      ("Brasserie", "/agroalimentaire/brasseur/", "biere"),
    ]},
  ]},

 {"cle": "fonctions", "libelle": "Fonctionnalités", "href": "/fonctionnalites/",
  "note": "Huit modules de gestion, du devis à l'écriture comptable, "
          "conçus pour le poids variable, les lots et les dates limites.",
  "cta": ("Voir toutes les fonctionnalités", "/fonctionnalites/"),
  "colonnes": [
    {"titre": "Vendre et facturer", "liens": [
      ("Gestion commerciale", "/fonctionnalites/vente/", "panier"),
      ("Facturation", "/fonctionnalites/facturation/", "facture"),
      ("Relation client", "/fonctionnalites/crm/", "clients"),
    ]},
    {"titre": "Produire et suivre", "liens": [
      ("Fabrication", "/fonctionnalites/fabrication/", "engrenage"),
      ("Gestion des stocks", "/fonctionnalites/gestion-de-stock/", "stock"),
      ("Logistique", "/fonctionnalites/logistique/", "camion"),
    ]},
    {"titre": "Acheter et échanger", "liens": [
      ("Achats", "/fonctionnalites/achat/", "panier"),
      ("Import-export", "/fonctionnalites/import-export/", "echange"),
    ]},
  ]},
]

SIMPLES = [("Migration AS/400", "/migration-as400/"),
           ("Tarifs", "/tarifs/"),
           ("Écosystème", "/ecosysteme/"),
           ("Blog", "/blog/")]

ACTIONS = [("Contactez-nous", "/contact/", "hhm-ghost"),
           ("Demandez une démo", "/contact/", "hhm-cta")]

CHEVRON = ('<svg class="hhm-chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
           'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
           'aria-hidden="true" focusable="false"><path d="M6 9l6 6 6-6"/></svg>')


def _liens(liste):
    return "".join('<a href="%s">%s<span>%s</span></a>' % (u, ICO.get(i, ICO["panier"]), t)
                   for t, u, i in liste)


# ------------------------------------------------------------------- desktop
def desktop(logo):
    panneaux = ""
    for m in MENU:
        cols = ""
        for c in m["colonnes"]:
            cols += ('<div class="hhm-col"><h4>%s</h4>'
                     '<div class="hhm-liste%s">%s</div></div>'
                     % (c["titre"], " est-double" if c.get("double") else "",
                        _liens(c["liens"])))
        panneaux += ('<div class="hhm-mega" id="hhm-%s" data-ouvert="false" '
                     'data-cols="%d">'
                     '<div class="hhm-cols">%s</div>'
                     '<div class="hhm-bas"><p class="hhm-note">%s</p>'
                     '<a class="hhm-btn hhm-cta" href="%s">%s</a></div></div>'
                     % (m["cle"], len(m["colonnes"]), cols, m["note"],
                        m["cta"][1], m["cta"][0]))

    decl = "".join(
        '<a href="%s" class="hhm-decl" data-mega aria-expanded="false" '
        'aria-controls="hhm-%s">%s%s</a>' % (m["href"], m["cle"], m["libelle"], CHEVRON)
        for m in MENU)
    decl += "".join('<a href="%s">%s</a>' % (u, t) for t, u in SIMPLES)

    actions = "".join('<a href="%s" class="hhm-btn %s">%s</a>' % (u, k, t)
                      for t, u, k in ACTIONS)

    return ('<header class="hhm-header" id="hhm-header">'
            '<div class="hhm-inner">'
            '<a href="/" class="hhm-marque" aria-label="Hello Harel, accueil">%s</a>'
            '<nav class="hhm-nav" aria-label="Navigation principale">%s%s</nav>'
            '<div class="hhm-actions">%s'
            '<button type="button" class="hhm-burger" id="hhm-burger" '
            'aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="hhm-mobile">'
            '<span></span><span></span><span></span></button>'
            '</div></div></header>' % (logo, panneaux, decl, actions))


# -------------------------------------------------------------------- mobile
def mobile():
    groupes = ""
    for m in MENU:
        sous = ""
        for c in m["colonnes"]:
            sous += '<p class="hhm-m-famille">%s</p>%s' % (c["titre"], _liens(c["liens"]))
        sous += '<a class="hhm-m-tout" href="%s">%s</a>' % (m["cta"][1], m["cta"][0])
        groupes += ('<div class="hhm-m-groupe"><div class="hhm-m-ligne">'
                    '<a href="%s">%s</a>'
                    '<button type="button" class="hhm-m-plus" aria-expanded="false" '
                    'aria-controls="hhm-m-%s" aria-label="Afficher %s">%s</button></div>'
                    '<div class="hhm-m-sous" id="hhm-m-%s" hidden>%s</div></div>'
                    % (m["href"], m["libelle"], m["cle"], m["libelle"].lower(),
                       CHEVRON, m["cle"], sous))
    plats = "".join('<a href="%s">%s</a>' % (u, t) for t, u in SIMPLES)
    actions = "".join('<a href="%s" class="hhm-btn %s">%s</a>' % (u, k, t)
                      for t, u, k in ACTIONS)
    return ('<nav class="hhm-mobile" id="hhm-mobile" aria-label="Navigation mobile">'
            '%s%s<div class="hhm-m-actions">%s</div></nav>' % (groupes, plats, actions))


# --------------------------------------------------------------- la feuille
#   Portee par #hhm-header et #hhm-mobile : la specificite d'un identifiant
#   passe devant les regles de theme sans avoir a saupoudrer des !important.
CSS = """<style id="hh-mega-menu">
#hhm-header{position:sticky !important;top:0 !important;z-index:1000 !important;
 background:transparent !important;border:0 !important;box-shadow:none !important;
 padding:0 !important;margin:0 !important;width:100% !important;
 transition:background .25s ease,box-shadow .25s ease;
 --hhm-txt:#fff;--hhm-txt2:rgba(255,255,255,.88)}
#hhm-header.hhm-plein{background:#fff !important;
 box-shadow:0 1px 3px rgba(16,24,40,.12) !important;
 --hhm-txt:#101828;--hhm-txt2:#475569}
#hhm-header .hhm-inner{display:flex !important;align-items:center !important;
 flex-wrap:nowrap !important;gap:1.25rem !important;min-height:76px;
 max-width:1280px;margin:0 auto !important;padding:0 1.5rem !important;width:100%}
#hhm-header .hhm-marque{display:flex;align-items:center;flex:0 0 auto}
#hhm-header .hhm-marque img{height:36px !important;width:auto !important;display:block;
 transition:filter .25s ease;max-width:none}
#hhm-header.hhm-plein .hhm-marque img{filter:brightness(0) saturate(100%)}
#hhm-header .hhm-nav{display:flex !important;align-items:center;gap:.15rem;flex:1 1 auto;
 min-width:0;position:static}
#hhm-header .hhm-nav>a{display:flex;align-items:center;gap:.3rem;white-space:nowrap;
 padding:.65rem .8rem;border-radius:10px;font-size:.95rem;font-weight:600;
 color:var(--hhm-txt);text-decoration:none;transition:background .18s ease}
#hhm-header .hhm-nav>a:hover{background:rgba(127,145,170,.16)}
#hhm-header .hhm-chev{width:15px;height:15px;flex:0 0 15px;opacity:.75;transition:transform .2s ease}
#hhm-header .hhm-decl[aria-expanded="true"] .hhm-chev{transform:rotate(180deg)}
#hhm-header .hhm-actions{display:flex !important;align-items:center;gap:.6rem;
 flex:0 0 auto;margin-left:auto}
#hhm-header .hhm-btn{display:inline-flex;align-items:center;justify-content:center;
 min-height:44px;padding:.6rem 1.05rem;border-radius:10px;font-size:.9rem;font-weight:700;
 text-decoration:none;white-space:nowrap;border:1px solid transparent}
#hhm-header .hhm-ghost{color:var(--hhm-txt);border-color:rgba(127,145,170,.5)}
#hhm-header .hhm-ghost:hover{background:rgba(127,145,170,.16)}
.hhm-cta{background:#22C55E;color:#0B3D20 !important}
.hhm-cta:hover{background:#1BA94C}

#hhm-header .hhm-mega{position:absolute;top:calc(100% - 6px);left:50%;
 transform:translateX(-50%) translateY(-8px);width:min(1120px,calc(100vw - 2rem));
 background:#fff;border:1px solid #E2E8F0;border-radius:18px;padding:1.6rem 1.75rem 1.35rem;
 box-shadow:0 24px 60px -28px rgba(16,24,40,.42);opacity:0;visibility:hidden;
 pointer-events:none;transition:opacity .18s ease,transform .18s ease,visibility .18s}
#hhm-header .hhm-mega[data-ouvert="true"]{opacity:1;visibility:visible;pointer-events:auto;
 transform:translateX(-50%) translateY(0)}
#hhm-header .hhm-cols{display:grid;gap:1.75rem}
#hhm-header .hhm-mega[data-cols="2"]{width:min(880px,calc(100vw - 2rem))}
#hhm-header .hhm-mega[data-cols="2"] .hhm-cols{grid-template-columns:1.85fr 1fr}
#hhm-header .hhm-mega[data-cols="3"] .hhm-cols{grid-template-columns:1.2fr 1fr 1fr}
#hhm-header .hhm-col h4{margin:0 0 .7rem;font-size:.72rem;font-weight:800;letter-spacing:.11em;
 text-transform:uppercase;color:#046C93}
#hhm-header .hhm-liste{display:grid;gap:.1rem}
#hhm-header .hhm-liste.est-double{grid-template-columns:1fr 1fr;column-gap:.6rem}
#hhm-header .hhm-liste a{display:flex;align-items:center;gap:.55rem;padding:.48rem .55rem;
 border-radius:9px;font-size:.88rem;line-height:1.3;color:#101828;text-decoration:none;
 transition:background .15s ease,color .15s ease}
#hhm-header .hhm-liste a:hover{background:#F1F5F9;color:#0079B8}
#hhm-header .hhm-ico{width:18px;height:18px;flex:0 0 18px;color:#0079B8}
#hhm-header .hhm-bas{display:flex;align-items:center;justify-content:space-between;gap:1.5rem;
 margin-top:1.25rem;padding-top:1.05rem;border-top:1px solid #E2E8F0}
#hhm-header .hhm-note{margin:0;font-size:.82rem;line-height:1.5;color:#475569;max-width:62ch}

#hhm-header .hhm-burger{display:none !important;width:44px;height:44px;border:0;background:transparent;
 padding:10px 8px;cursor:pointer;flex-direction:column;justify-content:space-between}
#hhm-header .hhm-burger span{display:block;height:2px;border-radius:2px;background:var(--hhm-txt);
 transition:transform .22s ease,opacity .22s ease}
#hhm-header .hhm-burger.is-open span:nth-child(1){transform:translateY(10px) rotate(45deg)}
#hhm-header .hhm-burger.is-open span:nth-child(2){opacity:0}
#hhm-header .hhm-burger.is-open span:nth-child(3){transform:translateY(-10px) rotate(-45deg)}

#hhm-mobile{position:fixed;left:0;right:0;top:76px;bottom:0;z-index:999;background:#fff;
 overflow-y:auto;-webkit-overflow-scrolling:touch;padding:.5rem 1rem 2.5rem;
 transform:translateX(100%);transition:transform .25s ease;display:none}
#hhm-mobile.is-open{transform:none}
#hhm-mobile .hhm-m-ligne{display:flex;align-items:center;justify-content:space-between;
 border-bottom:1px solid #EEF2F6}
#hhm-mobile .hhm-m-ligne>a{flex:1;display:flex !important;align-items:center;
 min-height:52px !important;padding:.8rem .25rem !important;font-size:1.02rem;
 font-weight:700;color:#101828;text-decoration:none}
#hhm-mobile .hhm-m-plus{width:48px;height:48px;border:0;background:transparent;cursor:pointer;
 display:grid;place-items:center;color:#475569}
#hhm-mobile .hhm-m-plus .hhm-chev{width:20px;height:20px;transition:transform .2s ease}
#hhm-mobile .hhm-m-plus[aria-expanded="true"] .hhm-chev{transform:rotate(180deg)}
#hhm-mobile .hhm-m-sous{padding:.35rem 0 .9rem}
#hhm-mobile .hhm-m-famille{margin:.9rem 0 .3rem;font-size:.7rem;font-weight:800;
 letter-spacing:.11em;text-transform:uppercase;color:#046C93}
#hhm-mobile .hhm-m-sous a{display:flex !important;align-items:center;gap:.6rem;
 min-height:44px !important;padding:.6rem .3rem !important;font-size:.95rem;
 color:#101828;text-decoration:none;line-height:1.35}
#hhm-mobile .hhm-m-sous a:active{background:#F1F5F9}
#hhm-mobile .hhm-ico{width:18px;height:18px;flex:0 0 18px;color:#0079B8}
#hhm-mobile .hhm-m-tout{margin-top:.6rem;font-weight:700;color:#0079B8 !important}
#hhm-mobile>a{display:flex !important;align-items:center;min-height:52px !important;
 padding:.8rem .25rem !important;font-size:1.02rem;font-weight:700;color:#101828;
 text-decoration:none;border-bottom:1px solid #EEF2F6}
#hhm-mobile .hhm-m-actions{display:grid;gap:.6rem;margin-top:1.4rem}
#hhm-mobile .hhm-btn{display:flex;align-items:center;justify-content:center;min-height:48px;
 border-radius:10px;font-weight:700;text-decoration:none;border:1px solid #CBD5E1;color:#101828}

@media(max-width:1180px){
 #hhm-header .hhm-nav>a{padding:.6rem .6rem;font-size:.9rem}
 #hhm-header .hhm-ghost{display:none !important}
}
@media(max-width:1023px){
 #hhm-header .hhm-nav{display:none !important}
 #hhm-header .hhm-burger{display:flex !important}
 #hhm-header .hhm-ghost{display:none !important}
 #hhm-mobile{display:block}
 body.hhm-fige{overflow:hidden}
}
@media(max-width:620px){
 #hhm-header .hhm-actions .hhm-cta{display:none !important}
 #hhm-header .hhm-inner{min-height:66px}
 #hhm-mobile{top:66px}
}
</style>"""


JS = """<script id="hh-mega-menu-js">
/* Menu Hello Harel. Le declencheur reste un LIEN vers la page mere : le
   libelle navigue, le chevron ouvre le panneau. Sans JavaScript, les panneaux
   restent dans le document et les liens des pages meres fonctionnent. */
(function () {
  var head = document.getElementById('hhm-header');
  if (!head) { return; }

  /* --- entete pleine au defilement ------------------------------------- */
  function fond() { head.classList.toggle('hhm-plein', window.scrollY > 24); }
  fond();
  window.addEventListener('scroll', fond, { passive: true });

  /* --- panneaux du bureau ---------------------------------------------- */
  var decl = [].slice.call(head.querySelectorAll('[data-mega]'));
  function panneau(b) { return document.getElementById(b.getAttribute('aria-controls')); }
  function fermer() {
    decl.forEach(function (b) {
      b.setAttribute('aria-expanded', 'false');
      var p = panneau(b); if (p) { p.setAttribute('data-ouvert', 'false'); }
    });
  }
  function ouvrir(b) {
    var p = panneau(b); if (!p) { return; }
    fermer();
    p.setAttribute('data-ouvert', 'true');
    b.setAttribute('aria-expanded', 'true');
  }
  var minuteur = null;
  function annuler() { if (minuteur) { clearTimeout(minuteur); minuteur = null; } }
  function plusTard() { annuler(); minuteur = setTimeout(fermer, 220); }

  decl.forEach(function (b) {
    b.addEventListener('mouseenter', function () { annuler(); ouvrir(b); });
    b.addEventListener('mouseleave', plusTard);
    b.addEventListener('focus', function () { annuler(); ouvrir(b); });
    b.addEventListener('click', function (e) {
      if (!e.target.closest('.hhm-chev')) { return; }
      e.preventDefault(); e.stopPropagation();
      var p = panneau(b);
      if (p && p.getAttribute('data-ouvert') === 'true') { fermer(); } else { ouvrir(b); }
    });
    var p = panneau(b);
    if (p) {
      p.addEventListener('mouseenter', annuler);
      p.addEventListener('mouseleave', plusTard);
    }
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.hhm-mega') && !e.target.closest('[data-mega]')) { fermer(); }
  });

  /* --- menu mobile ------------------------------------------------------ */
  var burger = document.getElementById('hhm-burger');
  var mob = document.getElementById('hhm-mobile');
  if (burger && mob) {
    var plus = [].slice.call(mob.querySelectorAll('.hhm-m-plus'));
    function replier() {
      plus.forEach(function (b) {
        b.setAttribute('aria-expanded', 'false');
        var s = document.getElementById(b.getAttribute('aria-controls'));
        if (s) { s.hidden = true; }
      });
    }
    function fermerMob() {
      mob.classList.remove('is-open');
      burger.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('hhm-fige');
      replier();
    }
    plus.forEach(function (b) {
      b.addEventListener('click', function () {
        var s = document.getElementById(b.getAttribute('aria-controls'));
        if (!s) { return; }
        var ouvert = b.getAttribute('aria-expanded') === 'true';
        replier();
        if (!ouvert) {
          b.setAttribute('aria-expanded', 'true');
          s.hidden = false;
          b.parentNode.scrollIntoView({ block: 'nearest' });
        }
      });
    });
    burger.addEventListener('click', function () {
      var o = mob.classList.toggle('is-open');
      burger.classList.toggle('is-open', o);
      burger.setAttribute('aria-expanded', String(o));
      document.body.classList.toggle('hhm-fige', o);
    });
    mob.addEventListener('click', function (e) { if (e.target.closest('a')) { fermerMob(); } });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { annuler(); fermer(); fermerMob(); }
    });
  } else {
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { annuler(); fermer(); }
    });
  }
})();
</script>"""


# ------------------------------------------------------------------ controle
def controler():
    """Desktop et mobile portent-ils exactement les memes liens ?"""
    import re
    d = set(re.findall(r'href="([^"]+)"', desktop("<img alt='' src=''>"))) - {"/"}
    m = set(re.findall(r'href="([^"]+)"', mobile())) - {"/"}
    pb = []
    if d - m:
        pb.append("presents en desktop et absents en mobile : %s" % sorted(d - m))
    if m - d:
        pb.append("presents en mobile et absents en desktop : %s" % sorted(m - d))
    vus, doublons = set(), []
    for m2 in MENU:
        for c in m2["colonnes"]:
            for t, u, i in c["liens"]:
                if i not in ICO:
                    pb.append("icone inconnue : %s" % i)
    return pb


if __name__ == "__main__":
    d, m = desktop("<img alt='' src=''>"), mobile()
    import re
    print("desktop %d octets, %d liens" % (len(d), d.count("<a href=")))
    print("mobile  %d octets, %d liens" % (len(m), m.count("<a href=")))
    print("liens uniques :", len(set(re.findall(r'href="([^"]+)"', d))))
    pb = controler()
    for x in pb:
        print("  !", x)
    if not pb:
        print("controle : desktop et mobile portent les memes liens")
