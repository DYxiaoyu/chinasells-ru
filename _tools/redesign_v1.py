# -*- coding: utf-8 -*-
"""首页去模板化改造 v1。只改 index.html；回滚：git checkout pre-redesign-20261121 -- index.html"""
from pathlib import Path
import re

P = Path(r"C:\Users\Administrator\Doubao\chats\2026-11-17\new-chat-1\chinasells-ru\index.html")
html = P.read_text(encoding="utf-8")

# 允许重复执行：先移除上一次注入的新样式，再按 section id 替换内容
html = re.sub(r"\n?<!--redesign-v1:start-->[\s\S]*?<!--redesign-v1:end-->\n?", "\n", html)
html = re.sub(r"\n?<!--white-test:start-->[\s\S]*?<!--white-test:end-->\n?", "\n", html)

def section(name, content):
    global html
    pat = rf'<section\b[^>]*\bid="{re.escape(name)}"[^>]*>[\s\S]*?</section>'
    html, n = re.subn(pat, lambda m: content.strip(), html, count=1)
    if n != 1:
        if n == 0 and not content.strip():
            return  # 已删除的区块：允许脚本重复执行
        raise RuntimeError(f"section {name}: expected 1 replacement, got {n}")

hero = """
<section class="hero redesign-hero" id="hero">
  <div class="container">
    <div class="rd-hero-grid">
      <div class="rd-hero-copy">
        <div class="rd-eyebrow">Закупки в Китае · Наньтун</div>
        <h1>Закупаем в Китае.<br><span>Проверяем до оплаты.</span></h1>
        <p class="rd-hero-lead">Пришлите ссылку, фото или спецификацию. Подберём фабрики, согласуем образцы, проверим партию и организуем поставку на ваш склад или на наш склад в России.</p>
        <div class="rd-actions">
          <a class="rd-btn rd-btn-primary" href="https://hyjj.shop/enquiry" target="_blank" rel="noreferrer">Отправить запрос</a>
          <a class="rd-btn rd-btn-secondary" href="https://wa.me/8619895947232" target="_blank" rel="noreferrer">Обсудить в WhatsApp</a>
        </div>
        <p class="rd-hero-note">Переписку и координацию ведёт Алия. Русский язык · договор · расчёты в рублях.</p>
      </div>
      <figure class="rd-hero-media">
        <img src="img/work/textile-inspection.webp" alt="Демонстрационное изображение: контроль размеров текстильного изделия" width="1400" height="933" decoding="async">
        <figcaption><span>Контроль размеров на фабрике</span><span>Иллюстративное фото</span></figcaption>
      </figure>
    </div>
    <div class="rd-hero-facts" aria-label="Основные этапы">
      <div class="rd-fact"><span>01</span><h3>Сначала образцы</h3><p>Сравниваем фабрики, материалы, комплектацию и условия производства.</p></div>
      <div class="rd-fact"><span>02</span><h3>Потом проверка партии</h3><p>Фото, видео и список замечаний до оплаты и отгрузки. <a href="docs/inspection-report-sample.pdf" target="_blank" rel="noopener">Образец отчёта · PDF</a></p></div>
      <div class="rd-fact"><span>03</span><h3>Затем документы и доставка</h3><p>Договор, сертификаты по товару, таможня и приёмка на складе.</p></div>
    </div>
  </div>
</section>
"""
section("hero", hero)

capability = """
<section class="section section-white rd-proof" id="capability">
  <div class="container">
    <div class="rd-split">
      <div>
        <div class="section-kicker">До подписания договора</div>
        <h2 class="section-title">Сначала проверьте нас и товар</h2>
        <p class="section-copy rd-intro">Не нужно принимать решение по обещаниям на сайте. Запросите реквизиты, согласуйте образец и посмотрите, как оформляется проверка.</p>
        <div class="rd-check-list">
          <article><span>01</span><div><h3>Реквизиты и условия</h3><p>Сторона договора, спецификация, порядок оплаты и ответственность — до подписания.</p></div></article>
          <article><span>02</span><div><h3>Образец и производство</h3><p>Материал, размеры, комплектность и упаковка фиксируются до запуска партии.</p></div></article>
          <article><span>03</span><div><h3>Инспекция и замечания</h3><p>Вы видите не только общие фото, но и дефекты, количество и предложенное действие.</p></div></article>
        </div>
      </div>
      <a class="rd-report-card" href="docs/inspection-report-sample.pdf" target="_blank" rel="noopener" aria-label="Открыть демонстрационный образец отчёта в PDF">
        <img src="docs/inspection-report-preview.webp" alt="Первая страница демонстрационного отчёта об инспекции" width="893" height="1263" loading="lazy" decoding="async">
        <div class="rd-report-caption"><strong>Образец отчёта инспекции</strong><span>PDF · 2 страницы · данные и фото для примера</span><em>Открыть документ ↗</em></div>
      </a>
    </div>
    <p class="rd-legal-note">Для российских компаний доступны договор и расчёты в рублях. Реквизиты стороны договора и пакет документов передаём до подписания.</p>
  </div>
</section>
"""
section("capability", capability)
section("guarantee", "")

cases = """
<section class="section" id="cases">
  <div class="container">
    <div class="section-head">
      <div>
        <div class="section-kicker">Проверка и отгрузка</div>
        <h2 class="section-title">Показываем работу, а не только фабрики</h2>
      </div>
      <p class="section-copy">В процессе вы получаете фото и видео проверок, список замечаний и следующий шаг по каждому вопросу. Фотографии ниже — иллюстрации для макета, которые заменим снимками реальных проверок.</p>
    </div>
    <div class="rd-work-grid">
      <figure><img src="img/work/warehouse.webp" alt="Иллюстративное фото склада и консолидации груза" width="1400" height="933" loading="lazy" decoding="async"><figcaption>Склад и консолидация <span>иллюстрация</span></figcaption></figure>
      <figure><img src="img/work/tools-inspection.webp" alt="Иллюстративное фото проверки электроинструмента" width="1400" height="933" loading="lazy" decoding="async"><figcaption>Проверка электроинструмента <span>иллюстрация</span></figcaption></figure>
      <figure><img src="img/work/packing.webp" alt="Иллюстративное фото подготовки паллет к отгрузке" width="1400" height="933" loading="lazy" decoding="async"><figcaption>Подготовка к отгрузке <span>иллюстрация</span></figcaption></figure>
    </div>

    <div class="rd-orders-head"><h3>Как выглядит карточка заказа</h3><span>Демонстрационные сценарии · не клиентские кейсы</span></div>
    <div class="rd-order-grid">
      <article class="rd-order">
        <div class="rd-order-top"><span>Пример 01</span><strong>Домашний текстиль</strong></div>
        <dl><div><dt>Объём</dt><dd>240 комплектов</dd></div><div><dt>Ориентир по сроку</dt><dd>28–35 дней</dd></div><div><dt>Что проверяем</dt><dd>Размеры, швы, цвет, комплектность и упаковку</dd></div><div><dt>До отгрузки</dt><dd>Отчёт, фото замечаний и подтверждение исправлений</dd></div></dl>
      </article>
      <article class="rd-order">
        <div class="rd-order-top"><span>Пример 02</span><strong>Электроинструмент</strong></div>
        <dl><div><dt>Объём</dt><dd>600 штук</dd></div><div><dt>Ориентир по сроку</dt><dd>30–40 дней</dd></div><div><dt>Что проверяем</dt><dd>Комплектность, АКБ, запуск, маркировку и упаковку</dd></div><div><dt>До отгрузки</dt><dd>Результаты теста и видео по согласованному чек-листу</dd></div></dl>
      </article>
    </div>
    <p class="rd-demo-note">Цифры показывают только формат карточки и не подтверждают выполненные поставки. Здесь будут размещены фактические проекты после согласования с клиентами.</p>
    <div class="rd-text-actions"><a class="text-link" href="cases.html">Производственные партнёры</a><a class="text-link" href="docs/inspection-report-sample.pdf" target="_blank" rel="noopener">Скачать образец отчёта · PDF</a></div>
  </div>
</section>
"""
section("cases", cases)

manager = """
<section class="section rd-manager" id="manager">
  <div class="container">
    <div class="rd-manager-grid">
      <div>
        <div class="section-kicker">Один контакт по заказу</div>
        <h2 class="section-title">Ваш заказ ведёт Алия</h2>
        <p class="rd-manager-role">Заместитель генерального директора</p>
        <p class="section-copy rd-intro">Напишите ей напрямую. Она уточнит задачу, согласует следующий шаг и останется на связи по заказу — без повторного объяснения разным менеджерам.</p>
        <div class="rd-contact-lines">
          <a href="https://wa.me/8619895947232" target="_blank" rel="noreferrer"><span>WhatsApp</span><strong>+86 198 9594 7232</strong></a>
          <a href="https://t.me/aliyachinabiz" target="_blank" rel="noreferrer"><span>Telegram</span><strong>@aliyachinabiz</strong></a>
          <a href="mailto:aliya@chinasells.ru"><span>Email</span><strong>aliya@chinasells.ru</strong></a>
        </div>
      </div>
      <aside class="rd-brief">
        <h3>Что прислать для расчёта</h3>
        <ol><li><span>01</span>Ссылка, фото или описание товара</li><li><span>02</span>Количество и желаемая цена</li><li><span>03</span>Срок и город доставки</li><li><span>04</span>Требования к упаковке и документам</li></ol>
        <p>Если пока есть только фото товара — этого достаточно для первого разговора.</p>
        <a class="rd-btn rd-btn-primary" href="https://hyjj.shop/enquiry" target="_blank" rel="noreferrer">Отправить запрос</a>
      </aside>
    </div>
  </div>
</section>
"""
section("manager", manager)

process = """
<section class="section rd-process" id="process">
  <div class="container">
    <div class="section-head">
      <div><div class="section-kicker">Схема работы</div><h2 class="section-title">Четыре понятных шага</h2></div>
      <p class="section-copy">Перед началом фиксируем состав работ и точки подтверждения. Вы заранее знаете, что согласуем с вами, а что берём на себя.</p>
    </div>
    <ol class="rd-steps">
      <li><span>01</span><h3>Запрос</h3><p>Товар, количество, бюджет, сроки и город доставки.</p></li>
      <li><span>02</span><h3>Фабрика и образец</h3><p>Сравнение предложений, переговоры, образцы и спецификация.</p></li>
      <li><span>03</span><h3>Договор и инспекция</h3><p>Документы, контроль партии, замечания и подтверждение отгрузки.</p></li>
      <li><span>04</span><h3>Доставка и приёмка</h3><p>Таможня, маршрут и доставка на ваш склад или склад в России.</p></li>
    </ol>
  </div>
</section>
"""
section("process", process)

contact = """
<section class="section" id="contact">
  <div class="container">
    <div class="contact-band">
      <div>
        <div class="section-kicker">Контакты</div>
        <h2>Пришлите задачу — начнём с товара и объёма</h2>
        <p>Можно без технического задания. Достаточно ссылки или фото, примерного количества и города доставки. Если товар не подходит для закупки, скажем об этом прямо.</p>
        <div class="hero-actions">
          <a class="rd-btn rd-btn-primary" href="https://hyjj.shop/enquiry" target="_blank" rel="noreferrer">Оставить заявку</a>
          <a class="rd-btn rd-btn-secondary" href="https://wa.me/8619895947232" target="_blank" rel="noreferrer">WhatsApp</a>
          <a class="rd-btn rd-btn-secondary" href="https://t.me/aliyachinabiz" target="_blank" rel="noreferrer">Telegram</a>
        </div>
      </div>
      <div class="contact-list">
        <div class="contact-item"><span class="contact-label">WhatsApp</span><span class="contact-value"><a href="https://wa.me/8619895947232" target="_blank" rel="noreferrer">+86 198 9594 7232</a></span></div>
        <div class="contact-item"><span class="contact-label">Telegram</span><span class="contact-value"><a href="https://t.me/aliyachinabiz" target="_blank" rel="noreferrer">@aliyachinabiz</a></span></div>
        <div class="contact-item"><span class="contact-label">Email</span><span class="contact-value"><a href="mailto:hello@chinasells.ru">hello@chinasells.ru</a></span></div>
        <div class="contact-item"><span class="contact-label">Алия · личный менеджер</span><span class="contact-value"><a href="mailto:aliya@chinasells.ru">aliya@chinasells.ru</a></span></div>
        <div class="contact-item"><span class="contact-label">Адрес</span><span class="contact-value">Международный торговый центр, офис 3606, ул. Чунчуань, д. 88, район Чунчуань, г. Наньтун, провинция Цзянсу, Китай</span></div>
      </div>
    </div>
  </div>
</section>
"""
section("contact", contact)
section("social", "")

html = html.replace('<a href="#capability">Возможности</a>', '<a href="#capability">Документы</a>')
html = html.replace('<a href="#cases">Кейсы</a>', '<a href="#cases">Проверка</a>')
html = html.replace('<title>China Sells — поставки из Китая под ключ | Партнёр для бизнеса</title>', '<title>China Sells — закупки и проверка товара в Китае</title>')
html = html.replace('Работаем по всем направлениям, которые нужны вашему бизнесу — от домашнего текстиля до инструмента, медтехники и стройматериалов. Внутри каждого направления десятки подкатегорий: подбираем фабрику под конкретную позицию, а не «что есть на складе». Ниже — основные направления, но перечень не ограничивает ассортимент.', 'Основные направления — ниже. Если вашего товара нет в списке, пришлите ссылку или фото: подберём фабрику под конкретную позицию, а не предложим случайный складской остаток.')

CSS = r"""
<!--redesign-v1:start-->
<style id="redesign-v1">
/* 首页去模板化 v1：更少的金色、粗标题和卡片，更多工作记录与可检查的信息 */
body{background:#f7f8fa;color:#1c2a38;}
.site-header{background:rgba(255,255,255,.94);border-bottom:1px solid #e2e7ec;backdrop-filter:blur(14px);}
.brand{color:#172a3d}.brand small{color:#7b8793}.brand strong em{color:#8b6a30}
.nav-links a{color:#566575}.nav-links a:hover,.nav-links a.active{color:#173c5c;background:#edf2f5}
.nav-links a.nav-cta,.nav-links a.nav-cta:hover,.nav-links a.nav-cta.active{background:#174d78;color:#fff;box-shadow:none;border-radius:6px;filter:none;transform:none}
.nav-toggle{color:#174d78;border-color:#d7dfe6;background:#fff}

.hero.redesign-hero{min-height:0;padding:136px 0 62px;background:#f7f8fa;color:var(--ink);overflow:visible}
.hero.redesign-hero::after{display:none}
.rd-hero-grid{display:grid;grid-template-columns:minmax(0,1.02fr) minmax(380px,.98fr);gap:66px;align-items:center}
.rd-eyebrow{margin-bottom:20px;color:#6d7b88;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.rd-hero-copy h1{max-width:620px;color:#152638;font-size:54px;line-height:1.08;font-weight:650;letter-spacing:-1.5px}
.rd-hero-copy h1 span{color:#174d78}
.rd-hero-lead{max-width:570px;margin-top:24px;color:#596979;font-size:17px;line-height:1.8}
.rd-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:30px}
.rd-btn{display:inline-flex;align-items:center;justify-content:center;min-height:46px;padding:0 21px;border:1px solid transparent;border-radius:6px;font-size:14px;font-weight:650;line-height:1.2;transition:background .18s,border-color .18s,color .18s}
.rd-btn-primary{background:#174d78;color:#fff}.rd-btn-primary:hover{background:#103e62}
.rd-btn-secondary{border-color:#cbd5de;background:transparent;color:#243b50}.rd-btn-secondary:hover{border-color:#174d78;color:#174d78}
.rd-hero-note{margin-top:18px;color:#7a8793;font-size:12.5px;line-height:1.7}
.rd-hero-media{margin:0}.rd-hero-media img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border:1px solid #dce2e7;border-radius:3px;filter:saturate(.9)}
.rd-hero-media figcaption{display:flex;justify-content:space-between;gap:16px;margin-top:10px;color:#657483;font-size:11px}.rd-hero-media figcaption span:last-child{color:#929ca5}
.rd-hero-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:34px;margin-top:56px;padding-top:25px;border-top:1px solid #dce3e9}
.rd-fact>span{display:block;color:#8b98a3;font-size:11px;font-weight:650}.rd-fact h3{margin-top:8px;color:#213346;font-size:15px;font-weight:650}.rd-fact p{margin-top:7px;color:#6b7885;font-size:13px;line-height:1.7}.rd-fact a{color:#174d78;text-decoration:underline;text-underline-offset:3px}

.section{padding:76px 0}.section-head{display:block;max-width:800px;margin-bottom:32px}
.section-kicker{color:#7b8793;font-size:11px;font-weight:650;letter-spacing:.11em}
.section-title{margin-top:8px;font-size:31px;line-height:1.24;font-weight:650;letter-spacing:-.55px}
.section-copy{font-size:15px;line-height:1.75}.section-head .section-copy{max-width:690px;margin-top:14px}.rd-intro{max-width:650px;margin-top:15px}
.about-home-text .section-copy{font-size:15px;line-height:1.8}.about-metrics{gap:0;border:0;border-top:1px solid var(--line);background:transparent;box-shadow:none}.about-metric{padding:18px 0;border:0;border-bottom:1px solid var(--line);background:transparent}.about-metric strong{color:#1c2a38;font-size:25px;font-weight:650}.about-metric span{color:#6d7b88;font-size:12.5px}

.rd-split{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:78px;align-items:start}
.rd-check-list{margin-top:30px;border-top:1px solid #dce3e9}.rd-check-list article{display:grid;grid-template-columns:34px 1fr;gap:12px;padding:20px 0;border-bottom:1px solid #dce3e9}.rd-check-list article>span{padding-top:2px;color:#94a0aa;font-size:11px;font-weight:650}.rd-check-list h3{font-size:15px;font-weight:650}.rd-check-list p{margin-top:6px;color:#667583;font-size:13.5px;line-height:1.7}
.rd-report-card{display:block;border:1px solid #d8e0e6;background:#f7f8fa}.rd-report-card>img{display:block;width:100%;height:auto;max-height:405px;object-fit:cover;object-position:top;border-bottom:1px solid #d8e0e6}.rd-report-caption{padding:17px 18px 18px}.rd-report-caption strong{display:block;font-size:14px}.rd-report-caption span{display:block;margin-top:5px;color:#74818c;font-size:11.5px;line-height:1.5}.rd-report-caption em{display:block;margin-top:13px;color:#174d78;font-size:12.5px;font-style:normal;font-weight:650}.rd-report-card:hover{border-color:#9eb2c2}
.rd-legal-note{margin-top:34px;padding-top:20px;border-top:1px solid #dce3e9;color:#667583;font-size:13px;line-height:1.75}

.cat-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px;border:0;border-top:1px solid #dce3e9;background:transparent;box-shadow:none}
.cat-card{position:relative;display:block;padding:18px 34px 18px 0;border:0;border-bottom:1px solid #dce3e9;border-radius:0;background:transparent;box-shadow:none}
.cat-card:hover{background:transparent;box-shadow:none;transform:none}.cat-ico{display:none}.cat-card h3{font-size:15.5px;font-weight:650}.cat-card p{margin-top:5px;color:#77838e;font-size:12.5px}.cat-arrow{position:absolute;right:2px;top:21px;color:#8a98a4;font-size:16px}.cat-card:hover h3,.cat-card:hover .cat-arrow{color:#174d78}
.cat-omitted{margin-top:26px;padding:0;border:0;background:transparent;box-shadow:none}.cat-omitted-plus{display:none}.cat-omitted p{font-size:13.5px;line-height:1.75}.cat-omitted-note{font-size:12.5px}.cat-omitted-link,.cat-omitted-link:hover{min-height:0;padding:0;border:0;background:transparent;box-shadow:none;color:#174d78;font-size:13px;transform:none}.cat-omitted-link::after,.cat-omitted-link:hover::after{color:#174d78;transform:none}
.cat-more{margin-top:28px;padding:24px 0 0;border:0;border-top:1px solid #dce3e9;background:transparent;box-shadow:none;color:#1c2a38}.cat-more p{color:#1c2a38;font-size:15px;font-weight:650}.cat-more span{display:none}.cat-more .btn{min-height:42px;border:1px solid #cbd5de;border-radius:6px;background:transparent;color:#174d78;box-shadow:none;font-size:13px}

.rd-work-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.rd-work-grid figure{margin:0}.rd-work-grid img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:2px;filter:saturate(.88)}.rd-work-grid figcaption{display:flex;justify-content:space-between;gap:8px;margin-top:9px;color:#4e6171;font-size:11.5px}.rd-work-grid figcaption span{color:#98a1a9;font-size:10px}
.rd-orders-head{display:flex;align-items:baseline;justify-content:space-between;gap:24px;margin-top:44px;padding-top:26px;border-top:1px solid #dce3e9}.rd-orders-head h3{font-size:18px;font-weight:650}.rd-orders-head>span{color:#8a959e;font-size:11.5px}
.rd-order-grid{display:grid;grid-template-columns:1fr 1fr;gap:42px;margin-top:22px}.rd-order-top{display:flex;align-items:center;gap:14px;padding-bottom:13px;border-bottom:2px solid #29465f}.rd-order-top span{color:#8a969f;font-size:11px;text-transform:uppercase}.rd-order-top strong{font-size:17px;font-weight:650}.rd-order dl>div{display:grid;grid-template-columns:140px 1fr;gap:16px;padding:11px 0;border-bottom:1px solid #e1e6eb}.rd-order dt{color:#7b8791;font-size:12px}.rd-order dd{margin:0;color:#35495a;font-size:13px;line-height:1.55}
.rd-demo-note{max-width:840px;margin-top:20px;color:#8a7570;font-size:11.5px;line-height:1.65}.rd-text-actions{display:flex;flex-wrap:wrap;gap:26px;margin-top:24px}.text-link,.about-home-text .text-link{color:#174d78;font-size:13px}.text-link::after{color:#174d78}

.rd-manager{background:#fff}.rd-manager-grid{display:grid;grid-template-columns:minmax(0,1fr) 390px;gap:90px;align-items:start}.rd-manager-role{margin-top:9px;color:#174d78;font-size:13.5px;font-weight:650}.rd-contact-lines{max-width:520px;margin-top:26px;border-top:1px solid #dce3e9}.rd-contact-lines a{display:grid;grid-template-columns:100px 1fr;gap:20px;padding:14px 0;border-bottom:1px solid #dce3e9}.rd-contact-lines span{color:#7c8994;font-size:12px}.rd-contact-lines strong{font-size:14px;font-weight:600}.rd-contact-lines a:hover strong{color:#174d78}
.rd-brief{padding:26px 28px;border-left:2px solid #174d78;background:#f4f6f8}.rd-brief h3{font-size:17px;font-weight:650}.rd-brief ol{margin-top:17px;list-style:none}.rd-brief li{display:grid;grid-template-columns:28px 1fr;gap:9px;padding:9px 0;color:#3e5263;font-size:13px}.rd-brief li span{color:#94a0aa;font-size:10px}.rd-brief p{margin-top:16px;color:#73808b;font-size:12px;line-height:1.65}.rd-brief .rd-btn{margin-top:20px;width:100%}
.rd-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;margin:0;padding:0;border-top:1px solid #d9e1e7;list-style:none}.rd-steps li{padding:23px 24px 10px 0}.rd-steps li+li{padding-left:24px;border-left:1px solid #d9e1e7}.rd-steps li>span{color:#8c98a2;font-size:11px;font-weight:650}.rd-steps h3{margin-top:12px;font-size:16px;font-weight:650}.rd-steps p{margin-top:8px;color:#697784;font-size:13px;line-height:1.7}

#contact{background:#fff}#contact .section-kicker{color:#7b8793}#contact .contact-band{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:70px;padding:42px 0;border:0;border-top:1px solid #dce3e9;border-bottom:1px solid #dce3e9;background:transparent;color:#1c2a38;box-shadow:none}#contact .contact-band h2{max-width:620px;margin-top:10px;font-size:30px;line-height:1.25;font-weight:650;letter-spacing:-.45px}#contact .contact-band p{max-width:610px;margin-top:17px;color:#657482;font-size:14px;line-height:1.8}#contact .hero-actions{margin-top:26px}#contact .contact-list{display:block;border:0;background:transparent}#contact .contact-item{padding:12px 0;border-bottom:1px solid #e0e6eb;background:transparent}#contact .contact-item:first-child{padding-top:0}#contact .contact-label{color:#89949e;font-size:10px;font-weight:650}#contact .contact-value{margin-top:3px;color:#24394b;font-size:13px;line-height:1.55}
.footer{padding:23px 0}.footer-inner{font-size:11px}

@media(max-width:1180px){
 .nav-links{background:#fff;border-color:#dce3e9;box-shadow:0 18px 40px rgba(20,40,60,.12)}.nav-links a{color:#465a6c}.nav-links a:hover,.nav-links a.active{color:#174d78;background:#edf2f5}
 .rd-hero-grid{gap:38px}.rd-hero-copy h1{font-size:45px}.rd-split{gap:44px}.rd-manager-grid{gap:48px}
}
@media(max-width:900px){
 .hero.redesign-hero{padding:116px 0 50px}.rd-hero-grid{grid-template-columns:1fr;gap:34px}.rd-hero-copy h1{max-width:680px;font-size:43px}.rd-hero-lead{max-width:650px}.rd-hero-media{max-width:680px}
 .rd-split,.rd-manager-grid{grid-template-columns:1fr;gap:38px}.rd-report-card{max-width:430px}.rd-report-card>img{max-height:none}
 .rd-work-grid{grid-template-columns:1fr 1fr}.rd-work-grid figure:last-child{grid-column:1/-1;max-width:calc(50% - 9px)}
 .rd-order-grid{gap:28px}.rd-order dl>div{grid-template-columns:120px 1fr}.rd-steps{grid-template-columns:1fr 1fr}.rd-steps li:nth-child(3){border-left:0;padding-left:0}.rd-steps li{padding-bottom:22px;border-bottom:1px solid #d9e1e7}
 #contact .contact-band{grid-template-columns:1fr;gap:34px}
}
@media(max-width:640px){
 .hero.redesign-hero{padding:104px 0 42px}.rd-hero-copy h1{font-size:36px;line-height:1.1;letter-spacing:-.8px}.rd-hero-lead{margin-top:19px;font-size:15px;line-height:1.75}.rd-actions{margin-top:24px}.rd-actions .rd-btn{width:100%}.rd-hero-note{font-size:11.5px}.rd-hero-media figcaption{font-size:10px}
 .rd-hero-facts{grid-template-columns:1fr;gap:18px;margin-top:34px;padding-top:20px}.rd-fact{display:grid;grid-template-columns:26px 1fr;gap:0 8px}.rd-fact>span{grid-row:1/3}.rd-fact h3{margin-top:0}.rd-fact p{margin-top:4px}
 .section{padding:54px 0}.section-title{font-size:26px;line-height:1.25;letter-spacing:-.35px}.section-copy{font-size:14px}.section-head{margin-bottom:25px}
 .cat-grid{grid-template-columns:1fr}.cat-card{padding-top:16px;padding-bottom:16px}.cat-omitted{display:block}.cat-omitted-link{display:inline-block;margin-top:12px}.cat-more{display:block}.cat-more .btn{margin-top:15px;width:100%}
 .rd-check-list article{padding:17px 0}.rd-report-card{max-width:100%}.rd-legal-note{margin-top:26px}
 .rd-work-grid{grid-template-columns:1fr;gap:24px}.rd-work-grid figure:last-child{grid-column:auto;max-width:none}.rd-orders-head{display:block;margin-top:34px}.rd-orders-head>span{display:block;margin-top:6px}.rd-order-grid{grid-template-columns:1fr;gap:30px}.rd-order dl>div{grid-template-columns:110px 1fr;gap:12px}.rd-demo-note{font-size:11px}
 .rd-contact-lines a{grid-template-columns:82px 1fr;gap:12px}.rd-brief{padding:22px 20px}.rd-steps{grid-template-columns:1fr}.rd-steps li,.rd-steps li+li,.rd-steps li:nth-child(3){padding:18px 0;border-left:0;border-bottom:1px solid #d9e1e7}.rd-steps li:last-child{border-bottom:0}
 #contact .contact-band{padding:30px 0;gap:28px}#contact .contact-band h2{font-size:26px}#contact .hero-actions .rd-btn{width:100%}.footer-inner{gap:8px}
}
</style>
<!--redesign-v1:end-->
"""

# 放在原样式之后、</head> 之前；不影响其他三个页面
html = html.replace("</head>", CSS + "\n</head>", 1)
P.write_text(html, encoding="utf-8")
print("redesign v1 written; sections:", len(re.findall(r"<section\b", html)))
