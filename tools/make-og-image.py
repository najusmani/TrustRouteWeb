"""Generates site/assets/img/og-image.png: the 1200x630 preview shown when the site is shared
(LinkedIn, WhatsApp, email). Run:  python tools/make-og-image.py   (needs Pillow; Windows fonts)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY_DEEP, NAVY = (9, 21, 48), (14, 31, 63)
GOLD, GOLD_SOFT = (168, 131, 63), (201, 174, 120)
WHITE, MUTED = (255, 255, 255), (184, 196, 216)
FONTS = Path('C:/Windows/Fonts')

def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)

img = Image.new('RGB', (W, H), NAVY_DEEP)
d = ImageDraw.Draw(img)

# soft vertical gradient
for y in range(H):
    t = y / H
    c = tuple(int(NAVY[i] * (1 - t) + NAVY_DEEP[i] * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# faint concentric diamonds on the right (brand motif)
cx, cy = 1010, 315
for r, a in ((330, 40), (250, 55), (170, 70)):
    col = tuple(int(NAVY_DEEP[i] + (GOLD_SOFT[i] - NAVY_DEEP[i]) * a / 255) for i in range(3))
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], outline=col, width=2)

# a gold route line
d.line([(560, 560), (760, 470), (900, 360), (1010, 315)], fill=GOLD_SOFT, width=2)
d.ellipse([1003, 308, 1017, 322], fill=GOLD_SOFT)

# emblem: diamond + serif T + destination diamond
ex, ey, s = 120, 150, 2.2   # top-left of a 56x56 emblem, scaled
P = lambda x, y: (ex + x * s, ey + y * s)
d.polygon([P(28, 2), P(54, 28), P(28, 54), P(2, 28)], outline=GOLD_SOFT, width=3)
d.line([P(17.5, 20.5), P(38.5, 20.5)], fill=WHITE, width=6)
d.line([P(17.5, 20.5), P(17.5, 24)], fill=WHITE, width=3)
d.line([P(38.5, 20.5), P(38.5, 24)], fill=WHITE, width=3)
d.line([P(28, 20.5), P(28, 36.5)], fill=WHITE, width=6)
d.polygon([P(28, 39.5), P(30.6, 42.1), P(28, 44.7), P(25.4, 42.1)], fill=GOLD_SOFT)

# wordmark (letter-spaced)
def spaced(xy, text, f, fill, spacing):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing
    return x

spaced((270, 168), 'TRUSTROUTE', font('GARA.TTF', 50), WHITE, 9)
spaced((273, 232), 'TECHNOLOGIES', font('bahnschrift.ttf', 17), GOLD_SOFT, 11)

# tagline
d.text((120, 330), 'Trusted counsel for the', font=font('GARA.TTF', 62), fill=WHITE)
d.text((120, 400), 'future of banking.', font=font('GARAIT.TTF', 62), fill=GOLD_SOFT)

# footer line
d.line([(120, 520), (300, 520)], fill=GOLD, width=2)
d.text((120, 540), 'BANKING TECHNOLOGY ADVISORY & SOLUTIONS', font=font('bahnschrift.ttf', 18), fill=MUTED)
d.text((120, 568), 'trustroutetechnologies.com', font=font('bahnschrift.ttf', 18), fill=GOLD_SOFT)

out = Path(__file__).resolve().parent.parent / 'site' / 'assets' / 'img' / 'og-image.png'
img.save(out, 'PNG', optimize=True)
print(f'wrote {out} ({out.stat().st_size // 1024} KB)')
