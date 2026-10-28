#!/usr/bin/env python3
"""언리얼 프로젝트의 모듈 의존 지도를 만든다 (TD 고문 구조 점검의 '모듈 의존' 범위).

Godot 프로젝트(--engine godot, 또는 project.godot 만 있을 때)는 godot_graph.py 가 만든다. 아래 설명은 언리얼 기준이다.

읽기만 한다. 프로젝트·엔진 파일을 고치지 않고, 결과는 표준 출력으로만 낸다.

읽는 것
- 프로젝트 파일(.uproject)과 플러그인 파일(.uplugin)의 Modules: 모듈 이름, 종류(Type), 로딩 단계
- 게임 코드 폴더의 *.Build.cs: Public/Private 의존, 동적 로드, include 경로 모듈. 줄 번호와 감싼 if 조건까지
- (--engine-root) 엔진 모듈의 종류: Engine/Source 아래 Build.cs 의 맨 위 폴더(Runtime, Editor, Developer …)와 엔진 .uplugin
- (--includes) 다른 모듈의 헤더를 include 하는 수. 모듈 폴더 아래 모든 헤더를 경로 끝부분으로 찾는다

내는 것 (마크다운)
- 모듈 표, 프로젝트 모듈 사이 간선 표, 프로젝트 모듈이 많이 의존하는 엔진 모듈
- 순환 의존(서로 의존하는 모듈 묶음)
- 런타임 종류 모듈이 에디터 종류 모듈에 의존하는 간선(if 조건 칸 포함)
- --layer 를 주면 아래 층 모듈이 위 층 모듈에 의존하는 간선
- --layer-draft 를 주면 지금 의존에서 뽑은 층 초안과, 그대로 넘길 수 있는 --layer 인자
- --includes 를 주면 include 가 많은 헤더, include 를 못 찾은 의존 간선, 의존 선언 없이 include 하는 곳
- 해석 못 한 줄, 일부만 해석한 줄(변수·반복문·함수로 만든 의존 목록 등). 그 줄의 의존은 표에 없다

시간 상한에 걸린 단계는 '검색 실패'로 적는다. 그 단계에 기대는 절은 '없음' 대신 '검색 실패 — 일부다'를 찍고,
끝날 때 종료 코드 3 을 낸다. 0 건으로 읽지 않게 하기 위해서다.
"""

import argparse
import glob
import json
import os
import re
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKIP_DIRS = {
    "Intermediate", "Saved", "Binaries", "DerivedDataCache", ".git", ".svn", ".vs", ".idea",
    "__pycache__", "node_modules", "Content", "Resources",
}
EDITOR_TYPES = {"Editor", "EditorNoCommandlet", "EditorAndProgram", "UncookedOnly", "Developer", "DeveloperTool"}
RUNTIME_TYPES = {"Runtime", "RuntimeNoCommandlet", "RuntimeAndProgram", "ClientOnly", "ClientOnlyNoCommandlet",
                 "ServerOnly", "CookedOnly"}
ENGINE_SOURCE_KINDS = {"runtime": "Runtime", "editor": "Editor", "developer": "Developer", "programs": "Program",
                       "thirdparty": "외부 라이브러리"}
DEP_KINDS = {
    "PublicDependencyModuleNames": "Public",
    "PrivateDependencyModuleNames": "Private",
    "DynamicallyLoadedModuleNames": "동적 로드",
    "PublicIncludePathModuleNames": "Public include 경로",
    "PrivateIncludePathModuleNames": "Private include 경로",
}
LINK_KINDS = {"Public", "Private", "uproject 추가 의존"}
CALL_RE = re.compile(r"\b(" + "|".join(DEP_KINDS) + r")\s*\.\s*(AddRange|Add)\s*\(")
MENTION_RE = re.compile(r"\b(" + "|".join(DEP_KINDS) + r")\b")
IF_RE = re.compile(r"\b(if)\s*\(|\belse\b(?!\s+if\b)")
INCLUDE_RE = re.compile(r'^[ \t]*#[ \t]*include[ \t]*"([^"]+)"', re.M)
HEADER_EXT = {".h", ".hpp", ".inl"}
CODE_EXT = {".h", ".hpp", ".inl", ".cpp", ".cc", ".c"}
BUILD_CS = ".build.cs"
SEARCH_FAIL = "검색 실패 — 이 절의 결과는 일부다(0 건으로 읽지 않는다)"


class Budget:
    def __init__(self, seconds):
        self.deadline = time.monotonic() + seconds
        self.hit = None

    def ok(self):
        if self.hit is None and time.monotonic() > self.deadline:
            self.hit = "시간 초과"
        return self.hit is None


def norm(path):
    return os.path.normpath(os.path.abspath(path))


_GLOB_CHARS = re.compile(r"[*?\[]")


def expand_roots(patterns, base):
    """폴더 인자를 절대 경로 목록으로 바꾼다. 와일드카드(*, ?, [])가 든 항목은 맞는 폴더들로 펼친다.

    프로필 폴더 칸에는 `Plugins/*/Source` 같은 패턴을 적을 수 있다. SKILL.md 가 값마다 따옴표로 감싸 넘기라고
    정해서 셸이 펼치지 않으므로 여기서 펼친다. 반환은 (폴더 목록, 맞는 폴더가 없는 패턴 목록)이다.
    패턴이 아닌 항목은 폴더가 없어도 그대로 돌려주고, 없는 폴더는 호출한 쪽이 기록한다.
    """
    out, unmatched = [], []
    for s in patterns:
        if not _GLOB_CHARS.search(s):
            out.append(norm(s if os.path.isabs(s) else os.path.join(base, s)))
            continue
        # 기준 폴더 이름에 대괄호가 있어도 패턴으로 읽히지 않게 이스케이프한다
        pat = s if os.path.isabs(s) else os.path.join(glob.escape(base), s)
        hits = sorted(norm(p) for p in glob.glob(pat) if os.path.isdir(p))
        if hits:
            out += hits
        else:
            unmatched.append(s)
    return list(dict.fromkeys(out)), unmatched


def show(path, base):
    p = norm(path)
    if base and (p == base or p.startswith(base + os.sep)):
        return os.path.relpath(p, base).replace(os.sep, "/")
    return p.replace(os.sep, "/")


def md(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def is_build_cs(name):
    return name.lower().endswith(BUILD_CS)


def module_name(build_cs_path):
    base = os.path.basename(build_cs_path)
    return base[:-len(BUILD_CS)]


def walk(root, budget, max_depth=14, stop_if=None):
    """(폴더, 파일 이름 목록) 을 돌려준다. stop_if(파일 목록) 이 참이면 그 폴더 아래로 내려가지 않는다."""
    stack = [(root, 0)]
    while stack:
        if not budget.ok():
            return
        path, depth = stack.pop()
        try:
            entries = list(os.scandir(path))
        except OSError:
            continue
        files = [e.name for e in entries if e.is_file(follow_symlinks=False)]
        yield path, files
        if stop_if and stop_if(files):
            continue
        if depth < max_depth:
            for e in entries:
                if e.is_dir(follow_symlinks=False) and e.name not in SKIP_DIRS and not e.name.startswith("."):
                    stack.append((e.path, depth + 1))


def read_text(path):
    """UTF-8 을 먼저 읽고, 안 되면 CP949, 그래도 안 되면 깨진 글자를 바꿔 읽는다."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError:
        return None
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    for enc in ("utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def read_descriptor(path):
    text = read_text(path)
    if text is None:
        return None
    try:
        return json.loads(text)
    except ValueError:
        try:
            return json.loads(re.sub(r",(\s*[}\]])", r"\1", text))
        except ValueError:
            return None


def string_end(text, i):
    """text[i] 가 '"' 일 때 그 문자열이 끝난 다음 위치. C# 의 @"…"(역슬래시를 이스케이프로 보지 않고 "" 가 따옴표 하나)도 다룬다."""
    n = len(text)
    verbatim = False
    k = i - 1
    while k >= 0 and text[k] in "@$":
        if text[k] == "@":
            verbatim = True
        k -= 1
    i += 1
    while i < n:
        c = text[i]
        if not verbatim and c == "\\":
            i += 2
            continue
        if c == '"':
            if verbatim and i + 1 < n and text[i + 1] == '"':
                i += 2
                continue
            return i + 1
        i += 1
    return n


def strip_comments(src):
    """주석을 공백으로 바꾼다. 줄바꿈과 글자 위치는 그대로 둔다(줄 번호 계산용)."""
    out = list(src)
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            i = string_end(src, i)
        elif src.startswith("//", i):
            while i < n and src[i] != "\n":
                out[i] = " "
                i += 1
        elif src.startswith("/*", i):
            while i < n and not src.startswith("*/", i):
                if src[i] != "\n":
                    out[i] = " "
                i += 1
            for k in range(i, min(i + 2, n)):
                out[k] = " "
            i += 2
        else:
            i += 1
    return "".join(out)


def match_close(text, i, open_ch, close_ch):
    """text[i] 가 open_ch 일 때 짝이 맞는 close_ch 의 위치. 문자열 안은 건너뛴다. 못 찾으면 -1."""
    depth, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            i = string_end(text, i)
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def condition_spans(code):
    """if / else 가 감싸는 범위 목록: (시작, 끝, 조건 글)."""
    spans = []
    for m in IF_RE.finditer(code):
        if m.group(1):
            p = code.find("(", m.start())
            q = match_close(code, p, "(", ")")
            if q < 0:
                continue
            cond = " ".join(code[p + 1:q].split())[:80]
            body = q + 1
        else:
            cond = "else"
            body = m.end()
        while body < len(code) and code[body].isspace():
            body += 1
        if body < len(code) and code[body] == "{":
            end = match_close(code, body, "{", "}")
        else:
            end = code.find(";", body)
        if end > 0:
            spans.append((body, end, cond))
    return spans


def parse_build_cs(path):
    """(간선 목록, 해석 못 한 줄 목록). 간선 = (의존 모듈, 종류, 줄, 조건 글)."""
    src = read_text(path)
    if src is None:
        return None, ["읽기 실패"]
    code = strip_comments(src)
    src_lines = src.splitlines()
    line_of = lambda off: code.count("\n", 0, off) + 1
    spans = condition_spans(code)
    edges, used, partial = [], set(), []
    for m in CALL_RE.finditer(code):
        p = code.find("(", m.end() - 1)
        q = match_close(code, p, "(", ")")
        if q < 0:
            continue
        inner = code[p + 1:q]
        conds = [c for s, e, c in spans if s <= m.start() <= e]
        found = False
        for s in re.finditer(r'"([A-Za-z_][A-Za-z0-9_]*)"', inner):
            edges.append((s.group(1), DEP_KINDS[m.group(1)], line_of(p + 1 + s.start()), " 그리고 ".join(conds)))
            found = True
        # 문자열·빈 목록 틀을 지우고도 이름이 남으면 변수나 함수로 넘긴 의존이 있다
        rest = re.sub(r'"(?:[^"\\]|\\.)*"|new\s*(?:string|List\s*<\s*string\s*>)?\s*(?:\[\s*\])?|[\s{}()\[\],;]', "", inner)
        if not rest:
            used.add(m.start())
        elif found:
            used.add(m.start())
            no = line_of(m.start())
            partial.append("{}: 일부만 해석함 — {}".format(no, " ".join(src_lines[no - 1].split())[:120]))
    unresolved = list(partial)
    for m in MENTION_RE.finditer(code):
        if m.start() not in used:
            no = line_of(m.start())
            unresolved.append("{}: {}".format(no, " ".join(src_lines[no - 1].split())[:120]))
    return edges, unresolved


def find_uproject(root, given):
    if given:
        p = given if os.path.isabs(given) else os.path.join(root, given)
        return norm(p) if os.path.isfile(p) else None
    found = []
    for path, files in walk(root, Budget(20), max_depth=3):
        if os.path.basename(path) in ("Engine", "Templates", "Samples"):
            continue
        found += [os.path.join(path, f) for f in files if f.endswith(".uproject")]
    return norm(found[0]) if len(found) == 1 else None


def engine_module_types(engine_root, budget):
    """엔진 모듈 이름 → 종류. Engine/Source 아래 Build.cs 의 맨 위 폴더와 엔진 플러그인 .uplugin 에서 읽는다."""
    types = {}
    src = os.path.join(engine_root, "Source")
    has_build = lambda files: any(is_build_cs(f) for f in files)
    for path, files in walk(src, budget, max_depth=6, stop_if=has_build):
        for f in files:
            if is_build_cs(f):
                top = os.path.relpath(path, src).split(os.sep)[0].lower()
                types.setdefault(module_name(f), ENGINE_SOURCE_KINDS.get(top, "모름"))
    plugins = os.path.join(engine_root, "Plugins")
    has_plugin = lambda files: any(f.endswith(".uplugin") for f in files)
    for path, files in walk(plugins, budget, max_depth=6, stop_if=has_plugin):
        for f in files:
            if f.endswith(".uplugin"):
                data = read_descriptor(os.path.join(path, f)) or {}
                for mod in data.get("Modules", []) or []:
                    if isinstance(mod, dict) and mod.get("Name"):
                        types[mod["Name"]] = mod.get("Type", "모름")
    return types


def tarjan(nodes, adj):
    index, low, on, stack, out = {}, {}, set(), [], []
    counter = [0]
    sys.setrecursionlimit(max(1000, len(nodes) * 4))

    def visit(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in adj.get(v, ()):
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(sorted(comp))

    for v in sorted(nodes):
        if v not in index:
            visit(v)
    return out  # 모든 묶음(한 모듈짜리 포함)


def layer_draft(nodes, adj):
    """의존을 따라 깊이를 센 층 초안. 서로 의존하는 묶음은 한 층에 둔다. 결과: [(깊이, [모듈…])]."""
    comps = tarjan(nodes, adj)
    comp_of = {m: i for i, c in enumerate(comps) for m in c}
    cadj = {}
    for v, ws in adj.items():
        for w in ws:
            if comp_of[v] != comp_of[w]:
                cadj.setdefault(comp_of[v], set()).add(comp_of[w])
    depth = {}

    def d(c):
        if c not in depth:
            depth[c] = 0  # 묶음끼리는 순환이 없으므로 재귀가 끝난다
            depth[c] = 1 + max((d(x) for x in cadj.get(c, ())), default=-1)
        return depth[c]

    levels = {}
    for i, c in enumerate(comps):
        levels.setdefault(d(i), []).extend(c)
    return sorted((k, sorted(v)) for k, v in levels.items())


def engine_kind(root, args):
    """--engine auto 면 프로젝트 파일 이름으로, 그것도 없으면 .uproject 가 없고 project.godot 가 있을 때만 godot."""
    if args.engine != "auto":
        return args.engine
    if args.project_file:
        return "godot" if os.path.basename(args.project_file).lower() == "project.godot" else "unreal"
    if find_uproject(root, None):
        return "unreal"
    for path, files in walk(root, Budget(20), max_depth=3):
        if "project.godot" in files:
            return "godot"
    return "unreal"


def main():
    ap = argparse.ArgumentParser(description="언리얼·Godot 프로젝트의 모듈 의존 지도를 만든다. 읽기만 한다.")
    ap.add_argument("project_root", help="프로젝트 루트 폴더. 결과의 경로는 이 폴더 기준 상대 경로다")
    ap.add_argument("--project-file", help="프로젝트 파일(.uproject). 상대 경로면 프로젝트 루트 기준. 없으면 깊이 3 까지 찾는다")
    ap.add_argument("--source-roots", nargs="*", default=[], help="게임 코드 폴더들. 와일드카드를 쓸 수 있다(예: 'Plugins/*/Source'). 없으면 프로젝트 파일 옆 Source 와 Plugins")
    ap.add_argument("--extra-roots", nargs="*", default=[], help="Build.cs 를 더 찾을 폴더들 (도구·서버 모듈 등). 항목마다 따옴표로 감싼다")
    ap.add_argument("--engine-root", help="엔진 폴더. 주면 엔진 모듈의 종류(런타임·에디터)를 읽어 에디터 의존 검사에 쓴다")
    ap.add_argument("--exclude", nargs="*", default=[],
                    help="판정 절에서 뺄 폴더들(프로젝트 루트 기준). 외부 공급사 플러그인 등. 모듈 표에는 '제외'로 남는다")
    ap.add_argument("--layer", action="append", default=[],
                    help="층 규칙 '이름=모듈1,모듈2'. 아래 층부터 순서대로 여러 번 준다. 아래 층이 위 층에 의존하면 위반")
    ap.add_argument("--layer-draft", action="store_true", help="지금 의존에서 뽑은 층 초안과 --layer 인자를 낸다")
    ap.add_argument("--includes", action="store_true", help="헤더 include 수를 센다 (느릴 수 있다)")
    ap.add_argument("--top", type=int, default=20, help="순위 표의 줄 수 (기본 20)")
    ap.add_argument("--seconds", type=float, default=120.0,
                    help="Build.cs·엔진 읽기 시간 상한 초 (기본 120). include 세기는 이 값의 절반을 따로 쓴다")
    ap.add_argument("--engine", choices=("auto", "unreal", "godot"), default="auto",
                    help="엔진 종류 (프로필 engine.kind). auto 면 프로젝트 파일 이름이나 폴더의 .uproject·project.godot 로 정한다. "
                         "godot 이면 godot_graph.py 가 지도를 만든다")
    ap.add_argument("--unit-depth", type=int, default=1,
                    help="Godot 만: addons 밖 모듈을 프로젝트 폴더 아래 몇 단계 폴더로 나눌지 (기본 1)")
    ap.add_argument("--max-bytes", type=int, default=4_000_000, help="Godot 만: 이보다 큰 파일은 읽지 않는다 (기본 4MB)")
    args = ap.parse_args()

    root = norm(args.project_root)
    if not os.path.isdir(root):
        print("오류: 프로젝트 루트 폴더가 없다 — " + root)
        return 2
    if engine_kind(root, args) == "godot":
        import godot_graph
        return godot_graph.run(args)
    uproject = find_uproject(root, args.project_file)
    if not uproject:
        print("오류: 프로젝트 파일을 정하지 못했다. --project-file 로 지정할 것")
        return 2
    project_dir = os.path.dirname(uproject)
    budget = Budget(args.seconds)
    notes = []
    failed = False

    roots, unmatched = expand_roots(args.source_roots, root)
    # 인자를 줬는데 맞는 폴더가 하나도 없으면 기본 폴더로 바꾸지 않는다. 범위가 몰래 바뀌지 않게 하기 위해서다
    if not args.source_roots:
        roots = [norm(os.path.join(project_dir, "Source")), norm(os.path.join(project_dir, "Plugins"))]
    extra, unmatched_extra = expand_roots(args.extra_roots, root)
    roots += extra
    for s in unmatched + unmatched_extra:
        notes.append("패턴 '{}' 에 맞는 폴더가 없음".format(s))
    excludes = [norm(s if os.path.isabs(s) else os.path.join(root, s)) for s in args.exclude]

    # 모듈 정보: 프로젝트 파일 + 플러그인 파일
    info = {}  # 모듈 → {type, phase, owner}
    extra_deps = []  # (모듈, 의존, 근거)
    up = read_descriptor(uproject) or {}
    for mod in up.get("Modules", []) or []:
        if isinstance(mod, dict) and mod.get("Name"):
            info[mod["Name"]] = {"type": mod.get("Type", "모름"), "phase": mod.get("LoadingPhase", "Default"),
                                 "owner": "프로젝트"}
            for dep in mod.get("AdditionalDependencies", []) or []:
                extra_deps.append((mod["Name"], dep, show(uproject, root) + " AdditionalDependencies"))

    build_files, plugin_dirs = [], {}
    for r in roots:
        if not os.path.isdir(r):
            notes.append("없는 폴더: " + show(r, root))
            continue
        for path, files in walk(r, budget):
            for f in files:
                full = os.path.join(path, f)
                if is_build_cs(f):
                    build_files.append(norm(full))
                elif f.endswith(".uplugin"):
                    pname = f[:-len(".uplugin")]
                    plugin_dirs[norm(path)] = pname
                    data = read_descriptor(full) or {}
                    for mod in data.get("Modules", []) or []:
                        if isinstance(mod, dict) and mod.get("Name"):
                            info.setdefault(mod["Name"], {"type": mod.get("Type", "모름"),
                                                          "phase": mod.get("LoadingPhase", "Default"),
                                                          "owner": "플러그인 " + pname})
    if budget.hit:
        failed = True
        notes.append("검색 실패: Build.cs·.uplugin 찾기가 {} 로 중단됨 — 아래 표는 일부다".format(budget.hit))

    def owner_of(path):
        d = os.path.dirname(path)
        while d and d.startswith(root):
            if d in plugin_dirs:
                return "플러그인 " + plugin_dirs[d]
            parent = os.path.dirname(d)
            if parent == d:
                break
            d = parent
        return "프로젝트"

    def excluded(path):
        return any(path == e or path.startswith(e + os.sep) for e in excludes)

    modules = {}  # 모듈 → Build.cs 경로
    edges, unresolved = [], {}
    by_lower = {k.lower(): k for k in info}  # 파일 이름의 대소문자가 달라도(예: solo.build.cs) 프로젝트·플러그인 파일의 이름을 쓴다
    for bf in sorted(build_files):
        name = module_name(bf)
        name = by_lower.get(name.lower(), name)
        modules[name] = bf
        third = os.sep + "thirdparty" + os.sep in bf.lower()
        info.setdefault(name, {"type": "외부 라이브러리" if third else "목록에 없음", "phase": "-",
                               "owner": owner_of(bf)})
        if info[name]["owner"] == "프로젝트" and owner_of(bf) != "프로젝트":
            info[name]["owner"] = owner_of(bf)
        es, bad = parse_build_cs(bf)
        if es is None:
            unresolved[name] = bad
            continue
        for dep, kind, line, cond in es:
            edges.append((name, dep, kind, "{}:{}".format(show(bf, root), line), cond))
        if bad:
            unresolved[name] = bad
    for src, dep, where in extra_deps:
        edges.append((src, dep, "uproject 추가 의존", where, ""))

    engine_types = {}
    if args.engine_root:
        eroot = norm(args.engine_root)
        engine_types = engine_module_types(eroot, budget)
        if budget.hit:
            failed = True
            notes.append("검색 실패: 엔진 모듈 종류 읽기가 {} 로 중단됨 — 종류를 모르는 엔진 모듈이 있을 수 있다".format(budget.hit))

    engine_lower = {k.lower(): v for k, v in engine_types.items()}

    def type_of(m):
        if m in info:
            return info[m]["type"]
        # Build.cs 파일 이름과 의존 선언의 대소문자가 다를 수 있다(예: HttpServer.Build.cs 와 "HTTPServer")
        return engine_types.get(m) or engine_lower.get(m.lower(), "모름")

    project = set(modules)
    skipped = {m for m in project if excluded(modules[m])}
    judged = project - skipped
    none_or_fail = SEARCH_FAIL if failed else None

    print("# 모듈 의존 지도 (읽기 전용)")
    print("- 프로젝트 파일: " + show(uproject, root))
    print("- 읽은 폴더: " + ", ".join(show(r, root) for r in roots))
    print("- 간선은 Build.cs 나 프로젝트 파일에 적힌 의존 선언 하나다. 같은 두 모듈이라도 Public 과 동적 로드로 따로 적혀 있으면 둘로 센다.")
    print("- Build.cs {} 개, 모듈 {} 개, 의존 간선 {} 개(프로젝트 모듈 사이 {} 개)".format(
        len(build_files), len(project), len(edges), sum(1 for e in edges if e[0] in project and e[1] in project)))
    print("- 해석 못 했거나 일부만 해석한 줄: {} 개 (끝 절의 목록)".format(sum(len(v) for v in unresolved.values())))
    print("- 엔진 모듈 종류: " + ("{} 개 읽음 ({})".format(len(engine_types), show(norm(args.engine_root), root))
                              if args.engine_root else "읽지 않음(--engine-root 없음) — 에디터 의존 검사는 프로젝트 모듈끼리만 한다"))
    if skipped:
        print("- 판정 절에서 뺀 모듈 {} 개(--exclude): {}".format(len(skipped), ", ".join(sorted(skipped))))
    for n in notes:
        print("- 주의: " + n)

    print("\n## 모듈 표")
    print("| 모듈 | 소속 | 모듈 종류 | 로딩 단계 | Build.cs | 이 모듈이 의존하는 프로젝트 모듈 수 | 이 모듈에 의존하는 프로젝트 모듈 수 | 이 모듈이 의존하는 엔진 모듈 수 |")
    print("|---|---|---|---|---|---|---|---|")
    out_p = {m: set() for m in project}
    in_p = {m: set() for m in project}
    out_e = {m: set() for m in project}
    for s, d, kind, where, cond in edges:
        if s not in project or s == d:
            continue
        if d in project:
            out_p[s].add(d)
            in_p[d].add(s)
        else:
            out_e[s].add(d)
    for m in sorted(project):
        i = info[m]
        print("| {} | {} | {} | {} | {} | {} | {} | {} |".format(
            md(m) + (" (제외)" if m in skipped else ""), md(i["owner"]), md(i["type"]), md(i["phase"]),
            md(show(modules[m], root)), len(out_p[m]), len(in_p[m]), len(out_e[m])))

    print("\n## 프로젝트 모듈 사이 간선")
    print("| 의존하는 모듈 | 의존 대상 모듈 | 의존 종류 | 조건 | 위치(Build.cs:줄) |")
    print("|---|---|---|---|---|")
    inner = sorted((e for e in edges if e[0] in project and e[1] in project and e[0] != e[1]),
                   key=lambda e: (e[0], e[1], e[2]))
    for s, d, kind, where, cond in inner:
        print("| {} | {} | {} | {} | {} |".format(md(s), md(d), md(kind), md(cond or "-"), md(where)))
    if not inner:
        print("| - | {} | | | |".format(none_or_fail or "없음"))

    print("\n## 프로젝트 모듈이 많이 의존하는 엔진 모듈 (상위 {})".format(args.top))
    print("| 엔진 모듈 | 모듈 종류 | 이 엔진 모듈에 의존하는 프로젝트 모듈 수 |")
    print("|---|---|---|")
    users = {}
    for s, d, kind, where, cond in edges:
        if s in project and d not in project:
            users.setdefault(d, set()).add(s)
    for d, us in sorted(users.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:args.top]:
        print("| {} | {} | {} |".format(md(d), md(type_of(d)), len(us)))

    adj = {}
    for s, d, kind, where, cond in inner:
        if kind != "동적 로드" and s in judged and d in judged:
            adj.setdefault(s, set()).add(d)
    print("\n## 순환 의존")
    cycles = [c for c in tarjan(judged, adj) if len(c) > 1]
    if cycles:
        print("서로 의존하는 모듈 묶음이다(동적 로드와 제외한 모듈은 뺐다). 묶음 안 간선은 위 간선 표에서 찾는다.")
        for c in cycles:
            print("- " + " ↔ ".join(c))
    else:
        print("- " + (none_or_fail or "없음 (동적 로드를 뺀 프로젝트 모듈 사이 간선 기준)"))

    print("\n## 런타임 종류 모듈이 에디터 종류 모듈에 의존하는 간선")
    print("조건 칸이 비어 있으면 if 로 감싸지 않은 의존이다. 조건이 있으면(예: Target.bBuildEditor) 참고로만 본다.")
    print("| 의존하는 모듈(모듈 종류) | 의존 대상 모듈(모듈 종류) | 의존 종류 | 조건 | 위치(Build.cs:줄) |")
    print("|---|---|---|---|---|")
    found, unknown = 0, set()
    for s, d, kind, where, cond in sorted(edges):
        if s not in judged or info[s]["type"] not in RUNTIME_TYPES:
            continue
        t = type_of(d)
        if t == "모름":
            unknown.add(d)
            continue
        if t in EDITOR_TYPES:
            found += 1
            print("| {} ({}) | {} ({}) | {} | {} | {} |".format(md(s), md(info[s]["type"]), md(d), md(t), md(kind),
                                                                md(cond or "-"), md(where)))
    if not found:
        print("| - | {} | | | |".format(none_or_fail or "없음"))
    if unknown:
        print("\n- 종류를 몰라 검사하지 못한 의존 대상 모듈 {} 개: {}".format(
            len(unknown), ", ".join(sorted(unknown)[:30]) + (" …" if len(unknown) > 30 else "")))

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
        print("| 의존하는 모듈(층) | 의존 대상 모듈(층) | 의존 종류 | 조건 | 위치(Build.cs:줄) |")
        print("|---|---|---|---|---|")
        bad = 0
        for s, d, kind, where, cond in inner:
            if s in judged and s in layer_of and d in layer_of and layer_of[s] < layer_of[d]:
                bad += 1
                print("| {} ({}) | {} ({}) | {} | {} | {} |".format(md(s), md(names[layer_of[s]]), md(d),
                                                                    md(names[layer_of[d]]), md(kind), md(cond or "-"),
                                                                    md(where)))
        if not bad:
            print("| - | {} | | | |".format(none_or_fail or "없음"))
        missing = sorted(m for m in judged if m not in layer_of)
        if missing:
            print("\n- 층이 정해지지 않은 프로젝트 모듈 {} 개: {}".format(len(missing), ", ".join(missing)))

    if args.layer_draft:
        print("\n## 층 초안 — 목표 구조 아님")
        print("지금 의존(동적 로드와 제외한 모듈은 뺐다)을 따라 깊이를 센 것이다. 깊이 0 은 다른 프로젝트 모듈에 의존하지 않는다. "
              "서로 의존하는 묶음은 한 층에 둔다.")
        levels = layer_draft(judged, adj)
        for depth, mods in levels:
            print("- 깊이 {}: {}".format(depth, ", ".join(mods)))
        print("\n그대로 넘길 수 있는 인자:")
        print("```")
        print(" ".join('--layer "깊이{}={}"'.format(depth, ",".join(mods)) for depth, mods in levels))
        print("```")
        if failed:
            print("- " + SEARCH_FAIL)

    inc_failed = False
    if args.includes:
        inc_failed = print_includes(project, judged, modules, inner, args, root, failed)

    print("\n## 해석 못 한 줄")
    print("의존 목록을 변수·반복문·함수로 만들거나 문자열이 아닌 값을 넘긴 줄이다. 이 줄의 의존은 위 표에 없다.")
    if unresolved:
        for m in sorted(unresolved):
            for line in unresolved[m][:10]:
                print("- {} ({}): {}".format(m, show(modules[m], root) if m in modules else "-", line))
    else:
        print("- " + (none_or_fail or "없음"))
    return 3 if (failed or inc_failed) else 0


def print_includes(project, judged, modules, inner, args, root, failed_before):
    """include 집계. 검색이 끊겼으면 True."""
    budget = Budget(max(10.0, args.seconds / 2))
    mod_root = {m: os.path.dirname(p) for m, p in modules.items()}
    owners = {}      # 헤더 경로 끝부분(예: 'AI/Foo.h', 'Foo.h') → 모듈 집합
    own_keys = {}    # 모듈 → 자기 헤더 경로 끝부분 집합
    files_of = {}
    for m, mr in mod_root.items():
        files_of[m] = []
        own_keys[m] = set()
        for path, files in walk(mr, budget, max_depth=12):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in CODE_EXT:
                    continue
                full = os.path.join(path, f)
                files_of[m].append(full)
                if ext in HEADER_EXT:
                    parts = os.path.relpath(full, mr).replace(os.sep, "/").split("/")
                    for k in range(len(parts)):
                        key = "/".join(parts[k:])
                        owners.setdefault(key, set()).add(m)
                        own_keys[m].add(key)
    print("\n## include 가 많은 헤더 (상위 {})".format(args.top))
    print("다른 모듈의 헤더를 include 하는 파일 수다. 헤더는 모듈 폴더 아래 어디에 있든 include 경로의 끝부분으로 찾는다.")
    if budget.hit:
        print("- " + SEARCH_FAIL + " ({}: 파일 목록을 다 모으지 못했다)".format(budget.hit))
        return True
    no_headers = sorted(m for m in project if not own_keys.get(m))
    count, ambiguous = {}, 0
    used_pairs = set()
    for m, files in files_of.items():
        for full in files:
            if not budget.ok():
                break
            text = read_text(full)
            if text is None:
                continue
            for inc in INCLUDE_RE.findall(strip_comments(text)):
                key = inc.replace("\\", "/").lstrip("./")
                if key in own_keys[m]:
                    continue  # 자기 모듈 헤더
                cands = owners.get(key)
                if not cands:
                    continue
                if len(cands) > 1:
                    ambiguous += 1
                    continue
                owner = next(iter(cands))
                used_pairs.add((m, owner))
                c = count.setdefault((owner, key), [set(), set()])
                c[0].add(full)
                c[1].add(m)
    if budget.hit:
        print("- " + SEARCH_FAIL + " ({}: include 를 다 세지 못했다)".format(budget.hit))
        return True
    print("| 헤더 | 모듈 | include 하는 다른 모듈의 파일 수 | 다른 모듈 수 |")
    print("|---|---|---|---|")
    for (owner, header), (fs, ms) in sorted(count.items(), key=lambda kv: (-len(kv[1][0]), kv[0]))[:args.top]:
        print("| {} | {} | {} | {} |".format(md(header), md(owner), len(fs), len(ms)))
    if ambiguous:
        print("\n- 같은 경로 끝부분의 헤더가 여러 모듈에 있어 어느 모듈의 헤더인지 정하지 못한 include {} 건은 세지 않았다".format(ambiguous))
    if no_headers:
        print("- 헤더가 하나도 없어 include 를 셀 수 없는 모듈 {} 개: {}".format(len(no_headers), ", ".join(no_headers)))

    declared = {}       # Public·Private 의존 (지울 후보를 볼 때)
    declared_any = set()  # 종류와 상관없이 선언된 의존 (include 경로 모듈 포함)
    for s, d, kind, where, cond in inner:
        declared_any.add((s, d))
        if kind in LINK_KINDS:
            declared.setdefault((s, d), kind)
    print("\n## include 를 못 찾은 의존 간선")
    print("Build.cs 의 Public·Private 의존인데 의존하는 모듈의 파일이 의존 대상 모듈의 헤더를 include 하지 않는다. "
          "모듈 로드 순서를 맞추려고만 선언했거나 리플렉션·블루프린트로만 쓰는 경우가 있다. 그래서 이 목록은 지워도 되는지 따로 확인해야 하는 후보다. "
          "동적 로드 간선, 헤더가 없는 모듈로 가는 간선, 제외한 모듈은 뺐다.")
    rows = sorted((s, d, k) for (s, d), k in declared.items()
                  if (s, d) not in used_pairs and s in judged and d in judged and d not in no_headers)
    for s, d, k in rows:
        print("- {} → {} ({})".format(s, d, k))
    if not rows:
        print("- " + (SEARCH_FAIL if failed_before else "없음"))
    print("\n## 의존 선언 없이 include 하는 곳")
    print("의존하는 모듈의 Build.cs 에 의존 대상 모듈이 어떤 종류로도 선언되지 않았는데 그 헤더를 include 한다. "
          "다른 모듈의 Public 의존을 거쳐 빌드되는 경우다.")
    rows = sorted(p for p in used_pairs if p not in declared_any and p[0] in judged and p[1] in judged)
    for s, d in rows:
        print("- {} → {}".format(s, d))
    if not rows:
        print("- " + (SEARCH_FAIL if failed_before else "없음"))
    return False


if __name__ == "__main__":
    sys.exit(main())
