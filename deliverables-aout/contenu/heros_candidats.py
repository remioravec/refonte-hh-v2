#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Candidats de photos de hero pour les pages metier — recherche et planches.

Critere de selection, dit clairement : on cherche des scenes de travail
REELLES, dans un decor europeen, aux codes du metier francais. Le geste doit
etre lisible — la farine sur le tablier, la main sur la balance, le lot sur le
carreau — et surtout pas une mise en scene de studio. On ne selectionne pas
les personnes sur leur couleur de peau ; on selectionne le decor, le geste et
la credibilite du lieu.

Format : paysage uniquement, au moins 1600 px de large, pour tenir dans un
hero 1920x1080 sans etre etire.

Licence : Pexels, libre d'utilisation commerciale, sans attribution
obligatoire. Le photographe est cite quand meme dans le livrable.

Etape 1 : ce script interroge Pexels et fabrique une planche contact par
metier, que l'on REGARDE avant de choisir. Rien n'est retenu automatiquement.

Usage :  python3 heros_candidats.py [metier ...]
"""

import json
import os
import subprocess
import sys
import urllib.parse

from PIL import Image, ImageDraw

CLE = "IFT3qGE8x9uADo91NDzk160HrBwSS5D2hjBIk2H6AsGJP0PmaRzz1iyp"
S = "/tmp/claude-0/-home-user-refonte-hh-v2/b317f75d-1f06-5053-a6cf-6b758c5a645c/scratchpad/heros2"

# metier -> (libelle, [requetes])
METIERS = {
 "agroalimentaire": ("Agroalimentaire (page mère)", [
    "food factory production line workers", "food processing plant employees",
    "food manufacturing workers hygiene", "industrial food production workers"]),
 "boulanger": ("Boulanger", [
    "professional bakery baker oven", "bakery production bread trays worker",
    "baker loading bread oven bakery", "artisan bakery workshop baker working"]),
 "brasseur": ("Brasseur", [
    "brewery worker stainless tanks", "craft brewery brewer working tanks",
    "brewery production hall", "brewer checking fermentation tank"]),
 "charcutier": ("Charcutier", [
    "butcher shop cutting meat professional", "charcuterie sausage production workshop",
    "butcher working meat counter", "meat curing sausages hanging workshop"]),
 "chocolatier": ("Chocolatier", [
    "chocolate workshop chocolatier working", "chocolate production tempering workshop",
    "chocolate maker moulds workshop", "chocolate factory worker"]),
 "conserverie": ("Conserverie", [
    "canning factory production line jars", "food preserving jars workshop worker",
    "cannery workers production", "glass jars food production line"]),
 "fromager": ("Fromager", [
    "cheese maker dairy working wheels", "cheese ripening cellar shelves",
    "cheese production workshop worker", "cheese shop counter seller"]),
 "glacier": ("Glacier", [
    "ice cream production workshop", "gelato artisan making workshop",
    "ice cream shop professional maker", "frozen dessert production"]),
 "industrie-laitiere": ("Industrie laitière", [
    "dairy processing plant worker", "milk factory production line",
    "dairy plant stainless tanks worker", "milk tank dairy industry"]),
 "maraicher": ("Fruits et légumes", [
    "wholesale market vegetables crates worker", "produce warehouse vegetables pallets",
    "vegetable sorting packing warehouse", "greengrocer market stall professional"]),
 "patissier": ("Pâtissier", [
    "pastry chef professional kitchen piping", "patisserie production pastry chef",
    "pastry kitchen chef trays", "pastry chef decorating professional"]),
 "plats-cuisines": ("Plats cuisinés", [
    "industrial kitchen meal production", "catering kitchen large pots cooking",
    "commercial kitchen workers cooking", "ready meals production line"]),
 "poissonnier": ("Poissonnier", [
    "fish market ice fishmonger", "fish wholesale market crates worker",
    "fishmonger cutting fish counter", "seafood market stall professional"]),
 "torrefacteur": ("Torréfacteur", [
    "coffee roasting machine roaster working", "coffee roastery worker beans",
    "coffee roasting drum professional", "coffee roaster checking beans"]),
 "traiteur": ("Traiteur", [
    "catering kitchen chef trays", "caterer plating dishes professional kitchen",
    "banquet kitchen chefs working", "catering buffet preparation kitchen"]),
 "viande": ("Viande", [
    "meat processing plant worker", "butcher cutting carcass workshop",
    "meat cutting room professional", "meat industry worker knife"]),
 "negoce": ("Négoce alimentaire", [
    "food wholesale warehouse crates worker", "warehouse worker pallets food",
    "wholesale food distribution warehouse", "forklift warehouse food crates"]),
}


def chercher(requete, n=12):
    u = ("https://api.pexels.com/v1/search?query=%s&per_page=%d&orientation=landscape"
         % (urllib.parse.quote(requete), n))
    r = subprocess.run(["curl", "-s", "-H", "Authorization: " + CLE, u],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get("photos", [])
    except Exception:
        return []


def vignette(pid, largeur=430):
    f = "%s/src/%d.jpg" % (S, pid)
    if not os.path.exists(f) or os.path.getsize(f) < 4000:
        subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0",
                        "https://images.pexels.com/photos/%d/pexels-photo-%d.jpeg"
                        "?auto=compress&cs=tinysrgb&w=900" % (pid, pid), "-o", f],
                       capture_output=True)
    try:
        im = Image.open(f).convert("RGB")
    except Exception:
        return None
    r = largeur / im.width
    return im.resize((largeur, round(im.height * r)), Image.LANCZOS)


def planche(cle):
    libelle, requetes = METIERS[cle]
    vus, retenus = set(), []
    for q in requetes:
        for p in chercher(q):
            if p["id"] in vus:
                continue
            if p["width"] < 1600:
                continue
            vus.add(p["id"])
            retenus.append(p)
    retenus = retenus[:15]
    cols, larg = 3, 430
    ims = []
    for p in retenus:
        im = vignette(p["id"], larg)
        if im:
            ims.append((p, im))
    if not ims:
        print("  aucun candidat pour", cle)
        return []
    h = max(i.height for _, i in ims)
    lignes = (len(ims) + cols - 1) // cols
    out = Image.new("RGB", (cols * larg, lignes * (h + 26)), "white")
    d = ImageDraw.Draw(out)
    for k, (p, im) in enumerate(ims):
        x, y = (k % cols) * larg, (k // cols) * (h + 26)
        d.text((x + 5, y + 6), "%d  %s" % (p["id"], p["photographer"][:34]), fill="black")
        out.paste(im, (x, y + 22))
    f = "%s/planches/%s.png" % (S, cle)
    out.save(f)
    json.dump([{"id": p["id"], "ph": p["photographer"], "url": p["url"],
                "w": p["width"], "h": p["height"], "alt": p.get("alt") or ""}
               for p, _ in ims], open("%s/planches/%s.json" % (S, cle), "w"),
              ensure_ascii=False, indent=1)
    print("  %-20s %2d candidats -> %s" % (cle, len(ims), f))
    return retenus


if __name__ == "__main__":
    cibles = sys.argv[1:] or list(METIERS)
    for c in cibles:
        if c in METIERS:
            planche(c)
