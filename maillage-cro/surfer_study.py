"""Reasonable-surfer PageRank + internal mesh study from crawl.json."""
import json,re,collections
d=json.load(open('crawl.json'))
items={i['path']:i for i in d['items']}
graph=d['graph']; status=d['status']
own=set(items)  # indexable own URLs (published pages+posts)

# Keep only internal links to OWN published URLs that are 200 (a real surfer
# won't follow 404s/system endpoints).
def ok(u): return u in own and status.get(u,0)==200
# Reasonable surfer: weight links by zone. We approximate from live HTML zones:
#  - boilerplate (header/footer/nav) links get low weight, contextual high.
# We don't have per-link zone here, so use: links present on MANY pages == boilerplate.
linkfreq=collections.Counter()
for p,info in graph.items():
    for u in info['out']:
        if ok(u): linkfreq[u]+=1
N=len(own)
# A link appearing on >50% of pages is boilerplate (menu/footer).
boiler_thresh=0.5*N
edges=collections.defaultdict(list)  # src -> [(dst,weight)]
for p,info in graph.items():
    if p not in own: continue
    for u in info['out']:
        if not ok(u) or u==p: continue
        w=0.3 if linkfreq[u]>boiler_thresh else 1.0  # reasonable-surfer weighting
        edges[p].append((u,w))

# Weighted PageRank
damp=0.85
PR={u:1.0/N for u in own}
for _ in range(60):
    newPR={u:(1-damp)/N for u in own}
    dangling=0.0
    for u in own:
        outs=edges.get(u,[])
        tot=sum(w for _,w in outs)
        if tot==0: dangling+=PR[u]; continue
        for v,w in outs:
            newPR[v]+=damp*PR[u]*(w/tot)
    # distribute dangling evenly
    for u in own: newPR[u]+=damp*dangling/N
    PR=newPR
s=sum(PR.values()); PR={k:v/s for k,v in PR.items()}

# Inbound contextual (non-boilerplate) link counts
inbound=collections.Counter(); inbound_ctx=collections.Counter()
for p,outs in edges.items():
    for v,w in outs:
        inbound[v]+=1
        if w>=1.0: inbound_ctx[v]+=1

posts=[u for u in own if items[u]['kind']=='post']
pages=[u for u in own if items[u]['kind']=='page']
orphans=[u for u in own if inbound_ctx[u]==0]
deadend=[u for u in own if sum(1 for v,w in edges.get(u,[]) if w>=1.0)==0]  # no ctx out

rank=sorted(own,key=lambda u:-PR[u])
out={
 "n":N,"posts":len(posts),"pages":len(pages),
 "top_pr":[(u,round(PR[u]*1000,2)) for u in rank[:15]],
 "bottom_pr":[(u,round(PR[u]*1000,3)) for u in rank[-15:]],
 "orphans_ctx":sorted(orphans),
 "deadends_ctx":sorted(deadend),
 "money_pr":{u:round(PR[u]*1000,2) for u in ['/agroalimentaire/','/fonctionnalites/','/negoce/','/comparatifs/','/contact/','/tarifs/','/fonctionnalites/gestion-de-stock/','/fonctionnalites/fabrication/','/agroalimentaire/traiteur/','/agroalimentaire/charcutier/'] if u in PR},
}
json.dump({"PR":{k:PR[k] for k in own},"inbound_ctx":dict(inbound_ctx),
           "edges":{k:[[v,w] for v,w in vs] for k,vs in edges.items()},
           "summary":out},open('surfer.json','w'),ensure_ascii=False,indent=1)
print("=== SURFER-RAISONNABLE STUDY ===")
print(f"indexable URLs: {N} ({len(pages)} pages, {len(posts)} posts)")
print(f"orphans (0 contextual inbound): {len(orphans)}")
for u in orphans[:40]: print("   ORPHAN",u)
print(f"dead-ends (0 contextual outbound): {len(deadend)}")
for u in deadend[:20]: print("   DEADEND",u)
print("\nTop PR:")
for u,v in out['top_pr']: print(f"   {v:7.2f}  {u}")
print("\nMoney pages PR:")
for u,v in out['money_pr'].items(): print(f"   {v:7.2f}  {u}")
