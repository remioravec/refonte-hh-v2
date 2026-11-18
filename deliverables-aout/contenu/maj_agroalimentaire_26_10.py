# -*- coding: utf-8 -*-
"""/agroalimentaire/ (1726) — lot du 26/10.

Trois choses, dans cet ordre d'importance :

1. « +150 clients » devient « +200 ». L'AI Overview de « erp agroalimentaire »
   est en position absolue 1 et recopie fidelement ce que la page dit : il
   annonce « 150+ clients » parce que la page l'ecrit. Le site revendique 200+
   PME depuis le title de l'accueil.

2. Le tarif reel entre sur la page, sous forme extractible. L'AIO annonce
   « des 29 EUR/mois/utilisateur », un prix qui n'existe plus : il le tire
   d'ailleurs, faute de source fraiche ici. L'entree de gamme est la licence
   Blossom a 49 EUR HT par mois et par utilisateur.

3. Le bloc « Conformite HACCP » gagne deux points precis et citables. C'est le
   lot qualite : plutot que creer /fonctionnalites/qualite-qhse-agroalimentaire/
   sur une SERP tenue par des LIMS et des SMQ, on renforce la page qui tient
   deja la position 15 sur ce champ.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'maillage-cro'))
import wp_common as w

SAUVE = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PLAFOND = 275_000

R = [
    # --- 1 : le nombre de clients, aligne sur le reste du site
    ('<span class="stat-number">+150</span><span class="stat-label">Clients</span>',
     '<span class="stat-number">+200</span><span class="stat-label">Clients</span>', 1),

    ('Accompagne + de 150 clients agroalimentaires français.',
     'Accompagne + de 200 clients agroalimentaires français.', 1),

    ('<span class="hh2-author-tag">+ de 150 clients</span>',
     '<span class="hh2-author-tag">+ de 200 clients</span>', 1),

    # --- 2 : le tarif reel, en clair et extractible
    ('<div class="about-stat-card"><span class="stat-number">+200</span><span class="stat-label">Clients</span></div>',
     '<div class="about-stat-card"><span class="stat-number">+200</span><span class="stat-label">Clients</span></div>'
     '<div class="about-stat-card"><span class="stat-number">49 €</span>'
     '<span class="stat-label">HT / mois / utilisateur</span></div>', 1),

    # --- 3 : le bloc conformite, plus precis donc plus citable
    ('<h2>Conformité HACCP</h2><ul class="hhf-pts">'
     '<li><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
     '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M5 13l4 4L19 7"/></svg>'
     'Enregistrements numériques, plans de nettoyage, documentation pour les autorités sanitaires.</li>',

     '<h2>Conformité HACCP</h2><ul class="hhf-pts">'
     '<li><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
     '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M5 13l4 4L19 7"/></svg>'
     'Traçabilité ascendante et descendante, comme l\'exige l\'article 18 du '
     '<strong>règlement CE 178/2002</strong> : d\'un lot sortant à ses matières premières, '
     'et d\'une matière première à tous les lots qui la contiennent.</li>'
     '<li><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
     '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M5 13l4 4L19 7"/></svg>'
     'Relevés de température horodatés, non-conformités tracées, plan d\'action par écart — '
     'de quoi répondre à un audit IFS ou BRC sans ressortir un classeur.</li>'
     '<li><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">'
     '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" d="M5 13l4 4L19 7"/></svg>'
     'Enregistrements numériques, plans de nettoyage, documentation pour les autorités sanitaires.</li>', 1),
]


def main():
    p = w.api("pages/1726?context=edit&_fields=id,slug,content,meta")
    c = avant = p['content']['raw']
    el = (p.get('meta') or {}).get('_elementor_data', '')
    assert el in ('', '[]', None), "_elementor_data NON VIDE — on ne touche pas"
    open(f"{SAUVE}/1726-avant.html", "w").write(avant)

    for vieux, neuf, att in R:
        n = c.count(vieux)
        if n != att:
            print(f"ABANDON — « {vieux[:62]}… » trouve {n} fois, attendu {att}")
            sys.exit(1)
        c = c.replace(vieux, neuf)
        print(f"  OK  « {vieux[:66]}… »")

    assert len(c) < max(PLAFOND, len(avant)), f"rendu hors plafond : {len(c)}"
    assert '+150' not in c and '+ de 150 clients' not in c, "il reste un 150"
    cartes = c.count('<div class="about-stat-card">')
    assert cartes == 4, f"{cartes} cartes au lieu de 4"
    assert 'CE 178/2002' in c and 'Blossom' not in c
    for mot in ('Conformité HACCP', 'Timothy Jollivet', 'hero-title'):
        assert mot in c, f"{mot} a disparu"

    w.api("pages/1726", method="POST", data={"content": c})
    open(f"{SAUVE}/1726-apres.html", "w").write(c)
    print(f"\n1726 /agroalimentaire/ enregistre — {len(avant)} o -> {len(c)} o")


if __name__ == "__main__":
    main()
