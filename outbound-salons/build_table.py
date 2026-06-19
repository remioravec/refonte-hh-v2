#!/usr/bin/env python3
"""
Generate ONE self-contained HTML file (no API, no CDN) showing the full outbound
database. Reads every *-exposants.csv in this folder, merges + dedupes, embeds
the data as JSON inside the page, and renders an interactive table (search,
filters salon/ICP/type email, tri colonnes, pagination, export CSV).

Single deliverable file: base-outbound.html  (regenerate after each salon lot)

Run: python3 build_table.py
"""
import csv, glob, json, html, datetime

COLS = ["salon", "edition_annee", "entreprise", "secteur_metier", "site_web", "email",
        "type_email", "nom_contact", "fonction", "ville", "departement", "telephone",
        "source_url", "date_collecte", "statut_validation", "segment_ICP"]


def load():
    rows, seen = [], set()
    for f in sorted(glob.glob("*-exposants.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8"), delimiter=";"):
            k = (r.get("entreprise", "").lower().strip(), r.get("email", "").lower().strip())
            if k in seen:
                continue
            seen.add(k)
            rows.append({c: r.get(c, "") for c in COLS})
    return rows


def main():
    rows = load()
    salons = sorted({r["salon"] for r in rows if r["salon"]})
    n_email = sum(1 for r in rows if r["email"])
    n_gen = sum(1 for r in rows if r["type_email"] == "generique")
    n_hi = sum(1 for r in rows if r["segment_ICP"] == "Haute")
    data_json = json.dumps(rows, ensure_ascii=False)
    stats = {"total": len(rows), "email": n_email, "gen": n_gen, "hi": n_hi,
             "salons": len(salons)}
    page = TEMPLATE.replace("__DATA__", data_json) \
                   .replace("__STATS__", json.dumps(stats, ensure_ascii=False)) \
                   .replace("__DATE__", datetime.date.today().isoformat()) \
                   .replace("__SALONS__", str(len(salons)))
    open("base-outbound.html", "w", encoding="utf-8").write(page)
    print(f"WROTE base-outbound.html | {len(rows)} exposants | {n_email} emails | "
          f"{n_gen} génériques | {n_hi} ICP Haute | {len(salons)} salon(s)")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Base Outbound — Salons Agroalimentaire · Hello Harel</title>
<style>
  :root{--green:#16a34a;--green-d:#15803d;--ink:#0f172a;--muted:#64748b;--bg:#f8fafc;
        --line:#e2e8f0;--card:#fff;--chip:#ecfdf5;--chipink:#166534;}
  *{box-sizing:border-box}
  body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       color:var(--ink);background:var(--bg);font-size:14px}
  header{background:linear-gradient(120deg,#0f172a,#15803d);color:#fff;padding:22px 26px}
  header h1{margin:0;font-size:1.25rem;font-weight:700}
  header p{margin:4px 0 0;color:#cbd5e1;font-size:.85rem}
  .wrap{padding:18px 26px 60px}
  .cards{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}
  .card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 18px;min-width:130px;flex:1}
  .card .v{font-size:1.5rem;font-weight:800;color:var(--green-d)}
  .card .l{color:var(--muted);font-size:.78rem;margin-top:2px}
  .toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
  input[type=search],select{padding:9px 12px;border:1px solid var(--line);border-radius:9px;font-size:.9rem;background:#fff}
  input[type=search]{flex:1;min-width:220px}
  .btn{background:var(--green);color:#fff;border:0;padding:9px 14px;border-radius:9px;font-weight:600;cursor:pointer;font-size:.9rem}
  .btn:hover{background:var(--green-d)}
  .count{color:var(--muted);font-size:.82rem;margin-left:auto}
  .tablewrap{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:auto}
  table{border-collapse:collapse;width:100%;min-width:1000px}
  th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
  th{background:#f1f5f9;position:sticky;top:0;cursor:pointer;font-size:.78rem;text-transform:uppercase;letter-spacing:.02em;color:#475569;white-space:nowrap}
  th:hover{color:var(--ink)}
  th .ar{color:#94a3b8;font-size:.7rem}
  tr:hover td{background:#f8fafc}
  td.ent{font-weight:600}
  a{color:var(--green-d);text-decoration:none}a:hover{text-decoration:underline}
  .chip{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.72rem;font-weight:600}
  .chip.hi{background:var(--chip);color:var(--chipink)}
  .chip.lo{background:#f1f5f9;color:#64748b}
  .chip.gen{background:#eff6ff;color:#1d4ed8}
  .chip.nom{background:#fef3c7;color:#92400e}
  .pager{display:flex;gap:6px;align-items:center;justify-content:center;margin-top:16px}
  .pager button{border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 11px;cursor:pointer}
  .pager button:disabled{opacity:.4;cursor:default}
  .muted{color:var(--muted)}
</style>
</head>
<body>
<header>
  <h1>📇 Base Outbound — Salons Agroalimentaire</h1>
  <p>Hello Harel · prospection B2B · généré le __DATE__ · __SALONS__ salon(s) · 1 seul fichier</p>
</header>
<div class="wrap">
  <div class="cards" id="cards"></div>
  <div class="toolbar">
    <input type="search" id="q" placeholder="🔎 Rechercher (entreprise, email, ville, secteur…)">
    <select id="fSalon"></select>
    <select id="fIcp"><option value="">ICP : tous</option><option>Haute</option><option>Faible/à qualifier</option></select>
    <select id="fType"><option value="">Email : tous</option><option value="generique">Génériques</option><option value="nominatif">Nominatifs</option><option value="__empty__">Sans email</option></select>
    <button class="btn" id="export">⬇️ Export CSV (filtré)</button>
    <span class="count" id="count"></span>
  </div>
  <div class="tablewrap">
    <table>
      <thead><tr id="head"></tr></thead>
      <tbody id="body"></tbody>
    </table>
  </div>
  <div class="pager" id="pager"></div>
</div>
<script>
const DATA = __DATA__;
const STATS = __STATS__;
const PAGE = 50;
let view = DATA.slice(), sortKey="entreprise", sortDir=1, page=1;

const COLS=[
 {k:"entreprise",t:"Entreprise"},{k:"secteur_metier",t:"Secteur / métier"},
 {k:"ville",t:"Ville"},{k:"email",t:"Email"},{k:"type_email",t:"Type"},
 {k:"telephone",t:"Tél"},{k:"site_web",t:"Site"},{k:"salon",t:"Salon"},
 {k:"segment_ICP",t:"ICP"}
];

function cards(){
  const c=[["total","Exposants"],["email","Avec email"],["gen","Génériques"],["hi","ICP Haute"],["salons","Salons"]];
  document.getElementById('cards').innerHTML=c.map(([k,l])=>
    `<div class="card"><div class="v">${STATS[k]}</div><div class="l">${l}</div></div>`).join('');
}
function fillSalon(){
  const s=[...new Set(DATA.map(r=>r.salon).filter(Boolean))].sort();
  document.getElementById('fSalon').innerHTML='<option value="">Salon : tous</option>'+s.map(x=>`<option>${x}</option>`).join('');
}
function head(){
  document.getElementById('head').innerHTML=COLS.map(c=>
    `<th data-k="${c.k}">${c.t} <span class="ar">${sortKey===c.k?(sortDir>0?'▲':'▼'):''}</span></th>`).join('');
  document.querySelectorAll('th').forEach(th=>th.onclick=()=>{
    const k=th.dataset.k; if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=1;} render();});
}
function esc(s){return (s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));}
function chipIcp(v){return v==='Haute'?'<span class="chip hi">Haute</span>':`<span class="chip lo">${esc(v||'—')}</span>`;}
function chipType(v){if(v==='generique')return '<span class="chip gen">générique</span>';if(v==='nominatif')return '<span class="chip nom">nominatif</span>';return '<span class="muted">—</span>';}
function apply(){
  const q=document.getElementById('q').value.toLowerCase().trim();
  const fs=document.getElementById('fSalon').value, fi=document.getElementById('fIcp').value, ft=document.getElementById('fType').value;
  view=DATA.filter(r=>{
    if(fs&&r.salon!==fs)return false;
    if(fi&&r.segment_ICP!==fi)return false;
    if(ft==='__empty__'){if(r.email)return false;}else if(ft&&r.type_email!==ft)return false;
    if(q){const blob=(r.entreprise+' '+r.email+' '+r.ville+' '+r.secteur_metier+' '+r.nom_contact).toLowerCase();if(!blob.includes(q))return false;}
    return true;
  });
  page=1; render();
}
function render(){
  view.sort((a,b)=>{const x=(a[sortKey]||'').toLowerCase(),y=(b[sortKey]||'').toLowerCase();return x<y?-sortDir:x>y?sortDir:0;});
  const pages=Math.max(1,Math.ceil(view.length/PAGE));
  if(page>pages)page=pages;
  const slice=view.slice((page-1)*PAGE,page*PAGE);
  document.getElementById('body').innerHTML=slice.map(r=>`<tr>
    <td class="ent">${esc(r.entreprise)}</td>
    <td class="muted">${esc(r.secteur_metier)}</td>
    <td>${esc(r.ville)}${r.departement?` <span class="muted">(${esc(r.departement)})</span>`:''}</td>
    <td>${r.email?`<a href="mailto:${esc(r.email)}">${esc(r.email)}</a>`:'<span class="muted">—</span>'}</td>
    <td>${chipType(r.type_email)}</td>
    <td class="muted">${esc(r.telephone)}</td>
    <td>${r.site_web?`<a href="${esc(r.site_web)}" target="_blank" rel="noopener">↗</a>`:''}</td>
    <td class="muted">${esc(r.salon)}</td>
    <td>${chipIcp(r.segment_ICP)}</td></tr>`).join('') || '<tr><td colspan="9" class="muted" style="padding:30px;text-align:center">Aucun résultat</td></tr>';
  head();
  document.getElementById('count').textContent=`${view.length} / ${DATA.length} exposants`;
  document.getElementById('pager').innerHTML=
    `<button ${page<=1?'disabled':''} id="prev">‹ Préc.</button>
     <span class="muted">Page ${page} / ${pages}</span>
     <button ${page>=pages?'disabled':''} id="next">Suiv. ›</button>`;
  const pv=document.getElementById('prev'),nx=document.getElementById('next');
  if(pv)pv.onclick=()=>{page--;render();}; if(nx)nx.onclick=()=>{page++;render();};
}
function exportCSV(){
  const cols=["salon","entreprise","secteur_metier","ville","departement","email","type_email","nom_contact","telephone","site_web","segment_ICP","source_url","date_collecte"];
  const lines=[cols.join(';')].concat(view.map(r=>cols.map(c=>`"${(r[c]||'').replace(/"/g,'""')}"`).join(';')));
  const blob=new Blob(["﻿"+lines.join('\n')],{type:'text/csv;charset=utf-8'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='base-outbound-filtre.csv';a.click();
}
cards();fillSalon();
document.getElementById('q').oninput=apply;
document.getElementById('fSalon').onchange=apply;
document.getElementById('fIcp').onchange=apply;
document.getElementById('fType').onchange=apply;
document.getElementById('export').onclick=exportCSV;
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
