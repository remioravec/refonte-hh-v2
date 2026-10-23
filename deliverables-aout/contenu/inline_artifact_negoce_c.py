"""Copie autonome de la variante C : images en data: URI pour l'apercu."""
import base64, os, re, subprocess
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad"
MIM = {".webp": "image/webp", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg"}
html = open("preview-negoce-c.html", encoding="utf-8").read()
os.makedirs(S + "/dl", exist_ok=True)
urls = sorted(set(re.findall(r'src="(https://www\.helloharel\.com[^"]+)"', html)))
for u in urls:
    nom = u.rsplit("/", 1)[1]; f = S + "/dl/" + nom
    if not os.path.exists(f) or os.path.getsize(f) < 500:
        subprocess.run(["curl", "-sk", "-A", "Mozilla/5.0", u, "-o", f], check=True)
    ext = os.path.splitext(nom)[1].lower()
    html = html.replace(u, "data:%s;base64,%s" % (MIM.get(ext, "image/jpeg"),
                        base64.b64encode(open(f, "rb").read()).decode()))
tete = ("<title>Négoce Variante C</title>\n"
        "<style>:root{color-scheme:light}body{margin:0;background:#fff}</style>\n")
open("artifact-negoce-c.html", "w", encoding="utf-8").write(tete + html)
print("artifact-negoce-c.html — %d ko, %d images incorporees"
      % (os.path.getsize("artifact-negoce-c.html") // 1024, len(urls)))
