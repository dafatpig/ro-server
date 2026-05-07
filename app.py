#!/usr/bin/env python3
"""RO專業帶本代拉"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

orders = []
ratio = {f'{i}-{i+1}E': '' for i in range(10)}
order_id = 1

# 副本價格
PRICES = {'飛空艇英靈': 500, '博物島英靈': 300, '迷蹤島英靈': 100, '星座塔Ⅵ': 800, '混亂時空噩夢': 800, '12人英靈': 100, '神諭11': 100}
TWD_CNY = 0.217

# 客戶版HTML
CLIENT_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RO專業帶本代拉</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: #fff; min-height: 100vh; padding: 16px; }
.container { max-width: 480px; margin: 0 auto; }
h1 { text-align: center; font-size: 26px; font-weight: 700; background: linear-gradient(90deg, #ffd700, #e6b800); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { text-align: center; color: #888; font-size: 13px; margin-bottom: 16px; }
.tabs { display: flex; gap: 8px; margin-bottom: 16px; }
.tab { flex: 1; padding: 12px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #888; font-size: 14px; font-weight: 600; border-radius: 10px; text-align: center; cursor: pointer; }
.tab.active { background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; }
.panel { display: none; }
.panel.active { display: block; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 12px 14px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
.item.checked { background: linear-gradient(135deg, #b8860b, #daa520); border-color: #ffd700; }
.item-name { font-size: 14px; }
.item-price { font-size: 13px; color: #aaa; }
.item.checked .item-price { color: #fff; }
.qty-box { display: none; align-items: center; gap: 4px; }
.item.checked .qty-box { display: flex; }
.qty-btn { width: 24px; height: 24px; background: rgba(255,255,255,0.25); border: none; border-radius: 6px; color: #fff; font-size: 14px; font-weight: 700; cursor: pointer; }
.qty-num { min-width: 18px; text-align: center; font-size: 13px; font-weight: 700; }
.total { text-align: center; font-size: 16px; font-weight: 700; color: #ffd700; margin: 12px 0; }
.input { width: 100%; padding: 12px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #fff; border-radius: 8px; font-size: 14px; margin-bottom: 10px; }
.input::placeholder { color: #666; }
textarea.input { min-height: 70px; resize: none; }
.submit { width: 100%; padding: 14px; background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border: none; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; }
.submit:active { transform: scale(0.98); }
.ratio-row { display: flex; justify-content: space-between; padding: 8px 12px; background: rgba(255,255,255,0.04); border-radius: 6px; margin-bottom: 6px; font-size: 13px; }
.ratio-row span:first-child { color: #888; }
.ratio-row span:last-child { color: #4ade80; font-weight: 600; }
.upload { padding: 16px; background: rgba(255,255,255,0.04); border: 2px dashed rgba(255,255,255,0.15); border-radius: 10px; text-align: center; margin-bottom: 10px; }
.upload input { display: none; }
.upload-label { color: #888; font-size: 13px; cursor: pointer; }
.hint { color: #666; font-size: 12px; margin-top: 4px; margin-bottom: 10px; }
</style>
</head>
<body>
<div class="container">
<h1>⚔️ RO專業帶本代拉</h1>
<p class="subtitle">仙境傳說RO守護永恆的愛 Classic</p>
<div class="tabs">
<button class="tab active" data-t="dungeon" onclick="tn(this)">📦 躺本</button>
<button class="tab" data-t="buy" onclick="tn(this)">💰 代拉</button>
</div>

<div id="dungeon" class="panel active">
<div class="items">
<div class="item" onclick="tk(this)" data-n="飛空艇英靈"><span class="item-name">飛空艇英靈</span><span class="item-price">NT500</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
<div class="item" onclick="tk(this)" data-n="博物島英靈"><span class="item-name">博物島英靈</span><span class="item-price">NT300</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
<div class="item" onclick="tk(this)" data-n="迷蹤島英靈"><span class="item-name">迷蹤島英靈</span><span class="item-price">NT100</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
<div class="item" onclick="tk(this)" data-n="星座塔Ⅵ"><span class="item-name">星座塔Ⅵ</span><span class="item-price">NT800</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
<div class="item" onclick="tk(this)" data-n="混亂時空噩夢"><span class="item-name">混亂時空噩夢</span><span class="item-price">NT800</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
<div class="item" onclick="tk(this)" data-n="12人英靈"><span class="item-name">12人英靈</span><span class="item-price">NT100</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
<div class="item" onclick="tk(this)" data-n="神諭11"><span class="item-name">神諭11</span><span class="item-price">NT100</span><div class="qty-box"><button class="qty-btn" onclick="ev.stopPropagation();cg(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="ev.stopPropagation();cg(this,1)">+</button></div></div>
</div>
<div class="total">總計：<span id="tt">0</span> 元</div>
<textarea class="input" id="note" placeholder="選填，可以備註時間要求"></textarea>
<input class="input" id="lineid" placeholder="必填，提交後馬上聯繫您">
<button class="submit" onclick="sb()">🚀 提交訂單</button>
</div>

<div id="buy" class="panel">
<div id="ratio"></div>
<div class="upload"><input type="file" id="img" accept="image/*"><label class="upload-label" for="img">📎 點擊上傳圖片</label></div>
<p class="hint">上傳需要代拉的物品圖片即可，馬上為您拉掉</p>
<input class="input" id="lineid2" placeholder="必填，提交後馬上聯繫您">
<button class="submit" onclick="sb2()">🚀 提交訂單</button>
</div>
</div>

<script>
const P = ''' + str(PRICES) + ''';
let rd = {};

async function lr() {
    let r = await fetch('/api/ratio');
    rd = await r.json();
    let h = '';
    for (let i = 0; i <= 9; i++) h += '<div class="ratio-row"><span>' + i + '-' + (i+1) + 'E</span><span>' + (rd[i + '-' + (i+1) + 'E'] || '--') + '</span></div>';
    document.getElementById('ratio').innerHTML = h;
}

function tn(b) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    b.classList.add('active');
    document.getElementById(b.dataset.t).classList.add('active');
    if (b.dataset.t === 'buy') lr();
}

function tk(el) {
    el.classList.toggle('checked');
    if (el.classList.contains('checked') && el.querySelector('.qty-num').textContent === '0') el.querySelector('.qty-num').textContent = '1';
    ut();
}

function cg(btn, d) {
    let el = btn.closest('.item');
    let n = parseInt(el.querySelector('.qty-num').textContent) + d;
    if (n < 0) n = 0;
    if (n > 10) n = 10;
    el.querySelector('.qty-num').textContent = n;
    if (n === 0) el.classList.remove('checked');
    ut();
}

function ut() {
    let t = 0;
    document.querySelectorAll('#dungeon .item.checked').forEach(el => t += (P[el.dataset.n] || 0) * parseInt(el.querySelector('.qty-num').textContent));
    document.getElementById('tt').textContent = t;
}

async function sb() {
    let items = [];
    document.querySelectorAll('#dungeon .item.checked').forEach(el => {
        let n = parseInt(el.querySelector('.qty-num').textContent);
        for (let i = 0; i < n; i++) items.push(el.dataset.n);
    });
    let lid = document.getElementById('lineid').value.trim();
    let note = document.getElementById('note').value.trim();
    if (!lid) return alert('請輸入 LINE ID');
    if (items.length === 0) return alert('請選擇副本');
    await fetch('/api/order', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ type: '帶本', items, lineid: lid, note }) });
    alert('✅ 提交成功！');
    document.querySelectorAll('.item').forEach(el => el.classList.remove('checked'));
    document.querySelectorAll('.qty-num').forEach(el => el.textContent = '0');
    document.getElementById('lineid').value = '';
    document.getElementById('note').value = '';
    ut();
}

async function sb2() {
    let lid = document.getElementById('lineid2').value.trim();
    if (!lid) return alert('請輸入 LINE ID');
    await fetch('/api/order', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ type: '代拉', items: [], lineid: lid, note: '' }) });
    alert('✅ 提交成功！');
    document.getElementById('lineid2').value = '';
}

lr();
</script>
</body>
</html>'''

# 管理版HTML
ADMIN_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RO管理後台</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: #fff; min-height: 100vh; }
.container { max-width: 600px; margin: 0 auto; padding: 16px; }
h1 { text-align: center; font-size: 24px; font-weight: 700; color: #4ade80; margin-bottom: 16px; }
.tabs { display: flex; gap: 6px; margin-bottom: 16px; }
.tab { flex: 1; padding: 10px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); color: #888; font-size: 13px; font-weight: 600; border-radius: 8px; text-align: center; cursor: pointer; }
.tab.active { background: #e6b800; color: #1a1a2e; }
.count { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 12px; }
.count span:first-child { color: #fbbf24; font-size: 14px; }
.count-num { font-size: 20px; font-weight: 700; color: #fbbf24; }
.panel { display: none; }
.panel.active { display: block; }
.card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 14px; border-radius: 10px; margin-bottom: 10px; }
.card-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.card-type { font-size: 14px; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
.card-type.d { background: rgba(139,92,246,0.2); color: #a78bfa; }
.card-type.b { background: rgba(34,197,94,0.2); color: #4ade80; }
.card-time { color: #777; font-size: 12px; }
.card-items { margin: 8px 0; }
.tag { display: inline-block; background: rgba(230,184,0,0.15); color: #ffd700; padding: 3px 8px; border-radius: 4px; margin: 0 4px 4px 0; font-size: 12px; }
.card-price { color: #fbbf24; font-size: 14px; font-weight: 600; margin: 8px 0; }
.card-line { color: #4ade80; font-size: 13px; }
.card-note { color: #888; font-size: 12px; font-style: italic; margin-top: 6px; }
.btns { display: flex; gap: 6px; margin-top: 10px; }
.btn { padding: 8px 12px; border: none; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-c { background: #22c55e; color: #fff; }
.btn-p { background: #fbbf24; color: #1a1a2e; }
.btn-pdone { background: #444; color: #888; cursor: default; }
.btn-d { background: rgba(239,68,68,0.2); color: #fca5a5; }
.grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.row { display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; background: rgba(255,255,255,0.04); border-radius: 6px; }
.row label { color: #777; font-size: 12px; }
.row input { width: 60px; padding: 4px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 4px; text-align: center; font-size: 12px; }
.save { width: 100%; padding: 12px; background: #e6b800; color: #1a1a2e; border: none; border-radius: 8px; font-size: 14px; font-weight: 700; cursor: pointer; margin-top: 12px; }
.empty { text-align: center; color: #555; padding: 20px; }
</style>
</head>
<body>
<div class="container">
<h1>⚙️ RO管理後台</h1>
<div class="tabs">
<button class="tab active" data-t="pending" onclick="tn(this)">⏳ 待辦</button>
<button class="tab" data-t="history" onclick="tn(this)">📋 記錄</button>
<button class="tab" data-t="ratio" onclick="tn(this)">💰 代拉比例</button>
</div>

<div id="pending" class="panel active">
<div class="count"><span>待辦事項</span><span class="count-num" id="pc">0</span></div>
<div id="plist"></div>
</div>

<div id="history" class="panel">
<div id="hlist"></div>
</div>

<div id="ratio" class="panel">
<div class="grid">
<div class="row"><label>0-1E：</label><input id="r0-1"></div>
<div class="row"><label>1-2E：</label><input id="r1-2"></div>
<div class="row"><label>2-3E：</label><input id="r2-3"></div>
<div class="row"><label>3-4E：</label><input id="r3-4"></div>
<div class="row"><label>4-5E：</label><input id="r4-5"></div>
<div class="row"><label>5-6E：</label><input id="r5-6"></div>
<div class="row"><label>6-7E：</label><input id="r6-7"></div>
<div class="row"><label>7-8E：</label><input id="r7-8"></div>
<div class="row"><label>8-9E：</label><input id="r8-9"></div>
<div class="row"><label>9-10E：</label><input id="r9-10"></div>
</div>
<button class="save" onclick="sv()">💾 儲存</button>
</div>
</div>

<script>
const C = 0.217;
const P = ''' + str(PRICES) + ''';

async function lo() {
    let d = await (await fetch('/api/orders')).json();
    let all = d.orders || [];
    
    let pending = all.filter(o => !o.done).sort((a,b) => b.id - a.id);
    let history = all.filter(o => o.done);
    let unpaid = history.filter(o => !o.paid).sort((a,b) => b.id - a.id);
    let paid = history.filter(o => o.paid).sort((a,b) => b.id - a.id);
    history = [...unpaid, ...paid];
    
    document.getElementById('pc').textContent = pending.length;
    document.getElementById('plist').innerHTML = pending.length ? pending.map(o => rc(o,true)).join('') : '<div class="empty">���無���辦事項</div>';
    document.getElementById('hlist').innerHTML = history.length ? history.map(o => rc(o,false)).join('') : '<div class="empty">暫無記錄</div>';
}

function rc(o, sh) {
    let tc = o.type === '帶本' ? 'd' : 'b';
    let ih = '';
    if (o.items && o.items.length) {
        let cnt = {};
        o.items.forEach(i => cnt[i] = (cnt[i] || 0) + 1);
        ih = '<div class="card-items">' + Object.entries(cnt).map(([n,q]) => '<span class="tag">' + n + 'x' + q + '</span>').join('') + '</div>';
    }
    let ph = '';
    if (o.type === '帶本' && o.items && o.items.length) {
        let twd = o.items.reduce((s,i) => s + (P[i]||0), 0);
        ph = '<div class="card-price">' + twd + ' 元 ≈ ' + Math.floor(twd*C) + ' 人民币</div>';
    }
    let nh = o.note ? '<div class="card-note">備註：' + o.note + '</div>' : '';
    let bh = '';
    if (sh) {
        bh = '<div class="btns"><button class="btn btn-c" onclick="cp(' + o.id + ')">✅ 完成</button><button class="btn btn-p" onclick="pd(' + o.id + ')">❌ 未收款</button><button class="btn btn-d" onclick="dl(' + o.id + ')">🗑️</button></div>';
    } else {
        let pb = o.paid ? '<span style="color:#666;font-size:12px;margin-right:6px;">已收款</span>' : '<button class="btn btn-p" onclick="pd(' + o.id + ')">❌ 未收款</button>';
        bh = '<div class="btns">' + pb + '<button class="btn btn-d" onclick="dl(' + o.id + ')">🗑️</button></div>';
    }
    return '<div class="card"><div class="card-head"><span class="card-type ' + tc + '">' + o.type + '</span><span class="card-time">' + o.time + '</span></div>' + ih + ph + '<div class="card-line">LINE: ' + (o.lineid||'--') + '</div>' + nh + bh + '</div>';
}

async function cp(id) { await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'complete'})}); lo(); }
async function pd(id) { await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'paid'})}); lo(); }
async function dl(id) { if(!confirm('確定？'))return; await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,action:'delete'})}); lo(); }

function tn(b) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    b.classList.add('active');
    document.getElementById(b.dataset.t).classList.add('active');
    if(b.dataset.t==='ratio')lr();
    if(b.dataset.t==='pending'||b.dataset.t==='history')lo();
}

async function lr() {
    let d = await (await fetch('/api/ratio')).json();
    for(let i=0;i<=9;i++) document.getElementById('r'+i+'-'+(i+1)).value = d[i+'-'+(i+1)+'E']||'';
}

async function sv() {
    let r={};
    for(let i=0;i<=9;i++) r[i+'-'+(i+1)+'E'] = document.getElementById('r'+i+'-'+(i+1)).value;
    await fetch('/api/ratio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(r)});
    alert('✅ 已儲存！');
}

lo(); setInterval(lo, 15000);
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
    return jsonify({'orders': orders})

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
        'type': data.get('type', '帶本'),
        'items': data.get('items', []),
        'lineid': data.get('lineid', ''),
        'note': data.get('note', ''),
        'done': False,
        'paid': False,
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
            if action == 'complete': o['done'] = True
            elif action == 'paid': o['paid'] = True
            elif action == 'delete': orders.remove(o)
            break
    return jsonify({'ok': True})