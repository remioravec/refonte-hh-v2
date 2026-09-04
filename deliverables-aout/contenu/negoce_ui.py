# -*- coding: utf-8 -*-
"""
Kit d'interface de la variante C — les ecrans du logiciel rebatis en HTML et CSS.

La variante B montre des captures matricielles. Ici les memes ecrans sont
reproduits en code : ils restent nets a toutes les densites, s'adaptent au
mobile, se selectionnent au curseur, pesent quelques kilo-octets au lieu de
deux cent, et leurs dates ne vieillissent pas.

Palette relevee au pixel sur les captures de doc.harelsystems.io :
  cyan de barre   #2CBAE7      actif du menu   #36BDE8
  en-tete de bloc #ECF0F5      filet           #D3D6D9
  corail          #FA8F92      ambre           #FFDDA8
  vert            #00A65A      bleu de filtre  #3C8DBC
  rouge           #DD4B39      ligne alertee   #F2DEDE

Chaque ecran est un <figure role="img"> porteur d'une alternative textuelle :
c'est une illustration de l'interface, une aide a la lecture ne doit pas avoir
a traverser un tableau de donnees de demonstration.
"""

CSS = """<style id="hh-vC-ui">
#hvc .ui{--c:#2CBAE7;--c2:#36BDE8;--hd:#ECF0F5;--fl:#D3D6D9;--co:#FA8F92;--am:#FFDDA8;
 --ok:#00A65A;--bl:#3C8DBC;--rd:#DD4B39;--al:#F2DEDE;--tx:#333;--tx2:#767676;
 background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;
 font-family:'Inter',-apple-system,sans-serif;color:var(--tx)}
#hvc .ui *{box-sizing:border-box}
#hvc .ui-bar{display:flex;align-items:center;gap:7px;padding:9px 14px;background:var(--wash);border-bottom:1px solid var(--line)}
#hvc .ui-bar i{width:9px;height:9px;border-radius:50%;background:#CBD5E1;display:block;flex:0 0 9px}
#hvc .ui-bar b{margin-left:6px;font-size:.75rem;font-weight:700;color:var(--ink3)}
#hvc .ui-cap{font-size:.8125rem;line-height:1.5;color:var(--ink3);padding:11px 14px;border-top:1px solid var(--line);background:var(--wash)}

/* --- barre applicative --- */
#hvc .ui-top{display:flex;align-items:center;gap:22px;background:var(--c);color:#fff;padding:0 14px;height:44px;font-size:.8125rem}
#hvc .ui-logo{display:flex;align-items:center;gap:7px;font-weight:800;font-size:.95rem;letter-spacing:-.01em;padding-right:6px}
#hvc .ui-logo svg{width:22px;height:22px}
#hvc .ui-nav{display:flex;gap:18px;flex:1;min-width:0;overflow:hidden}
#hvc .ui-nav span{display:flex;align-items:center;gap:5px;white-space:nowrap;opacity:.92}
#hvc .ui-nav span.on{opacity:1;font-weight:700;position:relative}
#hvc .ui-nav span.on::after{content:"";position:absolute;left:50%;bottom:-13px;transform:translateX(-50%);
 border:6px solid transparent;border-bottom-color:#fff}
#hvc .ui-me{display:flex;align-items:center;gap:12px;white-space:nowrap;opacity:.95}

/* --- corps : menu + page --- */
#hvc .ui-body{display:grid;grid-template-columns:190px 1fr;min-height:230px}
#hvc .ui-side{border-right:1px solid var(--fl);padding:0;background:#fff}
#hvc .ui-side a{display:flex;align-items:center;gap:9px;padding:9px 13px;font-size:.78rem;color:var(--tx2);border-bottom:1px solid #F4F6F8}
#hvc .ui-side a.on{background:var(--c2);color:#fff;font-weight:600}
#hvc .ui-side a b{width:12px;height:12px;background:currentColor;border-radius:3px;flex:0 0 12px;opacity:.3}
#hvc .ui-main{background:var(--hd);padding:12px}
#hvc .ui-h{display:flex;align-items:center;justify-content:space-between;margin:0 0 11px;padding:0 2px}
#hvc .ui-h span{font-size:1.05rem;font-weight:400;color:#444}
#hvc .ui-h em{font-style:normal;color:#9AA3AC;font-size:1.1rem;letter-spacing:.18em}
#hvc .ui-h em.cnt{letter-spacing:0;font-size:.72rem}
#hvc .ui-grid{display:grid;grid-template-columns:1fr 1fr;gap:11px}
#hvc .ui-grid.one{grid-template-columns:1fr}

/* --- bloc --- */
#hvc .ui-card{background:#fff;border:1px solid var(--fl);border-top:3px solid var(--c);min-width:0}
#hvc .ui-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%}
#hvc .ui-main,#hvc .ui-modal{min-width:0}
#hvc .ui-card>p{display:flex;align-items:center;justify-content:space-between;gap:8px;
 padding:9px 12px;border-bottom:1px solid #F0F2F4;font-size:.8125rem;color:#444;font-weight:400}
#hvc .ui-card>p em{font-style:normal;color:#B4BCC4;font-size:.9rem}
#hvc .ui-in{padding:11px 12px}

/* --- anneau, en aplat : un simple degrade conique --- */
#hvc .ui-donut{display:flex;align-items:center;gap:14px}
#hvc .ui-ring{width:96px;height:96px;border-radius:50%;flex:0 0 96px;position:relative}
#hvc .ui-ring::after{content:"";position:absolute;inset:26px;background:#fff;border-radius:50%}
#hvc .ui-leg{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px;font-size:.72rem}
#hvc .ui-leg div{display:flex;align-items:center;gap:6px}
#hvc .ui-leg i{width:8px;height:8px;border-radius:50%;flex:0 0 8px}
#hvc .ui-leg u{text-decoration:none;color:#3C8DBC;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#hvc .ui-leg b{color:#444;font-weight:600;font-variant-numeric:tabular-nums}
#hvc .ui-leg s{text-decoration:none;color:#767676;font-variant-numeric:tabular-nums;min-width:38px;text-align:right}

/* --- segments de periode --- */
#hvc .ui-seg{display:grid;grid-template-columns:repeat(3,1fr);margin-top:10px;font-size:.68rem;text-align:center;color:#666}
#hvc .ui-seg span{border:1px solid var(--fl);padding:4px 2px;background:#F7F8FA}
#hvc .ui-seg span.on{background:#E7EAEE;font-weight:600;color:#333}
#hvc .ui-seg span+span{border-left:none}

/* --- tableau --- */
#hvc .ui-tab{width:100%;border-collapse:collapse;font-size:.72rem}
#hvc .ui-tab th{background:var(--hd);color:#444;font-weight:600;text-align:left;padding:7px 9px;border-bottom:1px solid var(--fl);white-space:nowrap}
#hvc .ui-tab td{padding:7px 9px;border-bottom:1px solid #F0F2F4;color:#555;vertical-align:middle}
#hvc .ui-tab tr:last-child td{border-bottom:none}
#hvc .ui-tab .lk{color:#3C8DBC}
#hvc .ui-tab .nb{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
#hvc .ui-tab tr.alert td{background:var(--al)}
#hvc .ui-tab tr.zebra td{background:#FAFBFC}

/* --- pastilles et encarts --- */
#hvc .ui-chip{display:inline-flex;align-items:center;gap:5px;background:var(--bl);color:#fff;font-size:.68rem;font-weight:600;padding:3px 9px;border-radius:3px}
#hvc .ui-box{display:flex;align-items:stretch;border:1px solid var(--fl);background:#fff;min-height:52px}
#hvc .ui-box i{width:52px;flex:0 0 52px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.1rem;font-weight:800}
#hvc .ui-box div{padding:7px 11px;font-size:.72rem;color:#555;display:flex;flex-direction:column;justify-content:center;gap:2px}
#hvc .ui-box div b{color:#333;font-weight:700;font-variant-numeric:tabular-nums}
#hvc .ui-boxes{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:11px}
#hvc .ui-pill{display:inline-block;font-size:.66rem;font-weight:700;padding:2px 8px;border-radius:3px}
#hvc .ui-pill.a{background:#E8F5EE;color:#1B7A48}
#hvc .ui-pill.b{background:#FDECEA;color:#B02A1B}
#hvc .ui-pill.c{background:#FEF6E6;color:#96650E}

/* --- courbe, en aplat --- */
#hvc .ui-plot{width:100%;height:118px;display:block}
#hvc .ui-plot .ax{stroke:#E6E9ED;stroke-width:1}
#hvc .ui-plot .ln{fill:none;stroke:var(--bl);stroke-width:2}
#hvc .ui-plot .ar{fill:rgba(60,141,188,.12)}
#hvc .ui-plot text{font-size:8px;fill:#9AA3AC;font-family:inherit}

/* --- fenetre modale --- */
#hvc .ui-modal{background:#fff}
#hvc .ui-modal>p:first-child{display:flex;align-items:center;justify-content:space-between;
 padding:11px 14px;border-bottom:1px solid var(--fl);font-size:.85rem;color:#333;font-weight:600}
#hvc .ui-modal>p:first-child em{font-style:normal;color:#9AA3AC;font-weight:400;font-size:.78rem}
#hvc .ui-warn{background:#F39C12;color:#fff;font-size:.74rem;padding:7px 14px}
#hvc .ui-opts{padding:11px 14px;font-size:.74rem;color:#555;display:flex;flex-direction:column;gap:8px}
#hvc .ui-opts span{display:flex;align-items:flex-start;gap:8px;line-height:1.45}
#hvc .ui-opts i{position:relative;width:13px;height:13px;border-radius:50%;border:2px solid var(--ok);flex:0 0 13px;margin-top:2px}
/* le point plein d'un bouton radio : un pseudo-element, pas une ombre interne */
#hvc .ui-opts i.on::after{content:"";position:absolute;inset:1.5px;background:var(--ok);border-radius:50%}
#hvc .ui-acts{display:flex;justify-content:space-between;padding:11px 14px;border-top:1px solid var(--fl)}
#hvc .ui-btn{font-size:.74rem;font-weight:600;padding:6px 14px;border:1px solid var(--fl);background:#fff;color:#555;border-radius:3px}
#hvc .ui-btn.pr{background:var(--bl);border-color:var(--bl);color:#fff}

@media(max-width:900px){
 #hvc .ui-body{grid-template-columns:1fr}
 #hvc .ui-side{display:none}
 #hvc .ui-grid{grid-template-columns:1fr}
 #hvc .ui-boxes{grid-template-columns:1fr}
 #hvc .ui-nav span:nth-child(n+4){display:none}
}
@media(max-width:560px){
 #hvc .ui-top{gap:12px;font-size:.72rem}
 #hvc .ui-nav span:nth-child(n+3){display:none}
 #hvc .ui-tab{font-size:.66rem}
 #hvc .ui-tab th,#hvc .ui-tab td{padding:6px 7px}
 /* l'anneau passe au-dessus de sa legende : en colonne etroite, la legende
    etait ecretee par le cadre plutot que reduite */
 #hvc .ui-donut{flex-direction:column;align-items:flex-start;gap:10px}
 #hvc .ui-ring{width:78px;height:78px;flex:0 0 78px}
 #hvc .ui-ring::after{inset:21px}
 #hvc .ui-leg{width:100%;font-size:.68rem}
 #hvc .ui-seg{font-size:.6rem}
 #hvc .ui-main,#hvc .ui-in{padding:9px}
 #hvc .ui-boxes{gap:7px}
}
</style>"""


# --------------------------------------------------------------------- briques
def _nuage():
    return ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
            '<path d="M19 18H6a4 4 0 010-8 5.5 5.5 0 0110.5-1.5A3.5 3.5 0 0119 18z"/></svg>')


def _top(actif):
    items = ["CRM", "Produits", "Vente", "Achats", "Comptabilité"]
    nav = "".join('<span%s>%s</span>' % (' class="on"' if i == actif else '', i) for i in items)
    return ('<div class="ui-top"><span class="ui-logo">' + _nuage() + 'Hello Harel</span>'
            '<span class="ui-nav">' + nav + '</span>'
            '<span class="ui-me">Paul Dupont ▾</span></div>')


def _side(items, actif=0):
    return ('<div class="ui-side">' + "".join(
        '<a%s><b></b>%s</a>' % (' class="on"' if k == actif else '', t)
        for k, t in enumerate(items)) + '</div>')


def _ring(parts):
    """parts : [(couleur, pourcentage)] — un degrade conique, sans bibliotheque."""
    stops, cur = [], 0.0
    for coul, pct in parts:
        stops.append("%s %.2f%% %.2f%%" % (coul, cur, cur + pct))
        cur += pct
    return '<span class="ui-ring" style="background:conic-gradient(%s)"></span>' % ", ".join(stops)


def _leg(lignes):
    return '<span class="ui-leg">' + "".join(
        '<div><i style="background:%s"></i><u>%s</u><b>%s</b><s>%s</s></div>' % l
        for l in lignes) + '</span>'


def _seg(actif=0):
    p = ["30 derniers jours", "12 dernières semaines", "12 derniers mois"]
    return '<span class="ui-seg">' + "".join(
        '<span%s>%s</span>' % (' class="on"' if k == actif else '', t)
        for k, t in enumerate(p)) + '</span>'


def _card(titre, corps, croix=True):
    return ('<div class="ui-card"><p>' + titre + ('<em>×</em>' if croix else '') + '</p>'
            '<div class="ui-in">' + corps + '</div></div>')


def _tab(entetes, lignes):
    th = "".join('<th%s>%s</th>' % (' class="nb"' if e.startswith("^") else '', e.lstrip("^"))
                 for e in entetes)
    tr = ""
    for l in lignes:
        # le marqueur de ligne est le premier caractere de la premiere cellule :
        # « ! » pour une ligne en alerte, « ~ » pour une ligne grisee.
        cls = ""
        if l and l[0][:1] == "!":
            cls, l = ' class="alert"', [l[0][1:]] + list(l[1:])
        elif l and l[0][:1] == "~":
            cls, l = ' class="zebra"', [l[0][1:]] + list(l[1:])
        tr += '<tr%s>%s</tr>' % (cls, "".join(
            '<td%s>%s</td>' % (' class="nb"' if c.startswith("^") else
                               (' class="lk"' if c.startswith("@") else ''), c.lstrip("^@"))
            for c in l))
    return ('<div class="ui-tw"><table class="ui-tab"><thead><tr>' + th
            + '</tr></thead><tbody>' + tr + '</tbody></table></div>')


def _fig(alt, corps, titre, legende):
    return ('<figure class="ui" role="img" aria-label="' + alt + '">'
            '<div class="ui-bar"><i></i><i></i><i></i><b>' + titre + '</b></div>'
            + corps +
            '<figcaption class="ui-cap">' + legende + '</figcaption></figure>')


# --------------------------------------------------------------------- ecrans
# Les libelles, les colonnes et les intitules sont ceux de la documentation
# produit. Les dates sont rafraichies : une reproduction n'a pas de raison de
# porter les dates de 2020 des captures d'origine.

def _vente():
    corps = (
        _top("Vente") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Devis", "Commandes", "Préparations", "Livraisons",
                 "Réclamations", "Vue d'ensemble des prix", "Journal des ventes"])
        + '<div class="ui-main"><div class="ui-h"><span>Vente</span><em>+ ⎙</em></div>'
        '<div class="ui-grid">'
        + _card("Top des clients par montant HT commandé",
                '<span class="ui-donut">' + _ring([("#FA8F92", 67), ("#3ECF8E", 33)])
                + _leg([("#FA8F92", "0001 — Client", "14 €", "67 %"),
                        ("#3ECF8E", "0002 — Client particulier", "7 €", "33 %")])
                + '</span>' + _seg(0))
        + _card("Produits les plus souvent vendus",
                '<span class="ui-donut">' + _ring([("#FA8F92", 46), ("#3ECF8E", 31), ("#FFDDA8", 23)])
                + _leg([("#FA8F92", "0001 — Pomme Golden", "46 %", "3"),
                        ("#3ECF8E", "0046 — Poêlée de légumes", "31 %", "2"),
                        ("#FFDDA8", "0016 — Carottes râpées", "23 %", "1")])
                + '</span>' + _seg(2))
        + '</div></div></div>')
    return _fig("Reproduction du tableau de bord Vente de Hello Harel : top des clients et "
                "produits les plus vendus", corps, "Hello Harel — Vente",
                "Vente — devis, commandes, préparations, livraisons")


def _achats():
    corps = (
        _top("Achats") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Commandes", "Arrivages", "Régularisations en attente",
                 "Réclamations", "Catalogue", "Liste d'approvisionnement", "Journal des achats"])
        + '<div class="ui-main"><div class="ui-h"><span>Achats</span><em>+ ⎙</em></div>'
        '<div class="ui-grid">'
        + _card("Top des fournisseurs par montant HT facturé",
                '<span class="ui-donut">' + _ring([("#FA8F92", 58), ("#3ECF8E", 42)])
                + _leg([("#FA8F92", "0003 — Fournisseur", "1 240 €", "58 %"),
                        ("#3ECF8E", "0007 — Fournisseur", "900 €", "42 %")])
                + '</span>' + _seg(0))
        + _card("Derniers arrivages validés",
                _tab(["Numéro d'arrivage", "Date d'achat", "Date d'arrivage", "Fournisseur", "^Total"],
                     [["@PUR/2609111", "02/09/2026", "04/09/2026", "@0003 — Fournisseur", "^1 240,00 €"],
                      ["~@PUR/2609108", "01/09/2026", "03/09/2026", "@0007 — Fournisseur", "^900,00 €"],
                      ["@PUR/2609102", "28/08/2026", "31/08/2026", "@0003 — Fournisseur", "^612,40 €"]]))
        + '</div></div></div>')
    return _fig("Reproduction du tableau de bord Achats de Hello Harel : top des fournisseurs et "
                "derniers arrivages validés", corps, "Hello Harel — Achats",
                "Achats — fournisseurs, arrivages, approvisionnements")


def _stock():
    corps = (
        _top("Stock") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Produits stockés", "Tout le stock", "Emplacements",
                 "Inventaires", "Transferts"])
        + '<div class="ui-main"><div class="ui-h"><span>Stock</span><em>+ ⎙</em></div>'
        '<div class="ui-grid">'
        + _card("Stratégies de prélèvement",
                '<span class="ui-donut">' + _ring([("#FA8F92", 67), ("#FFDDA8", 33)])
                + _leg([("#FA8F92", "FIFO", "2", "67 %"),
                        ("#FFDDA8", "FEFO", "1", "33 %")])
                + '</span>')
        + _card("Éléments de stock à retirer",
                _tab(["Élément de stock", "Produit", "^Quantité", "Date de prélèvement",
                      "Date de péremption"],
                     [["!@0003.0001", "Semoule", "^500 kg", "05/09/2026", "08/09/2026"],
                      ["@0016.0004", "Carottes râpées fraîches", "^42 kg", "06/09/2026", "11/09/2026"],
                      ["~@0064.0002", "Épinards", "^120 kg", "09/09/2026", "16/09/2026"]]))
        + '</div></div></div>')
    return _fig("Reproduction du tableau de bord Stock de Hello Harel : stratégies de prélèvement "
                "FIFO et FEFO, éléments à retirer avec leur date de péremption", corps,
                "Hello Harel — Stock", "Stock — stratégies FIFO / FEFO et dates de péremption")


def _preparation():
    corps = (
        '<div class="ui-modal">'
        '<p>Quantité manquante<em>Commande 2609101</em></p>'
        '<div class="ui-warn">Certains produits commandés n\'ont pas été préparés.</div>'
        + _tab(["", "Produit", "Conditionnement", "^Commandé", "^Préparé", "^Manque"],
               [["✓", "@0001 — Pomme Golden", "Kilogramme", "^10 kg", "^7 kg", "^3 kg"],
                ["~✓", "@0016 — Carottes râpées fraîches", "Kilogramme (net)",
                 "^25 kg", "^24,6 kg", "^0,4 kg"]])
        + '<div class="ui-opts">'
        '<span><i class="on"></i>Expédier la préparation incomplète et créer une nouvelle '
        'préparation avec les quantités manquantes des articles sélectionnés</span>'
        '<span><i></i>Expédier la préparation incomplète</span>'
        '</div>'
        '<div class="ui-acts"><span class="ui-btn">Annuler</span>'
        '<span class="ui-btn pr">Suivant ➜</span></div>'
        '</div>')
    return _fig("Reproduction de l'écran Quantité manquante de Hello Harel : 10 kg commandés, "
                "7 kg préparés, 3 kg manquants", corps, "Hello Harel — Préparation",
                "L'écart entre le commandé et le préparé, au kilo")


def _compta():
    pts = [(0, 104), (34, 101), (68, 99), (102, 97), (136, 94), (170, 90), (204, 84),
           (238, 74), (272, 58), (306, 34), (340, 12)]
    ligne = " ".join("%d,%d" % p for p in pts)
    aire = "0,112 " + ligne + " 340,112"
    plot = ('<svg class="ui-plot" viewBox="0 0 340 118" preserveAspectRatio="none" '
            'aria-hidden="true">'
            + "".join('<line class="ax" x1="0" y1="%d" x2="340" y2="%d"/>' % (y, y)
                      for y in (12, 37, 62, 87, 112))
            + '<polygon class="ar" points="' + aire + '"/>'
            '<polyline class="ln" points="' + ligne + '"/></svg>')
    corps = (
        _top("Comptabilité") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Comptes", "Factures de vente", "Factures d'achat",
                 "Paiements", "Journaux", "Balance âgée", "Suivi des factures de vente"])
        + '<div class="ui-main"><div class="ui-h"><span>Comptabilité</span><em>+ ⎙</em></div>'
        '<div class="ui-grid">'
        + _card("Chiffre d'affaires (factures - avoirs HT)", plot + _seg(1))
        + _card("Factures de vente en attente",
                _tab(["Numéro", "Client", "^Total HT", "^Total TTC", "État"],
                     [["@FAC-2609-0113", "@0001 — Client", "^15,00 €", "^16,46 €",
                       '<span class="ui-pill c">En attente</span>'],
                      ["~@FAC-2609-0111", "@0002 — Client particulier", "^3,58 €", "^3,78 €",
                       '<span class="ui-pill b">En retard</span>'],
                      ["@FAC-2609-0108", "@0003 — Client", "^1 240,00 €", "^1 308,20 €",
                       '<span class="ui-pill a">Émise</span>']]))
        + '</div></div></div>')
    return _fig("Reproduction du tableau de bord Comptabilité de Hello Harel : chiffre d'affaires "
                "et factures de vente en attente", corps, "Hello Harel — Comptabilité",
                "Comptabilité — encours, balance âgée, suivi des factures")


def _tarifs():
    boxes = ('<div class="ui-boxes">'
             '<div class="ui-box"><i style="background:#DD4B39">▥</i>'
             '<div><span><b>1 576</b> tarifs définis</span><span><b>59</b> tarifs manquants</span></div></div>'
             '<div class="ui-box"><i style="background:#00A65A">⚙</i>'
             '<div><span>Global — <b>Marge : 9 %</b></span></div></div>'
             '<div class="ui-box"><i style="background:#00A65A">i</i>'
             '<div><span>1 groupe de clients est basé sur ce catalogue</span>'
             '<span>Ce catalogue est le catalogue par défaut</span></div></div>'
             '</div>')
    corps = (
        '<div class="ui-main" style="padding:14px">'
        '<div class="ui-h"><span>Catalogue <em style="letter-spacing:0;font-size:.85rem">'
        'Catalogue 7</em></span><em class="cnt">1–10 sur 41</em></div>'
        + boxes
        + '<p style="margin:0 0 9px"><span class="ui-chip">× Fruits et Légumes</span></p>'
        '<div style="background:#fff;border:1px solid var(--fl)">'
        + _tab(["Produit", "Conditionnement", "^Taux de marge", "^Prix unitaire", "^Taxes",
                "^Prix unitaire TTC"],
               [["@0016 — Carottes râpées fraîches", "Kilogramme", "^9,89 %", "^2,89 €", "^0,16 €", "^3,05 €"],
                ["~@0026 — Salade de fruits exotiques", "Kilogramme", "^9,89 %", "^3,30 €", "^0,18 €", "^3,48 €"],
                ["@0045 — Frites", "Sac de 2,5 kg", "^15,00 %", "^1,09 €", "^0,06 €", "^1,15 €"],
                ["~@0046 — Poêlée de légumes", "Kilogramme", "^9,89 %", "^3,08 €", "^0,17 €", "^3,25 €"],
                ["@0064 — Épinards", "Kilogramme", "^9,89 %", "^8,77 €", "^0,48 €", "^9,25 €"],
                ["~@099 — Coulis de framboises surgelé", "Unité", "^13,97 %", "^4,73 €", "^0,26 €", "^4,99 €"],
                ["!@1028 — Coriandre déshydratée", "Kilogramme (net)", "^9,89 %", "^0,00 €", "^0,00 €", "^0,00 €"],
                ["@1091 — Pomme de terre Parisienne", "Kilogramme", "^9,89 %", "^1,26 €", "^0,07 €", "^1,33 €"]])
        + '</div></div>')
    return _fig("Reproduction du catalogue tarifaire de Hello Harel : 1 576 tarifs définis, "
                "marge suivie ligne par ligne", corps, "Hello Harel — Tarifs",
                "Tarifs — 1 576 tarifs définis, marge suivie par ligne")


ECRANS = {
    "vente": _vente, "achats": _achats, "stock": _stock,
    "preparation": _preparation, "compta": _compta, "tarifs": _tarifs,
}


def ecran(cle):
    return ECRANS[cle]()
