import wp_common as w, csv, re, html, json, sys

csvdesc={}
for r in csv.DictReader(open('/home/user/refonte-hh-v2/deliverables-aout/technique/tableau-de-balisage-aout.csv',encoding='utf-8')):
    csvdesc[r['URL'].strip().replace("https://www.helloharel.com","")]=r['NOUVELLE description (≤985px)'].strip()

urls=[]
for line in open('/home/user/refonte-hh-v2/deliverables-aout/technique/T1-urls-affectees.txt',encoding='utf-8'):
    m=re.search(r'https://www\.helloharel\.com(/\S*)', line.strip())
    if m: urls.append(m.group(1))
urls=sorted(set(urls))

# bulk load
idx={}
for kind in ("pages","posts"):
    page=1
    while True:
        r=w.api(f"{kind}?per_page=100&page={page}&context=edit&_fields=id,slug,link,title,excerpt")
        if not r: break
        for it in r: idx[(it['slug'])]=(kind,it)
        if len(r)<100: break
        page+=1
print("indexed:",len(idx),flush=True)

def gen(title,path):
    t=html.unescape(re.sub(r'\s*[•|]\s*.*$','',title)).strip(); t=re.sub(r'\s*☁️','',t).strip()
    if '/negoce/' in path:
        s=f"{t} : stocks multi-dépôts, tarifs, télévente et marges pilotés par l'ERP négoce alimentaire Hello Harel."
    elif '/blog/' in path:
        s=f"{t} : guide pratique pour les PME agroalimentaires, par Hello Harel, éditeur d'ERP spécialisé."
    else:
        s=f"{t} : traçabilité par lot, coût de revient, poids variable et DLC pilotés par l'ERP agroalimentaire Hello Harel."
    return s[:154]

ok=[];skip=[];fail=[]
for p in urls:
    slug=[s for s in p.split('/') if s][-1]
    got=idx.get(slug)
    if not got: fail.append((p,"introuvable")); continue
    kind,it=got
    cur=(it.get('excerpt') or {}).get('raw','') or ''
    if cur.strip() and '{' not in cur: skip.append((p,"déjà propre")); continue
    title=html.unescape(it['title'].get('raw') or it['title'].get('rendered',''))
    desc=csvdesc.get(p) or gen(title,p)
    try:
        w.api(f"{kind}/{it['id']}", method="POST", data={"excerpt":desc}); ok.append(p)
    except Exception as e:
        fail.append((p,str(e)[:60]))
    print(f"{len(ok)+len(skip)+len(fail)}/{len(urls)}",flush=True)

json.dump({"ok":ok,"skip":skip,"fail":fail}, open('/home/user/refonte-hh-v2/deliverables-aout/technique/T1-excerpts-appliques.json','w'), ensure_ascii=False, indent=1)
print(f"\nDONE ok={len(ok)} skip={len(skip)} fail={len(fail)}")
for p,s in fail: print(" FAIL",p,s)
