# -*- coding: utf-8 -*-
"""重写衔接样式：改为「透明→深色」叠层渐变，并补上页脚、汇总条过渡（幂等）。"""
import io, os, re

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'index.html')
t = io.open(p, encoding='utf-8').read()

NEW = '''/* ===================== 深浅过渡带 ===================== */
.seam{height:116px;position:relative;z-index:2;pointer-events:none;}
.seam-to-dark{background:linear-gradient(180deg,rgba(9,32,60,0) 0%,rgba(9,32,60,.26) 24%,rgba(9,32,60,.58) 52%,rgba(9,32,60,.85) 78%,#0a2240 100%);}
.seam-to-light{background:linear-gradient(180deg,#0a2240 0%,rgba(9,32,60,.88) 20%,rgba(9,32,60,.58) 48%,rgba(9,32,60,.24) 76%,rgba(9,32,60,0) 100%);}
@media (max-width:900px){.seam{height:88px;}}
/* 内部深色卡（品类汇总条）与上下浅色区的衔接 */
.cat-more{position:relative;}
.cat-more::before{content:"";position:absolute;left:-1px;right:-1px;bottom:100%;height:44px;
  background:linear-gradient(180deg,rgba(9,32,60,0) 0%,rgba(9,32,60,.5) 55%,#0a2240 100%);pointer-events:none;}
.cat-more::after{content:"";position:absolute;left:-1px;right:-1px;top:100%;height:44px;
  background:linear-gradient(180deg,#0a2240 0%,rgba(9,32,60,.5) 45%,rgba(9,32,60,0) 100%);pointer-events:none;}
/* 页脚深色与上方浅色区的衔接 */
.footer{position:relative;}
.footer::before{content:"";position:absolute;left:0;right:0;bottom:100%;height:76px;pointer-events:none;
  background:linear-gradient(180deg,rgba(5,13,24,0) 0%,rgba(5,13,24,.4) 38%,rgba(5,13,24,.78) 70%,#050d18 100%);}
'''

start = t.index('/* ===================== 深浅过渡带 ===================== */')
end_marker = '@media (max-width:900px){.seam{height:88px;}}'
end = t.index(end_marker, start) + len(end_marker)
t = t[:start] + NEW.rstrip('\n') + t[end:]
io.open(p, 'w', encoding='utf-8').write(t)
print('rewritten', start, end)
