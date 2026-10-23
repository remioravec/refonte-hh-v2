# -*- coding: utf-8 -*-
"""Comparatif facturation grossiste (7922) : aligner les tarifs Hello Harel sur les
licences reelles et retirer la promesse d'inclusion du deploiement et de la formation,
desormais vendus a part via Harel Formation.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'maillage-cro'))
import wp_common as w

SAUVE = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
PLAFOND = 400_000   # cette page est longue : 354 ko avant

# (vieux, neuf, occurrences attendues)
R = [
 ("Starter 99 € HT/mois — Pro 199 € HT/mois (par utilisateur, déploiement et formation inclus).",
  "Blossom 49 € — Garden 79 € — Forest 99 € HT/mois (par utilisateur). "
  "Déploiement et formation en option.", 1),

 ("(Hello Harel) : 99 à 199 € HT/utilisateur/mois, déploiement inclus.",
  "(Hello Harel) : 49 à 99 € HT/utilisateur/mois, déploiement et formation en option.", 2),

 ("dès 99 €/mois", "dès 49 €/mois", 1),

 ("à un tarif PME (99 €/mois)", "à un tarif PME (dès 49 €/mois)", 1),

 ("<strong>Support 100% France</strong> depuis Lille, équipe dédiée, formation incluse au déploiement.",
  "<strong>Support 100% France</strong> depuis Lille, équipe dédiée. "
  "Formation et déploiement assurés en option.", 1),

 ("Temps moyen entre signature et go-live, formation incluse.",
  "Temps moyen entre signature et go-live.", 1),
]

def main():
    p = w.api("pages/7922?context=edit&_fields=id,slug,content,meta")
    c = avant = p['content']['raw']
    el = (p.get('meta') or {}).get('_elementor_data', '')
    assert el in ('', '[]', None), "_elementor_data NON VIDE — on ne touche pas"
    open(f"{SAUVE}/7922-avant.html", "w").write(avant)

    notes = []
    for vieux, neuf, attendu in R:
        n = c.count(vieux)
        if n != attendu:
            print(f"ABANDON — « {vieux[:60]}… » trouve {n} fois, attendu {attendu}")
            sys.exit(1)
        c = c.replace(vieux, neuf)
        notes.append(f"OK x{n}  « {vieux[:58]}… »")

    assert len(c) < max(PLAFOND, len(avant)), f"rendu hors plafond : {len(c)}"
    for mot in ("déploiement inclus", "formation incluse", "199 € HT/mois"):
        assert mot not in c, f"« {mot} » encore present"
    for mot in ("Hello Harel", "Factur-X", "Pennylane", "Sage X3"):
        assert mot in c, f"{mot} a disparu"

    w.api("pages/7922", method="POST", data={"content": c})
    open(f"{SAUVE}/7922-apres.html", "w").write(c)
    print("\n".join(notes))
    print(f"\n7922 enregistre — {len(avant)} o -> {len(c)} o")

if __name__ == "__main__":
    main()
