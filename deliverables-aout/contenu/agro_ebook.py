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
#hh-page .hhg{background:linear-gradient(160deg,#04263a 0%,#07364f 52%,#052c41 100%);
 color:#e2f3fb;padding:5rem 0;position:relative;overflow:hidden}
#hh-page .hhg::before{content:"";position:absolute;inset:auto -12% -55% auto;width:640px;height:640px;
 border-radius:50%;background:radial-gradient(circle,rgba(0,177,245,.26),transparent 68%);pointer-events:none}
#hh-page .hhg-in{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);
 gap:3.5rem;align-items:center;position:relative}

/* --- la couverture, dessinee --- */
#hh-page .hhg-book{perspective:1400px;display:flex;justify-content:center}
#hh-page .hhg-cover{width:252px;aspect-ratio:3/4;border-radius:4px 12px 12px 4px;
 background:linear-gradient(135deg,#00B1F5 0%,#0079b8 58%,#005F88 100%);
 box-shadow:0 30px 60px -28px rgba(0,0,0,.85), inset 14px 0 24px -18px rgba(0,0,0,.6);
 transform:rotateY(-13deg) rotateX(3deg);padding:1.9rem 1.6rem;display:flex;
 flex-direction:column;justify-content:space-between;position:relative}
#hh-page .hhg-cover::after{content:"";position:absolute;left:0;top:0;bottom:0;width:11px;
 border-radius:4px 0 0 4px;background:linear-gradient(90deg,rgba(0,0,0,.42),transparent)}
#hh-page .hhg-cover span{font-size:.62rem;font-weight:700;letter-spacing:.2em;
 text-transform:uppercase;color:rgba(255,255,255,.82);margin:0 !important}
#hh-page .hhg-cover strong{font-size:1.5rem;line-height:1.2;color:#fff;font-weight:800;
 letter-spacing:-.022em;text-wrap:balance}
#hh-page .hhg-cover em{font-style:normal;font-size:.74rem;color:rgba(255,255,255,.9);
 display:flex;align-items:center;gap:.45rem;font-weight:600}
#hh-page .hhg-cover em::before{content:"";width:22px;height:2px;background:#16DB7F;flex:0 0 22px}

/* --- le sommaire --- */
#hh-page .hhg-txt>*{margin:0 !important}
#hh-page .hhg-kick{font-size:.74rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 color:#16DB7F;margin:0 0 .85rem !important}
#hh-page .hhg h2{font-size:clamp(1.7rem,3.4vw,2.5rem);line-height:1.14;color:#fff;
 font-weight:800;letter-spacing:-.025em;margin:0 0 1rem !important;text-wrap:balance}
#hh-page .hhg-chapo{color:#a9cee4;font-size:1.05rem;line-height:1.66;max-width:56ch;
 margin:0 0 2rem !important}
#hh-page .hhg-som{list-style:none;padding:0;margin:0 0 2.1rem !important;
 display:grid;gap:1px;background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.13);
 border-radius:14px;overflow:hidden}
#hh-page .hhg-som li{margin:0 !important;background:rgba(4,38,58,.72)}
#hh-page .hhg-som a{display:flex;align-items:center;gap:1rem;padding:.95rem 1.25rem;
 color:#d6ecf8;text-decoration:none;font-size:.97rem;line-height:1.45;transition:background .18s ease}
#hh-page .hhg-som a:hover,#hh-page .hhg-som a:focus-visible{background:rgba(0,177,245,.16);color:#fff}
#hh-page .hhg-som b{font-variant-numeric:tabular-nums;font-size:.76rem;font-weight:800;
 color:#16DB7F;flex:0 0 auto;letter-spacing:.04em}
#hh-page .hhg-som a>span{flex:1;min-width:0}
#hh-page .hhg-som a::after{content:"→";color:#5fa9cd;flex:0 0 auto;font-size:.95rem}
#hh-page .hhg-cta{display:inline-flex;align-items:center;gap:.6rem;background:#16DB7F;color:#04263a;
 font-weight:700;font-size:1rem;padding:.95rem 1.7rem;border-radius:999px;text-decoration:none;
 box-shadow:0 14px 30px -14px rgba(22,219,127,.8)}
#hh-page .hhg-cta:hover,#hh-page .hhg-cta:focus-visible{background:#0fc971;color:#04263a}
#hh-page .hhg-note{display:block;margin:.95rem 0 0 !important;font-size:.83rem;color:#7fb1cd}

@media(max-width:900px){
 #hh-page .hhg{padding:3.5rem 0}
 #hh-page .hhg-in{grid-template-columns:1fr;gap:2.4rem}
 #hh-page .hhg-cover{transform:none;width:208px}
}
</style>"""


def section():
    som = "".join(
        '<li><a href="%s"><b>%02d</b><span>%s</span></a></li>' % (u, k + 1, t)
        for k, (t, u) in enumerate(CHAPITRES))
    return (CSS + '<section class="hhg" id="guide-erp-agroalimentaire"><div class="container">'
            '<div class="hhg-in">'
            '<div class="hhg-book"><div class="hhg-cover" role="img" '
            'aria-label="Couverture du guide : comment choisir un ERP agroalimentaire">'
            '<span>Guide Hello Harel</span>'
            '<strong>Comment choisir un ERP agroalimentaire</strong>'
            '<em>5 chapitres · édition 2026</em></div></div>'
            '<div class="hhg-txt">'
            '<p class="hhg-kick">Le guide</p>'
            '<h2>Comment choisir un ERP agroalimentaire</h2>'
            '<p class="hhg-chapo">Cinq questions décident du choix, et aucune ne porte sur le '
            'nombre de fonctionnalités. Chaque chapitre répond à l\'une d\'elles, chiffres et '
            'sources à l\'appui, puis le comparatif par métier vous donne le classement.</p>'
            '<ul class="hhg-som">' + som + '</ul>'
            '<a class="hhg-cta" href="' + HUB + '">Ouvrir le comparatif par métier →</a>'
            '<span class="hhg-note">Lecture libre, sans formulaire. '
            'Comparatifs mis à jour en 2026.</span>'
            '</div></div></div></section>')
