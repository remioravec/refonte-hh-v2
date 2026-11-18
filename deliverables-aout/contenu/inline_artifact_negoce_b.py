#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fabrique la copie autonome de la variante B, images incorporees en data: URI.

Sert a la faire lire sans acces au back-office : le brouillon WordPress repond
404 en anonyme, et la politique de securite d'un artefact bloque les images
servies depuis un autre domaine. Le fichier produit est donc volumineux et
entierement reconstructible — il n'est pas versionne.

Usage :  python3 inline_artifact_negoce_b.py
Sortie :  artifact-negoce-b.html
"""

import base64
import os
import re
import subprocess
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(ICI, "preview-negoce-b.html")
SORTIE = os.path.join(ICI, "artifact-negoce-b.html")
CACHE = os.path.join(tempfile.gettempdir(), "hh-medias")

MIMES = {".webp": "image/webp", ".svg": "image/svg+xml",
         ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def main():
    html = open(SOURCE, encoding="utf-8").read()
    os.makedirs(CACHE, exist_ok=True)

    urls = sorted(set(re.findall(r'src="(https://www\.helloharel\.com[^"]+)"', html)))
    for u in urls:
        nom = u.rsplit("/", 1)[1]
        f = os.path.join(CACHE, nom)
        if not os.path.exists(f) or os.path.getsize(f) < 500:
            subprocess.run(["curl", "-sk", "-A", "Mozilla/5.0", u, "-o", f], check=True)
        ext = os.path.splitext(nom)[1].lower()
        html = html.replace(u, "data:%s;base64,%s"
                            % (MIMES.get(ext, "image/jpeg"),
                               base64.b64encode(open(f, "rb").read()).decode()))

    # La page porte deja toute sa direction artistique. On n'ajoute que son nom
    # et un fond explicite : identite de marque claire, theme unique assume.
    tete = ("<title>Négoce Variante B</title>\n"
            "<style>:root{color-scheme:light}body{margin:0;background:#fff}</style>\n")
    open(SORTIE, "w", encoding="utf-8").write(tete + html)
    print("%s — %d ko, %d images incorporees"
          % (os.path.basename(SORTIE), os.path.getsize(SORTIE) // 1024, len(urls)))


if __name__ == "__main__":
    main()
