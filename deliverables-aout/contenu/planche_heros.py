# -*- coding: utf-8 -*-
import base64, json, os

H = {e["url"]: e for e in json.load(open("heros.json"))}

FICHES = [
 ("/agroalimentaire/", 1726, "Agroalimentaire (page mère)"),
 ("/agroalimentaire/boulanger/", 3309, "Boulanger"),
 ("/agroalimentaire/brasseur/", 10896, "Brasseur"),
 ("/agroalimentaire/charcutier/", 2818, "Charcutier"),
 ("/agroalimentaire/chocolatier/", 10894, "Chocolatier"),
 ("/agroalimentaire/conserverie/", 10933, "Conserverie"),
 ("/agroalimentaire/fromager/", 10867, "Fromager"),
 ("/agroalimentaire/glacier/", 10895, "Glacier"),
 ("/agroalimentaire/industrie-laitiere/", 5470, "Industrie laitière"),
 ("/agroalimentaire/maraicher/", 2824, "Fruits et légumes"),
 ("/agroalimentaire/negoce-alimentaire/", 10934, "Négoce alimentaire"),
 ("/agroalimentaire/patissier/", 10865, "Pâtissier"),
 ("/agroalimentaire/plats-cuisines-industriels/", 5477, "Plats cuisinés"),
 ("/agroalimentaire/poissonnier/", 10868, "Poissonnier"),
 ("/agroalimentaire/torrefacteur/", 10935, "Torréfacteur"),
 ("/agroalimentaire/traiteur/", 2839, "Traiteur"),
 ("/agroalimentaire/viande/", 11332, "Viande"),
 ("/negoce/", 5957, "Négoce (page porteuse)"),
]

def data_uri(url):
    f = "mini/" + url.strip("/").replace("/", "-") + ".webp"
    return "data:image/webp;base64," + base64.b64encode(open(f, "rb").read()).decode()

cartes = []
for url, pid, metier in FICHES:
    fichier = H[url]["img"].split("/")[-1] if H[url]["img"] else "—"
    cartes.append(f'''<article class="frame">
 <a class="shot" href="https://www.helloharel.com{url}" target="_blank" rel="noopener">
  <img src="{data_uri(url)}" alt="Section hero de la page {metier}" loading="lazy" width="900">
 </a>
 <div class="meta">
  <h2>{metier}</h2>
  <p class="path">{url} <span class="sep">·</span> ID {pid}</p>
  <p class="file">{fichier}</p>
 </div>
</article>''')

HTML = f'''<title>Planche contact des heros métiers</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {{
  --pap:#EDEEEA; --surf:#FFFFFF; --enc:#161A17; --enc2:#4C544E; --enc3:#7E8781;
  --trait:#D3D7CF; --trait2:#BEC4BC; --slate:#41525E;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --pap:#15181A; --surf:#1D2124; --enc:#EAEEEB; --enc2:#A8B2AC; --enc3:#7A847E;
    --trait:#2C3236; --trait2:#3C444A; --slate:#9FB4C2;
  }}
}}
:root[data-theme="dark"] {{
  --pap:#15181A; --surf:#1D2124; --enc:#EAEEEB; --enc2:#A8B2AC; --enc3:#7A847E;
  --trait:#2C3236; --trait2:#3C444A; --slate:#9FB4C2;
}}
* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--pap); color:var(--enc);
  font-family:Archivo,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased;
}}
.wrap {{ max-width:1180px; margin:0 auto; padding-inline:20px; padding-block:44px 72px; }}

header {{ border-bottom:2px solid var(--enc); padding-bottom:20px; margin-bottom:34px; }}
.kicker {{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--enc3); margin:0 0 10px;
}}
h1 {{ font-size:clamp(28px,4.4vw,42px); font-weight:800; letter-spacing:-.022em; margin:0; text-wrap:balance; }}
.chapo {{ margin:14px 0 0; max-width:62ch; color:var(--enc2); }}

.planche {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(340px,1fr)); gap:34px 26px; }}
.shot {{ display:block; background:var(--trait); border:1px solid var(--trait2); line-height:0; }}
.shot img {{ width:100%; height:auto; display:block; }}
.shot:focus-visible {{ outline:2px solid var(--slate); outline-offset:2px; }}

.meta {{ margin-top:12px; }}
h2 {{ font-size:19px; font-weight:600; letter-spacing:-.012em; margin:0; }}
.path, .file {{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11.5px; color:var(--enc3);
  margin:6px 0 0; word-break:break-word;
}}
.file {{ margin-top:2px; opacity:.78; }}
.sep {{ opacity:.5; }}

footer {{ margin-top:56px; border-top:1px solid var(--trait2); padding-top:18px; color:var(--enc3); font-size:13.5px; max-width:70ch; }}
@media (max-width:600px) {{ .planche {{ grid-template-columns:1fr; }} }}
</style>

<div class="wrap">
<header>
  <p class="kicker">Hello Harel · relevé du 11 septembre 2026 · 18 pages</p>
  <h1>Planche contact des heros métiers</h1>
  <p class="chapo">La section hero de chaque page métier, telle qu'elle s'affiche en ligne, avec le nom du fichier réellement servi.</p>
</header>

<div class="planche">
{chr(10).join(cartes)}
</div>

<footer>
  <p>Captures prises sur les pages en ligne, largeur 1280 px, section <code>.hero-section</code> seule. Cliquer une vignette ouvre la page correspondante.</p>
</footer>
</div>
'''
open("planche-heros.html", "w", encoding="utf-8").write(HTML)
print("ecrit", os.path.getsize("planche-heros.html") // 1024, "ko")
