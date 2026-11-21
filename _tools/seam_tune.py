# -*- coding: utf-8 -*-
"""微调过渡带：深→浅侧更沉，长度略增（幂等）。"""
import io, os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'index.html')
t = io.open(p, encoding='utf-8').read()

old_h = '.seam{height:116px;position:relative;z-index:2;pointer-events:none;}'
new_h = '.seam{height:132px;position:relative;z-index:2;pointer-events:none;}'
t = t.replace(old_h, new_h)

old_d = '.seam-to-dark{background:linear-gradient(180deg,rgba(9,32,60,0) 0%,rgba(9,32,60,.26) 24%,rgba(9,32,60,.58) 52%,rgba(9,32,60,.85) 78%,#0a2240 100%);}'
new_d = '.seam-to-dark{background:linear-gradient(180deg,rgba(9,32,60,0) 0%,rgba(9,32,60,.14) 18%,rgba(9,32,60,.4) 44%,rgba(9,32,60,.72) 70%,rgba(9,32,60,.93) 88%,#0a2240 100%);}'
t = t.replace(old_d, new_d)

old_l = '.seam-to-light{background:linear-gradient(180deg,#0a2240 0%,rgba(9,32,60,.88) 20%,rgba(9,32,60,.58) 48%,rgba(9,32,60,.24) 76%,rgba(9,32,60,0) 100%);}'
new_l = '.seam-to-light{background:linear-gradient(180deg,#0a2240 0%,rgba(9,32,60,.94) 26%,rgba(9,32,60,.72) 50%,rgba(9,32,60,.4) 72%,rgba(9,32,60,.15) 88%,rgba(9,32,60,0) 100%);}'
t = t.replace(old_l, new_l)

t = t.replace('@media (max-width:900px){.seam{height:88px;}}', '@media (max-width:900px){.seam{height:96px;}}')

io.open(p, 'w', encoding='utf-8').write(t)
print('tuned', new_d in t, new_l in t)
