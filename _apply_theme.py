# -*- coding: utf-8 -*-
"""一次性把维吾尔族主题的文案/结构改动应用到模板（避免并行编辑互相覆盖）。"""
import io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.chdir(r'C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes')
P = 'webui/templates/mountainriverechoes.html'
s = open(P, encoding='utf-8').read()
orig = s

REPL = [
    # 1) <title>
    ('<title>山河回响 听见56个民族的音乐</title>',
     '<title>山河回响 · 维吾尔族｜十二木卡姆典藏</title>'),
    # 2) 侧栏品牌
    ('<div><b>山河回响</b><small>听见56个民族的音乐</small></div>',
     '<div><b>山河回响 · 维吾尔族</b><small>ئۇيغۇر مۇقامى · 木卡姆典藏</small></div>'),
    # 3) 发现页 Hero
    ('''        <div class="hero">
          <h2>在这里，听见全世界</h2>
          <p>聚合 · 搜索 / 试听 / 歌词 / </p>
          <div class="hot" id="hot-words"></div>
        </div>''',
     '''        <div class="hero">
          <span class="uyg">ئۇيغۇر مۇقامى · 十二木卡姆</span>
          <h2>维吾尔族音乐地图</h2>
          <p>十二木卡姆 12 套全收录 · 刀郎木卡姆 9 套全收录<br>覆盖木卡姆套曲、达斯坦、麦西来甫、南北疆民歌与器乐曲</p>
          <div class="mk-badges">
            <span class="mk-badge on"><b>12</b>十二木卡姆</span>
            <span class="mk-badge on"><b>9</b>刀郎木卡姆</span>
            <span class="mk-badge">哈密木卡姆</span>
            <span class="mk-badge">吐鲁番木卡姆</span>
            <span class="mk-badge"><b>2293</b>首馆藏</span>
          </div>
          <div class="hot" id="hot-words"></div>
        </div>'''),
    # 4) 民族专区页标题
    ('<div class="page-title">民族音乐专区<small>56 个民族歌单 · 点击卡片进入</small></div>',
     '<div class="page-title">维吾尔族音乐专区<small>十二木卡姆 · 刀郎木卡姆 · 麦西来甫 · 民歌</small></div>'),
    # 5) 索引页 Hero
    ('''            <h2>五十六个民族 · 音乐地图</h2>
            <p>遍历多音源聚合搜索，为 56个少数民族逐一构建民族音乐歌单（民歌 / 特色曲种 / 民族语言歌曲）</p>''',
     '''            <h2>维吾尔族 · 十二木卡姆典藏</h2>
            <p>全库 2293 首：十二木卡姆 12 套（每套 1.5–2.2 小时完整录音）· 刀郎木卡姆 9 套（1997 学术录音版 + 现代录音棚版双版本）· 麦西来甫舞曲 · 达斯坦 · 南北疆民歌与器乐</p>'''),
    # 6) 民族卡片网格：不再强制塞入「汉族民间小调」
    ("applyOrder([...new Set([...order, '汉族民间小调'])], store.get('cm_order_ethcards', ETHCARD_ORDER_DEFAULT))",
     "applyOrder([...new Set([...order, '维吾尔族'])], store.get('cm_order_ethcards', ETHCARD_ORDER_DEFAULT))"),
    # 7) 索引副标题
    ("${(d.stats || {}).songs || 0} 首歌曲 · ${(d.stats || {}).ethnos_playlists || 56} 个民族歌单",
     "${(d.stats || {}).songs || 0} 首歌曲 · 维吾尔族曲库"),
]

fail = []
for old, new in REPL:
    n = s.count(old)
    if n != 1:
        fail.append('期望命中 1 次，实际 %d 次: %s' % (n, old[:60]))
        continue
    s = s.replace(old, new, 1)

if fail:
    print('!! 以下替换未通过校验，已放弃写入：')
    for f in fail:
        print('  ', f)
    sys.exit(1)

tmp = P + '.tmp'
open(tmp, 'w', encoding='utf-8').write(s)
os.replace(tmp, P)
print('已写入 %d 处替换' % len(REPL))
print('文件大小: %d -> %d' % (len(orig.encode('utf-8')), len(s.encode('utf-8'))))

# 复查
chk = open(P, encoding='utf-8').read()
for k in ['维吾尔族｜十二木卡姆典藏', '山河回响 · 维吾尔族', '维吾尔族音乐地图',
          '维吾尔族音乐专区', '维吾尔族 · 十二木卡姆典藏', '维吾尔族曲库', "ETHCARD_ORDER_DEFAULT = ['维吾尔族']"]:
    print('  %-34s %s' % (k, k in chk))
print('  剩余「56个民族」:', chk.count('56个民族'))
print('  剩余「五十六」:', chk.count('五十六'))
print('  #player 元素存在:', '#player' in chk)
