/* China Sells — site 2026 interactions */
(function () {
  'use strict';

  var STORE_KEY = 'chinasells_inquiry_v1';
  var WA_PHONE = '8619895947232';

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function track(name, params) {
    try { if (typeof window.gtag === 'function') window.gtag('event', name, params || {}); } catch (e) {}
  }

  /* ---------- mobile menu ---------- */
  var burger = $('.ix-burger');
  var mobile = $('#mobileMenu');
  if (burger && mobile) {
    burger.addEventListener('click', function () {
      var open = mobile.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
      burger.textContent = open ? '✕' : '☰';
    });
    $all('a', mobile).forEach(function (a) {
      a.addEventListener('click', function () {
        mobile.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
        burger.textContent = '☰';
      });
    });
  }

  /* ---------- toast ---------- */
  var toastEl = $('#toast');
  var toastTimer = null;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2600);
  }

  /* ---------- inquiry basket ---------- */
  function readStore() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr.filter(function (x) { return x && x.id && x.title; }) : [];
    } catch (e) { return []; }
  }
  function writeStore(items) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(items)); } catch (e) {}
  }
  function inquiryMessage(items) {
    return 'Здравствуйте, Алия! Интересует закупка из Китая по направлениям:\n' +
      items.map(function (it, i) { return (i + 1) + '. ' + it.title + (it.cat ? ' (' + it.cat + ')' : ''); }).join('\n') +
      '\n\nПодскажите, пожалуйста, MOQ, срок и цену. Готов(а) уточнить детали.';
  }
  function renderInquiry() {
    var items = readStore();
    var countEl = $('#inquiryCount');
    var titlesEl = $('#inquiryTitles');
    var thumbsEl = $('#inquiryThumbs');
    var bar = $('#inquiryBar');
    if (countEl) countEl.textContent = String(items.length);
    if (titlesEl) {
      titlesEl.textContent = items.length
        ? items.map(function (it) { return it.title; }).join(' · ')
        : 'Выберите карточки каталога';
    }
    if (thumbsEl) {
      thumbsEl.innerHTML = items.slice(0, 4).map(function (it) {
        return it.img ? '<img src="' + it.img.replace(/"/g, '&quot;') + '" alt="">' : '';
      }).join('');
    }
    if (bar) bar.classList.toggle('show', items.length > 0);

    /* sync add buttons */
    $all('[data-add]').forEach(function (btn) {
      var id = btn.getAttribute('data-id');
      var inQ = items.some(function (it) { return it.id === id; });
      btn.classList.toggle('on', inQ);
      btn.setAttribute('aria-pressed', inQ ? 'true' : 'false');
      if (btn.classList.contains('ix-add')) {
        btn.textContent = inQ ? '✓ В запросе' : '+ В запрос';
      } else {
        btn.textContent = inQ ? '✓' : '+';
      }
    });
  }
  function addItem(btn) {
    var id = btn.getAttribute('data-id');
    if (!id) return;
    var items = readStore();
    if (items.some(function (it) { return it.id === id; })) {
      toast('Уже в запросе');
      return;
    }
    items.push({
      id: id,
      title: btn.getAttribute('data-title') || id,
      cat: btn.getAttribute('data-cat') || '',
      img: btn.getAttribute('data-img') || ''
    });
    writeStore(items);
    renderInquiry();
    toast('Добавлено в запрос');
    track('add_to_inquiry', { item_id: id, item_name: btn.getAttribute('data-title') || id });
  }
  $all('[data-add]').forEach(function (btn) {
    btn.addEventListener('click', function () { addItem(btn); });
  });

  var clearBtn = $('#inquiryClear');
  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      writeStore([]);
      renderInquiry();
      toast('Запрос очищен');
    });
  }

  var sendBtn = $('#inquirySend');
  if (sendBtn) {
    sendBtn.addEventListener('click', function () {
      var items = readStore();
      if (!items.length) { toast('Сначала выберите направления'); return; }
      var text = inquiryMessage(items);
      track('inquiry_send', { items: items.map(function (it) { return it.id; }).join(',') });
      window.open('https://wa.me/' + WA_PHONE + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
    });
  }

  renderInquiry();

  /* ---------- home catalog rail ---------- */
  var rail = $('#catalogRail');
  var prev = $('[data-rail-prev]');
  var next = $('[data-rail-next]');
  function scrollRail(dir) {
    if (!rail) return;
    var card = rail.querySelector('.ix-pcard');
    var step = card ? card.getBoundingClientRect().width + 16 : 300;
    rail.scrollBy({ left: dir * step * 2, behavior: 'smooth' });
  }
  if (prev) prev.addEventListener('click', function () { scrollRail(-1); });
  if (next) next.addEventListener('click', function () { scrollRail(1); });

  /* ---------- catalog filters ---------- */
  var grid = $('#catalogGrid');
  if (grid) {
    var cards = $all('.ix-grid-card', grid);
    var filters = $all('.ix-filter');
    var search = $('#catSearch');
    var empty = $('#emptyState');
    var activeFilter = 'all';

    function normalize(s) {
      return (s || '').toLowerCase().replace(/ё/g, 'е').replace(/[‐‑‎]/g, '-');
    }
    function apply() {
      var q = normalize(search ? search.value.trim() : '');
      var visible = 0;
      cards.forEach(function (card) {
        var cat = card.getAttribute('data-cat') || '';
        var hay = normalize(card.getAttribute('data-search') + ' ' + card.textContent);
        var ok = (activeFilter === 'all' || cat === activeFilter) && (!q || hay.indexOf(q) !== -1);
        card.hidden = !ok;
        if (ok) visible++;
      });
      if (empty) empty.hidden = visible > 0;
    }
    filters.forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeFilter = btn.getAttribute('data-filter') || 'all';
        filters.forEach(function (b) { b.classList.toggle('on', b === btn); });
        apply();
        track('catalog_filter', { filter: activeFilter });
      });
    });
    if (search) {
      search.addEventListener('input', apply);
      search.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { search.value = ''; apply(); }
      });
    }
    var params = new URLSearchParams(window.location.search);
    var initial = params.get('cat');
    if (initial) {
      var found = filters.filter(function (b) { return b.getAttribute('data-filter') === initial; })[0];
      if (found) {
        activeFilter = initial;
        filters.forEach(function (b) { b.classList.toggle('on', b === found); });
      }
    }
    apply();

    var filterToggle = $('#filterToggle');
    var panel = $('#filterPanel');
    if (filterToggle && panel) {
      filterToggle.addEventListener('click', function () {
        var open = panel.classList.toggle('open');
        filterToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
  }

  /* ---------- brief form ---------- */
  var form = $('#briefForm');
  if (form) {
    var fProduct = $('#briefProduct');
    var fQty = $('#briefQty');
    var fBudget = $('#briefBudget');
    var fDeadline = $('#briefDeadline');
    var fContact = $('#briefContact');
    var preview = $('#briefPreview');
    var copyBtn = $('#briefCopy');
    var waBtn = $('#briefWhatsApp');
    var FORM_URL = 'https://hyjj.shop/quote';

    function val(el, fallback) {
      var v = el && el.value ? el.value.trim() : '';
      return v || fallback || '';
    }
    function buildText() {
      var lines = [];
      lines.push('Заявка с сайта China Sells');
      lines.push('Что ищем: ' + val(fProduct, '—'));
      lines.push('Количество: ' + val(fQty, '—'));
      lines.push('Бюджет на единицу: ' + val(fBudget, 'обсудим'));
      lines.push('Срок: ' + val(fDeadline, 'обсудим'));
      lines.push('Контакт: ' + val(fContact, 'уточним в переписке'));
      return lines.join('\n');
    }
    function updatePreview() {
      if (!preview) return;
      var has = fProduct && fProduct.value.trim();
      preview.textContent = has ? buildText() : 'Заполните продукт и количество — здесь появится готовый текст.';
    }
    [fProduct, fQty, fBudget, fDeadline, fContact].forEach(function (el) {
      if (el) el.addEventListener('input', updatePreview);
    });
    updatePreview();

    function copyText(text) {
      if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
      }
      return new Promise(function (resolve, reject) {
        try {
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          resolve();
        } catch (e) { reject(e); }
      });
    }
    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        copyText(buildText()).then(function () { toast('Текст заявки скопирован'); })
          .catch(function () { toast('Не удалось скопировать — выделите текст вручную'); });
      });
    }

    function needsBrief() {
      var product = fProduct ? fProduct.value.trim() : '';
      var qty = fQty ? fQty.value.trim() : '';
      if (!product || !qty) {
        toast('Заполните продукт и количество');
        if (!product && fProduct) fProduct.focus();
        else if (!qty && fQty) fQty.focus();
        return false;
      }
      return true;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!needsBrief()) return;
      var text = buildText();
      var product = fProduct.value.trim();
      track('generate_lead', { channel: 'form', product: product });
      var params = new URLSearchParams({
        product: product,
        qty: val(fQty),
        budget: val(fBudget),
        deadline: val(fDeadline),
        contact: val(fContact),
        source: 'website_home_form'
      });
      var win = window.open(FORM_URL + '?' + params.toString(), '_blank');
      if (win) win.opener = null;
      copyText(text).then(function () {
        toast('Форма открыта. Поля подставятся автоматически; текст заявки скопирован.');
      }).catch(function () {
        toast('Форма открыта. Текст заявки — в предпросмотре ниже.');
      });
      if (!win) toast('Разрешите всплывающие окна или откройте hyjj.shop/quote');
    });

    if (waBtn) {
      waBtn.addEventListener('click', function () {
        if (!needsBrief()) return;
        var text = buildText();
        track('generate_lead', { channel: 'whatsapp', product: fProduct.value.trim() });
        window.open('https://wa.me/' + WA_PHONE + '?text=' + encodeURIComponent(text), '_blank', 'noopener');
      });
    }
  }
})();
