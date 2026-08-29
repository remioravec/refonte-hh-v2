# -*- coding: utf-8 -*-
"""DA Hello Harel portee par la variante B (page autonome, pas de wrapper #hh-page)."""

CSS = """<style id="hh-vB">
#hvb{
 --brand:#00B1F5; --brand-d:#0090C8; --brand-50:#EFF6FF; --brand-100:#DBEAFE;
 --ink:#0F172A; --ink2:#475569; --ink3:#64748B; --line:#E2E8F0; --wash:#F8FAFC;
 --go:#22C55E; --go-d:#16A34A;
 font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 color:var(--ink); background:#fff; font-size:16px; line-height:1.6;
 -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale;
 display:block; overflow-x:clip}
#hvb *,#hvb *::before,#hvb *::after{box-sizing:border-box}
#hvb h1,#hvb h2,#hvb h3,#hvb h4,#hvb p,#hvb ul,#hvb ol,#hvb li,#hvb figure,#hvb table{margin:0;padding:0}
#hvb ul,#hvb ol{list-style:none}
#hvb img{max-width:100%;height:auto;display:block}
#hvb a{color:inherit;text-decoration:none}
#hvb button{font:inherit;color:inherit}

#hvb .w{max-width:1200px;margin:0 auto;padding:0 24px}
#hvb .sec{padding:clamp(3.75rem,7.5vw,6.5rem) 0}
#hvb .sec.wash{background:var(--wash)}
#hvb .over{font-size:.6875rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--brand);margin-bottom:.75rem}
#hvb h2{font-size:clamp(1.85rem,3.9vw,2.7rem);font-weight:900;line-height:1.14;letter-spacing:-.022em;color:var(--ink)}
#hvb h3{font-size:1.0625rem;font-weight:700;letter-spacing:-.01em}
#hvb .lead{color:var(--ink2);font-size:1.0625rem;line-height:1.75;margin-top:.9rem;max-width:62ch}
#hvb .head{text-align:center;max-width:760px;margin:0 auto clamp(2.5rem,4vw,3.5rem)}
#hvb .head .lead{margin-left:auto;margin-right:auto}

/* ---- listes a coche ---- */
#hvb .ticks{display:flex;flex-direction:column;gap:.85rem;margin-top:1.6rem}
#hvb .tick{display:flex;gap:.7rem;align-items:flex-start}
#hvb .tick svg{flex:0 0 20px;width:20px;height:20px;margin-top:.15rem;color:var(--brand)}
#hvb .tick span{color:var(--ink2);font-size:1rem;line-height:1.6}
#hvb .tick b{color:var(--ink);font-weight:600}

/* ---- boutons ---- */
#hvb .btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
 font-weight:700;font-size:.9375rem;padding:.9rem 1.6rem;border-radius:999px;border:1.5px solid transparent;
 transition:transform .2s ease,box-shadow .2s ease,background .2s ease}
#hvb .btn-1{background:var(--go);color:#fff;box-shadow:0 6px 18px rgba(34,197,94,.28)}
#hvb .btn-1:hover{background:var(--go-d);transform:translateY(-1px)}
#hvb .btn-2{background:#fff;color:var(--ink);border-color:var(--line)}
#hvb .btn-2:hover{border-color:var(--ink);transform:translateY(-1px)}
#hvb .btn-3{background:transparent;color:var(--brand-d);border-color:rgba(0,177,245,.4)}
#hvb .btn-3:hover{background:var(--brand-50)}
#hvb .btns{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:2rem}
#hvb .more{display:inline-flex;align-items:center;gap:.4rem;color:var(--brand-d);font-weight:700;font-size:.9375rem;margin-top:1.6rem}
#hvb .more svg{width:16px;height:16px;transition:transform .3s ease}
#hvb .more:hover svg{transform:translateX(5px)}

/* ---- bandeau brouillon ---- */
#hvb .draft{background:#FEF3C7;border-bottom:1px solid #FDE68A;color:#92400E;
 font-size:.8125rem;font-weight:600;text-align:center;padding:.6rem 1rem}

/* ---- HERO ---- */
#hvb .hero{background:linear-gradient(180deg,#F8FAFC 0%,#fff 100%);padding:clamp(3rem,5.5vw,4.75rem) 0 clamp(3rem,5vw,4.5rem)}
#hvb .hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(2rem,4vw,3.5rem);align-items:center}
#hvb .pill{display:inline-flex;align-items:center;gap:.5rem;background:var(--brand-50);color:var(--brand-d);
 font-size:.75rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;padding:.45rem 1rem;border-radius:999px}
#hvb .pill i{width:7px;height:7px;border-radius:50%;background:var(--go);display:inline-block}
#hvb h1{font-size:clamp(2.2rem,4.8vw,3.5rem);font-weight:900;line-height:1.08;letter-spacing:-.03em;margin:1.1rem 0 0}
#hvb h1 em{font-style:normal;color:var(--brand-d)}
#hvb .reassure{display:flex;align-items:center;gap:.55rem;margin-top:1.1rem;color:var(--ink3);font-size:.875rem}
#hvb .reassure svg{width:18px;height:18px;color:var(--ink3);flex:0 0 18px}
#hvb .hero-media{border-radius:24px;overflow:hidden;box-shadow:0 24px 60px rgba(15,23,42,.18)}
#hvb .hero-media img{width:100%;aspect-ratio:4/3;object-fit:cover}

/* ---- PREUVE + MARQUEE ---- */
#hvb .proof{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:#fff;padding:2.5rem 0 2rem;overflow:hidden}
#hvb .proof-top{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:1rem 2rem;text-align:center;margin-bottom:1.75rem}
#hvb .proof-top p{font-size:1.0625rem;color:var(--ink2)}
#hvb .proof-top b{color:var(--ink);font-weight:800}
#hvb .rate{display:inline-flex;align-items:center;gap:.5rem;font-size:.875rem;font-weight:700;color:var(--ink)}
#hvb .rate .stars{color:#F59E0B;letter-spacing:.08em}
#hvb .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;max-width:900px;margin:0 auto 1.9rem}
#hvb .stat{background:var(--wash);border:1px solid var(--line);border-radius:18px;padding:1.05rem .9rem;text-align:center}
#hvb .stat b{display:block;font-size:1.5rem;font-weight:900;color:var(--brand);line-height:1.15;font-variant-numeric:tabular-nums}
#hvb .stat span{display:block;font-size:.6875rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--ink3);margin-top:.3rem;line-height:1.35}
#hvb .marq{position:relative;width:100%;overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
#hvb .marq-t{display:flex;width:max-content;align-items:center;gap:3rem;animation:hvb-marq 46s linear infinite}
#hvb .marq-t img{height:34px;width:auto;object-fit:contain;filter:grayscale(1);opacity:.62;transition:filter .3s ease,opacity .3s ease}
#hvb .marq:hover .marq-t img{filter:grayscale(0);opacity:1}
@keyframes hvb-marq{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

/* ---- ONGLETS ---- */
#hvb .tabbar{display:flex;flex-wrap:wrap;justify-content:center;gap:.5rem;margin-bottom:clamp(2rem,3.5vw,3rem)}
#hvb .tabbtn{display:inline-flex;align-items:center;gap:.55rem;background:#fff;border:1.5px solid var(--line);
 border-radius:999px;padding:.7rem 1.15rem;font-size:.9375rem;font-weight:700;color:var(--ink3);cursor:pointer;
 transition:border-color .25s ease,color .25s ease,background .25s ease}
#hvb .tabbtn svg{width:18px;height:18px}
#hvb .tabbtn:hover{color:var(--ink);border-color:#CBD5E1}
#hvb .tabbtn[aria-selected="true"]{background:var(--ink);border-color:var(--ink);color:#fff}
#hvb .tabpane{display:grid;grid-template-columns:.92fr 1.08fr;gap:clamp(2rem,4vw,3.5rem);align-items:center}
#hvb .tabpane[hidden]{display:none}
#hvb .tabpane .shot{border-radius:24px;overflow:hidden;border:1px solid var(--line);box-shadow:0 18px 48px rgba(15,23,42,.12)}
#hvb .tabpane .shot img{width:100%;aspect-ratio:16/11;object-fit:cover}

/* ---- CALCUL ---- */
#hvb .calc-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,4vw,3.5rem);align-items:start}
#hvb .card{background:#fff;border:1px solid var(--line);border-radius:24px;padding:1.75rem;box-shadow:0 12px 34px rgba(15,23,42,.06)}
#hvb .card-h{font-size:.6875rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--ink3);margin-bottom:1.1rem}
#hvb .lines{width:100%;border-collapse:collapse;font-size:.9375rem}
#hvb .lines td{padding:.62rem 0;border-bottom:1px solid var(--line);color:var(--ink2)}
#hvb .lines td:last-child{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;color:var(--ink);white-space:nowrap}
#hvb .lines tr.tot td{border-bottom:none;border-top:2px solid var(--ink);padding-top:.9rem;font-weight:800;color:var(--ink);font-size:1.0625rem}
#hvb .lines tr.coef td{border-bottom:none;padding-top:.2rem;color:var(--brand-d);font-weight:800}
#hvb .note{font-size:.8125rem;color:var(--ink3);line-height:1.6;margin-top:1rem}
#hvb .warn{background:var(--brand-50);border-left:4px solid var(--brand);border-radius:0 16px 16px 0;padding:1.25rem 1.4rem;margin-top:1.5rem}
#hvb .warn p{color:var(--ink2);font-size:1rem;line-height:1.7}
#hvb .warn p+p{margin-top:.75rem}
#hvb .warn b{color:var(--ink);font-weight:700}

/* ---- TERRAIN ---- */
#hvb .split{display:grid;grid-template-columns:1fr 1fr;gap:clamp(2rem,4vw,3.5rem);align-items:center}
#hvb .split .shot{border-radius:24px;overflow:hidden;box-shadow:0 18px 48px rgba(15,23,42,.14)}
#hvb .split .shot img{width:100%;aspect-ratio:4/3;object-fit:cover}

/* ---- COMPARATIF ---- */
#hvb .tw{overflow-x:auto;border:1px solid var(--line);border-radius:24px;background:#fff;-webkit-overflow-scrolling:touch}
#hvb table.cmp{width:100%;border-collapse:collapse;font-size:.9375rem;min-width:720px}
#hvb table.cmp th,#hvb table.cmp td{padding:.9rem 1.15rem;text-align:left;border-top:1px solid var(--line);color:var(--ink2);vertical-align:top;line-height:1.5}
#hvb table.cmp thead th{background:var(--wash);border-top:none;color:var(--ink);font-weight:800;font-size:.6875rem;text-transform:uppercase;letter-spacing:.07em}
#hvb table.cmp thead th:last-child{background:var(--brand-50);color:var(--brand-d)}
#hvb table.cmp tbody td:first-child{color:var(--ink);font-weight:600}
#hvb table.cmp tbody td:last-child{background:rgba(239,246,255,.55);color:var(--ink);font-weight:600}

/* ---- MODULES ---- */
#hvb .mods{display:grid;grid-template-columns:repeat(3,1fr);gap:1.15rem}
#hvb .mod{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:24px;
 overflow:hidden;transition:transform .3s cubic-bezier(.25,.46,.45,.94),box-shadow .3s ease}
#hvb .mod:hover{transform:translateY(-4px);box-shadow:0 20px 44px rgba(15,23,42,.12)}
#hvb .mod-img{position:relative;aspect-ratio:16/9;overflow:hidden}
#hvb .mod-img img{width:100%;height:100%;object-fit:cover}
#hvb .mod-no{position:absolute;top:.85rem;left:.85rem;background:rgba(15,23,42,.82);color:#fff;font-size:.6875rem;
 font-weight:800;letter-spacing:.08em;padding:.3rem .6rem;border-radius:8px;backdrop-filter:blur(4px)}
#hvb .mod-b{padding:1.3rem 1.35rem 1.45rem;display:flex;flex-direction:column;flex:1}
#hvb .mod-b p{color:var(--ink3);font-size:.9375rem;line-height:1.6;margin-top:.45rem;flex:1}
#hvb .mod-b .more{margin-top:1.1rem}

/* ---- CTA FINAL ---- */
#hvb .final{background:var(--ink);border-radius:32px;padding:clamp(2.5rem,5vw,4rem);text-align:center;color:#fff}
#hvb .final h2{color:#fff}
#hvb .final .lead{color:#CBD5E1;margin-left:auto;margin-right:auto}
#hvb .final .btns{justify-content:center}
#hvb .final .btn-2{background:transparent;color:#fff;border-color:rgba(255,255,255,.35)}
#hvb .final .btn-2:hover{border-color:#fff;background:rgba(255,255,255,.08)}

/* ---- FAQ ---- */
#hvb .faq{max-width:860px;margin:0 auto}
#hvb .qa{border-bottom:1px solid var(--line)}
#hvb .qa button{width:100%;display:flex;align-items:center;justify-content:space-between;gap:1.25rem;
 background:none;border:0;padding:1.3rem 0;text-align:left;cursor:pointer;font-size:1.0625rem;font-weight:700;color:var(--ink)}
#hvb .qa .ic{position:relative;flex:0 0 24px;width:24px;height:24px}
#hvb .qa .ic::before,#hvb .qa .ic::after{content:'';position:absolute;left:50%;top:50%;background:var(--brand);
 border-radius:2px;transform:translate(-50%,-50%);transition:transform .35s cubic-bezier(.25,.8,.25,1),opacity .35s ease}
#hvb .qa .ic::before{width:14px;height:2px}
#hvb .qa .ic::after{width:2px;height:14px}
#hvb .qa[data-open="1"] .ic::after{transform:translate(-50%,-50%) rotate(90deg);opacity:0}
#hvb .qa .ans{overflow:hidden;max-height:0;opacity:0;transition:max-height .4s cubic-bezier(.25,.8,.25,1),opacity .3s ease}
#hvb .qa[data-open="1"] .ans{max-height:620px;opacity:1}
#hvb .qa .ans p{color:var(--ink2);font-size:1rem;line-height:1.75;padding:0 3rem 1.4rem 0}

/* ---- animations ----
   Regle de securite : rien n'est masque par defaut. L'etat masque n'existe QUE
   sous .anim-on, classe posee par le script lui-meme. Sans JavaScript, avec un
   JavaScript en erreur ou sans IntersectionObserver, tout le contenu reste
   visible — c'est le defaut « scroll-reveal » deja rencontre sur ce site en
   07/2026, ou du contenu a opacity:0 n'etait jamais revele. */
#hvb.anim-on [data-anim="rise"]{opacity:0;transform:translateY(46px);
 transition:opacity .8s cubic-bezier(.25,.46,.45,.94),transform .8s cubic-bezier(.25,.46,.45,.94)}
#hvb.anim-on [data-anim="rise"].seen{opacity:1;transform:none}
#hvb [data-anim="words"] .wd{display:inline-block}
#hvb.anim-on [data-anim="words"] .wd{opacity:0;transform:translateY(14px);
 transition:opacity .5s cubic-bezier(.25,.46,.45,.94),transform .5s cubic-bezier(.25,.46,.45,.94)}
#hvb.anim-on [data-anim="words"].seen .wd{opacity:1;transform:none}

/* ---- responsive ---- */
@media(max-width:980px){
 #hvb .hero-grid,#hvb .tabpane,#hvb .calc-grid,#hvb .split{grid-template-columns:1fr}
 #hvb .split .shot{order:-1}
 #hvb .mods{grid-template-columns:repeat(2,1fr)}
 #hvb .stats{grid-template-columns:repeat(2,1fr)}
}
@media(max-width:640px){
 #hvb .mods{grid-template-columns:1fr}
 #hvb .tabbar{justify-content:flex-start;flex-wrap:nowrap;overflow-x:auto;padding-bottom:.4rem;
  margin-left:-24px;margin-right:-24px;padding-left:24px;padding-right:24px}
 #hvb .tabbtn{flex:0 0 auto}
 #hvb .btns .btn{width:100%}
 #hvb .qa .ans p{padding-right:0}
}
@media(prefers-reduced-motion:reduce){
 #hvb [data-anim],#hvb [data-anim="words"] .wd{opacity:1!important;transform:none!important;transition:none!important}
 #hvb .marq-t{animation:none}
}
</style>"""
