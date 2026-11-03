# Swap in a new logo (trim empty transparent margins first so it reads at 48px tall):
# copies the PNG to assets/logo_en.png and rewrites the base64 block and the checksum in SKILL.md
# Usage: python3 scripts/update_logo.py <new_logo.png>
import base64, hashlib, pathlib, re, struct, sys, textwrap

root = pathlib.Path(__file__).resolve().parent.parent
data = pathlib.Path(sys.argv[1]).read_bytes()
if data[:8] != b'\x89PNG\r\n\x1a\n': sys.exit('Not a PNG file')
w, h = struct.unpack('>II', data[16:24])

skill = root / 'SKILL.md'; s = skill.read_text(encoding='utf-8')
b64 = '\n'.join(textwrap.wrap(base64.b64encode(data).decode(), 76))
digest = hashlib.sha256(data).hexdigest()[:16]
s, n1 = re.subn(r'(## Logo file.*?```text\n).*?(\n```)', lambda m: m.group(1) + b64 + m.group(2), s, count=1, flags=re.S)
s, n2 = re.subn(r'(# Expected output: )[0-9a-f]{16}', lambda m: m.group(1) + digest, s)
if n1 != 1 or n2 != 1: sys.exit('Could not find the logo block or checksum line in SKILL.md; nothing was changed')

(root / 'assets' / 'logo_en.png').write_bytes(data)
skill.write_text(s, encoding='utf-8')
print(f'Logo updated: {w}x{h}px, checksum {digest}')
print('The slides show the logo at 48px tall. Re-render a test deck and check the logo strip on every slide')
