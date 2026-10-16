#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reconstruit le classeur de roadmap de Hello Harel et pose les statuts d'octobre.

POURQUOI UN NOUVEAU FICHIER. Le connecteur Google Drive de ma session sait
créer un fichier et renommer ou déplacer un fichier existant ; il n'a aucune
opération qui écrive DANS un fichier déjà là. Ce n'est pas une question de
droits : avec les droits d'écriture, l'outil n'existe toujours pas. Le
classeur maître n'est donc pas touché, et ce script produit un classeur à
poser à côté.

CE QU'IL REPREND À L'IDENTIQUE. Les deux feuilles de roadmap, lues dans
l'export du classeur maître :
  - ROADMAP CONTENU : 365 lignes, de août 2026 à décembre 2028 ;
  - ROADMAP TECHNIQUE : 11 lignes, T1 à T8 plus trois chantiers.
L'export rend les cellules à plat, sans frontière de ligne, et perd une partie
des cellules vides. La reconstruction ne découpe donc pas tous les 7 jetons —
ça dérive dès la première ligne à cellule vide. Elle s'accroche à des ancres
sûres : « Création » / « Mise à jour » en colonne TYPE DE PRODUCTION pour le
contenu, le statut en dernière colonne pour la technique. Chaque ligne est
ensuite vérifiée : URL du bon domaine, statut dans la liste. Une seule ligne
qui échoue arrête le script.

LES DEUX FEUILLES NON REPRISES. ROADMAP NETLINKING et CONTACTER ne sont pas
reconstruites. Elles n'ont rien à voir avec le travail d'octobre, et les
rebâtir depuis un export à plat ferait courir à la base de prospection un
risque de décalage silencieux pour aucun gain. Elles restent dans le maître.

CE QUI CHANGE : les 9 statuts du 21/09, du 28/09 et du 05/10, et 8 lignes
ajoutées à la feuille technique pour les tickets T9 à T16.
"""
import csv, io, json, os, re, sys

SRC = os.environ.get('HH_ROADMAP_TXT', '/tmp/t/roadmap.txt')
SORTIE = os.environ.get('HH_SORTIE',
    '/home/user/refonte-hh-v2/deliverables-octobre/'
    '2026-10-01-roadmap-hello-harel-2026.xlsx')

BORNES = {'contenu': (0, 57409), 'technique': (57409, 61133)}
STATUTS = ['A FAIRE', 'EN COURS', 'TERMINE', 'BLOQUE', 'INDEXE', 'ANNULEE']
MOIS = re.compile(r'^[A-ZÉÈÀÂÎÔÛ]{3,}\s+\d{4}$')
DATE = re.compile(r'^\d{2}/\d{2}/\d{4}$')


def jetons(seg, ncol):
    """En-tête + flux de cellules. La dernière cellule d'en-tête colle
    « STATUT » et le premier libellé de mois : on les redécolle."""
    t = next(csv.reader(io.StringIO(seg)))
    ent, flux = t[:ncol], list(t[ncol:])
    assert ent[-1].startswith('STATUT'), ent[-1]
    reste = ent[-1][len('STATUT'):].strip()
    ent[-1] = 'STATUT'
    if reste:
        flux.insert(0, reste)
    return ent, flux


def decoller(v):
    """« TERMINE SEPTEMBRE 2026 » -> ('TERMINE', 'SEPTEMBRE 2026')."""
    for s in STATUTS:
        if v == s:
            return s, ''
        if v.startswith(s + ' '):
            return s, v[len(s):].strip()
    return None, ''


def lire_contenu(seg):
    ent, flux = jetons(seg, 7)
    pos = [i for i, t in enumerate(flux) if t.strip() in ('Création', 'Mise à jour')]
    lignes, report = [], ''
    for k, i in enumerate(pos):
        page, url, brut = flux[i + 1].strip(), flux[i + 2].strip(), flux[i + 3].strip()
        statut, suite = decoller(brut)
        if statut is None:
            raise RuntimeError('statut inconnu ligne %d : %r' % (k, brut))
        debut = pos[k - 1] + 4 if k else 0
        tete = [x.strip() for x in flux[debut:i]]
        mois, date = report, ''
        report = suite
        req = tete[-1] if tete else ''
        for x in tete[:-1]:
            if MOIS.match(x):
                mois = x
            elif DATE.match(x):
                date = x
            elif x:
                raise RuntimeError('cellule inattendue ligne %d : %r' % (k, x))
        lignes.append([mois, date, req, flux[i].strip(), page, url, statut])
    for k, l in enumerate(lignes):
        if not l[5].startswith('https://www.helloharel.com'):
            raise RuntimeError('URL douteuse ligne %d : %r' % (k, l[5]))
    return ent, lignes


def lire_technique(seg):
    ent, flux = jetons(seg, 6)
    lignes, cour, report = [], [], ''
    for t in flux:
        v = t.strip()
        statut, suite = decoller(v)
        cour.append(v if statut is None else statut)
        if statut is not None:
            if report:
                cour.insert(0, report)
            lignes.append(([''] * (6 - len(cour))) + cour if len(cour) < 6 else cour)
            cour, report = [], suite
    if report or cour:
        raise RuntimeError('reliquat en fin de feuille technique')
    for k, l in enumerate(lignes):
        if len(l) != 6 or l[-1] not in STATUTS:
            raise RuntimeError('ligne technique %d mal formée : %r' % (k, l))
    return ent, lignes


# --------------------------------------------------------------------------
# Ce qui change
# --------------------------------------------------------------------------
NEUFS = {
    '/agroalimentaire/distribution-alimentaire/': (
        'TERMINE', 'https://www.helloharel.com/negoce/'),
    '/fonctionnalites/achat/': ('TERMINE', None),
    '/fonctionnalites/crm/': ('TERMINE', None),
    '/fonctionnalites/fabrication/': ('TERMINE', None),
    '/fonctionnalites/facturation/': ('TERMINE', None),
    '/fonctionnalites/facturation-automatique-bon-livraison/': ('TERMINE', None),
    '/fonctionnalites/gestion-consigne-bouteille-logiciel/': ('TERMINE', None),
    '/fonctionnalites/gestion-de-stock/': ('TERMINE', None),
    '/fonctionnalites/gestion-rendement-matiere-logiciel/': ('TERMINE', None),
}

TECHNIQUE_OCTOBRE = [
    ['OCTOBRE 2026', 'T9 · Les 3 landings de septembre sortaient en noindex',
     "Trois landings livrées en septembre et données INDEXE sortaient nofollow, noindex, "
     "plus /blog/erp-agroalimentaire/. Ce n'était pas l'extrait « pages de test A/B » mais "
     "un réglage Rank Math posé page par page. ACCEPTATION : les 4 URL en index, follow au "
     "recrawl — ATTEINT, 0 page en noindex sur 172.", 'CLAUDE', '1', 'TERMINE'],
    ['', 'T10 · Le générateur de meta description avait relâché',
     "4 pages créées depuis août resservaient du CSS brut comme description, "
     "/conformite-loi-anti-fraude-tva/ n'en avait aucune. ACCEPTATION : 0 description "
     "contenant { ou } — ATTEINT, et 0 description vide. LA CAUSE RESTE OUVERTE : le gabarit "
     "sert du CSS quand le champ est vide, chaque nouvelle page naîtra avec le défaut.",
     'REMI ORAVEC', '2', 'EN COURS'],
    ['', 'T11 · 88 descriptions dépassaient 985 px',
     "La plupart finissaient par une signature de marque de 50 à 70 caractères, soit "
     "exactement le dépassement, et c'est la partie la moins utile en SERP puisque la marque "
     "est déjà dans le title et l'URL. 55 traitées par règle, 31 réécrites à la main, 2 "
     "écartées. Au passage /migration-as400/ servait une description coupée en plein mot : "
     "réparée. ACCEPTATION : toutes entre 400 et 985 px — ATTEINT, 0 hors bornes.",
     'CLAUDE', '4', 'TERMINE'],
    ['', 'T12 · 39 titles en casse anglaise',
     "Cause trouvée : le réglage Rank Math « Capitalize Titles » est sur ON et applique "
     "ucwords DANS la composition du title, avant tout filtre — c'est pourquoi renvoyer le "
     "title de Rank Math ne corrigeait rien. 13 titles étaient faux en base aussi : réécrits. "
     "Les 26 autres sont corrects en base. RESTE UN CLIC : Rank Math > Titres & Méta > "
     "décocher « Capitaliser les titles ». L'écriture de ce réglage a été refusée côté "
     "sécurité de ma session. 41 titles fautifs le matin, 27 après, dont 2 voulus.",
     'REMI ORAVEC', '0.1', 'BLOQUE'],
    ['', 'T13 · Le balisage structuré dupliqué',
     "Le chiffre du matin (133 pages, ×10) était un comptage à plat des @type : sur un "
     "comparatif, l'ItemList porte légitimement un AggregateRating par concurrent. Mesuré "
     "entité par entité : 33 pages déclaraient deux fois la note de Hello Harel. L'extrait "
     "Elementor 4143 reçoit @id /#software, les SoftwareApplication fusionnent, la note est "
     "retirée des LocalBusiness et Organization. ACCEPTATION : une seule entité notée par "
     "page — 33 passées à 2, les 2 restantes sont une décision (notes éditoriales des "
     "comparatifs, 4,7 sur 1 avis contre 5 sur 31).", 'CLAUDE', '3', 'TERMINE'],
    ['', 'T14 · Les images hors WebP',
     "207 occurrences, mais 17 fichiers distincts dont 3 pèsent 183 des 207. Tous appelés "
     "depuis le contenu. WebP avec perte et sans perte essayés, le plus petit retenu, pour ne "
     "pas alourdir les captures à aplats. 648 ko vers 27, 619 vers 34, 171 vers 28 sur 70 "
     "pages. srcset et sizes retirés des img convertis. 5 images cassées (404) trouvées au "
     "passage et réparées, dont l'avatar de la signature sur 3 pages. ACCEPTATION : 100 % en "
     "WebP — ATTEINT, 207 passées à 0.", 'CLAUDE', '3', 'TERMINE'],
    ['', 'T15 · Les pages lourdes',
     "Les 2 pages comparatives servent toujours 432 ko, et le crawl compte 48 pages au-dessus "
     "de 300 ko, pas 2. Le seuil de rendu n'est pas atteint mais il n'y a aucune marge. C'est "
     "un ticket de gabarit : le CSS et le JS du gabarit métier pèsent l'essentiel, et les "
     "alléger demande de mesurer quelles règles servent à quel gabarit avant d'en retirer "
     "une. ACCEPTATION : moins de 300 ko servis — NON ATTEINT.", 'CLAUDE', '3', 'A FAIRE'],
    ['', 'T16 · Les H1',
     "/comparatifs/ servait deux H1 : celui du gabarit du thème, qui imprimait le titre du "
     "post — un title de SERP, pas un H1 — et celui du contenu. Titre du post refait, H1 du "
     "contenu passé en H2, et le hub liste les 4 comparatifs au lieu de 3. 0 page à deux H1 "
     "au recrawl. 4 pages restent sans H1 : 3 sont construites dans Elementor (widget titre, "
     "à changer dans l'éditeur), la 4e est rendue par un gabarit sans contenu en base.",
     'REMI ORAVEC', '1', 'EN COURS'],
]


def appliquer(lignes):
    faits = set()
    for l in lignes:
        u = l[5].replace('https://www.helloharel.com', '')
        if u in NEUFS and l[6] == 'A FAIRE':
            statut, url = NEUFS[u]
            l[6] = statut
            if url:
                l[5] = url
            faits.add(u)
    manquants = set(NEUFS) - faits
    if manquants:
        raise RuntimeError('lignes non trouvées : ' + ', '.join(sorted(manquants)))
    return len(faits)


# --------------------------------------------------------------------------

def ecrire(ent_c, lignes_c, ent_t, lignes_t, chemin):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    COULEURS = {'A FAIRE': ('F1F3F4', '5F6368'), 'EN COURS': ('FEF7E0', 'B06000'),
                'TERMINE': ('E6F4EA', '1E8E3E'), 'BLOQUE': ('FCE8E6', 'C5221F'),
                'INDEXE': ('E6F4EA', '1E8E3E'), 'ANNULEE': ('F1F3F4', '5F6368')}
    trait = Side(style='thin', color='E3E5E8')
    bord = Border(left=trait, right=trait, top=trait, bottom=trait)
    centre = Alignment(horizontal='center', vertical='center', wrap_text=False)

    wb = Workbook()
    for nom, ent, lignes, large in (
            ('ROADMAP CONTENU', ent_c, lignes_c, False),
            ('ROADMAP TECHNIQUE', ent_t, lignes_t, True)):
        ws = wb.create_sheet(nom)
        ws.append(ent)
        for l in lignes:
            ws.append(l)
        for c in ws[1]:
            c.font = Font(name='Comfortaa', size=10, bold=True, color='FFFFFF')
            c.fill = PatternFill('solid', fgColor='1A73E8')
            c.alignment = centre
            c.border = bord
        i_st = len(ent)
        for r in range(2, ws.max_row + 1):
            st = str(ws.cell(r, i_st).value or '').strip()
            fond, texte = COULEURS.get(st, (None, '202124'))
            for c in ws[r]:
                c.font = Font(name='Comfortaa', size=10, color=texte)
                c.alignment = centre
                c.border = bord
                if fond:
                    c.fill = PatternFill('solid', fgColor=fond)
        for j, libelle in enumerate(ent, start=1):
            vals = [str(ws.cell(r, j).value or '') for r in range(1, ws.max_row + 1)]
            l = max([len(libelle)] + [len(v) for v in vals])
            ws.column_dimensions[get_column_letter(j)].width = min(90, max(14, l + 4))
        ws.freeze_panes = 'A2'
    del wb['Sheet']
    wb.save(chemin)
    return chemin


def main():
    c = open(SRC, encoding='utf-8').read()
    ent_c, lignes_c = lire_contenu(c[slice(*BORNES['contenu'])])
    ent_t, lignes_t = lire_technique(c[slice(*BORNES['technique'])])
    print('ROADMAP CONTENU   : %d lignes relues' % len(lignes_c))
    print('ROADMAP TECHNIQUE : %d lignes relues' % len(lignes_t))
    n = appliquer(lignes_c)
    print('%d statuts de contenu passés à jour' % n)
    lignes_t += TECHNIQUE_OCTOBRE
    print('%d lignes techniques après ajout de T9 à T16' % len(lignes_t))
    p = ecrire(ent_c, lignes_c, ent_t, lignes_t, SORTIE)
    print('écrit :', p, os.path.getsize(p), 'o')


if __name__ == '__main__':
    main()
