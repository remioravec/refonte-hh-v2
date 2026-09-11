# -*- coding: utf-8 -*-
"""
Les ecrans du logiciel, rebatis en HTML et CSS, pour la page agroalimentaire.

Meme principe que le kit de la variante C du negoce : au lieu d'une capture
matricielle qui pese deux cents kilo-octets, vieillit et se floute sur un
ecran dense, l'ecran est reproduit en code. Il reste net partout, se plie au
mobile, se selectionne au curseur et ses dates ne perimeront pas.

Palette relevee sur doc.harelsystems.io, identique a celle de la variante C.
Les donnees affichees sont des donnees de demonstration, dites comme telles
dans la legende de chaque figure.

Le kit est porte sous #hh-page .hhf pour ne pas heurter le CSS du site, et
chaque marge y est marquee !important : le theme applique
  #hh-page p, blockquote, figure { margin: 0 !important }
et ecrase sinon toute mise en page injectee.
"""

C = {"c": "#2CBAE7", "c2": "#36BDE8", "hd": "#ECF0F5", "fl": "#D3D6D9",
     "co": "#FA8F92", "am": "#FFDDA8", "ok": "#00A65A", "bl": "#3C8DBC",
     "rd": "#DD4B39", "al": "#F2DEDE"}

CSS = """<style id="hh-agro-fonctionnalites">
#hh-page .hhf{display:block;margin:0 !important}
#hh-page .hhf-row{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);
 gap:2.75rem;align-items:center}
/* rangee inversee : la capture reste dans la colonne large, sinon les tableaux
   se retrouvent ecrases dans 5 colonnes et le contenu est ecrete */
#hh-page .hhf-row.rev{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}
#hh-page .hhf-row.rev>.hhf-txt{order:2}
#hh-page .hhf-txt>*{margin:0 !important}
#hh-page .hhf-num{display:inline-flex;align-items:center;gap:.6rem;font-size:.75rem;
 font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0891b2;
 margin:0 0 1rem !important}
#hh-page .hhf-num b{display:grid;place-items:center;width:26px;height:26px;border-radius:8px;
 background:#ecfeff;color:#0e7490;font-size:.78rem;font-weight:800;letter-spacing:0}
#hh-page .hhf-txt h3{font-size:clamp(1.35rem,2.4vw,1.85rem);line-height:1.2;
 color:#0f172a;font-weight:700;margin:0 0 .9rem !important;letter-spacing:-.02em}
#hh-page .hhf-txt>p{color:#475569;font-size:1.02rem;line-height:1.68;margin:0 0 1.25rem !important}
#hh-page .hhf-pts{list-style:none;padding:0;margin:0 !important;display:flex;
 flex-direction:column;gap:.7rem}
#hh-page .hhf-pts li{display:flex;gap:.65rem;align-items:flex-start;color:#334155;
 font-size:.95rem;line-height:1.5;margin:0 !important}
#hh-page .hhf-pts li svg{width:19px;height:19px;flex:0 0 19px;margin-top:2px;color:#16DB7F}

/* ---------------------------------------------------------------- la fenetre */
#hh-page .hhf .ui{--c:%(c)s;--c2:%(c2)s;--hd:%(hd)s;--fl:%(fl)s;--co:%(co)s;--am:%(am)s;
 --ok:%(ok)s;--bl:%(bl)s;--rd:%(rd)s;--al:%(al)s;
 background:#fff;border:1px solid #e2e8f0;border-radius:16px;overflow:hidden;
 color:#333;margin:0 !important;box-shadow:0 18px 44px -24px rgba(15,23,42,.34)}
#hh-page .hhf .ui *{box-sizing:border-box}
#hh-page .hhf .ui-bar{display:flex;align-items:center;gap:7px;padding:9px 14px;
 background:#f8fafc;border-bottom:1px solid #e2e8f0}
#hh-page .hhf .ui-bar i{width:9px;height:9px;border-radius:50%%;background:#CBD5E1;display:block;flex:0 0 9px}
#hh-page .hhf .ui-bar b{margin-left:6px;font-size:.75rem;font-weight:700;color:#64748b}
#hh-page .hhf .ui-cap{font-size:.8rem;line-height:1.5;color:#64748b;padding:11px 14px;
 border-top:1px solid #e2e8f0;background:#f8fafc;margin:0 !important}

#hh-page .hhf .ui-top{display:flex;align-items:center;gap:22px;background:var(--c);color:#fff;
 padding:0 14px;height:44px;font-size:.8125rem}
#hh-page .hhf .ui-logo{display:flex;align-items:center;gap:7px;font-weight:800;font-size:.95rem;
 letter-spacing:-.01em;padding-right:6px}
#hh-page .hhf .ui-logo svg{width:22px;height:22px}
#hh-page .hhf .ui-nav{display:flex;gap:18px;flex:1;min-width:0;overflow:hidden}
#hh-page .hhf .ui-nav span{display:flex;align-items:center;gap:5px;white-space:nowrap;opacity:.92}
#hh-page .hhf .ui-nav span.on{opacity:1;font-weight:700;position:relative}
#hh-page .hhf .ui-nav span.on::after{content:"";position:absolute;left:50%%;bottom:-13px;
 transform:translateX(-50%%);border:6px solid transparent;border-bottom-color:#fff}
#hh-page .hhf .ui-me{display:flex;align-items:center;gap:12px;white-space:nowrap;opacity:.95}

#hh-page .hhf .ui-body{display:grid;grid-template-columns:186px 1fr;min-height:236px}
#hh-page .hhf .ui-side{border-right:1px solid var(--fl);background:#fff}
#hh-page .hhf .ui-side span{display:flex;align-items:center;gap:9px;padding:9px 13px;font-size:.78rem;
 color:#767676;border-bottom:1px solid #F4F6F8;text-decoration:none}
#hh-page .hhf .ui-side span.on{background:var(--c2);color:#fff;font-weight:600}
#hh-page .hhf .ui-side span b{width:12px;height:12px;background:currentColor;border-radius:3px;
 flex:0 0 12px;opacity:.3}
#hh-page .hhf .ui-main{background:var(--hd);padding:12px;min-width:0}
#hh-page .hhf .ui-h{display:flex;align-items:center;justify-content:space-between;
 margin:0 0 11px !important;padding:0 2px}
#hh-page .hhf .ui-h span{font-size:1.05rem;font-weight:400;color:#444}
#hh-page .hhf .ui-h em{font-style:normal;color:#9AA3AC;font-size:1.1rem;letter-spacing:.18em}
#hh-page .hhf .ui-grid{display:grid;grid-template-columns:1fr 1fr;gap:11px}
#hh-page .hhf .ui-grid.one{grid-template-columns:1fr}

#hh-page .hhf .ui-card{background:#fff;border:1px solid var(--fl);border-top:3px solid var(--c);min-width:0}
#hh-page .hhf .ui-card>p{display:flex;align-items:center;justify-content:space-between;gap:8px;
 padding:9px 12px !important;border-bottom:1px solid #F0F2F4;font-size:.8125rem;
 color:#444;font-weight:400;margin:0 !important}
#hh-page .hhf .ui-card>p em{font-style:normal;color:#B4BCC4;font-size:.9rem}
#hh-page .hhf .ui-in{padding:11px 12px}
#hh-page .hhf .ui-tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%%}

#hh-page .hhf .ui-donut{display:flex;align-items:center;gap:14px}
#hh-page .hhf .ui-ring{width:96px;height:96px;border-radius:50%%;flex:0 0 96px;position:relative}
#hh-page .hhf .ui-ring::after{content:"";position:absolute;inset:26px;background:#fff;border-radius:50%%}
#hh-page .hhf .ui-leg{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px;font-size:.72rem}
#hh-page .hhf .ui-leg div{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
/* en colonne etroite le libelle passe sur sa propre ligne : il etait reduit
   a zero par le chiffre et le pourcentage, et disparaissait completement */
#hh-page .hhf .ui-leg u{flex:1 1 7rem}
#hh-page .hhf .ui-leg i{width:8px;height:8px;border-radius:50%%;flex:0 0 8px}
#hh-page .hhf .ui-leg u{text-decoration:none;color:#3C8DBC;flex:1;min-width:0;overflow:hidden;
 text-overflow:ellipsis;white-space:nowrap}
#hh-page .hhf .ui-leg b{color:#444;font-weight:600;font-variant-numeric:tabular-nums}
#hh-page .hhf .ui-leg s{text-decoration:none;color:#767676;font-variant-numeric:tabular-nums;
 min-width:40px;text-align:right}

#hh-page .hhf .ui-tab{width:100%%;border-collapse:collapse;font-size:.72rem;margin:0 !important}
#hh-page .hhf .ui-tab th{background:var(--hd);color:#444;font-weight:600;text-align:left;
 padding:7px 9px;border-bottom:1px solid var(--fl);white-space:nowrap}
#hh-page .hhf .ui-tab td{padding:7px 9px;border-bottom:1px solid #F0F2F4;color:#555;vertical-align:middle}
#hh-page .hhf .ui-tab tr:last-child td{border-bottom:none}
#hh-page .hhf .ui-tab .lk{color:#3C8DBC}
#hh-page .hhf .ui-tab .nb{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
#hh-page .hhf .ui-tab tr.alert td{background:var(--al)}
#hh-page .hhf .ui-tab tr.zebra td{background:#FAFBFC}

#hh-page .hhf .ui-box{display:flex;align-items:stretch;border:1px solid var(--fl);background:#fff;min-height:54px}
#hh-page .hhf .ui-box i{width:54px;flex:0 0 54px;display:flex;align-items:center;justify-content:center;
 color:#fff;font-size:.95rem;font-weight:800;font-style:normal;font-variant-numeric:tabular-nums}
#hh-page .hhf .ui-box div{padding:7px 11px;font-size:.72rem;color:#555;display:flex;
 flex-direction:column;justify-content:center;gap:2px}
#hh-page .hhf .ui-box div b{color:#333;font-weight:700;font-variant-numeric:tabular-nums}
#hh-page .hhf .ui-boxes{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:11px !important}
#hh-page .hhf .ui-pill{display:inline-block;font-size:.66rem;font-weight:700;padding:2px 8px;border-radius:3px}
#hh-page .hhf .ui-pill.a{background:#E8F5EE;color:#1B7A48}
#hh-page .hhf .ui-pill.b{background:#FDECEA;color:#B02A1B}
#hh-page .hhf .ui-pill.c{background:#FEF6E6;color:#96650E}

#hh-page .hhf .ui-modal{background:#fff}
#hh-page .hhf .ui-modal>p:first-child{display:flex;align-items:center;justify-content:space-between;
 padding:11px 14px;border-bottom:1px solid var(--fl);font-size:.85rem;color:#333;
 font-weight:600;margin:0 !important}
#hh-page .hhf .ui-modal>p:first-child em{font-style:normal;color:#9AA3AC;font-weight:400;font-size:.78rem}
#hh-page .hhf .ui-warn{background:#F39C12;color:#fff;font-size:.74rem;padding:7px 14px;margin:0 !important}
#hh-page .hhf .ui-opts{padding:11px 14px;font-size:.74rem;color:#555;display:flex;
 flex-direction:column;gap:8px}
#hh-page .hhf .ui-opts span{display:flex;align-items:flex-start;gap:8px;line-height:1.45}
#hh-page .hhf .ui-opts i{position:relative;width:13px;height:13px;border-radius:50%%;
 border:2px solid var(--ok);flex:0 0 13px;margin-top:2px}
#hh-page .hhf .ui-opts i.on::after{content:"";position:absolute;inset:1.5px;background:var(--ok);border-radius:50%%}
#hh-page .hhf .ui-acts{display:flex;justify-content:space-between;padding:11px 14px;border-top:1px solid var(--fl)}
#hh-page .hhf .ui-btn{font-size:.74rem;font-weight:600;padding:6px 14px;border:1px solid var(--fl);
 background:#fff;color:#555;border-radius:3px}
#hh-page .hhf .ui-btn.pr{background:var(--bl);border-color:var(--bl);color:#fff}

@media(max-width:980px){
 #hh-page .hhf-row{grid-template-columns:1fr;gap:1.6rem}
 #hh-page .hhf-row.rev>.hhf-txt{order:0}
 #hh-page .hhf .ui-body{grid-template-columns:1fr}
 #hh-page .hhf .ui-side{display:none}
 #hh-page .hhf .ui-grid{grid-template-columns:1fr}
 #hh-page .hhf .ui-boxes{grid-template-columns:1fr}
 #hh-page .hhf .ui-nav span:nth-child(n+4){display:none}
}
@media(max-width:560px){
 #hh-page .hhf .ui-top{gap:12px;font-size:.72rem}
 #hh-page .hhf .ui-nav span:nth-child(n+3){display:none}
 #hh-page .hhf .ui-tab{font-size:.66rem}
 #hh-page .hhf .ui-tab th,#hh-page .hhf .ui-tab td{padding:6px 7px}
 #hh-page .hhf .ui-donut{flex-direction:column;align-items:flex-start;gap:10px}
 #hh-page .hhf .ui-ring{width:78px;height:78px;flex:0 0 78px}
 #hh-page .hhf .ui-ring::after{inset:21px}
 #hh-page .hhf .ui-leg{width:100%%;font-size:.68rem}
 #hh-page .hhf .ui-main,#hh-page .hhf .ui-in{padding:9px}
}

/* ------------------------------------------------------- module a onglets */
/* Le module marche SANS JavaScript : ce sont des boutons radio caches et des
   labels. Sans CSS, les cinq panneaux s'affichent a la suite — rien ne
   disparait jamais du document, ni pour un moteur, ni pour un lecteur
   d'ecran. Aucun contenu n'est injecte au clic. */
#hh-page .hhf-pick{position:absolute;opacity:0;width:1px;height:1px;margin:-1px;
 overflow:hidden;clip-path:inset(50%%);pointer-events:none}
#hh-page .hhf-bar{display:flex;gap:.5rem;overflow-x:auto;scrollbar-width:thin;
 padding:.35rem;margin:0 0 2.25rem !important;background:#f1f5f9;border-radius:999px}
#hh-page .hhf-bar label{display:flex;align-items:center;gap:.55rem;white-space:nowrap;
 padding:.72rem 1.15rem;border-radius:999px;font-size:.93rem;font-weight:600;color:#475569;
 cursor:pointer;transition:background .18s ease,color .18s ease;user-select:none;margin:0 !important}
#hh-page .hhf-bar label:hover{background:#e2e8f0;color:#0f172a}
#hh-page .hhf-bar label b{font-variant-numeric:tabular-nums;font-size:.72rem;font-weight:800;
 color:#94a3b8;letter-spacing:.04em}
#hh-page .hhf-panel{display:none}
#hh-page .hhf-panel.on{display:grid}
#hh-page .hhf-pick:nth-of-type(1):checked ~ .hhf-bar label[for="hhf-o1"]{background:#00B1F5;color:#fff;box-shadow:0 8px 18px -10px rgba(0,177,245,.9)}
#hh-page .hhf-pick:nth-of-type(1):checked ~ .hhf-bar label[for="hhf-o1"] b{color:rgba(255,255,255,.8)}
#hh-page .hhf-pick:nth-of-type(1):checked ~ .hhf-panels > .hhf-row:nth-child(1){display:grid}
#hh-page .hhf-pick:nth-of-type(1):focus-visible ~ .hhf-bar label[for="hhf-o1"]{outline:3px solid #0f172a;outline-offset:2px}
#hh-page .hhf-pick:nth-of-type(2):checked ~ .hhf-bar label[for="hhf-o2"]{background:#00B1F5;color:#fff;box-shadow:0 8px 18px -10px rgba(0,177,245,.9)}
#hh-page .hhf-pick:nth-of-type(2):checked ~ .hhf-bar label[for="hhf-o2"] b{color:rgba(255,255,255,.8)}
#hh-page .hhf-pick:nth-of-type(2):checked ~ .hhf-panels > .hhf-row:nth-child(2){display:grid}
#hh-page .hhf-pick:nth-of-type(2):focus-visible ~ .hhf-bar label[for="hhf-o2"]{outline:3px solid #0f172a;outline-offset:2px}
#hh-page .hhf-pick:nth-of-type(3):checked ~ .hhf-bar label[for="hhf-o3"]{background:#00B1F5;color:#fff;box-shadow:0 8px 18px -10px rgba(0,177,245,.9)}
#hh-page .hhf-pick:nth-of-type(3):checked ~ .hhf-bar label[for="hhf-o3"] b{color:rgba(255,255,255,.8)}
#hh-page .hhf-pick:nth-of-type(3):checked ~ .hhf-panels > .hhf-row:nth-child(3){display:grid}
#hh-page .hhf-pick:nth-of-type(3):focus-visible ~ .hhf-bar label[for="hhf-o3"]{outline:3px solid #0f172a;outline-offset:2px}
#hh-page .hhf-pick:nth-of-type(4):checked ~ .hhf-bar label[for="hhf-o4"]{background:#00B1F5;color:#fff;box-shadow:0 8px 18px -10px rgba(0,177,245,.9)}
#hh-page .hhf-pick:nth-of-type(4):checked ~ .hhf-bar label[for="hhf-o4"] b{color:rgba(255,255,255,.8)}
#hh-page .hhf-pick:nth-of-type(4):checked ~ .hhf-panels > .hhf-row:nth-child(4){display:grid}
#hh-page .hhf-pick:nth-of-type(4):focus-visible ~ .hhf-bar label[for="hhf-o4"]{outline:3px solid #0f172a;outline-offset:2px}
#hh-page .hhf-pick:nth-of-type(5):checked ~ .hhf-bar label[for="hhf-o5"]{background:#00B1F5;color:#fff;box-shadow:0 8px 18px -10px rgba(0,177,245,.9)}
#hh-page .hhf-pick:nth-of-type(5):checked ~ .hhf-bar label[for="hhf-o5"] b{color:rgba(255,255,255,.8)}
#hh-page .hhf-pick:nth-of-type(5):checked ~ .hhf-panels > .hhf-row:nth-child(5){display:grid}
#hh-page .hhf-pick:nth-of-type(5):focus-visible ~ .hhf-bar label[for="hhf-o5"]{outline:3px solid #0f172a;outline-offset:2px}
#hh-page .hhf-panels > .hhf-row{display:none}
#hh-page .hhf-aide{margin:2rem 0 0 !important;font-size:.9rem;color:#64748b;text-align:center}
@media(max-width:700px){
 #hh-page .hhf-bar{border-radius:16px}
 #hh-page .hhf-bar label{padding:.6rem .85rem;font-size:.86rem}
}
</style>""" % C


# ------------------------------------------------------------------- briques
def _nuage():
    return ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
            '<path d="M19 18H6a4 4 0 010-8 5.5 5.5 0 0110.5-1.5A3.5 3.5 0 0119 18z"/></svg>')


def _check():
    return ('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" '
            'd="M5 13l4 4L19 7"/></svg>')


def _top(actif):
    items = ["Produits", "Production", "Stock", "Qualité", "Comptabilité"]
    nav = "".join('<span%s>%s</span>' % (' class="on"' if i == actif else '', i) for i in items)
    return ('<div class="ui-top"><span class="ui-logo">' + _nuage() + 'Hello Harel</span>'
            '<span class="ui-nav">' + nav + '</span>'
            '<span class="ui-me">Paul Dupont ▾</span></div>')


def _side(items, actif=0):
    # <span> et non <a> : ce sont les entrees de menu d'une reproduction, pas
    # des liens. Un <a> sans href pollue la navigation au clavier et le plan
    # de liens de la page.
    return ('<div class="ui-side">' + "".join(
        '<span%s><b></b>%s</span>' % (' class="on"' if k == actif else '', t)
        for k, t in enumerate(items)) + '</div>')


def _ring(parts):
    stops, cur = [], 0.0
    for coul, pct in parts:
        stops.append("%s %.2f%% %.2f%%" % (coul, cur, cur + pct))
        cur += pct
    return '<span class="ui-ring" style="background:conic-gradient(%s)"></span>' % ", ".join(stops)


def _leg(lignes):
    return '<span class="ui-leg">' + "".join(
        '<div><i style="background:%s"></i><u>%s</u><b>%s</b><s>%s</s></div>' % l
        for l in lignes) + '</span>'


def _card(titre, corps, croix=True):
    return ('<div class="ui-card"><p>' + titre + ('<em>×</em>' if croix else '') + '</p>'
            '<div class="ui-in">' + corps + '</div></div>')


def _tab(entetes, lignes):
    th = "".join('<th%s>%s</th>' % (' class="nb"' if e.startswith("^") else '', e.lstrip("^"))
                 for e in entetes)
    tr = ""
    for l in lignes:
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


# -------------------------------------------------------------------- ecrans
def ecran_tracabilite():
    corps = (
        _top("Qualité") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Lots", "Traçabilité amont", "Traçabilité aval",
                 "Rappels", "Contrôles", "Non-conformités"], 3)
        + '<div class="ui-main"><div class="ui-h"><span>Traçabilité aval — lot L2609-114</span>'
        '<em>⎙</em></div><div class="ui-grid one">'
        + _card("Où est parti ce lot",
                _tab(["Produit fini", "Lot sortant", "^Quantité", "Client", "Bon de livraison", "Date"],
                     [["@0142 — Terrine de campagne", "@L2609-114", "^86 kg",
                       "@0021 — Grossiste Ouest", "@BL/2609-341", "04/09/2026"],
                      ["~@0142 — Terrine de campagne", "@L2609-114", "^54 kg",
                       "@0008 — Enseigne régionale", "@BL/2609-348", "05/09/2026"],
                      ["@0142 — Terrine de campagne", "@L2609-114", "^31 kg",
                       "@0034 — Traiteur Le Verger", "@BL/2609-352", "05/09/2026"]]))
        + _card("D'où vient ce lot",
                _tab(["Matière première", "Lot fournisseur", "Fournisseur", "Réception", "^Quantité"],
                     [["@0004 — Épaule de porc", "@F-88214", "@0003 — Abattoir Val de Loire",
                       "01/09/2026", "^120 kg"],
                      ["~@0019 — Sel nitrité", "@F-51007", "@0011 — Épices & Co",
                       "22/08/2026", "^3,2 kg"],
                      ["@0027 — Vin blanc de cuisine", "@F-77420", "@0011 — Épices & Co",
                       "22/08/2026", "^8 L"]]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Traçabilité de Hello Harel : un lot de terrine remonté "
        "à ses trois matières premières et redescendu à ses trois clients livrés",
        corps, "Hello Harel — Traçabilité",
        "Traçabilité aval et amont d'un même lot, sur un seul écran. Données de démonstration.")


def ecran_dlc():
    corps = (
        _top("Stock") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Produits stockés", "Tout le stock", "Emplacements",
                 "Inventaires", "Transferts"], 2)
        + '<div class="ui-main"><div class="ui-h"><span>Dates limites</span><em>+ ⎙</em></div>'
        '<div class="ui-grid one">'
        + _card("Stratégie de prélèvement appliquée",
                '<span class="ui-donut">' + _ring([("#FA8F92", 71), ("#FFDDA8", 29)])
                + _leg([("#FA8F92", "FEFO — au plus près de la DLC", "71 %", "34"),
                        ("#FFDDA8", "FIFO — au plus ancien", "29 %", "14")])
                + '</span>')
        + _card("À prélever en priorité",
                _tab(["Élément de stock", "Produit", "^Quantité", "DLC", "^Reste"],
                     [["!@0004.0117", "Épaule de porc", "^34 kg", "12/09/2026", "^1 j"],
                      ["@0088.0031", "Crème UHT 35 %", "^48 L", "16/09/2026", "^5 j"],
                      ["~@0016.0004", "Carottes râpées", "^42 kg", "18/09/2026", "^7 j"],
                      ["@0064.0002", "Épinards en branches", "^120 kg", "24/09/2026", "^13 j"]]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Dates limites de Hello Harel : répartition FEFO et FIFO, "
        "et la liste des éléments de stock à prélever en priorité avec leur DLC",
        corps, "Hello Harel — Stock",
        "La ligne rouge est celle qui périme demain. Données de démonstration.")


def ecran_cout():
    corps = (
        _top("Production") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Ordres de fabrication", "Nomenclatures", "Recettes",
                 "Coût de revient", "Rendements"], 4)
        + '<div class="ui-main"><div class="ui-h"><span>Coût de revient — 0142 Terrine</span>'
        '<em>⎙</em></div><div class="ui-grid one">'
        + _card("Décomposition du coût au kilo",
                '<span class="ui-donut">'
                + _ring([("#FA8F92", 61), ("#3C8DBC", 19), ("#FFDDA8", 11), ("#3ECF8E", 9)])
                + _leg([("#FA8F92", "Matières premières", "4,88 €", "61 %"),
                        ("#3C8DBC", "Main-d'œuvre", "1,52 €", "19 %"),
                        ("#FFDDA8", "Emballage", "0,88 €", "11 %"),
                        ("#3ECF8E", "Énergie et pertes", "0,72 €", "9 %")])
                + '</span>')
        + _card("Marge par produit fini",
                _tab(["Produit", "^Revient", "^Tarif", "^Marge", "Statut"],
                     [["@0142 — Terrine de campagne", "^8,00 €", "^11,40 €", "^29,8 %",
                       '<span class="ui-pill a">Dans la cible</span>'],
                      ["~@0151 — Rillettes pur porc", "^6,42 €", "^8,20 €", "^21,7 %",
                       '<span class="ui-pill c">À surveiller</span>'],
                      ["!@0163 — Pâté en croûte", "^12,90 €", "^14,60 €", "^11,6 %",
                       '<span class="ui-pill b">Sous le seuil</span>']]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Coût de revient de Hello Harel : décomposition du coût au kilo "
        "en quatre postes, et marge de trois produits finis dont un sous le seuil",
        corps, "Hello Harel — Production",
        "Le coût se décompose poste par poste, la marge se lit produit par produit. "
        "Données de démonstration.")


def ecran_stocks_sensibles():
    boxes = ('<div class="ui-boxes">'
             '<span class="ui-box"><i style="background:#3C8DBC">2°</i>'
             '<div><b>Chambre froide A</b>Consigne 0 à 4 °C</div></span>'
             '<span class="ui-box"><i style="background:#00A65A">-19°</i>'
             '<div><b>Congélation B</b>Consigne −18 °C max</div></span>'
             '<span class="ui-box"><i style="background:#DD4B39">9°</i>'
             '<div><b>Chambre froide C</b>Hors consigne depuis 40 min</div></span>'
             '</div>')
    corps = (
        _top("Stock") + '<div class="ui-body">'
        + _side(["Tableau de bord", "Produits stockés", "Tout le stock", "Emplacements",
                 "Relevés", "Alertes"], 3)
        + '<div class="ui-main"><div class="ui-h"><span>Emplacements sous contrainte</span>'
        '<em>⎙</em></div>' + boxes + '<div class="ui-grid one">'
        + _card("Derniers relevés",
                _tab(["Emplacement", "Relevé", "Température", "Hygrométrie", "Seuil", "Statut"],
                     [["!@Chambre froide C", "11/09 07:12", "9,1 °C", "78 %", "0 à 4 °C",
                       '<span class="ui-pill b">Alerte envoyée</span>'],
                      ["@Chambre froide A", "11/09 07:12", "2,4 °C", "82 %", "0 à 4 °C",
                       '<span class="ui-pill a">Conforme</span>'],
                      ["~@Congélation B", "11/09 07:12", "−19,3 °C", "—", "−18 °C max",
                       '<span class="ui-pill a">Conforme</span>'],
                      ["@Cave d'affinage", "11/09 07:12", "11,8 °C", "94 %", "10 à 13 °C",
                       '<span class="ui-pill a">Conforme</span>']]))
        + '</div></div></div>')
    return _fig(
        "Reproduction de l'écran Emplacements de Hello Harel : trois chambres suivies en "
        "température, dont une hors consigne, et le tableau des derniers relevés",
        corps, "Hello Harel — Emplacements",
        "Le dépassement se voit avant l'inventaire, pas après. Données de démonstration.")


def ecran_haccp():
    corps = (
        '<div class="ui-modal">'
        '<p>Contrôle à réception<em>Arrivage PUR/2609214</em></p>'
        '<div class="ui-warn">Un point de contrôle est hors tolérance : la validation est bloquée.</div>'
        + _tab(["", "Point de contrôle", "Attendu", "Relevé", "Statut"],
               [["✓", "@Température du camion", "≤ 4 °C", "3,1 °C",
                 '<span class="ui-pill a">Conforme</span>'],
                ["~✓", "@Intégrité des emballages", "Aucun défaut", "Aucun défaut",
                 '<span class="ui-pill a">Conforme</span>'],
                ["!✕", "@DLC restante à réception", "≥ 8 jours", "5 jours",
                 '<span class="ui-pill b">Hors tolérance</span>']])
        + '<div class="ui-opts">'
        '<span><i class="on"></i>Refuser le lot, éditer la non-conformité et notifier le '
        'fournisseur</span>'
        '<span><i></i>Accepter sous dérogation, avec motif et signature du responsable qualité</span>'
        '</div>'
        '<div class="ui-acts"><span class="ui-btn">Annuler</span>'
        '<span class="ui-btn pr">Enregistrer ➜</span></div>'
        '</div>')
    return _fig(
        "Reproduction de l'écran Contrôle à réception de Hello Harel : trois points de contrôle "
        "dont un hors tolérance, avec refus du lot ou dérogation signée",
        corps, "Hello Harel — Qualité",
        "L'enregistrement du contrôle est daté, nominatif et opposable. Données de démonstration.")


# ------------------------------------------------------------------- montage
BLOCS = [
    ("Gestion des lots et traçabilité",
     "Chaque mouvement est tracé de l'entrée matière première au produit fini. En cas d'alerte "
     "sanitaire, vous retrouvez l'origine d'un lot et la liste des clients livrés sans "
     "rouvrir un classeur.",
     ["Traçabilité ascendante et descendante",
      "Historique complet par lot",
      "Rappel produit en quelques secondes"],
     ecran_tracabilite),

    ("Gestion des DLC et DLUO",
     "Vos dates limites pilotent le prélèvement, pas l'inverse. Le stock sort au plus près de "
     "la DLC, et l'alerte tombe avant la perte, pas au moment de l'inventaire.",
     ["FEFO et FIFO appliqués automatiquement",
      "Alerte à l'approche de la date limite",
      "Pertes suivies par produit et par lot"],
     ecran_dlc),

    ("Calcul du coût de revient",
     "Le coût de revient se décompose poste par poste : matières, main-d'œuvre, emballage, "
     "énergie et pertes. Quand un prix matière bouge, la marge de chaque produit fini bouge "
     "avec lui, sous vos yeux.",
     ["Coût au kilo et au produit fini",
      "Répercussion d'une hausse matière simulée avant application",
      "Marge comparée à votre seuil, produit par produit"],
     ecran_cout),

    ("Gestion des stocks sensibles",
     "Chambres froides, congélation, caves d'affinage : chaque emplacement porte sa consigne "
     "et son relevé. Le dépassement déclenche l'alerte au moment où il se produit.",
     ["Température et hygrométrie par emplacement",
      "Seuils par contrainte sanitaire",
      "Alerte immédiate en cas de dépassement"],
     ecran_stocks_sensibles),

    ("Conformité HACCP et réglementaire",
     "Les contrôles à réception, les plans de nettoyage et les non-conformités sont enregistrés "
     "en base, datés et nominatifs. Le jour du contrôle, la documentation est déjà prête.",
     ["Points de contrôle paramétrables par matière",
      "Refus de lot ou dérogation signée",
      "Historique exportable pour les autorités sanitaires"],
     ecran_haccp),
]


COURTS = ["Traçabilité des lots", "DLC et DLUO", "Coût de revient",
          "Stocks sensibles", "Conformité HACCP"]


def section(entete, blocs=None, courts=None):
    """entete : le bloc .section-header, blocs et courts : le contenu du metier.

    Les cinq fonctionnalites tiennent dans un seul ecran de page : on choisit
    celle qu'on veut voir au lieu de derouler cinq fois la meme mise en page.
    C'est ce qui retient la session plutot que de la rendre a la SERP.
    """
    blocs = blocs or BLOCS
    courts = courts or COURTS
    radios, onglets, panneaux = [], [], []
    for k, (titre, chapo, points, fabrique) in enumerate(blocs):
        n = k + 1
        radios.append('<input class="hhf-pick" type="radio" name="hhf-onglet" id="hhf-o%d"%s>'
                      % (n, ' checked' if k == 0 else ''))
        onglets.append('<label for="hhf-o%d"><b>%02d</b>%s</label>' % (n, n, courts[k]))
        pts = "".join("<li>%s%s</li>" % (_check(), p) for p in points)
        panneaux.append(
            '<div class="hhf-row">'
            '<div class="hhf-txt"><p class="hhf-num"><b>%02d</b>Fonctionnalité</p>'
            '<h3>%s</h3><p>%s</p><ul class="hhf-pts">%s</ul></div>'
            '<div class="hhf-shot">%s</div></div>' % (n, titre, chapo, pts, fabrique()))

    return (CSS + '<section class="features-section" id="fonctionnalites"><div class="container">'
            + entete
            + '<div class="hhf">' + "".join(radios)
            + '<div class="hhf-bar">' + "".join(onglets) + '</div>'
            + '<div class="hhf-panels">' + "".join(panneaux) + '</div>'
            + '<p class="hhf-aide">%d fonctionnalités, %d écrans réels du logiciel. '
              'Choisissez la vôtre.</p>' % (len(blocs), len(blocs))
            + '</div></div></section>')
