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
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>RO專業帶本</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(180deg, #1e3a5f 0%, #2d4a6f 30%, #1e3a5f 70%, #0f2744 100%); color: #fff; min-height: 100vh; padding: 20px; }
.container { max-width: 500px; margin: 0 auto; }
h1 { text-align: center; font-size: 26px; font-weight: 700; background: linear-gradient(90deg, #ffd700, #e6b800, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px; }
.subtitle { text-align: center; color: #888; font-size: 14px; margin-bottom: 20px; }
.tabs { display: flex; gap: 10px; margin-bottom: 20px; }
.tab { flex: 1; padding: 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #aaa; cursor: pointer; font-size: 15px; font-weight: 600; border-radius: 12px; text-align: center; }
.tab.active { background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; }
.panel { display: none; }
.panel.active { display: block; }
.checkbox-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 10px; cursor: pointer; transition: all 0.2s; }
.checkbox-item.checked { background: linear-gradient(135deg, #b8860b, #daa520); border-color: #ffd700; box-shadow: 0 4px 15px rgba(255,215,0,0.3); }
.checkbox-item span:first-child { font-size: 15px; }
.checkbox-item span:last-child { font-size: 14px; color: #aaa; }
.checkbox-item.checked span:last-child { color: #fff; }
.qty-btn { display: none; width: 32px; height: 32px; background: rgba(255,255,255,0.3); border: none; border-radius: 8px; color: #fff; font-size: 20px; cursor: pointer; margin-left: 4px; }
.checkbox-item.checked .qty-btn { display: inline-block; }
.qty-num { display: none; min-width: 26px; text-align: center; font-weight: bold; margin: 0 4px; font-size: 16px; }
.checkbox-item.checked .qty-num { display: inline-block; }
.total-box { text-align: center; font-size: 18px; font-weight: bold; margin: 16px 0; color: #ffd700; }
input[type="text"] { width: 100%; padding: 14px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 12px; font-size: 15px; margin-bottom: 12px; }
input[type="file"] { width: 100%; padding: 12px; background: rgba(255,255,255,0.08); border: 1px dashed rgba(255,255,255,0.3); border-radius: 12px; color: #aaa; margin-bottom: 12px; }
.btn { width: 100%; padding: 16px; background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border: none; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; }
.btn:active { transform: scale(0.98); }
.ratio-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.ratio-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; background: rgba(255,255,255,0.05); border-radius: 10px; }
.ratio-item span:first-child { color: #aaa; font-size: 14px; }
.ratio-item span:last-child { color: #4ade80; font-weight: 600; }
</style></head>
<body>
<div class="container">
<h1>⚔️ RO專業帶本</h1>
<p class="subtitle">仙境傳說RO守護永恆的愛 Classic</p>
<div class="tabs">
<button class="tab active" data-tab="副本" onclick="switchTab(this)">📦 躺本</button>
<button class="tab" data-tab="代拉" onclick="switchTab(this)">💰 代拉</button>
</div>
<div id="副本" class="panel active">
<div class="checkbox-group">
<div class="checkbox-item" onclick="toggle(this)"><span>飛空艇英靈</span><span>NT500</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
<div class="checkbox-item" onclick="toggle(this)"><span>博物島英靈</span><span>NT300</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
<div class="checkbox-item" onclick="toggle(this)"><span>迷蹤島英靈</span><span>NT100</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
<div class="checkbox-item" onclick="toggle(this)"><span>星座塔Ⅵ</span><span>NT800</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
<div class="checkbox-item" onclick="toggle(this)"><span>混亂噩夢</span><span>NT800</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
<div class="checkbox-item" onclick="toggle(this)"><span>12人英靈</span><span>NT100</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
<div class="checkbox-item" onclick="toggle(this)"><span>神諭11</span><span>NT100</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,-1)">-</span><span class="qty-num">0</span><span class="qty-btn" onclick="event.stopPropagation();qty(this,1)">+</span></div>
</div>
<div class="total-box">總計: <span id="total-amount">0</span> 元</div>
<input type="text" id="lineid" placeholder="LINE ID（會馬上聯係您）">
<button class="btn" onclick="submitOrder()">🚀 提交訂單</button>
</div>
<div id="代拉" class="panel">
<div class="ratio-grid" id="ratio-grid"></div>
<input type="text" id="lineid2" placeholder="LINE ID（會馬上聯係您）" style="margin-top:12px;">
<input type="file" id="screenshot" accept="image/*">
<p style="color:#888;font-size:13px;margin-bottom:8px;">上傳需要代拉的物品截圖即可</p>
<button class="btn" onclick="submitBuy()">🚀 提交訂單</button>
</div>
</div>
<script>
const PRICES={'飛空艇英靈':500,'博物島英靈':300,'迷蹤島英靈':100,'星座塔Ⅵ':800,'混亂噩夢':800,'12人英靈':100,'神諭11':100};
function switchTab(btn){document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));document.getElementById(btn.dataset.tab).classList.add('active');btn.classList.add('active');if(btn.dataset.tab==='代拉')loadRatio();}
function toggle(item){item.classList.toggle('checked');const q=item.querySelector('.qty-num');if(item.classList.contains('checked')&&q.textContent==='0')q.textContent='1';updateTotal();}
function qty(btn,delta){const item=btn.closest('.checkbox-item');const q=item.querySelector('.qty-num');let n=parseInt(q.textContent)+delta;if(n<0)n=0;if(n>10)n=10;q.textContent=n;if(n>0)item.classList.add('checked');else item.classList.remove('checked');updateTotal();}
function updateTotal(){let t=0;document.querySelectorAll('#副本 .checkbox-item.checked').forEach(i=>{const name=i.querySelector('span:first-child').textContent;t+=(PRICES[name]||0)*parseInt(i.querySelector('.qty-num').textContent);});document.getElementById('total-amount').textContent=t;}
async function loadRatio(){const r=await fetch('/api/ratio');const d=await r.json();const keys=['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','9-10'];document.getElementById('ratio-grid').innerHTML=keys.map(k=>`<div class="ratio-item"><span>${k}E</span><span>${d[k]||'--'}</span></div>`).join('');}
async function submitOrder(){const items=[];document.querySelectorAll('#副本 .checkbox-item.checked').forEach(i=>{const name=i.querySelector('span:first-child').textContent;const qty=parseInt(i.querySelector('.qty-num').textContent)||0;for(let n=0;n<qty;n++)items.push(name+'-'+PRICES[name]);});const lineid=document.getElementById('lineid').value.trim();if(!lineid)return alert('請輸入LINE ID');if(items.length===0)return alert('請選擇至少一個副本');await fetch('/api/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'副本',items,lineid})});alert('✅ 提交成功！');document.querySelectorAll('.checkbox-item').forEach(i=>i.classList.remove('checked'));document.querySelectorAll('.qty-num').forEach(q=>q.textContent='0');document.getElementById('lineid').value='';updateTotal();}
async function submitBuy(){const lineid=document.getElementById('lineid2').value.trim();if(!lineid)return alert('請輸入LINE ID');await fetch('/api/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'代拉',items:[],lineid})});alert('✅ 提交成功！');document.getElementById('lineid2').value='';}
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
.btn-complete { padding: 8px 14px; background: #22c55e; color: white; border: none; border-radius: 8px; cursor: pointer; margin-right: 6px; }
.btn-paid { padding: 8px 14px; background: #fbbf24; color: #1a1a2e; border: none; border-radius: 8px; cursor: pointer; margin-right: 6px; font-weight: 600; }
.btn-paid-done { background: #666; color: #aaa; cursor: default; }
.btn-delete { padding: 8px 14px; background: rgba(239,68,68,0.2); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); border-radius: 8px; cursor: pointer; }
.order-card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 14px; margin-bottom: 10px; border-radius: 12px; }
.order-items { margin: 8px 0; }
.order-btns { margin-top: 10px; }
.stats { display: flex; gap: 15px; margin-bottom: 20px; }
.stat-item { background: rgba(255,255,255,0.05); padding: 12px 20px; border-radius: 10px; text-align: center; min-width: 100px; }
.stat-num { font-size: 24px; font-weight: 700; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 15px; }
.ratio-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.ratio-item { display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(255,255,255,0.05); border-radius: 8px; }
.ratio-item input { width: 80px; padding: 6px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #fff; border-radius: 6px; }
.btn-ratio { width: 100%; padding: 14px; background: #e6b800; color: #1a1a2e; border: none; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 15px; }
.pending-title { color: #fbbf24; }
.history-title { color: #4ade80; }
</style></head>
<body>
<div class="container">
<h1>⚙️ RO管理後台</h1>
<div class="toolbar">
<button class="toolbar-btn active" onclick="showPending()">⏳ 待辦</button>
<button class="toolbar-btn" onclick="showHistory()">📋 歷史</button>
<button class="toolbar-btn" onclick="showRatio()">💰 代拉比例</button>
</div>
<div class="stats" id="stats">
<div class="stat-item stat-pending"><div class="stat-num" id="stat-pending">0</div><div>待辦事項</div></div>
</div>
<div id="ratio-section" style="display:none;">
<h2 class="section-title">💰 代拉比例設置</h2>
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
<div id="pending-section">
<h2 class="section-title">📋 待辦事項</h2>
<div id="pending-orders"></div>
</div>
<div id="history-section" style="display:none;">
<h2 class="section-title">📋 歷史記錄</h2>
<div id="history-orders"></div>
</div>

ADMIN_HTML = ADMIN_HTML.replace('{{ADMIN_CONTENT}}', '''
async function deleteOrder(id){ if(!confirm('確定？'))return; await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'delete'})}); loadOrders(); }
function showPending(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active'));event.target.classList.add('active'); document.getElementById('stats').style.display='flex'; document.getElementById('pending-section').style.display='block'; document.getElementById('history-section').style.display='none'; loadOrders(); }
function showHistory(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active'));event.target.classList.add('active'); document.getElementById('stats').style.display='none'; document.getElementById('pending-section').style.display='none'; document.getElementById('history-section').style.display='block'; loadOrders(); }
function showRatio(){ document.querySelectorAll('.toolbar-btn').forEach(b=>b.classList.remove('active'));event.target.classList.add('active'); document.getElementById('stats').style.display='none'; document.getElementById('pending-section').style.display='none'; document.getElementById('history-section').style.display='none'; fetch('/api/ratio').then(r=>r.json()).then(d=>{['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','9-10'].forEach(k=>document.getElementById('ratio-'+k).value=d[k]||'');}); }
async function saveRatio(){ const r={};['0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','9-10'].forEach(k=>r[k]=document.getElementById('ratio-'+k).value); await fetch('/api/ratio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(r)}); alert('✅ 已保存！'); }
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
            elif action == 'unpaid':
                o['paid'] = False
            elif action == 'delete':
                orders.remove(o)
            break
    return jsonify({'ok': True})