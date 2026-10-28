#!/usr/bin/env python3
"""Godot 프로젝트의 기술 목록(radar-inventory.md)을 만든다. tech_inventory.py 가 엔진 종류를 보고 부른다(직접 실행하지 않는다).

읽기만 한다. 프로젝트·엔진 파일을 고치지 않는다. 결과는 --out 으로 받은 경로에만 쓰고, 없으면 표준 출력으로 낸다.
출력 형식은 언리얼 판과 같다(advisors 플러그인 shared/state-formats.md 의 radar-inventory.md 형식).

모으는 것
- 엔진 버전: --engine-root 의 version.py(커스텀 빌드) → C# 프로젝트 파일의 Godot.NET.Sdk 버전 →
  project.godot 의 config/features 버전(패치 번호 모름) → config_version 으로 짐작한 큰 버전 순으로 처음 찾은 것.
- 플러그인·기능: addons/ 아래 폴더마다 한 행. plugin.cfg 가 있으면 에디터 플러그인, .gdextension 이 있으면 GDExtension,
  둘 다 없으면 스크립트 애드온이다. addons 밖의 .gdextension 도 한 행씩, project.godot [editor_plugins] 에
  켜짐으로 적혔는데 plugin.cfg 가 없는 것도 한 행씩 넣는다.
- 사용 흔적: 그 애드온 폴더 밖의 게임 코드·씬·리소스(.gd .cs .tscn .tres .gdshader .gdshaderinc)에 있는
  그 폴더의 res:// 경로, 그 애드온이 선언한 class_name 과 C# namespace(using), project.godot 의 autoload 와
  그 애드온 이름의 설정 섹션.
- 설정: project.godot 의 주요 렌더링·물리·네트워크 설정. 찾은 것만 줄 번호와 함께.
- 엔진 수정 블록 수: tech_inventory.py 와 같은 함수로 센다.

다시 만드는 조건 (--previous 를 줬을 때)
- 입력 지문(엔진 version.py, project.godot, export_presets.cfg, *.csproj, plugin.cfg, *.gdextension, 인자)이 직전 목록과 다를 때
- 직전 목록의 마지막 갱신일에서 --stale-days 일이 지났을 때
- --force 를 줬을 때
게임 코드는 자주 바뀌어서 입력 지문에 넣지 않는다. 사용 흔적만 바뀐 것은 --stale-days 가 지나거나 --force 로 다시 만들 때 반영된다.
"""

import datetime
import os
import re
import sys

import godot_project as gp
import tech_inventory as ti

STATUS = ti.STATUS
STATUS_HELP = (
    ("없음", "project.godot [editor_plugins] 에 켜짐으로 적혀 있지만 plugin.cfg 를 못 찾았거나, 직전 목록에 있었는데 이번에 못 찾았다"),
    ("엔진에 있으나 꺼짐", "addons 폴더에 plugin.cfg 가 있는데 [editor_plugins] 에 켜짐으로 적혀 있지 않다. "
     "Godot 은 에디터 플러그인을 꺼도 그 애드온의 런타임 스크립트를 쓸 수 있으므로 근거 칸의 사용 흔적을 함께 본다"),
    ("켜짐·사용 흔적 없음", "켜진 에디터 플러그인, GDExtension, plugin.cfg 없는 스크립트 애드온인데 그 폴더 밖 게임 코드·씬·리소스에서 "
     "res:// 경로, class_name, namespace, autoload, 설정 섹션을 못 찾았다. 에디터 도구만 더하는 플러그인과 "
     "GDExtension 이 등록한 클래스(이름을 텍스트로 알 수 없다)는 흔적이 남지 않으므로 '안 쓴다' 는 뜻이 아니다"),
    ("사용 중", "켜져 있고(또는 늘 쓸 수 있는 GDExtension·스크립트 애드온이고), 위 흔적 가운데 하나가 그 폴더 밖에 있다"),
    ("엔진을 고쳐서 씀", "그 애드온 폴더 안에 수정 블록이 있다(애드온을 고쳐서 씀). 엔진 소스 수정은 엔진 표의 수정 블록 수로 본다. "
     "수정 블록을 세지 않았거나 검색이 실패했으면 이 상태가 없다고 '고치지 않음' 으로 읽지 않는다"),
)
DEFAULT_KEYS = [
    r"rendering/renderer/rendering_method",
    r"rendering/rendering_device/driver",
    r"rendering/gl_compatibility/driver",
    r"rendering/(quality/)?driver/driver_name",
    r"rendering/driver/threads/thread_model",
    r"rendering/global_illumination/.+",
    r"rendering/anti_aliasing/.+",
    r"rendering/scaling_3d/.+",
    r"rendering/lights_and_shadows/.+",
    r"rendering/occlusion_culling/.+",
    r"rendering/mesh_lod/.+",
    r"physics/(2d|3d)/physics_engine",
    r"physics/common/(physics_ticks_per_second|physics_fps|max_physics_steps_per_frame|physics_jitter_fix|physics_interpolation)",
    r"application/run/max_fps",
    r"display/window/vsync/.+",
    r"network/.+",
]
SCAN_EXT = {".gd", ".cs", ".tscn", ".tres", ".gdshader", ".gdshaderinc"}
CODE_EXT = {".gd", ".cs"}
# 애드온 이름과 같아도 그 애드온의 설정 섹션으로 보지 않는 엔진 기본 섹션
CORE_SECTIONS = {
    "application", "autoload", "editor_plugins", "rendering", "physics", "input", "input_devices", "display", "audio",
    "debug", "gui", "layer_names", "filesystem", "internationalization", "navigation", "network", "dotnet", "mono",
    "editor", "importer_defaults", "xr", "threading", "memory", "global_group", "animation", "shader_globals",
}
RES_RE = re.compile(r"res://([^\"'\s)\]]+)")
CLASS_RE = re.compile(r"^[ \t]*(?:@\w+(?:\([^)\n]*\))?[ \t]+)*class_name[ \t]+([A-Za-z_]\w*)", re.M)
NAMESPACE_RE = re.compile(r"^[ \t]*namespace[ \t]+([A-Za-z_][\w.]*)", re.M)
USING_RE = re.compile(r"^[ \t]*using[ \t]+(?:static[ \t]+)?([A-Za-z_][\w.]*)[ \t]*;", re.M)


def find_project(root, given):
    if given:
        p = given if os.path.isabs(given) else os.path.join(root, given)
        return ([ti.norm(p)] if os.path.isfile(p) else []), None
    found = []
    budget = ti.Budget(15, 100000)
    for path, depth, dirs, files in ti.walk(root, 3, budget, skip_names=gp.GODOT_GENERATED_DIRS | {"addons"}):
        if "project.godot" in files:
            found.append(ti.norm(os.path.join(path, "project.godot")))
    return found, budget.hit


def list_units(project_dir, budget):
    """애드온·GDExtension 단위 목록. 단위 = {name, dir, res, cfg, gdext, own, addon}.
    own 은 사용 흔적에서 뺄 자기 폴더, addon 은 addons/ 아래 폴더인지(아니면 addons 밖 .gdextension)."""
    units = []
    adir = os.path.join(project_dir, "addons")
    if os.path.isdir(adir):
        for name in sorted(os.listdir(adir)):
            d = os.path.join(adir, name)
            if not os.path.isdir(d):
                continue
            gdext = []
            for path, depth, dirs, files in ti.walk(d, 6, budget, skip_names=gp.GODOT_GENERATED_DIRS):
                gdext += [ti.norm(os.path.join(path, f)) for f in files if f.endswith(".gdextension")]
            cfg = os.path.join(d, "plugin.cfg")
            units.append({"name": name, "dir": ti.norm(d), "res": "res://addons/{}/".format(name),
                          "cfg": ti.norm(cfg) if os.path.isfile(cfg) else None, "gdext": sorted(gdext), "own": ti.norm(d),
                          "addon": True})
    for path, depth, dirs, files in ti.walk(project_dir, 6, budget, skip_names=gp.GODOT_GENERATED_DIRS | {"addons"}):
        for f in files:
            if not f.endswith(".gdextension"):
                continue
            full = ti.norm(os.path.join(path, f))
            rel = os.path.relpath(full, project_dir).replace(os.sep, "/")
            at_root = ti.norm(path) == ti.norm(project_dir)
            # 프로젝트 폴더 바로 아래 파일이면 폴더 전체가 자기 폴더가 되므로 파일 경로만 본다
            units.append({"name": rel, "dir": ti.norm(path), "cfg": None, "gdext": [full],
                          "res": "res://" + rel if at_root else "res://" + os.path.dirname(rel) + "/",
                          "own": None if at_root else ti.norm(path), "addon": False})
    return units


def declared_names(units, budget, max_bytes):
    """애드온이 선언한 class_name·namespace → 단위 번호. 두 단위가 같은 이름을 선언하면 뺀다."""
    classes, spaces, dup = {}, {}, set()
    for idx, u in enumerate(units):
        if not u["own"]:
            continue
        for path, depth, dirs, files in ti.walk(u["own"], 20, budget, skip_names=gp.GODOT_GENERATED_DIRS):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in CODE_EXT:
                    continue
                fp = os.path.join(path, f)
                try:
                    if os.path.getsize(fp) > max_bytes:
                        continue
                except OSError:
                    continue
                text = gp.read_text(fp)
                if not text:
                    continue
                nc, _ = gp.strip_code(text, ext)
                table, rx = (classes, CLASS_RE) if ext == ".gd" else (spaces, NAMESPACE_RE)
                for m in rx.finditer(nc):
                    name = m.group(1)
                    if table.get(name, idx) != idx:
                        dup.add(name)
                    table[name] = idx
    for name in dup:
        classes.pop(name, None)
        spaces.pop(name, None)
    return classes, spaces, sorted(dup)


def scan_usage(source_roots, units, classes, spaces, budget, max_bytes):
    """단위 번호 → {흔적 종류: (파일, 줄)}. 그 단위 자기 폴더 안의 흔적은 뺀다. 결과: (흔적, 언어별 파일 수, 메모)."""
    hits = {}
    counts = {".gd": 0, ".cs": 0}
    skipped = {"big": 0, "fail": 0}
    name_re = None
    if classes:
        alt = "|".join(re.escape(n) for n in sorted(classes, key=len, reverse=True))
        name_re = re.compile(r"(?<![\w.$])(" + alt + r")(?!\w)")

    def record(idx, kind, fp, text, pos):
        slot = hits.setdefault(idx, {})
        if kind not in slot:
            slot[kind] = (fp, text.count("\n", 0, pos) + 1)

    def owned(fp):
        return {i for i, u in enumerate(units) if u["own"] and fp.startswith(u["own"] + os.sep)}

    for r in source_roots:
        if not os.path.isdir(r):
            continue
        for path, depth, dirs, files in ti.walk(r, 40, budget, skip_names=gp.GODOT_GENERATED_DIRS):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext not in SCAN_EXT:
                    continue
                fp = ti.norm(os.path.join(path, f))
                try:
                    if os.path.getsize(fp) > max_bytes:
                        skipped["big"] += 1
                        continue
                except OSError:
                    skipped["fail"] += 1
                    continue
                text = gp.read_text(fp)
                if text is None:
                    skipped["fail"] += 1
                    continue
                own = owned(fp)
                if ext in counts and not own:
                    counts[ext] += 1
                if ext in CODE_EXT:
                    nc, ns = gp.strip_code(text, ext)
                else:
                    nc = ns = text
                for m in RES_RE.finditer(nc):
                    ref = "res://" + m.group(1)
                    for idx, u in enumerate(units):
                        if idx in own:
                            continue
                        if ref.startswith(u["res"]) if u["res"].endswith("/") else ref == u["res"]:
                            record(idx, "res:// 경로", fp, nc, m.start())
                if ext == ".gd" and name_re:
                    for m in name_re.finditer(ns):
                        idx = classes[m.group(1)]
                        if idx not in own:
                            record(idx, "class_name " + m.group(1), fp, ns, m.start())
                if ext == ".cs" and spaces:
                    for m in USING_RE.finditer(ns):
                        name = m.group(1)
                        idx = next((spaces[s] for s in spaces if name == s or name.startswith(s + ".")), None)
                        if idx is not None and idx not in own:
                            record(idx, "namespace " + name, fp, ns, m.start())
    memo = []
    if skipped["fail"]:
        memo.append("읽기 실패 파일 {} 개".format(skipped["fail"]))
    if skipped["big"]:
        memo.append("크기 상한으로 건너뛴 파일 {} 개".format(skipped["big"]))
    return hits, counts, ", ".join(memo)


def nuget_rows(closure, source_roots, roots_for_show, max_bytes):
    """C# 프로젝트의 NuGet 패키지마다 한 행. 패키지 이름으로 시작하는 namespace 를 using 하거나 그 이름으로 직접 부르면 '사용 중'.
    결과: (행 목록 [이름, 상태, 근거], 주의 한 줄 또는 None)."""
    pkgs = {}
    for cp, plist in closure:
        for name, ver, line in plist:
            pkgs.setdefault(name, []).append((cp, ver, line))
    if not pkgs:
        return [], None
    dirs = list(dict.fromkeys([os.path.dirname(p) for p, _ in closure] + list(source_roots)))
    budget = ti.Budget(60, 300000)
    found = {}
    alt = "|".join(re.escape(n) for n in sorted(pkgs, key=len, reverse=True))
    use_re = re.compile(r"(?<![\w.])(" + alt + r")(?=[.;\s])")
    seen = set()
    for d in dirs:
        for path, depth, sub, files in ti.walk(d, 30, budget, skip_names=gp.GODOT_GENERATED_DIRS | {"bin"}):
            for f in files:
                fp = ti.norm(os.path.join(path, f))
                if not f.endswith(".cs") or fp in seen:
                    continue
                seen.add(fp)
                try:
                    if os.path.getsize(fp) > max_bytes:
                        continue
                except OSError:
                    continue
                text = gp.read_text(fp)
                if not text:
                    continue
                _, ns = gp.strip_code(text, ".cs")
                for m in use_re.finditer(ns):
                    found.setdefault(m.group(1), (fp, ns.count("\n", 0, m.start()) + 1))
    rows = []
    for name, decl in sorted(pkgs.items()):
        ev = ["NuGet 패키지 " + "; ".join("{}:{} Version={}".format(ti.show(cp, roots_for_show), line, ver or "-") for cp, ver, line in decl)]
        hit = found.get(name)
        if hit:
            status = STATUS[3]
            ev.append("namespace 사용: {}:{}".format(ti.show(hit[0], roots_for_show), hit[1]))
        else:
            status = STATUS[2]
            ev.append("패키지 이름으로 시작하는 using·직접 호출 없음 — 패키지 이름과 namespace 가 다르거나 다른 패키지가 끌어 쓰는 것일 수 있다")
        rows.append(["NuGet " + name, status, "; ".join(ev)])
    note = None
    if budget.hit:
        note = "NuGet 패키지 사용 흔적 검색이 {} 로 중단됨 — '켜짐·사용 흔적 없음' 은 확인 실패일 수 있음".format(budget.hit)
    return rows, note


def norm_name(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def run(args, root, today, marker_re, exts):
    engine_root = ti.norm(args.engine_root) if args.engine_root else None
    roots_for_show = [("", root)]
    if engine_root and not (engine_root == root or engine_root.startswith(root + os.sep)):
        roots_for_show.insert(0, ("<엔진>", engine_root))
    mod_dirs = ti.resolve_mod_dirs(args.mod_dirs, engine_root, root)
    if (args.mod_list or args.mod_end) and not args.mod_only:
        print("오류: --mod-list 와 --mod-end 는 --mod-only 와 함께 쓴다")
        return 2
    if args.mod_only:
        return ti.run_mod_only(args, mod_dirs, marker_re, exts, today, roots_for_show)

    projects, p_hit = find_project(root, args.project_file)
    if not projects:
        if args.project_file:
            print("오류: 프로젝트 파일이 없다 — {}".format(args.project_file))
        elif p_hit:
            print("검색 실패({}): 프로젝트 파일을 찾는 중 상한에 걸렸다. --project-file 로 지정할 것".format(p_hit))
        else:
            print("프로젝트 파일(project.godot)을 깊이 3 까지 찾지 못했다. --project-file 로 지정할 것")
        return 2
    if len(projects) > 1:
        print("프로젝트 파일이 여러 개다. --project-file 로 하나를 지정할 것:")
        for p in projects:
            print("- " + p)
        return 2
    project_file = projects[0]
    project_dir = os.path.dirname(project_file)
    facts = gp.project_facts(project_file)
    if "error" in facts:
        print("오류: 프로젝트 파일을 읽지 못했다 — {} ({})".format(project_file, facts["error"]))
        return 2
    pf = ti.show(project_file, roots_for_show)

    notes = []
    source_roots, unmatched = ti.expand_roots(args.source_roots, root)
    for s in unmatched:
        notes.append("--source-roots 패턴 '{}' 에 맞는 폴더가 없음".format(s))
    # 인자를 줬는데 맞는 폴더가 하나도 없으면 기본 폴더로 바꾸지 않는다. 범위가 몰래 바뀌지 않게 하기 위해서다
    if not args.source_roots:
        source_roots = [ti.norm(project_dir)]
    for s in source_roots:
        if not os.path.isdir(s):
            notes.append("없는 게임 코드 폴더: " + ti.show(s, roots_for_show))

    budget = ti.Budget(30, 300000)
    units = list_units(project_dir, budget)
    if budget.hit:
        notes.append("애드온·GDExtension 찾기가 {} 로 중단됨 — 목록이 일부일 수 있음".format(budget.hit))

    # 입력 지문: 엔진 version.py + project.godot + export_presets.cfg + *.csproj + plugin.cfg + *.gdextension + 인자
    csprojs = gp.csproj_files(project_dir)
    fp_paths = []
    if engine_root:
        fp_paths.append(os.path.join(engine_root, "version.py"))
    fp_paths.append(project_file)
    presets = os.path.join(project_dir, "export_presets.cfg")
    if os.path.isfile(presets):
        fp_paths.append(presets)
    fp_paths += csprojs
    # 게임과 함께 빌드되는 C# 프로젝트(ProjectReference 로 이어진 것, res:// 밖 포함)와 그 NuGet 패키지
    closure = gp.csproj_closure(project_dir)
    fp_paths += [p for p, _ in closure if p not in csprojs]
    descriptors = sorted({p for u in units for p in ([u["cfg"]] if u["cfg"] else []) + u["gdext"]})
    fp_paths += descriptors
    fp_extra = ["godot", args.mod_marker or "", str(args.literal)] + list(args.mod_dirs) + args.extra_key
    fp_extra += ["src:" + s for s in args.source_roots]
    fp = ti.fingerprint(fp_paths, "|".join(fp_extra), root)

    prev = ti.parse_previous(args.previous)
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
              "project.godot·export_presets.cfg·C# 프로젝트 파일·plugin.cfg·.gdextension 이 그대로이고, {}. "
              "게임 코드만 바뀐 것은 지문에 들지 않는다. 다시 만들려면 --force.".format(fp, prev["date"] or "날짜 미상", age_text))
        return 0

    if args.force:
        reason = "--force 로 다시 만듦"
    elif not args.previous:
        reason = "직전 목록을 주지 않음(--previous 없음)"
    elif not os.path.isfile(args.previous):
        reason = "직전 목록 없음 — 처음 만듦"
    elif not prev["fp"]:
        reason = "직전 목록에 입력 지문이 없음"
    elif prev["fp"] != fp:
        reason = "입력 지문이 다름 (직전 {}, 이번 {}) — 엔진 version.py·project.godot·export_presets.cfg·C# 프로젝트 파일·plugin.cfg·.gdextension·인자 가운데 바뀐 것이 있음".format(prev["fp"], fp)
    else:
        reason = "마지막 갱신({}) 후 {}일 지남 — 기준 {}일(stale_after_days)".format(prev["date"], age, args.stale_days)

    # 엔진 버전
    engine_rows = []
    sv, spath = gp.engine_source_version(engine_root)
    sdk = [(p, gp.csproj_sdk_version(p)) for p in csprojs]
    sdk_hit = next(((p, v) for p, v in sdk if v), None)
    fver = facts["feature_version"]
    if sv:
        engine_rows.append(("엔진 버전", sv, ti.show(spath, roots_for_show)))
    elif engine_root:
        notes.append("--engine-root({})에 version.py 가 없어 엔진 소스 트리로 읽지 못했다. 엔진 버전은 프로젝트 파일에서 읽었다".format(
            ti.show(engine_root, roots_for_show)))
    if not sv and sdk_hit:
        engine_rows.append(("엔진 버전", sdk_hit[1], ti.show(sdk_hit[0], roots_for_show) + " Godot.NET.Sdk"))
    elif not sv and fver:
        engine_rows.append(("엔진 버전", fver + " (패치 번호 모름)", "{}:{} config/features".format(pf, facts["features_line"])))
    elif not sv and gp.godot_major_guess(facts):
        engine_rows.append(("엔진 버전", gp.godot_major_guess(facts) + " (config_version 으로 짐작)",
                            "{}:{} config_version={}".format(pf, facts["config_version_line"], facts["config_version"])))
    elif not sv:
        engine_rows.append(("엔진 버전", "모름 — config/features 에 버전이 없음", pf))
    if fver and sdk_hit and not sdk_hit[1].startswith(fver + "."):
        notes.append("C# 프로젝트 파일의 Godot.NET.Sdk({})와 project.godot config/features 의 버전({})이 다르다. 어느 쪽이 이 프로젝트의 엔진인지 확인할 것".format(sdk_hit[1], fver))
    if sv and fver and not sv.startswith(fver):
        notes.append("엔진 폴더의 버전({})과 project.godot config/features 의 버전({})이 다르다. 지정한 엔진 폴더가 이 프로젝트의 엔진인지 확인할 것".format(sv, fver))
    if sv:
        src = "예로 보임 (--engine-root 가 엔진 소스 트리)"
    else:
        src = "모름 — Godot 프로젝트 파일에는 적히지 않는다. 프로필 engine.source_build 로 정한다"
    engine_rows.append(("소스 빌드 여부", src, "엔진 폴더 version.py" if sv else "-"))

    mod_results = []
    mod_hits_all = {}
    if marker_re and mod_dirs:
        mod_results = ti.count_mod_blocks(mod_dirs, marker_re, exts, args.seconds, args.max_files, args.max_bytes)
        for d, n, fail, hits, memo in mod_results:
            mod_hits_all.update(hits)
            if memo:
                notes.append("엔진 수정 블록 검색 {}: {} — 그 파일들의 블록은 세지 않았다".format(ti.show(d, roots_for_show), memo))
        if any(fail for _, _, fail, _, _ in mod_results):
            notes.append("엔진 수정 블록 검색이 끝나지 않아 '엔진을 고쳐서 씀' 상태를 다 가리지 못했다. 그 상태가 없는 것을 '수정 안 함' 으로 읽지 말 것")
            parts = ["{} {}".format(ti.show(d, roots_for_show), fail or "{} 개".format(n)) for d, n, fail, _, _ in mod_results]
            val = "검색 실패 ({})".format("; ".join(parts))
        else:
            total = sum(n for _, n, _, _, _ in mod_results)
            val = "{} ({})".format(total, ", ".join(
                "{} {}{}".format(ti.show(d, roots_for_show), n, " — " + memo if memo else "") for d, n, _, _, memo in mod_results))
        engine_rows.append(("엔진 수정 블록 수", val, "패턴 '{}'{}, 확장자 {}".format(
            args.mod_marker, " 글자 그대로" if args.literal else " 정규식", ",".join(sorted(exts)))))
    else:
        engine_rows.append(("엔진 수정 블록 수", "세지 않음 — 수정 표시 규칙이나 셀 폴더가 주어지지 않음", "프로필 radar.engine_mod_marker, radar.engine_mod_dirs"))

    if facts["features"]:
        engine_rows.append(("프로젝트 기능 태그", ", ".join(facts["features"]), "{}:{} config/features".format(pf, facts["features_line"])))

    # 사용 흔적
    sbudget = ti.Budget(90, 400000)
    classes, spaces, dup = declared_names(units, sbudget, args.max_bytes)
    if dup:
        notes.append("두 애드온 이상이 같은 이름을 선언해 사용 흔적에서 뺀 class_name·namespace: " + ", ".join(dup[:20]))
    hits, counts, scan_memo = scan_usage(source_roots, units, classes, spaces, sbudget, args.max_bytes)
    if sbudget.hit:
        notes.append("사용 흔적 검색이 {} 로 중단됨 — '켜짐·사용 흔적 없음' 은 확인 실패일 수 있음".format(sbudget.hit))
    if scan_memo:
        notes.append("사용 흔적 검색: {} — 그 파일들의 흔적은 보지 못했다".format(scan_memo))
    for a in facts["autoloads"]:
        for idx, u in enumerate(units):
            if a["path"].startswith(u["res"]) if u["res"].endswith("/") else a["path"] == u["res"]:
                hits.setdefault(idx, {}).setdefault("autoload " + a["name"], (project_file, a["line"]))
    first_line = {}
    for sec, k, v, no in facts["entries"]:
        if sec:
            first_line.setdefault(sec, no)
    for idx, u in enumerate(units):
        cands = {norm_name(os.path.basename(u["own"]))} if u["own"] else set()
        if u["cfg"]:
            entries, _ = gp.parse_config(u["cfg"])
            pname, _ = gp.lookup(entries, "plugin", "name")
            if pname:
                cands.add(norm_name(gp.unquote(pname)))
        for sec in facts["sections"]:
            top = sec.split("/")[0]
            if top not in CORE_SECTIONS and norm_name(top) in cands - {""}:
                hits.setdefault(idx, {}).setdefault("설정 섹션 [{}]".format(sec), (project_file, first_line[sec]))
                break

    lang = []
    if counts[".gd"]:
        lang.append("GDScript 파일 {} 개".format(counts[".gd"]))
    if csprojs or counts[".cs"]:
        lang.append("C# 파일 {} 개 ({})".format(counts[".cs"], ", ".join(ti.show(p, roots_for_show) for p in csprojs) or "C# 프로젝트 파일 없음"))
    engine_rows.append(("스크립트 언어", ", ".join(lang) or "게임 코드 파일 못 찾음", "게임 코드 폴더의 .gd·.cs (애드온 폴더 제외)"))
    plats, ppath = gp.export_platforms(project_dir)
    if plats:
        engine_rows.append(("내보내기 대상 플랫폼", ", ".join(sorted({p for _, p, _ in plats})), ti.show(ppath, roots_for_show)))
    if facts["autoloads"]:
        engine_rows.append(("autoload", ", ".join(a["name"] for a in facts["autoloads"]), "{} [autoload]".format(pf)))
    engine_rows.append(("입력 지문", fp, "엔진 version.py + project.godot + export_presets.cfg + C# 프로젝트 파일 {} 개 + plugin.cfg·.gdextension {} 개 + 인자의 SHA-256 앞 16자".format(
        len(set(csprojs) | {p for p, _ in closure}), len(descriptors))))

    # 플러그인·기능
    rows = []
    enabled_refs = facts["enabled_plugins"]
    for idx, u in enumerate(units):
        ev = []
        enabled = True
        if u["cfg"]:
            entries, perr = gp.parse_config(u["cfg"])
            meta = []
            for key in ("name", "version"):
                v, _ = gp.lookup(entries, "plugin", key)
                if v:
                    meta.append("{}={}".format(key, gp.unquote(v)))
            if perr:
                meta.append(perr)
            ev.append("에디터 플러그인 {}{}".format(ti.show(u["cfg"], roots_for_show), " (" + ", ".join(meta) + ")" if meta else ""))
            enabled = any(gp.plugin_ref_matches(r, u["name"]) for r in enabled_refs)
            ev.append("{}:{} [editor_plugins] {}".format(pf, facts["enabled_plugins_line"] or "-", "켜짐" if enabled else "켜짐 목록에 없음"))
        for g in u["gdext"]:
            entries, _ = gp.parse_config(g)
            cmin, _ = gp.lookup(entries, "configuration", "compatibility_minimum")
            ev.append("GDExtension {}{}".format(ti.show(g, roots_for_show), " (compatibility_minimum={})".format(gp.unquote(cmin)) if cmin else ""))
        if not u["cfg"] and not u["gdext"]:
            ev.append("plugin.cfg·.gdextension 없음 — 스크립트·리소스 묶음")
        modified = [f for f in mod_hits_all if u["own"] and f.startswith(u["own"] + os.sep)]
        found = hits.get(idx, {})
        found_ev = ["{}: {}{}".format(k, ti.show(p, roots_for_show), ":{}".format(no) if no else "") for k, (p, no) in sorted(found.items())]
        if not enabled:
            status = STATUS[1]
            if found_ev:
                ev.append("꺼져 있지만 사용 흔적 있음 — " + "; ".join(found_ev[:3]))
        elif modified:
            status = STATUS[4]
            ev.append("수정 블록 {} 개, 파일 {} 개".format(sum(mod_hits_all[f] for f in modified), len(modified)))
        elif found_ev:
            status = STATUS[3]
            ev += found_ev[:3]
        else:
            status = STATUS[2]
            ev.append("폴더 밖 게임 코드·씬·리소스에 res:// 경로·class_name·namespace·autoload·설정 섹션 없음 — "
                      "에디터 도구만 더하거나 GDExtension 클래스 이름으로만 쓰는 경우는 텍스트로 확인 못 함")
        rows.append([u["name"], status, "; ".join(e for e in ev if e)])
    pkg_rows, pkg_note = nuget_rows(closure, source_roots, roots_for_show, args.max_bytes)
    rows += pkg_rows
    if pkg_note:
        notes.append(pkg_note)
    for ref in enabled_refs:
        if any(gp.plugin_ref_matches(ref, u["name"]) for u in units if u["cfg"]):
            continue
        m = re.match(r"res://addons/([^/]+)/", ref)
        rows.append([m.group(1) if m else ref, STATUS[0],
                     "{}:{} [editor_plugins] 에 켜짐으로 적혀 있으나 plugin.cfg 를 못 찾음 ({})".format(pf, facts["enabled_plugins_line"], ref)])

    current = {r[0] for r in rows}
    for pname, (pid, pstatus) in prev["ids"].items():
        if pname not in current:
            rows.append([pname, STATUS[0], "직전 목록({})에는 '{}' 이었으나 이번에 addons 폴더·project.godot 에서 못 찾음".format(prev["date"] or "날짜 미상", pstatus)])

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
    cfg_rows = []
    for sec, k, v, no in facts["entries"]:
        full = "{}/{}".format(sec, k) if sec else k
        base = full.split(".", 1)[0]  # 'rendering_method.mobile' 같은 기능 태그별 값도 같은 설정으로 본다
        if any(kr.fullmatch(base) for kr in key_res):
            val = gp.unquote(" ".join(v.split()))
            if len(val) > 120:
                val = val[:117] + "..."
            cfg_rows.append((full, val, no, sec))

    if args.next_check:
        next_check = args.next_check
    else:
        next_check = "조건 — 엔진 version.py, project.godot, export_presets.cfg, C# 프로젝트 파일, plugin.cfg, .gdextension 이 바뀌었을 때{} (기술 동향 고문이 실행마다 입력 지문과 갱신일로 비교)".format(
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
    out.append("| 엔진 | Godot | {} |".format(ti.md_cell(pf)))
    for a, b, c in engine_rows:
        out.append("| {} | {} | {} |".format(ti.md_cell(a), ti.md_cell(b), ti.md_cell(c)))
    out.append("")
    out.append("## 플러그인·기능")
    out.append("| ID | 이름 | 상태 | 근거 위치 |")
    out.append("|---|---|---|---|")
    for r in rows:
        out.append("| {} | {} | {} | {} |".format(*[ti.md_cell(x) for x in r]))
    out.append("")
    out.append("상태는 다섯 가지 중 하나: " + " / ".join(STATUS))
    out.append("")
    for name, help_text in STATUS_HELP:
        out.append("- {}: {}".format(name, help_text))
    out.append("")
    if pkg_rows:
        out.append("- NuGet 행: 게임과 함께 빌드되는 C# 프로젝트의 PackageReference 다. 늘 켜져 있으므로 '사용 중' 아니면 '켜짐·사용 흔적 없음' 이다. "
                   "사용 흔적은 패키지 이름으로 시작하는 namespace 의 using 이나 직접 호출만 본다")
        out.append("")
    out.append("목록에 없다는 것만으로 \"없음\"이라고 하지 않는다. 엔진에 들어 있는 기능(렌더러, 물리 엔진 등)은 플러그인이 아니라 아래 설정 표에서 본다.")
    out.append("")
    out.append("## 주요 렌더링·네트워크 설정")
    out.append("| 설정 | 값 | 근거 위치 |")
    out.append("|---|---|---|")
    if cfg_rows:
        for key, val, no, sec in cfg_rows:
            out.append("| {} | {} | {}:{} [{}] |".format(ti.md_cell(key), ti.md_cell(val), ti.md_cell(pf), no, ti.md_cell(sec)))
    else:
        out.append("| (찾은 설정 없음) | | {} — 적히지 않은 설정은 엔진 기본값이다 |".format(ti.md_cell(pf)))
    out.append("")
    out.append("## 만든 방법과 검색 기록")
    out.append("- 만든 도구: tech_inventory.py --engine godot (tech_inventory_godot.py, 읽기 전용). 값의 뜻(예: 설정 값 2 가 무엇인지)은 풀지 않았다. 뜻은 엔진 공식 문서로 확인한다.")
    out.append("- 다시 만든 이유: " + reason)
    out.append("- 프로젝트 파일: " + pf)
    out.append("- 엔진 폴더: " + (ti.show(engine_root, roots_for_show) if engine_root else "주지 않음(--engine-root 없음) — 공식 배포판이면 필요 없다"))
    out.append("- 플러그인 탐색: {} 아래 폴더 {} 개, addons 밖 .gdextension {} 개".format(
        ti.show(os.path.join(project_dir, "addons"), roots_for_show),
        sum(1 for u in units if u["addon"]), sum(1 for u in units if not u["addon"])))
    out.append("- 사용 흔적 탐색: {} 의 {} 파일. 애드온 자기 폴더 안의 흔적은 치지 않는다. 표시 문자열(대사 등) 안의 class_name 은 치지 않는다".format(
        ", ".join(ti.show(s, roots_for_show) for s in source_roots), " ".join(sorted(SCAN_EXT))))
    out.append("- 설정 탐색: {} 의 [섹션] 키. 기능 태그별 값(예: rendering_method.mobile)도 넣었다. 적히지 않은 설정은 엔진 기본값이라 표에 없다".format(pf))
    if closure:
        out.append("- C# 프로젝트: {} — 게임의 C# 프로젝트 파일과 ProjectReference 로 이어진 프로젝트(테스트 프로젝트는 뺐다). "
                   "NuGet 패키지 행은 이 프로젝트들의 PackageReference 이고, 사용 흔적은 그 폴더와 게임 코드 폴더의 .cs 에서 찾았다".format(
                       ", ".join(ti.show(p, roots_for_show) for p, _ in closure)))
    out.append("- 사용 흔적은 텍스트로 보이는 것만이다. GDExtension 이 등록한 클래스, 에디터에서만 쓰는 도구, 이진 리소스(.res, .scn) 안의 참조는 보지 못한다")
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
            out.append("  - {} : {}".format(ti.show(k, roots_for_show), n))
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
