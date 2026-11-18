# -*- coding: utf-8 -*-
"""/blog/conformite-haccp/ (5574) — lot du 26/10, volet maillage.

L'article est deja bien equipe : FAQPage pose, chiffre client a jour, trois
liens vers /agroalimentaire/. Mais zero lien vers
/fonctionnalites/tracabilite-alimentaire/, alors que la tracabilite est le coeur
du sujet et que cette page est la fille dominee par sa mere (position 35,6
contre 24,5 pour /agroalimentaire/).

Un lien contextuel depuis un article en position 24,2 vers une page en 35,6,
avec une ancre exact match et naturelle, posee dans la phrase qui parle
precisement de ca.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'maillage-cro'))
import wp_common as w

SAUVE = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PLAFOND = 275_000
CIBLE = "https://www.helloharel.com/fonctionnalites/tracabilite-alimentaire/"

VIEUX = ("<p>Lien automatique entre lots de production et contrôles HACCP pour une "
         "traçabilité ascendante et descendante parfaite.</p>")
NEUF = ('<p>Lien automatique entre lots de production et contrôles HACCP. Le '
        '<a href="%s">logiciel de traçabilité alimentaire</a> remonte d\'un lot sortant à '
        'ses matières premières et redescend à tous les clients livrés.</p>' % CIBLE)


def main():
    p = w.api("posts/5574?context=edit&_fields=id,slug,content,meta")
    c = avant = p['content']['raw']
    el = (p.get('meta') or {}).get('_elementor_data', '')
    assert el in ('', '[]', None), "_elementor_data NON VIDE — on ne touche pas"
    open(f"{SAUVE}/5574-avant.html", "w").write(avant)

    assert c.count(CIBLE) == 0, "le lien existe deja"
    n = c.count(VIEUX)
    assert n == 1, f"phrase d'accueil trouvee {n} fois, attendu 1"
    c = c.replace(VIEUX, NEUF)

    assert len(c) < max(PLAFOND, len(avant))
    assert c.count(CIBLE) == 1, "le lien n'est pas unique"
    assert c.count('FAQPage') == avant.count('FAQPage'), "le FAQPage a bouge"
    for mot in ('Principes HACCP', 'Hello Harel', 'Actions correctives'):
        assert mot in c, f"{mot} a disparu"

    w.api("posts/5574", method="POST", data={"content": c})
    open(f"{SAUVE}/5574-apres.html", "w").write(c)
    print("  OK  lien pose, ancre « logiciel de traçabilité alimentaire »")
    print(f"\n5574 /blog/conformite-haccp/ — {len(avant)} o -> {len(c)} o")


if __name__ == "__main__":
    main()
