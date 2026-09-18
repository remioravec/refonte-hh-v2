# -*- coding: utf-8 -*-
"""
Section « guide » de bas de page — la porte d'entree vers le hub comparatif.

Le bloc a l'allure d'un livre blanc : couverture, sommaire, bouton. Ce n'est
pas un PDF a telecharger — il n'en existe pas, et promettre un fichier qui
n'existe pas est le meilleur moyen de perdre le lecteur au clic. C'est un
parcours de lecture : chaque chapitre pointe une page reelle du site, et le
bouton ouvre le hub /comparatifs/.

La couverture est dessinee en CSS. Aucune image, donc rien a televerser,
rien a recadrer, et elle reste nette a toutes les densites.
"""

HUB = "/comparatifs/"


def en_data_uri(chemin):
    """La couverture voyage avec la page : aucune image distante dans un artefact."""
    import base64
    import os
    if not chemin or not os.path.exists(chemin):
        return None
    return "data:image/webp;base64," + base64.b64encode(open(chemin, "rb").read()).decode()

CHAPITRES = [
    ("Ce que coûte vraiment un ERP, au-delà des licences",
     "/blog/roi-erp/"),
    ("Cloud ou serveur : la question à trancher avant de comparer",
     "/blog/erp-cloud-saas-vs-on-premise/"),
    ("Traçabilité : le test qui élimine la moitié des candidats",
     "/blog/erp-tracabilite-agroalimentaire/"),
    ("Conformité : ce que l'éditeur doit être capable de prouver",
     "/blog/erp-conformite-agroalimentaire/"),
    ("Migrer sans arrêter la production",
     "/blog/migration-erp-agroalimentaire/"),
]

CSS = """<style id="hh-agro-guide">
#hh-page .hhg, .hhg{background:linear-gradient(160deg,#04263a 0%,#07364f 52%,#052c41 100%);
 color:#e2f3fb;padding:5rem 0;position:relative;overflow:hidden}
#hh-page .hhg::before, .hhg::before{content:"";position:absolute;inset:auto -12% -55% auto;width:640px;height:640px;
 border-radius:50%;background:radial-gradient(circle,rgba(0,177,245,.26),transparent 68%);pointer-events:none}
#hh-page .hhg-in, .hhg-in{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);
 gap:3.5rem;align-items:center;position:relative}

/* --- la couverture --- */
/* Elle porte une photo du metier, pas un aplat : c'est ce que le lecteur
   reconnait avant de lire le titre. Le voile sombre monte du bas pour que le
   titre reste lisible quelle que soit la photo. */
#hh-page .hhg-book, .hhg-book{perspective:1500px;display:flex;justify-content:center}
#hh-page .hhg-cover, .hhg-cover{position:relative;width:264px;aspect-ratio:3/4;
 border-radius:3px 10px 10px 3px;overflow:hidden;isolation:isolate;
 transform:rotateY(-13deg) rotateX(2.5deg);
 box-shadow:0 34px 64px -26px rgba(0,0,0,.9), 0 2px 0 rgba(255,255,255,.08) inset;
 display:flex;flex-direction:column;justify-content:space-between;
 padding:1.45rem 1.35rem 1.6rem;background:#04263a}
#hh-page .hhg-cover .ph, .hhg-cover .ph{position:absolute;inset:0;z-index:-2;
 background-size:cover;background-position:center;filter:saturate(.82)}
#hh-page .hhg-cover .vo, .hhg-cover .vo{position:absolute;inset:0;z-index:-1;
 background:linear-gradient(178deg,rgba(4,38,58,.34) 0%,rgba(4,38,58,.52) 38%,
 rgba(3,30,46,.93) 74%,rgba(3,26,40,.98) 100%)}
/* la tranche : un filet sombre a gauche, puis le rappel vert de la marque */
#hh-page .hhg-cover::after, .hhg-cover::after{content:"";position:absolute;left:0;top:0;bottom:0;
 width:13px;background:linear-gradient(90deg,rgba(0,0,0,.55),rgba(0,0,0,.06))}
#hh-page .hhg-cover::before, .hhg-cover::before{content:"";position:absolute;left:13px;top:0;bottom:0;
 width:2px;background:#16DB7F;opacity:.9}
#hh-page .hhg-cover .kick, .hhg-cover .kick{display:flex;align-items:center;gap:.5rem;
 font-size:.58rem;font-weight:800;letter-spacing:.22em;text-transform:uppercase;
 color:rgba(255,255,255,.9);margin:0 0 0 .35rem !important}
#hh-page .hhg-cover .kick::before, .hhg-cover .kick::before{content:"";width:16px;height:2px;
 background:#16DB7F;flex:0 0 16px}
#hh-page .hhg-cover .bas, .hhg-cover .bas{margin:0 0 0 .35rem !important}
#hh-page .hhg-cover strong, .hhg-cover strong{display:block;font-size:1.42rem;line-height:1.1;
 color:#fff;font-weight:800;letter-spacing:-.028em;text-wrap:balance;
 text-shadow:0 2px 14px rgba(0,0,0,.5)}
#hh-page .hhg-cover hr, .hhg-cover hr{border:0;height:2px;width:34px;background:#16DB7F;
 margin:.75rem 0 .6rem !important}
#hh-page .hhg-cover em, .hhg-cover em{font-style:normal;display:block;font-size:.68rem;
 font-weight:600;letter-spacing:.03em;color:rgba(255,255,255,.82)}

/* --- le sommaire --- */
#hh-page .hhg-txt>*, .hhg-txt>*{margin:0 !important}
#hh-page .hhg-kick, .hhg-kick{font-size:.74rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:#16DB7F;margin:0 0 .85rem !important}
#hh-page .hhg h2, .hhg h2{font-size:clamp(1.7rem,3.4vw,2.5rem);line-height:1.14;color:#fff;
 font-weight:800;letter-spacing:-.025em;margin:0 0 1rem !important;text-wrap:balance}
#hh-page .hhg-chapo, .hhg-chapo{color:#a9cee4;font-size:1.05rem;line-height:1.66;max-width:56ch;
 margin:0 0 2rem !important}
#hh-page .hhg-som, .hhg-som{list-style:none;padding:0;margin:0 0 2.1rem !important;
 display:grid;gap:1px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.13);
 border-radius:14px;overflow:hidden}
#hh-page .hhg-som li, .hhg-som li{margin:0 !important;background:rgba(4,38,58,.72)}
#hh-page .hhg-som a, .hhg-som a{display:flex;align-items:center;gap:1rem;padding:.95rem 1.25rem;
 min-height:48px;box-sizing:border-box;
 color:#d6ecf8 !important;text-decoration:none;font-size:.97rem;line-height:1.45;
 transition:background .18s ease}
#hh-page .hhg-som a:hover, .hhg-som a:hover, #hh-page .hhg-som a:focus-visible, .hhg-som a:focus-visible{background:rgba(0,177,245,.16);color:#fff}
#hh-page .hhg-som b, .hhg-som b{font-variant-numeric:tabular-nums;font-size:.76rem;font-weight:800;
 color:#16DB7F;flex:0 0 auto;letter-spacing:.04em}
#hh-page .hhg-som a>span, .hhg-som a>span{flex:1;min-width:0}
#hh-page .hhg-som a::after, .hhg-som a::after{content:"→";color:#5fa9cd;flex:0 0 auto;font-size:.95rem}
#hh-page .hhg-cta, .hhg-cta{display:inline-flex;align-items:center;gap:.6rem;
 background:#16DB7F !important;color:#04263a !important;
 font-weight:700;font-size:1rem;padding:.95rem 1.7rem;border-radius:999px;text-decoration:none;
 box-shadow:0 14px 30px -14px rgba(22,219,127,.8)}
#hh-page .hhg-cta:hover, .hhg-cta:hover, #hh-page .hhg-cta:focus-visible, .hhg-cta:focus-visible{
 background:#0fc971 !important;color:#04263a !important}
#hh-page .hhg-note, .hhg-note{display:block;margin:.95rem 0 0 !important;font-size:.83rem;color:#7fb1cd}

/* Le bloc peut vivre HORS de #hh-page — c'est le cas juste avant le pied de
   page. Il n'herite alors ni de la police du site, ni de la largeur utile de
   son conteneur, qui deborde de 32 px. Les deux se reposent ici. */
.hhg{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.hhg>.container{width:100%;max-width:1440px;margin-inline:auto;
 padding-inline:24px;box-sizing:border-box}

@media(max-width:900px){
 #hh-page .hhg, .hhg{padding:3.5rem 0}
 #hh-page .hhg-in, .hhg-in{grid-template-columns:1fr;gap:2.4rem}
 #hh-page .hhg-cover, .hhg-cover{transform:none;width:208px}
}
</style>"""


def section(titre="Comment choisir un ERP agroalimentaire", chapitres=None, hub=HUB,
            chapo=None, couverture=None, cadrage="center"):
    """cadrage : le point de la photo qu'on garde une fois recadree en 3/4.

    Une photo de metier est presque toujours en paysage, la couverture est en
    portrait : la recadrer au centre coupe les visages. Le cadrage se choisit
    donc a l'oeil, sur le rendu, pas au jugé.
    """
    chapitres = chapitres or CHAPITRES
    som = "".join(
        '<li><a href="%s"><b>%02d</b><span>%s</span></a></li>' % (u, k + 1, t)
        for k, (t, u) in enumerate(chapitres))
    return (CSS + '<section class="hhg" id="guide-erp-agroalimentaire"><div class="container">'
            '<div class="hhg-in">'
            '<div class="hhg-book"><div class="hhg-cover" role="img" '
            'aria-label="Couverture du guide : ' + titre.lower() + '">'
            + ('<span class="ph" style="background-image:url(%s);background-position:%s">'
               '</span>' % (couverture, cadrage) if couverture else '')
            + '<span class="vo"></span>'
            '<span class="kick">Guide Hello Harel</span>'
            '<span class="bas"><strong>' + titre + '</strong><hr>'
            '<em>%d chapitres · édition 2026</em></span></div></div>' % len(chapitres) +
            '<div class="hhg-txt">'
            '<p class="hhg-kick">Le guide</p>'
            '<h2>' + titre + '</h2>'
            '<p class="hhg-chapo">' + (chapo or
              "Cinq questions décident du choix, et aucune ne porte sur le nombre de "
              "fonctionnalités. Chaque chapitre répond à l'une d'elles, chiffres et "
              "sources à l'appui, puis le comparatif par métier vous donne le "
              "classement.") + '</p>'
            '<ul class="hhg-som">' + som + '</ul>'
            '<a class="hhg-cta" href="' + hub + '">Ouvrir le comparatif par métier →</a>'
            '<span class="hhg-note">Lecture libre, sans formulaire. '
            'Comparatifs mis à jour en 2026.</span>'
            '</div></div></div></section>')
