"""Create two counter-moving rows of technology badges for GitHub."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, SCALE = 960, 160, 2
FONT = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16*SCALE)
ICON = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 14*SCALE)
ROWS = [
    [('PyTorch', 'PT', '#EE4C2C'), ('TensorFlow', 'TF', '#FF9C38'), ('Python', 'Py', '#70B7F3'), ('OpenCV', 'CV', '#A99AFF')],
    [('FastAPI', 'FA', '#44D9BF'), ('Docker', 'DK', '#59B9FF'), ('Pandas', 'PD', '#BA9EFF'), ('Raspberry Pi', 'RP', '#F47CA4')],
]
frames = []
for frame_index in range(80):
    phase = 2*math.pi*frame_index/80
    im = Image.new('RGB', (W*SCALE, H*SCALE), '#14112b')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 2, W*SCALE-3, H*SCALE-3), radius=16*SCALE, outline='#39334f', width=SCALE)
    for row_index, row in enumerate(ROWS):
        # Cosine easing changes direction smoothly; every badge remains visible.
        shift = math.cos(phase) * 38 * (1 if row_index == 0 else -1)
        y = (20+row_index*70)*SCALE
        for column, (name, symbol, color) in enumerate(row):
            x = int((60+column*216+shift)*SCALE)
            d.rounded_rectangle((x, y, x+190*SCALE, y+50*SCALE), radius=12*SCALE, fill='#202039', outline='#45415c', width=SCALE)
            d.rounded_rectangle((x+10*SCALE, y+10*SCALE, x+40*SCALE, y+40*SCALE), radius=7*SCALE, fill=color)
            d.text((x+25*SCALE, y+25*SCALE), symbol, font=ICON, fill='#14112b', anchor='mm')
            d.text((x+51*SCALE, y+25*SCALE), name, font=FONT, fill='#f0edff', anchor='lm')
    frames.append(im.resize((W,H), Image.Resampling.LANCZOS))
frames[0].save(ROOT/'toolkit-motion.gif', save_all=True, append_images=frames[1:], duration=90, loop=0, optimize=True)
frames[0].save(ROOT/'toolkit-preview.png')
print('Created toolkit-motion.gif')
