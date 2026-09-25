# -*- coding: utf-8 -*-
"""DA editoriale de la variante A, reprise telle quelle de la page 11493.

Elle n'est pas modifiee : le test compare deux UX a fond identique, donc la
mise en forme de A doit rester exactement celle qui a ete construite.
"""

CSS = """<style id="hh-vA">
#hva{
 --ink:#10151C; --ink2:#3C4753; --ink3:#79838F;
 --paper:#FCFCFD; --wash:#F2F4F7; --rule:#DCE2E9;
 --acc:#0090C8; --acc-d:#00658C;
 --serif:'Instrument Serif',Georgia,serif;
 --sans:'IBM Plex Sans',system-ui,sans-serif;
 --mono:'IBM Plex Mono',ui-monospace,Menlo,monospace;
 font-family:var(--sans); color:var(--ink); background:var(--paper);
 font-size:17px; line-height:1.62; -webkit-font-smoothing:antialiased}
#hva *{box-sizing:border-box}
#hva .w{max-width:1200px;margin:0 auto;padding:0 32px}
#hva p{color:var(--ink2);margin:0 0 1rem}
#hva a{color:var(--acc-d);text-decoration:none;border-bottom:1px solid rgba(0,144,200,.34)}
#hva a:hover{border-bottom-color:var(--acc)}
#hva strong,#hva b{font-weight:600;color:var(--ink)}

/* --- gouttiere a numeros : la grille qui tient toute la page --- */
#hva .blk{display:grid;grid-template-columns:112px 1fr;gap:0;
 border-top:1px solid var(--rule);padding:clamp(46px,5.4vw,88px) 0}
#hva .gut{position:sticky;top:24px;align-self:start}
#hva .gut .no{font-family:var(--mono);font-size:.72rem;letter-spacing:.16em;color:var(--acc);
 font-weight:600;display:block;margin-bottom:14px}
#hva .gut .vert{font-family:var(--mono);font-size:.66rem;letter-spacing:.22em;
 text-transform:uppercase;color:var(--ink3);writing-mode:vertical-rl;transform:rotate(180deg)}
#hva .bd{min-width:0}

/* --- titres : serif, alignes a droite sur les grands blocs --- */
#hva h2{font-family:var(--serif);font-weight:400;font-size:clamp(2rem,4.4vw,3.4rem);
 line-height:1.04;letter-spacing:-.012em;color:var(--ink);margin:0 0 1.1rem;max-width:19ch}
#hva h2 em{font-style:italic;color:var(--acc-d)}
#hva h3{font-family:var(--sans);font-size:1.02rem;font-weight:600;margin:0 0 .35rem;
 letter-spacing:-.005em}
#hva .kick{font-family:var(--mono);font-size:.72rem;letter-spacing:.17em;text-transform:uppercase;
 color:var(--ink3);margin:0 0 1.5rem}
#hva .intro{font-size:1.14rem;color:var(--ink2);max-width:62ch}

/* --- HERO : tagline a gauche, titre a droite, bande image dessous --- */
#hva .hero{padding:clamp(40px,5vw,84px) 0 0}
#hva .hero .row{display:grid;grid-template-columns:112px 1fr;gap:0;align-items:start}
#hva .hero .lab{font-family:var(--mono);font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;
 color:var(--ink3);line-height:1.8;padding-top:.9rem}
#hva .hero h1{font-family:var(--serif);font-weight:400;font-size:clamp(2.5rem,6.6vw,5.1rem);
 line-height:.99;letter-spacing:-.02em;margin:0 0 1.3rem;max-width:15ch;color:var(--ink)}
#hva .hero h1 em{font-style:italic;color:var(--acc-d)}
#hva .hero .sub{font-size:1.16rem;max-width:56ch;color:var(--ink2)}
#hva .band{margin-top:clamp(34px,4.2vw,64px);height:clamp(240px,32vw,420px);overflow:hidden;
 border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
#hva .band img{width:100%;height:100%;object-fit:cover;display:block;filter:saturate(.92)}

/* --- bandeau de preuve en mono --- */
#hva .facts{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--rule)}
#hva .facts div{padding:22px 26px;border-right:1px solid var(--rule)}
#hva .facts div:last-child{border-right:none}
#hva .facts .n{font-family:var(--mono);font-size:1.42rem;font-weight:600;color:var(--ink);
 font-variant-numeric:tabular-nums;line-height:1}
#hva .facts .l{font-size:.83rem;color:var(--ink3);margin-top:7px;line-height:1.4}

/* --- le calcul : tableau technique, pas une carte --- */
#hva .calc{display:grid;grid-template-columns:1.02fr .98fr;gap:clamp(28px,4vw,60px);align-items:start}
#hva table.led{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:.9rem}
#hva table.led caption{font-family:var(--mono);font-size:.7rem;letter-spacing:.15em;
 text-transform:uppercase;color:var(--ink3);text-align:left;padding-bottom:12px}
#hva table.led td{padding:11px 0;border-bottom:1px solid var(--rule);color:var(--ink2)}
#hva table.led td:last-child{text-align:right;font-variant-numeric:tabular-nums;color:var(--ink);font-weight:500}
#hva table.led tr.sum td{border-top:2px solid var(--ink);border-bottom:none;padding-top:15px;
 color:var(--ink);font-weight:600;font-size:1.02rem}
#hva table.led tr.coef td{border-bottom:none;padding-top:3px;color:var(--acc-d);font-weight:600}
#hva .cap{font-family:var(--mono);font-size:.74rem;line-height:1.65;color:var(--ink3);margin-top:14px}

/* --- fonctions : liste numerotee a filets, PAS de cartes --- */
#hva .fx{border-top:1px solid var(--rule);margin-top:2rem}
#hva .fx .it{display:grid;grid-template-columns:56px 1fr;gap:0;
 padding:26px 0;border-bottom:1px solid var(--rule)}
#hva .fx .k{font-family:var(--mono);font-size:.78rem;color:var(--acc);font-weight:600;padding-top:.25rem}
#hva .fx p{margin:0;font-size:.98rem;color:var(--ink2);max-width:66ch}

/* --- triptyque plein cadre, angles droits --- */
#hva .trip{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--rule);
 border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-top:2rem}
#hva .trip figure{margin:0;background:var(--paper)}
#hva .trip img{width:100%;aspect-ratio:5/4;object-fit:cover;display:block;filter:saturate(.92)}
#hva .trip figcaption{padding:18px 22px;font-size:.92rem;color:var(--ink2);line-height:1.55}
#hva .trip .t{font-family:var(--mono);font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;
 color:var(--acc);display:block;margin-bottom:6px}

/* --- comparatif : grille technique --- */
#hva .cmpw{overflow-x:auto;margin-top:2rem;border-top:1px solid var(--ink)}
#hva table.cmp{width:100%;border-collapse:collapse;font-size:.94rem;min-width:660px}
#hva table.cmp th{text-align:left;padding:14px 18px 14px 0;font-family:var(--mono);font-size:.7rem;
 letter-spacing:.13em;text-transform:uppercase;color:var(--ink3);font-weight:500;
 border-bottom:1px solid var(--rule);vertical-align:bottom}
#hva table.cmp th:last-child{color:var(--acc)}
#hva table.cmp td{padding:13px 18px 13px 0;border-bottom:1px solid var(--rule);color:var(--ink2)}
#hva table.cmp td:first-child{color:var(--ink);font-weight:500;width:30%}
#hva table.cmp td:last-child{color:var(--ink);font-weight:500}
#hva table.cmp tr:hover td{background:var(--wash)}

/* --- index du silo --- */
#hva .idx{border-top:1px solid var(--rule);margin-top:2rem}
#hva .idx a{display:grid;grid-template-columns:56px 1fr auto;gap:0;align-items:baseline;
 padding:22px 0;border-bottom:1px solid var(--rule);border-bottom-color:var(--rule);
 color:var(--ink);transition:padding-left .18s ease}
#hva .idx a:hover{padding-left:10px;background:var(--wash)}
#hva .idx .k{font-family:var(--mono);font-size:.78rem;color:var(--acc);font-weight:600}
#hva .idx .t{font-size:1.06rem;font-weight:600}
#hva .idx .d{display:block;font-weight:400;font-size:.93rem;color:var(--ink3);margin-top:3px;max-width:56ch}
#hva .idx .ar{font-family:var(--mono);color:var(--acc);font-size:.9rem}

/* --- FAQ a filets --- */
#hva .qa{border-top:1px solid var(--rule);margin-top:2rem}
#hva details{border-bottom:1px solid var(--rule)}
#hva summary{list-style:none;cursor:pointer;padding:20px 0;font-weight:600;font-size:1.02rem;
 display:flex;justify-content:space-between;gap:22px;align-items:baseline}
#hva summary::-webkit-details-marker{display:none}
#hva summary:after{content:"+";font-family:var(--mono);color:var(--acc);font-weight:500;flex:0 0 auto}
#hva details[open] summary:after{content:"\2212"}
#hva details p{padding:0 0 22px;max-width:70ch;font-size:.98rem}

/* --- CTA plein cadre --- */
#hva .end{background:var(--ink);color:#fff;margin-top:0}
#hva .end .in{display:grid;grid-template-columns:1.1fr .9fr;align-items:center;gap:clamp(28px,4vw,58px);
 padding:clamp(48px,5.6vw,86px) 0}
#hva .end h2{color:#fff;margin-bottom:.9rem}
#hva .end p{color:rgba(255,255,255,.72);max-width:48ch}
#hva .end img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;filter:saturate(.9)}
#hva .cta{display:inline-block;font-family:var(--mono);font-size:.86rem;letter-spacing:.1em;
 text-transform:uppercase;font-weight:600;background:var(--acc);color:#fff!important;
 padding:17px 34px;border:none;margin-top:.7rem;transition:background .18s ease}
#hva .cta:hover{background:#00a6e6}
#hva .cta.line{background:transparent;color:var(--acc-d)!important;border:1px solid var(--rule);padding:15px 28px}
#hva .cta.line:hover{border-color:var(--acc);background:transparent}
#hva a.cta{border-bottom:none}
#hva .note{font-family:var(--mono);font-size:.76rem;background:var(--wash);
 border-left:2px solid var(--acc);padding:14px 18px;color:var(--ink2);margin:0}
#hva :focus-visible{outline:2px solid var(--acc);outline-offset:3px}
@media(prefers-reduced-motion:reduce){#hva *{transition:none!important}}
@media(max-width:940px){
 #hva .blk,#hva .hero .row{grid-template-columns:1fr}
 #hva .gut{position:static;display:flex;gap:14px;align-items:center;margin-bottom:18px}
 #hva .gut .vert{writing-mode:horizontal-tb;transform:none}
 #hva .gut .no{margin:0}
 #hva .hero .lab{padding-top:0;margin-bottom:1.1rem}
 #hva .calc,#hva .trip,#hva .end .in{grid-template-columns:1fr}
 #hva .facts{grid-template-columns:1fr 1fr}
 #hva .facts div:nth-child(2){border-right:none}
 #hva h2{max-width:none}
}
</style>"""
