#!/usr/bin/env python3
"""Find review candidates in line-based Korean game scripts.

Each line of a script is one of three kinds:
  command  - structure or engine syntax (scene labels, jumps, choices, stage
             commands, variables, comments). Skipped.
  spoken   - a speaker prefix followed by the line. Matches --speaker.
  narration - everything else.

The defaults fit the Dialogue Manager style (`~ cue`, `id: line`, `- choice`,
`do ...`, `set ...`). A project's format file (.claude/story/format.md) gives
other regexes when its script looks different.

A hit is a candidate, not a verdict. The reviewer reads each hit in context.
Standard library only.
"""
import argparse
import collections
import re
import sys

DEFAULT_COMMAND = r"^\s*(#|~|=>|-|%|do |set |if |elif |else|while |match )"
DEFAULT_SPEAKER = r"^\s*[A-Za-z_]\w*\s*:\s*"
DEFAULT_TAG = r"\[[^\]]*\]|\{\{[^}]*\}\}"
DEFAULT_CHOICE = r"^\s*- "

# Emotion names in narration (step 4 "Emotion"). Past and present forms.
EMOTION = re.compile(
    r"(슬펐|기뻤|화가 났|두려웠|무서웠|불안했|당황했|놀랐|안도했|외로웠|긴장했|서운했|억울했"
    r"|슬퍼졌|불안해졌|두려워졌|무서워졌|외로워졌|서운해졌|억울해졌|긴장됐|긴장되었|당황스러웠"
    r"|슬프다|기쁘다|화가 난다|두렵다|무섭다|불안하다|당황한다|놀란다|안도한다|외롭다|긴장한다|서운하다|억울하다)"
)
# First-person filter verbs in narration.
FILTER = re.compile(r"(느꼈|보였|생각했|깨달았|알았|듯했|것 같았|느낀다|생각한다|깨닫는다|것 같다)")
# Double passive.
PASSIVE = re.compile(r"(잊혀|믿겨|쓰여|불려|읽혀|열려|닫혀|보여)(지|진|졌|져)")
# Translationese signals.
TRANSLATIONESE = re.compile(r"(에 의해|에 대한|으로 인해|로 인해|을 가지고 있|를 가지고 있)")
# Clock times and minutes written in Korean words. 시간 is excluded. A lone 이 before 분
# is skipped because 이분 / 이 분 usually means "this person"; 이십 분 still matches.
NUMBER = re.compile(
    r"(?<![가-힣])(한|두|세|네|다섯|여섯|일곱|여덟|아홉|열|열한|열두) ?시(?!간|작|절|대|장|선|청|민|기|켜|키|계)"
    r"|(?<![가-힣])((일|이|삼|사|오|육|칠|팔|구|십){2,}|일|삼|사|오|육|칠|팔|구|십) ?분(?!명|위|야|노|석|리|별|량|해|배|자|들)"
)
END_TRIM = re.compile(r"[\s.…\"'!?」』)]+$")
SPACE = re.compile(r"\s+")

CHECKS = ("emotion", "filter", "passive", "translationese", "number", "length", "colon", "choices", "endings")


def classify(line, command, speaker):
    if not line.strip():
        return "blank", ""
    if command.match(line):
        return "command", ""
    m = speaker.match(line)
    if m:
        return "spoken", line[m.end():]
    return "narration", line


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--command", default=DEFAULT_COMMAND, help="regex for command lines (skipped)")
    ap.add_argument("--speaker", default=DEFAULT_SPEAKER, help="regex for the speaker prefix of a spoken line")
    ap.add_argument("--tag", default=DEFAULT_TAG, help="regex for inline markup removed before measuring")
    ap.add_argument("--choice", default=DEFAULT_CHOICE, help="regex for choice lines (listed by the choices check)")
    ap.add_argument("--max-len", type=int, default=60, help="box length above which a line is listed")
    ap.add_argument("--checks", default="all", help="comma list of: " + ",".join(CHECKS))
    ap.add_argument("--summary", action="store_true", help="print counts only")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    command = re.compile(args.command)
    speaker = re.compile(args.speaker)
    tag = re.compile(args.tag)
    choice = re.compile(args.choice)
    checks = set(CHECKS) if args.checks == "all" else {c.strip() for c in args.checks.split(",")}
    unknown = checks - set(CHECKS)
    if unknown:
        ap.error("unknown checks: " + ", ".join(sorted(unknown)))

    counts = collections.Counter()
    endings = collections.Counter()
    kinds = collections.Counter()

    def hit(name, path, n, text, extra=""):
        counts[name] += 1
        if not args.summary:
            shown = text.strip()
            if len(shown) > 90:
                shown = shown[:87] + "..."
            print(f"{path}:{n}: [{name}{extra}] {shown}")

    for path in args.files:
        try:
            lines = open(path, encoding="utf-8-sig").read().splitlines()
        except OSError as e:
            print(f"{path}: cannot read: {e}", file=sys.stderr)
            continue
        for n, line in enumerate(lines, 1):
            if choice.match(line):
                if "choices" in checks:
                    hit("choices", path, n, line)
                # Choice text is shown to the player too: check its wording.
                text = tag.sub("", choice.sub("", line, count=1)).strip()
                for name, rx in (("passive", PASSIVE), ("translationese", TRANSLATIONESE), ("number", NUMBER)):
                    if name in checks and rx.search(text):
                        hit(name, path, n, line)
                kinds["choice"] += 1
                continue
            kind, text = classify(line, command, speaker)
            kinds[kind] += 1
            if kind in ("blank", "command"):
                continue
            plain = tag.sub("", text).strip()
            if kind == "narration":
                if "emotion" in checks and EMOTION.search(plain):
                    hit("emotion", path, n, line)
                if "filter" in checks and FILTER.search(plain):
                    hit("filter", path, n, line)
                if "colon" in checks and ": " in plain:
                    hit("colon", path, n, line)
                if "endings" in checks:
                    tail = SPACE.sub("", END_TRIM.sub("", plain))[-2:]
                    if tail:
                        endings[tail] += 1
            if "passive" in checks and PASSIVE.search(plain):
                hit("passive", path, n, line)
            if "translationese" in checks and TRANSLATIONESE.search(plain):
                hit("translationese", path, n, line)
            if "number" in checks and NUMBER.search(plain):
                hit("number", path, n, line)
            if "length" in checks and len(plain) > args.max_len:
                hit("length", path, n, line, f" {len(plain)}")

    print(f"lines: spoken {kinds['spoken']}, narration {kinds['narration']}, choice {kinds['choice']}, command {kinds['command']}")
    print("hits: " + (", ".join(f"{k} {counts[k]}" for k in CHECKS if counts[k]) or "none"))
    if "endings" in checks and endings:
        total = sum(endings.values())
        top = ", ".join(f"{e} {c}" for e, c in endings.most_common(15))
        print(f"narration endings (last two characters, {total} lines): {top}")


if __name__ == "__main__":
    main()
