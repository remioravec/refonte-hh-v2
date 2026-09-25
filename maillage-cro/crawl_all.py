import os,re,json,ssl,urllib.request,urllib.error,time
ctx=ssl.create_default_context();ctx.check_hostname=False;ctx.verify_mode=ssl.CERT_NONE
S="https://www.helloharel.com"
import base64
A=base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_PASS']}".encode()).decode()
def rest(ep):
    r=urllib.request.Request(f"{S}/wp-json/wp/v2/{ep}",headers={"Authorization":f"Basic {A}"})
    return json.loads(urllib.request.urlopen(r,timeout=60,context=ctx).read().decode())
def allitems(kind):
    out=[];pg=1
    while True:
        b=rest(f"{kind}?per_page=50&page={pg}&status=publish&_fields=id,slug,link")
        if not isinstance(b,list) or not b: break
        out+=b
        if len(b)<50: break
        pg+=1
    return out
pages=allitems("pages"); posts=allitems("posts")
items=[{"kind":"page",**p} for p in pages]+[{"kind":"post",**p} for p in posts]
def norm(h):
    h=h.strip()
    if h.startswith(S): h=h[len(S):] or "/"
    if h.startswith("http"): return None
    if not h.startswith("/"): return None
    return h.split("#")[0].split("?")[0]
# fetch each live, collect internal links (whole page)
def getp(u):
    r=urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(r,timeout=60,context=ctx) as x: return x.status,x.read().decode("utf-8","ignore")
    except urllib.error.HTTPError as e: return e.code,""
    except Exception as e: return 0,""
graph={}; srcof={}; allurls=set()
own={norm(i["link"]) for i in items}
for it in items:
    path=norm(it["link"])
    st,h=getp(S+path+"?cb=cr"+str(time.time()))
    links=set()
    for m in re.findall(r'href="([^"]+)"',h):
        n=norm(m)
        if n: links.add(n); srcof.setdefault(n,set()).add(path); allurls.add(n)
    graph[path]={"status":st,"out":sorted(links)}
    time.sleep(0.05)
# check every unique target
status={}
for u in sorted(allurls|own):
    st,_=getp(S+u)
    status[u]=st
json.dump({"items":[{"kind":i["kind"],"path":norm(i["link"]),"id":i["id"]} for i in items],
           "graph":graph,"status":status,
           "srcof":{k:sorted(v) for k,v in srcof.items()}},
          open("crawl.json","w"),ensure_ascii=False)
broken={u:s for u,s in status.items() if s>=400 or s==0}
print("pages crawled:",len(items),"| unique links:",len(allurls),"| broken:",len(broken))
for u,s in sorted(broken.items()):
    print(f"  {s}  {u}   <= {', '.join(srcof.get(u,[])[:4])}")
