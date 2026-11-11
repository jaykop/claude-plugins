#!/usr/bin/env python3
"""Find glossary candidates and style signals in Korean comments and documents.

The glossary is the Markdown tables under ../glossary/ that have `Use` and
`Avoid` columns, plus an optional project terms file. Avoid forms are matched
against comment and document text only: code, identifiers and string literals
are skipped. Every hit is a candidate. A person or agent decides each one.

Usage:
  python ko_lint.py [--summary] [--kind replace,review,density] [--terms FILE] PATH [PATH ...]

Exit code is 0 unless the arguments are wrong.
"""
import argparse
import collections
import errno
import io
import os
import re
import sys

HANGUL = re.compile('[가-힣぀-ヿ]')  # Hangul, or kana mixed into Korean text
C_LIKE = {'.h', '.hh', '.hpp', '.inl', '.c', '.cc', '.cpp', '.cxx', '.cs', '.java', '.kt', '.swift',
          '.js', '.ts', '.tsx', '.go', '.rs', '.hlsl', '.usf', '.ush', '.shader', '.uc'}
HASH = {'.py', '.gd', '.ps1', '.sh', '.yaml', '.yml', '.toml'}
DOCS = {'.md', '.txt', '.rst'}
INI = {'.ini'}
SKIP_DIRS = {'.git', '.svn', '.vs', '.idea', 'Binaries', 'Intermediate', 'Saved', 'DerivedDataCache',
             'node_modules', 'ThirdParty', '__pycache__'}
IGNORE_MARK = 'ko-lint: ignore-file'
KINDS = ('replace', 'review', 'density')
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GLOSSARY_DIR = os.path.join(SKILL_DIR, 'glossary')
PROJECT_TERMS = os.path.join('.claude', 'ko-gamedev', 'terms.md')

Form = collections.namedtuple('Form', 'label needle rx')
Entry = collections.namedtuple('Entry', 'use forms kind note source')


def read_text(path):
    raw = open(path, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        return raw[3:].decode('utf-8', 'replace')
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
        return raw.decode('utf-16', 'replace')
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
            item = item[1:-1]  # keep spaces inside backticks: a regex may end in one
        if not item.strip() or item.strip() in ('-', '—'):
            continue
        if item.startswith('re:'):
            forms.append(Form(item, None, re.compile(item[3:])))
        else:
            forms.append(Form(item, item, re.compile(r'(?<![가-힣])' + re.escape(item))))
    return forms


def load_glossary(paths):
    entries, allows = [], []
    for path in paths:
        lines = [ln for _, ln in doc_lines(read_text(path), keep_code_spans=True)]
        i = 0
        while i < len(lines):
            is_table = (lines[i].lstrip().startswith('|') and i + 1 < len(lines)
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
                    if forms and kind in KINDS:
                        entries.append(Entry(row['use'], forms, kind, row.get('note', ''), os.path.basename(path)))
                elif 'allow' in row:
                    allows.extend(parse_forms(row['allow']))
                j += 1
            i = j
    return entries, allows


# ---------- text extraction ----------

def strip_marker(s):
    return re.sub(r'^\s*(/+[!<]?|\*+(?!/))', '', s).strip()


def c_comments(text):
    """Yield (line, text) for each line of // and /* */ comments. String literals are skipped."""
    i, n, line = 0, len(text), 1
    while i < n:
        c = text[i]
        if c == '\n':
            line += 1
            i += 1
            continue
        if c == '"' and i > 0 and text[i - 1] == 'R':
            m = re.match(r'"([^(\s"]{0,16})\(', text[i:])
            if m:
                end = text.find(')' + m.group(1) + '"', i)
                end = n if end < 0 else end
                line += text.count('\n', i, end)
                i = end + len(m.group(1)) + 2
                continue
        if c in '"\'':
            i += 1
            while i < n and text[i] != c and text[i] != '\n':
                i += 2 if text[i] == '\\' else 1
            i += 1
            continue
        if text.startswith('//', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            yield line, strip_marker(text[i:j])
            i = j
            continue
        if text.startswith('/*', i):
            j = text.find('*/', i + 2)
            j = n if j < 0 else j
            for k, part in enumerate(text[i + 2:j].split('\n')):
                yield line + k, strip_marker(part)
            line += text.count('\n', i, j)
            i = j + 2
            continue
        i += 1


def hash_index(ln):
    quote, i = None, 0
    while i < len(ln):
        ch = ln[i]
        if quote:
            if ch == '\\':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in '"\'':
            quote = ch
        elif ch == '#':
            return i
        i += 1
    return -1


def hash_comments(text):
    triple = None
    for no, ln in enumerate(text.split('\n'), 1):
        if triple:
            end = ln.find(triple)
            yield no, ln if end < 0 else ln[:end]
            if end >= 0:
                triple = None
            continue
        m = re.match(r'\s*[rRbBuU]?("""|\'\'\')', ln)
        if m:
            rest = ln[m.end():]
            if m.group(1) in rest:
                yield no, rest[:rest.find(m.group(1))]
            else:
                triple = m.group(1)
                yield no, rest
            continue
        k = hash_index(ln)
        if k >= 0:
            yield no, ln[k + 1:].strip()


def ini_comments(text):
    for no, ln in enumerate(text.split('\n'), 1):
        s = ln.strip()
        if s.startswith((';', '#')):
            yield no, s[1:].strip()
        for m in re.finditer(r'DevComment\s*=\s*"([^"]*)"', ln):
            yield no, m.group(1)


def doc_lines(text, keep_code_spans=False):
    """Yield (line, text) outside fenced code blocks. Inline code spans and HTML comments become spaces."""
    fence = None
    for no, ln in enumerate(text.split('\n'), 1):
        m = re.match(r'^\s*(```|~~~)', ln)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            continue
        if fence:
            continue
        if not keep_code_spans:
            ln = re.sub(r'`[^`]*`', ' ', ln)
            ln = re.sub(r'<!--.*?-->', ' ', ln)
        yield no, ln


def extract(path, text):
    ext = os.path.splitext(path)[1].lower()
    if ext in C_LIKE:
        return c_comments(text)
    if ext in HASH:
        return hash_comments(text)
    if ext in INI:
        return ini_comments(text)
    if ext in DOCS:
        return doc_lines(text)
    return iter(())


def walk(paths):
    exts = C_LIKE | HASH | DOCS | INI
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        if not os.path.isdir(p):
            print(f'ko_lint: not found: {p}', file=sys.stderr)
            continue
        for dp, dn, fn in os.walk(p):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for name in sorted(fn):
                if os.path.splitext(name)[1].lower() in exts:
                    yield os.path.join(dp, name)


# ---------- style ----------

def ending(ln):
    s = re.sub(r'[\s.!?…~\-=/*:;,]+$', '', ln)
    m = re.search(r'([가-힣A-Za-z0-9_)\]"\']+)$', s)
    w = m.group(1) if m else s[-1:]
    if not re.search('[가-힣]$', w):
        return 'other'
    # ~니다 only after a syllable ending in ㅂ (합니다, 입니다, 습니다); 아니다 is a ~다 sentence.
    if len(w) >= 3 and w.endswith('니다') and (ord(w[-3]) - 0xAC00) % 28 == 17:
        return '~니다'
    if re.search('(어요|아요|해요|에요|예요|네요|지요|죠|까요|세요|래요)$', w):
        return '~요'
    if re.search('(함|음|임|됨)$', w):
        return '~함'
    if re.search('다$', w):
        return '~다'
    return 'noun'


def pretty(label):
    """Drop "re:" and lookaround groups so a density regex prints as the mark itself."""
    return re.sub(r'\(\?<?[=!](?:\[[^\]]*\]|[^)])*\)', '', label[3:]) if label.startswith('re:') else label


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('paths', nargs='+')
    ap.add_argument('--terms', action='append', default=[], help='extra glossary file (repeatable)')
    ap.add_argument('--kind', default='replace,review',
                    help='kinds to list per line: replace, review, density (default replace,review)')
    ap.add_argument('--summary', action='store_true', help='totals and per-file lines only')
    ap.add_argument('--max-per-file', type=int, default=200)
    args = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    glossary = sorted(os.path.join(GLOSSARY_DIR, f) for f in os.listdir(GLOSSARY_DIR) if f.endswith('.md'))
    project = list(args.terms)
    if not project and os.path.isfile(PROJECT_TERMS):
        project.append(PROJECT_TERMS)
    entries, allows = load_glossary(glossary + project)
    listed = {k.strip() for k in args.kind.split(',')}

    totals = collections.Counter()
    by_entry = collections.Counter()
    words = collections.defaultdict(collections.Counter)
    endings_all = collections.Counter()
    density_all = collections.Counter()
    reports = []
    n_files = n_lines = 0

    for path in walk(args.paths):
        try:
            text = read_text(path)
        except OSError as e:
            print(f'ko_lint: {path}: {e}', file=sys.stderr)
            continue
        if IGNORE_MARK in text[:4000]:
            continue
        hits, endings, density = [], collections.Counter(), collections.Counter()
        lines = 0
        for no, txt in extract(path, text):
            if not HANGUL.search(txt):
                continue
            lines += 1
            endings[ending(txt)] += 1
            blocked = [m.span() for f in allows for m in f.rx.finditer(txt)]
            for e in entries:
                found = None  # one hit per line and entry; 돌려준다 and 돌려준 are the same hit
                for f in e.forms:
                    if f.needle and f.needle not in txt:
                        continue
                    for m in f.rx.finditer(txt):
                        if any(s <= m.start() and m.end() <= t for s, t in blocked):
                            continue
                        if e.kind == 'density':
                            density[pretty(f.label)] += 1
                        # Show the whole word: the form 돌려주 prints as 돌려주므로.
                        word = m.group(0) + re.match('[가-힣]*', txt[m.end():]).group(0)
                        if found is None or len(word) > len(found):
                            found = word
                if found:
                    hits.append((no, e, found.strip(), txt.strip()))
        if not lines:
            continue
        n_files += 1
        n_lines += lines
        endings_all.update(endings)
        density_all.update(density)
        for _, e, word, _ in hits:
            if e.kind == 'density':
                continue
            totals[e.kind] += 1
            by_entry[(e.kind, e.use, e.note)] += 1
            words[(e.kind, e.use, e.note)][word] += 1
        reports.append((path, lines, endings, density, hits))

    def ending_text(c):
        tot = sum(c.values()) or 1
        return ' / '.join(f'{k} {100 * c[k] // tot}%' for k in ('noun', '~다', '~함', '~니다', '~요') if c[k])

    def density_text(c):
        return ', '.join(f'{k} x{n}' for k, n in c.most_common())

    print(f'ko_lint: {n_files} files, {n_lines} Korean lines, '
          f'{sum(totals.values())} hits (replace {totals["replace"]}, review {totals["review"]})')
    print(f'glossary: {len(entries)} entries from {len(glossary)} files'
          + (f'; project terms: {", ".join(project)}' if project else '; no project terms file'))
    print(f'endings (all): {ending_text(endings_all)}')
    if density_all:
        print(f'density (all, not in hits): {density_text(density_all)}')
    if by_entry:
        print('\ntop entries')
        for (kind, use, note), n in by_entry.most_common(30):
            sample = ', '.join(w for w, _ in words[(kind, use, note)].most_common(4))
            print(f'  {kind:7} {use} <- {sample}  x{n}')

    for path, lines, endings, density, hits in reports:
        shown = [h for h in hits if h[1].kind in listed]
        if args.summary and not shown and not density:
            continue
        rel = os.path.relpath(path) if not os.path.isabs(path) or os.path.splitdrive(path)[0] == os.path.splitdrive(os.getcwd())[0] else path
        n_hits = sum(1 for h in hits if h[1].kind != 'density')
        print(f'\n== {rel} ({lines} lines; {ending_text(endings)}'
              + (f'; {density_text(density)}' if density else '') + f'; hits {n_hits})')
        if args.summary:
            continue
        for no, e, form, txt in shown[:args.max_per_file]:
            print(f'  L{no:<5} {e.kind:7} {form} -> {e.use}  | {txt[:110]}')
        if len(shown) > args.max_per_file:
            print(f'  ... {len(shown) - args.max_per_file} more')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except OSError as e:
        # A reader such as `head` closed the pipe; on Windows this shows up as EINVAL.
        if e.errno not in (errno.EPIPE, errno.EINVAL):
            raise
        sys.stdout = open(os.devnull, 'w')
        sys.exit(0)
