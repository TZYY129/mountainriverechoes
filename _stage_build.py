# -*- coding: utf-8 -*-
"""搭建维吾尔族单民族版打包源（独立目录 build_uyghur/，不动主工作副本）。
并在其中对 mountainriverechoes.py 做冻结环境适配与单民族裁剪。
"""
import io, os, re, shutil, sys, glob

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = r'C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes'
DST = r'C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\build_uyghur'

if os.path.isdir(DST):
    shutil.rmtree(DST)
os.makedirs(DST)

log = []


def cp(src, dst=None, isdir=False):
    s = os.path.join(SRC, src)
    if not os.path.exists(s):
        log.append('  跳过(不存在): ' + src)
        return
    d = os.path.join(DST, dst or src)
    os.makedirs(os.path.dirname(d), exist_ok=True)
    if isdir:
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)
    log.append('  复制: ' + (dst or src))


# ---------- 1. 复制源码 ----------
cp('webui/mountainriverechoes.py')
cp('webui/templates', 'webui/templates', True)
cp('webui/ethnos_cache/e03_维吾尔族.json')
cp('webui/ethnos_cache/index_snapshot.json')
cp('musicdl', 'musicdl', True)
cp('wx_video_album.py')
cp('import_bili_favlist.py')
cp('mountain_echo.ico')
cp('LICENSE')
cp('README.md')

# 清掉模板目录里的备份
for f in glob.glob(os.path.join(DST, 'webui', 'templates', '_original*')):
    os.remove(f)

# ---------- 2. 打补丁 ----------
PY = os.path.join(DST, 'webui', 'mountainriverechoes.py')
s = open(PY, encoding='utf-8').read()
original_len = len(s)
patches = []


def rep(old, new, tag, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit('!! 补丁 [%s] 期望命中 %d 次，实际 %d 次' % (tag, count, n))
    s = s.replace(old, new, count)
    patches.append(tag)


# (a) BASE_DIR：冻结后优先用 exe 同级目录，保证 JSON 可被用户直接替换
rep(
    "BASE_DIR = Path(__file__).resolve().parent.parent",
    ("# [单民族分装版] 冻结环境适配：优先使用 exe 同级目录，用户可直接替换 webui/ethnos_cache 下的 JSON\n"
     "if getattr(sys, 'frozen', False):\n"
     "    _exe_dir = Path(sys.executable).resolve().parent\n"
     "    if (_exe_dir / 'webui' / 'ethnos_cache').is_dir():\n"
     "        BASE_DIR = _exe_dir\n"
     "    else:\n"
     "        BASE_DIR = Path(getattr(sys, '_MEIPASS', _exe_dir))\n"
     "else:\n"
     "    BASE_DIR = Path(__file__).resolve().parent.parent"),
    'BASE_DIR 冻结适配')

# (b) 模板目录改为走 BASE_DIR，避免 __file__ 在冻结环境指错
rep(
    "app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent / 'templates'))",
    "app = Flask(__name__, template_folder=str(BASE_DIR / 'webui' / 'templates'))",
    'template_folder 冻结适配')

# (c) 单民族裁剪：只保留维吾尔族（key 固定 e03）
rep(
    "ETHNIC_BY_KEY = {g['key']: g for g in ETHNIC_GROUPS}",
    ("# [单民族分装版] 只保留维吾尔族（key 固定 e03，不可按数组下标重算）\n"
     "ETHNIC_GROUPS = [g for g in ETHNIC_GROUPS if g['key'] == 'e03']\n"
     "ETHNIC_BY_KEY = {g['key']: g for g in ETHNIC_GROUPS}\n"
     "assert len(ETHNIC_GROUPS) == 1 and ETHNIC_GROUPS[0]['name'] == '维吾尔族', '单民族裁剪失败'"),
    'ETHNIC_GROUPS 裁剪为 e03')

# (d) 景颇优先排序里写死的 e26 要去掉
rep(
    "    order = ['e26'] + [g['key'] for g in ETHNIC_GROUPS if g['key'] != 'e26']",
    "    order = [g['key'] for g in ETHNIC_GROUPS]",
    '去掉写死的 e26 排序')

# (e) 文件签名列表里去掉 han
rep(
    "    for key in [g['key'] for g in ETHNIC_GROUPS] + ['han']:",
    "    for key in [g['key'] for g in ETHNIC_GROUPS]:",
    '签名列表去掉 han')

# (f) 启动后自动打开浏览器
rep(
    "if __name__ == '__main__':\n"
    "    print(f'[mountainriverechoes] serving at http://{HOST}:{PORT}  (downloads -> {DOWNLOAD_DIR})', flush=True)",
    ("if __name__ == '__main__':\n"
     "    print(f'[mountainriverechoes] serving at http://{HOST}:{PORT}  (downloads -> {DOWNLOAD_DIR})', flush=True)\n"
     "    # [单民族分装版] 启动后延迟自动打开浏览器，避免用户双击 exe 后以为没反应\n"
     "    def _open_browser():\n"
     "        import time as _t, webbrowser as _wb\n"
     "        _t.sleep(1.5)\n"
     "        try:\n"
     "            _wb.open(f'http://{HOST}:{PORT}')\n"
     "        except Exception:\n"
     "            pass\n"
     "    threading.Thread(target=_open_browser, daemon=True).start()"),
    '启动后自动打开浏览器')

open(PY, 'w', encoding='utf-8', newline='\n').write(s)

# ---------- 3. 校验补丁后的文件可编译 ----------
import py_compile
try:
    py_compile.compile(PY, doraise=True)
    log.append('  语法校验: 通过')
except Exception as e:
    raise SystemExit('!! 补丁后语法错误: %s' % e)

print('=== 打包源已就绪: %s ===' % DST)
print('\n'.join(log))
print()
print('已应用补丁:')
for p in patches:
    print('  -', p)
print()
print('mountainriverechoes.py: %d -> %d 字节' % (original_len, len(s.encode('utf-8'))))
print()
print('=== build_uyghur 结构 ===')
for root, dirs, files in os.walk(DST):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    rel = os.path.relpath(root, DST)
    depth = 0 if rel == '.' else rel.count(os.sep) + 1
    if depth > 2:
        continue
    print('  ' * depth + (os.path.basename(root) if rel != '.' else DST) + '/')
    for f in files[:6]:
        print('  ' * (depth + 1) + f)
