#!/usr/bin/env python3
"""기획 판정에 쓰는 계산 두 가지를 한다. 판정은 하지 않고 계산 결과만 낸다.

1) dominance — 선택지 × 상황 표에서 지배 관계를 찾는다.
   어느 상황에서도 1등인 선택지, 다른 선택지에 밀리기만 하는 선택지,
   어느 상황에서도 1등이 아닌 선택지를 가린다.
2) breakeven — 위험한 행동과 안전한 행동을 비교해, 위험한 행동이
   이득이 되려면 성공률이 얼마 이상이어야 하는지(손익분기 성공률)를 구한다.

기획 고문(design)은 계산을 머릿속으로 하지 않는다(공통 규칙 §2).
이 스크립트의 명령과 출력은 리포트 부록에 그대로 붙인다.
프로젝트 파일은 읽기만 한다. 결과는 --out 경로에만 쓰고, 없으면 표준 출력으로 낸다.
Python 3.8 이상, 표준 라이브러리만 쓴다.
"""

import argparse
import csv
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


class InputError(Exception):
    pass


def to_num(text, where):
    t = (text or "").strip().replace(",", "")
    if t == "":
        raise InputError("빈 값: %s" % where)
    try:
        return float(t)
    except ValueError:
        raise InputError("숫자가 아닌 값 '%s': %s" % (text, where))


def fmt(x):
    if x is None:
        return "-"
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return "%.4g" % x


def command_line():
    return "python choice_calc.py " + " ".join(
        ('"%s"' % a) if (" " in a or not a) else a for a in sys.argv[1:])


# ── dominance ─────────────────────────────────────────────

def load_matrix(a):
    names, cols, rows = [], [], []
    if a.csv:
        with open(a.csv, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            header = None
            for ln, rec in enumerate(reader, 1):
                if not rec or not any(c.strip() for c in rec) or rec[0].strip().startswith("#"):
                    continue
                if header is None:
                    header = [c.strip() for c in rec]
                    cols = header[1:]
                    if not cols:
                        raise InputError("CSV 첫 줄에 상황 칸이 없다 (첫 칸은 선택지 이름, 다음 칸부터 상황)")
                    continue
                if len(rec) - 1 != len(cols):
                    raise InputError("%d행: 칸 수가 머리 줄과 다르다 (%d개, 기대 %d개)" % (ln, len(rec) - 1, len(cols)))
                names.append(rec[0].strip())
                rows.append([to_num(v, "%d행 '%s' 칸" % (ln, cols[i])) for i, v in enumerate(rec[1:])])
    else:
        if not a.cols or not a.row:
            raise InputError("--csv 를 주거나, --cols 와 --row 를 함께 준다")
        cols = [c.strip() for c in a.cols.split(",")]
        for r in a.row:
            if "=" not in r:
                raise InputError("--row 형식은 이름=값1,값2,... : %s" % r)
            n, _, vals = r.partition("=")
            parts = vals.split(",")
            if len(parts) != len(cols):
                raise InputError("'%s' 의 값 개수 %d 가 상황 개수 %d 와 다르다" % (n, len(parts), len(cols)))
            names.append(n.strip())
            rows.append([to_num(v, "'%s' 의 '%s'" % (n.strip(), cols[i])) for i, v in enumerate(parts)])
    if len(names) < 2:
        raise InputError("선택지가 두 개 이상이어야 비교할 수 있다")
    if len(set(names)) != len(names):
        raise InputError("선택지 이름이 겹친다")
    return names, cols, rows


def dominance(a):
    names, cols, rows = load_matrix(a)
    tol = a.tol
    sign = -1.0 if a.lower_better else 1.0

    def better(x, y):  # x 가 y 보다 확실히 낫다
        return sign * (x - y) > tol

    def not_worse(x, y):
        return sign * (y - x) <= tol

    per_situation = []
    best_count = {n: 0 for n in names}
    for j, c in enumerate(cols):
        vals = [(rows[i][j], names[i]) for i in range(len(names))]
        vals.sort(key=lambda t: sign * t[0], reverse=True)
        top = vals[0][0]
        winners = [n for v, n in vals if not better(top, v)]
        for n in winners:
            best_count[n] += 1
        runner = next(((v, n) for v, n in vals if n not in winners), None)
        per_situation.append({
            "situation": c,
            "best": winners,
            "best_value": top,
            "runner_up": runner[1] if runner else None,
            "runner_up_value": runner[0] if runner else None,
            "gap": (abs(top - runner[0]) if runner else None),
        })

    dominated_by = {n: [] for n in names}
    for i, ni in enumerate(names):
        for k, nk in enumerate(names):
            if i == k:
                continue
            all_nw = all(not_worse(rows[k][j], rows[i][j]) for j in range(len(cols)))
            some_b = any(better(rows[k][j], rows[i][j]) for j in range(len(cols)))
            if all_nw and some_b:
                dominated_by[ni].append(nk)

    always_best = [n for n in names if best_count[n] == len(cols)]
    never_best = [n for n in names if best_count[n] == 0]
    pareto = [n for n in names if not dominated_by[n]]

    return {
        "kind": "dominance",
        "command": command_line(),
        "direction": "작을수록 좋음" if a.lower_better else "클수록 좋음",
        "tolerance": tol,
        "options": names,
        "situations": cols,
        "matrix": rows,
        "per_situation": per_situation,
        "always_best": always_best,
        "dominated_by": {k: v for k, v in dominated_by.items() if v},
        "never_best": never_best,
        "pareto": pareto,
    }


def render_dominance(r):
    L = ["# 선택지 지배 관계 계산", ""]
    L.append("- 명령: `%s`" % r["command"])
    L.append("- 입력: 선택지 %d개 × 상황 %d개, %s, 같음으로 보는 차이 %s 이하" % (
        len(r["options"]), len(r["situations"]), r["direction"], fmt(r["tolerance"])))
    L.append("- 뜻: 'A 가 B 를 지배한다' = 모든 상황에서 A 가 B 보다 같거나 낫고, 한 상황 이상에서 낫다.")
    L.append("")
    L.append("## 상황별 1등")
    L.append("")
    L.append("| 상황 | 1등 | 값 | 2등 | 값 | 차이 |")
    L.append("|---|---|---|---|---|---|")
    for p in r["per_situation"]:
        L.append("| %s | %s | %s | %s | %s | %s |" % (
            p["situation"], ", ".join(p["best"]), fmt(p["best_value"]),
            p["runner_up"] or "-", fmt(p["runner_up_value"]), fmt(p["gap"])))
    L.append("")
    L.append("## 계산 결과")
    L.append("")
    L.append("- 모든 상황에서 1등(같음 포함): " + (", ".join(r["always_best"]) or "없음"))
    if r["dominated_by"]:
        for k, v in r["dominated_by"].items():
            L.append("- 지배되는 선택지 '%s' — 모든 상황에서 이것과 같거나 나은 선택지: %s" % (k, ", ".join(v)))
    else:
        L.append("- 다른 선택지에 지배되는 선택지: 없음")
    L.append("- 어느 상황에서도 1등이 아닌 선택지: " + (", ".join(r["never_best"]) or "없음"))
    L.append("- 지배되지 않는 선택지: " + ", ".join(r["pareto"]))
    L.append("")
    L.append("## 입력 표")
    L.append("")
    L.append("| 선택지 | " + " | ".join(r["situations"]) + " |")
    L.append("|---|" + "---|" * len(r["situations"]))
    for n, row in zip(r["options"], r["matrix"]):
        L.append("| %s | %s |" % (n, " | ".join(fmt(v) for v in row)))
    L.append("")
    L.append("이 결과는 입력 값이 맞다는 전제의 계산이다. 상황 칸이 그 선택이 실제로 일어나는 장면인지는 따로 확인한다.")
    return "\n".join(L)


# ── breakeven ─────────────────────────────────────────────

def breakeven_one(name, S, F, X, ts, tf, tx):
    """위험 행동(성공 S, 실패 F, 걸리는 시간 ts/tf)과 안전 행동(X, 시간 tx)을 비교한다.

    시간 당 기대 이득으로 비교한다.
      위험 행동의 시간 당 기대 이득 = (p*S + (1-p)*F) / (p*ts + (1-p)*tf)
      안전 행동의 시간 당 이득       = X / tx = r
    둘이 같아지는 p 가 손익분기 성공률 p* 다.
      p* = (r*tf - F) / (S - F - r*(ts - tf))
    시간을 주지 않으면 ts = tf = tx = 1 이고, p* = (X - F) / (S - F) 가 된다.
    """
    for label, t in (("성공 시간", ts), ("실패 시간", tf), ("안전 시간", tx)):
        if t <= 0:
            raise InputError("%s: %s은 0 보다 커야 한다" % (name, label))
    r = X / tx
    num = r * tf - F
    den = S - F - r * (ts - tf)
    if abs(den) < 1e-12:
        if num <= 0:
            p, note = None, "성공률과 상관없이 위험 행동이 안전 행동과 같거나 낫다"
        else:
            p, note = None, "성공률과 상관없이 위험 행동이 안전 행동보다 못하다"
    else:
        p = num / den
        if den > 0:
            # 성공률이 높을수록 위험 행동이 유리하다. p* 이상이면 이득.
            if p > 1:
                note = "성공률이 100%여도 안전 행동보다 낫지 않다"
            elif p <= 0:
                note = "실패해도 안전 행동과 같거나 낫다. 위험 행동에 실제 위험이 없다"
            else:
                note = "성공률이 %s 이상일 때만 위험 행동이 이득이다" % (fmt(p * 100) + "%")
        else:
            # 성공이 시간 당 이득을 오히려 깎는 입력(성공에 걸리는 시간이 길어서 등). p* 이하일 때만 이득.
            if p <= 0:
                note = "성공률과 상관없이 위험 행동이 안전 행동보다 못하다(성공해도 시간 당 이득이 안전 행동보다 작다)"
            elif p >= 1:
                note = "성공률과 상관없이 위험 행동이 안전 행동과 같거나 낫다"
            else:
                note = ("성공률이 %s 이하일 때만 위험 행동이 이득이다. 성공할수록 시간 당 이득이 줄어드는 입력이므로 "
                        "성공·실패 값과 시간이 바뀌지 않았는지 확인한다" % (fmt(p * 100) + "%"))
    return {"name": name, "success": S, "fail": F, "safe": X,
            "success_time": ts, "fail_time": tf, "safe_time": tx,
            "breakeven": p, "note": note}


def check_times(name, ts, tf, tx):
    """시간은 모두 주거나 모두 빼야 한다. 일부만 주면 단위가 섞이므로 오류로 낸다.

    실패 시간은 비우면 성공 시간과 같다고 본다. 시간을 하나도 주지 않으면 모두 1 이다.
    """
    if ts is None and tf is None and tx is None:
        return 1.0, 1.0, 1.0
    if ts is None or tx is None:
        raise InputError("%s: 시간을 쓰려면 성공 시간과 안전 시간을 모두 준다(실패 시간은 비우면 성공 시간과 같음). "
                         "일부만 주면 비교하는 두 행동의 시간 단위가 섞인다" % name)
    return ts, (tf if tf is not None else ts), tx


def breakeven(a):
    items = []
    if a.csv:
        with open(a.csv, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            need = {"name", "success", "fail", "safe"}
            if not reader.fieldnames or not need.issubset({h.strip() for h in reader.fieldnames}):
                raise InputError("CSV 머리 줄에 name,success,fail,safe 가 있어야 한다 (선택: success_time,fail_time,safe_time)")
            for ln, rec in enumerate(reader, 2):
                rec = {k.strip(): v for k, v in rec.items() if k}
                if not rec.get("name") or rec["name"].strip().startswith("#"):
                    continue
                g = lambda k, d=None: to_num(rec[k], "%d행 '%s'" % (ln, k)) if (rec.get(k) or "").strip() else d
                for k in ("success", "fail", "safe"):
                    if g(k) is None:
                        raise InputError("%d행: '%s' 값이 비어 있다" % (ln, k))
                ts, tf, tx = check_times(rec["name"].strip(), g("success_time"), g("fail_time"), g("safe_time"))
                items.append(breakeven_one(rec["name"].strip(), g("success"), g("fail"), g("safe"), ts, tf, tx))
    else:
        if a.success is None or a.fail is None or a.safe is None:
            raise InputError("--csv 를 주거나, --success --fail --safe 를 모두 준다")
        ts, tf, tx = check_times(a.name, a.success_time, a.fail_time, a.safe_time)
        items.append(breakeven_one(a.name, a.success, a.fail, a.safe, ts, tf, tx))
    timed = any(not (i["success_time"] == i["fail_time"] == i["safe_time"] == 1.0) for i in items)
    return {"kind": "breakeven", "command": command_line(), "timed": timed, "items": items}


def render_breakeven(r):
    L = ["# 위험 행동의 손익분기 성공률", ""]
    L.append("- 명령: `%s`" % r["command"])
    if r["timed"]:
        L.append("- 식: p* = (r × 실패 시간 − 실패 값) / (성공 값 − 실패 값 − r × (성공 시간 − 실패 시간)), r = 안전 값 ÷ 안전 시간")
        L.append("- 뜻: 시간 당 기대 이득으로 비교한다. 위험 행동의 시간 당 기대 이득이 안전 행동과 같아지는 성공률이 p* 다.")
    else:
        L.append("- 식: p* = (안전 값 − 실패 값) / (성공 값 − 실패 값)")
        L.append("- 뜻: 위험 행동의 기대 이득(p × 성공 값 + (1 − p) × 실패 값)이 안전 행동과 같아지는 성공률이 p* 다.")
    L.append("- 전제: 성공 값, 실패 값, 안전 값은 같은 단위다(예: 모두 '준 피해', 또는 모두 '얻은 자원'). 손해는 음수로 넣는다.")
    L.append("")
    head = "| 이름 | 성공 값 | 실패 값 | 안전 값 |"
    sep = "|---|---|---|---|"
    if r["timed"]:
        head += " 성공 시간 | 실패 시간 | 안전 시간 |"
        sep += "---|---|---|"
    head += " p* | 해석 |"
    sep += "---|---|"
    L.append(head)
    L.append(sep)
    for i in r["items"]:
        row = "| %s | %s | %s | %s |" % (i["name"], fmt(i["success"]), fmt(i["fail"]), fmt(i["safe"]))
        if r["timed"]:
            row += " %s | %s | %s |" % (fmt(i["success_time"]), fmt(i["fail_time"]), fmt(i["safe_time"]))
        row += " %s | %s |" % (fmt(i["breakeven"]), i["note"])
        L.append(row)
    L.append("")
    L.append("p* 는 계산값이다. 플레이어의 실제 성공률은 플레이테스트에서 관찰해야 알 수 있다.")
    return "\n".join(L)


# ── 진입점 ────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="기획 판정용 계산. dominance(선택지 지배 관계) 와 breakeven(위험 행동 손익분기 성공률) 두 가지.")
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("dominance", help="선택지 × 상황 표에서 지배 관계를 찾는다")
    d.add_argument("--csv", help="CSV 파일. 첫 줄은 머리(첫 칸 아무 이름, 다음 칸부터 상황 이름), 다음 줄부터 '선택지, 값...'. #으로 시작하는 줄은 건너뛴다")
    d.add_argument("--cols", help="CSV 대신 직접 줄 때 상황 이름들, 쉼표로 구분. 예: 근접1명,원거리3명,보스")
    d.add_argument("--row", action="append", help="CSV 대신 직접 줄 때 선택지 한 줄. 예: 검=120,40,300 (여러 번 준다)")
    d.add_argument("--lower-better", action="store_true", help="값이 작을수록 좋다 (예: 처치 시간). 기본은 클수록 좋음")
    d.add_argument("--tol", type=float, default=0.0, help="이 차이 이하는 같다고 본다 (기본 0)")
    d.add_argument("--format", choices=["md", "json"], default="md", help="출력 형식 (기본 md)")
    d.add_argument("--out", help="결과를 쓸 파일 경로. 없으면 표준 출력")

    b = sub.add_parser("breakeven", help="위험 행동이 이득이 되는 최소 성공률을 구한다")
    b.add_argument("--csv", help="CSV 파일. 머리 줄: name,success,fail,safe[,success_time,fail_time,safe_time]")
    b.add_argument("--name", default="위험 행동", help="직접 줄 때 행동 이름")
    b.add_argument("--success", type=float, help="위험 행동이 성공했을 때 얻는 값")
    b.add_argument("--fail", type=float, help="위험 행동이 실패했을 때 얻는 값. 손해면 음수")
    b.add_argument("--safe", type=float, help="안전 행동으로 얻는 값")
    b.add_argument("--success-time", type=float, help="위험 행동이 성공할 때 걸리는 시간 (선택. 주면 --safe-time 도 함께 준다)")
    b.add_argument("--fail-time", type=float, help="위험 행동이 실패할 때 걸리는 시간 (선택, 없으면 성공 시간과 같음)")
    b.add_argument("--safe-time", type=float, help="안전 행동에 걸리는 시간 (선택. 주면 --success-time 도 함께 준다)")
    b.add_argument("--format", choices=["md", "json"], default="md", help="출력 형식 (기본 md)")
    b.add_argument("--out", help="결과를 쓸 파일 경로. 없으면 표준 출력")
    a = p.parse_args()
    if not a.cmd:
        p.print_help()
        sys.exit(2)
    return a


def main():
    a = parse_args()
    try:
        if a.cmd == "dominance":
            r = dominance(a)
            text = render_dominance(r) if a.format == "md" else json.dumps(r, ensure_ascii=False, indent=1)
        else:
            r = breakeven(a)
            text = render_breakeven(r) if a.format == "md" else json.dumps(r, ensure_ascii=False, indent=1)
    except InputError as e:
        print("입력 오류: %s" % e, file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print("파일 오류: %s" % e, file=sys.stderr)
        sys.exit(2)
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print("저장함: %s" % a.out)
    else:
        print(text)


if __name__ == "__main__":
    main()
