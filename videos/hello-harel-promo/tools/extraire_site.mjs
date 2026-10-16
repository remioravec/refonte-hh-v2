import pkg from '/opt/node22/lib/node_modules/playwright/index.js';
import { mkdir, writeFile } from 'node:fs/promises';
const { chromium } = pkg;
const OUT = '/home/user/refonte-hh-v2/videos/hello-harel-promo/capture';
const M = 'http://127.0.0.1:8099';
const PAGES = [
  ['/', 'accueil'],
  ['/negoce/', 'negoce'],
  ['/agroalimentaire/', 'agroalimentaire'],
  ['/fonctionnalites/tracabilite-alimentaire/', 'tracabilite'],
  ['/fonctionnalites/gestion-de-stock/', 'stock'],
  ['/fonctionnalites/import-export/', 'import-export'],
];

await mkdir(`${OUT}/extracted`, { recursive: true });
await mkdir(`${OUT}/assets`, { recursive: true });
await mkdir(`${OUT}/screenshots`, { recursive: true });
await mkdir(`${OUT}/dashboards`, { recursive: true });

const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1, locale: 'fr-FR' });

const tokens = { title: '', description: '', colors: [], fonts: [] };
const allText = [];
const dashboards = [];
const assets = new Map();

for (const [path, slug] of PAGES) {
  const p = await ctx.newPage();
  await p.goto(M + path, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {});
  await p.waitForTimeout(1500);

  if (slug === 'accueil') {
    tokens.title = await p.title();
    tokens.description = await p.$eval('meta[name="description"]', e => e.content).catch(() => '');
    // couleurs : variables CSS :root + couleurs effectivement peintes
    const css = await p.evaluate(() => {
      const vars = {};
      const rs = getComputedStyle(document.documentElement);
      for (const s of document.styleSheets) {
        try { for (const r of s.cssRules) {
          if (r.style) for (const n of r.style) if (n.startsWith('--')) vars[n] = rs.getPropertyValue(n).trim();
        } } catch {}
      }
      const fams = new Set();
      document.querySelectorAll('body,h1,h2,h3,p,a,button,span').forEach(e => {
        const f = getComputedStyle(e).fontFamily; if (f) fams.add(f);
      });
      return { vars, fonts: [...fams] };
    });
    tokens.fonts = [...new Set(css.fonts.flatMap(f => f.split(',').map(s => s.replace(/["']/g, '').trim())))]
      .filter(f => f && !/^(ui-|system-ui|-apple|BlinkMac|sans-serif|serif|monospace|Segoe|Roboto|Helvetica|Arial|Apple Color|Noto Color)/i.test(f));
    tokens.colors = [...new Set(Object.values(css.vars).filter(v => /^#[0-9a-f]{3,8}$/i.test(v)).map(v => v.toLowerCase()))];
    tokens._cssVars = css.vars;
  }

  const txt = await p.evaluate(() => document.body.innerText.replace(/\n{3,}/g, '\n\n'));
  allText.push(`\n\n===== ${path} =====\n${txt}`);

  // tableaux de bord : <figure class="ui">
  const figs = await p.evaluate(() => [...document.querySelectorAll('figure.ui')].map((f, i) => ({
    i, label: f.getAttribute('aria-label') || '', html: f.outerHTML,
    w: Math.round(f.getBoundingClientRect().width), h: Math.round(f.getBoundingClientRect().height),
  })));
  for (const f of figs) {
    if (dashboards.some(d => d.label === f.label)) continue;
    dashboards.push({ page: path, slug, ...f });
  }
  // capture image de chaque figure
  const els = await p.$$('figure.ui');
  for (let i = 0; i < els.length; i++) {
    const lab = figs[i]?.label || `fig${i}`;
    const name = `${slug}-ui-${i}-${lab.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 44)}.png`;
    await els[i].scrollIntoViewIfNeeded().catch(() => {});
    await p.waitForTimeout(250);
    await els[i].screenshot({ path: `${OUT}/screenshots/${name}` }).catch(() => {});
  }

  // CSS des tableaux de bord (une seule fois)
  if (slug === 'accueil' || dashboards.length) {
    const uiCss = await p.evaluate(() => {
      const out = [];
      for (const s of document.styleSheets) {
        try { for (const r of s.cssRules) {
          const t = r.cssText || '';
          if (/(^|[\s,>{])\.ui[-\s.,:{>]/.test(t) || /\.ui\b/.test(r.selectorText || '')) out.push(t);
        } } catch {}
      }
      return out.join('\n');
    });
    if (uiCss.length > 500) await writeFile(`${OUT}/dashboards/ui-${slug}.css`, uiCss);
  }

  // images
  const imgs = await p.evaluate(() => [...document.querySelectorAll('img')]
    .map(i => ({ src: i.currentSrc || i.src, alt: i.alt || '', w: i.naturalWidth, h: i.naturalHeight }))
    .filter(i => i.src && i.w > 60));
  for (const im of imgs) if (!assets.has(im.src)) assets.set(im.src, { ...im, page: path });

  if (slug === 'accueil') {
    await p.screenshot({ path: `${OUT}/screenshots/full-page.png`, fullPage: true }).catch(e => console.log('fullpage KO', e.message));
    await p.screenshot({ path: `${OUT}/screenshots/hero.png` });
  } else {
    await p.screenshot({ path: `${OUT}/screenshots/${slug}-hero.png` });
  }
  await p.close();
  console.log('ok', path, '| figures', figs.length, '| images', imgs.length);
}

// telechargement des images
const dl = await ctx.newPage();
let n = 0;
for (const [src, meta] of assets) {
  const local = src.replace(M, '');
  const ext = (local.split('?')[0].match(/\.(png|jpe?g|svg|webp|avif|gif)$/i) || ['.png'])[0];
  const name = `asset-${String(n).padStart(2, '0')}${ext}`;
  try {
    const r = await dl.request.get(src);
    if (r.ok()) { await writeFile(`${OUT}/assets/${name}`, await r.body()); meta.file = name; n++; }
  } catch {}
}
await dl.close();
await b.close();

await writeFile(`${OUT}/extracted/tokens.json`, JSON.stringify(tokens, null, 2));
await writeFile(`${OUT}/extracted/visible-text.txt`, allText.join(''));
await writeFile(`${OUT}/extracted/dashboards.json`, JSON.stringify(dashboards, null, 2));

const md = ['# Inventaire des assets — helloharel.com', '',
  `Relevé le ${new Date().toISOString().slice(0, 10)} sur le site réel (DOM live, miroir HTTP local du site de production).`, '',
  '## Tableaux de bord produit (HTML/CSS natifs, réutilisables tels quels)', '',
  `**${dashboards.length} tableaux de bord distincts** trouvés dans le site, construits en pur HTML/CSS`,
  '(`<figure class="ui">`), donc animables image par image sans capture d\'écran.', '',
  '| # | Tableau de bord | Page | Dimensions | Capture |', '|---|---|---|---|---|',
  ...dashboards.map((d, i) => `| ${i + 1} | ${d.label} | \`${d.page}\` | ${d.w}×${d.h} | \`screenshots/${d.slug}-ui-${d.i}-*.png\` |`),
  '', '## Images du site', '', '| Fichier | Alt | Dimensions | Page |', '|---|---|---|---|',
  ...[...assets.values()].filter(a => a.file).map(a => `| \`assets/${a.file}\` | ${(a.alt || '—').slice(0, 70)} | ${a.w}×${a.h} | \`${a.page}\` |`),
  '', '## Captures de page', '', '- `screenshots/full-page.png` — plaque pleine page de l\'accueil, 1920 de large',
  '- `screenshots/hero.png`, `screenshots/<page>-hero.png` — premier écran de chaque page',
].join('\n');
await writeFile(`${OUT}/extracted/asset-descriptions.md`, md);
console.log('\nTOKENS', JSON.stringify({ ...tokens, _cssVars: undefined }));
console.log('dashboards', dashboards.length, '| assets', n);
