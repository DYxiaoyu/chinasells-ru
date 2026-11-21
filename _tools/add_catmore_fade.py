# -*- coding: utf-8 -*-
"""给内部深色卡 .cat-more 增加与上下浅色区的渐变衔接（幂等）。"""
import io, os

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(base, 'index.html')
t = io.open(p, encoding='utf-8').read()

add = '''/* 内部深色卡（品类汇总条）与上下浅色区的衔接 */
.cat-more{position:relative;}
.cat-more::before{content:"";position:absolute;left:-1px;right:-1px;bottom:100%;height:40px;
  background:linear-gradient(to bottom,#f6f8fb 0%,#dfe7f1 32%,#86a6c6 66%,#16395c 90%,#0a2544 100%);pointer-events:none;}
.cat-more::after{content:"";position:absolute;left:-1px;right:-1px;top:100%;height:40px;
  background:linear-gradient(to bottom,#0a2544 0%,#16395c 10%,#86a6c6 34%,#dfe7f1 68%,#f6f8fb 100%);pointer-events:none;}
'''

mark = '.seam{height:116px;'
if '内部深色卡' not in t:
    i = t.index(mark)
    t = t[:i] + add + t[i:]

io.open(p, 'w', encoding='utf-8').write(t)
print('cat-more fade ok')
