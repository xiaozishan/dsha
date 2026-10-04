# Generate preview PNGs that mimic a real launcher crop:
# show the VISIBLE 72x72 dp of the 108x108 adaptive canvas, masked (square/circle),
# with the current 1.08x whale scale applied. Also verifies the whale stays inside
# the 66dp safe circle (radius 33dp) / visible circle (r=36dp).
import re, subprocess, os, time, math
from PIL import Image

BASE = r'C:\Users\Administrator\.openclaw\workspace\projects\dsha-v1.2.0-rc1.4\preview'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
SCALE = 1.0

fg_xml = open(os.path.join(BASE, '..', r'app\src\main\res\drawable\dsha_launcher_foreground.xml'), encoding='utf-8').read()
PATH = re.search(r'android:pathData="([^"]+)"', fg_xml).group(1)

# 108-space visible region [18,90] -> full 512 canvas
S = 512 / 72.0
TX = -18 * S

TPL = """<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;overflow:hidden;background:#AEB6C4}}</style></head>
<body><svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="s">{clip}</clipPath></defs>
<g transform="translate({tx},{tx}) scale({s})">
<g clip-path="url(#s)">
<rect width="108" height="108" fill="{bg}"/>
<g transform="translate(54,54) scale({scale}) translate(-54,-54)">
<path d="{path}" fill="{fg}" fill-rule="evenodd"/>
</g></g></g></svg></body></html>"""

SQUARE = '<rect x="18" y="18" width="72" height="72" rx="18"/>'
CIRCLE = '<circle cx="54" cy="54" r="36"/>'

jobs = [
    ('light_square', SQUARE, '#EDF1FA', '#1C2635'),
    ('dark_square',  SQUARE, '#161D29', '#F2F5FC'),
    ('light_circle', CIRCLE, '#EDF1FA', '#1C2635'),
    ('dark_circle',  CIRCLE, '#161D29', '#F2F5FC'),
    ('monochrome',   CIRCLE, '#E4E8F0', '#3D4B63'),
]

def shot(html, png, w, h):
    html_path = os.path.splitext(png)[0] + '.html'
    open(html_path, 'w', encoding='utf-8').write(html)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                    '--no-first-run', '--no-default-browser-check',
                    rf'--user-data-dir={os.environ["TEMP"]}\chrome-hl',
                    f'--screenshot={png}', f'--window-size={w},{h}',
                    f'file:///{html_path.replace(os.sep, "/")}'],
                   capture_output=True, text=True, timeout=60)
    time.sleep(1.2)

for name, clip, bg, fg in jobs:
    html = TPL.format(clip=clip, tx=round(TX, 3), s=round(S, 4), bg=bg, fg=fg, scale=SCALE, path=PATH)
    shot(html, os.path.join(BASE, f'{name}.png'), 512, 512)
    print(name, 'ok', os.path.getsize(os.path.join(BASE, f'{name}.png')))

# ---- verification: whale-only at 10x, measure radius from center in 108-space ----
vhtml = f"""<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#fff}}</style></head>
<body><svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">
<g transform="scale(10)"><g transform="translate(54,54) scale({SCALE}) translate(-54,-54)">
<path d="{PATH}" fill="#000" fill-rule="evenodd"/></g></g></svg></body></html>"""
vpng = os.path.join(BASE, '_verify_whale.png')
shot(vhtml, vpng, 1080, 1080)
im = Image.open(vpng).convert('L')
px = im.load()
maxr = 0.0; minx=999; maxx=-1; miny=999; maxy=-1
for y in range(1080):
    for x in range(1080):
        if px[x, y] < 128:
            cx, cy = x/10.0, y/10.0
            r = math.hypot(cx-54, cy-54)
            if r > maxr: maxr = r
            minx=min(minx,cx); maxx=max(maxx,cx); miny=min(miny,cy); maxy=max(maxy,cy)
print('whale bbox 108-space: x[%.2f,%.2f] y[%.2f,%.2f]  w=%.2f h=%.2f' % (minx,maxx,miny,maxy,maxx-minx,maxy-miny))
print('max radius from center = %.2f dp   (visible circle r=36, safe circle r=33)' % maxr)
