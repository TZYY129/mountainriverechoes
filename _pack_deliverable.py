# -*- coding: utf-8 -*-
"""把作业四件套打包成「姓名+学号.zip」。
用法: python _pack_deliverable.py 张三 20231234
产出: C:/Users/20318/WorkBuddy/2026-10-09-20-30-45/张三20231234.zip
"""
import io, os, sys, zipfile, time, json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'C:\Users\20318\WorkBuddy\2026-10-09-20-30-45'
MRE = os.path.join(ROOT, 'mountainriverechoes')
DIST = os.path.join(ROOT, 'build_uyghur', 'dist', 'MountainRiverEchoes-Uyghur')

name = sys.argv[1] if len(sys.argv) > 1 else '未命名'
sid = sys.argv[2] if len(sys.argv) > 2 else ''
stem = '%s%s' % (name, sid)
ZIP = os.path.join(ROOT, stem + '.zip')

# ---------- 源文件 ----------
SRC = [
    ('1_民族数据库JSON/e03_维吾尔族.json',
     os.path.join(MRE, 'webui', 'ethnos_cache', 'e03_维吾尔族.json')),
    ('2_UI页面/mountainriverechoes.html',
     os.path.join(MRE, 'webui', 'templates', 'mountainriverechoes.html')),
    ('3_数据库变动报告/维吾尔族曲库数据库变动总结报告.md',
     os.path.join(MRE, '维吾尔族曲库数据库变动总结报告.md')),
    ('3_数据库变动报告/维吾尔族曲库补充挖掘报告.md',
     os.path.join(MRE, '维吾尔族曲库补充挖掘报告.md')),
    ('3_数据库变动报告/维吾尔族入库执行报告.md',
     os.path.join(MRE, '维吾尔族入库执行报告.md')),
    ('3_数据库变动报告/维吾尔族补录专辑链接清单.md',
     os.path.join(MRE, '维吾尔族补录专辑链接清单.md')),
    ('3_数据库变动报告/维吾尔族UI页面设计说明.md',
     os.path.join(MRE, '维吾尔族UI页面设计说明.md')),
]

# 交付说明
doc = '''作业交付说明
=====================================

提交人：%s
学　号：%s
负责民族：维吾尔族
提交日期：%s

-------------------------------------
【本次交付的四个部分】
-------------------------------------
1_民族数据库JSON
    e03_维吾尔族.json
    路径对应项目内 webui/ethnos_cache/ 下的库文件。
    本次维护结果：曲目 2310 → 2293 首（净变化 −17：入库阶段新增 24 首，清洗阶段删除 41 条误收的无关条目）
    完整收录：十二木卡姆 12 套、刀郎木卡姆 9 套。

2_UI页面
    mountainriverechoes.html
    路径对应项目内 webui/templates/ 下的页面文件。
    设计主题：艾德莱斯绸 + 十二木卡姆，详见 3_数据库变动报告/维吾尔族UI页面设计说明.md

3_数据库变动报告
    维吾尔族曲库数据库变动总结报告.md      ← 主报告（增删统计·前后对比）
    维吾尔族曲库补充挖掘报告.md            ← 缺口分析
    维吾尔族入库执行报告.md                ← 入库明细
    维吾尔族补录专辑链接清单.md            ← 音源出处
    维吾尔族UI页面设计说明.md              ← 界面设计说明

4_exe安装包
    MountainRiverEchoes-Uyghur/
    解压后双击 MountainRiverEchoes-Uyghur.exe 即可运行，无需安装 Python。
    注意：exe 必须与 _internal 文件夹放在一起。
    曲库与界面文件已外置于 exe 同级 webui 目录，可直接替换 JSON 更新音源。

-------------------------------------
【关于「全栈开发专家 / 软件开发团队 / 高级开发工程师」】
-------------------------------------
本项目的单民族版封装环节在「软件开发团队」专家协作下完成。

-------------------------------------
【数据来源】
-------------------------------------
网易云音乐 / 酷我音乐 / 咪咕音乐 / B站 等公开音源聚合，仅供学习研究使用。
''' % (name, sid, time.strftime('%Y-%m-%d'))


def p(*a):
    print(' '.join(str(x) for x in a), flush=True)


p('打包目标:', ZIP)
total = 0
n = 0
t0 = time.time()

with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    # 交付说明
    z.writestr('%s/交付说明.txt' % stem, doc.encode('utf-8-sig'))
    # 固定 4 项
    for arc, src in SRC:
        if not os.path.exists(src):
            p('  !! 缺失:', src); continue
        z.write(src, '%s/%s' % (stem, arc))
        n += 1; total += os.path.getsize(src)
        p('  + %-46s %8.2f MB' % (arc, os.path.getsize(src) / 1024 / 1024))
    # exe 整个目录
    if os.path.isdir(DIST):
        for root, dirs, files in os.walk(DIST):
            for f in files:
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, DIST)
                z.write(fp, '%s/4_exe安装包/MountainRiverEchoes-Uyghur/%s' % (stem, rel))
                n += 1; total += os.path.getsize(fp)
        p('  + 4_exe安装包/MountainRiverEchoes-Uyghur/  (整目录)')
    else:
        p('  !! exe 目录不存在:', DIST)

p('')
p('文件数 %d  原始大小 %.1f MB  zip 大小 %.1f MB  耗时 %.1fs'
  % (n, total / 1024 / 1024, os.path.getsize(ZIP) / 1024 / 1024, time.time() - t0))
p('产出:', ZIP)
