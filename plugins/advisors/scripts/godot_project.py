#!/usr/bin/env python3
"""Godot 프로젝트 파일 읽기 도우미. profile_scan.py, tech_inventory.py, td 의 godot_graph.py 가 함께 쓴다.

읽기만 한다. 직접 실행하는 스크립트가 아니다.

Godot 의 설정 파일(project.godot, export_presets.cfg, plugin.cfg, *.gdextension, .godot/extension_list.cfg)은
모두 ConfigFile 형식이다: [섹션] 머리 줄, 키=값 줄, ';' 로 시작하는 주석. 값은 여러 줄에 걸칠 수 있다(괄호·따옴표가 닫힐 때까지).
"""

import os
import re

# 생성되는 폴더. 게임 코드나 설정으로 읽지 않는다. bin 은 GDExtension 파일이 들 수 있어서 넣지 않는다
GODOT_GENERATED_DIRS = {".godot", ".import", ".mono", "android", ".git", ".svn", ".vs", ".vscode", ".idea",
                        "__pycache__", "node_modules", "obj"}
_KEY_RE = re.compile(r"^([^=;\[\s][^=]*?)\s*=(.*)$")
_STR_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')
_VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")
_SDK_RE = re.compile(r'Sdk\s*=\s*"Godot\.NET\.Sdk/([0-9][^"]*)"', re.I)


def read_text(path):
    """UTF-8 을 먼저 읽고, 안 되면 CP949, 그래도 안 되면 깨진 글자를 바꿔 읽는다. 못 읽으면 None."""
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


def _balance(text, state):
    """괄호 깊이와 따옴표 상태를 이어서 센다. state = [깊이, 따옴표 안인지]."""
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if state[1]:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                state[1] = False
        elif c == '"':
            state[1] = True
        elif c in "([{":
            state[0] += 1
        elif c in ")]}":
            state[0] -= 1
        i += 1
    return state


def parse_config(path):
    """(항목 목록, 오류). 항목 = (섹션, 키, 원래 값 글, 줄 번호). 섹션 밖의 키는 섹션이 빈 글이다."""
    text = read_text(path)
    if text is None:
        return [], "읽기 실패"
    lines = text.splitlines()
    entries = []
    section = ""
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        i += 1
        if not s or s.startswith(";"):
            continue
        if s.startswith("[") and s.endswith("]"):
            section = s[1:-1].strip()
            continue
        m = _KEY_RE.match(s)
        if not m:
            continue
        start = i
        key, value = m.group(1).strip(), m.group(2).strip()
        state = _balance(value, [0, False])
        # 값이 여러 줄에 걸치면 괄호와 따옴표가 닫힐 때까지 붙인다
        while (state[0] > 0 or state[1]) and i < len(lines):
            value += "\n" + lines[i]
            state = _balance("\n" + lines[i], state)
            i += 1
        entries.append((section, key, value, start))
    return entries, None


def unquote(value):
    """'"글"' 이면 따옴표 안 글. 아니면 앞뒤 공백을 지운 원래 값."""
    v = value.strip()
    m = _STR_RE.fullmatch(v)
    if m:
        return m.group(1).replace('\\"', '"').replace("\\\\", "\\")
    return v


def strings(value):
    """값 안의 따옴표 문자열 목록. PackedStringArray("a", "b") 나 PoolStringArray( "a" ) 에 쓴다."""
    return [s.replace('\\"', '"').replace("\\\\", "\\") for s in _STR_RE.findall(value)]


def lookup(entries, section, key):
    """(값, 줄 번호). 없으면 (None, None). 같은 키가 여러 번 있으면 마지막 것이 이긴다(Godot 과 같다)."""
    hit = (None, None)
    for sec, k, v, no in entries:
        if sec == section and k == key:
            hit = (v, no)
    return hit


def section_items(entries, section):
    return [(k, v, no) for sec, k, v, no in entries if sec == section]


def project_facts(project_file):
    """project.godot 에서 고문이 쓰는 값만 뽑는다. 오류가 있으면 'error' 키가 있다."""
    entries, err = parse_config(project_file)
    facts = {"path": project_file, "entries": entries}
    if err:
        facts["error"] = err
        return facts
    cv, cv_line = lookup(entries, "", "config_version")
    facts["config_version"] = unquote(cv) if cv else ""
    facts["config_version_line"] = cv_line
    name, _ = lookup(entries, "application", "config/name")
    facts["name"] = unquote(name) if name else ""
    feats, feats_line = lookup(entries, "application", "config/features")
    facts["features"] = strings(feats) if feats else []
    facts["features_line"] = feats_line
    facts["feature_version"] = next((f for f in facts["features"] if _VERSION_RE.match(f)), None)
    enabled, enabled_line = lookup(entries, "editor_plugins", "enabled")
    facts["enabled_plugins"] = strings(enabled) if enabled else []
    facts["enabled_plugins_line"] = enabled_line
    facts["autoloads"] = []
    for k, v, no in section_items(entries, "autoload"):
        p = unquote(v)
        facts["autoloads"].append({"name": k, "path": p.lstrip("*"), "singleton": p.startswith("*"), "line": no})
    facts["sections"] = sorted({sec for sec, _, _, _ in entries if sec})
    return facts


def godot_major_guess(facts):
    """config_version 으로 큰 버전을 짐작한다. 5 는 Godot 4, 4 는 Godot 3. 그 밖이면 None."""
    return {"5": "4.x", "4": "3.x"}.get(facts.get("config_version", ""))


def csproj_files(project_dir):
    try:
        return sorted(os.path.join(project_dir, f) for f in os.listdir(project_dir) if f.lower().endswith(".csproj"))
    except OSError:
        return []


def csproj_sdk_version(path):
    """C# 프로젝트 파일의 Godot.NET.Sdk 버전(예: 4.3.0). 없으면 None."""
    text = read_text(path)
    if not text:
        return None
    m = _SDK_RE.search(text)
    return m.group(1) if m else None


_PKG_RE = re.compile(r"<PackageReference\b[^>]*\bInclude\s*=\s*\"([^\"]+)\"([^>]*)>", re.I)
_PKG_VER_RE = re.compile(r"\bVersion\s*=\s*\"([^\"]*)\"", re.I)
_PROJREF_RE = re.compile(r"<ProjectReference\b[^>]*\bInclude\s*=\s*\"([^\"]+)\"", re.I)
TEST_PACKAGES = ("xunit", "nunit", "mstest.testframework", "microsoft.net.test.sdk", "gdunit4.api", "gdunit4.test.adapter")


def csproj_info(path):
    """C# 프로젝트 파일에서 (패키지 목록, 참조 프로젝트 목록, 테스트 프로젝트인지).
    패키지 = (이름, 버전, 줄), 참조 프로젝트 = (절대 경로, 줄). 못 읽으면 ([], [], False)."""
    text = read_text(path)
    if text is None:
        return [], [], False
    line_of = lambda pos: text.count("\n", 0, pos) + 1
    pkgs = []
    for m in _PKG_RE.finditer(text):
        v = _PKG_VER_RE.search(m.group(2))
        pkgs.append((m.group(1), v.group(1) if v else "", line_of(m.start())))
    base = os.path.dirname(path)
    refs = [(os.path.normpath(os.path.join(base, m.group(1).replace("\\", os.sep))), line_of(m.start()))
            for m in _PROJREF_RE.finditer(text)]
    is_test = bool(re.search(r"<IsTestProject>\s*true\s*</IsTestProject>", text, re.I)) or \
        any(p[0].lower() in TEST_PACKAGES for p in pkgs)
    return pkgs, refs, is_test


def csproj_closure(project_dir):
    """Godot 프로젝트의 C# 프로젝트 파일과, 그것이 ProjectReference 로 이어지는 프로젝트 파일 전부(테스트 프로젝트는 뺀다).
    결과: [(경로, 패키지 목록)]. 게임에 함께 빌드되는 코드의 범위다."""
    out, seen = [], set()
    stack = list(csproj_files(project_dir))
    while stack:
        p = os.path.normpath(stack.pop())
        if p in seen or not os.path.isfile(p):
            continue
        seen.add(p)
        pkgs, refs, is_test = csproj_info(p)
        if is_test:
            continue
        out.append((p, pkgs))
        stack += [r for r, _ in refs]
    return sorted(out)


def engine_source_version(engine_root):
    """Godot 엔진 소스 트리의 version.py 에서 (버전, 경로). 소스 트리가 아니면 (None, None)."""
    if not engine_root:
        return None, None
    path = os.path.join(engine_root, "version.py")
    text = read_text(path)
    if not text:
        return None, None
    vals = dict(re.findall(r'^\s*(major|minor|patch|status)\s*=\s*"?([^"\n#]*?)"?\s*$', text, re.M))
    if "major" not in vals or "minor" not in vals:
        return None, None
    v = "{}.{}".format(vals["major"], vals["minor"])
    if vals.get("patch") and vals["patch"] != "0":
        v += "." + vals["patch"]
    if vals.get("status"):
        v += "-" + vals["status"]
    return v, path


def export_platforms(project_dir):
    """export_presets.cfg 의 (프리셋 이름, 플랫폼, 줄) 목록."""
    path = os.path.join(project_dir, "export_presets.cfg")
    if not os.path.isfile(path):
        return [], None
    entries, err = parse_config(path)
    out = []
    for sec, k, v, no in entries:
        if re.fullmatch(r"preset\.\d+", sec) and k == "platform":
            name, _ = lookup(entries, sec, "name")
            out.append((unquote(name) if name else sec, unquote(v), no))
    return out, path


def res_to_path(res, project_dir):
    """res://a/b → <프로젝트 폴더>/a/b. res:// 가 아니면 None."""
    if not res.startswith("res://"):
        return None
    return os.path.normpath(os.path.join(project_dir, res[len("res://"):].replace("/", os.sep)))


def plugin_ref_matches(ref, folder):
    """[editor_plugins] enabled 항목이 addons/<folder> 를 가리키는가. Godot 4 는 plugin.cfg 경로, 3.0 무렵은 폴더 이름만 적는다."""
    r = ref.replace("\\", "/").rstrip("/")
    return r == folder or r.startswith("res://addons/{}/".format(folder))


def strip_code(text, ext):
    """(주석을 지운 글, 주석과 문자열 안까지 지운 글). 줄바꿈 위치는 그대로 둔다(줄 번호 계산용).

    res:// 경로는 문자열 안에 있으므로 앞의 것에서, class_name 사용은 대사 같은 글에 걸리지 않게 뒤의 것에서 찾는다.
    """
    nc, ns = list(text), list(text)
    gd = ext == ".gd"
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if (gd and c == "#") or (not gd and text.startswith("//", i)):
            j = text.find("\n", i)
            j = n if j < 0 else j
            for k in range(i, j):
                nc[k] = ns[k] = " "
            i = j
        elif not gd and text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if text[k] != "\n":
                    nc[k] = ns[k] = " "
            i = j
        elif c in "\"'":
            q = c * 3 if gd and text.startswith(c * 3, i) else c
            j = i + len(q)
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text.startswith(q, j) or (len(q) == 1 and text[j] == "\n"):
                    break
                j += 1
            for k in range(i + len(q), min(j, n)):
                if text[k] != "\n":
                    ns[k] = " "
            i = min(n, j + len(q))
        else:
            i += 1
    return "".join(nc), "".join(ns)
