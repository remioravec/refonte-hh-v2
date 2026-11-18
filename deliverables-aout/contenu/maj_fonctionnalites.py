#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Roadmap contenu — mises a jour du 21/09, du 28/09 et du 05/10/2026.

Cinq pages /fonctionnalites/ livrees en avril portent encore un H1 de benefice
(« Optimisez vos couts et securisez vos approvisionnements ») : la requete cible
n'apparait nulle part dans le premier ecran, et leur FAQ — six questions, 1 500
caracteres de reponse chacune — n'est pas balisee. Trois autres pages, livrees
depuis, sont deja redigees : elles ne recoivent que leur balisage.

Ce que le script pose, page par page :
  1. un H1 qui porte la requete exacte, different du title ;
  2. une accroche qui repond des la premiere phrase ;
  3. une signature datee (auteur, publication, mise a jour) ;
  4. le FAQPage JSON-LD construit sur les <details> deja en ligne ;
  5. title et meta description via Rank Math.

GARDE-FOUS
  - sauvegarde du contenu avant ecriture ;
  - refus si _elementor_data n'est pas vide ;
  - refus si le contenu depasse le plafond de rendu ;
  - refus si un « & » nu entre dans un bloc <script> (WordPress le transforme
    en &#038; et casse le JSON).
"""
import json, os, re, sys, html

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

PLAFOND = 275_000
SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-maj')

# --------------------------------------------------------------------------
# Lecture equilibree
# --------------------------------------------------------------------------

def bornes_section(c, classe):
    m = re.search(r'<section[^>]*class="[^"]*' + re.escape(classe) + r'[^"]*"[^>]*>', c)
    if not m:
        return None
    i, p = m.start(), 0
    for t in re.finditer(r'<section\b|</section>', c[i:]):
        p += 1 if t.group(0) != '</section>' else -1
        if p == 0:
            return (i, i + t.end())
    return None


def details(bloc):
    out = []
    for m in re.finditer(r'<details\b[^>]*>', bloc):
        i, p = m.start(), 0
        d = None
        for t in re.finditer(r'<details\b|</details>', bloc[i:]):
            p += 1 if t.group(0) != '</details>' else -1
            if p == 0:
                d = bloc[i:i + t.end()]
                break
        if d is None:
            continue
        q = re.search(r'(?is)<summary[^>]*>(.*?)</summary>', d)
        if not q:
            continue
        out.append((html.unescape(re.sub(r'<[^>]+>', '', q.group(1))).strip(),
                    re.sub(r'(?is)</details>\s*$', '', d[q.end():])))
    return out


def texte(h):
    t = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', h)
    t = re.sub(r'(?is)</(p|li|h[1-6]|div)>', ' ', t)
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', t))).strip()


def resume(h, maxi=320):
    t = re.sub(r'\s+', ' ', texte(h).replace('&', ' et ')).strip()
    if len(t) > maxi:
        coupe = t[:maxi]
        for sep in ('. ', ' : ', '; '):
            j = coupe.rfind(sep)
            if j > 140:
                t = coupe[:j + 1].strip()
                break
        else:
            t = coupe.rsplit(' ', 1)[0].rstrip(',;') + '.'
    if t and t[-1] not in '.!?…':
        t += '.'
    return t


# --------------------------------------------------------------------------
# Largeur en pixels (regle 1 : title 200-561 px, description 400-985 px)
# --------------------------------------------------------------------------
LARGE = set("mwMW—…")


def px(s):
    t = 0.0
    for c in s:
        t += 11.0 if c in LARGE else (8.0 if c.isalnum() else 5.5)
    return round(t)


# --------------------------------------------------------------------------
# Contenu redige
# --------------------------------------------------------------------------
BYLINE_CSS = """<style id="hh-byline-css">
.eeat-byline{display:flex;flex-wrap:wrap;align-items:center;gap:1.25rem;margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
#hh-page .eeat-byline{display:flex;flex-wrap:wrap;align-items:center;gap:1.25rem;margin:1.5rem 0;padding:1rem 1.25rem;background:rgba(255,255,255,.08);border-radius:14px;border:1px solid rgba(255,255,255,.15)}
.eeat-byline img,#hh-page .eeat-byline img{width:48px;height:48px;border-radius:50%;border:2px solid #16DB7F;object-fit:cover}
.eeat-byline-author,#hh-page .eeat-byline-author{color:#fff;font-size:.9375rem}
.eeat-byline-author strong,#hh-page .eeat-byline-author strong{color:#16DB7F;display:block;font-size:1rem;margin-bottom:.15rem}
.eeat-byline-meta,#hh-page .eeat-byline-meta{color:rgba(255,255,255,.85);font-size:.8125rem;display:flex;flex-wrap:wrap;gap:.75rem;margin-top:.25rem}
.eeat-byline-meta span,#hh-page .eeat-byline-meta span{display:inline-flex;align-items:center;gap:.35rem}
</style>
"""

BYLINE = """<div class="eeat-byline">
<img loading="lazy" src="https://ui-avatars.com/api/?name=Timothy+Jollivet&amp;background=16DB7F&amp;color=fff&amp;size=96" alt="Timothy Jollivet, fondateur de Hello Harel">
<div class="eeat-byline-author"><strong>Timothy Jollivet</strong>Fondateur de Hello Harel, éditeur d'ERP agroalimentaire
<div class="eeat-byline-meta"><span>Publié le 1er avril 2026</span><span>Mis à jour le 1er octobre 2026</span><span>{LECTURE} min de lecture</span></div>
</div></div>"""

PAGES = {
    'achat': dict(
        pid=4798, lecture=7,
        badge='Logiciel achat agroalimentaire',
        h1=("Le logiciel achat agroalimentaire qui ", "sécurise vos approvisionnements"),
        accroche="Un logiciel achat agroalimentaire compare les offres fournisseurs, "
                 "recalcule le prix moyen pondéré à chaque réception et déclenche l'alerte "
                 "avant la rupture. Le stock se valorise sur le poids réellement reçu, "
                 "jamais sur le poids commandé.",
        title="Logiciel achat agroalimentaire \u2022 Fournisseurs, PMP et seuils",
        desc="Logiciel achat agroalimentaire : comparaison fournisseurs, PMP recalculé à chaque "
             "réception, alertes de seuil. Démo gratuite.",
    ),
    'crm': dict(
        pid=4736, lecture=7,
        badge='CRM agroalimentaire',
        h1=("Le CRM agroalimentaire ", "conçu pour la vente au poids"),
        accroche="Un CRM agroalimentaire relié à l'ERP donne au commercial, pendant l'appel, "
                 "le cadencier du client, ses tarifs négociés, ses impayés et le stock "
                 "disponible au lot près. Pas un CRM généraliste branché sur une passerelle.",
        title="CRM agroalimentaire \u2022 Cadencier, télévente et tarifs client",
        desc="CRM agroalimentaire intégré à l'ERP : cadencier de télévente, tarifs négociés par "
             "client, relances automatiques. Démo gratuite.",
    ),
    'fabrication': dict(
        pid=4778, lecture=8,
        badge='Logiciel de fabrication agroalimentaire',
        h1=("Le logiciel de fabrication agroalimentaire qui ", "calcule votre coût de revient réel"),
        accroche="Un logiciel de fabrication agroalimentaire pilote les ordres de fabrication, "
                 "les nomenclatures à poids variable et le rendement de chaque atelier. "
                 "Le coût de revient se recalcule à chaque lot produit, pas une fois par mois.",
        title="Logiciel de fabrication agroalimentaire \u2022 Recettes et rendements",
        desc="Logiciel de fabrication agroalimentaire : nomenclatures, ordres de fabrication, "
             "rendement et coût de revient. Démo gratuite.",
    ),
    'facturation': dict(
        pid=4750, lecture=7,
        badge='Logiciel de facturation agroalimentaire',
        h1=("Le logiciel de facturation agroalimentaire qui ", "facture le poids réellement livré"),
        accroche="Un logiciel de facturation agroalimentaire reprend le bon de livraison, applique "
                 "le tarif négocié du client et facture le poids pesé à l'expédition. Les avoirs, "
                 "la piste d'audit fiable et l'export comptable suivent sans ressaisie.",
        title="Logiciel de facturation agroalimentaire \u2022 Poids réel et tarifs",
        desc="Logiciel de facturation agroalimentaire : facture au poids réellement livré, "
             "multi-tarifs, avoirs automatiques. Démo gratuite.",
    ),
    'gestion-de-stock': dict(
        pid=4772, lecture=8,
        badge='Logiciel de gestion de stock agroalimentaire',
        h1=("Le logiciel de gestion de stock agroalimentaire qui ", "sort le lot le plus proche de la DLC"),
        accroche="Un logiciel de gestion de stock agroalimentaire suit chaque lot en pièces et en "
                 "kilos, impose la rotation FEFO au picking et alerte avant la date limite. "
                 "Le règlement (CE) n\u00b0 178/2002, applicable depuis le 1er janvier 2005, impose "
                 "de retrouver chaque lot une étape en amont et une étape en aval.",
        title="Logiciel de gestion de stock agroalimentaire \u2022 FEFO, DLC, lots",
        desc="Logiciel de gestion de stock agroalimentaire : rotation FEFO, suivi des DLC, "
             "traçabilité par lot, multi-entrepôts. Démo gratuite.",
    ),
}

# Pages déjà rédigées : balisage seul.
BALISAGE_SEUL = {
    'facturation-automatique-bon-livraison': dict(
        pid=7905,
        title="Facturation automatique depuis bon de livraison \u2022 ERP grossiste",
        desc="Facturation automatique depuis le bon de livraison : facture en un clic, "
             "regroupement multi-BL, zéro ressaisie. Démo gratuite.",
    ),
    'gestion-consigne-bouteille-logiciel': dict(
        pid=7912,
        title="Consigne bouteille \u2022 Logiciel de suivi, retours et soldes client",
        desc="Logiciel de gestion de la consigne bouteille : compte de consigne par client, "
             "retours et rapprochement. Démo gratuite.",
    ),
    'gestion-rendement-matiere-logiciel': dict(
        pid=7909,
        title="Rendement matière \u2022 Logiciel de suivi des pertes et des freintes",
        desc="Logiciel de rendement matière : taux de transformation par poste, écart réel contre "
             "théorique, freintes. Démo gratuite.",
    ),
}


# --------------------------------------------------------------------------
# Transformations
# --------------------------------------------------------------------------

def remplacer_h1(c, debut, accent):
    m = re.search(r'(?is)(<h1[^>]*class="[^"]*hero-title[^"]*"[^>]*>)(.*?)(</h1>)', c)
    if not m:
        raise RuntimeError('h1.hero-title introuvable')
    couleur = re.search(r'class="accent"[^>]*style="color:([^";]+)', m.group(2))
    couleur = couleur.group(1) if couleur else '#60a5fa'
    neuf = (m.group(1) + debut
            + '<span class="accent" style="color:' + couleur + '">' + accent + '</span>'
            + m.group(3))
    return c[:m.start()] + neuf + c[m.end():]


def remplacer_accroche(c, texte_neuf):
    m = re.search(r'(?is)(<p class="hero-description">)(.*?)(</p>)', c)
    if not m:
        raise RuntimeError('p.hero-description introuvable')
    return c[:m.start()] + m.group(1) + texte_neuf + m.group(3) + c[m.end():]


def remplacer_badge(c, badge):
    m = re.search(r'(?is)(<div class="hero-badge">\s*<span class="dot"></span>)(.*?)(</div>)', c)
    if not m:
        return c
    return c[:m.start()] + m.group(1) + badge + m.group(3) + c[m.end():]


def poser_byline(c, lecture):
    if 'eeat-byline' in c:
        return c
    m = re.search(r'(?is)<p class="hero-cta-sub">.*?</p>', c)
    if not m:
        raise RuntimeError('p.hero-cta-sub introuvable')
    bloc = BYLINE.replace('{LECTURE}', str(lecture))
    c = c[:m.end()] + bloc + c[m.end():]
    s = re.search(r'<section[^>]*class="[^"]*hero-section', c)
    return c[:s.start()] + BYLINE_CSS + c[s.start():]


def faq_jsonld(c):
    b = bornes_section(c, 'faq-section')
    if not b:
        raise RuntimeError('faq-section introuvable')
    qs = details(c[b[0]:b[1]])
    if len(qs) < 3:
        raise RuntimeError('moins de 3 questions dans la FAQ')
    entites = [{"@type": "Question", "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": resume(r)}} for q, r in qs]
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entites}
    return '\n<script type="application/ld+json">' + \
           json.dumps(data, ensure_ascii=False) + '</script>\n'


def sans_amp_nu_dans_scripts(c):
    """Aucun « & » qui ne soit pas deja une entite, a l'interieur d'un <script>."""
    for m in re.finditer(r'(?is)<script\b[^>]*>(.*?)</script>', c):
        corps = m.group(1)
        for a in re.finditer(r'&', corps):
            suite = corps[a.start():a.start() + 10]
            if not re.match(r'&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]+);', suite):
                return False
    return True


# --------------------------------------------------------------------------

def lire(pid):
    d = n.call(f'wp/v2/pages/{pid}?context=edit&_fields=id,slug,link,content,meta')
    if d['meta'].get('_elementor_data') not in ('', '[]', None):
        raise RuntimeError(f"{pid} : _elementor_data non vide, on ne touche pas")
    return d


def ecrire(pid, contenu):
    n.call(f'wp/v2/pages/{pid}', 'POST', {'content': contenu})


def rankmath(pid, title, desc):
    n.call('rankmath/v1/updateMeta', 'POST', {
        'objectID': pid, 'objectType': 'post',
        'meta': {'rank_math_title': title, 'rank_math_description': desc},
    })


def main(ecrire_vraiment=False):
    os.makedirs(SAUVE, exist_ok=True)
    rapport = []
    for slug, p in PAGES.items():
        d = lire(p['pid'])
        c = d['content']['raw']
        open(os.path.join(SAUVE, slug + '.html'), 'w').write(c)
        avant = len(c)
        c = remplacer_badge(c, p['badge'])
        c = remplacer_h1(c, p['h1'][0], p['h1'][1])
        c = remplacer_accroche(c, p['accroche'])
        c = poser_byline(c, p['lecture'])
        if 'FAQPage' in c:
            raise RuntimeError(f'{slug} : un FAQPage existe deja, verifier a la main')
        c = c + faq_jsonld(c)
        assert len(c) < PLAFOND, f'{slug} : {len(c)} o au-dessus du plafond'
        assert sans_amp_nu_dans_scripts(c), f'{slug} : un & nu dans un <script>'
        assert '<h1' in c and c.count('<h1') == 1, f'{slug} : nombre de H1 anormal'
        if ecrire_vraiment:
            ecrire(p['pid'], c)
            rankmath(p['pid'], p['title'], p['desc'])
        rapport.append((slug, avant, len(c), px(p['title']), px(p['desc'])))

    for slug, p in BALISAGE_SEUL.items():
        if ecrire_vraiment:
            rankmath(p['pid'], p['title'], p['desc'])
        rapport.append((slug, '-', '-', px(p['title']), px(p['desc'])))

    print(f"{'page':48} {'avant':>8} {'apres':>8} {'title px':>9} {'desc px':>8}")
    for slug, a, b, tp, dp in rapport:
        alerte = '' if (200 <= tp <= 561 and 400 <= dp <= 985) else '  <-- HORS BORNES'
        print(f'{slug:48} {a!s:>8} {b!s:>8} {tp:>9} {dp:>8}{alerte}')


if __name__ == '__main__':
    main(ecrire_vraiment='--ecrire' in sys.argv)
