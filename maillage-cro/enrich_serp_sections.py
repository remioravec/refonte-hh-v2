#!/usr/bin/env python3
"""
"Faire mieux que la SERP" — inject an additive, self-contained SEO content
section into 3 money pages, tuned to the subtopics the ranking competitors
cover (live SERP recon, July 2026). Purely additive: inserted right before
<section class="faq-section"> using inline styles, so it can't break the
theme layout or the FAQ drawer / JSON-LD.

Idempotent: keyed by a unique marker id; re-running replaces the block.

DRY-RUN by default. Live:
    export WP_USER=... WP_PASS=...
    python3 enrich_serp_sections.py --live
"""
import sys
import re
import wp_common as w

MARK = "hh-serp-boost"

WRAP_OPEN = (
    '<section class="{mid}" id="{mid}" '
    'style="background:linear-gradient(180deg,#ffffff,#f8fafc);padding:60px 0;'
    'border-top:1px solid #e2e8f0;">'
    '<style>.{mid} .hh-sb-wrap{{max-width:1000px;margin:0 auto;padding:0 22px;'
    'font-family:Inter,-apple-system,Segoe UI,Roboto,sans-serif;color:#0f172a;}}'
    '.{mid} .hh-sb-eyebrow{{display:inline-block;background:rgba(0,177,245,.12);'
    'color:#0090c8;font-weight:700;font-size:.72rem;letter-spacing:.06em;'
    'text-transform:uppercase;padding:.35rem .8rem;border-radius:999px;}}'
    '.{mid} h2{{font-size:clamp(1.5rem,3.2vw,2.05rem);line-height:1.2;margin:.7rem 0 .3rem;font-weight:800;}}'
    '.{mid} .hh-sb-lead{{color:#475569;font-size:1.05rem;max-width:720px;margin:0 0 1.6rem;}}'
    '.{mid} .hh-sb-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px 34px;}}'
    '.{mid} h3{{font-size:1.06rem;margin:.2rem 0 .35rem;font-weight:700;color:#0f172a;}}'
    '.{mid} p{{color:#475569;font-size:.96rem;line-height:1.65;margin:0 0 .5rem;}}'
    '.{mid} .hh-sb-pills{{display:flex;flex-wrap:wrap;gap:8px;margin:1.4rem 0 0;}}'
    '.{mid} .hh-sb-pill{{background:#ecfeff;color:#0e7490;border:1px solid #cffafe;'
    'border-radius:999px;padding:5px 13px;font-size:.82rem;font-weight:600;}}'
    '@media(max-width:760px){{.{mid} .hh-sb-grid{{grid-template-columns:1fr;}}}}'
    '</style>'
    '<div class="hh-sb-wrap">'
    '<span class="hh-sb-eyebrow">{eyebrow}</span>'
    '<h2>{h2}</h2>'
    '<p class="hh-sb-lead">{lead}</p>'
    '<div class="hh-sb-grid">'
)
WRAP_CLOSE = '</div>{pills}</div></section>\n'


def pills(items):
    return ('<div class="hh-sb-pills">'
            + ''.join(f'<span class="hh-sb-pill">{x}</span>' for x in items)
            + '</div>')


def block(h3, body):
    return f'<div><h3>{h3}</h3>{body}</div>'


PAGES = {
    5477: dict(
        eyebrow="ERP plats cuisinés & plats préparés",
        h2="Le logiciel qui sécurise vos plats cuisinés, de la recette au rappel de lot",
        lead="Fabricants de plats cuisinés, traiteurs industriels et produits élaborés : "
             "Hello Harel relie recette, coût de revient et conformité dans un seul ERP agroalimentaire, "
             "pensé pour les DLC courtes et les cadences GMS.",
        blocks=[
            ("Nomenclatures multi-niveaux et PRI au centime",
             "<p>Construisez des recettes arborescentes jusqu'à 8 niveaux — ingrédient, préparation, "
             "sous-recette, recette mère, plat fini — et réutilisez une même sous-recette dans des "
             "dizaines de plats sans la ressaisir. Le <b>prix de revient industriel (PRI)</b> remonte "
             "toute la nomenclature et se recalcule dès qu'un cours matière bouge, pour piloter vos marges plat par plat.</p>"),
            ("DLC courtes, FEFO et rotation des stocks",
             "<p>Gérez des <b>DLC courtes</b> calculées depuis la date de fabrication et la durée de vie "
             "validée par votre labo (J+3 viande hachée, J+5 plats sauce, J+7 sous-vide pasteurisé). "
             "La logique <b>FEFO</b> (First Expired, First Out) impose d'expédier en priorité les lots "
             "les plus proches de la péremption et réduit vos pertes.</p>"),
            ("Traçabilité et rappel de lot en quelques secondes",
             "<p>Traçabilité <b>ascendante et descendante</b>, quantitative et qualitative : à partir d'un "
             "lot matière suspect, identifiez instantanément tous les produits finis concernés et les lots "
             "déjà expédiés. Vous déclenchez un <b>plan de rappel ciblé</b> en secondes, preuve à l'appui "
             "pour la DGCCRF et vos clients.</p>"),
            ("Étiquetage INCO, GMS et food-service",
             "<p>Éditez des étiquettes conformes <b>INCO</b> (allergènes en gras, valeurs nutritionnelles, "
             "estampille sanitaire) et répondez aux exigences de la GMS et de la RHF : colisage, DLC "
             "imprimées, <b>EDI</b> et commandes grande surface. De l'atelier traiteur au fabricant "
             "multi-sites, la même base pilote production, planning et expéditions.</p>"),
        ],
        pills=["erp plats cuisinés", "logiciel plats préparés", "PRI plat cuisiné",
               "traçabilité DLC", "FEFO", "étiquetage INCO", "recettes multi-niveaux"],
    ),
    5959: dict(
        eyebrow="ERP dispositifs médicaux",
        h2="L'ERP qui met vos dispositifs médicaux en conformité UDI, MDR et ISO 13485",
        lead="Fabricants et distributeurs de dispositifs médicaux : centralisez production, qualité et "
             "traçabilité réglementaire dans un ERP conçu pour l'UDI, le règlement MDR et la norme ISO 13485.",
        blocks=[
            ("UDI, numéros de série et EUDAMED",
             "<p>Gérez l'<b>Identifiant Unique des Dispositifs (UDI-DI / UDI-PI)</b>, les numéros de série "
             "et de lot tout au long du cycle de vie. La traçabilité par UDI et la déclaration vers "
             "<b>EUDAMED</b> deviennent obligatoires : Hello Harel structure vos données produit pour "
             "alimenter la base européenne et retrouver chaque référence expédiée.</p>"),
            ("Conformité MDR 2026 et IVDR",
             "<p>Le <b>règlement MDR (UE 2017/745)</b> et l'IVDR renforcent les exigences de traçabilité, "
             "de documentation technique et de surveillance après commercialisation. L'ERP conserve "
             "l'historique complet — du lot matière au dispositif livré — et sécurise vos <b>libérations "
             "de lot</b> avec workflow de validation et contrôle documentaire.</p>"),
            ("ISO 13485, ISO 14971 et maîtrise qualité",
             "<p>Rattachez plans de contrôle, agréments clients, homologations fournisseurs et documents "
             "qualité à chaque référence, dans l'esprit <b>ISO 13485</b> (système de management de la "
             "qualité) et <b>ISO 14971</b> (gestion du risque). Change control, non-conformités et "
             "libérations tracées : vous êtes prêt pour l'audit.</p>"),
            ("Stocks, DMI et matériovigilance",
             "<p>Pilotez des stocks à date de péremption et à numéro de série, gérez les <b>dispositifs "
             "médicaux implantables (DMI)</b> et leur traçabilité patient, et déclenchez un <b>rappel "
             "ou une action de matériovigilance</b> ciblée en identifiant instantanément les lots et "
             "clients concernés.</p>"),
        ],
        pills=["erp dispositifs médicaux", "logiciel UDI", "conformité MDR", "ISO 13485",
               "EUDAMED", "traçabilité DMI", "libération de lot"],
    ),
    10934: dict(
        eyebrow="ERP grossiste & négoce alimentaire",
        h2="Le logiciel des grossistes et distributeurs alimentaires : achats, marges et livraison",
        lead="Grossistes, distributeurs food-service et négociants : réceptionnez, stockez et "
             "redistribuez vite vers restaurants, GMS et collectivités, avec un ERP qui protège vos "
             "marges et votre traçabilité.",
        blocks=[
            ("Achat, prix au cours du jour et marges",
             "<p>Négociez et enregistrez vos <b>achats au cours du jour</b>, répercutez les variations "
             "sur vos tarifs clients et suivez la <b>marge en temps réel</b>, référence par référence. "
             "Gérez grilles tarifaires, remises par canal (RHF, GMS, détail) et conditions fournisseurs "
             "dans une base unique.</p>"),
            ("Poids variable, colisage et multi-dépôts",
             "<p>Gérez le <b>poids variable</b>, le colisage, les unités de vente et de facturation, ainsi "
             "que plusieurs dépôts et chambres froides. Les stocks sont pilotés en DLC/DDM avec "
             "<b>FEFO</b> pour limiter la casse sur les produits frais et à rotation rapide.</p>"),
            ("Prise de commande, tournées et livraison",
             "<p>Saisissez les commandes (téléphone, e-mail, <b>EDI</b>, portail), préparez par tournée et "
             "éditez bons de livraison et étiquettes en un flux. La distribution vers restaurants, "
             "supermarchés et collectivités est cadencée, traçée et facturée sans ressaisie.</p>"),
            ("Traçabilité food et rappel fournisseur",
             "<p>Traçabilité <b>ascendante et descendante</b> par lot : du fournisseur au client livré. "
             "En cas d'alerte, vous bloquez les lots concernés et éditez la liste des clients à rappeler "
             "en quelques clics — conformité HACCP et Paquet Hygiène assurée.</p>"),
        ],
        pills=["erp grossiste alimentaire", "logiciel négoce alimentaire", "distribution food-service",
               "poids variable", "gestion des marges", "traçabilité lot", "EDI"],
    ),
}


def build(cfg, mid):
    inner = "".join(block(h, b) for h, b in cfg["blocks"])
    html = WRAP_OPEN.format(mid=mid, eyebrow=cfg["eyebrow"], h2=cfg["h2"], lead=cfg["lead"])
    html += inner
    html += WRAP_CLOSE.format(pills=pills(cfg["pills"]))
    return html


def main():
    live = "--live" in sys.argv
    for pid, cfg in PAGES.items():
        page = w.get_raw("pages", pid)
        c = page["content"]["raw"]
        sec = build(cfg, MARK)

        # Idempotent: strip a previous injection if present.
        c = re.sub(r'<section class="%s".*?</section>\n?' % MARK, "", c, flags=re.S)

        anchor = '<section class="faq-section">'
        if anchor not in c:
            print(f"[{pid}] anchor faq-section NOT found — skipped")
            continue
        c2 = c.replace(anchor, sec + anchor, 1)

        res = w.update_content("pages", pid, c2, live=live)
        tag = "LIVE" if live else "DRY-RUN"
        print(f"[{pid}] {page['slug']}: +{len(sec)} chars, new total {len(c2)} — {tag}")


if __name__ == "__main__":
    main()
