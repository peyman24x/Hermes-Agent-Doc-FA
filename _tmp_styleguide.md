# دستورالعمل ترجمه — مرجع فارسی Hermes Agent

این دستورالعمل برای ترجمهٔ صفحات مستندات Hermes Agent از انگلیسی به فارسی است. دقیقاً همین قوانین را اجرا کن.

## ۱. لحن و وفاداری
- فارسی روان، ساده و فنی. مخاطب: توسعه‌دهنده. مثل یک مستند رسمی حرفه‌ای بنویس، نه ترجمهٔ ماشینی.
- **وفاداری ۱۰۰٪:** هیچ پاراگراف، جدول، گام، لیست، هشدار یا مثالی حذف، ادغام یا خلاصه نمی‌شود. ترتیب بخش‌ها عیناً مثل اصلی.
- کل متنِ صفحهٔ منبع باید در صفحهٔ مقصد بیاید. اگر منبع چند نسخهٔ تکراری h1 داشت، فقط یکی را در h1 صفحه بیاور.
- لینک‌های خارجی، دستورها، مسیر فایل‌ها و متغیرهای محیطی عیناً حفظ می‌شوند.

## ۲. قوانین فنی
- **کد و دستورها بایت‌به‌بایت بدون تغییر** (فقط کامنت‌های داخل کد فارسی می‌شوند).
- اسم فایل، متغیر، پرچم، کلید API، مسیر، نام پکیج → همیشه داخل `<code>`.
- **اسکیپ HTML در `<pre>` و `<code>`:** `<` ← `&lt;`، `>` ← `&gt;`، `&` ← `&amp;`. (مهم برای `<<'EOF'`، `&&`، `<>`.)
- بلوک کد: `<pre dir="ltr"><code>…</code></pre>` — بدون wrapper اضافه.
- کدِ درون‌خطی: `<code dir="ltr">…</code>` لازم نیست؛ `<code>` ساده کافی است (CSS خودش جهت را می‌دهد)؛ اگر کد با متن فارسی قاطی شد و به‌هم ریخت، از ‎<code dir="ltr">‎ استفاده کن.
- **اعداد:** در متن فارسی با ارقام فارسی (۱۲، ۳.۹)؛ داخل کد و جدول‌های فنی همان لاتین. اعداد داخل شناسه‌ها/دستورها لاتین می‌مانند.
- در متن فارسی برای جدا کردن اصطلاح لاتین از حروف فارسی از نیم‌فاصلهٔ U+200C استفاده نکن؛ در صورت به‌هم‌ریختگی bidi از کاراکتر ‎ (U+200E LRM) قبل/بعد اصطلاح لاتین استفاده کن.

## ۳. اصطلاح‌نامهٔ تثبیت‌شده (دقیقاً همین‌ها)
| انگلیسی | فارسی |
|---|---|
| agent | ایجنت |
| gateway | گیت‌وی |
| container | کانتینر |
| image (docker) | ایمیج |
| volume | والوم |
| session | نشست |
| profile | پروفایل |
| backend | بک‌اند |
| provider | ارائه‌دهنده |
| checkpoint | چک‌پوینت |
| hook | هوک |
| snapshot | اسنپ‌شات |
| rollback | بازگشت (Rollback) — بار اول با لاتین |
| sandbox | سندباکس |
| dashboard | داشبورد |
| cron | کرون |
| subagent | ساب‌ایجنت |
| supervised | تحت نظارت |
| supervisor | ناظر |
| prompt | پرامپت |
| context | زمینه |
| delegation | واگذاری |
| tool call | فراخوانی ابزار |
| whitelist | فهرست مجاز |
| rate limit | محدودیت نرخ |
| toolset | تول‌ست |
| skill | مهارت |
| memory | حافظه |
| worktree | ورک‌تری |
| messaging platform | پلتفرم پیام‌رسانی |
| endpoint | نقطهٔ پایانی |
| webhook | وب‌هوک |
| pipeline | خط لوله |
| blueprint | نقشهٔ اتوماسیون (blueprint) بار اول با لاتین |
| fallback | پشتیبان |
| routing | مسیریابی |
| credential | اعتبارنامه |
| secret | رمز |
| token (auth) | توکن |
| token (LLM) | توکن |
| embed/embedding | امبدینگ |
| fine-tuning | تنظیم دقیق (fine-tuning) |
| handoff | تحویل دست‌به‌دست |
| runbook | راهنمای عملیاتی |
| go-live | راه‌اندازی نهایی |

- برندهای محصول هرگز ترجمه نمی‌شوند: Telegram, Discord, Slack, Docker, GitHub, AWS, Bedrock, Microsoft Foundry, Ollama, Gemini, Grok, SuperGrok, Nous Portal و غیره.
- بار اول «معادل فارسی (اصطلاح لاتین)»، بعد از آن فقط فارسی.

## ۴. کالاوت‌ها
- تیتر کالاوت: 💡 نکته (tip) · ℹ️ توجه (info/note) · ⚠️ هشدار (warning) · ⛔ احتیاط (caution/danger).
- اگر در منبع کالاوت تیتر متنی دارد، همان تیتر ترجمه می‌شود و ایموجی مناسب در ابتدای `.callout-title` می‌آید.
- اگر کالاوت فقط آیکون دارد: `<div class="callout-title">💡</div>`.
- ساختار:
```html
<div class="callout tip">
  <div class="callout-title">💡</div>
  <p>متن نکته</p>
</div>
```
- کلاس‌های مجاز برای `callout`: `tip`، `note`، `warn`، `caution` (warning→`warn`).

## ۵. ساختار صفحه (اسکلت HTML)
```html
<!DOCTYPE html>
<html lang="fa" dir="rtl" data-root="{ROOT}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TITLE} — مرجع فارسی Hermes Agent</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{ROOT}/assets/style.css">
<script src="{ROOT}/assets/nav-data.js"></script>
</head>
<body>
<header class="topbar">
  <div class="topbar-inner">
    <button class="hamburger" id="navToggle" aria-label="باز کردن فهرست">☰</button>
    <a class="doc-brand" href="{ROOT}/index.html"><span class="logo">🪽</span><span>مرجع فارسی Hermes Agent</span></a>
    <div class="top-actions">
      <a class="icon-btn" href="{EN_URL}" target="_blank" rel="noopener">🌐 نسخهٔ اصلی</a>
      <a class="icon-btn" href="https://github.com/peyman24x/Hermes-Agent-Doc-FA" target="_blank" rel="noopener">⭐ GitHub</a>
      <button class="icon-btn" id="themeToggle">🌙 حالت شب</button>
      <button class="icon-btn" id="printBtn">🖨 چاپ</button>
    </div>
  </div>
</header>
<div class="breadcrumb"><a href="{ROOT}/index.html">خانه</a><span class="sep">/</span>{CAT}<span class="sep">/</span><strong>{TITLE}</strong></div>
<div class="container">
<aside class="sidebar" id="sidebar"></aside>
<main>

<h1>{TITLE}</h1>
… محتوا …

<div class="pager">
  {PREV}
  {NEXT}
</div>
</main>
</div>
<footer class="page-footer">
  ترجمهٔ فارسی غیررسمی · متن اصلی: <a href="{EN_URL}" target="_blank" rel="noopener">{EN_TITLE}</a><br>
  طراحی و اجرا: <a href="https://peyman24x.ir" target="_blank" rel="noopener"><strong>peyman24x.ir</strong></a> · © ۲۰۲۶ · <a href="https://opensource.org/licenses/MIT" target="_blank" rel="noopener">MIT</a> · <a href="{ROOT}/index.html#donate">☕ حمایت از پروژه</a>
</footer>
<button id="toTop" title="بازگشت به بالا">↑</button>
<script src="{ROOT}/assets/main.js"></script>
</body>
</html>
```

- `{ROOT}`: ریشه = `.` (مثل user-stories.html) · یک‌پوشه = `..` (مثل guides/*، developer-guide/*، reference/*، user-guide/*) · دوتایی = `../..` (مثل user-guide/egress/iron-proxy.html، user-guide/skills/google-workspace.html).
- `{CAT}`: نام بخش فارسی برای بردکرامب.
- `{EN_URL}`: آدرس انگلیسی صفحه (داده می‌شود).
- `{EN_TITLE}`: عنوان انگلیسی صفحه برای فوتر.
- `{TITLE}`: دقیقاً همان عنوان فارسی ثبت‌شده در nav-data (داده می‌شود) — هم در `<title>`، هم بردکرامب، هم h1.

## ۶. سکشن‌ها و محتوا
- هر h2 اصلی داخل:
```html
<section class="doc-sec">
<h2><span class="secnum">۱</span> عنوان بخش</h2>
…
</section>
```
- شمارهٔ secnum با ارقام فارسی: ۱ ۲ ۳ … و عیناً به ترتیب h2های منبع.
- h3/h4 بدون secnum، فقط متن فارسی.
- جدول‌ها داخل `<div class="table-wrap"> … </div>`.
- لیست‌ها `<ul>`/`<ol>` معمولی.
- لینک داخلی: اگر صفحهٔ مقصد ترجمه شده → لینک نسبی به `.html` (نام فارسی لینک). اگر نه → آدرس انگلیسی رسمی با `target="_blank" rel="noopener"`. صفحه‌های ترجمه‌شده را می‌توانی از `assets/nav-data.js` (رکوردهای `d:1`) تشخیص دهی.
- لینک‌های anchor داخل صفحه: `#id` (id انگلیسیِ اسلاگ‌شده از تیتر اصلی بماند).
- تصاویر منبع (اگر باشد): همان `src` اصلی با alt فارسی و `loading="lazy"`.
- کامنت‌های HTML توضیحی ننویس.

## ۷. پِیجر (قبلی/بعدی)
- پیجِ قبلی و بعدی دقیقاً همان که داده می‌شود:
```html
<div class="pager">
  <a href="{PREV_HREF}"><span class="dir">→ قبلی</span><span class="ttl">{PREV_TITLE}</span></a>
  <a class="next" href="{NEXT_HREF}"><span class="dir">بعدی ←</span><span class="ttl">{NEXT_TITLE}</span></a>
</div>
```
- اگر قبلی/بعدی وجود ندارد: `<span class="off prev"><span class="dir">→ قبلی</span><span class="ttl">(اولین صفحهٔ گروه)</span></span>` یا برای بعدیِ ناموجود: `<span class="off next"><span class="dir">بعدی ←</span><span class="ttl">{NEXT_TITLE}</span></span>`.
- `{PREV_HREF}`/`{NEXT_HREF}`: لینک نسبی از موقعیت فایل فعلی (هم‌پوشه = فقط نام فایل؛ پوشهٔ دیگر = مسیر نسبی مثل `../guides/x.html`).

## ۸. چک‌لیست نهایی قبل از تحویل
1. همهٔ بخش‌های منبع حاضرند (h2ها یکی‌به‌یک‌اند؛ هیچ جدول/لیست/کد جا نیفتاده).
2. همهٔ `<pre><code>`ها اسکیپ درست دارند (جستجو برای `&&` و `<` خام داخل pre).
3. ارقام فارسی در متن، لاتین در کد.
4. هیچ کلمهٔ انگلیسی اضافه‌ای که باید ترجمه می‌شد باقی نمانده (برندها و اصطلاحات فنی مجازند).
5. title، h1، breadcrumb یکسان‌اند و با عنوان داده‌شده مطابقت دارند.
6. مسیرهای `{ROOT}/assets/...` درست‌اند.
7. فایل با `</html>` تمام می‌شود و HTML معتبر است.
8. فایل فقط با UTF-8 (بدون BOM) ذخیره شود.

## ۹. موارد جزئی نگارشی فارسی
- «می‌کنم» با نیم‌فاصله (U+200C) — همهٔ «می‌»ها و «…‌ها» با نیم‌فاصله.
- «به‌روزرسانی»، «به‌صورت»، «هم‌چنین»، «یک‌بار» — با نیم‌فاصله.
- «را» جدا نوشته می‌شود: «این کار را انجام بده» (نه «این‌کار را»).
- ی/ک فارسی (نه عربی). هیچ «ي» یا «ك» عربی نباشد.
- علامت سؤال فارسی «؟»، ویرگول فارسی «،»، نقطه‌ویرگول «؛».
- صلۀ اضافه با U+06C0 (هٔ): «خانهٔ» — نه «خانه ی» و نه «خانه‌ی».
- گیومهٔ فارسی «…» برای نقل‌قول.
- بین عدد و واحد فارسی نیم‌فاصله: «۱۰ مگابایت».
