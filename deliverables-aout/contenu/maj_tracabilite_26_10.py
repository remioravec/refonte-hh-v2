# -*- coding: utf-8 -*-
"""/fonctionnalites/tracabilite-alimentaire/ (10968) — lot du 26/10.

Le releve dit que cette page est dominee par sa propre mere : sur les
1 607 impressions du champ tracabilite, /agroalimentaire/ en capte 62 % a la
position 24,5, contre 30 % ici a la position 35,6. Zero clic des deux cotes.

Trois corrections :

1. « Plus de 100 clients » devient « Plus de 200 ». Le site annoncait trois
   chiffres differents : 200 sur l'accueil, 150 sur /agroalimentaire/ et 100
   ici. C'est ce genre d'ecart qui nourrit les erreurs de l'AI Overview.

2. Les six questions de la page gagnent leur balisage FAQPage. Elles existaient
   en <details> sans aucune donnee structuree : invisibles pour un moteur comme
   pour un modele.

3. Un bloc de procedure entre en haut de page. C'est la difference que la fille
   doit faire avec la mere : la mere vend le secteur, la fille doit vendre la
   fonction — le rappel comme exercice chronometre, pas comme argument.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'maillage-cro'))
import wp_common as w

SAUVE = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PLAFOND = 275_000

PROCEDURE = (
 '<section class="hh-proc" style="margin:2.5rem 0;padding:1.6rem 1.8rem;border:1px solid #E2E8F0;'
 'border-radius:16px;background:#F8FAFC">'
 '<h2 style="margin:0 0 .4rem;font-size:1.35rem">Un rappel de lot, étape par étape</h2>'
 '<p style="margin:0 0 1.1rem;color:#475569;font-size:.95rem">'
 'L\'article 18 du <strong>règlement CE 178/2002</strong> impose de retrouver l\'origine et la '
 'destination de chaque lot. Voici ce que cela donne un jour où il faut vraiment le faire.</p>'
 '<ol style="margin:0;padding-left:1.2rem;display:flex;flex-direction:column;gap:.7rem;'
 'color:#334155;font-size:.95rem">'
 '<li><strong>Le lot suspect est identifié.</strong> Numéro de lot, produit fini, date de '
 'fabrication — saisis une fois à la production, retrouvés par recherche.</li>'
 '<li><strong>La traçabilité ascendante remonte aux matières premières.</strong> Quels lots '
 'fournisseurs sont entrés dans ce lot, en quelles quantités, livrés quand.</li>'
 '<li><strong>La traçabilité descendante redescend aux clients.</strong> Quels bons de livraison '
 'ont emporté ce lot, chez qui, à quelle date, pour quel poids.</li>'
 '<li><strong>Le périmètre s\'élargit si besoin.</strong> Si une matière première est en cause, '
 'tous les lots qui la contiennent remontent d\'un coup, pas un par un.</li>'
 '<li><strong>La liste part.</strong> Clients à prévenir, quantités concernées, documents à '
 'produire pour les autorités — exportables sans ressaisie.</li>'
 '</ol>'
 '<p style="margin:1.1rem 0 0;color:#475569;font-size:.9rem">'
 'C\'est cette capacité à démontrer un exercice de retrait-rappel qui est évaluée lors d\'un '
 'audit <strong>IFS</strong> ou <strong>BRC</strong>.</p>'
 '</section>'
)


def faq_jsonld(contenu):
    """Construit le FAQPage a partir des <details> reellement presents."""
    paires = re.findall(r'<details><summary[^>]*>(.*?)</summary>(.*?)</details>', contenu, re.S)
    net = lambda x: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip()
    items = [{"@type": "Question", "name": net(q),
              "acceptedAnswer": {"@type": "Answer", "text": net(r)}}
             for q, r in paires if net(q) and net(r)]
    assert len(items) >= 5, f"{len(items)} questions seulement"
    bloc = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return ('<script type="application/ld+json">'
            + json.dumps(bloc, ensure_ascii=False).replace('&', r'&')
            + '</script>'), len(items)


def main():
    p = w.api("pages/10968?context=edit&_fields=id,slug,content,meta")
    c = avant = p['content']['raw']
    el = (p.get('meta') or {}).get('_elementor_data', '')
    assert el in ('', '[]', None), "_elementor_data NON VIDE — on ne touche pas"
    open(f"{SAUVE}/10968-avant.html", "w").write(avant)

    # 1 — le nombre de clients
    vieux = 'Plus de 100 clients nous font confiance'
    assert c.count(vieux) == 1, f"« {vieux} » trouve {c.count(vieux)} fois"
    c = c.replace(vieux, 'Plus de 200 clients nous font confiance')
    print("  OK  nombre de clients : 100 -> 200")

    # 2 — le balisage FAQPage, absent
    assert 'FAQPage' not in c, "un FAQPage existe deja"
    bloc, n = faq_jsonld(c)
    c = c + bloc
    print(f"  OK  FAQPage pose — {n} questions")

    # 3 — le bloc de procedure, avant la FAQ
    ancre = '<details><summary>'
    i = c.find(ancre)
    assert i > 0, "aucun <details> pour se reperer"
    c = c[:i] + PROCEDURE + c[i:]
    print("  OK  bloc « Un rappel de lot, étape par étape » insere")

    assert len(c) < max(PLAFOND, len(avant)), f"rendu hors plafond : {len(c)}"
    assert c.count('FAQPage') == 1 and c.count('hh-proc') == 1
    assert '100 clients' not in c
    for mot in ('<h1 class="hero-title"', 'traçabilité alimentaire', 'de vos lots', 'INCO', 'FEFO'):
        assert mot in c, f"{mot} a disparu"

    w.api("pages/10968", method="POST", data={"content": c})
    open(f"{SAUVE}/10968-apres.html", "w").write(c)
    print(f"\n10968 /fonctionnalites/tracabilite-alimentaire/ — {len(avant)} o -> {len(c)} o")


if __name__ == "__main__":
    main()
