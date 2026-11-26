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

  /* ---------- brief form: native lead submit ---------- */
  var form = $('#briefForm');
  if (form) {
    var FORM_URL = 'https://hyjj.shop/quote';
    var API_URL = 'https://hyjj.shop/api/lead';
    var NATIVE_LEAD_FORM = true;
    var SOURCE_RE = /^[a-z0-9_]{1,50}$/;
    var source = 'website_home_form';
    var qs = new URLSearchParams(window.location.search);
    var qsSource = (qs.get('source') || '').trim();
    if (qsSource && SOURCE_RE.test(qsSource)) source = qsSource;

    var fName = $('#briefName');
    var fPhone = $('#briefPhone');
    var fProduct = $('#briefProduct');
    var fQty = $('#briefQty');
    var fBudget = $('#briefBudget');
    var fDeadline = $('#briefDeadline');
    var fTelegram = $('#briefTelegram');
    var fWhatsapp = $('#briefWhatsapp');
    var fEmail = $('#briefEmail');
    var fCompany = $('#briefCompany');
    var fAddress = $('#briefAddress');
    var fRequirement = $('#briefRequirement');
    var fHp = $('#briefHp');
    var body = $('#briefBody');
    var success = $('#briefSuccess');
    var againBtn = $('#briefAgain');
    var submitBtn = $('#briefSubmit');
    var errorBox = $('#briefFormError');
    var fallback = $('#briefFallback');
    var fallbackLink = fallback ? fallback.querySelector('a') : null;

    ['product', 'qty', 'budget', 'deadline'].forEach(function (key) {
      var el = { product: fProduct, qty: fQty, budget: fBudget, deadline: fDeadline }[key];
      var v = qs.get(key);
      if (el && v) el.value = v.slice(0, 240);
    });

    function val(el) {
      return el && el.value ? el.value.trim() : '';
    }

    function fieldOf(el) {
      return el ? el.closest('.ix-field') : null;
    }

    function setErr(el, errEl, msg) {
      var field = fieldOf(el);
      if (field) field.classList.add('invalid');
      if (el) el.setAttribute('aria-invalid', 'true');
      if (errEl) errEl.textContent = msg;
    }

    function clearErr(el, errEl) {
      var field = fieldOf(el);
      if (field) field.classList.remove('invalid');
      if (el) el.removeAttribute('aria-invalid');
      if (errEl) errEl.textContent = '';
    }

    function clearAllErrors() {
      [[fName, '#briefNameErr'], [fPhone, '#briefPhoneErr'],
        [fRequirement, '#briefRequirementErr']].forEach(function (pair) {
        clearErr(pair[0], pair[0] ? $(pair[1]) : null);
      });
      if (errorBox) { errorBox.hidden = true; errorBox.textContent = ''; }
      if (fallback) fallback.hidden = true;
    }

    function validate() {
      var first = null;
      function required(el, errEl, msg) {
        if (!val(el)) {
          setErr(el, errEl, msg);
          if (!first) first = el;
          return false;
        }
        clearErr(el, errEl);
        return true;
      }

      var okName = required(fName, $('#briefNameErr'), 'Укажите имя');
      var phone = val(fPhone).replace(/\s/g, '');
      var okPhone = /^\+?[0-9\s\-]{7,20}$/.test(phone);
      if (!okPhone) {
        setErr(fPhone, $('#briefPhoneErr'), 'Укажите корректный телефон');
        if (!first) first = fPhone;
      } else {
        clearErr(fPhone, $('#briefPhoneErr'));
      }
      var okRequirement = required(fRequirement, $('#briefRequirementErr'), 'Опишите вашу потребность');

      if (first) first.focus();
      return okName && okPhone && okRequirement;
    }

    function payload() {
      return {
        name: val(fName),
        phone: val(fPhone),
        whatsapp: val(fWhatsapp),
        telegram: val(fTelegram),
        email: val(fEmail),
        company: val(fCompany),
        address: val(fAddress),
        product: val(fProduct),
        qty: val(fQty),
        budget: val(fBudget),
        deadline: val(fDeadline),
        requirement: val(fRequirement),
        source: source,
        formKey: 'website'
      };
    }

    function updateFallbackLink() {
      if (!fallbackLink) return;
      var p = new URLSearchParams();
      [['product', val(fProduct)], ['qty', val(fQty)],
        ['budget', val(fBudget)], ['deadline', val(fDeadline)]].forEach(function (pair) {
        if (pair[1]) p.set(pair[0], pair[1]);
      });
      p.set('source', source);
      fallbackLink.href = FORM_URL + '?' + p.toString();
    }

    function setBusy(busy) {
      form.setAttribute('aria-busy', busy ? 'true' : 'false');
      if (submitBtn) {
        submitBtn.disabled = busy;
        submitBtn.textContent = busy ? 'Отправка...' : 'Отправить заявку ↗';
      }
    }

    function showError(msg) {
      if (errorBox) {
        errorBox.textContent = msg || 'Не удалось отправить заявку. Попробуйте ещё раз.';
        errorBox.hidden = false;
      }
      updateFallbackLink();
      if (fallback) fallback.hidden = false;
    }

    function showSuccess(withTrack) {
      if (success) {
        success.hidden = false;
        success.focus();
      }
      if (body) body.hidden = true;
      if (errorBox) errorBox.hidden = true;
      if (fallback) fallback.hidden = true;
      if (withTrack) {
        track('generate_lead', {
          channel: 'form',
          form_key: 'website',
          source: source,
          product: val(fProduct)
        });
      }
    }

    function openExternal() {
      updateFallbackLink();
      if (fallbackLink) window.open(fallbackLink.href, '_blank', 'noopener');
    }

    if (againBtn) {
      againBtn.addEventListener('click', function () {
        form.reset();
        clearAllErrors();
        if (success) success.hidden = true;
        if (body) body.hidden = false;
        setBusy(false);
        if (fName) fName.focus();
      });
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      clearAllErrors();

      if (fHp && fHp.value.trim()) {
        showSuccess(false);
        return;
      }

      if (!validate()) return;

      if (!NATIVE_LEAD_FORM) {
        openExternal();
        return;
      }

      track('quote_form_submit', {
        form_key: 'website',
        source: source,
        product: val(fProduct)
      });

      setBusy(true);
      var controller = typeof AbortController === 'function' ? new AbortController() : null;
      var timer = controller ? setTimeout(function () { controller.abort(); }, 20000) : null;

      fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload()),
        credentials: 'omit',
        signal: controller ? controller.signal : undefined
      }).then(function (res) {
        if (!res.ok) {
          return res.json().catch(function () { return {}; }).then(function (data) {
            throw new Error((data && data.message) || 'Не удалось отправить заявку. Попробуйте ещё раз.');
          });
        }
        showSuccess(true);
      }).catch(function (err) {
        var msg = err && err.name === 'AbortError'
          ? 'Превышено время ожидания. Попробуйте ещё раз или откройте форму.'
          : (err && err.message && err.message !== 'Failed to fetch'
            ? err.message
            : 'Не удалось отправить заявку. Попробуйте ещё раз или откройте форму.');
        showError(msg);
      }).finally(function () {
        if (timer) clearTimeout(timer);
        setBusy(false);
      });
    });
  }
})();
