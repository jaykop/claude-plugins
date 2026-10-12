#!/usr/bin/env python3
"""프로젝트 폴더에서 고문 프로필에 넣을 값을 찾아 출력한다.

읽기만 한다. 파일을 만들거나 고치지 않는다.
찾는 것: 버전 관리 종류, 언리얼 프로젝트 파일(.uproject), 엔진 버전, 문서가 많은 폴더, 테스트 코드 흔적.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKIP_DIRS = {
    ".git", ".svn", ".vs", ".vscode", ".idea", "node_modules", "__pycache__",
    "Binaries", "Intermediate", "Saved", "DerivedDataCache", "Build", ".claude",
}
# 엔진 소스·템플릿·샘플 안의 .uproject 는 프로젝트가 아니다
SKIP_NESTED = {"Engine", "Templates", "Samples", "FeaturePacks"}
TEST_PATTERNS = re.compile(
    rb"IMPLEMENT_SIMPLE_AUTOMATION_TEST|IMPLEMENT_COMPLEX_AUTOMATION_TEST|BEGIN_DEFINE_SPEC|TEST_CLASS\s*\("
)


class Budget:
    """탐색 시간과 개수 상한."""

    def __init__(self, seconds, max_entries):
        self.deadline = time.monotonic() + seconds
        self.max_entries = max_entries
        self.entries = 0
        self.hit = None  # 상한에 걸리면 이유

    def tick(self):
        self.entries += 1
        if self.entries > self.max_entries:
            self.hit = "개수 상한"
        elif time.monotonic() > self.deadline:
            self.hit = "시간 초과"
        return self.hit is None


def walk(root, max_depth, budget, skip_plugins=True):
    """(경로, 깊이, 하위 폴더 목록, 파일 목록) 을 깊이 우선으로 돌려준다."""
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
                            if entry.name in SKIP_DIRS:
                                continue
                            if skip_plugins and entry.name == "Plugins":
                                continue
                            if skip_plugins and entry.name in SKIP_NESTED:
                                continue
                            dirs.append(entry.name)
                        else:
                            files.append(entry.name)
                    except OSError:
                        continue
        except OSError:
            continue
        yield path, depth, dirs, files
        if depth < max_depth:
            for d in dirs:
                stack.append((os.path.join(path, d), depth + 1))


def detect_vcs(root):
    found = []
    probe = os.path.abspath(root)
    for _ in range(6):
        if os.path.isdir(os.path.join(probe, ".git")):
            found.append(("git", probe))
            break
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    p4config_name = os.environ.get("P4CONFIG")
    probe = os.path.abspath(root)
    for _ in range(6):
        for name in filter(None, [p4config_name, ".p4config", "p4config.txt"]):
            if os.path.isfile(os.path.join(probe, name)):
                found.append(("p4", os.path.join(probe, name)))
                break
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    if not found:
        client = p4_client_for(root)
        if client:
            found.append(("p4", "작업 공간 " + client))
        else:
            # 루트는 작업 공간 밖이고 하위 폴더만 매핑된 경우 (예: 루트/Dev 만 작업 공간)
            try:
                subs = sorted(e.name for e in os.scandir(root) if e.is_dir() and not e.name.startswith("."))[:20]
            except OSError:
                subs = []
            for name in subs:
                client = p4_client_for(os.path.join(root, name))
                if client:
                    found.append(("p4", "작업 공간 {} — 루트가 아니라 하위 폴더 '{}' 만 매핑됨".format(client, name)))
                    break
    return found


def p4_client_for(root):
    """이 폴더가 p4 작업 공간 안인지 본다. 읽기 명령(p4 where)만, 5초 상한.

    p4 info 만 보면 환경 변수에 잡힌 작업 공간 이름이 어느 폴더에서나 나오므로,
    p4 where 로 이 폴더가 실제로 작업 공간에 매핑되는지 확인한다.
    """
    target = os.path.join(root, "...")
    try:
        # -d 로 현재 폴더를 알려 준다. 안 주면 p4 가 부모 셸의 PWD 를 보고 다른 루트(AltRoots)를 고른다
        r = subprocess.run(["p4", "-d", root, "-ztag", "where", target], cwd=root, capture_output=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    text = r.stdout.decode("utf-8", "replace")
    if "... depotFile" not in text:
        return None
    try:
        info = subprocess.run(["p4", "-d", root, "-ztag", "info"], cwd=root, capture_output=True, timeout=5)
        m = re.search(r"^\.\.\. clientName (.+)$", info.stdout.decode("utf-8", "replace"), re.M)
        return m.group(1).strip() if m else "이름 모름"
    except (OSError, subprocess.SubprocessError):
        return "이름 모름"


def read_json(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f), None
    except (OSError, ValueError) as e:
        return None, str(e)


def find_engine_version(uproject_path, engine_hint):
    """소스 빌드면 Engine/Build/Build.version 을 찾는다. 런처판이면 EngineAssociation 만 돌려준다."""
    candidates = []
    if engine_hint:
        candidates.append(os.path.join(engine_hint, "Build", "Build.version"))
        candidates.append(os.path.join(engine_hint, "Engine", "Build", "Build.version"))
    probe = os.path.dirname(os.path.abspath(uproject_path))
    for _ in range(4):
        candidates.append(os.path.join(probe, "Engine", "Build", "Build.version"))
        parent = os.path.dirname(probe)
        if parent == probe:
            break
        probe = parent
    for c in candidates:
        if os.path.isfile(c):
            data, err = read_json(c)
            if data:
                v = "{}.{}.{}".format(data.get("MajorVersion"), data.get("MinorVersion"), data.get("PatchVersion"))
                return v, c
    return None, None


def main():
    ap = argparse.ArgumentParser(description="고문 프로필에 넣을 값을 프로젝트 폴더에서 찾아 출력한다 (읽기 전용).")
    ap.add_argument("project_root", nargs="?", default="", help="프로젝트 루트 폴더. 없거나 빈 값이면 현재 폴더")
    ap.add_argument("--engine-root", help="엔진 소스 폴더를 알면 지정 (Build.version 탐색용)")
    ap.add_argument("--max-depth", type=int, default=4, help="폴더 탐색 깊이 (기본 4)")
    ap.add_argument("--seconds", type=float, default=20.0, help="탐색 시간 상한 초 (기본 20)")
    ap.add_argument("--max-entries", type=int, default=200000, help="탐색 항목 수 상한 (기본 200000)")
    ap.add_argument("--json", action="store_true", help="JSON 으로 출력")
    args = ap.parse_args()

    root = os.path.abspath(args.project_root or os.getcwd())
    if not os.path.isdir(root):
        print("오류: 폴더가 없다 — " + root)
        return 2

    out = {"project_root": root, "vcs": [], "uprojects": [], "doc_folders": [], "test_files": [], "notes": []}
    out["vcs"] = [{"type": k, "evidence": v} for k, v in detect_vcs(root)]

    budget = Budget(args.seconds, args.max_entries)
    md_count = {}
    source_dirs = []
    for path, depth, dirs, files in walk(root, args.max_depth, budget):
        for name in files:
            low = name.lower()
            if low.endswith(".uproject"):
                out["uprojects"].append(os.path.join(path, name))
            elif low.endswith(".md"):
                rel = os.path.relpath(path, root)
                top = rel.split(os.sep)[:2]
                key = os.path.join(*top) if top and top[0] != "." else "."
                md_count[key] = md_count.get(key, 0) + 1
        if os.path.basename(path) == "Source" and depth <= args.max_depth:
            source_dirs.append(path)
    if budget.hit:
        out["notes"].append("폴더 탐색이 {} 로 중단됨 — 결과가 일부만일 수 있다. --seconds 나 --max-depth 를 조정하거나 하위 폴더를 직접 지정할 것.".format(budget.hit))

    for up in out["uprojects"]:
        data, err = read_json(up)
        info = {"path": up}
        if err:
            info["error"] = "읽기 실패: " + err
        else:
            assoc = data.get("EngineAssociation", "")
            info["engine_association"] = assoc
            info["source_build_guess"] = (assoc == "" or not re.match(r"^\d+\.\d+$", assoc))
            plugins = data.get("Plugins", []) or []
            info["plugins_total"] = len(plugins)
            info["plugins_enabled"] = sum(1 for p in plugins if p.get("Enabled", False))
            info["plugins_disabled"] = [p.get("Name") for p in plugins if not p.get("Enabled", False)]
            info["modules"] = [m.get("Name") for m in data.get("Modules", []) or []]
            info["target_platforms"] = data.get("TargetPlatforms", [])
            v, vpath = find_engine_version(up, args.engine_root)
            if v:
                info["engine_version"] = v
                info["engine_version_source"] = vpath
            elif re.match(r"^\d+\.\d+$", assoc or ""):
                info["engine_version"] = assoc + " (런처판, 패치 번호 모름)"
            else:
                info["engine_version"] = "모름 — Build.version 을 못 찾음. --engine-root 로 지정"
        # 측정 파일 폴더: Saved 는 탐색에서 빼므로 여기서 따로 본다
        prof = os.path.join(os.path.dirname(up), "Saved", "Profiling")
        if os.path.isdir(prof):
            counts = {"utrace": 0, "csv": 0}
            pbudget = Budget(5.0, 20000)
            for path, depth, dirs, files in walk(prof, 4, pbudget, skip_plugins=False):
                for name in files:
                    low = name.lower()
                    if low.endswith(".utrace"):
                        counts["utrace"] += 1
                    elif low.endswith(".csv") or low.endswith(".csv.gz"):
                        counts["csv"] += 1
            info["profiling_dir"] = prof
            info["profiling_counts"] = counts
            if pbudget.hit:
                info["profiling_note"] = "측정 파일 개수 세기가 {} 로 중단됨 — 최소 값".format(pbudget.hit)
        else:
            info["profiling_dir"] = None
        out.setdefault("uproject_info", []).append(info)

    out["doc_folders"] = sorted(([k, n] for k, n in md_count.items() if n >= 5), key=lambda x: -x[1])[:15]

    # 테스트 코드 흔적: 프로젝트 파일 옆 Source 폴더를 먼저 보고, 프로젝트 파일이 없을 때만 찾은 Source 폴더를 본다
    project_sources = []
    for info in out.get("uproject_info", []):
        sd = os.path.join(os.path.dirname(info["path"]), "Source")
        if os.path.isdir(sd):
            project_sources.append(sd)
    scan_dirs = project_sources or source_dirs[:5]
    out["test_scan_dirs"] = scan_dirs
    tbudget = Budget(max(5.0, args.seconds / 2), 50000)
    for sd in scan_dirs:
        for path, depth, dirs, files in walk(sd, 8, tbudget, skip_plugins=False):
            for name in files:
                if not name.endswith((".cpp", ".h")):
                    continue
                fp = os.path.join(path, name)
                try:
                    with open(fp, "rb") as f:
                        if TEST_PATTERNS.search(f.read(2_000_000)):
                            out["test_files"].append(fp)
                except OSError:
                    continue
            if len(out["test_files"]) >= 30:
                break
    if tbudget.hit:
        out["notes"].append("테스트 코드 검색이 {} 로 중단됨 — 0건이어도 '없음'으로 단정하지 말 것.".format(tbudget.hit))

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0

    print("# 프로필 스캔 결과 (읽기 전용)")
    print("- 프로젝트 루트: " + root)
    if out["vcs"]:
        for v in out["vcs"]:
            print("- 버전 관리: {} ({})".format(v["type"], v["evidence"]))
    else:
        print("- 버전 관리: 찾지 못함 — 사용자에게 확인")
    infos = out.get("uproject_info", [])
    if not infos:
        print("- 언리얼 프로젝트 파일: 찾지 못함 (깊이 {} 까지)".format(args.max_depth))
    for info in infos:
        print("- 프로젝트 파일: " + info["path"])
        if "error" in info:
            print("  - " + info["error"])
            continue
        print("  - EngineAssociation: '{}'{}".format(info["engine_association"], " → 소스 빌드로 보임" if info["source_build_guess"] else ""))
        print("  - 엔진 버전: {}{}".format(info["engine_version"], " ({})".format(info.get("engine_version_source")) if info.get("engine_version_source") else ""))
        if info.get("engine_version_source"):
            # .../Engine/Build/Build.version → .../Engine
            print("  - 엔진 폴더 후보 (engine.root): " + os.path.dirname(os.path.dirname(info["engine_version_source"])))
        print("  - 플러그인: {} 개 중 {} 개 켜짐".format(info["plugins_total"], info["plugins_enabled"]))
        if info["plugins_disabled"]:
            print("  - 일부러 끈 플러그인: " + ", ".join(str(x) for x in info["plugins_disabled"]))
        print("  - 모듈: " + ", ".join(str(x) for x in info["modules"]))
        if info["target_platforms"]:
            print("  - TargetPlatforms: " + ", ".join(info["target_platforms"]))
        if info.get("profiling_dir"):
            c = info["profiling_counts"]
            print("  - 측정 파일 폴더: {} (.utrace {} 개, .csv {} 개){}".format(
                info["profiling_dir"], c["utrace"], c["csv"],
                " — " + info["profiling_note"] if info.get("profiling_note") else ""))
        else:
            print("  - 측정 파일 폴더: Saved/Profiling 없음")
    print("- 마크다운 문서가 5개 이상인 폴더 (기획서 후보, 위 2단계 기준):")
    for k, n in out["doc_folders"]:
        print("  - {} : {} 개".format(k, n))
    if out["test_files"]:
        print("- 자동화 테스트가 있는 파일 (최대 30): {} 개".format(len(out["test_files"])))
        for fp in out["test_files"][:10]:
            print("  - " + fp)
    else:
        print("- 자동화 테스트 파일: 찾지 못함 (검색한 폴더: " + ", ".join(out["test_scan_dirs"]) + ")")
    for n in out["notes"]:
        print("- 주의: " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
