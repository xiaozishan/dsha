# Convert simpleicons DeepSeek whale (24x24 viewBox) -> Android pathData
# 108x108 viewport, content centered inside 66x66 safe zone.
import re

svg = open(r'C:\Users\Administrator\AppData\Local\Temp\deepseek.svg', encoding='utf-8').read()
d = re.search(r'<path d="([^"]+)"', svg).group(1)

tok = re.findall(r'[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?', d)

# Parse to absolute segments
segs = []          # (cmd, [coords...]) with cmd in {M,L,C,Q,A,Z}, absolute
i = 0
cmd = None
x = y = 0.0        # current point
sx = sy = 0.0      # subpath start
pcx = pcy = None   # last cubic control (for S)
pqx = pqy = None   # last quad control (for T)
ARITY = {'M':2,'L':2,'H':1,'V':1,'C':6,'S':4,'Q':4,'T':2,'A':7,'Z':0}
while i < len(tok):
    if re.match(r'^[A-Za-z]$', tok[i]):
        cmd = tok[i]; i += 1
        if cmd in 'Zz':
            segs.append(('Z', [])); x, y = sx, sy
            pcx = pcy = pqx = pqy = None
            continue
    rel = cmd.islower()
    C = cmd.upper()
    n = ARITY[C]
    first_m = True
    while i < len(tok) and not re.match(r'^[A-Za-z]$', tok[i]):
        v = [float(tok[i+k]) for k in range(n)]; i += n
        if C == 'M':
            nx, ny = (v[0]+x, v[1]+y) if rel else (v[0], v[1])
            segs.append(('M', [nx, ny])); sx, sy = nx, ny; x, y = nx, ny
            cmd = 'l' if rel else 'L'; C = 'L'; rel = cmd.islower(); n = 2
            pcx = pcy = pqx = pqy = None
        elif C == 'L':
            nx, ny = (v[0]+x, v[1]+y) if rel else (v[0], v[1])
            segs.append(('L', [nx, ny])); x, y = nx, ny
            pcx = pcy = pqx = pqy = None
        elif C == 'H':
            nx = v[0]+x if rel else v[0]
            segs.append(('L', [nx, y])); x = nx
            pcx = pcy = pqx = pqy = None
        elif C == 'V':
            ny = v[0]+y if rel else v[0]
            segs.append(('L', [x, ny])); y = ny
            pcx = pcy = pqx = pqy = None
        elif C == 'C':
            pts = [(v[0]+x, v[1]+y), (v[2]+x, v[3]+y), (v[4]+x, v[5]+y)] if rel else [(v[0], v[1]), (v[2], v[3]), (v[4], v[5])]
            segs.append(('C', [*pts[0], *pts[1], *pts[2]]))
            pcx, pcy = pts[1]; x, y = pts[2]; pqx = pqy = None
        elif C == 'S':
            c1 = (2*x-pcx, 2*y-pcy) if pcx is not None else (x, y)
            p2 = (v[0]+x, v[1]+y) if rel else (v[0], v[1])
            pe = (v[2]+x, v[3]+y) if rel else (v[2], v[3])
            segs.append(('C', [*c1, *p2, *pe])); pcx, pcy = p2; x, y = pe; pqx = pqy = None
        elif C == 'Q':
            p1 = (v[0]+x, v[1]+y) if rel else (v[0], v[1])
            pe = (v[2]+x, v[3]+y) if rel else (v[2], v[3])
            segs.append(('Q', [*p1, *pe])); pqx, pqy = p1; x, y = pe; pcx = pcy = None
        elif C == 'T':
            p1 = (2*x-pqx, 2*y-pqy) if pqx is not None else (x, y)
            pe = (v[0]+x, v[1]+y) if rel else (v[0], v[1])
            segs.append(('Q', [*p1, *pe])); pqx, pqy = p1; x, y = pe; pcx = pcy = None
        elif C == 'A':
            pe = (v[5]+x, v[6]+y) if rel else (v[5], v[6])
            segs.append(('A', [v[0], v[1], v[2], int(v[3]), int(v[4]), *pe])); x, y = pe
            pcx = pcy = pqx = pqy = None

# bbox from all points (control-point hull; close enough for centering)
xs, ys = [], []
for c, v in segs:
    if c in ('M', 'L'):
        xs.append(v[0]); ys.append(v[1])
    elif c in ('C', 'Q'):
        xs += v[0::2]; ys += v[1::2]
    elif c == 'A':
        xs.append(v[5]); ys.append(v[6])
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
bw, bh = maxx-minx, maxy-miny
print(f'bbox: x[{minx:.3f},{maxx:.3f}] y[{miny:.3f},{maxy:.3f}] w={bw:.3f} h={bh:.3f}')

SAFE = 66.0
s = min(SAFE/bw, SAFE/bh)
tx = (108 - bw*s)/2 - minx*s
ty = (108 - bh*s)/2 - miny*s
def T(px, py): return (px*s+tx, py*s+ty)

def fmt(v):
    r = round(v, 3)
    out = f'{r:.3f}'.rstrip('0').rstrip('.')
    return '0' if out in ('-0', '') else out

parts = []
for c, v in segs:
    if c == 'Z':
        parts.append('z')
    elif c in ('M', 'L'):
        nx, ny = T(v[0], v[1])
        parts.append(f'{c}{fmt(nx)},{fmt(ny)}')
    elif c == 'C':
        p = [T(v[0], v[1]), T(v[2], v[3]), T(v[4], v[5])]
        parts.append('C' + ','.join(f'{fmt(a)} {fmt(b)}' for a, b in p).replace(' ', ','))
    elif c == 'Q':
        p = [T(v[0], v[1]), T(v[2], v[3])]
        parts.append('Q' + ','.join(f'{fmt(a)},{fmt(b)}' for a, b in p))
    elif c == 'A':
        pe = T(v[5], v[6])
        parts.append(f'A{fmt(v[0]*s)},{fmt(v[1]*s)} {fmt(v[2])} {v[3]},{v[4]} {fmt(pe[0])},{fmt(pe[1])}')

pathdata = ''.join(parts)
print(f'scale={s:.4f} tx={tx:.3f} ty={ty:.3f}')
print('PATHDATA_START')
print(pathdata)
print('PATHDATA_END')
# transformed bbox sanity
nxs, nys = [px*s+tx for px in xs], [py*s+ty for py in ys]
print(f'new bbox: x[{min(nxs):.2f},{max(nxs):.2f}] y[{min(nys):.2f},{max(nys):.2f}] center=({(min(nxs)+max(nxs))/2:.2f},{(min(nys)+max(nys))/2:.2f})')
