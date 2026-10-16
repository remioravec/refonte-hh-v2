import { chromium } from 'playwright-core';
import fs from 'fs';
const EXE='/opt/pw-browsers/chromium-1223/chrome-linux64/chrome';
const SITE='https://www.helloharel.com';
const slugs=JSON.parse(fs.readFileSync('/tmp/shotaudit/slugs.json','utf8'));
// pages to also audit (site-wide coherence)
const pages=['/','/agroalimentaire/','/fonctionnalites/','/negoce/','/comparatifs/','/tarifs/','/contact/','/blog/',
 '/agroalimentaire/traiteur/','/agroalimentaire/charcutier/','/fonctionnalites/gestion-de-stock/'];
const SHOTS='/tmp/shotaudit/full'; fs.mkdirSync(SHOTS+'/desk',{recursive:true}); fs.mkdirSync(SHOTS+'/mob',{recursive:true});
const b=await chromium.launch({headless:true,executablePath:EXE,args:['--no-sandbox','--disable-dev-shm-usage']});

// ---- link set: collect internal links from all article + page bodies, then HEAD-check uniques
const ctxD=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:1280,height:1000}});
const ctxM=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:390,height:844},isMobile:true});
const results=[]; const linkSet=new Set();
const targets=[...slugs.map(s=>['post',`/blog/${s}/`]), ...pages.map(p=>['page',p])];
let i=0;
for(const [kind,path] of targets){
  i++;
  const r={kind,path}; const url=SITE+path+'?cb=fa'+Date.now()+i;
  const pd=await ctxD.newPage(); const errs=[];
  pd.on('pageerror',e=>errs.push(String(e).slice(0,100)));
  try{
    const resp=await pd.goto(url,{waitUntil:'load',timeout:60000}); r.status=resp?resp.status():0;
    await pd.waitForTimeout(900);
    const d=await pd.evaluate(()=>{
      const dw=document.documentElement.clientWidth;
      const links=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'));
      const root=document.querySelector('#hh-page')||document.body;
      let wide=[];root.querySelectorAll('*').forEach(e=>{const b=e.getBoundingClientRect();if(b.right>dw+3&&b.width>dw+3)wide.push((e.className||e.tagName).toString().slice(0,30))});
      return {links, overflow:document.documentElement.scrollWidth>dw+3, wide:wide.slice(0,4),
        header:!!(document.querySelector('.site-header')||document.querySelector('header')),
        footer:!!(document.querySelector('footer'))};
    });
    r.overflow_d=d.overflow; r.wide_d=d.wide; r.header=d.header; r.footer=d.footer; r.jserr=errs.slice(0,3);
    (d.links||[]).forEach(h=>{ if(h && h.startsWith('/')) linkSet.add(h.split('#')[0]); });
    await pd.screenshot({path:`${SHOTS}/desk/${String(i).padStart(3,'0')}_${kind}_${path.replace(/\//g,'_')}.png`,fullPage:true});
  }catch(e){ r.error=String(e).slice(0,120); }
  await pd.close();
  // mobile
  const pm=await ctxM.newPage();
  try{
    await pm.goto(url,{waitUntil:'load',timeout:60000}); await pm.waitForTimeout(800);
    const m=await pm.evaluate(()=>({overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+3}));
    r.overflow_m=m.overflow;
    await pm.screenshot({path:`${SHOTS}/mob/${String(i).padStart(3,'0')}_${kind}_${path.replace(/\//g,'_')}.png`,fullPage:true});
  }catch(e){ r.error_m=String(e).slice(0,120); }
  await pm.close();
  const iss=[];
  if(r.status!==200) iss.push('status '+r.status);
  if(r.overflow_d) iss.push('overflow-desktop'+(r.wide_d&&r.wide_d.length?':'+r.wide_d.join(','):''));
  if(r.overflow_m) iss.push('overflow-mobile');
  if(!r.header) iss.push('no-header'); if(!r.footer) iss.push('no-footer');
  if((r.jserr||[]).length) iss.push('jserr:'+r.jserr[0]);
  r.issues=iss;
  results.push(r);
  console.log(`${i}/${targets.length} ${path} -> ${iss.length?'⚠ '+iss.join(' | '):'OK'}`);
}
// ---- link check
console.log('\nChecking '+linkSet.size+' unique internal links...');
const ctxL=await b.newContext({ignoreHTTPSErrors:true});
const broken=[]; let lc=0;
for(const path of linkSet){
  lc++;
  const pg=await ctxL.newPage();
  try{ const resp=await pg.goto(SITE+path,{waitUntil:'commit',timeout:30000}); const st=resp?resp.status():0;
    if(st>=400) broken.push({path,status:st}); }
  catch(e){ broken.push({path,status:'ERR'}); }
  await pg.close();
}
await b.close();
fs.writeFileSync('/tmp/shotaudit/fullreport.json',JSON.stringify({pages:results,brokenLinks:broken,checked:linkSet.size},null,1));
const bad=results.filter(r=>r.issues.length);
console.log(`\n=== PAGES: ${results.length}, with issues: ${bad.length} ===`);
console.log(`=== LINKS: ${linkSet.size} checked, broken: ${broken.length} ===`);
broken.slice(0,30).forEach(b=>console.log('  BROKEN',b.status,b.path));
