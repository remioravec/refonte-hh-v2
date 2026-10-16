import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
import { writeFile } from 'node:fs/promises';
const { chromium } = pkg;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
await p.goto('http://127.0.0.1:8099/agroalimentaire/', { waitUntil: 'networkidle', timeout: 90000 });
const css = await p.evaluate(() => {
  const keep = (sel) => /\.ui(\b|-)/.test(sel || '');
  const out = [];
  const walk = (rules, cond) => {
    for (const r of rules) {
      if (r.type === 4 /* media */) {
        // on ne garde que les blocs qui s'appliquent a 1920 de large
        if (!window.matchMedia(r.conditionText).matches) continue;
        walk(r.cssRules, r.conditionText);
      } else if (r.selectorText && keep(r.selectorText)) {
        out.push(r.cssText);
      }
    }
  };
  for (const s of document.styleSheets) { try { walk(s.cssRules, null); } catch {} }
  return out.join('\n');
});
await writeFile('/home/user/refonte-hh-v2/videos/hello-harel-promo/assets/ui.css', css);
console.log('regles gardees :', css.split('\n').length, '|', css.length, 'o');
console.log('display:none restants :', (css.match(/display: none/g) || []).length);
await b.close();
