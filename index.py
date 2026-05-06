#!/usr/bin/env python3
"""RO專業帶本代拉"""

from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

orders = []
ratio = {'0-1':'','1-2':'','2-3':'','3-4':'','4-5':'','5-6':'','6-7':'','7-8':'','8-9':'','9-10':''}
order_id = 1
PRICES = {'飛空艇英靈-500':500,'博物島英靈-300':300,'迷蹤島英靈-100':100,'星座塔Ⅵ-800':800,'混亂噩夢-800':800,'12人英靈-100':100,'神諭11-100':100}

CLIENT_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RO專業帶本代拉</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(180deg, #1e3a5f 0%, #2d4a6f 30%, #1e3a5f 70%, #0f2744 100%); color: #fff; min-height: 100vh; }
.container { max-width: 800px; margin: 0 auto; padding: 30px 20px; }
h1 { text-align: center; font-size: 32px; font-weight: 700; background: linear-gradient(90deg, #ffd700, #e6b800, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
.subtitle { text-align: center; color: #888; margin-bottom: 30px; }
.tabs { display: flex; gap: 10px; margin-bottom: 25px; }
.tab { flex: 1; padding: 16px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #aaa; cursor: pointer; font-size: 17px; font-weight: 600; border-radius: 16px; text-align: center; }
.tab.active { background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; }
.panel { display: none; }
.panel.active { display: block; }
.checkbox-group { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.checkbox-item { display: flex; align-items: center; justify-content: space-between; padding: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; cursor: pointer; }
.checkbox-item.checked { background: linear-gradient(135deg, #b8860b, #daa520); border-color: #ffd700; }
.checkbox-price { color: #ffd700; font-weight: 700; }
.qty-ctrl { display: flex; align-items: center; gap: 8px; }
.qty-ctrl button { width: 28px; height: 28px; background: rgba(255,255,255,0.2); border: none; border-radius: 6px; color: #fff; font-size: 18px; cursor: pointer; }
.qty-ctrl .qty-num { min-width: 20px; text-align: center; font-weight: 700; }
#total-display { text-align: center; font-size: 20px; font-weight: 700; margin: 15px 0; color: #ffd700; }
input { width: 100%; padding: 16px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 14px; font-size: 16px; margin-bottom: 15px; }
.btn { width: 100%; padding: 18px; background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border: none; border-radius: 14px; font-size: 17px; font-weight: 700; cursor: pointer; margin-top: 10px; }
.ratio-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.ratio-item { display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(255,255,255,0.05); border-radius: 8px; }
.ratio-item span:last-child { color: #4ade80; font-weight: 600; }
</style></head>
<body>
<div class="container">
<h1>⚔️ RO專業帶本代拉</h1>
<p class="subtitle">仙境傳說RO守護永恆的愛 Classic</p>
<div class="tabs">
<button class="tab active" data-tab="副本" onclick="switchTab(this)">📦 舒心躺本</button>
<button class="tab" data-tab="代拉" onclick="switchTab(this)">💰 代拉貨</button>
</div>
<div id="副本" class="panel active">
<form onsubmit="submitOrder(event)">
<div class="checkbox-group">
<div class="checkbox-item" onclick="toggle(this)" data-item="飛空艇英靈-500"><span>飛空艇英靈</span><span class="checkbox-price">NT$500</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="飛空艇英靈-500"></label>
<div class="checkbox-item" onclick="toggle(this)" data-item="博物島英靈-300"><span>博物島英靈</span><span class="checkbox-price">NT$300</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="博物島英靈-300"></label>
<div class="checkbox-item" onclick="toggle(this)" data-item="迷蹤島英靈-100"><span>迷蹤島英靈</span><span class="checkbox-price">NT$100</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="迷蹤島英靈-100"></label>
<div class="checkbox-item" onclick="toggle(this)" data-item="星座塔Ⅵ-800"><span>星座塔Ⅵ</span><span class="checkbox-price">NT$800</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="星座塔Ⅵ-800"></label>
<div class="checkbox-item" onclick="toggle(this)" data-item="混亂噩夢-800"><span>混亂噩夢</span><span class="checkbox-price">NT$800</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="混亂噩夢-800"></label>
<div class="checkbox-item" onclick="toggle(this)" data-item="12人英靈-100"><span>12人英靈</span><span class="checkbox-price">NT$100</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="12人英靈-100"></label>
<div class="checkbox-item" onclick="toggle(this)" data-item="神諭11-100"><span>神諭11</span><span class="checkbox-price">NT$100</span><div class="qty-ctrl"><button onclick="event.stopPropagation();qty(this,-1)">-</button><span class="qty-num">0</span><button onclick="event.stopPropagation();qty(this,1)">+</button></div><input type="hidden" name="item" value="神諭11-100"></label>
</div>
.input-group { margin-bottom: 15px; }
.input-group input { margin-bottom: 0; }
<input type="text" name="lineid" placeholder="LINE ID（會馬上聯係您）" required>
<div id="total-display">總計: NT$<span id="total-amount">0</span></div>
<button type="submit" class="btn">🚀 提交訂單</button>
</form>
</div>
<div id="代拉" class="panel">
<form onsubmit="submitBuy(event)">
<div class="ratio-grid" id="ratio-grid"><div class="ratio-item"><span>0-1E</span><span class="ratio-val" data-key="0-1">--</span></div><div class="ratio-item"><span>1-2E</span><span class="ratio-val" data-key="1-2">--</span></div><div class="ratio-item"><span>2-3E</span><span class="ratio-val" data-key="2-3">--</span></div><div class="ratio-item"><span>3-4E</span><span class="ratio-val" data-key="3-4">--</span></div><div class="ratio-item"><span>4-5E</span><span class="ratio-val" data-key="4-5">--</span></div><div class="ratio-item"><span>5-6E</span><span class="ratio-val" data-key="5-6">--</span></div><div class="ratio-item"><span>6-7E</span><span class="ratio-val" data-key="6-7">--</span></div><div class="ratio-item"><span>7-8E</span><span class="ratio-val" data-key="7-8">--</span></div><div class="ratio-item"><span>8-9E</span><span class="ratio-val" data-key="8-9">--</span></div><div class="ratio-item"><span>9-10E</span><span class="ratio-val" data-key="9-10">--</span></div></div>
<input type="text" name="lineid" placeholder="LINE ID（會馬上聯係您）" required>
<button type="submit" class="btn">🚀 提交訂單</button>
</form>
</div>
</div>
<script>
const PRICES2={'飛空艇英靈-500':500,'博物島英靈-300':300,'迷蹤島英靈-100':100,'星座塔Ⅵ-800':800,'混亂噩夢-800':800,'12人英靈-100':100,'神諭11-100':100};
function switchTab(btn) { document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active')); document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active')); document.getElementById(btn.dataset.tab).classList.add('active'); btn.classList.add('active'); if(btn.dataset.tab==='代拉') loadRatio(); }
function toggle(item) { item.classList.toggle('checked'); const qty=item.querySelector('.qty-num'); if(item.classList.contains('checked')&&qty.textContent==='0') qty.textContent='1'; updateTotal(); }
function qty(btn,delta) { const item=btn.closest('.checkbox-item'); const qty=item.querySelector('.qty-num'); let n=parseInt(qty.textContent)+delta; if(n<0)n=0; if(n>10)n=10; qty.textContent=n; if(n>0)item.classList.add('checked'); else item.classList.remove('checked'); updateTotal(); }
function updateTotal() { let t=0; document.querySelectorAll('#副本 .checkbox-item').forEach(i=>{ const v=i.dataset.item; const qty=parseInt(i.querySelector('.qty-num').textContent)||0; t+=(PRICES2[v]||0)*qty; }); document.getElementById('total-amount').textContent=t; }
async function loadRatio() { const r=await fetch('/api/ratio'); const d=await r.json(); document.querySelectorAll('.ratio-val').forEach(el=>{ el.textContent = d[el.dataset.key]||'--'; }); }
async function submitOrder(e) { e.preventDefault(); const items=[]; document.querySelectorAll('#副本 .checkbox-item').forEach(i=>{ const v=i.dataset.item; const qty=parseInt(i.querySelector('.qty-num').textContent)||0; for(let n=0;n<qty;n++)items.push(v); }); if(items.length===0) return alert('請選擇至少一個副本'); const lineid=e.target.lineid.value; await fetch('/api/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'副本',items,lineid})}); alert('✅ 提交成功！'); e.target.reset(); document.querySelectorAll('.qty-num').forEach(q=>q.textContent='0'); document.querySelectorAll('.checkbox-item').forEach(i=>i.classList.remove('checked')); updateTotal(); }
async function submitBuy(e) { e.preventDefault(); const lineid=e.target.lineid.value; await fetch('/api/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'代拉',items:[],lineid})}); alert('✅ 提交成功！'); e.target.reset(); }
</script>
</body>
</html>'''

ADMIN_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RO管理後台</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: #fff; min-height: 100vh; }
.container { max-width: 900px; margin: 0 auto; padding: 30px 20px; }
h1 { text-align: center; font-size: 28px; font-weight: 700; color: #4ade80; margin-bottom: 25px; }
.toolbar { display: flex; gap: 10px; margin-bottom: 25px; }
.toolbar-btn { padding: 12px 20px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #ccc; border-radius: 10px; cursor: pointer; }
.toolbar-btn.active { background: #e6b800; color: #1a1a2e; }
.order-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 18px; margin-bottom: 12px; border-radius: 14px; }
.order-type { font-size: 15px; font-weight: 600; padding: 4px 12px; border-radius: 6px; display: inline-block; margin-right: 10px; }
.order-type.dungeon { background: rgba(139,92,246,0.2); color: #a78bfa; }
.order-type.buy { background: rgba(34,197,94,0.2); color: #4ade80; }
.order-total { color: #fbbf24; font-weight: 700; }
.order-tag { background: rgba(230,184,0,0.2); color: #ffd700; padding: 4px 10px; border-radius: 6px; margin-right: 6px; display: inline-block; font-size: 13px; }
.order-line { color: #4ade80; margin: 10px 0; }
.btn-complete { padding: 10px 20px; background: #22c55e; color: white; border: none; border-radius: 10px; cursor: pointer; margin-right: 8px; }
.btn-paid { padding: 10px 20px; background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border: none; border-radius: 10px; cursor: pointer; margin-right: 8px; font-weight: 600; }
.btn-delete { padding: 10px 20px; background: rgba(239,68,68,0.2); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); border-radius: 10px; cursor: pointer; }
.stat-paid .stat-num { color: #e6b800; }
.paid-title { color: #e6b800; }
.stats { display: flex; gap: 20px; margin-bottom: 25px; }
.stat-item { background: rgba(255,255,255,0.05); padding: 15px 25px; border-radius: 12px; text-align: center; min-width: 120px; }
.stat-num { font-size: 28px; font-weight: 700; }
.stat-pending .stat-num { color: #fbbf24; }
.stat-done .stat-num { color: #4ade80; }
.ratio-section { display: none; }
.ratio-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(150px,1fr)); gap: 12px; }
.ratio-item { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); padding: 10px 12px; border-radius: 8px; }
.ratio-item input { width: 60px; padding: 6px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #fff; border-radius: 6px; }
.btn-ratio { padding: 12px 30px; background: #22c55e; color: white; border: none; border-radius: 10px; cursor: pointer; margin-top: 15px; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); }
.pending-title { color: #fbbf24; }
.history-title { color: #4ade80; }
</style></head>
<body>
<div class="container">
<h1>⚙️ RO管理後台</h1>
<div class="toolbar">
<button class="toolbar-btn active" onclick="showPending()">⏳ 待辦</button>
<button class="toolbar-btn" onclick="showPaid()">💰 已收款</button>
<button class="toolbar-btn" onclick="showDone()">✅ 歷史</button>
<button class="toolbar-btn" onclick="showRatio()">💰 代拉比例</button>
</div>
<div class="ratio-section" id="ratio-section">
<div style="font-size:16px;font-weight:600;color:#4ade80;margin-bottom:15px;">💰 代拉比例設置</div>
<div class="ratio-grid">
<div class="ratio-item"><label>0-1E：</label><input id="ratio-0-1"></div>
<div class="ratio-item"><label>1-2E：</label><input id="ratio-1-2"></div>
<div class="ratio-item"><label>2-3E：</label><input id="ratio-2-3"></div>
<div class="ratio-item"><label>3-4E：</label><input id="ratio-3-4"></div>
<div class="ratio-item"><label>4-5E：</label><input id="ratio-4-5"></div>
<div class="ratio-item"><label>5-6E：</label><input id="ratio-5-6"></div>
<div class="ratio-item"><label>6-7E：</label><input id="ratio-6-7"></div>
<div class="ratio-item"><label>7-8E：</label><input id="ratio-7-8"></div>
<div class="ratio-item"><label>8-9E：</label><input id="ratio-8-9"></div>
<div class="ratio-item"><label>9-10E：</label><input id="ratio-9-10"></div>
</div>
<button class="btn-ratio" onclick="saveRatio()">💾 提交更改</button>
</div>
<div class="stats" id="stats">
<div class="stat-item stat-pending"><div class="stat-num" id="stat-pending">0</div><div>待辦事項</div></div>
<div class="stat-item stat-paid"><div class="stat-num" id="stat-paid">0</div><div>已收款</div></div>
<div class="stat-item stat-done"><div class="stat-num" id="stat-done">0</div><div>已完成</div></div>
</div>
<div id="pending-section">
<h2 class="section-title pending-title">📋 待辦事項</h2>
<div id="pending-orders"></div>
</div>
<div id="paid-section" style="display:none;">
<h2 class="section-title paid-title">💰 已收款</h2>
<div id="paid-orders"></div>
</div>
<div id="done-section" style="display:none;">
<h2 class="section-title history-title">✅ 歷史記錄</h2>
<div id="done-orders"></div>
</div>
</div>
<script>
async function loadOrders(){ const res=await fetch('/api/orders'); const data=await res.json(); const p=data.orders.filter(o=>!o.done&&!o.paid); const paid=data.orders.filter(o=>o.paid&&!o.done); const d=data.orders.filter(o=>o.done); document.getElementById('stat-pending').textContent=p.length; document.getElementById('stat-paid').textContent=paid.length; document.getElementById('stat-done').textContent=d.length; const prices=data.prices||{}; document.getElementById('pending-orders').innerHTML=p.length?p.map(o=>render(o,prices)).join(''):'暫無待辦事項'; document.getElementById('paid-orders').innerHTML=paid.length?paid.map(o=>render(o,prices)).join(''):'暫無已收款'; document.getElementById('done-orders').innerHTML=d.length?d.map(o=>render(o,prices)).join(''):'暫無歷史記錄'; }
function render(o,prices){ let items=''; if(o.items&&o.items.length){ items='<div style="margin:10px 0;">'+o.items.map(n=>{ const price=prices[n.split('-')[0]]||0; return '<span class="order-tag">'+n.split('-')[0]+(price?' NT$'+price:'')+'</span>'}).join('')+'</div>'; } let total=''; if(o.type=='副本'&&o.items){ let t=0; o.items.forEach(i=>t+=prices[i.split('-')[0]]||0); total='<span class="order-total">NT$'+t+'</span>'; } let btns=''; if(o.done){ btns='<button class="btn-delete" onclick="deleteOrder('+o.id+')">🗑️</button>'; } else if(o.paid){ btns='<button class="btn-complete" onclick="completeOrder('+o.id+')">✅ 完成</button><button class="btn-delete" onclick="deleteOrder('+o.id+')">🗑️</button>'; } else { btns='<button class="btn-paid" onclick="paidOrder('+o.id+')">💰 已收款</button><button class="btn-delete" onclick="deleteOrder('+o.id+')">🗑️</button>'; } return '<div class="order-card"><span class="order-type '+(o.type=='副本'?'dungeon':'buy')+'">'+(o.type=='副本'?'📦 副本':'💰 代拉')+'</span><span>#'+o.id+'</span><span>'+o.time+'</span>'+total+'</div>'+items+'<div class="order-line">LINE: '+o.lineid+'</div><div>'+btns+'</div></div>'; }
async function paidOrder(id){ await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'paid'})}); loadOrders(); }
async function completeOrder(id){ await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'complete'})}); loadOrders(); }
async function deleteOrder(id){ if(!confirm('確定？'))return; await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'delete'})}); loadOrders(); }
function showPending(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='none'; document.getElementById('stats').style.display='flex'; document.getElementById('pending-section').style.display='block'; document.getElementById('paid-section').style.display='none'; document.getElementById('done-section').style.display='none'; loadOrders(); }
function showPaid(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='none'; document.getElementById('stats').style.display='flex'; document.getElementById('pending-section').style.display='none'; document.getElementById('paid-section').style.display='block'; document.getElementById('done-section').style.display='none'; loadOrders(); }
function showDone(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='none'; document.getElementById('stats').style.display='none'; document.getElementById('pending-section').style.display='none'; document.getElementById('paid-section').style.display='none'; document.getElementById('done-section').style.display='block'; loadOrders(); }
function showRatio(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active')); event.target.classList.add('active'); document.getElementById('ratio-section').style.display='block'; document.getElementById('stats').style.display='none'; document.getElementById('pending-section').style.display='none'; document.getElementById('paid-section').style.display='none'; document.getElementById('done-section').style.display='none'; fetch('/api/ratio').then(r=>r.json()).then(d=>{ document.getElementById('ratio-0-1').value=d['0-1']||''; document.getElementById('ratio-1-2').value=d['1-2']||''; document.getElementById('ratio-2-3').value=d['2-3']||''; document.getElementById('ratio-3-4').value=d['3-4']||''; document.getElementById('ratio-4-5').value=d['4-5']||''; document.getElementById('ratio-5-6').value=d['5-6']||''; document.getElementById('ratio-6-7').value=d['6-7']||''; document.getElementById('ratio-7-8').value=d['7-8']||''; document.getElementById('ratio-8-9').value=d['8-9']||''; document.getElementById('ratio-9-10').value=d['9-10']||''; }); }
async function saveRatio(){ const r={'0-1':document.getElementById('ratio-0-1').value,'1-2':document.getElementById('ratio-1-2').value,'2-3':document.getElementById('ratio-2-3').value,'3-4':document.getElementById('ratio-3-4').value,'4-5':document.getElementById('ratio-4-5').value,'5-6':document.getElementById('ratio-5-6').value,'6-7':document.getElementById('ratio-6-7').value,'7-8':document.getElementById('ratio-7-8').value,'8-9':document.getElementById('ratio-8-9').value,'9-10':document.getElementById('ratio-9-10').value}; await fetch('/api/ratio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(r)}); alert('✅ 已保存！'); }
loadOrders(); setInterval(loadOrders, 15000);
</script>
</body>
</html>'''

@app.route('/')
@app.route('/client')
def client():
    return CLIENT_HTML

@app.route('/admin')
def admin():
    return ADMIN_HTML

@app.route('/api/orders')
def api_orders():
    return jsonify({'orders': orders, 'prices': PRICES})

@app.route('/api/ratio', methods=['GET'])
def api_ratio():
    return jsonify(ratio)

@app.route('/api/ratio', methods=['POST'])
def api_save_ratio():
    global ratio
    ratio.update(request.json)
    return jsonify({'ok': True})

@app.route('/api/order', methods=['POST'])
def api_order():
    global order_id
    data = request.json
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
    return jsonify({'ok': True})

@app.route('/api/action', methods=['POST'])
def api_action():
    data = request.json
    oid = data.get('id')
    action = data.get('action')
    for o in orders:
        if o['id'] == oid:
            if action == 'complete':
                o['done'] = True
            elif action == 'paid':
                o['paid'] = True
            elif action == 'delete':
                orders.remove(o)
            break
    return jsonify({'ok': True})