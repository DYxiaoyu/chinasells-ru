# -*- coding: utf-8 -*-
from pathlib import Path
import re
p = Path(r"C:\Users\Administrator\Doubao\chats\2026-11-17\new-chat-1\chinasells-ru\index.html")
h = p.read_text(encoding="utf-8")
refs = re.findall(r'(?:src|href)="([^"]+)"', h)
missing = []
for x in refs:
    if re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:)", x):
        continue
    if not (p.parent / x.split("#")[0]).exists():
        missing.append(x)
ids = re.findall(r'\bid="([^"]+)"', h)
print("missing local refs:", missing)
print("duplicate ids:", sorted({x for x in ids if ids.count(x) > 1}))
print("sections:", re.findall(r'<section[^>]+id="([^"]+)"', h))
