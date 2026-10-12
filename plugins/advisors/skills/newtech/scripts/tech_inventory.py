#!/usr/bin/env python3
"""언리얼 프로젝트의 기술 목록(newtech-inventory.md)을 만든다.

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

출력 형식은 advisors 플러그인 shared/state-formats.md 의 newtech-inventory.md 형식을 따른다.
"""

import argparse
import concurrent.futures
import datetime
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


def count_mod_blocks(dirs, marker_re, exts, seconds, max_files, max_bytes, workers=8):
    """폴더별 수정 블록 수. 결과: [(폴더, 개수 또는 None, 실패 이유, 블록이 있는 파일 {경로: 개수}, 메모)].

    파일 목록을 먼저 모은 뒤 여러 스레드로 읽는다. 묶음마다 시간 상한을 확인하고,
    상한에 걸린 폴더와 그 뒤 폴더는 개수 대신 '검색 실패' 를 돌려준다(0 으로 치지 않는다).
    읽지 못한 파일과 크기 상한으로 건너뛴 파일은 개수를 메모에 남긴다.
    """

    def scan(fp):
        try:
            if os.path.getsize(fp) > max_bytes:
                return fp, "big"
            with open(fp, "rb") as fh:
                return fp, len(marker_re.findall(fh.read()))
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


def main():
    ap = argparse.ArgumentParser(
        description="언리얼 프로젝트의 기술 목록(newtech-inventory.md)을 만든다. 프로젝트·엔진 파일은 읽기만 한다.")
    ap.add_argument("project_root", help="프로젝트 루트 폴더 (근거 위치를 이 폴더 기준 상대 경로로 적는다)")
    ap.add_argument("--project-file", help="프로젝트 파일(.uproject) 경로. 상대 경로면 프로젝트 루트 기준. 없으면 깊이 3 까지 찾는다")
    ap.add_argument("--engine-root", help="엔진 폴더(안에 Build/Build.version 이 있는 폴더). 없으면 프로젝트 파일 위쪽에서 찾는다")
    ap.add_argument("--mod-marker", help="엔진 수정 블록의 시작 줄을 찾는 정규식 (예: 'MYGAME_BEGIN')")
    ap.add_argument("--literal", action="store_true", help="--mod-marker 를 정규식이 아니라 글자 그대로 찾는다")
    ap.add_argument("--mod-dirs", nargs="*", default=[], help="수정 블록을 셀 폴더들. 상대 경로면 엔진 폴더 기준, 거기 없으면 프로젝트 루트 기준")
    ap.add_argument("--mod-ext", default=DEFAULT_MOD_EXT, help="수정 블록을 찾을 파일 확장자, 쉼표로 구분 (기본: {})".format(DEFAULT_MOD_EXT))
    ap.add_argument("--mod-only", action="store_true", help="목록은 만들지 않고 --mod-dirs 의 수정 블록 수만 출력한다")
    ap.add_argument("--source-roots", nargs="*", default=[], help="게임 코드 폴더들 (사용 흔적 검색). 없으면 프로젝트 파일 옆 Source 와 Plugins")
    ap.add_argument("--extra-key", action="append", default=[], help="더 볼 설정 이름 정규식 (여러 번 줄 수 있음)")
    ap.add_argument("--previous", help="직전 newtech-inventory.md. 주면 ID 를 이어 쓰고, 입력 지문이 같고 --stale-days 안이면 다시 만들지 않는다")
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

    root = norm(args.project_root)
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
    exts = {e.strip().lower() if e.strip().startswith(".") else "." + e.strip().lower()
            for e in args.mod_ext.split(",") if e.strip()}

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

    mod_dirs = []
    for d in args.mod_dirs:
        if os.path.isabs(d):
            mod_dirs.append(norm(d))
            continue
        # 상대 경로는 엔진 폴더 기준으로 먼저 보고, 없으면 프로젝트 루트 기준으로 본다
        cands = [os.path.join(b, d) for b in (engine_root, root) if b]
        mod_dirs.append(norm(next((c for c in cands if os.path.isdir(c)), cands[0])))

    if args.mod_only:
        if not marker_re or not mod_dirs:
            print("오류: --mod-only 에는 --mod-marker 와 --mod-dirs 가 필요하다")
            return 2
        res = count_mod_blocks(mod_dirs, marker_re, exts, args.seconds, args.max_files, args.max_bytes)
        print("# 엔진 수정 블록 수 (읽기 전용, {})".format(today))
        print("- 패턴: {}{}".format(args.mod_marker, " (글자 그대로)" if args.literal else " (정규식)"))
        for d, n, fail, hits, memo in res:
            print("- {}: {}{}".format(show(d, roots_for_show), fail if fail else "{} 개, 파일 {} 개".format(n, len(hits)),
                                      " ({})".format(memo) if memo else ""))
            for fp, c in sorted(hits.items(), key=lambda x: -x[1])[:15]:
                print("  - {} : {}".format(show(fp, roots_for_show), c))
        return 0

    data, err = read_json(uproject)
    if err:
        print("오류: 프로젝트 파일을 읽지 못했다 — {} ({})".format(uproject, err))
        return 2

    notes = []
    # 게임 코드 폴더: 사용 흔적 검색과 입력 지문이 같은 폴더를 쓴다
    source_roots = [norm(s if os.path.isabs(s) else os.path.join(root, s)) for s in args.source_roots]
    if not source_roots:
        source_roots = [norm(os.path.join(project_dir, "Source")), norm(os.path.join(project_dir, "Plugins"))]
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
        engine_rows.append(("엔진 수정 블록 수", "세지 않음 — 수정 표시 규칙이나 셀 폴더가 주어지지 않음", "프로필 newtech.engine_mod_marker, newtech.engine_mod_dirs"))

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
        next_check = "조건 — 엔진 버전 파일, 프로젝트 파일, Config 폴더, 게임 코드 Build.cs 가 바뀌었을 때{} (신기술 고문이 실행마다 입력 지문과 갱신일로 비교)".format(
            ", 또는 마지막 갱신 후 {}일이 지났을 때".format(args.stale_days) if args.stale_days is not None else "")
    out = []
    out.append("# 프로젝트 기술 목록")
    out.append("")
    out.append("다음 점검: " + next_check)
    out.append("작성: newtech / 마지막 갱신: {} / 기준 리비전: {}".format(today, args.revision))
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
