# -*- coding: utf-8 -*-
"""用桌面新素材 aliya.png（真透明底 + 底部自然渐隐）重做 hero 人物图。"""
import io, os
from PIL import Image

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = r'C:\Users\Administrator\Desktop\aliya.png'
im = Image.open(src).convert('RGBA')
print('src', im.size)

# 裁掉四周全透明边缘，保留少量留白
bbox = im.split()[-1].getbbox()
print('alpha bbox', bbox)
im = im.crop(bbox)

out1 = im.resize((int(im.width * 0.98), int(im.height * 0.98)), Image.LANCZOS)
p1 = os.path.join(base, 'img', 'aliya-hero.webp')
out1.save(p1, 'WEBP', quality=90, method=6)
p2 = os.path.join(base, 'img', 'aliya-hero@2x.webp')
im.save(p2, 'WEBP', quality=90, method=6)
for p in (p1, p2):
    print(p, Image.open(p).size, round(os.path.getsize(p) / 1024, 1), 'KB')
