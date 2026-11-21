# -*- coding: utf-8 -*-
"""生成明确标注为演示样本的俄文验货报告 PDF（非真实成交/验收记录）"""
from pathlib import Path
from io import BytesIO
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

ROOT = Path(r"C:\Users\Administrator\Doubao\chats\2026-11-17\new-chat-1\chinasells-ru")
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)
PDF = OUT / "inspection-report-sample.pdf"

pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")

INK = colors.HexColor("#172638")
MUTED = colors.HexColor("#637184")
LINE = colors.HexColor("#d9e0e7")
PALE = colors.HexColor("#f4f6f8")
BLUE = colors.HexColor("#174d78")
RED = colors.HexColor("#a33b35")

styles = {
    "small": ParagraphStyle("small", fontName="Arial", fontSize=7.8, leading=11, textColor=MUTED),
    "label": ParagraphStyle("label", fontName="Arial-Bold", fontSize=8.2, leading=11, textColor=MUTED),
    "body": ParagraphStyle("body", fontName="Arial", fontSize=9.2, leading=13.5, textColor=INK),
    "bodyb": ParagraphStyle("bodyb", fontName="Arial-Bold", fontSize=9.2, leading=13.5, textColor=INK),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=19, leading=23, textColor=INK, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=11.5, leading=15, textColor=INK, spaceBefore=8, spaceAfter=6),
    "note": ParagraphStyle("note", fontName="Arial", fontSize=8, leading=11.5, textColor=RED),
    "caption": ParagraphStyle("caption", fontName="Arial", fontSize=8.2, leading=11, textColor=MUTED),
}

def P(text, style="body"):
    return Paragraph(text, styles[style])

def JImage(path, width, height):
    """以 JPEG 嵌入，避免 PNG/WebP 解码成超大无损位图"""
    im = PILImage.open(path).convert("RGB")
    im.thumbnail((1100, 800))
    buf = BytesIO()
    im.save(buf, "JPEG", quality=78, optimize=True)
    buf.seek(0)
    return Image(buf, width=width, height=height)

def footer_watermark(c, doc):
    w, h = A4
    c.saveState()
    c.setFillColor(colors.Color(0.64, 0.23, 0.21, alpha=0.09))
    c.setFont("Arial-Bold", 48)
    c.translate(w/2, h/2)
    c.rotate(34)
    c.drawCentredString(0, 0, "ОБРАЗЕЦ / ДЕМО")
    c.restoreState()
    c.saveState()
    c.setStrokeColor(LINE)
    c.line(18*mm, 14*mm, w-18*mm, 14*mm)
    c.setFont("Arial", 7.4)
    c.setFillColor(MUTED)
    c.drawString(18*mm, 9.5*mm, "Демонстрационный макет отчёта · не является документом о выполненной поставке")
    c.drawRightString(w-18*mm, 9.5*mm, f"{doc.page} / 2")
    c.restoreState()

doc = SimpleDocTemplate(str(PDF), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm,
                        topMargin=16*mm, bottomMargin=19*mm,
                        title="Образец отчёта об инспекции — ДЕМО",
                        author="China Sells — демонстрационный макет")
story = []

head = Table([[P("CHINA SELLS / КОНТРОЛЬ КАЧЕСТВА", "bodyb"), P("ОБРАЗЕЦ · НЕ ОТЧЁТ ПО РЕАЛЬНОЙ ПОСТАВКЕ", "note")]],
             colWidths=[100*mm, 74*mm])
head.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("ALIGN", (1,0), (1,0), "RIGHT"),
                          ("LINEBELOW", (0,0), (-1,-1), 0.8, BLUE), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
story += [head, Spacer(1, 7*mm), P("Отчёт об инспекции партии", "h1"),
          P("Пример того, какие данные и фотографии вы получаете до оплаты и отгрузки.", "body"), Spacer(1, 4*mm)]

info = [
    [P("Номер документа", "label"), P("DEMO-QC-014 · демонстрационный номер", "body"),
     P("Дата", "label"), P("ДД.ММ.ГГГГ", "body")],
    [P("Заказчик", "label"), P("ООО «[СКРЫТО]»", "body"),
     P("Тип инспекции", "label"), P("Выборочная, до отгрузки", "body")],
    [P("Товар", "label"), P("Постельное бельё · 240 компл. · пример", "body"),
     P("Поставщик", "label"), P("Фабрика № 2 · данные скрыты", "body")],
    [P("Выборка", "label"), P("80 упаковок · пример расчёта", "body"),
     P("Критерий", "label"), P("AQL 2.5 / 4.0 · пример", "body")],
]
t = Table(info, colWidths=[28*mm, 65*mm, 26*mm, 55*mm])
t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("BACKGROUND", (0,0), (-1,-1), PALE),
                       ("GRID", (0,0), (-1,-1), 0.45, colors.white),
                       ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
                       ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)]))
story += [t, Spacer(1, 4*mm), P("1. Что проверялось", "h2")]

checks = [
    [P("Пункт", "label"), P("Метод", "label"), P("Результат · пример", "label"), P("Комментарий · пример", "label")],
    [P("Размеры"), P("Сантиметровая лента"), P("Соответствует"), P("Допуск по спецификации")],
    [P("Швы и строчка"), P("Визуально + растяжение"), P("2 minor"), P("Отдельные концы ниток")],
    [P("Цвет и ткань"), P("Сравнение с образцом"), P("Соответствует"), P("Проверка при дневном свете")],
    [P("Комплектность"), P("Пересчёт по упаковкам"), P("Соответствует"), P("Простынь / пододеяльник / наволочки")],
    [P("Упаковка"), P("Визуально + пересчёт"), P("1 minor"), P("Заменён один пакет")],
]
ct = Table(checks, colWidths=[34*mm, 48*mm, 37*mm, 55*mm], repeatRows=1)
ct.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("BACKGROUND", (0,0), (-1,0), PALE),
                        ("LINEBELOW", (0,0), (-1,-1), 0.45, LINE),
                        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
                        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
story += [ct, Spacer(1, 4*mm)]

result = Table([[P("ИТОГ · ПРИМЕР", "label"), P("0 critical / 0 major / 3 minor. Пример условия: замечания устраняются и подтверждаются фото до отгрузки.", "body")]],
               colWidths=[36*mm, 138*mm])
result.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 0.7, BLUE), ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f2f7fa")),
                            ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 8),
                            ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
story += [result, Spacer(1, 4*mm), P("2. Замечания и следующий шаг", "h2"),
          P("В реальном отчёте здесь перечисляются конкретные дефекты, количество единиц, номера коробок и требуемое действие. Заказчик получает список замечаний и подтверждает: исправить, заменить, согласовать скидку или остановить отгрузку.", "body"),
          Spacer(1, 3*mm), P("Все числа на этой странице заполнены для демонстрации формата.", "note"),
          PageBreak()]

story += [P("Фотографии инспекции", "h1"),
          P("Пример размещения фотографий. Изображения сгенерированы для макета и не являются съёмкой реальной партии.", "note"), Spacer(1, 4*mm)]

img1 = JImage(ROOT / "img/work/textile-inspection.webp", width=150*mm, height=100*mm)
story += [img1, Spacer(1, 2*mm), P("Фото 01 · Контроль размера изделия · демонстрационное изображение", "caption"), Spacer(1, 5*mm)]

row = Table([[JImage(ROOT / "img/work/packing.webp", width=72*mm, height=48*mm),
              JImage(ROOT / "img/work/warehouse.webp", width=72*mm, height=48*mm)]], colWidths=[75*mm, 75*mm])
row.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0),
                         ("RIGHTPADDING", (0,0), (-1,-1), 3)]))
story += [row, Spacer(1, 2*mm), P("Фото 02–03 · Упаковка и склад · демонстрационные изображения", "caption"), Spacer(1, 5*mm),
          P("3. Что прикладывается к реальному отчёту", "h2"),
          P("• общий вид партии и коробок;<br/>• проверка размеров, внешнего вида и комплектности;<br/>• крупные фотографии каждого дефекта;<br/>• видео тестов, если они предусмотрены для товара;<br/>• итоговое количество critical / major / minor;<br/>• подтверждение исправлений до отгрузки.", "small"),
          Spacer(1, 5*mm),
          P("ВАЖНО: этот файл — образец структуры отчёта. Заказ, значения, выводы и изображения демонстрационные. Он не подтверждает инспекцию, оплату или поставку реального товара.", "note")]

doc.build(story, onFirstPage=footer_watermark, onLaterPages=footer_watermark)
print(PDF)
