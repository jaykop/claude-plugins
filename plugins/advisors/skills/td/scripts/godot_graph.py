#!/usr/bin/env python3
"""Godot 프로젝트의 모듈 의존 지도를 만든다 (TD 고문 구조 점검의 '모듈 의존' 범위). module_graph.py 가 엔진 종류를 보고 부른다.

읽기만 한다. 프로젝트·엔진 파일을 고치지 않고, 결과는 표준 출력으로만 낸다.

Godot 에는 언리얼의 Build.cs 같은 의존 선언이 없다. 그래서 '모듈'은 폴더로 정하고, 간선은 파일 안의 참조로 센다.
- 모듈: addons/<이름> 은 애드온 하나. 그 밖은 project.godot 가 있는 폴더 아래 --unit-depth 단계(기본 1) 폴더 하나.
  그 폴더 바로 아래 파일은 '(루트)' 모듈이다.
- 간선(참조 종류)
  - preload, extends 경로, extends class_name, class_name 사용, autoload 이름 사용 (.gd)
  - 동적 로드: load(), ResourceLoader.load(), GD.Load() 등 실행할 때 읽는 경로
  - 씬·리소스 참조: .tscn·.tres 의 [ext_resource] (uid 만 있으면 .uid 파일과 씬 머리의 uid 로 경로를 푼다)
  - 셰이더 include: .gdshader 의 #include
  - C# using: 다른 모듈이 선언한 namespace 를 using 하는 곳
  - 경로 문자열: 위에 들지 않는 "res://..." 글
- 에디터 전용 코드: EditorPlugin 같은 Editor* 클래스를 상속한 파일과 plugin.cfg 의 script.
  에디터 전용이 아닌 파일이 Editor* 클래스를 쓰거나 에디터 전용 파일을 참조하는 곳을 조건(감싼 if, #if TOOLS)과 함께 낸다.

내는 것 (마크다운)
- 모듈 표, 모듈 사이 간선 표(종류별 참조 수와 첫 위치), 다른 모듈이 많이 참조하는 파일, autoload 표
- 순환 의존(동적 로드와 경로 문자열은 뺀다), 에디터 전용 코드에 기대는 곳
- --layer 를 주면 층 규칙 위반, --layer-draft 를 주면 층 초안
- 가리키는 파일이 없는 res:// 경로, 해석 못 한 것

시간 상한에 걸리면 '검색 실패'로 적고 종료 코드 3 을 낸다. 0 건으로 읽지 않게 하기 위해서다.
"""

import os
import re
import sys

import module_graph as mg

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "scripts")))
import godot_project as gp  # noqa: E402

SCAN_EXT = {".gd", ".cs", ".tscn", ".tres", ".gdshader", ".gdshaderinc"}
RES_RE = re.compile(r"\"((?:res|uid)://[^\"]+)\"")
EXT_RES_RE = re.compile(r"^\[ext_resource\b([^\]]*)\]", re.M)
ATTR_RE = re.compile(r"(\w+)=\"([^\"]*)\"")
HEADER_UID_RE = re.compile(r"^\[gd_(?:scene|resource)\b[^\]]*\buid=\"(uid://[^\"]+)\"", re.M)
INCLUDE_RE = re.compile(r"^[ \t]*#include[ \t]+\"((?:res|uid)://[^\"]+)\"", re.M)
CLASS_RE = re.compile(r"^[ \t]*(?:@\w+(?:\([^)\n]*\))?[ \t]+)*class_name[ \t]+([A-Za-z_]\w*)", re.M)
NAMESPACE_RE = re.compile(r"^[ \t]*namespace[ \t]+([A-Za-z_][\w.]*)", re.M)
USING_RE = re.compile(r"^[ \t]*using[ \t]+(?:static[ \t]+)?([A-Za-z_][\w.]*)[ \t]*;", re.M)
EDITOR_BASE_GD = re.compile(r"^[ \t]*extends[ \t]+(Editor[A-Z]\w*)", re.M)
EDITOR_BASE_CS = re.compile(r"\bclass\s+\w+\s*:\s*(?:Godot\.)?(Editor[A-Z]\w*)")
EDITOR_USE = re.compile(r"(?<![\w.])(Editor[A-Z]\w*)(?!\w)")
GUARD_GD = re.compile(r"^[ \t]*(?:el)?if\b(.*)$")
LOAD_CALL = re.compile(r"(?:\bload|\bload_threaded_request|ResourceLoader\.\w+|GD\.Load(?:<[^>]*>)?)\s*\(\s*$")
# 순환 의존과 층 판정에서 빼는 참조 종류: 실행할 때만 읽거나, 무엇을 하는 글인지 모르는 것
LOOSE_KINDS = {"동적 로드", "경로 문자열"}


def walk(root, budget, max_depth=30):
    """(폴더, 파일 이름 목록). module_graph.walk 는 언리얼 폴더 이름(Content, Resources)을 건너뛰므로 따로 둔다."""
    stack = [(root, 0)]
    while stack:
        if not budget.ok():
            return
        path, depth = stack.pop()
        try:
            entries = list(os.scandir(path))
        except OSError:
            continue
        yield path, [e.name for e in entries if e.is_file(follow_symlinks=False)]
        if depth < max_depth:
            for e in entries:
                if e.is_dir(follow_symlinks=False) and e.name not in gp.GODOT_GENERATED_DIRS and not e.name.startswith("."):
                    stack.append((e.path, depth + 1))


def gd_guard(lines, no):
    """GDScript 줄(1부터)을 감싼 if·elif 조건들. 들여쓰기로 거슬러 올라간다."""
    text = lines[no - 1]
    indent = len(text) - len(text.lstrip())
    conds = []
    for k in range(no - 2, -1, -1):
        s = lines[k]
        if not s.strip():
            continue
        ind = len(s) - len(s.lstrip())
        if ind >= indent:
            continue
        indent = ind
        m = GUARD_GD.match(s)
        if m:
            conds.append(" ".join(m.group(1).rstrip(":").split())[:80])
        if ind == 0:
            break
    return " 그리고 ".join(reversed(conds))


def cs_guard(code, raw, pos):
    """C# 위치를 감싼 if 조건과 #if 전처리 조건."""
    conds = [c for s, e, c in mg.condition_spans(code) if s <= pos <= e]
    stack = []
    for m in re.finditer(r"^[ \t]*#(if|elif|else|endif)\b(.*)$", raw[:pos], re.M):
        kind = m.group(1)
        if kind == "if":
            stack.append("#if " + m.group(2).strip())
        elif kind in ("elif", "else") and stack:
            stack[-1] = "#{} {}".format(kind, m.group(2).strip()).strip()
        elif kind == "endif" and stack:
            stack.pop()
    return " 그리고 ".join(stack + conds)


def run(args):
    root = mg.norm(args.project_root)
    if not os.path.isdir(root):
        print("오류: 프로젝트 루트 폴더가 없다 — " + root)
        return 2
    if args.project_file:
        project_file = mg.norm(args.project_file if os.path.isabs(args.project_file) else os.path.join(root, args.project_file))
        if not os.path.isfile(project_file):
            print("오류: 프로젝트 파일이 없다 — " + args.project_file)
            return 2
    else:
        found = []
        for path, files in walk(root, mg.Budget(20), max_depth=3):
            if os.sep + "addons" not in path[len(root):] + os.sep and "project.godot" in files:
                found.append(os.path.join(path, "project.godot"))
        if len(found) != 1:
            print("오류: 프로젝트 파일(project.godot)을 정하지 못했다({} 개). --project-file 로 지정할 것".format(len(found)))
            return 2
        project_file = mg.norm(found[0])
    project_dir = os.path.dirname(project_file)
    addons_dir = os.path.join(project_dir, "addons")
    budget = mg.Budget(args.seconds)
    notes, failed = [], False
    facts = gp.project_facts(project_file)
    if "error" in facts:
        print("오류: 프로젝트 파일을 읽지 못했다 — " + facts["error"])
        return 2

    roots, unmatched = mg.expand_roots(args.source_roots, root)
    if not args.source_roots:
        roots = [project_dir]
    extra, unmatched_extra = mg.expand_roots(args.extra_roots, root)
    roots += extra
    for s in unmatched + unmatched_extra:
        notes.append("패턴 '{}' 에 맞는 폴더가 없음".format(s))
    excludes = [mg.norm(s if os.path.isabs(s) else os.path.join(root, s)) for s in args.exclude]
    depth = max(1, args.unit_depth)
    if args.includes:
        notes.append("--includes 는 언리얼 헤더 include 세기라 Godot 에서는 하지 않았다. '다른 모듈이 많이 참조하는 파일' 표가 그 몫이다")
    if args.engine_root:
        notes.append("--engine-root 는 Godot 지도에 쓰지 않는다. 엔진 클래스의 에디터 전용 여부는 이름(Editor*)으로만 가린다")

    def unit_of(path):
        rel = os.path.relpath(path, project_dir)
        parts = rel.split(os.sep)
        if parts[0] == "..":
            parts = os.path.relpath(path, root).split(os.sep)
        if parts[0] == "addons" and len(parts) > 2:
            return "addons/" + parts[1]
        dirs = parts[:-1]
        return "/".join(dirs[:depth]) if dirs else "(루트)"

    def res_path(res):
        return gp.res_to_path(res, project_dir)

    # 파일 모으기
    files = []
    seen_dirs = set()
    for r in roots:
        if not os.path.isdir(r):
            notes.append("없는 폴더: " + mg.show(r, root))
            continue
        for path, names in walk(r, budget):
            if path in seen_dirs:
                continue
            seen_dirs.add(path)
            files += [mg.norm(os.path.join(path, f)) for f in names if os.path.splitext(f)[1].lower() in SCAN_EXT]
    if budget.hit:
        failed = True
        notes.append("검색 실패: 파일 찾기가 {} 로 중단됨 — 아래 표는 일부다".format(budget.hit))

    # uid → 경로: .uid 파일(4.4 이후)과 씬·리소스 머리의 uid
    uid_map = {}
    for path, names in walk(project_dir, budget, max_depth=30):
        for f in names:
            if f.endswith(".uid"):
                t = (gp.read_text(os.path.join(path, f)) or "").strip()
                if t.startswith("uid://"):
                    uid_map[t] = mg.norm(os.path.join(path, f[:-4]))

    texts, unresolved = {}, []
    for fp in files:
        try:
            if os.path.getsize(fp) > args.max_bytes:
                unresolved.append("{}: 크기 상한으로 읽지 않음".format(mg.show(fp, root)))
                continue
        except OSError:
            continue
        t = gp.read_text(fp)
        if t is None:
            unresolved.append("{}: 읽기 실패".format(mg.show(fp, root)))
            continue
        texts[fp] = t
        if fp.endswith((".tscn", ".tres")):
            m = HEADER_UID_RE.search(t)
            if m:
                uid_map.setdefault(m.group(1), fp)

    # 선언: class_name, namespace, 에디터 전용 파일
    classes, spaces, editor_files = {}, {}, {}
    stripped = {}
    for fp, t in texts.items():
        ext = os.path.splitext(fp)[1].lower()
        if ext not in (".gd", ".cs"):
            continue
        nc, ns = gp.strip_code(t, ext)
        stripped[fp] = (nc, ns)
        if ext == ".gd":
            for m in CLASS_RE.finditer(nc):
                classes.setdefault(m.group(1), fp)
            m = EDITOR_BASE_GD.search(nc)
        else:
            for m2 in NAMESPACE_RE.finditer(nc):
                spaces.setdefault(m2.group(1), unit_of(fp))
            m = EDITOR_BASE_CS.search(ns)
        if m:
            editor_files[fp] = "{} 상속".format(m.group(1))
    if os.path.isdir(addons_dir):
        for name in sorted(os.listdir(addons_dir)):
            cfg = os.path.join(addons_dir, name, "plugin.cfg")
            if os.path.isfile(cfg):
                entries, _ = gp.parse_config(cfg)
                sc, _ = gp.lookup(entries, "plugin", "script")
                if sc:
                    p = gp.unquote(sc)
                    full = res_path(p) if p.startswith("res://") else mg.norm(os.path.join(addons_dir, name, p))
                    editor_files.setdefault(full, "plugin.cfg 의 script")
    autoloads = {}
    for a in facts["autoloads"]:
        p = res_path(a["path"]) if a["path"].startswith("res://") else None
        if p:
            autoloads[a["name"]] = (p, a["line"])

    # 간선
    edges = []        # (모듈, 대상 모듈, 종류, 위치, 원본 파일, 대상 파일)
    missing = {}      # 가리키는 파일이 없는 경로 → [위치]
    uid_fail = []

    def add(src_fp, target_fp, kind, text, pos, ref=None):
        line = text.count("\n", 0, pos) + 1
        where = "{}:{}".format(mg.show(src_fp, root), line)
        if target_fp is None:
            uid_fail.append("{}: {}".format(where, ref))
            return
        if ref and not os.path.exists(target_fp):
            missing.setdefault(ref, []).append(where)
        edges.append((unit_of(src_fp), unit_of(target_fp), kind, where, src_fp, target_fp))

    def resolve(ref):
        return uid_map.get(ref) if ref.startswith("uid://") else res_path(ref)

    name_re = None
    globals_ = dict((n, (p, "class_name")) for n, p in classes.items())
    for n, (p, _) in autoloads.items():
        globals_.setdefault(n, (p, "autoload"))
    if globals_:
        alt = "|".join(re.escape(n) for n in sorted(globals_, key=len, reverse=True))
        name_re = re.compile(r"(?<![\w.$])(" + alt + r")(?!\w)")
    editor_uses = []  # (파일, 줄, 무엇, 조건)

    for fp, t in sorted(texts.items()):
        if not budget.ok():
            failed = True
            notes.append("검색 실패: 참조 읽기가 {} 로 중단됨 — 간선이 일부다".format(budget.hit))
            break
        ext = os.path.splitext(fp)[1].lower()
        if ext in (".tscn", ".tres"):
            used = set()
            for m in EXT_RES_RE.finditer(t):
                attrs = dict(ATTR_RE.findall(m.group(1)))
                ref = attrs.get("path") or attrs.get("uid")
                if ref:
                    used.add(m.start())
                    add(fp, resolve(ref), "씬·리소스 참조", t, m.start(), ref)
            for m in RES_RE.finditer(t):
                line_start = t.rfind("\n", 0, m.start()) + 1
                if line_start in used or t.startswith("[gd_", line_start):
                    continue
                add(fp, resolve(m.group(1)), "경로 문자열", t, m.start(), m.group(1))
            continue
        if ext in (".gdshader", ".gdshaderinc"):
            for m in INCLUDE_RE.finditer(t):
                add(fp, resolve(m.group(1)), "셰이더 include", t, m.start(), m.group(1))
            continue
        nc, ns = stripped[fp]
        for m in RES_RE.finditer(nc):
            before = nc[nc.rfind("\n", 0, m.start()) + 1:m.start()]
            if ext == ".gd" and re.search(r"\bpreload\s*\(\s*$", before):
                kind = "preload"
            elif ext == ".gd" and re.match(r"^\s*extends\s+$", before):
                kind = "extends 경로"
            elif LOAD_CALL.search(before):
                kind = "동적 로드"
            else:
                kind = "경로 문자열"
            add(fp, resolve(m.group(1)), kind, nc, m.start(), m.group(1))
        if ext == ".gd" and name_re:
            for m in name_re.finditer(ns):
                target, how = globals_[m.group(1)]
                if target == fp:
                    continue
                if how == "class_name":
                    line_head = ns[ns.rfind("\n", 0, m.start()) + 1:m.start()]
                    kind = "extends class_name" if re.match(r"^\s*extends\s+$", line_head) else "class_name 사용"
                else:
                    kind = "autoload 사용"
                add(fp, target, kind, ns, m.start())
        if ext == ".cs":
            for m in USING_RE.finditer(ns):
                u = next((spaces[s] for s in spaces if m.group(1) == s or m.group(1).startswith(s + ".")), None)
                if u:
                    line = ns.count("\n", 0, m.start()) + 1
                    edges.append((unit_of(fp), u, "C# using", "{}:{}".format(mg.show(fp, root), line), fp, None))
        if fp not in editor_files:
            lines = t.splitlines()
            for m in EDITOR_USE.finditer(ns):
                line = ns.count("\n", 0, m.start()) + 1
                cond = gd_guard(lines, line) if ext == ".gd" else cs_guard(ns, t, m.start())
                editor_uses.append((fp, line, m.group(1) + " 사용", cond))

    for s, d, kind, where, sfp, dfp in edges:
        if dfp in editor_files and sfp not in editor_files and kind not in ("경로 문자열",):
            editor_uses.append((sfp, int(where.rsplit(":", 1)[1]), "에디터 전용 파일 {} ({}) 참조 — {}".format(
                mg.show(dfp, root), editor_files[dfp], kind), ""))

    # 모듈
    unit_files = {}
    for fp in texts:
        unit_files.setdefault(unit_of(fp), []).append(fp)
    # 코드가 폴더 하나(예: scripts/)에 몰리면 모듈이 하나로 뭉쳐 순환·층 판정이 뜻을 잃는다
    code_count = {u: sum(f.endswith((".gd", ".cs")) for f in fs) for u, fs in unit_files.items()}
    total_code = sum(code_count.values())
    if total_code >= 10:
        top_unit, top_n = max(code_count.items(), key=lambda kv: kv[1])
        if top_n / total_code >= 0.6:
            notes.append("코드 파일(.gd·.cs) {} 개 가운데 {} 개({:.0f}%)가 모듈 '{}' 하나에 있다. 순환 의존과 층 판정이 뭉개지므로 "
                         "--unit-depth {} 로 다시 돌릴 것".format(total_code, top_n, 100.0 * top_n / total_code, top_unit, depth + 1))

    def unit_kind(u):
        if u not in unit_files:
            return "읽은 파일 없음(가리키는 곳만 있음)"
        if u.startswith("addons/"):
            d = os.path.join(project_dir, *u.split("/"))
            if os.path.isfile(os.path.join(d, "plugin.cfg")):
                return "에디터 플러그인 애드온"
            for path, names in walk(d, mg.Budget(5), max_depth=6):
                if any(n.endswith(".gdextension") for n in names):
                    return "GDExtension 애드온"
            return "스크립트 애드온"
        return "게임 폴더"

    def unit_dir(u):
        return os.path.join(project_dir, *u.split("/")) if u != "(루트)" else project_dir

    project = set(unit_files) | {e[1] for e in edges}
    skipped = {u for u in project if u != "(루트)" and any(
        mg.norm(unit_dir(u)) == e or mg.norm(unit_dir(u)).startswith(e + os.sep) for e in excludes)}
    judged = project - skipped
    none_or_fail = mg.SEARCH_FAIL if failed else None

    agg = {}
    for s, d, kind, where, sfp, dfp in edges:
        if s == d:
            continue
        a = agg.setdefault((s, d, kind), [0, where])
        a[0] += 1

    print("# 모듈 의존 지도 (읽기 전용) — Godot")
    print("- 프로젝트 파일: " + mg.show(project_file, root))
    print("- 읽은 폴더: " + ", ".join(mg.show(r, root) for r in roots))
    print("- 모듈은 폴더다: addons/<이름> 은 애드온 하나, 그 밖은 프로젝트 폴더 아래 {} 단계 폴더 하나(바로 아래 파일은 '(루트)'). "
          "Godot 에는 의존 선언 파일이 없어서 간선은 파일 안의 참조(preload, class_name, 씬의 ext_resource 등)를 센 것이다.".format(depth))
    print("- 파일 {} 개(.gd {} / .cs {} / .tscn·.tres {} / 셰이더 {}), 모듈 {} 개, 참조 {} 개(모듈 사이 {} 개)".format(
        len(texts), sum(f.endswith(".gd") for f in texts), sum(f.endswith(".cs") for f in texts),
        sum(f.endswith((".tscn", ".tres")) for f in texts), sum(f.endswith((".gdshader", ".gdshaderinc")) for f in texts),
        len(project), len(edges), sum(1 for e in edges if e[0] != e[1])))
    print("- class_name {} 개, autoload {} 개, 에디터 전용 파일 {} 개를 찾았다".format(len(classes), len(autoloads), len(editor_files)))
    print("- C# 은 res:// 경로와 namespace using 만 센다. C# 클래스 이름으로 쓰는 것과 이진 리소스(.res, .scn) 안의 참조는 세지 못한다")
    if skipped:
        print("- 판정 절에서 뺀 모듈 {} 개(--exclude): {}".format(len(skipped), ", ".join(sorted(skipped))))
    for n in notes:
        print("- 주의: " + n)

    print("\n## 모듈 표")
    print("| 모듈 | 소속 | 모듈 종류 | 파일 수 | 이 모듈이 의존하는 모듈 수 | 이 모듈에 의존하는 모듈 수 |")
    print("|---|---|---|---|---|---|")
    out_m = {u: set() for u in project}
    in_m = {u: set() for u in project}
    for (s, d, kind) in agg:
        out_m.setdefault(s, set()).add(d)
        in_m.setdefault(d, set()).add(s)
    for u in sorted(project):
        print("| {} | {} | {} | {} | {} | {} |".format(
            mg.md(u) + (" (제외)" if u in skipped else ""), "애드온" if u.startswith("addons/") else "프로젝트",
            unit_kind(u), len(unit_files.get(u, [])), len(out_m[u]), len(in_m[u])))

    print("\n## 모듈 사이 간선")
    print("같은 두 모듈 사이 참조를 종류별로 묶었다. 첫 위치는 정렬해서 처음 나온 파일:줄이다.")
    print("| 의존하는 모듈 | 의존 대상 모듈 | 참조 종류 | 참조 수 | 첫 위치(파일:줄) |")
    print("|---|---|---|---|---|")
    for (s, d, kind), (n, where) in sorted(agg.items()):
        print("| {} | {} | {} | {} | {} |".format(mg.md(s), mg.md(d), mg.md(kind), n, mg.md(where)))
    if not agg:
        print("| - | {} | | | |".format(none_or_fail or "없음"))

    print("\n## 다른 모듈이 많이 참조하는 파일 (상위 {})".format(args.top))
    print("| 파일 | 모듈 | 참조하는 다른 모듈의 파일 수 | 다른 모듈 수 |")
    print("|---|---|---|---|")
    by_target = {}
    for s, d, kind, where, sfp, dfp in edges:
        if s != d and dfp:
            b = by_target.setdefault(dfp, [set(), set()])
            b[0].add(sfp)
            b[1].add(s)
    for dfp, (fs, ms) in sorted(by_target.items(), key=lambda kv: (-len(kv[1][0]), kv[0]))[:args.top]:
        print("| {} | {} | {} | {} |".format(mg.md(mg.show(dfp, root)), mg.md(unit_of(dfp)), len(fs), len(ms)))
    if not by_target:
        print("| - | {} | | |".format(none_or_fail or "없음"))

    print("\n## autoload")
    print("전역에서 이름으로 부르는 싱글턴이다. 참조하는 모듈이 많을수록 바꿀 때 영향이 넓다.")
    print("| 이름 | 경로 | 모듈 | 이름으로 참조하는 다른 모듈 수 | 위치 |")
    print("|---|---|---|---|---|")
    for name, (p, line) in sorted(autoloads.items()):
        users = {s for s, d, kind, where, sfp, dfp in edges if dfp == p and kind == "autoload 사용" and s != unit_of(p)}
        print("| {} | {} | {} | {} | {}:{} |".format(mg.md(name), mg.md(mg.show(p, root)), mg.md(unit_of(p)), len(users),
                                                   mg.md(mg.show(project_file, root)), line))
    if not autoloads:
        print("| - | 없음 | | | |")

    adj = {}
    for (s, d, kind) in agg:
        if kind not in LOOSE_KINDS and s in judged and d in judged:
            adj.setdefault(s, set()).add(d)
    print("\n## 순환 의존")
    cycles = [c for c in mg.tarjan(judged, adj) if len(c) > 1]
    if cycles:
        print("서로 참조하는 모듈 묶음이다(동적 로드, 경로 문자열, 제외한 모듈은 뺐다). 묶음 안 참조는 위 간선 표에서 찾는다.")
        for c in cycles:
            print("- " + " ↔ ".join(c))
    else:
        print("- " + (none_or_fail or "없음 (동적 로드와 경로 문자열을 뺀 모듈 사이 참조 기준)"))

    print("\n## 에디터 전용 코드에 기대는 곳")
    print("에디터 전용 파일(Editor* 상속, plugin.cfg 의 script)이 아닌 파일이 Editor* 클래스를 쓰거나 에디터 전용 파일을 참조한다. "
          "내보낸 게임에는 에디터 클래스가 없다. 조건 칸(Engine.is_editor_hint(), #if TOOLS 등)이 있으면 참고로만 보고, "
          "그 조건으로 내보낸 빌드에서도 안전한지는 엔진 문서와 내보내기 시험으로 확인한다.")
    print("| 위치(파일:줄) | 모듈 | 무엇 | 조건 |")
    print("|---|---|---|---|")
    shown = 0
    for fp, line, what, cond in sorted(editor_uses):
        if unit_of(fp) not in judged:
            continue
        shown += 1
        print("| {}:{} | {} | {} | {} |".format(mg.md(mg.show(fp, root)), line, mg.md(unit_of(fp)), mg.md(what), mg.md(cond or "-")))
    if not shown:
        print("| - | {} | | |".format(none_or_fail or "없음"))

    if args.layer:
        print("\n## 층 규칙 위반")
        layer_of, names = {}, []
        for i, spec in enumerate(args.layer):
            name, _, mods = spec.partition("=")
            names.append(name.strip())
            for m in mods.split(","):
                if m.strip():
                    layer_of[m.strip()] = i
        print("- 층(아래부터): " + " < ".join(names))
        print("| 의존하는 모듈(층) | 의존 대상 모듈(층) | 참조 종류 | 참조 수 | 첫 위치(파일:줄) |")
        print("|---|---|---|---|---|")
        bad = 0
        for (s, d, kind), (n, where) in sorted(agg.items()):
            if s in judged and s in layer_of and d in layer_of and layer_of[s] < layer_of[d]:
                bad += 1
                print("| {} ({}) | {} ({}) | {} | {} | {} |".format(mg.md(s), mg.md(names[layer_of[s]]), mg.md(d),
                                                                    mg.md(names[layer_of[d]]), mg.md(kind), n, mg.md(where)))
        if not bad:
            print("| - | {} | | | |".format(none_or_fail or "없음"))
        missing_layer = sorted(m for m in judged if m not in layer_of)
        if missing_layer:
            print("\n- 층이 정해지지 않은 모듈 {} 개: {}".format(len(missing_layer), ", ".join(missing_layer)))

    if args.layer_draft:
        print("\n## 층 초안 — 목표 구조 아님")
        print("지금 참조(동적 로드, 경로 문자열, 제외한 모듈은 뺐다)를 따라 깊이를 센 것이다. 깊이 0 은 다른 모듈을 참조하지 않는다. "
              "서로 참조하는 묶음은 한 층에 둔다.")
        levels = mg.layer_draft(judged, adj)
        for lv, mods in levels:
            print("- 깊이 {}: {}".format(lv, ", ".join(mods)))
        print("\n그대로 넘길 수 있는 인자:")
        print("```")
        print(" ".join('--layer "깊이{}={}"'.format(lv, ",".join(mods)) for lv, mods in levels))
        print("```")
        if failed:
            print("- " + mg.SEARCH_FAIL)

    print("\n## 가리키는 파일이 없는 res:// 경로 (상위 {})".format(args.top))
    print("코드에서 만든 경로의 앞부분이거나, 옮기거나 지운 파일을 아직 가리키는 곳이다.")
    if missing:
        for ref, wheres in sorted(missing.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:args.top]:
            print("- {} — {} 곳 (처음: {})".format(ref, len(wheres), wheres[0]))
    else:
        print("- " + (none_or_fail or "없음"))

    print("\n## 해석 못 한 것")
    print("읽지 못한 파일과 경로로 풀지 못한 uid 다. 이 참조는 위 표에 없다.")
    rest = unresolved + ["uid 를 못 풂 — " + u for u in uid_fail]
    for line in rest[:30]:
        print("- " + line)
    if len(rest) > 30:
        print("- … 외 {} 건".format(len(rest) - 30))
    if not rest:
        print("- " + (none_or_fail or "없음"))
    return 3 if failed else 0
