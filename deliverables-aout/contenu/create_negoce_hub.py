#!/usr/bin/env python3
"""
Variante B de /negoce/ — LE HUB du modele boost <=> landing. BROUILLON NOINDEX.

MODELE (skill maillage-interne, profil SAAS) :
  Le HUB explique et rassure (« comment choisir »), il ne vise JAMAIS la requete
  de sa landing, et fait UN SEUL lien editorial sortant : vers elle.
  Les sections 1 a 5 arrosent les pages filles — l'etage que personne ne maille.
  La LANDING vend : /fonctionnalites/import-export/.

CONSTATS DATES (GSC 15/05->12/08/2026, releve du 18/08) :
  - Regle 6 — dispersion : /negoce/ porte 37 liens uniques dans son corps, dont
    6 seulement restent dans le silo. Fuites : 9 footer/legal, 8 fonctionnalites,
    7 metiers agro, 4 blog et 3 vers /medical/ (hors sujet).
  - Regle 7 — les 6 liens du silo existent DEJA : c'est une passe de cablage
    d'ancres, pas une reecriture. 3 ancres sont neutres (« En savoir plus »),
    ce que la politique d'ancres interdit.
  - Le silo /negoce/ fait 173 impressions et 0 clic ; la mere est en position
    51,7 et attire le negoce BTP.
  - Sur l'import-export, le comparatif surclasse la landing partout :
    erp importateur pos 5,1 vs 19,6 · logiciel import export pos 7,5 vs 21,1.

Statut : brouillon (inaccessible au public, donc non indexable).
DRY par defaut ; --live pour creer.
"""
import sys, json
import wp_common as w

SLUG = "negoce-test-b-hub"
TITLE = "[TEST B] Comment choisir son ERP de négoce alimentaire • Guide"
LANDING = "/fonctionnalites/import-export/"

# Jeu d'ancres exact-match qui tourne — aucune ancre neutre (politique d'ancres)
SECTIONS = [
 ("Par où commencer : l’achat, ou la vente ?",
  "Dans un négoce alimentaire, le désordre vient rarement de la vente. Il vient de l’amont : "
  "un cadencier fournisseur tenu sous tableur, des contrats d’achat renégociés à l’oral, des "
  "quantités engagées que personne ne suit. Si vous hésitez sur le point d’entrée, commencez "
  "par là — c’est celui qui fait bouger la marge le plus vite.",
  "/negoce/achats-approvisionnements/", "gérer les achats et approvisionnements"),

 ("Un entrepôt ou plusieurs : ce que ça change vraiment",
  "Tant qu’il n’y a qu’un dépôt, un tableur tient. Dès qu’il y en a deux, la question n’est plus "
  "« combien j’ai » mais « combien j’ai, où, et disponible à la vente ou pas ». La marchandise en "
  "transit et la marchandise réservée ne sont pas du stock vendable : les confondre, c’est vendre "
  "ce qu’on n’a pas.",
  "/negoce/stocks-multi-depots/", "stocks multi-dépôts"),

 ("La traçabilité : ce qu’on vous demandera le jour du contrôle",
  "La question posée en contrôle est toujours la même — ce lot est parti où, et qu’est-ce qui "
  "est entré dedans. Si la réponse suppose de rouvrir des bons papier et deux classeurs, le "
  "périmètre du rappel s’élargit par précaution, et c’est ce qui coûte cher.",
  "/negoce/tracabilite-lots/", "traçabilité des lots"),

 ("Télévente : le devis qui devient commande sans ressaisie",
  "En négoce alimentaire, une grande part des commandes se prend au téléphone, vite, avec des "
  "prix qui bougent. Le point à regarder n’est pas l’écran de saisie mais ce qui se passe après : "
  "le devis devient-il une commande, puis un bon de livraison, puis une facture, sans que "
  "personne ne retape quoi que ce soit ?",
  "/negoce/ventes-devis-commandes/", "ventes, devis et commandes"),

 ("Grilles tarifaires et EDI : le test qui départage les outils",
  "Un client par grille, des remises par volume, des accords annuels, et pour la grande "
  "distribution des échanges normalisés. C’est le sujet sur lequel beaucoup d’outils "
  "généralistes s’arrêtent — et celui qu’il faut faire démontrer sur vos propres grilles.",
  "/negoce/tarifs-reporting-edi/", "tarifs, reporting et EDI"),
]

# LE lien editorial sortant du hub — un seul, vers la landing
SECTION_LANDING = (
 "Si vous importez : le calcul qui décide de votre marge",
 "C’est le point qui sépare un outil de négoce d’un outil qui tient l’import. Le prix payé au "
 "fournisseur n’est pas votre coût : il faut y répartir le fret, les droits de douane, "
 "l’assurance et l’écart de change, référence par référence, sur chaque conteneur. Tant que ce "
 "calcul se fait à côté, dans un tableur, la marge affichée est une estimation.",
 LANDING, "logiciel import export")

AUTOPORTANTES = [
 ("Les trois erreurs qui coûtent le plus cher",
  "<p><b>Choisir sur la démonstration plutôt que sur ses propres données.</b> Toute solution est "
  "convaincante sur un jeu de données préparé. Demandez la démonstration sur vos grilles "
  "tarifaires, vos lots et vos conteneurs réels.</p>"
  "<p><b>Sous-estimer la reprise de l’existant.</b> Le catalogue, les tarifs client et les "
  "encours doivent être repris. C’est là que les projets dérapent, pas sur les fonctionnalités.</p>"
  "<p><b>Prendre un généraliste en pensant l’adapter.</b> Le poids variable, les DLC et le "
  "multi-devises s’ajoutent par développement spécifique : coûteux à l’achat, et à refaire à "
  "chaque montée de version.</p>"),
 ("Combien de temps avant d’être opérationnel",
  "<p>Sur un périmètre de négoce alimentaire, comptez <b>4 à 8 semaines</b> entre le cadrage et "
  "la bascule, reprise des données comprise. Ce délai tient parce que les processus de la filière "
  "sont préconfigurés : il n’y a pas à modéliser le poids variable ni le multi-devises, ils sont "
  "déjà là.</p>"
  "<p>Le facteur qui allonge réellement un projet n’est presque jamais le logiciel : c’est la "
  "disponibilité des données de départ et la décision sur les cas particuliers de tarification.</p>"),
]

FAQ = [
 ("Un ERP de négoce alimentaire, est-ce différent d’un ERP de négoce classique ?",
  "Oui, sur trois points qui ne sont pas des options : le poids variable — la quantité facturée est celle pesée, pas celle commandée ; les DLC, qui imposent une rotation FEFO et des alertes ; et la traçabilité par lot d’origine, exigible en contrôle."),
 ("Faut-il un module d’import-export dès le départ ?",
  "Seulement si vous achetez hors zone euro ou hors UE. Le déclencheur n’est pas la taille de l’entreprise mais le premier conteneur payé en devises : à partir de là, le coût de revient ne peut plus se calculer de tête."),
 ("Comment savoir si l’outil gère vraiment mes grilles tarifaires ?",
  "En le faisant démontrer sur vos grilles, pas sur un exemple. Prenez votre client le plus complexe — celui qui cumule remise de volume, accord annuel et tarif dérogatoire — et demandez à voir la facture sortir juste."),
 ("Peut-on démarrer sur une partie du périmètre ?",
  "Oui, et c’est souvent le bon choix : démarrer sur les achats et les stocks, puis brancher la vente et la facturation une fois les données propres."),
 ("Que devient l’historique de l’ancien outil ?",
  "Le catalogue, les tarifs clients, les encours et l’historique des mouvements sont repris. Ce qui ne se reprend jamais proprement, ce sont les tableurs parallèles : c’est le moment de trancher ce qui fait foi."),
 ("Le logiciel fonctionne-t-il sur l’entrepôt, pas seulement au bureau ?",
  "Oui. Réception, pesée, préparation et inventaire se font sur terminal mobile, et l’information remonte immédiatement — c’est ce qui évite le double travail de ressaisie le soir."),
 ("Combien ça coûte ?",
  "Le tarif dépend du nombre d’utilisateurs et des modules retenus. Le point à comparer n’est pas la licence seule mais le coût complet sur trois ans, délai de mise en service et développements spécifiques inclus."),
]

CSS = """
<style id="hh-hub">
#hhub{--c:#0090c8;--c2:#00B1F5;--ink:#0f172a;--gr:#475569;--gl:#64748b;--bd:#e2e8f0;--bg:#f8fafc;
font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:var(--ink);line-height:1.65}
#hhub *{box-sizing:border-box}
#hhub .w{max-width:880px;margin:0 auto;padding:0 22px}
#hhub .wide{max-width:1080px}
#hhub section{padding:clamp(38px,5vw,64px) 0}
#hhub .alt{background:var(--bg)}
#hhub h1{font-size:clamp(1.8rem,3.8vw,2.7rem);line-height:1.15;font-weight:800;letter-spacing:-.02em;margin:.7rem 0 .8rem}
#hhub h2{font-size:clamp(1.3rem,2.6vw,1.75rem);line-height:1.25;font-weight:800;margin:0 0 .55rem;letter-spacing:-.01em}
#hhub .eyebrow{display:inline-block;background:#e0f2fe;color:var(--c);font-weight:700;font-size:.72rem;
letter-spacing:.07em;text-transform:uppercase;padding:.4rem .85rem;border-radius:999px}
#hhub .lead{font-size:1.12rem;color:var(--gr);margin:0 0 1.3rem}
#hhub p{color:var(--gr)}
/* sommaire — le hub annonce son plan */
#hhub .toc{background:#fff;border:1px solid var(--bd);border-radius:16px;padding:22px 24px;margin-top:1.5rem}
#hhub .toc h3{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--gl);margin:0 0 .8rem;font-weight:700}
#hhub .toc ol{margin:0;padding-left:1.25rem;color:var(--gr)}
#hhub .toc li{margin:0 0 .45rem}
#hhub .toc a{color:var(--ink);text-decoration:none;font-weight:600}
#hhub .toc a:hover{color:var(--c);text-decoration:underline}
/* section numerotee */
#hhub .sec{border-top:1px solid var(--bd);padding-top:30px;margin-top:30px}
#hhub .sec:first-of-type{border-top:none;margin-top:0;padding-top:0}
#hhub .num{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem;color:var(--c);font-weight:700;letter-spacing:.08em}
#hhub .go{display:inline-flex;align-items:center;gap:7px;margin-top:.85rem;color:var(--c);
font-weight:700;text-decoration:none;border-bottom:2px solid #cfeafa;padding-bottom:2px}
#hhub .go:hover{border-color:var(--c)}
/* la section landing — le seul lien editorial sortant */
#hhub .keysec{background:linear-gradient(135deg,#0090c8,#00B1F5);color:#fff;border-radius:22px;
padding:clamp(22px,3vw,36px);margin-top:30px;box-shadow:0 18px 44px rgba(0,120,180,.22)}
#hhub .keysec h2{color:#fff}
#hhub .keysec p{color:rgba(255,255,255,.95)}
#hhub .keysec .go{color:#fff;border-color:rgba(255,255,255,.5)}
#hhub details{background:#fff;border:1px solid var(--bd);border-radius:13px;padding:15px 18px;margin:0 0 9px}
#hhub summary{font-weight:700;cursor:pointer;list-style:none;color:var(--ink)}
#hhub summary::-webkit-details-marker{display:none}
#hhub summary:after{content:"+";float:right;color:var(--c);font-weight:800}
#hhub details[open] summary:after{content:"\\2013"}
#hhub .note{background:#fffbeb;border:1px solid #fde68a;color:#92400e;border-radius:12px;padding:14px 18px;font-size:.9rem;margin:0}
#hhub .btn{display:inline-flex;align-items:center;gap:9px;background:linear-gradient(135deg,var(--c),var(--c2));
color:#fff!important;font-weight:800;padding:14px 26px;border-radius:14px;text-decoration:none;margin-top:.6rem}
</style>
"""

def build():
    toc = "".join('<li><a href="#s%d">%s</a></li>' % (i + 1, t)
                  for i, (t, _b, _u, _a) in enumerate(SECTIONS))
    toc += '<li><a href="#s6">%s</a></li>' % SECTION_LANDING[0]
    toc += "".join('<li><a href="#s%d">%s</a></li>' % (i + 7, t)
                   for i, (t, _c) in enumerate(AUTOPORTANTES))

    secs = ""
    for i, (titre, corps, url, ancre) in enumerate(SECTIONS, 1):
        secs += ('<div class="sec" id="s%d"><span class="num">§ %d</span>'
                 '<h2>%s</h2><p>%s</p>'
                 '<a class="go" href="%s">%s →</a></div>') % (i, i, titre, corps, url, ancre)

    t, b, u, a = SECTION_LANDING
    keysec = ('<div class="keysec" id="s6"><span class="num" style="color:#cfeafa">§ 6</span>'
              '<h2>%s</h2><p>%s</p><a class="go" href="%s">%s →</a></div>') % (t, b, u, a)

    autos = ""
    for i, (titre, corps) in enumerate(AUTOPORTANTES, 7):
        autos += ('<div class="sec" id="s%d"><span class="num">§ %d</span>'
                  '<h2>%s</h2>%s</div>') % (i, i, titre, corps)

    faq = "".join('<details><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQ)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

    return (CSS +
        '<div id="hhub">'
        '<section class="w" style="padding-bottom:0">'
        '<p class="note"><b>Variante B — test A/B, brouillon non indexé.</b> '
        'La page est reconstruite en <b>hub</b> du modèle boost ⇄ landing : elle explique '
        '« comment choisir », arrose les 5 pages filles du silo, et ne fait qu’<b>un seul lien '
        'éditorial sortant</b>, vers la landing. Ne pas publier sans avoir posé le noindex.</p>'
        '</section>'
        '<section class="w" style="padding-top:22px">'
        '<span class="eyebrow">Guide de décision</span>'
        '<h1>Comment choisir son ERP de négoce alimentaire</h1>'
        '<p class="lead">Ce guide ne vend rien. Il pose les six questions qui départagent '
        'réellement les solutions du marché, dans l’ordre où elles se posent quand on remplace '
        'un tableur ou un outil vieillissant.</p>'
        '<div class="toc"><h3>Les huit points à trancher</h3><ol>' + toc + '</ol></div>'
        '</section>'
        '<section class="w">' + secs + keysec + autos + '</section>'
        '<section class="alt"><div class="w">'
        '<h2>Les questions qu’on nous pose</h2>'
        '<div style="margin-top:1.1rem">' + faq + '</div>'
        '</div></section>'
        '<section class="w" style="text-align:center">'
        '<h2>Vous préférez qu’on le regarde ensemble ?</h2>'
        '<p>30 minutes sur vos propres grilles tarifaires et vos propres lots, sans engagement.</p>'
        '<a class="btn" href="/contact/">Réserver ma démonstration →</a>'
        '</section>'
        '</div>'
        '<script type="application/ld+json">%s</script>') % json.dumps(ld, ensure_ascii=False)


def main():
    live = "--live" in sys.argv
    c = build()
    print("taille : %d caracteres (~%.1f Ko)" % (len(c), len(c) / 1024))
    # controle du modele
    import re
    filles = re.findall(r'href="(/negoce/[a-z-]+/)"', c)
    land = c.count('href="%s"' % LANDING)
    neutres = [a for a in re.findall(r'class="go" href="[^"]+">([^<]+) ', c)
               if a.lower() in ("en savoir plus", "voir la page", "découvrir", "cliquez ici")]
    print("pages filles arrosees : %d/5" % len(set(filles)))
    print("liens editoriaux vers la landing : %d (doit valoir 1)" % land)
    print("ancres neutres : %d (doit valoir 0)" % len(neutres))
    ex = w.api("pages?slug=%s&status=any&_fields=id,status" % SLUG)
    if ex:
        pid = ex[0]["id"]
        print("existe deja id=%s (%s)" % (pid, ex[0]["status"]))
        if live:
            w.update_content("pages", pid, c, live=True); print("mise a jour")
        return
    if not live:
        print("DRY-RUN — ajouter --live"); return
    r = w.api("pages", method="POST", data={
        "title": TITLE, "slug": SLUG, "status": "draft",
        "content": c, "template": "elementor_canvas"})
    print("CREEE id=%s statut=%s" % (r.get("id"), r.get("status")))


if __name__ == "__main__":
    main()
