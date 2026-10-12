"""Render a compact, looping AI pipeline animation for the GitHub profile."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT = 960, 112
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 17)
SMALL = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
frames = []
for index in range(48):
    phase = index / 48
    image = Image.new('RGB', (WIDTH, HEIGHT), '#14112b')
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, WIDTH-2, HEIGHT-2), radius=16, outline='#39334f')
    draw.text((25, 18), 'FROM SIGNAL TO SYSTEM', font=SMALL, fill='#a4aec5')
    nodes = [(150, 'VISION', '#67e8f9'), (375, 'AUDIO', '#b8a0ff'), (600, 'INFERENCE', '#f472b6'), (825, 'EDGE AI', '#67e8f9')]
    for start, end in zip(nodes, nodes[1:]):
        draw.line((start[0]+75, 69, end[0]-75, 69), fill='#45415c', width=2)
        x = start[0]+75 + (end[0]-start[0]-150)*phase
        draw.ellipse((x-3, 66, x+3, 72), fill='#b8a0ff')
    for i, (x, label, color) in enumerate(nodes):
        pulse = (1+math.sin(2*math.pi*(phase-i/4)))/2
        draw.rounded_rectangle((x-72, 48, x+72, 90), radius=9, fill='#202039', outline=color, width=1)
        draw.text((x, 69), label, anchor='mm', font=FONT, fill=color)
        radius = 2 + int(pulse*2)
        draw.ellipse((x-radius, 36-radius, x+radius, 36+radius), fill=color)
    frames.append(image)
frames[0].save(ROOT/'ai-pipeline.gif', save_all=True, append_images=frames[1:], duration=80, loop=0, optimize=True)
print(f'Created ai-pipeline.gif: {len(frames)} frames')
