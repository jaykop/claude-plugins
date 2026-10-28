#!/usr/bin/env python3
"""언리얼 프로젝트의 기술 목록(radar-inventory.md)을 만든다.

Godot 프로젝트(--engine godot, 또는 project.godot 만 있을 때)는 tech_inventory_godot.py 가 같은 형식으로 만든다.
--mod-only 와 수정 블록 세기는 두 엔진이 이 파일의 함수를 함께 쓴다. 아래 설명은 언리얼 기준이다.

읽기만 한다. 프로젝트·엔진 파일을 고치지 않는다. 결과는 --out 으로 받은 경로에만 쓰고, 없으면 표준 출력으로 낸다.

모으는 것
- 엔진 버전: 엔진 폴더의 Build/Build.version. 런처판이면 프로젝트 파일의 EngineAssociation.
- 플러그인: 프로젝트 파일(.uproject)의 Plugins 항목(켜짐/꺼짐)과 프로젝트 Plugins 폴더의 플러그인.
  엔진·프로젝트 폴더에서 같은 이름의 .uplugin 을 찾아 엔진 기본 켜짐 여부와 성숙도 표시를 읽는다.
- 사용 흔적: 게임 코드의 *.Build.cs 와 프로젝트 파일의 의존 목록에 그 플러그인의 모듈 이름이 있는지.
- 설정: 프로젝트 Config/Default*.ini 의 주요 렌더링·네트워크 설정. 찾은 것만 줄 번호와 함께.
- 엔진 수정 블록 수: 지정한 폴더만, 시간·개수 상한 안에서 센다. 상한에 걸리면 '검색 실패'.

다시 만드는 조건 (--previous 를 줬을 때)
- 입력 지문(엔진 버전 파일, 프로젝트 파일, Config 폴더의 ini, 게임 코드의 *.Build.cs, 인자)이 직전 목록과 다를 때
- 직전 목록의 마지막 갱신일에서 --stale-days 일이 지났을 때
- --force 를 줬을 때
어느 쪽도 아니면 다시 만들지 않고 '변경 없음' 을 출력한다.

출력 형식은 advisors 플러그인 shared/state-formats.md 의 radar-inventory.md 형식을 따른다.

--mod-only 는 목록을 만들지 않고 지정한 폴더의 수정 블록 수만 낸다(radar 단일 기술 진단).
--mod-only --mod-list 는 블록마다 파일:줄, 끝 줄, 줄 수, 주제 태그, 수정 사유(시작 표시 뒤의 글. 시작 표시는 내지 않음)를 낸다(td 구조 점검의 엔진 수정 범위).
radar 와 td 가 함께 쓰므로 플러그인 공용 폴더(scripts/)에 둔다.
"""

import argparse
import concurrent.futures
import datetime
import glob
import hashlib
import json
import os
import re
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

GENERATED_DIRS = {
    "Intermediate", "Saved", "Binaries", "DerivedDataCache", ".git", ".svn", ".vs", ".idea",
    "__pycache__", "node_modules",
}
# .uplugin 이 있는 폴더에서 더 내려가지 않을 하위 폴더 (플러그인 본체 내용물)
PLUGIN_BODY_DIRS = {
    "Source", "Content", "Resources", "Shaders", "Config", "ThirdParty", "Docs",
    "Documentation", "Extras", "Tests",
}
DEFAULT_MOD_EXT = ".h,.hpp,.hh,.inl,.c,.cc,.cpp,.cs,.usf,.ush,.ini,.py"
# Godot 엔진 소스(C++·셰이더·빌드 스크립트)와 애드온(GDScript·C#·셰이더)
DEFAULT_MOD_EXT_GODOT = ".h,.hpp,.inc,.c,.cc,.cpp,.cs,.glsl,.py,.gd,.gdshader,.gdshaderinc"
DEFAULT_KEYS = [
    r"r\.DynamicGlobalIlluminationMethod",
    r"r\.ReflectionMethod",
    r"r\.Shadow\.Virtual\.Enable",
    r"r\.Nanite\.[A-Za-z0-9_.]+",
    r"r\.RayTracing",
    r"r\.Lumen\.HardwareRayTracing",
    r"r\.AntiAliasingMethod",
    r"r\.ForwardShading",
    r"r\.AllowStaticLighting",
    r"r\.Substrate",
    r"r\.VirtualTextures",
    r"DefaultGraphicsRHI",
    r"net\.[A-Za-z0-9_.]+",
    r"NetServerMaxTickRate",
    r"MaxClientRate",
    r"MaxInternetClientRate",
    r"NetDriverDefinitions",
]
STATUS = ("없음", "엔진에 있으나 꺼짐", "켜짐·사용 흔적 없음", "사용 중", "엔진을 고쳐서 씀")
# 목록 끝에 붙이는 상태 설명. 스크립트가 상태를 가린 기준 그대로다.
STATUS_HELP = (
    ("없음", "프로젝트 파일에 꺼짐으로 적혀 있지만 엔진·프로젝트 폴더에서 플러그인 파일을 못 찾았거나, 직전 목록에 있었는데 이번에 못 찾았다"),
    ("엔진에 있으나 꺼짐", "플러그인 파일(엔진 폴더나 프로젝트 Plugins 폴더)은 있는데 꺼져 있다. 프로젝트 폴더에 있지만 꺼 둔 플러그인도 여기에 든다. "
     "엔진 폴더를 못 찾았을 때 프로젝트 파일에 꺼짐으로 적힌 것도 이 상태로 두고 근거 칸에 그렇게 적는다"),
    ("켜짐·사용 흔적 없음", "켜져 있지만 게임 코드 *.Build.cs·프로젝트 파일의 의존 목록·설정 파일의 섹션에서 쓰는 흔적을 못 찾았다. "
     "에셋이나 에디터에서만 쓰는 경우는 텍스트로 확인할 수 없으므로 '안 쓴다' 는 뜻이 아니다"),
    ("사용 중", "켜져 있고, 게임 코드나 프로젝트 파일이 그 플러그인의 모듈에 의존하거나 설정 파일에 그 플러그인의 섹션이 있다"),
    ("엔진을 고쳐서 씀", "켜져 있고 그 플러그인 폴더 안에 엔진 수정 블록이 있다. 수정 블록을 세지 않았거나 검색이 실패했으면 이 상태가 없다고 '고치지 않음' 으로 읽지 않는다"),
)


class Budget:
    """탐색 시간과 개수 상한. 상한에 걸리면 hit 에 이유가 남는다."""

    def __init__(self, seconds, max_entries):
        self.deadline = time.monotonic() + seconds
        self.max_entries = max_entries
        self.entries = 0
        self.hit = None

    def tick(self):
        self.entries += 1
        if self.hit is None:
            if self.entries > self.max_entries:
                self.hit = "탐색 항목 수 상한"
            elif time.monotonic() > self.deadline:
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


def show(path, roots):
    """근거 위치용 경로. 아는 루트 안이면 상대 경로, 아니면 절대 경로. 구분자는 '/'."""
    p = norm(path)
    for label, root in roots:
        if root and (p == root or p.startswith(root + os.sep)):
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            return rel if not label else "{}/{}".format(label, rel)
    return p.replace(os.sep, "/")


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            text = f.read()
    except OSError as e:
        return None, "읽기 실패: {}".format(e)
    try:
        return json.loads(text), None
    except ValueError:
        # 끝에 쉼표가 남은 JSON 을 한 번 더 시도한다
        try:
            return json.loads(re.sub(r",(\s*[}\]])", r"\1", text)), None
        except ValueError as e:
            return None, "JSON 해석 실패: {}".format(e)


def walk(root, max_depth, budget, skip_names=GENERATED_DIRS, stop_in_plugin=False):
    """(경로, 깊이, 하위 폴더, 파일) 을 깊이 우선으로 낸다. budget 이 다하면 멈춘다."""
    stack = [(root, 0)]
    while stack:
        path, depth = stack.pop()
        try:
            with os.scandir(path) as it:
                dirs, files = [], []
                for entry in it:
                    if not budget.tick():
                        return
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name not in skip_names:
                                dirs.append(entry.name)
                        else:
                            files.append(entry.name)
                    except OSError:
                        continue
        except OSError:
            continue
        yield path, depth, dirs, files
        if depth >= max_depth:
            continue
        has_uplugin = stop_in_plugin and any(f.lower().endswith(".uplugin") for f in files)
        for d in sorted(dirs, reverse=True):
            if has_uplugin and d in PLUGIN_BODY_DIRS:
                continue
            stack.append((os.path.join(path, d), depth + 1))


def find_uproject(project_root, given):
    if given:
        p = given if os.path.isabs(given) else os.path.join(project_root, given)
        return [norm(p)] if os.path.isfile(p) else [], None
    found = []
    budget = Budget(15, 100000)
    for path, depth, dirs, files in walk(project_root, 3, budget):
        for f in files:
            if f.lower().endswith(".uproject"):
                found.append(norm(os.path.join(path, f)))
    return found, budget.hit


def find_engine_root(uproject, given):
    """Build/Build.version 이 있는 엔진 폴더를 찾는다."""
    cands = []
    if given:
        cands += [given, os.path.join(given, "Engine")]
    probe = os.path.dirname(uproject)
    for _ in range(5):
        cands.append(os.path.join(probe, "Engine"))
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    for c in cands:
        if os.path.isfile(os.path.join(c, "Build", "Build.version")):
            return norm(c)
    return None


def plugin_search_roots(engine_root, project_dir):
    roots = []
    if engine_root:
        roots.append(("엔진", os.path.join(engine_root, "Plugins")))
        for base in ("Platforms", "Restricted"):
            b = os.path.join(engine_root, base)
            if os.path.isdir(b):
                roots.append(("엔진", b))
    roots.append(("프로젝트", os.path.join(project_dir, "Plugins")))
    pp = os.path.join(project_dir, "Platforms")
    if os.path.isdir(pp):
        roots.append(("프로젝트", pp))
    return [(k, norm(r)) for k, r in roots if os.path.isdir(r)]


def index_plugins(search_roots, seconds):
    """이름(소문자) → [(출처 종류, .uplugin 경로)]."""
    index = {}
    budget = Budget(seconds, 600000)
    for kind, root in search_roots:
        for path, depth, dirs, files in walk(root, 7, budget, stop_in_plugin=True):
            for f in files:
                if f.lower().endswith(".uplugin"):
                    index.setdefault(f[:-8].lower(), []).append((kind, norm(os.path.join(path, f))))
        if budget.hit:
            break
    return index, budget.hit


def first_outside(locs, own_dir):
    """위치 목록에서 own_dir(플러그인 자기 폴더) 밖의 첫 위치. 자기 폴더 안의 Build.cs 는 사용 흔적이 아니다."""
    for loc in locs or []:
        if own_dir is None or not loc[0].startswith(own_dir + os.sep):
            return loc
    return None


def list_build_cs(source_roots, seconds):
    """게임 코드 폴더의 *.Build.cs 경로 목록(정렬). 입력 지문과 사용 흔적 검색이 같은 목록을 쓴다."""
    found = []
    budget = Budget(seconds, 300000)
    for root in source_roots:
        if not os.path.isdir(root):
            continue
        for path, depth, dirs, files in walk(root, 10, budget):
            for f in files:
                if f.endswith(".Build.cs"):
                    found.append(norm(os.path.join(path, f)))
        if budget.hit:
            break
    return sorted(found), budget.hit


def collect_build_cs(build_files, per_name=20):
    """*.Build.cs 안의 따옴표 문자열 → 위치(경로, 줄) 목록. 이름마다 per_name 개까지."""
    names = {}
    ident = re.compile(r'"([A-Za-z_][A-Za-z0-9_]*)"')
    for fp in build_files:
        try:
            with open(fp, "r", encoding="utf-8-sig", errors="replace") as fh:
                for no, line in enumerate(fh, 1):
                    code = line.split("//", 1)[0]
                    for m in ident.finditer(code):
                        lst = names.setdefault(m.group(1).lower(), [])
                        if len(lst) < per_name:
                            lst.append((fp, no))
        except OSError:
            continue
    return names


def count_mod_blocks(dirs, marker_re, exts, seconds, max_files, max_bytes, workers=8, end_re=None):
    """폴더별 수정 블록 수. 결과: [(폴더, 개수 또는 None, 실패 이유, 블록이 있는 파일 {경로: 개수}, 메모)].

    end_re 를 주면(--mod-list) 끝 표시만 있는 파일도 개수 0 으로 파일 목록에 넣는다. 짝이 맞지 않는 끝 줄을 찾기 위해서다.

    파일 목록을 먼저 모은 뒤 여러 스레드로 읽는다. 묶음마다 시간 상한을 확인하고,
    상한에 걸린 폴더와 그 뒤 폴더는 개수 대신 '검색 실패' 를 돌려준다(0 으로 치지 않는다).
    읽지 못한 파일과 크기 상한으로 건너뛴 파일은 개수를 메모에 남긴다.
    """

    def scan(fp):
        try:
            if os.path.getsize(fp) > max_bytes:
                return fp, "big"
            with open(fp, "rb") as fh:
                data = fh.read()
            n = len(marker_re.findall(data))
            if not n and end_re is not None and end_re.search(data):
                return fp, -1  # 끝 표시만 있다
            return fp, n
        except OSError:
            return fp, "fail"

    results = []
    deadline = time.monotonic() + seconds
    files_seen = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for i, d in enumerate(dirs):
            if not os.path.isdir(d):
                results.append((d, None, "폴더 없음", {}, ""))
                continue
            remaining = deadline - time.monotonic()
            fail = None
            hits = {}
            total = 0
            skipped = {"big": 0, "fail": 0}
            if remaining <= 0:
                fail = "검색 실패(시간 초과)"
            else:
                budget = Budget(remaining, max_files * 20)
                todo = []
                for path, depth, sub, files in walk(d, 40, budget):
                    for f in files:
                        if os.path.splitext(f)[1].lower() in exts:
                            todo.append(os.path.join(path, f))
                files_seen += len(todo)
                if budget.hit:
                    fail = "검색 실패({}, 파일 목록 수집 중)".format(budget.hit)
                elif files_seen > max_files:
                    fail = "검색 실패(파일 수 상한 {})".format(max_files)
                else:
                    step = 2000
                    for s in range(0, len(todo), step):
                        for fp, n in pool.map(scan, todo[s:s + step], chunksize=64):
                            if n in skipped:
                                skipped[n] += 1
                            elif n == -1:
                                hits[norm(fp)] = 0
                            elif n:
                                hits[norm(fp)] = n
                                total += n
                        if time.monotonic() > deadline and s + step < len(todo):
                            fail = "검색 실패(시간 초과, 파일 {} 개 중 {} 개까지 읽음)".format(len(todo), s + step)
                            break
            memo = []
            if skipped["fail"]:
                memo.append("읽기 실패 파일 {} 개".format(skipped["fail"]))
            if skipped["big"]:
                memo.append("크기 상한으로 건너뛴 파일 {} 개".format(skipped["big"]))
            results.append((norm(d), None if fail else total, fail, hits, ", ".join(memo)))
            if fail:
                # 상한에 걸리면 뒤 폴더도 세지 않는다
                for rest in dirs[i + 1:]:
                    results.append((norm(rest), None, "검색 실패 — 앞 폴더에서 상한에 걸려 세지 않음", {}, ""))
                break
    return results


def decode_line(raw):
    """엔진 파일 한 줄을 푼다. UTF-8 을 먼저, 안 되면 CP949, 그래도 안 되면 깨진 글자를 바꿔 푼다."""
    for enc in ("utf-8", "cp949"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def list_mod_blocks(files, start_re, end_re, tag_re):
    """수정 블록이 있는 파일들에서 블록마다 위치와 수정 사유를 뽑는다.

    결과: (블록 목록, 시작 표시 없는 끝 줄 목록, 읽기 실패 파일 수).
    블록 = (파일, 시작 줄, 끝 줄 또는 None, 짝 상태, 태그, 수정 사유).
    - 수정 사유는 시작 표시 뒤의 글만이다. 시작 표시(수정자 ID 가 든 경우가 많다)는 내지 않는다.
    - 끝 표시는 가장 가까운 열린 시작 표시와 짝짓는다(겹친 블록도 안쪽부터 닫힌다).
    - 한 줄에서 시작 표시와 끝 표시가 겹쳐 걸리면 끝 줄로 본다(시작 정규식이 'X_(BEGIN|END)' 처럼 끝 줄에도 걸리는 경우).
    - 한 줄에 시작 표시가 있고 그 뒤에 끝 표시가 따로 있으면 그 줄 하나로 닫힌 블록이다.
    """
    blocks, orphans, failed = [], [], 0
    for fp in files:
        try:
            with open(fp, "rb") as fh:
                lines = fh.read().splitlines()
        except OSError:
            failed += 1
            continue
        stack = []
        for no, raw in enumerate(lines, 1):
            m = start_re.search(raw)
            e = None
            if end_re is not None:
                e = end_re.search(raw, m.end()) if m else end_re.search(raw)
                if m and not e:
                    # 끝 표시가 시작 표시와 겹치면 끝 줄이다
                    e2 = end_re.search(raw)
                    if e2 and e2.start() < m.end():
                        m, e = None, e2
            if m:
                after = decode_line(raw[m.end():e.start() if e else len(raw)]).strip().lstrip(":").strip()
                t = tag_re.search(after) if tag_re else None
                b = [fp, no, None, "", t.group(1) if t else "", after[:200]]
                if e:
                    b[2], b[3] = no, "짝 맞음(한 줄)"
                    blocks.append(b)
                elif end_re is None:
                    b[3] = "끝 표시 미지정"
                    blocks.append(b)
                else:
                    stack.append(b)
                continue
            if e:
                if stack:
                    b = stack.pop()
                    b[2], b[3] = no, "짝 맞음"
                    blocks.append(b)
                else:
                    orphans.append((fp, no))
        for b in stack:
            b[3] = "끝 표시 못 찾음"
            blocks.append(b)
    blocks.sort(key=lambda b: (b[0], b[1]))
    return [tuple(b) for b in blocks], orphans, failed


def scan_config(config_dir, key_res, seconds):
    rows = []
    files = []
    if not os.path.isdir(config_dir):
        return rows, files, "Config 폴더 없음"
    for f in sorted(os.listdir(config_dir)):
        if f.lower().startswith("default") and f.lower().endswith(".ini"):
            files.append(os.path.join(config_dir, f))
    line_re = re.compile(r"^\s*([+\-!.]?)([A-Za-z0-9_.]+)\s*=(.*)$")
    for fp in files:
        section = ""
        try:
            with open(fp, "r", encoding="utf-8-sig", errors="replace") as fh:
                for no, line in enumerate(fh, 1):
                    s = line.strip()
                    if not s or s[0] in ";#":
                        continue
                    if s.startswith("[") and s.endswith("]"):
                        section = s[1:-1]
                        continue
                    m = line_re.match(line)
                    if not m:
                        continue
                    op, key, val = m.group(1), m.group(2), m.group(3).strip()
                    if any(k.fullmatch(key) for k in key_res):
                        if len(val) > 120:
                            val = val[:117] + "..."
                        rows.append((op + key, val, norm(fp), no, section))
        except OSError:
            continue
    return rows, files, None


def fingerprint(paths, extra, base):
    """파일 내용과 base 기준 상대 경로로 해시를 만든다. 드라이브 문자나 작업 폴더 위치가 달라도 같은 값이 나온다."""
    h = hashlib.sha256()
    for p in paths:
        try:
            label = os.path.relpath(p, base)
        except ValueError:  # 윈도우에서 드라이브가 다르면 상대 경로를 만들 수 없다
            label = os.path.basename(p)
        h.update(label.replace(os.sep, "/").encode("utf-8"))
        try:
            with open(p, "rb") as f:
                h.update(f.read())
        except OSError:
            h.update(b"<missing>")
    h.update(extra.encode("utf-8"))
    return h.hexdigest()[:16]


def parse_previous(path):
    """직전 목록에서 (지문, 이름→(ID, 상태), 날짜) 를 읽는다."""
    prev = {"fp": None, "ids": {}, "date": None}
    if not path or not os.path.isfile(path):
        return prev
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            m = re.match(r"^\|\s*입력 지문\s*\|\s*([0-9a-f]+)\s*\|", line)
            if m:
                prev["fp"] = m.group(1)
            m = re.match(r"^\|\s*(TI-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
            if m:
                prev["ids"][m.group(2)] = (m.group(1), m.group(3))
            m = re.search(r"마지막 갱신:\s*(\d{4}-\d{2}-\d{2})", line)
            if m:
                prev["date"] = m.group(1)
    return prev


def md_cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def print_mod_list(res, marker_re, end_re, tag_re, args, roots_for_show):
    """--mod-only --mod-list 결과: 폴더별 블록 수(목록 기준), 블록 표, 태그별 묶음, 짝이 맞지 않는 곳."""
    files = sorted({fp for _, _, _, hits, _ in res for fp in hits})
    failed_dirs = [show(d, roots_for_show) for d, _, fail, _, _ in res if fail and fail != "폴더 없음"]
    missing_dirs = [show(d, roots_for_show) for d, _, fail, _, _ in res if fail == "폴더 없음"]
    memos = ["{} — {}".format(show(d, roots_for_show), memo) for d, _, _, _, memo in res if memo]
    blocks, orphans, read_fail = list_mod_blocks(files, marker_re, end_re, tag_re)
    print()
    print("## 블록 목록")
    print("- 끝 표시: {}".format(
        "{}{}".format(args.mod_end, " (글자 그대로)" if args.literal else " (정규식)") if end_re else "지정 안 함 — 끝 줄과 줄 수는 모름"))
    if failed_dirs:
        print("- 주의: 검색 실패한 폴더가 있어 아래 목록은 일부다(0 으로 읽지 않는다) — " + ", ".join(failed_dirs))
    if missing_dirs:
        print("- 없는 폴더: " + ", ".join(missing_dirs))
    for m in memos:
        print("- 주의: 건너뛴 파일이 있어 이 폴더의 블록 수는 최소값이다 — " + m)
    if read_fail:
        print("- 주의: 목록을 만들 때 다시 읽지 못한 파일 {} 개".format(read_fail))
    print("- 수정 사유는 프로젝트 내부 정보다. 검색어에 넣지 않는다. 시작 표시(수정자 ID 가 들 수 있다)는 결과에 넣지 않았다.")

    # 폴더별 블록 수는 목록에서 다시 센다. 시작 표시 정규식이 끝 줄에도 걸리면 위의 개수(걸린 줄 수)와 다르다
    print()
    print("### 폴더별 블록 수 (목록 기준)")
    dirs = [d for d, _, fail, _, _ in res if fail != "폴더 없음"]
    for d, n, fail, hits, memo in res:
        if fail == "폴더 없음":
            continue
        inside = [b for b in blocks if b[0] == d or b[0].startswith(d + os.sep)]
        note = ""
        if n is not None and n != len(inside):
            note = " — 위의 개수({})와 다르다. 시작 표시 정규식이 끝 줄에도 걸리는지 확인할 것".format(n)
        print("- {}: {}{}".format(show(d, roots_for_show), fail if fail else "{} 개".format(len(inside)), note))

    print()
    print("| # | 위치 | 끝 줄 | 줄 수 | 짝 | 태그 | 수정 사유 |")
    print("|---|---|---|---|---|---|---|")
    for i, (fp, start, end, state, tag, text) in enumerate(blocks, 1):
        lines = end - start + 1 if end else "모름"
        print("| {} | {}:{} | {} | {} | {} | {} | {} |".format(
            i, md_cell(show(fp, roots_for_show)), start, end or "-", lines, state, md_cell(tag or "-"), md_cell(text or "(수정 사유 없음)")))
    if not blocks:
        print("| - | {} | | | | | |".format("검색 실패 — 일부다" if failed_dirs else "블록 없음"))

    print()
    print("## 태그별 묶음")
    print("태그가 없는 블록은 파일 단위로 묶는다. 줄 수 합은 끝 줄을 찾은 블록만 더한 값이다.")
    print()
    print("| 묶음 | 블록 수 | 파일 수 | 줄 수 합 | 끝 줄을 못 찾은 블록 |")
    print("|---|---|---|---|---|")
    groups = {}
    for fp, start, end, state, tag, text in blocks:
        key = "[{}]".format(tag) if tag else "(태그 없음) " + show(fp, roots_for_show)
        g = groups.setdefault(key, {"n": 0, "files": set(), "lines": 0, "open": 0})
        g["n"] += 1
        g["files"].add(fp)
        if end:
            g["lines"] += end - start + 1
        else:
            g["open"] += 1
    for key, g in sorted(groups.items(), key=lambda kv: (-kv[1]["n"], kv[0])):
        print("| {} | {} | {} | {} | {} |".format(md_cell(key), g["n"], len(g["files"]), g["lines"], g["open"]))
    broken = [k for k in groups if "�" in k]
    if broken:
        print()
        print("- 주의: 태그 글자가 깨진 묶음 {} 개 — 파일 인코딩을 확인할 것".format(len(broken)))

    if end_re:
        print()
        print("## 짝이 맞지 않는 곳")
        bad = [b for b in blocks if not b[3].startswith("짝 맞음")]
        if not bad and not orphans:
            print("- 없음" if not failed_dirs else "- 검색 실패 — 일부만 봤다")
        for fp, start, end, state, tag, text in bad:
            print("- {}:{} — {}".format(show(fp, roots_for_show), start, state))
        for fp, no in orphans:
            print("- {}:{} — 시작 표시 없는 끝 줄".format(show(fp, roots_for_show), no))


def run_mod_only(args, mod_dirs, marker_re, exts, today, roots_for_show):
    """--mod-only: 목록을 만들지 않고 수정 블록 수(와 --mod-list 면 블록 목록)만 낸다. 엔진 종류와 상관없다."""
    if not marker_re or not mod_dirs:
        print("오류: --mod-only 에는 --mod-marker 와 --mod-dirs 가 필요하다")
        return 2
    end_re = tag_re = None
    if args.mod_list:
        try:
            if args.mod_end:
                end_re = re.compile((re.escape(args.mod_end) if args.literal else args.mod_end).encode("utf-8"))
            tag_re = re.compile(args.mod_tag_re) if args.mod_tag_re else None
        except re.error as e:
            print("오류: --mod-end 나 --mod-tag-re 정규식이 잘못됐다 — {}".format(e))
            return 2
        if tag_re is not None and tag_re.groups < 1:
            print(r"오류: --mod-tag-re 에는 태그를 담을 캡처 그룹이 하나 있어야 한다 (예: '\[([^\]]+)\]')")
            return 2
    res = count_mod_blocks(mod_dirs, marker_re, exts, args.seconds, args.max_files, args.max_bytes, end_re=end_re)
    print("# 엔진 수정 블록 수 (읽기 전용, {})".format(today))
    print("- 패턴: {}{} — 시작 표시가 걸린 줄 수를 센다".format(args.mod_marker, " (글자 그대로)" if args.literal else " (정규식)"))
    for d, n, fail, hits, memo in res:
        with_start = {fp: c for fp, c in hits.items() if c}
        print("- {}: {}{}".format(show(d, roots_for_show), fail if fail else "{} 개, 파일 {} 개".format(n, len(with_start)),
                                  " ({})".format(memo) if memo else ""))
        for fp, c in sorted(with_start.items(), key=lambda x: -x[1])[:15]:
            print("  - {} : {}".format(show(fp, roots_for_show), c))
    if args.mod_list:
        print_mod_list(res, marker_re, end_re, tag_re, args, roots_for_show)
    return 0


def resolve_mod_dirs(mod_args, engine_root, root):
    """수정 블록을 셀 폴더. 상대 경로는 엔진 폴더 기준으로 먼저 보고, 없으면 프로젝트 루트 기준으로 본다."""
    out = []
    for d in mod_args:
        if os.path.isabs(d):
            out.append(norm(d))
            continue
        cands = [os.path.join(b, d) for b in (engine_root, root) if b]
        out.append(norm(next((c for c in cands if os.path.isdir(c)), cands[0])))
    return out


def detect_engine(root, project_file):
    """--engine auto 일 때 엔진 종류. 프로젝트 파일을 줬으면 그 이름으로, 아니면 .uproject 가 없고 project.godot 가 있을 때만 godot."""
    if project_file:
        return "godot" if os.path.basename(project_file).lower() == "project.godot" else "unreal"
    ups, _ = find_uproject(root, None)
    if ups:
        return "unreal"
    budget = Budget(15, 100000)
    for path, depth, dirs, files in walk(root, 3, budget, skip_names=GENERATED_DIRS | {".godot", "addons"}):
        if "project.godot" in files:
            return "godot"
    return "unreal"


def main():
    ap = argparse.ArgumentParser(
        description="언리얼·Godot 프로젝트의 기술 목록(radar-inventory.md)을 만든다. 프로젝트·엔진 파일은 읽기만 한다.")
    ap.add_argument("project_root", nargs="?", default="", help="프로젝트 루트 폴더 (근거 위치를 이 폴더 기준 상대 경로로 적는다). 없거나 빈 값이면 현재 폴더")
    ap.add_argument("--engine", choices=("auto", "unreal", "godot"), default="auto",
                    help="엔진 종류 (프로필 engine.kind). auto 면 프로젝트 파일 이름이나 폴더의 .uproject·project.godot 로 정한다 (기본 auto)")
    ap.add_argument("--project-file", help="프로젝트 파일(.uproject 또는 project.godot) 경로. 상대 경로면 프로젝트 루트 기준. 없으면 깊이 3 까지 찾는다")
    ap.add_argument("--engine-root", help="엔진 폴더. 언리얼은 안에 Build/Build.version 이 있는 폴더(없으면 프로젝트 파일 위쪽에서 찾는다), "
                                          "Godot 은 version.py 가 있는 엔진 소스 폴더(커스텀 빌드일 때만)")
    ap.add_argument("--mod-marker", help="엔진 수정 블록의 시작 줄을 찾는 정규식 (예: 'MYGAME_BEGIN')")
    ap.add_argument("--literal", action="store_true", help="--mod-marker 를 정규식이 아니라 글자 그대로 찾는다")
    ap.add_argument("--mod-dirs", nargs="*", default=[], help="수정 블록을 셀 폴더들. 상대 경로면 엔진 폴더 기준, 거기 없으면 프로젝트 루트 기준")
    ap.add_argument("--mod-ext", help="수정 블록을 찾을 파일 확장자, 쉼표로 구분 (기본: 언리얼 {}, Godot {})".format(
        DEFAULT_MOD_EXT, DEFAULT_MOD_EXT_GODOT))
    ap.add_argument("--mod-only", action="store_true", help="목록은 만들지 않고 --mod-dirs 의 수정 블록 수만 출력한다")
    ap.add_argument("--mod-list", action="store_true", help="--mod-only 와 함께: 블록마다 파일:줄, 끝 줄, 줄 수, 짝, 주제 태그, 수정 사유(시작 표시 뒤의 글)를 낸다")
    ap.add_argument("--mod-end", help="--mod-list 에서 블록 끝 줄을 찾는 정규식 (예: 'MYGAME_END'). --literal 이면 글자 그대로. 없으면 끝 줄과 줄 수는 '모름'")
    ap.add_argument("--mod-tag-re", default=r"\[([^\]]+)\]",
                    help="--mod-list 에서 시작 표시 뒤 글에서 주제 태그를 뽑는 정규식. 첫 번째 캡처 그룹을 태그로 쓴다 (기본: 대괄호 안 글)")
    ap.add_argument("--source-roots", nargs="*", default=[], help="게임 코드 폴더들 (사용 흔적 검색). 와일드카드를 쓸 수 있다(예: 'Plugins/*/Source'). "
                                                                  "없으면 언리얼은 프로젝트 파일 옆 Source 와 Plugins, Godot 은 project.godot 가 있는 폴더 전체")
    ap.add_argument("--extra-key", action="append", default=[], help="더 볼 설정 이름 정규식 (여러 번 줄 수 있음)")
    ap.add_argument("--previous", help="직전 radar-inventory.md. 주면 ID 를 이어 쓰고, 입력 지문이 같고 --stale-days 안이면 다시 만들지 않는다")
    ap.add_argument("--stale-days", type=int, help="직전 목록의 마지막 갱신일에서 이 일수가 지나면 입력 지문이 같아도 다시 만든다 (프로필 stale_after_days)")
    ap.add_argument("--force", action="store_true", help="입력 지문이 같아도 다시 만든다")
    ap.add_argument("--date", help="작성일 YYYY-MM-DD (기본: 시스템 날짜)")
    ap.add_argument("--revision", default="확인 못 함", help="기준 리비전 (CL 번호 또는 커밋 앞 12자)")
    ap.add_argument("--next-check", help="머리의 '다음 점검:' 값. 기본은 조건 문장")
    ap.add_argument("--seconds", type=float, default=180.0, help="수정 블록 검색 시간 상한 초 (기본 180)")
    ap.add_argument("--max-files", type=int, default=400000, help="수정 블록 검색 파일 수 상한 (기본 400000)")
    ap.add_argument("--max-bytes", type=int, default=8_000_000, help="이보다 큰 파일은 수정 블록 검색에서 건너뛴다 (기본 8MB)")
    ap.add_argument("--out", help="결과를 쓸 파일. 없으면 표준 출력")
    args = ap.parse_args()

    root = norm(args.project_root or os.getcwd())
    if not os.path.isdir(root):
        print("오류: 프로젝트 루트 폴더가 없다 — " + root)
        return 2
    today = args.date or datetime.date.today().isoformat()
    marker_re = None
    if args.mod_marker:
        pat = re.escape(args.mod_marker) if args.literal else args.mod_marker
        try:
            marker_re = re.compile(pat.encode("utf-8"))
        except re.error as e:
            print("오류: --mod-marker 정규식이 잘못됐다 — {}".format(e))
            return 2
    engine = args.engine if args.engine != "auto" else detect_engine(root, args.project_file)
    mod_ext = args.mod_ext or (DEFAULT_MOD_EXT_GODOT if engine == "godot" else DEFAULT_MOD_EXT)
    exts = {e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
            for e in mod_ext.split(",") if e.strip()}

    if engine == "godot":
        import tech_inventory_godot
        return tech_inventory_godot.run(args, root, today, marker_re, exts)

    ups, up_hit = find_uproject(root, args.project_file)
    if not ups:
        if args.project_file:
            print("오류: 프로젝트 파일이 없다 — {}".format(args.project_file))
        elif up_hit:
            print("검색 실패({}): 프로젝트 파일을 찾는 중 상한에 걸렸다. --project-file 로 지정할 것".format(up_hit))
        else:
            print("프로젝트 파일(.uproject)을 깊이 3 까지 찾지 못했다. --project-file 로 지정할 것")
        return 2
    if len(ups) > 1:
        print("프로젝트 파일이 여러 개다. --project-file 로 하나를 지정할 것:")
        for u in ups:
            print("- " + u)
        return 2
    uproject = ups[0]
    project_dir = os.path.dirname(uproject)
    engine_root = find_engine_root(uproject, args.engine_root)
    roots_for_show = [("", root)]
    if engine_root and not (engine_root == root or engine_root.startswith(root + os.sep)):
        roots_for_show.insert(0, ("<엔진>", engine_root))

    mod_dirs = resolve_mod_dirs(args.mod_dirs, engine_root, root)

    if (args.mod_list or args.mod_end) and not args.mod_only:
        print("오류: --mod-list 와 --mod-end 는 --mod-only 와 함께 쓴다")
        return 2
    if args.mod_only:
        return run_mod_only(args, mod_dirs, marker_re, exts, today, roots_for_show)

    data, err = read_json(uproject)
    if err:
        print("오류: 프로젝트 파일을 읽지 못했다 — {} ({})".format(uproject, err))
        return 2

    notes = []
    # 게임 코드 폴더: 사용 흔적 검색과 입력 지문이 같은 폴더를 쓴다
    source_roots, unmatched = expand_roots(args.source_roots, root)
    for s in unmatched:
        notes.append("--source-roots 패턴 '{}' 에 맞는 폴더가 없음".format(s))
    # 인자를 줬는데 맞는 폴더가 하나도 없으면 기본 폴더로 바꾸지 않는다. 범위가 몰래 바뀌지 않게 하기 위해서다
    if not args.source_roots:
        source_roots = [norm(os.path.join(project_dir, "Source")), norm(os.path.join(project_dir, "Plugins"))]
    for s in source_roots:
        if not os.path.isdir(s):
            # list_build_cs 는 없는 폴더를 말없이 건너뛴다. 그러면 "사용 흔적 없음"이 확인 실패와 구별되지 않는다
            notes.append("없는 게임 코드 폴더: " + show(s, roots_for_show))
    build_files, b_hit = list_build_cs(source_roots, 30)
    if b_hit:
        notes.append("Build.cs 찾기가 {} 로 중단됨 — '사용 흔적 없음' 은 확인 실패일 수 있고, "
                     "입력 지문도 찾은 파일로만 만들어서 다음 실행에서 지문이 달라질 수 있음".format(b_hit))

    # 입력 지문: 엔진 버전 파일 + 프로젝트 파일 + Config 폴더의 ini + 게임 코드 *.Build.cs + 인자
    config_dir = os.path.join(project_dir, "Config")
    fp_paths = []
    cfg_files = []
    if engine_root:
        fp_paths.append(os.path.join(engine_root, "Build", "Build.version"))
    fp_paths.append(uproject)
    if os.path.isdir(config_dir):
        cfg_budget = Budget(10, 20000)
        for path, depth, dirs, files in walk(config_dir, 4, cfg_budget):
            cfg_files += [os.path.join(path, f) for f in files if f.lower().endswith(".ini")]
        fp_paths += sorted(cfg_files)
    fp_paths += build_files
    fp_extra = [args.mod_marker or "", str(args.literal)] + list(args.mod_dirs) + args.extra_key
    fp_extra += ["src:" + s for s in args.source_roots]
    fp = fingerprint(fp_paths, "|".join(fp_extra), root)

    prev = parse_previous(args.previous)
    age = None
    if prev["date"]:
        try:
            age = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(prev["date"])).days
        except ValueError:
            age = None
    stale = args.stale_days is not None and age is not None and age > args.stale_days
    if prev["fp"] and prev["fp"] == fp and not args.force and not stale:
        if args.stale_days is None:
            age_text = "마지막 갱신 후 지난 일수는 보지 않았다(--stale-days 없음)"
        elif age is None:
            age_text = "직전 목록의 마지막 갱신일을 읽지 못해 지난 일수는 보지 않았다"
        else:
            age_text = "마지막 갱신 후 {}일로 기준 {}일 안이다".format(age, args.stale_days)
        print("변경 없음: 입력 지문 {} 이(가) 직전 목록({})과 같다. 다시 만들지 않았다. "
              "엔진 버전 파일·프로젝트 파일·Config·게임 코드 Build.cs 가 그대로이고, {}. "
              "다시 만들려면 --force.".format(fp, prev["date"] or "날짜 미상", age_text))
        return 0

    # 다시 만드는 이유
    if args.force:
        reason = "--force 로 다시 만듦"
    elif not args.previous:
        reason = "직전 목록을 주지 않음(--previous 없음)"
    elif not os.path.isfile(args.previous):
        reason = "직전 목록 없음 — 처음 만듦"
    elif not prev["fp"]:
        reason = "직전 목록에 입력 지문이 없음"
    elif prev["fp"] != fp:
        reason = "입력 지문이 다름 (직전 {}, 이번 {}) — 엔진 버전 파일·프로젝트 파일·Config·게임 코드 Build.cs·인자 가운데 바뀐 것이 있음".format(prev["fp"], fp)
    else:
        reason = "마지막 갱신({}) 후 {}일 지남 — 기준 {}일(stale_after_days)".format(prev["date"], age, args.stale_days)

    # 엔진 버전
    engine_rows = []
    assoc = data.get("EngineAssociation", "")
    launcher = bool(re.match(r"^\d+\.\d+$", assoc or ""))
    if engine_root:
        bv, berr = read_json(os.path.join(engine_root, "Build", "Build.version"))
        if bv:
            ver = "{}.{}.{}".format(bv.get("MajorVersion"), bv.get("MinorVersion"), bv.get("PatchVersion"))
            engine_rows.append(("엔진 버전", ver, show(os.path.join(engine_root, "Build", "Build.version"), roots_for_show)))
            if launcher and not ver.startswith(assoc + "."):
                notes.append("프로젝트 파일의 EngineAssociation({})과 엔진 폴더의 버전({})이 다르다. 지정한 엔진 폴더가 이 프로젝트의 엔진인지 확인할 것".format(assoc, ver))
        else:
            engine_rows.append(("엔진 버전", "모름 — " + berr, show(os.path.join(engine_root, "Build", "Build.version"), roots_for_show)))
    elif launcher:
        engine_rows.append(("엔진 버전", assoc + " (런처판, 패치 번호 모름)", show(uproject, roots_for_show) + " EngineAssociation"))
    else:
        engine_rows.append(("엔진 버전", "모름 — Build.version 을 못 찾음. --engine-root 로 지정", show(uproject, roots_for_show)))
    if launcher:
        src = "아니오 (EngineAssociation='{}')".format(assoc)
    elif assoc == "":
        src = "예 (EngineAssociation 이 비어 있음)"
    else:
        src = "예로 보임 (EngineAssociation='{}', 버전 번호 형식이 아님)".format(assoc)
    engine_rows.append(("소스 빌드 여부", src, show(uproject, roots_for_show) + " EngineAssociation"))

    # 엔진 수정 블록
    mod_results = []
    mod_hits_all = {}
    if marker_re and mod_dirs:
        mod_results = count_mod_blocks(mod_dirs, marker_re, exts, args.seconds, args.max_files, args.max_bytes)
        for d, n, fail, hits, memo in mod_results:
            mod_hits_all.update(hits)
            if memo:
                notes.append("엔진 수정 블록 검색 {}: {} — 그 파일들의 블록은 세지 않았다".format(show(d, roots_for_show), memo))
        if any(fail for _, _, fail, _, _ in mod_results):
            notes.append("엔진 수정 블록 검색이 끝나지 않아 '엔진을 고쳐서 씀' 상태를 다 가리지 못했다. 그 상태가 없는 것을 '수정 안 함' 으로 읽지 말 것")
            parts = ["{} {}".format(show(d, roots_for_show), fail or "{} 개".format(n)) for d, n, fail, _, _ in mod_results]
            val = "검색 실패 ({})".format("; ".join(parts))
        else:
            total = sum(n for _, n, _, _, _ in mod_results)
            val = "{} ({})".format(total, ", ".join(
                "{} {}{}".format(show(d, roots_for_show), n, " — " + memo if memo else "") for d, n, _, _, memo in mod_results))
        engine_rows.append(("엔진 수정 블록 수", val, "패턴 '{}'{}, 확장자 {}".format(
            args.mod_marker, " 글자 그대로" if args.literal else " 정규식", ",".join(sorted(exts)))))
    else:
        engine_rows.append(("엔진 수정 블록 수", "세지 않음 — 수정 표시 규칙이나 셀 폴더가 주어지지 않음", "프로필 radar.engine_mod_marker, radar.engine_mod_dirs"))

    mods = data.get("Modules", []) or []
    if mods:
        engine_rows.append(("프로젝트 모듈", ", ".join("{}({})".format(m.get("Name"), m.get("Type", "?")) for m in mods), show(uproject, roots_for_show) + " Modules"))
    tps = data.get("TargetPlatforms", []) or []
    if tps:
        engine_rows.append(("프로젝트 파일의 대상 플랫폼", ", ".join(tps), show(uproject, roots_for_show) + " TargetPlatforms"))
    engine_rows.append(("입력 지문", fp, "엔진 버전 파일 + 프로젝트 파일 + Config/*.ini {} 개 + 게임 코드 *.Build.cs {} 개 + 인자의 SHA-256 앞 16자".format(
        len(cfg_files), len(build_files))))

    # 플러그인
    if not engine_root:
        notes.append("엔진 폴더를 못 찾아 엔진 플러그인의 기본 켜짐 값과 성숙도 표시를 읽지 못했다. 런처판이면 설치 폴더를 --engine-root 로 줄 수 있다")
    search_roots = plugin_search_roots(engine_root, project_dir)
    pindex, p_hit = index_plugins(search_roots, 60)
    if p_hit:
        notes.append("플러그인 파일 찾기가 {} 로 중단됨 — '플러그인 파일 못 찾음' 은 확인 실패로 읽을 것".format(p_hit))
    build_names = collect_build_cs(build_files)
    for m in mods:
        for dep in m.get("AdditionalDependencies", []) or []:
            build_names.setdefault(dep.lower(), []).insert(0, (uproject, None))

    # 설정 파일의 섹션 이름: [이름] 또는 [/Script/모듈.클래스] → 첫 위치
    sections = {}
    sec_re = re.compile(r"^\s*\[(?:/Script/)?([A-Za-z_][A-Za-z0-9_]*)[.\]]")
    for cf in cfg_files:
        try:
            with open(cf, "r", encoding="utf-8-sig", errors="replace") as fh:
                for no, line in enumerate(fh, 1):
                    m = sec_re.match(line)
                    if m:
                        sections.setdefault(m.group(1).lower(), (norm(cf), no))
        except OSError:
            continue

    entries = []  # (이름, 켜짐 여부, 프로젝트 파일 항목, 어디서 나왔나)
    listed = set()
    for p in data.get("Plugins", []) or []:
        name = p.get("Name")
        if not name:
            continue
        listed.add(name.lower())
        enabled = bool(p.get("Enabled", False))
        entries.append((name, enabled, p, "프로젝트 파일"))
    # 프로젝트 Plugins 폴더에 있지만 프로젝트 파일에 없는 플러그인 (기본 켜짐 값을 따른다)
    for key, locs in sorted(pindex.items()):
        for kind, up in locs:
            if kind != "프로젝트" or key in listed:
                continue
            pdata, _ = read_json(up)
            en = bool(pdata.get("EnabledByDefault", True)) if pdata else True
            entries.append((os.path.basename(up)[:-8], en, {}, "프로젝트 Plugins 폴더"))
            listed.add(key)
    # 프로젝트 파일에 없지만 수정 블록이 들어 있는 엔진 플러그인 (엔진 기본값을 따른다)
    if mod_hits_all:
        for key, locs in sorted(pindex.items()):
            if key in listed:
                continue
            for kind, up in locs:
                pdir = os.path.dirname(up)
                if kind == "엔진" and any(f.startswith(pdir + os.sep) for f in mod_hits_all):
                    pdata, _ = read_json(up)
                    en = bool(pdata.get("EnabledByDefault", False)) if pdata else False
                    entries.append((os.path.basename(up)[:-8], en, {}, "엔진 기본값"))
                    listed.add(key)
                    break
    # 프로젝트 파일에 없지만 게임 코드가 그 모듈에 의존하는 엔진 플러그인.
    # 게임 코드가 의존해서 빌드되므로 켜져 있다고 본다(엔진 기본값이 꺼짐이면 다른 플러그인의 의존으로 켜진 것).
    dep_budget = Budget(20, 5000)
    for key, locs in sorted(pindex.items()):
        if key in listed:
            continue
        eng = [up for kind, up in locs if kind == "엔진"]
        if not eng:
            continue
        if not dep_budget.tick():
            notes.append("게임 코드가 의존하는 엔진 플러그인 찾기가 {} 로 중단됨 — 목록에서 빠진 엔진 플러그인이 있을 수 있음".format(dep_budget.hit))
            break
        pdata, _ = read_json(eng[0])
        if not pdata:
            continue
        pdir = os.path.dirname(eng[0])
        mnames = [m.get("Name") for m in pdata.get("Modules", []) or [] if m.get("Name")]
        if any(first_outside(build_names.get(mn.lower()), pdir) for mn in mnames):
            entries.append((os.path.basename(eng[0])[:-8], True, {}, "게임 코드 의존"))
            listed.add(key)

    rows = []
    for name, enabled, spec, origin in entries:
        locs = pindex.get(name.lower(), [])
        loc = None
        if locs:
            loc = sorted(locs, key=lambda x: 0 if x[0] == "프로젝트" else 1)[0]
        ev = []
        if origin == "프로젝트 파일":
            ev.append("{} Enabled={}".format(show(uproject, roots_for_show), "true" if enabled else "false"))
        elif origin == "엔진 기본값":
            ev.append("프로젝트 파일에 없음, 엔진 기본값 {} (수정 블록이 있어서 넣음)".format("켜짐" if enabled else "꺼짐"))
        elif origin == "게임 코드 의존":
            ev.append("프로젝트 파일에 없음, 게임 코드가 이 플러그인의 모듈에 의존해서 넣음")
        else:
            ev.append("프로젝트 파일에 없음, 폴더 기본값 {}".format("켜짐" if enabled else "꺼짐"))
        for k in ("TargetAllowList", "TargetDenyList", "PlatformAllowList", "PlatformDenyList", "SupportedTargetPlatforms"):
            if spec.get(k):
                ev.append("{}={}".format(k, "/".join(spec[k])))
        pdata = None
        modules = []
        if loc:
            pdata, perr = read_json(loc[1])
            flags = []
            if pdata:
                for k in ("IsExperimentalVersion", "IsBetaVersion"):
                    if pdata.get(k):
                        flags.append("{}=true".format(k))
                if loc[0] == "엔진" and "EnabledByDefault" in pdata:
                    flags.append("EnabledByDefault={}".format("true" if pdata.get("EnabledByDefault") else "false"))
                modules = [m.get("Name") for m in pdata.get("Modules", []) or [] if m.get("Name")]
            else:
                flags.append(perr)
            ev.append("{} 플러그인 {}{}".format(loc[0], show(loc[1], roots_for_show), " (" + ", ".join(flags) + ")" if flags else ""))
        else:
            ev.append("플러그인 파일 못 찾음" + (" (탐색 중단됨)" if p_hit else ""))
        if not modules:
            modules = [name]
            mod_guess = True
        else:
            mod_guess = False
        own_dir = os.path.dirname(loc[1]) if loc else None
        used_at = None
        self_only = False
        for mname in modules:
            locs_m = build_names.get(mname.lower())
            if not locs_m:
                continue
            hit = first_outside(locs_m, own_dir)
            if hit:
                used_at = (mname, hit)
                break
            self_only = True
        cfg_at = None
        for cname in [name] + modules:
            hit = sections.get(cname.lower())
            if hit:
                cfg_at = (cname, hit)
                break
        modified = []
        if loc:
            pdir = os.path.dirname(loc[1])
            modified = [f for f in mod_hits_all if f.startswith(pdir + os.sep)]

        if not enabled:
            if loc:
                status = STATUS[1]
            elif origin == "프로젝트 파일" and (engine_root is None or p_hit):
                # 프로젝트 파일이 일부러 끈 것은 대개 엔진에 있는 플러그인이다. 확인을 못 했을 뿐이다
                status = STATUS[1]
                ev.append("엔진 폴더를 못 찾았거나 탐색이 중단돼 플러그인 파일은 확인 못 함")
            else:
                status = STATUS[0]
                ev.append("프로젝트 파일에는 꺼짐으로 적혀 있으나 엔진·프로젝트 폴더에서 플러그인 파일을 못 찾음")
            if loc and pdata and pdata.get("EnabledByDefault") and origin == "프로젝트 파일" and loc[0] == "엔진":
                ev.append("엔진 기본은 켜짐인데 프로젝트가 끔 — 끈 이유 확인 필요")
        elif modified:
            status = STATUS[4]
            ev.append("수정 블록 {} 개, 파일 {} 개".format(sum(mod_hits_all[f] for f in modified), len(modified)))
        elif used_at or cfg_at:
            status = STATUS[3]
            if used_at:
                mname, (path, line) = used_at
                where = show(path, roots_for_show) + (":{}".format(line) if line else " AdditionalDependencies")
                ev.append("모듈 {} 의존: {}{}".format(mname, where, " (모듈 이름은 플러그인 이름으로 짐작)" if mod_guess else ""))
            if cfg_at:
                cname, (path, line) = cfg_at
                ev.append("설정 섹션 {}: {}:{}".format(cname, show(path, roots_for_show), line))
        else:
            status = STATUS[2]
            if self_only:
                ev.append("플러그인 자기 폴더 안의 Build.cs 만 그 모듈을 씀")
            ev.append("게임 코드 의존·설정 섹션 없음 — 에셋·에디터 쪽 사용은 텍스트로 확인 못 함")
        rows.append([name, status, "; ".join(ev)])

    # 직전 목록에 있었는데 이번에 없는 것
    current = {r[0] for r in rows}
    for pname, (pid, pstatus) in prev["ids"].items():
        if pname not in current:
            rows.append([pname, STATUS[0], "직전 목록({})에는 '{}' 이었으나 이번에 프로젝트 파일·Plugins 폴더에서 못 찾음".format(prev["date"] or "날짜 미상", pstatus)])

    # ID 부여: 직전 ID 를 이어 쓴다
    used_ids = [int(v[0][3:]) for v in prev["ids"].values()]
    next_id = (max(used_ids) + 1) if used_ids else 1
    changes = []
    for r in rows:
        old = prev["ids"].get(r[0])
        if old:
            r.insert(0, old[0])
            if old[1] != r[2]:
                changes.append("{} {}: {} → {}".format(old[0], r[1], old[1], r[2]))
        else:
            r.insert(0, "TI-{:03d}".format(next_id))
            if prev["ids"]:
                changes.append("TI-{:03d} {}: 새로 들어옴 ({})".format(next_id, r[1], r[2]))
            next_id += 1
    rows.sort(key=lambda r: r[0])

    # 설정
    key_res = [re.compile(k, re.IGNORECASE) for k in DEFAULT_KEYS + args.extra_key]
    cfg_rows, cfg_files, cfg_err = scan_config(config_dir, key_res, 10)
    if cfg_err:
        notes.append(cfg_err)

    # 출력
    if args.next_check:
        next_check = args.next_check
    else:
        next_check = "조건 — 엔진 버전 파일, 프로젝트 파일, Config 폴더, 게임 코드 Build.cs 가 바뀌었을 때{} (기술 동향 고문이 실행마다 입력 지문과 갱신일로 비교)".format(
            ", 또는 마지막 갱신 후 {}일이 지났을 때".format(args.stale_days) if args.stale_days is not None else "")
    out = []
    out.append("# 프로젝트 기술 목록")
    out.append("")
    out.append("다음 점검: " + next_check)
    out.append("작성: radar / 마지막 갱신: {} / 기준 리비전: {}".format(today, args.revision))
    out.append("")
    out.append("## 엔진")
    out.append("| 항목 | 값 | 근거 위치 |")
    out.append("|---|---|---|")
    for a, b, c in engine_rows:
        out.append("| {} | {} | {} |".format(md_cell(a), md_cell(b), md_cell(c)))
    out.append("")
    out.append("## 플러그인·기능")
    out.append("| ID | 이름 | 상태 | 근거 위치 |")
    out.append("|---|---|---|---|")
    for r in rows:
        out.append("| {} | {} | {} | {} |".format(*[md_cell(x) for x in r]))
    out.append("")
    out.append("상태는 다섯 가지 중 하나: " + " / ".join(STATUS))
    out.append("")
    for name, help_text in STATUS_HELP:
        out.append("- {}: {}".format(name, help_text))
    out.append("")
    out.append("목록에 없다는 것만으로 \"없음\"이라고 하지 않는다. 에셋에서만 쓰는 엔진 기본 플러그인은 목록에 없을 수 있다.")
    out.append("")
    out.append("## 주요 렌더링·네트워크 설정")
    out.append("| 설정 | 값 | 근거 위치 |")
    out.append("|---|---|---|")
    if cfg_rows:
        for key, val, path, no, section in cfg_rows:
            out.append("| {} | {} | {}:{} [{}] |".format(md_cell(key), md_cell(val), md_cell(show(path, roots_for_show)), no, md_cell(section)))
    else:
        out.append("| (찾은 설정 없음) | | Config/Default*.ini {} 개 |".format(len(cfg_files)))
    out.append("")
    out.append("## 만든 방법과 검색 기록")
    out.append("- 만든 도구: tech_inventory.py (읽기 전용). 값의 뜻(예: 설정 값 1 이 무엇인지)은 풀지 않았다. 뜻은 엔진 공식 문서로 확인한다.")
    out.append("- 다시 만든 이유: " + reason)
    out.append("- 프로젝트 파일: " + show(uproject, roots_for_show))
    out.append("- 엔진 폴더: " + (show(engine_root, roots_for_show) if engine_root else "못 찾음"))
    out.append("- 플러그인 파일 탐색: {} — .uplugin {} 종{}".format(
        ", ".join(show(r, roots_for_show) for _, r in search_roots) or "없음",
        len(pindex), ", 검색 실패({})".format(p_hit) if p_hit else ""))
    out.append("- 사용 흔적 탐색: {} 의 *.Build.cs {} 개와 프로젝트 파일 의존 목록{}".format(
        ", ".join(show(s, roots_for_show) for s in source_roots), len(build_files), ", 검색 실패({})".format(b_hit) if b_hit else ""))
    out.append("- 설정 탐색: {} (Default*.ini {} 개). 플랫폼별 ini 는 보지 않았다".format(show(config_dir, roots_for_show), len(cfg_files)))
    out.append("- 프로젝트 파일에 없는 엔진 플러그인은 게임 코드가 그 모듈에 의존하거나 수정 블록이 들어 있는 것만 넣었다. "
               "에셋에서만 쓰는 엔진 기본 켜짐 플러그인은 목록에 없을 수 있다")
    out.append("- 사용 흔적은 게임 코드 *.Build.cs·프로젝트 파일의 모듈 의존과 설정 파일의 섹션 이름만 본다. "
               "플러그인 자기 폴더 안의 Build.cs 는 사용 흔적으로 치지 않는다. 에셋 안의 사용은 보지 못한다")
    if mod_results:
        out.append("- 엔진 수정 블록 분포 (블록이 많은 폴더, 셀 폴더 아래 세 단계까지):")
        dist = {}
        for f, n in mod_hits_all.items():
            base = next((r[0] for r in mod_results if f.startswith(r[0] + os.sep)), None)
            if not base:
                continue
            rel = os.path.relpath(os.path.dirname(f), base).split(os.sep)[:3]
            key = os.path.join(base, *rel) if rel and rel[0] != "." else base
            dist[key] = dist.get(key, 0) + n
        for k, n in sorted(dist.items(), key=lambda x: -x[1])[:20]:
            out.append("  - {} : {}".format(show(k, roots_for_show), n))
        if not dist:
            out.append("  - (블록 없음 또는 검색 실패)")
    if prev["ids"]:
        out.append("- 직전 목록({})과 달라진 상태:".format(prev["date"] or "날짜 미상"))
        out += ["  - " + c for c in changes] or ["  - 없음"]
    for n in notes:
        out.append("- 주의: " + n)
    text = "\n".join(out) + "\n"

    if args.out:
        od = os.path.dirname(os.path.abspath(args.out))
        if od and not os.path.isdir(od):
            os.makedirs(od, exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("저장: {} (플러그인 {} 개, 설정 {} 줄, 입력 지문 {})".format(args.out, len(rows), len(cfg_rows), fp))
        print("- 다시 만든 이유: " + reason)
        for a, b, c in engine_rows:
            if a in ("엔진 버전", "엔진 수정 블록 수"):
                print("- {}: {}".format(a, b))
        if prev["ids"]:
            print("- 직전 목록과 달라진 상태: {} 건".format(len(changes)))
            for c in changes:
                print("  - " + c)
        for n in notes:
            print("- 주의: " + n)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
