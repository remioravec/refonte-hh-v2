# -*- coding: utf-8 -*-
"""Page /tarifs/ (608) : retrait de la promesse d'inclusion devenue fausse,
« plans » -> « licences », badge Populaire deplace de Garden vers Forest.

Demande de Maxence Flavigny, WhatsApp du 17/10/2026 : l'integration et la
formation sont desormais vendues a part, la page les annonce comme comprises.
"""
import os, re, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'maillage-cro'))
import wp_common as w

PLAFOND = 275_000
SAUVE = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/avant-tarifs"

REMPLACEMENTS = [
    # 1 — la promesse d'inclusion (hero) + « plan » -> « licence »
    ("Choisissez le plan adapté à vos besoins. Tous nos plans incluent le déploiement, "
     "la formation et le support. Sans engagement.",
     "Choisissez la licence adaptée à vos besoins. Tarif mensuel par utilisateur, sans engagement."),
    # 2 — le H2 de la grille
    ("Choisissez le plan adapté à votre activité",
     "Choisissez la licence adaptée à votre activité"),
    # 3 — la promesse d'inclusion (sous-titre de grille)
    ("Tous les plans incluent le déploiement et la formation",
     "Trois licences, au mois et par utilisateur"),
]

# 4 — le badge « Populaire » passe de Garden a Forest
BADGE = '<div class="pricing-badge">Populaire</div>'


def deplacer_badge(c, notes):
    # on retire featured + badge de GARDEN
    av = c
    c = c.replace(
        '<!-- GARDEN (FEATURED) -->             <div class="pricing-card featured">'
        '                 ' + BADGE,
        '<!-- GARDEN -->             <div class="pricing-card">')
    if c == av:  # espacement different : on retombe sur une regex bornee
        c = re.sub(
            r'(<!--\s*GARDEN[^>]*-->\s*<div class="pricing-card)\s+featured("\s*>)\s*'
            + re.escape(BADGE),
            r'\1\2', c, count=1)
    if c == av:
        notes.append("GARDEN : badge NON retire")
        return av
    notes.append("GARDEN : featured + badge retires")

    av2 = c
    c = re.sub(r'(<!--\s*FOREST\s*-->\s*<div class="pricing-card)("\s*>)',
               r'\1 featured\2' + BADGE, c, count=1)
    if c == av2:
        notes.append("FOREST : badge NON pose — ANNULATION")
        return av
    notes.append("FOREST : featured + badge poses")
    return c


def main():
    p = w.api("pages/608?context=edit&_fields=id,slug,content,meta")
    c = avant = p['content']['raw']
    el = (p.get('meta') or {}).get('_elementor_data', '')
    assert el in ('', '[]', None), f"_elementor_data NON VIDE — on ne touche pas ({len(str(el))} o)"
    open(f"{SAUVE}/608-avant.html", "w").write(avant)

    notes = []
    for vieux, neuf in REMPLACEMENTS:
        n = c.count(vieux)
        if n != 1:
            notes.append(f"ABANDON — « {vieux[:48]}… » trouve {n} fois (attendu 1)")
            print("\n".join(notes)); sys.exit(1)
        c = c.replace(vieux, neuf)
        notes.append(f"OK  « {vieux[:52]}… »  ->  « {neuf[:52]}… »")

    c = deplacer_badge(c, notes)

    # garde-fous
    assert len(c) < max(PLAFOND, len(avant)), f"rendu hors plafond : {len(c)}"
    assert c.count(BADGE) == 1, f"badge en {c.count(BADGE)} exemplaires"
    assert c.count('class="pricing-card featured"') == 1, "plus d'une carte mise en avant"
    assert 'incluent le déploiement' not in c, "promesse d'inclusion encore presente"
    for mot in ('Blossom', 'Garden', 'Forest', '49€', '79€', '99€'):
        assert mot in c, f"{mot} a disparu"

    w.api("pages/608", method="POST", data={"content": c})
    open(f"{SAUVE}/608-apres.html", "w").write(c)
    print("\n".join(notes))
    print(f"\n608 /tarifs/ enregistre — {len(avant)} o -> {len(c)} o")


if __name__ == "__main__":
    main()
