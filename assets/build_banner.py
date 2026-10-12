"""Build the animated profile banner using Pillow and local Windows fonts."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1200, 400
FONT_ROOT = Path('C:/Windows/Fonts')

def font(size, bold=False, mono=False):
    name = 'consola.ttf' if mono else ('segoeuib.ttf' if bold else 'segoeui.ttf')
    return ImageFont.truetype(str(FONT_ROOT / name), size)

base = Image.new('RGB', (W, H))
pixels = base.load()
for y in range(H):
    for x in range(W):
        glow = math.exp(-(((x-970)/330)**2 + ((y-190)/250)**2))
        pixels[x, y] = (int(16+21*glow), int(18+9*glow), int(35+44*glow))
grid = ImageDraw.Draw(base)
for x in range(0, W, 40):
    grid.line((x, 0, x, H), fill=(32, 31, 53))
for y in range(0, H, 40):
    grid.line((0, y, W, y), fill=(32, 31, 53))

frames = []
for i in range(48):
    phase = 2*math.pi*i/48
    frame = base.copy()
    d = ImageDraw.Draw(frame)
    cyan, purple, pink = '#67e8f9', '#b8a0ff', '#f472b6'
    # One shared left edge and measured text keep all labels aligned.
    d.rounded_rectangle((64, 44, 334, 76), radius=16, fill='#142d3e', outline='#31596c')
    pulse = int(170+70*(1+math.sin(phase))/2)
    d.ellipse((79, 56, 87, 64), fill=(70, pulse, 235))
    d.text((99, 50), 'COMPUTER VISION / APPLIED AI', font=font(13, True), fill=cyan)
    d.text((64, 103), 'Nguyen Minh Chanh', font=font(51, True), fill='#f6f4ff')
    d.text((64, 171), 'JayC  /  AI Undergraduate', font=font(22, True), fill=purple)
    d.text((64, 221), 'Building real-world intelligent systems.', font=font(23), fill='#d6d4f1')
    d.text((64, 263), 'FPT University  ·  Can Tho, Vietnam', font=font(17), fill='#a4aec5')
    for x, width, label, color, bg in [(64, 105, 'AI / ML', purple, '#30254f'), (181, 165, 'COMPUTER VISION', cyan, '#163747'), (358, 105, 'EDGE AI', pink, '#3c2442')]:
        d.rounded_rectangle((x, 321, x+width, 353), radius=9, fill=bg)
        d.text((x+width/2, 337), label, anchor='mm', font=font(12, True), fill=color)
    # Orbiting nodes around a fixed terminal.
    cx, cy = 949, 200
    for tilt, color in [(-0.5, '#514576'), (0.55, '#274959')]:
        points=[]
        for j in range(101):
            a=2*math.pi*j/100
            ex, ey=174*math.cos(a), 115*math.sin(a)
            points.append((cx+ex*math.cos(tilt)-ey*math.sin(tilt), cy+ex*math.sin(tilt)+ey*math.cos(tilt)))
        d.line(points, fill=color, width=1)
    for offset, color in [(0, cyan), (math.pi, pink)]:
        angle=phase+offset
        ex, ey=174*math.cos(angle), 115*math.sin(angle)
        nx=cx+ex*math.cos(-.5)-ey*math.sin(-.5)
        ny=cy+ex*math.sin(-.5)+ey*math.cos(-.5)
        d.ellipse((nx-7, ny-7, nx+7, ny+7), fill=color)
    d.rounded_rectangle((809, 99, 1089, 301), radius=17, fill='#15172b', outline='#71608f', width=2)
    d.line((810, 142, 1088, 142), fill='#33334e')
    for x, color in [(833, '#fb7185'), (851, '#fbbf24'), (869, '#34d399')]:
        d.ellipse((x-4, 117, x+4, 125), fill=color)
    d.text((833, 158), 'focus = [', font=font(16, mono=True), fill=purple)
    d.text((851, 191), '"vision",', font=font(16, mono=True), fill=cyan)
    d.text((851, 224), '"research", "build"', font=font(16, mono=True), fill=pink)
    d.text((833, 257), ']', font=font(16, mono=True), fill='#e2e8f0')
    if i < 24:
        d.rectangle((851, 260, 861, 279), fill=cyan)
    for x in range(64, 1137):
        t=(x-64)/1072
        d.line((x, 383, x, 385), fill=(int(34+210*t), int(211-97*t), int(238-56*t)))
    frames.append(frame)

# A shared palette avoids color flicker between frames.
palette = frames[0].quantize(colors=128)
indexed = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
indexed[0].save(ROOT/'banner.gif', save_all=True, append_images=indexed[1:], duration=90, loop=0, optimize=True, disposal=1)
frames[0].save(ROOT/'banner-preview.png')
with Image.open(ROOT/'banner.gif') as animation:
    assert animation.n_frames > 1
    assert animation.info.get('loop') == 0
    duration = 0
    for frame_index in range(animation.n_frames):
        animation.seek(frame_index)
        duration += animation.info['duration']
    assert duration == 48 * 90
    print(f'Validated {animation.n_frames} optimized frames, {duration} ms loop')
print(f'Built {len(frames)} frames: {(ROOT / "banner.gif").stat().st_size:,} bytes')
