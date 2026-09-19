import csv, subprocess, concurrent.futures as cf
BASE='https://www.helloharel.com'
rows=list(csv.DictReader(open('redirections-import.csv')))
def test(r):
    src=r['source']; tgt=r['target']
    url=BASE+src
    out=subprocess.run(['curl','-s','-L','-o','/dev/null','-w','%{http_code}|%{num_redirects}|%{url_effective}',url],
                       capture_output=True,text=True,timeout=25).stdout
    code,nred,final=out.split('|',2)
    finalp=final.replace(BASE,'') or '/'
    lands_home = finalp.rstrip('/')=='' 
    intended_ok = finalp.rstrip('/')==tgt.rstrip('/')
    return (src,tgt,code,int(nred or 0),finalp,lands_home,intended_ok)
res=[]
with cf.ThreadPoolExecutor(max_workers=10) as ex:
    for r in ex.map(test, rows): res.append(r)
print('SRC | intended -> ACTUAL | code | hops | flag')
home=[r for r in res if r[5]]
wrong=[r for r in res if not r[6] and not r[5]]
dbl=[r for r in res if r[3]>=2]
ok=[r for r in res if r[6] and r[3]<2]
print('\n🔴 LAND ON HOMEPAGE ({}):'.format(len(home)))
for r in home: print('  ',r[0],'\n       intended',r[1],'| code',r[2],'| ACTUAL',r[4])
print('\n🟠 LAND ON WRONG PAGE (not intended, not home) ({}):'.format(len(wrong)))
for r in wrong: print('  ',r[0],'\n       intended',r[1],'| ACTUAL',r[4],'| code',r[2])
print('\n🟡 DOUBLE-HOP (>=2 redirects) ({}):'.format(len(dbl)))
for r in dbl: print('  ',r[0],'| hops',r[3],'| ->',r[4])
print('\n✅ OK ({}/{})'.format(len(ok),len(res)))
