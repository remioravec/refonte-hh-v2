import { chromium } from 'playwright-core';
import fs from 'fs';
const EXE='/opt/pw-browsers/chromium-1223/chrome-linux64/chrome';
const SITE='https://www.helloharel.com';
const slugs = JSON.parse(fs.readFileSync('/tmp/shotaudit/slugs.json','utf8'));
const OUT='/tmp/shotaudit/shots'; fs.mkdirSync(OUT,{recursive:true});
const b = await chromium.launch({headless:true,executablePath:EXE,args:['--no-sandbox','--disable-dev-shm-usage']});
const ctx = await b.newContext({ignoreHTTPSErrors:true,viewport:{width:1280,height:1000},deviceScaleFactor:1});
const results=[];
let i=0;
for(const slug of slugs){
  i++;
  const url=`${SITE}/blog/${slug}/?cb=audit${Date.now()}${i}`;
  const r={slug,url};
  const page=await ctx.newPage();
  const errs=[];
  page.on('pageerror',e=>errs.push(String(e).slice(0,120)));
  try{
    const resp=await page.goto(url,{waitUntil:'load',timeout:60000});
    r.status=resp?resp.status():0;
    await page.waitForTimeout(1200);
    // Automated visual checks inside the page
    const checks=await page.evaluate(()=>{
      const q=s=>document.querySelector(s);
      const docW=document.documentElement.clientWidth;
      // horizontal overflow: any element wider than viewport within our template
      let overflow=[];
      const root=document.querySelector('.hha-tpl')||document.body;
      root.querySelectorAll('*').forEach(el=>{
        const r=el.getBoundingClientRect();
        if(r.width>docW+2 && r.right>docW+2){
          const tag=el.tagName.toLowerCase()+(el.className&&typeof el.className==='string'?'.'+el.className.split(' ')[0]:'');
          overflow.push(tag+':'+Math.round(r.width));
        }
      });
      const bodyScrollX = document.documentElement.scrollWidth>docW+2;
      const main=q('.hha-art');
      return {
        has_nav: !!q('.hha-nav'),
        has_menu_links: !!q('.hha-nav-links a'),
        has_hero: !!q('.hha-hero h1'),
        has_photo: !!(q('.hha-bio-av img')),
        has_toc: !!q('.hha-toc a'),
        has_cta: !!q('.hha-cta'),
        has_footer: !!q('.hha-foot'),
        has_article: !!main,
        article_chars: main?main.innerText.trim().length:0,
        h2_count: document.querySelectorAll('.hha-art h2').length,
        toc_count: document.querySelectorAll('.hha-toc a').length,
        img_count: document.querySelectorAll('.hha-art img').length,
        table_count: document.querySelectorAll('.hha-art table').length,
        page_overflow_x: bodyScrollX,
        overflow_elems: overflow.slice(0,6),
        stray_braces: (document.body.innerText.match(/\{\{|\}\}/g)||[]).length,
        raw_style_leak: document.body.innerText.includes('.hha-')||document.body.innerText.includes('px}'),
      };
    });
    r.checks=checks;
    r.jsErrors=errs.slice(0,4);
    await page.screenshot({path:`${OUT}/${String(i).padStart(2,'0')}_${slug}.png`,fullPage:true});
  }catch(e){ r.error=String(e).slice(0,160); r.jsErrors=errs.slice(0,4); }
  await page.close();
  // flag
  const c=r.checks||{};
  const issues=[];
  if(r.status!==200) issues.push('status '+r.status);
  if(c.page_overflow_x) issues.push('overflow-x');
  if((c.overflow_elems||[]).length) issues.push('wide:'+c.overflow_elems.join(','));
  if(!c.has_nav) issues.push('no-menu');
  if(!c.has_footer) issues.push('no-footer');
  if(!c.has_photo) issues.push('no-photo');
  if(!c.has_toc) issues.push('no-toc');
  if(!c.has_article||c.article_chars<400) issues.push('thin-article('+(c.article_chars||0)+')');
  if(c.toc_count && c.h2_count && Math.abs(c.toc_count-c.h2_count)>1) issues.push('toc!=h2('+c.toc_count+'/'+c.h2_count+')');
  if(c.stray_braces) issues.push('braces:'+c.stray_braces);
  if(c.raw_style_leak) issues.push('css-leak');
  if((r.jsErrors||[]).length) issues.push('jserr');
  r.issues=issues;
  results.push(r);
  console.log(`${i}/${slugs.length} ${slug} -> ${issues.length?('⚠ '+issues.join(' | ')):'OK'}`);
}
await b.close();
fs.writeFileSync('/tmp/shotaudit/report.json',JSON.stringify(results,null,1));
const bad=results.filter(r=>r.issues.length);
console.log(`\n=== ${results.length} articles, ${bad.length} with issues ===`);
