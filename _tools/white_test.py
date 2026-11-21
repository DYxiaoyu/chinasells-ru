# -*- coding: utf-8 -*-
"""把首页 Aliya / 流程 / 联系三块改白底（试验），独立 style 块，便于一键回退"""
import re, pathlib

p = pathlib.Path(r"C:\Users\Administrator\Doubao\chats\2026-11-17\new-chat-1\chinasells-ru\index.html")
html = p.read_text(encoding="utf-8")

CSTART = "<!--white-test:start-->"
CEND = "<!--white-test:end-->"
# 已有则先移除
html = re.sub(re.escape(CSTART) + r"[\s\S]*?" + re.escape(CEND) + r"\n?", "", html)

CSS = """<!--white-test:start-->
<style id="white-test">
/* 白底试验：Aliya / 流程 / 联系 三块 */
#manager.aliya-sec{color:var(--ink);
 background:radial-gradient(900px 440px at 14% 46%,rgba(215,168,79,.13),rgba(215,168,79,0) 62%),#fff;}
#manager .aliya-kicker{color:var(--gold);}
#manager .aliya-name{color:var(--ink);}
#manager .aliya-role{color:var(--blue);}
#manager .aliya-lead{color:var(--muted);}
#manager .aliya-item h4{color:var(--ink);}
#manager .aliya-item p{color:var(--muted);}
#manager .aliya-tag{position:static;display:inline-block;margin-top:16px;background:rgba(9,32,60,.05);color:var(--ink);}
#manager .aliya-ring{border-color:rgba(9,32,60,.09);}
#manager .aliya-ring-2{border-color:rgba(215,168,79,.18);}
#manager .aliya-photo img{filter:drop-shadow(0 18px 40px rgba(9,32,60,.26));}
#manager .btn-secondary{color:var(--ink);border-color:rgba(9,32,60,.22);background:transparent;}
#manager .btn-secondary:hover{color:var(--blue);border-color:var(--gold);}
#manager .aliya-chip{color:#20334a;border-color:rgba(9,32,60,.18);}
#manager .aliya-chip:hover{color:var(--blue);border-color:var(--gold);background:rgba(215,168,79,.1);}

#process{color:var(--ink);background:#fff;}
#process .section-title{color:var(--ink);}
#process .section-copy{color:var(--muted);}
#process .supplier-panel{background:#f6f8fb;border-color:var(--line);}
#process .process-layout{align-items:stretch;}
#process .supplier-panel{display:flex;flex-direction:column;justify-content:space-between;}
#process .supplier-panel h3{color:var(--blue);}
#process .supplier-row{border-top-color:var(--line);}
#process .supplier-row strong{color:var(--ink);}
#process .supplier-row span{color:var(--muted);}
#process .process-list{background:var(--line);border-color:var(--line);}
#process .process-step{background:#fff;}
#process .process-num{border-right-color:var(--line);color:var(--gold);}
#process .process-text{color:#46556a;}

#contact .contact-band{background:#fff;color:var(--ink);border:1px solid var(--line);}
#contact .contact-band h2{color:var(--ink);}
#contact .contact-band p{color:var(--muted);}
#contact .contact-list{background:var(--line);border-color:var(--line);}
#contact .contact-item{background:#f6f8fb;}
#contact .contact-label{color:var(--gold);}
#contact .contact-value{color:var(--ink);}#contact .contact-value{color:var(--ink);}

#manager.aliya-sec{padding-top:76px;padding-bottom:60px;}
#process{padding-top:72px;padding-bottom:72px;}
#contact{background:#fff;}
@media (max-width:640px){
 #manager.aliya-sec{padding:44px 0;}
 #process{padding:56px 0;}
}
</style>
<!--white-test:end-->
"""

# 插到第一个 </style> 之后
idx = html.find("</style>")
assert idx > 0
pos = idx + len("</style>")
html = html[:pos] + "\n" + CSS + html[pos:]
p.write_text(html, encoding="utf-8")
print("white test block inserted")
