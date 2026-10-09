import json, sys, urllib.request, urllib.error

BASE = "http://127.0.0.1:8766"
urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler({})))


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


print("=== 1) /api/ethnos  民族分组总览 ===")
st, b = get("/api/ethnos")
d = json.loads(b.decode("utf-8"))
print("HTTP", st, "| total =", d.get("total"), "| done =", d.get("done"), "| building =", d.get("building"))
groups = d.get("groups") or []
print("groups 条数:", len(groups))
print("字段样例:", list(groups[0].keys()) if groups else "无")
for g in groups[:3]:
    print("   ", g)
dai = [g for g in groups if "傣" in str(g.get("name"))]
print("傣族条目:", dai)
han = d.get("han")
print("汉族民间小调:", han)

print()
group_key = dai[0]["key"] if dai else "e16"
print(f"=== 2) /api/ethnos/custom?group={group_key}  单民族歌单详情 ===")
st, b = get(f"/api/ethnos/custom?group={group_key}")
print("HTTP", st, " 字节数:", len(b))
try:
    dc = json.loads(b.decode("utf-8"))
    if isinstance(dc, dict):
        print("顶层字段:", list(dc.keys()))
        for k, v in dc.items():
            if isinstance(v, list):
                print(f"   {k}: list[{len(v)}]")
                if v and isinstance(v[0], dict):
                    print(f"      首项字段: {list(v[0].keys())}")
                    print(f"      首项: {json.dumps(v[0], ensure_ascii=False)[:220]}")
            else:
                print(f"   {k}: {str(v)[:120]}")
except Exception as e:
    print("解析失败:", e, b[:300])

print()
print("=== 3) /api/sources  可用音源 ===")
st, b = get("/api/sources")
print("HTTP", st, "->", b.decode("utf-8", "replace")[:400])

print()
print("=== 4) 磁盘曲库统计（直接读 JSON，最可靠）===")
import os
EC = r"C:\Users\20318\WorkBuddy\2026-10-09-20-30-45\mountainriverechoes\webui\ethnos_cache"
tot_songs = tot_groups = 0
rows = []
for fn in sorted(os.listdir(EC)):
    if not fn.endswith(".json") or fn == "index_snapshot.json":
        continue
    p = os.path.join(EC, fn)
    try:
        with open(p, "r", encoding="utf-8") as f:
            j = json.load(f)
        n = j.get("count")
        if n is None:
            n = len(j.get("songs") or j.get("tracks") or [])
        rows.append((fn, n))
        tot_songs += n
        tot_groups += 1
    except Exception as e:
        rows.append((fn, f"读取失败 {e}"))
print(f"库文件数: {tot_groups}   曲目总数: {tot_songs}")
for fn, n in rows:
    if "傣" in fn or "德昂" in fn or "阿昌" in fn or "土族" in fn or "汉族" in fn:
        print(f"   {fn}: {n} 首")

print()
print("VERIFY_DONE")
