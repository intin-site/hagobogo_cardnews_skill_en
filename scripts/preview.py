# Preview sheet: shrink slides/*.png and tile them into one image (3 columns up to 6 slides, 4 columns from 7)
import sys, pathlib
from PIL import Image
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'slides'); out = sys.argv[2] if len(sys.argv) > 2 else 'preview_sheet.png'
fs = sorted(src.glob('*.png')); cols = 3 if len(fs) <= 6 else 4; rows = -(-len(fs) // cols)
W, H, g = 360, 450, 24
sheet = Image.new('RGB', (cols*W + (cols+1)*g, rows*H + (rows+1)*g), 'white')
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((W, H), Image.LANCZOS)
    sheet.paste(im, (g + (i % cols)*(W+g), g + (i // cols)*(H+g)))
sheet.save(out); print(f'{out} ({len(fs)} slides, {cols} columns)')
