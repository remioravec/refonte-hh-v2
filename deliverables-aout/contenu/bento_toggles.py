#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Le bento des fonctionnalites devient un module a onglets avec ecran.

CE QUI EST REPRIS DE LA PAGE, ET NON REECRIT — le bento porte deja le contenu
juste : un titre, un paragraphe, parfois des puces, souvent un lien de
maillage interne. Tout cela est extrait de la page et repose tel quel dans les
onglets. On ne change pas ce que la page dit ; on change la facon dont elle le
montre, et on ajoute un ecran du logiciel a chaque fonctionnalite.

LES LIENS DE MAILLAGE — chaque carte du bento porte souvent un lien vers une
autre page. Les perdre couterait du maillage interne sur trente et une pages.
Ils sont comptes avant et apres, et la conversion est refusee s'il en manque
un seul.

LE CHOIX DE L'ECRAN — vingt-trois ecrans en bibliotheque, choisis par mots
cles sur le titre et le texte de la carte. Un ecran deja pris sur la page
n'est pas repris : chaque page montre cinq ecrans differents.

Usage :  python3 bento_toggles.py <id_de_page>   (apercu d'une page)
"""

import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import agro_ui as A                         # noqa: E402
import traiteur_ui as T                     # noqa: E402
import rungis_modules as R                  # noqa: E402
import ecrans_plus as P                     # noqa: E402

# nom -> (fabrique, [mots cles])
ECRANS = {
 "cout":        (A.ecran_cout, ["coût", "cout", "revient", "marge", "rentab", "prix",
                                "valoris", "rendement"]),
 "tracabilite": (A.ecran_tracabilite, ["traçab", "tracab", "lot", "rappel", "origine",
                                       "sanitaire", "amont", "aval"]),
 "dlc":         (A.ecran_dlc, ["dlc", "date limite", "péremption", "peremption", "dluo",
                               "fefo", "fraîcheur", "fraicheur"]),
 "stocks":      (A.ecran_stocks_sensibles, ["stock", "chambre", "froid", "température",
                                            "temperature", "inventaire", "sensible"]),
 "haccp":       (A.ecran_haccp, ["haccp", "hygiène", "hygiene", "contrôle qualité",
                                 "non-conformité", "audit", "règlement", "reglement",
                                 "conformité", "conformite"]),
 "fiches":      (T.ecran_fiches, ["fiche technique", "recette", "gramm", "composant"]),
 "evenements":  (T.ecran_evenements, ["événement", "evenement", "prestation", "devis",
                                      "réception", "buffet", "commande client"]),
 "allergenes":  (T.ecran_allergenes, ["allergène", "allergene", "étiquetage", "etiquetage",
                                      "inco", "mention"]),
 "logistique":  (T.ecran_logistique, ["logistique", "livraison", "expédition", "expedition",
                                      "chargement"]),
 "achat":       (R.ecran_achat, ["achat", "approvision", "fournisseur", "cours",
                                 "négoc", "negoc", "tarif d'achat"]),
 "agreage":     (R.ecran_agreage, ["agréage", "agreage", "pesée", "pesee", "poids",
                                   "réception", "reception", "écart", "ecart"]),
 "preparation": (R.ecran_preparation, ["préparation", "preparation", "colisage",
                                       "picking", "découpe", "decoupe", "conditionn"]),
 "tournee":     (R.ecran_tournee, ["tournée", "tournee", "transport", "camion",
                                   "distribution"]),
 "facture":     (R.ecran_facture, ["factur", "compta", "règlement", "reglement",
                                   "tva", "avoir"]),
 "marge":       (R.ecran_marge, ["statistique", "reporting", "tableau de bord",
                                 "pilotage", "analyse", "indicateur", "performance"]),
 "clients":     (P.ecran_clients, ["client", "crm", "relation", "commercial", "prospect",
                                   "encours", "vente"]),
 "edi":         (P.ecran_edi, ["edi", "import", "export", "échange", "echange",
                               "interfac", "dématérial", "demateriali"]),
 "production":  (P.ecran_production, ["production", "fabrication", "fournée", "fournee",
                                      "planification", "atelier", "ordre de fab", "cuisson"]),
 "sites":       (P.ecran_sites, ["multi", "dépôt", "depot", "boutique", "site",
                                 "entrepôt", "entrepot", "point de vente", "magasin"]),
}

DEFAUT = ["cout", "tracabilite", "stocks", "production", "clients"]


def choisir(titre, texte, pris):
    """Ecran le mieux assorti, jamais deux fois le meme sur une page."""
    t = (titre + " " + texte).lower()
    scores = []
    for nom, (fab, mots) in ECRANS.items():
        if nom in pris:
            continue
        s = sum(3 if m in titre.lower() else 1 for m in mots if m in t)
        if s:
            scores.append((s, nom))
    if scores:
        scores.sort(reverse=True)
        return scores[0][1]
    for nom in DEFAUT:
        if nom not in pris:
            return nom
    for nom in ECRANS:
        if nom not in pris:
            return nom
    return "cout"


def _texte(x):
    import html as _h
    return _h.unescape(re.sub(r"<[^>]+>", "", x or "")).strip()


def _riche(x):
    """Comme _texte, mais garde les liens et la mise en valeur du texte.

    Un lien pose DANS le paragraphe d'une carte est du maillage interne au meme
    titre que le lien de pied de carte. Le nettoyer le ferait disparaitre.
    """
    x = re.sub(r"</?(?!a\b|strong\b|em\b|b\b|i\b)[a-zA-Z][^>]*>", "", x or "")
    return re.sub(r"\s+", " ", x).strip()


def cartes(section):
    """Extrait les cartes du bento : titre, chapo, puces, lien de maillage."""
    out = []
    for m in re.finditer(r'<div class="bento-card[^"]*"[^>]*>', section):
        i = m.start()
        prof, j = 0, i
        while j < len(section):
            a, b = section.find("<div", j), section.find("</div>", j)
            if b < 0:
                break
            if 0 <= a < b:
                prof += 1; j = a + 4
            else:
                prof -= 1; j = b + 6
                if prof == 0:
                    break
        bloc = section[i:j]
        h = re.search(r"<h3[^>]*>(.*?)</h3>", bloc, re.S)
        if not h:
            continue
        # le chapo est le premier <p> qui suit le titre, pas le premier du bloc :
        # sinon on recolle le titre devant le texte.
        pm = re.search(r"<p[^>]*>(.*?)</p>", bloc[h.end():], re.S)
        chapo = _riche(pm.group(1)) if pm else ""
        if chapo.startswith(_texte(h.group(1))):
            chapo = chapo[len(_texte(h.group(1))):].strip()
        puces = [_riche(x) for x in re.findall(r"<li[^>]*>(.*?)</li>", bloc, re.S)]
        # une carte peut porter PLUSIEURS liens de pied — la carte « Fabrication,
        # Achats, Logistique & Import-export » en porte quatre. N'en garder qu'un
        # couterait trois liens internes.
        liens = [(m.group(1), _texte(m.group(2))) for m in re.finditer(
            r'<a href="([^"]+)"[^>]*class="card-link"[^>]*>(.*?)</a>', bloc, re.S)]
        out.append({"titre": _texte(h.group(1)), "chapo": chapo, "puces": puces,
                    "liens": liens})
    return out


ARRET = {"de", "des", "du", "d'", "au", "aux", "la", "le", "les", "et", "&", "à",
         "en", "par", "sur", "pour", "dans", "un", "une", "avec", "sans", "ou"}


def court(titre):
    """Libelle d'onglet : deux ou trois mots, et jamais coupe sur un mot outil."""
    t = re.sub(r"\s*\(.*?\)\s*", " ", titre)
    t = re.split(r"[&,:—–]|\bet\b", t)[0].strip()
    t = re.sub(r"^(gestion|suivi|calcul|maîtrise|maitrise)\s+(de la|des|du|de|d')\s+",
               "", t, flags=re.I).strip()
    mots = t.split()
    gardes = []
    for m in mots:
        essai = " ".join(gardes + [m])
        if gardes and len(essai) > 19:
            break
        gardes.append(m)
    while gardes and gardes[-1].lower().strip(".,;") in ARRET:
        gardes.pop()
    if not gardes:
        gardes = [mots[0]] if mots else ["Fonction"]
    s = " ".join(gardes)
    return s[0].upper() + s[1:]


def module(section):
    """Le bento devient le module a onglets. Retourne (html, journal)."""
    ent = re.search(r'<div class="section-header">.*?</div>', section, re.S)
    if not ent:
        raise ValueError("entete de section introuvable")
    cs = cartes(section)
    if not 4 <= len(cs) <= 7:
        raise ValueError("%d cartes dans le bento" % len(cs))

    blocs, courts, pris = [], [], set()
    for c in cs:
        nom = choisir(c["titre"], c["chapo"] + " " + " ".join(c["puces"]), pris)
        pris.add(nom)
        puces = c["puces"] or [p.strip() for p in re.split(r"(?<=[.!?])\s+", c["chapo"])
                               if len(p.strip()) > 12][:3]
        lien = "".join('<a class="hhf-lien" href="%s">%s →</a>' % (u, t)
                       for u, t in c["liens"])
        blocs.append((c["titre"], c["chapo"], puces[:4], ECRANS[nom][0], lien))
        courts.append(court(c["titre"]))
    return A.section(ent.group(0), blocs, courts), [n for n in pris]


def convertir(contenu):
    """Remplace la section bento par le module. Retourne (contenu, journal)."""
    # certaines pages portent plusieurs features-section : on vise CELLE qui
    # contient le bento, pas la premiere venue.
    trouves = []
    for m in re.finditer(r'<section class="features-section"', contenu):
        i = m.start()
        j = contenu.find("</section>", i)
        # seules les cartes en <div> sont des fonctionnalites. Une carte en
        # <a class="bento-card"> est une vignette de navigation vers une autre
        # page : la convertir en onglet detruirait un bloc de liens.
        if j > 0 and '<div class="bento-card' in contenu[i:j]:
            trouves.append((i, j))
    if not trouves:
        raise ValueError("aucune features-section avec un bento")
    tous = []
    for i, j in reversed(trouves):          # a rebours : les bornes restent justes
        sec = contenu[i:j + 10]
        avant = len(re.findall(r'<a href="[^"]+"[^>]*class="card-link"', sec))
        neuf, ecrans = module(sec)
        apres = neuf.count('class="hhf-lien"')
        if apres != avant:
            raise ValueError("liens de pied de carte : %d avant, %d apres" % (avant, apres))
        contenu = contenu[:i] + neuf + contenu[j + 10:]
        tous = ecrans + tous
    return contenu, tous


if __name__ == "__main__":
    sys.path.insert(0, "/home/user/refonte-hh-v2/maillage-cro")
    import wp_common as w
    pid = int(sys.argv[1]) if len(sys.argv) > 1 else 3309
    c = w.get_raw("pages", pid)["content"]["raw"]
    n, ecrans = convertir(c)
    print("page %d : %d -> %d octets" % (pid, len(c), len(n)))
    print("ecrans retenus :", ", ".join(ecrans))
    i = n.find('<section class="features-section"')
    print("onglets :", re.findall(r'<label for="hhf-o\d+"><b>\d+</b>([^<]+)</label>',
                                  n[i:i + 40000]))
