# -*- coding: utf-8 -*-
"""在深/浅色区块交界处插入渐变过渡带 div（幂等）。"""
import io, os, re

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DARK = ('hero', 'aliya-sec', 'section-dark', 'page-hero', 'cat-hero')
LIGHT = ('section', 'section-white', 'stats', 'cat-search', 'cat-body-wrap', 'cat-tail')

def kind(cls):
    if 'section-dark' in cls or 'aliya-sec' in cls or 'page-hero' in cls or 'cat-hero' in cls or cls.strip() == 'hero':
        return 'dark'
    return 'light'

for name in ['index.html', 'categories.html', 'cases.html', 'about.html']:
    p = os.path.join(base, name)
    s = io.open(p, encoding='utf-8').read()
    # 清掉已有 seam
    s = re.sub(r'\n[ \t]*<div class="seam seam-(?:to-dark|to-light)"[^>]*></div>', '', s)

    matches = list(re.finditer(r'([ \t]*)<section[^>]*class="([^"]+)"', s))
    inserts = []
    for i in range(1, len(matches)):
        prev_cls, cur_cls = matches[i - 1].group(2), matches[i].group(2)
        if kind(prev_cls) == kind(cur_cls):
            continue
        seam = 'seam-to-dark' if kind(cur_cls) == 'dark' else 'seam-to-light'
        inserts.append((matches[i].start(), matches[i].group(1), seam))

    for pos, indent, seam in reversed(inserts):
        s = s[:pos] + '%s<div class="seam %s" aria-hidden="true"></div>\n' % (indent, seam) + s[pos:]

    io.open(p, 'w', encoding='utf-8').write(s)
    print(name, 'seams', len(inserts))
