# -*- coding: utf-8 -*-
import io, os, re

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(base, 'index.html')
t = io.open(src, encoding='utf-8').read()

MARK = '/* ===================== 深浅过渡带 ===================== */'
if MARK in t:
    css_start = t.index(MARK)
else:
    css_start = t.index('/* ===================== 统一排版节奏（移动端） ===================== */')
css_end = t.index('</style>', css_start)
css_block = t[css_start:css_end]

js_start = t.index('<!-- ==== 滚动进场动效 ==== -->')
js_end = t.index('</body>', js_start)
js_block = t[js_start:js_end]

targets = ['categories.html', 'cases.html', 'about.html']
for name in targets:
    p = os.path.join(base, name)
    s = io.open(p, encoding='utf-8').read()
    if MARK in s:
        a = s.index(MARK)
        b = s.index('</style>', a)
        s = s[:a] + css_block + s[b:]
    elif '统一排版节奏' in s:
        a = s.index('/* ===================== 统一排版节奏（移动端） ===================== */')
        b = s.index('</style>', a)
        s = s[:a] + css_block + s[b:]
    else:
        s = s.replace('</style>', css_block + '</style>', 1)
    if '滚动进场动效' in s:
        a = s.index('<!-- ==== 滚动进场动效 ==== -->')
        b = s.index('</body>', a)
        s = s[:a] + js_block + s[b:]
    else:
        s = s.replace('</body>', js_block + '</body>', 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('synced', name, 'css', len(css_block), 'js', len(js_block))
