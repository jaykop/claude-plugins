#!/usr/bin/env python3
"""ko-review 기계적 검사기.

한국어 Markdown 문서에서 판단이 필요 없는 항목만 검사한다. 읽기만 하고 파일을 고치지 않는다.
직역투 판정, 주술 호응, 어조 혼용처럼 판단이 필요한 항목은 검사하지 않는다(polish 스킬 본문에서 검토).

사용법:
    python doc_check.py <file1> [<file2> ...]
    python doc_check.py --tree <디렉터리>        # 하위 .md 전체 (파일 사이 표기 갈림 검출용)
    python doc_check.py --terms <terms.json> <file>   # 프로젝트 전용 목록을 함께 쓴다

프로젝트 전용 목록: --terms 를 주지 않으면 프로젝트 루트의 .claude/ko-review/terms.json 이 있을 때 읽는다.
형식은 플러그인의 shared/terms-format.md 를 따른다.

출력: 검사 항목별 결과. 확정 문제가 하나라도 있으면 exit code 1.
      참고 항목(informational)은 exit code 에 영향 없음.
"""
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

BOM = b"\xef\xbb\xbf"

# ---------------------------------------------------------------------------
# 금지어 -> 대체어 (확정 문제)
#
# 영어권 개발 문화의 비유를 낱말째 옮긴 표현. 실제 문서에서 확인된 것만 쌓는다.
# 이 목록은 규칙이 아니라 이미 새어나간 것들의 기록이다. 프로젝트마다 다른 낱말은 terms.json 에 둔다.
# ---------------------------------------------------------------------------
BANNED = {
    "논리 구멍": "빠진 경우 / 규칙이 안 다루는 경우",
    "폴백": "대체 (에디터 필드명 Fallback 은 그대로)",
    "센티넬": "잘못 넘어가는 걸 막는 장치",
    "스테일": "낡음 / 갱신 안 됨",
    "냄새가 난": "나중에 문제가 될 것 같",
    "냄새나는": "허술한 / 의심되는",
    "제품 코드": "실제 코드 (production code 를 낱말째 옮긴 말)",
    "관문": (
        "조건 / 단계 (gate 직역. '각각 다른 관문이다' -> '각각 다른 이유로 필요하다'). "
        "게임 안의 실제 문·관문이 주어면 그대로 둔다"
    ),
}

# 문맥에 따라 정상일 수 있어 참고로만 보고하는 낱말
BANNED_SOFT = {
    "계약": (
        "contract 직역일 수 있다 -> 지켜야 하는 규격 / 규정 (채널 계약 -> 채널별 응답 규정). "
        "'API 계약', '사용 계약'처럼 프로젝트가 용어로 정해 쓰는 곳이면 그대로 둔다"
    ),
    "구멍": "빠진 경우 / 안 다루는 경우 — '구멍'이 비유로 쓰였는지 확인",
    "리프": "끝단 / 말단",
    "고아": "지워지지 않고 남은 / 주인 없이 남은 — 데이터·객체가 주어면 영어 비유(orphan). 인물이 주어면 그대로 둔다",
}

# ---------------------------------------------------------------------------
# 정규식이 필요한 금지어 — 확정 문제
#
# 낱말이 다른 말 속에 흔히 섞여서 단순 포함 검사로는 오탐이 난다. 앞뒤 경계를 건다.
# ---------------------------------------------------------------------------
BANNED_PATTERNS = {
    r"화면\s*(을\s*)?(소유|쥐)": (
        "'화면을 소유한다ㆍ쥐고 있다' 는 영어 비유 -> 활성인 / 유지되는 / 지금 그리는 "
        "(하드락이 화면을 소유 중이면 -> 하드락이 활성이면)"
    ),
    r"기동(?!력|성|대|전)": (
        "'기동' 은 기계·부대에 붙는 말 -> 시작 / 걸다 / 켜다 "
        "(보간을 기동한다 -> 보간을 시작한다). 기동력·기동성·기동대는 정상"
    ),
    r"[぀-ゟ゠-ヿ]": (
        "일본어 가나가 섞였다 -> 한국어로 옮긴다 (パイプライン -> 파이프라인)"
    ),
    r"손이\s*갈(리|린|립|려|렸)": (
        "국어사전에 없는 관용구를 지어낸 말 -> 무엇이 어떻게 갈리는지 그대로 쓴다. "
        "'여기서 손이 갈립니다' -> '여기서부터는 일부를 직접 해야 한다'. "
        "지어낸 관용구는 읽는 쪽이 뜻부터 되물어야 한다"
    ),
}

# ---------------------------------------------------------------------------
# 정규식이 필요한 금지어 — 참고 보고
#
# 같은 낱말이 정상일 수 있어(캐릭터가 죽는다) 확정으로 못 잡는다. 주어가 무엇인지로 갈리므로 사람이 판단한다.
# ---------------------------------------------------------------------------
BANNED_SOFT_PATTERNS = {
    r"죽(은|는|어|음|였|인)|살아\s?있|살린|살려": (
        "기능·코드·값이 주어면 영어 비유(dead/alive) -> "
        "비활성 / 동작 안 함 / 적용 안 됨 / 안 쓰이는, 활성 / 동작 중. "
        "캐릭터·유닛이 주어면 그대로 둔다"
    ),
    r"열려\s*있|열어\s*(둔|두|놓)": (
        "결정·질문·선택지가 주어면 영어 직역(open question / leave open) -> "
        "아직 정하지 않은 것 / 나중에 쓸 수 있게 남겨 둔다. "
        "파일이 주어고 작업 상태를 뜻하면 -> 수정 중이다 / 스테이징돼 있다. "
        "문·창·경로가 주어면 그대로 둔다"
    ),
    r"깎(는|아|여|인|을|던|기)": (
        "표면·픽셀·메시가 주어면 영어 비유 -> 지운다 / 뚫는다 / 안 그린다. "
        "연필·가격·비용·값이 주어면 그대로 둔다"
    ),
}

# ---------------------------------------------------------------------------
# 낱말 짝 — 주체가 그 동작을 못 하는 조합 (참고 보고)
#
# 일반 규칙으로는 판단이 불안정해서 확인된 사례를 하나씩 옮긴다. 새 항목은 실제로 확인됐을 때만 추가한다.
# ---------------------------------------------------------------------------
LEXICAL_PAIRS = {
    r"지연이 지나": "지연이 지나는 게 아니라 지연 시간이 지남 -> '지연 시간이 지나면'",
    r"가르지\s*않": (
        "'거리가 아무것도 가르지 않는다' 는 지어낸 말 -> "
        "'거리로 행동이 나뉘지 않는다' / '값이 달라도 결과가 같다'"
    ),
    r"먹이(는|지|고|면|기|던|게)|먹여": (
        "값ㆍ데이터를 '먹인다' 는 영어 feed 직역 -> 넣는다 / 준다 / 사용한다 "
        "(미리보기가 태그를 못 먹인다 -> 미리보기가 태그를 넣어 주지 못한다). "
        "동물ㆍ사람에게 밥을 주는 뜻이면 그대로 둔다"
    ),
    r"(값|수치|각도|알파|파라미터|피치|입력|스틱|축)(을|를)\s*(민다|미는|밀어|밀고|밀면|밉니다|미세|미십)|(값|수치|각도|알파|파라미터|피치)\s*밀기": (
        "수치를 '민다' 는 영어 push 직역 -> 무엇이 어떻게 변하는지 그대로 쓴다 "
        "('스틱이 알파를 민다' -> '스틱을 움직이면 카메라가 레일 위를 이동한다'). "
        "물체를 손으로 밀거나 화면을 옆으로 밀어내는 뜻이면 그대로 둔다"
    ),
    r"(한국어|영어|일본어|한글)로\s*갈(려|린|리)": (
        "언어는 갈리는 게 아니라 쓰이는 것 -> '툴팁은 한국어로 쓰여 있다'. "
        "둘 이상으로 실제로 나뉘는 것이면 '나뉘어 있다'"
    ),
}

# ---------------------------------------------------------------------------
# 표기 변형 쌍 — 같은 뜻인데 표기가 갈리는 것
# 한 파일 안에 둘 이상 나오면 확정 문제, 파일별로 갈리면 참고 보고(트리 모드).
# ---------------------------------------------------------------------------
VARIANT_SETS = [
    ("나이아가라", "니아가라"),
    ("전용 서버", "데디서버", "데디케이티드 서버"),
    ("대미지", "데미지"),
    ("에셋", "애셋"),
    ("셰이프", "쉐이프"),
    ("블루프린트", "블프"),
    ("프레임레이트", "프레임 레이트"),
]

# ---------------------------------------------------------------------------
# 문서 밖 참조 후보 — 독자가 문서 안에서 찾을 수 없는 참조
# ---------------------------------------------------------------------------
DANGLING_PATTERNS = [
    (r"§\s*\d", "§번호 참조 — 이 문서에 번호 항목이 없으면 독자가 찾을 수 없다"),
    (r"기존과 동일", "'기존'이 무엇인지 문서 안에서 알 수 없다"),
    (r"기존[^.\n]{0,12}절[^.\n]{0,6}참조", "'기존 ~ 절'이 이 문서에 없으면 깨진 참조"),
]

MD_EXT = (".md", ".markdown")

# 이 표시가 파일 안에 있으면 검사를 건너뛴다.
# 금지어·표기 변형을 예시로 나열하는 문서(용어집, 이 플러그인의 설명서 등)를 위한 장치.
# doc-polish 표시는 이전 이름이다. 기존 문서를 고치지 않아도 되도록 함께 인정한다.
OPT_OUT = ("<!-- ko-review: ignore -->", "<!-- doc-polish: ignore -->")
TERMS_DEFAULT = ".claude/ko-review/terms.json"


def project_root():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return env
    try:
        top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                      encoding="utf-8", stderr=subprocess.DEVNULL).strip()
        if top:
            return top
    except (OSError, subprocess.CalledProcessError):
        pass
    return os.getcwd()


def load_terms(path):
    """프로젝트 전용 목록을 기본 목록에 더한다. 파일이 없으면 아무것도 하지 않는다."""
    if not path or not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    BANNED.update(data.get("banned", {}))
    BANNED_SOFT.update(data.get("banned_soft", {}))
    BANNED_PATTERNS.update(data.get("banned_patterns", {}))
    BANNED_SOFT_PATTERNS.update(data.get("soft_patterns", {}))
    LEXICAL_PAIRS.update(data.get("lexical_pairs", {}))
    VARIANT_SETS.extend(tuple(group) for group in data.get("variant_sets", []))
    return path


def show_path(path):
    """표시용 경로. 다른 드라이브면 relpath 가 실패하므로 절대경로로 물러난다."""
    try:
        return os.path.relpath(path)
    except ValueError:
        return path


def strip_code(text):
    """펜스 코드블록과 인라인 코드 스팬을 공백으로 치환.

    금지어·변형 검사가 코드 식별자(Fallback 등)를 오탐하지 않게 한다.
    줄 번호를 유지하려고 개행은 보존한다.
    """
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))

    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", blank, text)
    return text


def slug(heading):
    """GitHub 앵커 규칙: 소문자화 -> 낱말/공백/하이픈만 남김 -> 공백 하나하나를 하이픈으로.

    공백 묶음을 하이픈 하나로 합치면 안 된다. GitHub 는 공백을 하나씩 치환하므로
    기호가 지워져 공백이 둘 남으면 하이픈도 둘이 된다.
    예: `채널 규정 (`X` = Y)` -> `채널-규정-x--y`  (= 가 지워져 하이픈 2개)
    """
    s = heading.strip().lower()
    s = re.sub(r"<[^>]+>", "", s)                      # 인라인 HTML 태그
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)   # 낱말·공백·하이픈만
    return re.sub(r"\s", "-", s.strip())


def read_doc(path):
    with open(path, "rb") as f:
        raw = f.read()
    has_bom = raw.startswith(BOM)
    body = raw[3:] if has_bom else raw
    return has_bom, body.decode("utf-8", errors="replace")


def check_anchors(raw, clean):
    """문서 내 앵커 링크가 실제 제목과 맞는지.

    제목은 `raw` 에서 읽는다 — 제목 안의 인라인 코드도 앵커에 반영되기 때문이다.
    링크는 `clean` 에서 찾는다 — 코드 스팬 안의 링크는 표기 예시다.
    """
    headings = re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", raw)
    valid = {slug(h) for h in headings}

    problems = []
    for m in re.finditer(r"\[([^\]]*)\]\(#([^)]+)\)", clean):
        target = m.group(2).strip()
        if target in valid:
            continue
        line = clean[: m.start()].count("\n") + 1
        # 가장 비슷한 제목 추측 — 대상 슬러그를 포함하거나 포함되는 것
        hint = ""
        for h in headings:
            hs = slug(h)
            if target in hs or hs in target:
                hint = " -> #{}".format(hs)
                break
        problems.append("{}행: 앵커 #{} 가 어느 제목과도 안 맞음{}".format(line, target, hint))
    return problems


def check_links(path, text):
    """상대 경로 링크가 실제 파일을 가리키는지."""
    base = os.path.dirname(os.path.abspath(path))
    problems = []
    for m in re.finditer(r"\[([^\]]*)\]\(([^)#][^)]*)\)", text):
        target = m.group(2).strip()
        if re.match(r"^(https?:|mailto:|//)", target):
            continue
        target = target.split("#", 1)[0].strip()
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(resolved):
            line = text[: m.start()].count("\n") + 1
            problems.append("{}행: 링크 대상 없음 -> {}".format(line, target))
    return problems


def find_terms(clean, table):
    """금지어 표에서 걸린 것: {낱말: [행번호, ...]}"""
    hits = defaultdict(list)
    lines = clean.split("\n")
    for i, line in enumerate(lines, 1):
        for term in table:
            if term in line:
                hits[term].append(i)
    return hits


def check_variants(clean):
    """한 파일 안에서 표기가 갈린 경우."""
    problems = []
    for group in VARIANT_SETS:
        present = [(t, clean.count(t)) for t in group if clean.count(t) > 0]
        if len(present) > 1:
            desc = " / ".join("{}({})".format(t, n) for t, n in present)
            problems.append("표기 갈림: {} -> 다수 쪽으로 통일".format(desc))
    return problems


def check_symbols(clean):
    """기호 변형 혼용 — 참고 보고.

    같은 글자를 두 방식으로 인코딩한 경우만 본다.
    가운뎃점 앞뒤 공백은 검사하지 않는다 — 낱말 붙이기(`링크·앵커`)와
    구 나누기(`A · B · C`)가 서로 다른 용도라 섞여 있는 게 정상이다.
    """
    notes = []
    emoji_warn = len(re.findall("⚠️", clean))
    text_warn = len(re.findall("⚠(?!️)", clean))
    if emoji_warn and text_warn:
        notes.append(
            "경고 기호 혼용: 이모지형 U+26A0+FE0F {}개 / 텍스트형 U+26A0 {}개 "
            "-> 텍스트형 권장(이모지형은 렌더 폭이 환경마다 달라 표 정렬이 흔들림)".format(
                emoji_warn, text_warn
            )
        )
    return notes


def check_dangling(clean):
    """문서 밖 참조 후보 — 참고 보고."""
    notes = []
    lines = clean.split("\n")
    for pattern, why in DANGLING_PATTERNS:
        rows = [str(i) for i, ln in enumerate(lines, 1) if re.search(pattern, ln)]
        if rows:
            shown = ", ".join(rows[:8]) + (" …" if len(rows) > 8 else "")
            notes.append("{}행: {}".format(shown, why))
    return notes


def rows_text(rows):
    return ", ".join(map(str, rows[:8])) + (" …" if len(rows) > 8 else "")


def check_file(path):
    """반환: (확정 문제 리스트, 참고 항목 리스트, 건너뛴 이유 또는 None)"""
    problems, notes = [], []
    try:
        has_bom, text = read_doc(path)
    except OSError as e:
        return ["파일 열기 실패: {}".format(e)], [], None

    marker = next((m for m in OPT_OUT if m in text), None)
    if marker:
        return [], [], "{} 표시가 있어 건너뜀".format(marker)

    if has_bom:
        problems.append("UTF-8 BOM 있음 — 문서는 BOM 없는 UTF-8 로 저장한다")

    # 링크·앵커도 코드 스팬을 걸러낸 본문에서 찾는다.
    # 코드 스팬 안의 `[텍스트](#앵커)` 는 실제 링크가 아니라 표기 예시다.
    clean = strip_code(text)

    problems += check_anchors(text, clean)
    problems += check_links(path, clean)
    problems += check_variants(clean)

    for term, rows in sorted(find_terms(clean, BANNED).items()):
        problems.append("{}행: 금지어 '{}' -> {}".format(rows_text(rows), term, BANNED[term]))
    for term, rows in sorted(find_terms(clean, BANNED_SOFT).items()):
        notes.append("{}행: '{}' 확인 -> {}".format(rows_text(rows), term, BANNED_SOFT[term]))

    lines = clean.split("\n")
    for pattern, why in BANNED_PATTERNS.items():
        rows = [i for i, ln in enumerate(lines, 1) if re.search(pattern, ln)]
        if rows:
            problems.append("{}행: 금지어 — {}".format(rows_text(rows), why))

    for pattern, why in BANNED_SOFT_PATTERNS.items():
        rows = [i for i, ln in enumerate(lines, 1) if re.search(pattern, ln)]
        if rows:
            notes.append("{}행: 확인 — {}".format(rows_text(rows), why))

    for pattern, why in LEXICAL_PAIRS.items():
        rows = [i for i, ln in enumerate(lines, 1) if re.search(pattern, ln)]
        if rows:
            notes.append("{}행: 낱말 짝 — {}".format(rows_text(rows), why))

    notes += check_symbols(clean)
    notes += check_dangling(clean)
    return problems, notes, None


def tree_variants(files):
    """파일 사이에서 표기가 갈린 경우 — 파일 안에서는 안 보이는 종류."""
    per_group = []
    for group in VARIANT_SETS:
        counts = {}
        for f in files:
            try:
                _, text = read_doc(f)
            except OSError:
                continue
            if any(m in text for m in OPT_OUT):
                continue
            clean = strip_code(text)
            found = {t: clean.count(t) for t in group if clean.count(t) > 0}
            if found:
                counts[f] = found
        variants_used = set()
        for found in counts.values():
            variants_used |= set(found)
        if len(variants_used) > 1:
            per_group.append((group, counts))
    return per_group


def collect(args):
    """반환: (파일 목록, terms 경로 또는 None)"""
    files, terms, i = [], None, 0
    while i < len(args):
        if args[i] == "--tree":
            i += 1
            root = args[i] if i < len(args) else "."
            for dirpath, _, names in os.walk(root):
                for n in sorted(names):
                    if n.lower().endswith(MD_EXT):
                        files.append(os.path.join(dirpath, n))
        elif args[i] == "--terms":
            i += 1
            terms = args[i] if i < len(args) else None
        else:
            files.append(args[i])
        i += 1
    return files, terms


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    args = argv[1:]
    if not args:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    tree_mode = "--tree" in args
    files, terms = collect(args)
    if not files:
        print("검사할 .md 파일이 없습니다.", file=sys.stderr)
        return 2
    if terms and not os.path.isfile(terms):
        print("terms 파일이 없습니다: {}".format(terms), file=sys.stderr)
        return 2
    loaded = load_terms(terms or os.path.join(project_root(), TERMS_DEFAULT))

    print("## ko-review 자동 검사\n")
    print("대상 {}개 파일{}\n".format(
        len(files), " · 프로젝트 목록 {}".format(show_path(loaded)) if loaded else ""))

    any_problem = False
    for f in files:
        if not f.lower().endswith(MD_EXT):
            print("### {}\n\nskip — .md 아님\n".format(os.path.basename(f)))
            continue
        problems, notes, skipped = check_file(f)
        if skipped:
            print("### {}\n\nskip — {}\n".format(show_path(f), skipped))
            continue
        if not problems and not notes:
            continue
        print("### {}\n".format(show_path(f)))
        if problems:
            any_problem = True
            print("**확정 문제**\n")
            for p in problems:
                print("- {}".format(p))
            print()
        if notes:
            print("**확인 필요 (판단)**\n")
            for n in notes:
                print("- {}".format(n))
            print()

    if tree_mode:
        groups = tree_variants(files)
        if groups:
            print("### 파일 사이 표기 갈림\n")
            print("파일 안에서는 각각 일관돼서 안 보이는 종류. 일괄 결정이 필요하다.\n")
            for group, counts in groups:
                print("- **{}**".format(" / ".join(group)))
                for f, found in sorted(counts.items()):
                    desc = ", ".join("{} {}회".format(t, n) for t, n in found.items())
                    print("  - `{}` — {}".format(show_path(f), desc))
            print()

    print("---\n")
    if any_problem:
        print("확정 문제 있음. 판단 검토로 넘어가기 전에 조치 필요.")
    else:
        print("확정 문제 없음. 위 '확인 필요' 항목만 판단하면 된다.")
    return 1 if any_problem else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
