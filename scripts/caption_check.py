# caption.md format check: short caption / pinned comment length, hashtags (5, lowercase), standard disclaimer, HAGOBOGO paragraph in the pinned comment
# Usage: python3 caption_check.py caption.md
import re, sys

DISC = 'Note: For educational purposes only. For personal health concerns, talk to a doctor.'
BRAND_TAG = '#hagobogo'      # first hashtag; every hashtag is written in lowercase (brand decision)
SHORT_WORDS = (95, 170)      # short caption: about 130 words (hashtag line excluded)
PIN_WORDS = (60, 120)        # pinned comment: about 90 words
# Words that make HAGOBOGO read like a diagnostic device. Only "observe" wording is allowed in the product paragraph
BANNED = re.compile(r'\b(test(s|ed|ing)?|diagnos\w*|measur\w*|analy[sz]\w*|screening|detect\w*|assess\w*|evaluat\w*|exam(s|ine[sd]?|ining|ination)?|count(s|ed|ing)?)\b', re.I)

t = open(sys.argv[1] if len(sys.argv) > 1 else 'caption.md', encoding='utf-8').read()
bad, info = [], []

def sec(name):
    m = re.search(r'^## ' + name + r'\s*\n(.*?)(?=^---\s*$|^## |\Z)', t, re.S | re.M | re.I)
    return m.group(1).strip('\n') if m else None

def words(body):
    return sum(len(l.split()) for l in body.split('\n') if l.strip() and not l.strip().startswith('#'))

def chars(body):
    return len(''.join(l for l in body.split('\n') if l.strip() and not l.strip().startswith('#')))

def tags_check(name, body):
    lines = body.rstrip().split('\n')
    last = lines[-1].strip()
    if not last.startswith('#'):
        bad.append(f'{name}: the last line is not the hashtag line')
        return
    tags = last.split()
    if len(tags) != 5: bad.append(f'{name}: {len(tags)} hashtags (must be 5)')
    if tags[0].lower() != BRAND_TAG: bad.append(f'{name}: the first hashtag is not {BRAND_TAG}')
    upper = [x for x in tags if x != x.lower()]
    if upper: bad.append(f'{name}: hashtags must be all lowercase: {" ".join(upper)}')
    if len(lines) < 4 or lines[-2].strip() or lines[-3].strip() or not lines[-4].strip():
        bad.append(f'{name}: there must be exactly 2 blank lines between the last sentence and the hashtag line')

for name in ['Long caption', 'Short caption', 'Pinned comment']:
    if sec(name) is None: bad.append(f'missing "## {name}" section')

detail, short, pin = sec('Long caption'), sec('Short caption'), sec('Pinned comment')
for name, body in [('Long caption', detail), ('Short caption', short)]:
    if body is None: continue
    if DISC not in body: bad.append(f'{name}: the standard disclaimer line is missing or altered')
    tags_check(name, body)

if short:
    n = words(short)
    info.append(f'Short caption: {n} words / {chars(short)} characters (hashtag line excluded; target about 130 words)')
    if not SHORT_WORDS[0] <= n <= SHORT_WORDS[1]: bad.append(f'Short caption: {n} words, outside about 130 ({SHORT_WORDS[0]}-{SHORT_WORDS[1]})')

if pin:
    paras = [p for p in re.split(r'\n\s*\n', pin.strip()) if p.strip()]
    n = sum(len(l.split()) for l in pin.split('\n') if l.strip())
    info.append(f'Pinned comment: {n} words / {len("".join(l for l in pin.split(chr(10)) if l.strip()))} characters (target about 90 words)')
    if not PIN_WORDS[0] <= n <= PIN_WORDS[1]: bad.append(f'Pinned comment: {n} words, outside about 90 ({PIN_WORDS[0]}-{PIN_WORDS[1]})')
    if re.search(r'(^|\s)#\w', pin): bad.append('Pinned comment: contains a hashtag')
    last = paras[-1] if paras else ''
    if 'hagobogo' not in last.lower(): bad.append('Pinned comment: the last paragraph does not suggest HAGOBOGO')
    elif not re.search(r'\bobserv', last, re.I): bad.append('Pinned comment: the HAGOBOGO paragraph does not use "observe" wording')
    hit = sorted({m.group(0).lower() for m in BANNED.finditer(last)})
    if hit: bad.append(f'Pinned comment: banned wording in the HAGOBOGO paragraph: {", ".join(hit)}')
    if len(paras) < 2: bad.append('Pinned comment: the key-info paragraph and the HAGOBOGO paragraph are not separated')

print('\n'.join(info))
print('\n'.join(bad) if bad else 'Caption format OK')
