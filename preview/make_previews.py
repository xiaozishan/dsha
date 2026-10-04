# Generate 5 preview HTML files (light/dark x square/circle + monochrome)
# then screenshot each with Chrome headless at 512x512.
import re, subprocess, os

BASE = r'C:\Users\Administrator\.openclaw\workspace\projects\dsha-v1.2.0-rc1.4\preview'
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

fg_xml = open(os.path.join(BASE, '..', r'app\src\main\res\drawable\dsha_launcher_foreground.xml'), encoding='utf-8').read()
PATH = re.search(r'android:pathData="([^"]+)"', fg_xml).group(1)

HTML = """<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;padding:0;overflow:hidden;background:#B9C0CC}}</style></head>
<body><svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
<defs><clipPath id="s">{clip}</clipPath></defs>
<g transform="translate(40,40) scale(4)">
<g clip-path="url(#s)">
<rect width="108" height="108" fill="{bg}"/>
<path d="{path}" fill="{fg}" fill-rule="evenodd"/>
</g></g></svg></body></html>"""

SQUARE = '<rect width="108" height="108" rx="24"/>'
CIRCLE = '<circle cx="54" cy="54" r="54"/>'

jobs = [
    ('light_square', SQUARE, '#EDF1FA', '#1C2635'),
    ('dark_square',  SQUARE, '#161D29', '#F2F5FC'),
    ('light_circle', CIRCLE, '#EDF1FA', '#1C2635'),
    ('dark_circle',  CIRCLE, '#161D29', '#F2F5FC'),
    ('monochrome',   CIRCLE, '#E4E8F0', '#3D4B63'),
]

for name, clip, bg, fg in jobs:
    html_path = os.path.join(BASE, f'{name}.html')
    png_path = os.path.join(BASE, f'{name}.png')
    open(html_path, 'w', encoding='utf-8').write(HTML.format(clip=clip, bg=bg, fg=fg, path=PATH))
    r = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--no-first-run', '--no-default-browser-check',
                        rf'--user-data-dir={os.environ["TEMP"]}\chrome-hl',
                        f'--screenshot={png_path}', '--window-size=512,512',
                        f'file:///{html_path.replace(os.sep, "/")}'],
                       capture_output=True, text=True, timeout=60)
    import time; time.sleep(1.5)
    ok = os.path.exists(png_path) and os.path.getsize(png_path) > 1000
    print(f'{name}: exit={r.returncode} size={os.path.getsize(png_path) if os.path.exists(png_path) else 0} ok={ok}')
