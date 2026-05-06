#!/usr/bin/env python3
"""RO專業帶本代拉 - Vercel版本"""

import json
from datetime import datetime

# In-memory storage
orders = []
ratio = {'0-1':'','1-2':'','2-3':'','3-4':'','4-5':'','5-6':'','6-7':'','7-8':'','8-9':'','9-10':''}
order_id = 1

# 副本价格
PRICES = {'飛空艇英靈-500':500,'博物島英靈-300':300,'迷蹤島英靈-100':100,'星座塔Ⅵ-800':800,'混亂噩夢-800':800,'12人英靈-100':100,'神諭11-100':100}
EXCHANGE = 4.5

CLIENT_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RO專業帶本代拉</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(180deg, #1e3a5f 0%, #2d4a6f 30%, #1e3a5f 70%, #0f2744 100%); color: #fff; min-height: 100vh; background-attachment: fixed; }
body::before { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 15% 15%, rgba(255,215,0,0.2) 0%, transparent 40%), radial-gradient(ellipse at 85% 85%, rgba(78,205,196,0.15) 0%, transparent 40%); pointer-events: none; z-index: -1; }
.container { max-width: 800px; margin: 0 auto; padding: 30px 20px; }
h1 { text-align: center; font-size: 32px; font-weight: 700; background: linear-gradient(90deg, #ffd700, #e6b800, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
.subtitle { text-align: center; color: #888; margin-bottom: 30px; font-size: 14px; }
.tabs { display: flex; gap: 10px; margin-bottom: 25px; }
.tab { flex: 1; padding: 16px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #aaa; cursor: pointer; font-size: 17px; font-weight: 600; border-radius: 16px; text-align: center; transition: all 0.3s; }
.tab:hover { background: rgba(255,255,255,0.1); }
.tab.active { background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border-color: #e6b800; }
.panel { display: none; }
.panel.active { display: block; animation: fadeIn 0.3s; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.form-group { margin-bottom: 20px; }
.form-label { display: block; margin-bottom: 12px; color: #ccc; font-size: 15px; font-weight: 600; }
.checkbox-group { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
@media (max-width: 500px) { .checkbox-group { grid-template-columns: 1fr; } }
.checkbox-item { display: flex; align-items: center; justify-content: space-between; padding: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; cursor: pointer; transition: all 0.2s; }
.checkbox-item:hover { background: rgba(255,255,255,0.12); border-color: rgba(230,184,0,0.3); }
.checkbox-item.checked { background: linear-gradient(135deg, #b8860b, #daa520); border-color: #ffd700; box-shadow: 0 4px 15px rgba(255,215,0,0.3); }
.checkbox-name { font-size: 16px; font-weight: 600; }
.checkbox-price { font-size: 20px; font-weight: 700; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.5); }
input[type="text"] { width: 100%; padding: 16px 18px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 14px; font-size: 16px; }
input[type="text"]:focus { outline: none; border-color: #e6b800; }
input[type="text"]::placeholder { color: #666; }
.btn { width: 100%; padding: 18px; background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border: none; border-radius: 14px; font-size: 17px; font-weight: 700; cursor: pointer; margin-top: 25px; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(230,184,0,0.4); }
.ratio-display { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 16px; border-radius: 12px; margin-bottom: 20px; }
.ratio-title { font-size: 14px; font-weight: 600; color: #4ade80; margin-bottom: 12px; }
.ratio-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.ratio-item { display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(255,255,255,0.05); border-radius: 8px; font-size: 13px; }
.ratio-item span:first-child { color: #aaa; }
.ratio-item span:last-child { color: #4ade80; font-weight: 600; }
</style>
</head>
<body>
<div class="container">
<h1>⚔️ RO專業帶本代拉</h1>
<p class="subtitle">仙境傳說RO守護永恆的愛 Classic</p>
<div class="tabs">
<button class="tab active" data-tab="副本">📦 舒心躺本</button>
<button class="tab" data-tab="代拉">💰 代拉貨</button>
</div>
<div id="副本" class="panel active">
<form id="form-副本">
<div class="form-group">
<label class="form-label">選擇副本（可多選）</label>
<div class="checkbox-group">
<label class="checkbox-item" data-value="飛空艇英靈-500" onclick="toggleItem(this)"><span class="checkbox-name">飛空艇英靈</span><span class="checkbox-price">NT$500</span></label>
<label class="checkbox-item" data-value="博物島英靈-300" onclick="toggleItem(this)"><span class="checkbox-name">博物島英靈</span><span class="checkbox-price">NT$300</span></label>
<label class="checkbox-item" data-value="迷蹤島英靈-100" onclick="toggleItem(this)"><span class="checkbox-name">迷蹤島英靈</span><span class="checkbox-price">NT$100</span></label>
<label class="checkbox-item" data-value="星座塔Ⅵ-800" onclick="toggleItem(this)"><span class="checkbox-name">星座塔Ⅵ</span><span class="checkbox-price">NT$800</span></label>
<label class="checkbox-item" data-value="混亂噩夢-800" onclick="toggleItem(this)"><span class="checkbox-name">混亂噩夢</span><span class="checkbox-price">NT$800</span></label>
<label class="checkbox-item" data-value="12人英靈-100" onclick="toggleItem(this)"><span class="checkbox-name">12人英靈</span><span class="checkbox-price">NT$100</span></label>
<label class="checkbox-item" data-value="神諭11-100" onclick="toggleItem(this)"><span class="checkbox-name">神諭11</span><span class="checkbox-price">NT$100</span></label>
</div>
</div>
<div class="form-group"><label class="form-label">LINE ID <span style="font-size:12px;color:#888;">（留下LINE ID會馬上聯係您）</span></label><input type="text" id="副本-line-id" placeholder="請輸入您的LINE ID" required></div>
<button type="submit" class="btn">🚀 提交訂單</button>
</form>
</div>
<div id="代拉" class="panel">
<form id="form-代拉">
<div class="ratio-display"><div class="ratio-title">💰 代拉比例</div><div class="ratio-grid">
<div class="ratio-item"><span>0-1E</span><span class="ratio-val" data-key="0-1">--</span></div>
<div class="ratio-item"><span>1-2E</span><span class="ratio-val" data-key="1-2">--</span></div>
<div class="ratio-item"><span>2-3E</span><span class="ratio-val" data-key="2-3">--</span></div>
<div class="ratio-item"><span>3-4E</span><span class="ratio-val" data-key="3-4">--</span></div>
<div class="ratio-item"><span>4-5E</span><span class="ratio-val" data-key="4-5">--</span></div>
<div class="ratio-item"><span>5-6E</span><span class="ratio-val" data-key="5-6">--</span></div>
<div class="ratio-item"><span>6-7E</span><span class="ratio-val" data-key="6-7">--</span></div>
<div class="ratio-item"><span>7-8E</span><span class="ratio-val" data-key="7-8">--</span></div>
<div class="ratio-item"><span>8-9E</span><span class="ratio-val" data-key="8-9">--</span></div>
<div class="ratio-item"><span>9-10E</span><span class="ratio-val" data-key="9-10">--</span></div>
</div></div>
<div class="form-group"><label class="form-label">LINE ID <span style="font-size:12px;color:#888;">（留下LINE ID會馬上聯係您）</span></label><input type="text" id="代拉-line-id" placeholder="請輸入您的LINE ID" required></div>
<button type="submit" class="btn">🚀 提交訂單</button>
</form>
</div>
</div>
<script>
let selectedItems = [];
function loadRatio() { fetch('/api/ratio').then(r=>r.json()).then(d=>{ document.querySelectorAll('.ratio-val').forEach(el=>{ const k=el.dataset.key; el.textContent = d[k]||'--'; }); }); }
document.querySelectorAll('.tab').forEach(tab=>{ tab.onclick=()=>{ document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active')); document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active')); document.getElementById(tab.dataset.tab).classList.add('active'); tab.classList.add('active'); if(tab.dataset.tab==='代拉') loadRatio(); }; });
function toggleItem(item) { const v=item.dataset.value; if(selectedItems.includes(v)){ selectedItems = selectedItems.filter(x=>x!==v); item.classList.remove('checked'); }else{ selectedItems.push(v); item.classList.add('checked'); } }
document.getElementById('form-副本').onsubmit=async(e)=>{ e.preventDefault(); if(selectedItems.length===0) return alert('請選擇至少一個副本'); const lid=document.getElementById('副本-line-id').value; if(!lid) return alert('請輸入LINE ID'); const res=await fetch('/api/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'副本',items:selectedItems,lineid:lid})}); if(res.ok){ alert('✅ 提交成功！'); e.target.reset(); selectedItems=[]; document.querySelectorAll('.checkbox-item').forEach(i=>i.classList.remove('checked')); } };
document.getElementById('form-代拉').onsubmit=async(e)=>{ e.preventDefault(); const lid=document.getElementById('代拉-line-id').value; if(!lid) return alert('請輸入LINE ID'); const res=await fetch('/api/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'代拉',items:[],lineid:lid})}); if(res.ok){ alert('✅ 提交成功！'); e.target.reset(); } };
</script>
</body>
</html>'''

ADMIN_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RO管理後台</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #fff; min-height: 100vh; }
body::before{ content:''; position:fixed; top:0;left:0;right:0;bottom:0; background:radial-gradient(ellipse at 20% 80%,rgba(230,184,0,0.15),transparent 50%),radial-gradient(ellipse at 80% 20%,rgba(78,205,196,0.1),transparent 50%); pointer-events:none; z-index:-1; }
.container { max-width: 900px; margin: 0 auto; padding: 30px 20px; }
h1 { text-align: center; font-size: 28px; font-weight: 700; background: linear-gradient(90deg,#4ade80,#22c55e,#4ade80); -webkit-background-clip:text; -webkit-text-fill-color: transparent; margin-bottom: 25px; }
.toolbar { display: flex; gap: 10px; margin-bottom: 25px; flex-wrap: wrap; }
.toolbar-btn { padding: 12px 20px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #ccc; border-radius: 10px; cursor: pointer; font-size: 14px; }
.toolbar-btn.active { background: #e6b800; color: #1a1a2e; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.pending-title { color: #fbbf24; }
.history-title { color: #4ade80; }
.order-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 18px; margin-bottom: 12px; border-radius: 14px; }
.order-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px; }
.order-type { font-size: 15px; font-weight: 600; padding: 4px 12px; border-radius: 6px; }
.order-type.dungeon { background: rgba(139,92,246,0.2); color: #a78bfa; }
.order-type.buy { background: rgba(34,197,94,0.2); color: #4ade80; }
.order-total { background: linear-gradient(135deg,rgba(245,158,11,0.2),rgba(251,191,36,0.15)); color: #fbbf24; padding: 6px 14px; border-radius: 8px; font-size: 15px; font-weight: 700; }
.order-tag { background: linear-gradient(135deg,rgba(230,184,0,0.2),rgba(255,215,0,0.15)); color: #ffd700; padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: 500; margin-right: 6px; display: inline-block; }
.order-line { color: #4ade80; font-size: 15px; margin: 8px 0; }
.order-actions { display: flex; gap: 8px; margin-top: 15px; flex-wrap: wrap; }
.btn-complete { padding: 10px 20px; background: linear-gradient(135deg,#22c55e,#4ade80); color: white; border: none; border-radius: 10px; cursor: pointer; font-size: 14px; font-weight: 600; }
.btn-delete { padding: 10px 20px; background: rgba(239,68,68,0.2); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); border-radius: 10px; cursor: pointer; font-size: 14px; }
.no-orders { color: #666; text-align: center; padding: 40px; font-size: 15px; }
.stats { display: flex; gap: 20px; margin-bottom: 25px; flex-wrap: wrap; }
.stat-item { background: rgba(255,255,255,0.05); padding: 15px 25px; border-radius: 12px; text-align: center; min-width: 120px; }
.stat-num { font-size: 28px; font-weight: 700; }
.stat-label { font-size: 13px; color: #888; margin-top: 5px; }
.stat-pending .stat-num { color: #fbbf24; }
.stat-done .stat-num { color: #4ade80; }
.ratio-section { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 20px; border-radius: 14px; margin-bottom: 25px; display: none; }
.ratio-title { font-size: 16px; font-weight: 600; color: #4ade80; margin-bottom: 15px; }
.ratio-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(150px,1fr)); gap: 12px; }
.ratio-item { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); padding: 10px 12px; border-radius: 8px; }
.ratio-item label { font-size: 13px; color: #aaa; white-space: nowrap; }
.ratio-item input { width: 60px; padding: 6px 8px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #fff; border-radius: 6px; font-size: 14px; text-align: center; }
.btn-ratio { padding: 12px 30px; background: linear-gradient(135deg,#22c55e,#4ade80); color: white; border: none; border-radius: 10px; cursor: pointer; font-size: 15px; font-weight: 600; margin-top: 15px; }
</style>
</head>
<body>
<div class="container">
<h1>⚙️ RO管理後台</h1>
<div class="toolbar">
<button class="toolbar-btn active" onclick="showPending()">⏳ 待辦</button>
<button class="toolbar-btn" onclick="showDone()">✅ 歷史</button>
<button class="toolbar-btn" onclick="showRatio()">💰 代拉比例</button>
</div>
<div class="ratio-section" id="ratio-section">
<div class="ratio-title">💰 代拉比例設置</div>
<div class="ratio-grid">
<div class="ratio-item"><label>0-1E比例：</label><input type="text" id="ratio-0-1" placeholder="%"></div>
<div class="ratio-item"><label>1-2E比例：</label><input type="text" id="ratio-1-2" placeholder="%"></div>
<div class="ratio-item"><label>2-3E比例：</label><input type="text" id="ratio-2-3" placeholder="%"></div>
<div class="ratio-item"><label>3-4E比例：</label><input type="text" id="ratio-3-4" placeholder="%"></div>
<div class="ratio-item"><label>4-5E比例：</label><input type="text" id="ratio-4-5" placeholder="%"></div>
<div class="ratio-item"><label>5-6E比例：</label><input type="text" id="ratio-5-6" placeholder="%"></div>
<div class="ratio-item"><label>6-7E比例：</label><input type="text" id="ratio-6-7" placeholder="%"></div>
<div class="ratio-item"><label>7-8E比例：</label><input type="text" id="ratio-7-8" placeholder="%"></div>
<div class="ratio-item"><label>8-9E比例：</label><input type="text" id="ratio-8-9" placeholder="%"></div>
<div class="ratio-item"><label>9-10E比例：</label><input type="text" id="ratio-9-10" placeholder="%"></div>
</div>
<button class="btn-ratio" onclick="saveRatio()">💾 提交更改</button>
</div>
<div class="stats" id="stats">
<div class="stat-item stat-pending"><div class="stat-num" id="stat-pending">0</div><div class="stat-label">待辦事項</div></div>
<div class="stat-item stat-done"><div class="stat-num" id="stat-done">0</div><div class="stat-label">已完成</div></div>
</div>
<div class="section" id="pending-section">
<h2 class="section-title pending-title">📋 待辦事項</h2>
<div id="pending-orders"></div>
</div>
<div class="section" id="done-section" style="display:none;">
<h2 class="section-title history-title">✅ 歷史記錄</h2>
<div id="done-orders"></div>
</div>
</div>
<script>
function calcTotal(items){ let t=0; items.forEach(i=>t+=PRICES[i]||0); return {twd:t,cny:(t/EXCHANGE).toFixed(2)}; }
async function loadOrders(){ const res = await fetch('/api/orders'); const data = await res.json(); const p = data.orders.filter(o=>!o.done); const d = data.orders.filter(o=>o.done); document.getElementById('stat-pending').textContent = p.length; document.getElementById('stat-done').textContent = d.length; document.getElementById('pending-orders').innerHTML = p.length ? p.map(o=>render(o)).join('') : '<div class="no-orders">暫無待辦事項</div>'; document.getElementById('done-orders').innerHTML = d.length ? d.map(o=>render(o)).join('') : '<div class="no-orders">暫無歷史記錄</div>'; }
function render(o){ let items=''; if(o.items&&o.items.length){ items='<div style="margin:10px 0;">'+o.items.map(n=>'<span class="order-tag">'+n.split('-')[0]+'</span>').join('')+'</div>'; } let total=''; if(o.type=='副本'&&o.items&&o.items.length){ const {twd,cny}=calcTotal(o.items); total='<span class="order-total">NT$'+twd+' 約¥'+cny+'</span>'; } let btns = !o.done ? '<button class="btn-complete" onclick="completeOrder('+o.id+')">✅ 完成</button><button class="btn-delete" onclick="deleteOrder('+o.id+')">🗑️ 刪除</button>' : '<button class="btn-delete" onclick="deleteOrder('+o.id+')">🗑️ 刪除</button>'; return '<div class="order-card"><div class="order-header"><span class="order-type '+(o.type=='副本'?'dungeon':'buy')+'">'+(o.type=='副本'?'📦 代帶副本':'💰 代拉貨')+'</span><span>#'+o.id+'</span><span>'+o.time+'</span>'+total+'</div>'+items+'<div class="order-line">LINE: '+o.lineid+'</div><div class="order-actions">'+btns+'</div></div>'; }
async function completeOrder(id){ await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'complete'})}); loadOrders(); }
async function deleteOrder(id){ if(!confirm('確定要刪除？'))return; await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'delete'})}); loadOrders(); }
function showPending(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='none'; document.getElementById('stats').style.display='flex'; document.getElementById('pending-section').style.display='block'; document.getElementById('done-section').style.display='none'; loadOrders(); }
function showDone(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='none'; document.getElementById('stats').style.display='none'; document.getElementById('pending-section').style.display='none'; document.getElementById('done-section').style.display='block'; loadOrders(); }
function showRatio(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='block'; document.getElementById('stats').style.display='none'; document.getElementById('pending-section').style.display='none'; document.getElementById('done-section').style.display='none'; fetch('/api/ratio').then(r=>r.json()).then(d=>{ document.getElementById('ratio-0-1').value=d['0-1']||''; document.getElementById('ratio-1-2').value=d['1-2']||''; document.getElementById('ratio-2-3').value=d['2-3']||''; document.getElementById('ratio-3-4').value=d['3-4']||''; document.getElementById('ratio-4-5').value=d['4-5']||''; document.getElementById('ratio-5-6').value=d['5-6']||''; document.getElementById('ratio-6-7').value=d['6-7']||''; document.getElementById('ratio-7-8').value=d['7-8']||''; document.getElementById('ratio-8-9').value=d['8-9']||''; document.getElementById('ratio-9-10').value=d['9-10']||''; }); }
async function saveRatio(){ const r = { '0-1':document.getElementById('ratio-0-1').value,'1-2':document.getElementById('ratio-1-2').value,'2-3':document.getElementById('ratio-2-3').value,'3-4':document.getElementById('ratio-3-4').value,'4-5':document.getElementById('ratio-4-5').value,'5-6':document.getElementById('ratio-5-6').value,'6-7':document.getElementById('ratio-6-7').value,'7-8':document.getElementById('ratio-7-8').value,'8-9':document.getElementById('ratio-8-9').value,'9-10':document.getElementById('ratio-9-10').value }; await fetch('/api/ratio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(r)}); alert('✅ 代拉比例已保存！'); }
loadOrders(); setInterval(loadOrders, 15000);
</script>
</body>
</html>'''

# Vercel handler
def handler(request):
    global order_id, orders, ratio
    
    path = request.path
    method = request.method
    
    if path == '/' or path == '' or path == '/index.html' or path == '/client':
        return {'statusCode': 200, 'headers': {'Content-Type': 'text/html; charset=utf-8'}, 'body': CLIENT_HTML}
    
    if path == '/admin':
        return {'statusCode': 200, 'headers': {'Content-Type': 'text/html; charset=utf-8'}, 'body': ADMIN_HTML}
    
    if path == '/api/orders':
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'orders': orders})}
    
    if path == '/api/ratio':
        if method == 'POST':
            try:
                data = json.loads(request.body) if request.body else {}
                ratio.update(data)
                return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'ok': True})}
            except:
                return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Invalid request'})}
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(ratio)}
    
    if path == '/api/order' and method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            order = {
                'id': order_id,
                'type': data.get('type', '副本'),
                'items': data.get('items', []),
                'lineid': data.get('lineid', ''),
                'done': False,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            orders.append(order)
            order_id += 1
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'ok': True})}
        except:
            return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Invalid request'})}
    
    if path == '/api/action' and method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            oid = data.get('id')
            action = data.get('action')
            for o in orders:
                if o['id'] == oid:
                    if action == 'complete':
                        o['done'] = True
                    elif action == 'delete':
                        orders.remove(o)
                    break
            return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'ok': True})}
        except:
            return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Invalid request'})}
    
    return {'statusCode': 404, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Not found'})}