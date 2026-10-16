import { chromium } from 'playwright-core';
import fs from 'fs';
const EXE='/opt/pw-browsers/chromium-1223/chrome-linux64/chrome';
const SITE='https://www.helloharel.com';
const slugs=JSON.parse(fs.readFileSync('/tmp/shotaudit/slugs.json','utf8'));
const pages=['/','/agroalimentaire/','/fonctionnalites/','/negoce/','/comparatifs/','/tarifs/','/contact/','/blog/','/agroalimentaire/traiteur/','/agroalimentaire/charcutier/','/fonctionnalites/gestion-de-stock/'];
const b=await chromium.launch({headless:true,executablePath:EXE,args:['--no-sandbox','--disable-dev-shm-usage']});
const ctx=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:1280,height:1000}});
const linkSet=new Set(); const srcOf={};
const targets=[...slugs.map(s=>`/blog/${s}/`),...pages];
let i=0;
for(const path of targets){ i++;
  const p=await ctx.newPage();
  try{ await p.goto(SITE+path+'?cb=lc'+Date.now()+i,{waitUntil:'load',timeout:60000}); await p.waitForTimeout(700);
    const links=await p.evaluate(()=>[...document.querySelectorAll('#hh-page a[href], article a[href], .hha-art a[href]')].map(a=>a.getAttribute('href')));
    links.forEach(h=>{if(h&&h.startsWith('/')){const u=h.split('#')[0];linkSet.add(u);(srcOf[u]=srcOf[u]||new Set()).add(path);}});
  }catch(e){}
  await p.close();
}
const ctxL=await b.newContext({ignoreHTTPSErrors:true});
const broken=[];
for(const path of linkSet){ const pg=await ctxL.newPage();
  try{ const r=await pg.goto(SITE+path,{waitUntil:'commit',timeout:30000}); if((r?r.status():0)>=400) broken.push({path,status:r.status(),src:[...(srcOf[path]||[])].slice(0,3)});}
  catch(e){ broken.push({path,status:'ERR',src:[...(srcOf[path]||[])].slice(0,3)});}
  await pg.close();
}
await b.close();
fs.writeFileSync('/tmp/shotaudit/links.json',JSON.stringify({checked:linkSet.size,broken},null,1));
console.log('checked',linkSet.size,'broken',broken.length);
broken.forEach(x=>console.log('  ',x.status,x.path,'<=',x.src.join(', ')));
