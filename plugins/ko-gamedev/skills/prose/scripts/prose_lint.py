#!/usr/bin/env python3
"""Find word and sentence candidates in Korean story prose (synopses, pitches, story documents).

The word rules are the Markdown tables under ../glossary/ that have `Use` and
`Avoid` columns, plus an optional project file (.claude/ko-gamedev/prose-terms.md).
Text inside fenced code, inline code, HTML comments and quotation marks is
skipped unless --include-quotes is given, because quoted text is usually a
character's line or a defined term.

Every hit is a candidate. A person or agent reads the sentence and decides.

Usage:
  python prose_lint.py [--summary] [--kind replace,review,density,owner,long,paren]
                       [--terms FILE] [--include-quotes] [--long N] PATH [PATH ...]

Exit code is 0 unless the arguments are wrong. Standard library only.
"""
import argparse
import collections
import io
import os
import re
import sys

HANGUL = re.compile('[가-힣]')
TEXT_EXT = {'.md', '.txt', '.markdown'}
SKIP_DIRS = {'.git', '.svn', 'node_modules', '__pycache__', '.godot', '.import'}
IGNORE_MARKS = ('prose-lint: ignore-file', 'ko-lint: ignore-file')
WORD_KINDS = ('replace', 'review', 'density')
ALL_KINDS = WORD_KINDS + ('owner', 'long', 'paren')
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_DIR = os.path.join(SKILL_DIR, 'glossary')
PROJECT_TERMS = os.path.join('.claude', 'ko-gamedev', 'prose-terms.md')

# Book values (novels, Korean nonfiction) for the per-file summary, measured with
# this script on the N and E corpora (../glossary/README.md). Quoted text skipped.
BASE = {'conj': (51, 85), 'link': (0.33, 0.44), 'cond': (6.2, 13.6), 'date': (0.3, 0.8), 'go': (33, 29)}
METRICS = (
    ('conj', 'sentences opening with a connective, per 1,000', '{:.0f}'),
    ('link', 'linked sentences in paragraphs of 4+ sentences', '{:.2f}'),
    ('cond', '-면 conditions per 100 sentences', '{:.1f}'),
    ('date', 'sentences opening with a date or day, %', '{:.1f}'),
    ('go', '-고 joins per 100 sentences', '{:.0f}'),
)

# A sentence counts as linked when it opens with a connective or carries a
# linking ending or noun. The list is broad on purpose: the measure is a
# ratio compared with books measured the same way.
LINK_START = re.compile(
    r'^(그래서|그러나|하지만|그런데|그러자|그러면|그러니|그러므로|따라서|결국|마침내|게다가|또한|대신|오히려|즉|다만|물론'
    r'|이때|그때|그 뒤|그 후|그사이|한편|그렇게|이렇게|그리하여|왜냐하면|그 결과|덕분에|그래도|그럼에도|그리고|또|이제|곧|드디어|끝내)')
LINK_IN = re.compile(
    r'(때문|위해|위하여|려고|도록|면서|지만|는데|은데|던데|니까|으니|자마자|느라|더니|다가|바람에|탓에|덕분에|대신'
    r'|뒤에|후에|만에|채로|므로|기에|길래|어서|아서|해서|여서|워서|으면|면 |자 )')
CONJ_START = re.compile(
    r'^(그래서|그러나|하지만|그런데|그러자|그러면|그러니|그러므로|따라서|결국|마침내|게다가|또한|대신|오히려|즉|다만|물론'
    r'|한편|그리하여|왜냐하면|그래도|그럼에도|그리고|또)(?![가-힣])')
SENT_END = re.compile(r'(?<=[가-힣])[.?!](?=\s|$|["”’\')])')
# Last syllables of a finished sentence. A fragment such as "2월." or "1주(3월 5일 개업)."
# is a section label, not a sentence, and is left out of every count.
FINAL_SYLLABLES = set('다요죠까지자라네나어아냐니오군게걸데세래음함임됨기것야해돼봐줘워와져쳐겨려랴구')

# Reasoning with no owner (../style/sentences.md S3): an "only if" condition
# (~라야, ~해야 followed by something other than 하다/되다), or two -면 conditions
# in one sentence, with no verb of thinking and no reason or purpose marker.
ONLY_IF = re.compile(r'(?<=[가-힣])(라야|어야|아야|여야|해야|와야|워야)\s(?!(하|했|할|한|합|함|해|되|돼|됐|될|된|겠)[가-힣\s.,])')
COND = re.compile(r'([가-힣])면(?=[\s,])')
NOT_COND = set('장화측표방전외내정반후국지단평양수체대직당안일')  # 장면, 화면, 측면, 반면 ...: nouns, not -면
OWNER = re.compile(r'(계산|판단|생각|믿|여기|여긴|여겨|짐작|예상|노리|노린|두려|걱정|따지|따진|따져|저울질|속셈|계획|의도'
                   r'|려고|위해|때문|까닭|이유|셈이)')
FRAME = re.compile(r'(이렇게|이렇다|다음과|아래와)')
# A general rule is in the present tense. Past narration (~했어야 맞았다) and questions are not rules.
PRESENT_END = re.compile(r'(?<![었았였했겠])다[.!]?["”’\')]*$')
DATE_START = re.compile(r'^(\d+\s*(월|일|주|년|시)|[월화수목금토일]요일)')  # 그날, 이튿날 are the fix (S6), not the problem
GO_JOIN = re.compile(r'(?<=[가-힣])(?<![다라냐자])고(?=[\s,])')
QUOTED = re.compile(r'"[^"\n]*"|“[^”\n]*”|‘[^’\n]*’|「[^」\n]*」|『[^』\n]*』')

Form = collections.namedtuple('Form', 'label rx')
Entry = collections.namedtuple('Entry', 'use forms kind base note source')


def read_text(path):
    raw = open(path, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        return raw[3:].decode('utf-8', 'replace')
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('cp949', 'replace')


# ---------- glossary ----------

def split_row(line):
    cells = re.split(r'(?<!\\)\|', line.strip())
    if cells and cells[0].strip() == '':
        cells = cells[1:]
    if cells and cells[-1].strip() == '':
        cells = cells[:-1]
    return [c.strip().replace('\\|', '|') for c in cells]


def parse_forms(cell):
    forms = []
    for item in re.findall(r'`[^`]*`|[^,`]+', cell):
        item = item.strip()
        if len(item) >= 2 and item[0] == item[-1] == '`':
            item = item[1:-1]
        if not item.strip() or item.strip() in ('-', '—'):
            continue
        if item.startswith('re:'):
            forms.append(Form(item, re.compile(item[3:])))
        else:
            forms.append(Form(item, re.compile(r'(?<![가-힣])' + re.escape(item))))
    return forms


def parse_base(cell):
    m = re.search(r'\d+(\.\d+)?', cell or '')
    return float(m.group()) if m else None


def load_glossary(paths):
    entries, allows = [], []
    for path in paths:
        lines = read_text(path).split('\n')
        in_fence = False
        i = 0
        while i < len(lines):
            if re.match(r'^\s*(```|~~~)', lines[i]):
                in_fence = not in_fence
                i += 1
                continue
            is_table = (not in_fence and lines[i].lstrip().startswith('|') and i + 1 < len(lines)
                        and re.match(r'^\s*\|?\s*:?-{3,}', lines[i + 1]))
            if not is_table:
                i += 1
                continue
            header = [h.lower() for h in split_row(lines[i])]
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith('|'):
                row = dict(zip(header, split_row(lines[j])))
                if 'use' in row and 'avoid' in row:
                    kind = row.get('kind', 'review').strip().lower()
                    forms = parse_forms(row['avoid'])
                    if forms and kind in WORD_KINDS:
                        entries.append(Entry(row['use'], forms, kind, parse_base(row.get('base')),
                                             row.get('note', ''), os.path.basename(path)))
                elif 'allow' in row:
                    allows.extend(parse_forms(row['allow']))
                j += 1
            i = j
    return entries, allows


# ---------- text ----------

def prose_lines(text, include_quotes):
    """Yield (line number, text) outside fenced code. Table rows give their cells joined by ' / '."""
    fence = None
    for no, ln in enumerate(text.split('\n'), 1):
        m = re.match(r'^\s*(```|~~~)', ln)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            continue
        if fence:
            continue
        if re.match(r'^\s*\|?\s*:?-{3,}', ln):
            continue
        ln = re.sub(r'`[^`]*`', ' ', ln)
        ln = re.sub(r'<!--.*?-->', ' ', ln)
        ln = re.sub(r'\]\([^)]*\)', ']', ln)
        if ln.lstrip().startswith('|'):
            ln = ' / '.join(c for c in split_row(ln) if c)
        ln = re.sub(r'^\s*(#+|>|[-*+]|\d+[.)])\s+', '', ln)
        ln = ln.replace('**', '').replace('__', '')
        if not include_quotes:
            ln = QUOTED.sub(lambda q: ' ' * len(q.group()), ln)
        if HANGUL.search(ln):
            yield no, ln


def split_sentences(text):
    out, start = [], 0
    for m in SENT_END.finditer(text):
        out.append(text[start:m.end()].strip())
        start = m.end()
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return [s for s in out if len(HANGUL.findall(s)) >= 4 and is_sentence(s)]


def is_sentence(s):
    last = HANGUL.findall(s)
    return bool(last) and last[-1] in FINAL_SYLLABLES


def conditions(s):
    return sum(1 for m in COND.finditer(s) if m.group(1) not in NOT_COND)


def ownerless(s, prev):
    if not PRESENT_END.search(s.strip()):
        return False
    if not (ONLY_IF.search(s) or conditions(s) >= 2):
        return False
    if OWNER.search(s):
        return False
    return not (prev and OWNER.search(prev) and FRAME.search(prev))


def eojeol(s):
    return len([w for w in s.split() if HANGUL.search(w)])


class Stats:
    """Sentence measures for one file, compared in the summary with the book values in BASE."""

    def __init__(self):
        self.n = self.conj = self.cond = self.date = self.go = 0
        self.par_ratios = []

    def add(self, text, long_limit):
        """Count one prose line. Yield (sentence, kind, message) for owner, long and paren hits."""
        sents = split_sentences(text)
        self.n += len(sents)
        if len(sents) >= 4:
            self.par_ratios.append(sum(1 for s in sents if LINK_START.match(s) or LINK_IN.search(s)) / len(sents))
        prev = None
        for s in sents:
            bare = s.lstrip('"\'“” ')
            self.conj += bool(CONJ_START.match(bare))
            self.date += bool(DATE_START.match(bare))
            self.cond += conditions(s)
            self.go += len(GO_JOIN.findall(s))
            if ownerless(s, prev):
                yield s, 'owner', 'reason or condition with no owner (S3)'
            n = eojeol(s)
            if n > long_limit:
                yield s, 'long', f'{n} eojeol'
            if len(re.findall(r'\([^)]*[가-힣][^)]*\)', s)) >= 2:
                yield s, 'paren', 'parenthesis chain'
            prev = s

    def values(self):
        n = max(1, self.n)
        link = sum(self.par_ratios) / len(self.par_ratios) if self.par_ratios else None
        return {'conj': self.conj * 1000 / n, 'link': link, 'cond': self.cond * 100 / n,
                'date': self.date * 100 / n, 'go': self.go * 100 / n}

    def report(self):
        v = self.values()
        out = []
        for key, label, fmt in METRICS:
            if v[key] is None:
                continue
            nov, non = BASE[key]
            line = f'{label}: {fmt.format(v[key])} (books: novels {fmt.format(nov)}, Korean nonfiction {fmt.format(non)})'
            if key == 'link':
                line += f', {len(self.par_ratios)} paragraphs'
            if key == 'conj' and v[key] > 1.5 * non:
                line += '  ← above the books: check for a connective on every sentence (S2)'
            out.append(line)
        return out


# ---------- main ----------

def walk(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
                for f in sorted(files):
                    if os.path.splitext(f)[1].lower() in TEXT_EXT:
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            yield p
        else:
            print(f'not found: {p}', file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--terms', action='append', default=[], help='extra glossary file (repeatable)')
    ap.add_argument('--kind', default='replace,review,owner,long,paren',
                    help='kinds to list per line: ' + ', '.join(ALL_KINDS) + ' (default replace,review,owner,long,paren)')
    ap.add_argument('--summary', action='store_true', help='per-file totals only')
    ap.add_argument('--include-quotes', action='store_true', help='also check text inside quotation marks')
    ap.add_argument('--long', type=int, default=25, help='flag sentences longer than N eojeol (default 25)')
    ap.add_argument('--max-per-file', type=int, default=300)
    args = ap.parse_args()
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    show = {k.strip() for k in args.kind.split(',') if k.strip()}
    bad = show - set(ALL_KINDS)
    if bad:
        ap.error(f'unknown kind: {", ".join(sorted(bad))}')

    glossary = sorted(os.path.join(GLOSSARY_DIR, f) for f in os.listdir(GLOSSARY_DIR)
                      if f.endswith('.md') and f != 'README.md')
    extra = list(args.terms)
    if os.path.isfile(PROJECT_TERMS) and PROJECT_TERMS not in extra:
        extra.append(PROJECT_TERMS)
    entries, allows = load_glossary(glossary + extra)

    totals = collections.Counter()
    for path in walk(args.paths):
        text = read_text(path)
        if any(m in text for m in IGNORE_MARKS):
            continue
        lines = list(prose_lines(text, args.include_quotes))
        if not lines:
            continue
        chars = sum(len(HANGUL.findall(t)) for _, t in lines)
        hits = []
        density = collections.defaultdict(list)
        st = Stats()
        for no, t in lines:
            for s, kind, msg in st.add(t, args.long):
                hits.append((no, kind, msg, s[:60] + ('…' if len(s) > 60 else '')))
            allowed = [(m.start(), m.end()) for a in allows for m in a.rx.finditer(t)]
            for ei, e in enumerate(entries):
                for f in e.forms:
                    for m in f.rx.finditer(t):
                        if any(a <= m.start() < b for a, b in allowed):
                            continue
                        w = max(re.match(r'[가-힣]*', t[m.start():]).group(), m.group().strip(), key=len)
                        if e.kind == 'density':
                            density[ei].append((no, w))
                        else:
                            hits.append((no, e.kind, w, f'→ {e.use}' + (f'  ({e.note})' if e.note else '')))
        flagged = []
        for ei, found in density.items():
            e = entries[ei]
            rate = len(found) * 1e6 / max(1, chars)
            if len(found) >= 3 and (e.base is None or rate >= 3 * e.base):
                flagged.append((e, found, rate))
                for no, w in found:
                    hits.append((no, 'density', w, f'→ {e.use}'))
        hits.sort(key=lambda h: h[0])
        counts = collections.Counter(h[1] for h in hits)
        totals.update(counts)
        totals['files'] += 1

        print(f'== {path}  ({chars} hangul, {st.n} sentences)')
        print('   hits: ' + (', '.join(f'{k} {counts[k]}' for k in ALL_KINDS if counts[k]) or 'none'))
        for line in st.report():
            print('   ' + line)
        for e, found, rate in sorted(flagged, key=lambda x: -x[2]):
            base = f', books {e.base:g}' if e.base is not None else ''
            print(f'   density: {e.forms[0].label} ×{len(found)} ({rate:.0f} per 1M hangul{base}) → {e.use}')
        if args.summary:
            continue
        for no, kind, word, msg in hits[:args.max_per_file]:
            if kind in show:
                print(f'{path}:{no}: [{kind}] {word} {msg}')
        if len(hits) > args.max_per_file:
            print(f'   ... {len(hits) - args.max_per_file} more')
    print('total: ' + ', '.join(f'{k} {totals[k]}' for k in ('files',) + ALL_KINDS if totals[k]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
