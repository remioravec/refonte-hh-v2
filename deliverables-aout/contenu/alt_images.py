#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Onze images de contenu étaient servies sans texte alternatif utile.

CE QUI SE PASSAIT. Rank Math avait deux réglages d'images actifs :

    add_img_title = on,  format « %title% %count(title)% »
    add_img_alt   = on,  format « %filename% %search_query% »

Le premier posait, sur CHAQUE image du contenu, un attribut title qui recopie
le title de SERP suivi d'un compteur : sur une page métier, 65 images sur 67
affichaient au survol « ERP Boulangerie • Recettes & Coût de Revient • 0€ ☁️ 47 ».
Le second écrasait les alt vides par le nom de fichier ; sur les 14 avatars en
data:image/svg+xml, « %filename% » rendait la fin de l'URI, d'où alt="svg%3E"
quatorze fois par page.

Les deux réglages sont passés à off. Les avatars décoratifs retrouvent un alt
vide, ce qui est la bonne valeur pour une image décorative (la liste porte
déjà aria-hidden). Restent onze images de contenu qui n'avaient pas d'alt
propre et dont Rank Math masquait l'absence : elles en reçoivent un, écrit
après avoir regardé chaque image.
"""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'maillage-cro'))
import ns_api as n

SAUVE = os.environ.get('HH_SAUVE', '/tmp/t/avant-alt')

ALT = {
 'erp-boulanger-fournil-professionnel.webp':
   "Boulanger sortant une plaque de pains d'une échelle de cuisson, en fournil professionnel",
 'erp-negoce-alimentaire-epicerie-cagettes-salades.webp':
   "Commerçant disposant des cagettes de salades et de courgettes dans le rayon frais d'une épicerie",
 'erp-industrie-laitiere-atelier-fabrication.webp':
   "Fromagère démoulant des fromages frais à côté d'une balance, en atelier de fabrication laitière",
 'Screenshot-2026-02-14-08.34.42.webp':
   "Deux professionnels contrôlant des barquettes de tomates cerises dans un entrepôt de fruits et légumes",
 'Logiciel-de-gestion-des-achats-1.webp':
   "Magasinier en gilet de sécurité relevant les stocks sur un ordinateur portable dans un entrepôt",
 'Logiciel-de-gestion-des-achats-3.webp':
   "Charcutier parant une pièce de viande devant un rayon de saucissons secs",
 'Maxence-150x150-1.webp':
   "Maxence Flavigny, responsable commercial de Hello Harel",
 'Calculs-des-couts-de-production.svg':
   "Schéma opposant le coût de production, limité aux dépenses de fabrication, "
   "et le coût de revient, qui inclut la distribution et le marketing",
 'Exemple-de-facture-traiteur-724x1024-1.webp':
   "Exemple de facture de traiteur",
 'Optimiser-la-gestion-de-votre-inventaire-avec-erp-logiciel-comme-hello-harel-1024x683-1.webp':
   "Processus de gestion des inventaires en six étapes, des entrées et sorties "
   "en temps réel jusqu'au reporting",
 'Optimiser-la-relation-client-avec-automatisation-des-relances-683x1024-1.webp':
   "Processus de relance client, du premier contact à la clôture du dossier ou "
   "à une offre spéciale",
}


def corps():
    """Tous les posts et pages, contenu brut."""
    out = {}
    for base in ('posts', 'pages'):
        p = 1
        while True:
            try:
                lot = n.call(f'wp/v2/{base}?per_page=50&page={p}&context=edit'
                             f'&_fields=id,link,content,meta')
            except RuntimeError as e:
                if 'invalid_page_number' in str(e):
                    break
                raise
            if not isinstance(lot, list) or not lot:
                break
            for x in lot:
                out[(base, x['id'])] = x
            if len(lot) < 50:
                break
            p += 1
    return out


def poser(contenu):
    """Remplit l'alt vide des <img> connues. Ne touche jamais un alt déjà écrit."""
    faits = []

    def f(m):
        tag = m.group(0)
        s = re.search(r'\bsrc="([^"]*)"', tag)
        if not s:
            return tag
        nom = s.group(1).rsplit('/', 1)[-1].split('?')[0]
        if nom not in ALT:
            return tag
        a = re.search(r'\balt="([^"]*)"', tag)
        if a and a.group(1).strip():
            return tag
        faits.append(nom)
        if a:
            return tag[:a.start(1)] + ALT[nom] + tag[a.end(1):]
        return tag[:-1].rstrip() + ' alt="' + ALT[nom] + '">'

    return re.sub(r'(?is)<img\b[^>]*>', f, contenu), faits


def main(ecrire=False):
    os.makedirs(SAUVE, exist_ok=True)
    tout = corps()
    print(len(tout), 'posts et pages lus')
    total = {}
    pages = 0
    for (base, pid), x in sorted(tout.items()):
        c = x['content']['raw']
        c2, faits = poser(c)
        if not faits:
            continue
        if x['meta'].get('_elementor_data') not in ('', '[]', None):
            print(f'  IGNORÉE (elementor non vide) {base}/{pid}')
            continue
        assert '"' not in ''.join(ALT.values())
        assert len(c2) > len(c)
        pages += 1
        for nm in faits:
            total[nm] = total.get(nm, 0) + 1
        open(os.path.join(SAUVE, f'{base}-{pid}.html'), 'w').write(c)
        if ecrire:
            n.call(f'wp/v2/{base}/{pid}', 'POST', {'content': c2})
    print(f'\n{pages} pages touchées')
    for nm, k in sorted(total.items(), key=lambda kv: -kv[1]):
        print(f'  {k:3}x {nm}')


if __name__ == '__main__':
    main('--ecrire' in sys.argv)
