<div dir="rtl" align="right">

# گزارش آزمایش دوم آزمایشگاه مهندسی نرم‌افزار

## بررسی عملی اصول SOLID و ارزیابی OpenCode به‌عنوان AI Coding Agent

نام دانشجو: امیرهمایون شریفی زاده 
شماره دانشجویی: 401106114  

---

## 1. هدف آزمایش

در این آزمایش دو کار اصلی انجام دادم. اول، اصول SOLID را روی یک پروژه واقعی بررسی کردم تا فقط در حد تعریف‌های تئوری باقی نماند و بتوانم موارد نقض را در خود کد پیدا کنم، دلیل آن‌ها را توضیح بدهم و با Refactoring مناسب اصلاحشان کنم. در کنار آن، از OpenCode به‌عنوان AI Coding Agent استفاده کردم تا ببینم در تحلیل معماری، ساخت Plan و اعمال Refactoring چقدر قابل اتکاست و در چه جاهایی هنوز نیاز به بررسی و تصمیم‌گیری انسانی دارد.

برای اینکه اثر SOLID فقط در سطح نظری بررسی نشود، قابلیت جدید پرداخت نقدی (`cash`) دو بار به پروژه اضافه شد:

یک بار روی نسخه اولیه و بدون اصلاح معماری؛ یک بار پس از Refactoring نسخه دوم بر اساس اصول SOLID.

در پایان، میزان و نوع تغییرات لازم برای افزودن همان قابلیت در دو معماری مقایسه شد. این مقایسه نشان می‌دهد مزیت SOLID لزوماً «کم‌شدن تعداد خطوط کد» نیست، بلکه مهم‌تر از آن محدودشدن محل اثر تغییر، کاهش coupling و امکان افزودن رفتار جدید بدون دست‌کاری منطق مرکزی موجود است.

در طول کار، خروجی OpenCode را پاسخ قطعی در نظر نگرفتم. تحلیل‌ها، Planها و تغییرات پیشنهادی را بررسی کردم و هرجا لازم بود، پیشنهاد Agent را اصلاح یا محدود کردم.

---

## 2. ساختار نهایی پروژه

ساختار اصلی تحویل به شکل زیر است:


</div>

<div dir="ltr" align="left">

```text
2/
├── README.md
├── AGENTS.md
├── .opencode/
│   └── skills/
│       └── solid-review/
│           └── SKILL.md
│
├── 01-Without-OOD-Principles/
│   └── store/
│       ├── main.py
│       ├── models.py
│       ├── notification.py
│       ├── order_service.py
│       ├── payment.py
│       ├── pricing.py
│       └── storage.py
│
├── 02-Applied-OOD-Principles/
│   └── store/
│       ├── discount_rules.py
│       ├── main.py
│       ├── models.py
│       ├── notification.py
│       ├── order_service.py
│       ├── payment.py
│       ├── ports.py
│       ├── pricing.py
│       ├── pricing_service.py
│       ├── receipt.py
│       ├── storage.py
│       ├── strategies.py
│       └── validators.py
│
└── evidence/
    ├── original-baseline.txt
    ├── 01-cash-changes.diff
    ├── 02-after-solid.txt
    ├── 02-cash-changes.diff
    ├── source-only-stats.txt
    ├── final-verification.txt
    ├── git-history.txt
    └── opencode-sessions/
        └── session-01.json
```

</div>

<div dir="rtl" align="right">


دو پوشه‌ی `01-Without-OOD-Principles` و `02-Applied-OOD-Principles` از یک baseline مشترک ساخته شدند؛ بنابراین نسخه دوم از نسخه اولِ دارای Cash کپی نشده و مقایسه دو آزمایش مستقل باقی مانده است.

---

## 3. آماده‌سازی، Git و نقاط کنترل آزمایش

برای اینکه ترتیب آزمایش قابل اثبات باشد، چند checkpoint در Git ثبت شد. تاریخچه واقعی repository به صورت زیر است:

| Commit/Tag | توضیح |
|---|---|
| `bcb0a56` — `baseline` | ثبت دو کپی مستقل از پروژه اولیه |
| `eecb981` | افزودن دستورهای پروژه در `AGENTS.md` |
| `49455d1` — `without-ood-cash` | افزودن Cash به نسخه بدون SOLID |
| `99359ac` — `with-ood-refactor` | اعمال Refactoring روی نسخه دوم، پیش از Cash |
| `0eaff4f` — `with-ood-cash` | افزودن Cash به نسخه Refactorشده |

این ترتیب برای اعتبار مقایسه مهم است؛ زیرا نشان می‌دهد Cash در نسخه دوم پس از ثبت نسخه SOLID-only اضافه شده است.

### نکته درباره آمار Git

فایل‌های `__pycache__/*.pyc` در repository track شده‌اند و اگر diff خام Git مبنا قرار گیرد، تعداد فایل‌های تغییرکرده را به‌صورت مصنوعی افزایش می‌دهند. به همین دلیل تمام آمار مقایسه‌ای این گزارش فقط روی فایل‌های منبع `*.py` محاسبه شده است. خروجی این محاسبه در `evidence/source-only-stats.txt` قرار دارد.

---

# بخش اول — آشنایی و راه‌اندازی OpenCode

## 4. مفاهیم مورد استفاده از OpenCode

پیش از شروع Refactoring، مفاهیم اصلی مورد نیاز برای آزمایش بررسی شدند:

نصب و اجرای OpenCode؛ اتصال مدل زبانی و انتخاب مدل؛ فایل `AGENTS.md` برای دادن context و قوانین پایدار پروژه به Agent؛ مفهوم Agent و تفاوت نقش تحلیل/برنامه‌ریزی با اجرای تغییر؛ Skill برای تعریف workflow تخصصی پروژه؛ استفاده از Plan mode برای تحلیل و طراحی قبل از edit؛ استفاده از Build mode برای اعمال Plan تأییدشده؛ نوشتن Promptهای صریح درباره scope، محدودیت‌ها، خروجی مورد انتظار و شرط تأیید انسانی.

### تجربه عملی نصب روی Windows

OpenCode از طریق npm نصب شد. در PowerShell به دلیل Execution Policy اجرای wrapper با نام `opencode.ps1` مسدود بود، بنابراین از `opencode.cmd` استفاده شد. نسخه ثبت‌شده در session export موجود، OpenCode 1.18.22 است.

در تلاش اولیه برای مدل‌های رایگان Zen، مدل‌های `nemotron-3-ultra-free` و `mimo-v2.5-free` با پاسخ `403 Forbidden` مواجه شدند. این رخداد در `evidence/opencode-sessions/session-01.json` ثبت شده است. فایل session موجود فقط این تلاش‌های اولیه را پوشش می‌دهد و همه تعامل‌های موفق بعدی در export قرار نگرفته‌اند؛ بنابراین در این گزارش برای ادعاهای فنی، علاوه بر تعامل‌های ثبت‌شده، از Git history، diffها، کد نهایی و خروجی اجرای واقعی به‌عنوان شواهد اصلی استفاده شده است.

---

## 5. نقش `AGENTS.md`

فایل `AGENTS.md` برای جلوگیری از اشتباه Agent در ترتیب آزمایش ایجاد شد. مهم‌ترین قواعد ثبت‌شده عبارت‌اند از:

نسخه `01-Without-OOD-Principles` هنگام اضافه‌کردن Cash نباید Refactor شود؛ در نسخه `02-Applied-OOD-Principles` ابتدا SOLID اعمال شود و سپس Cash اضافه شود؛ پیاده‌سازی Cash از نسخه اول نباید مستقیماً به نسخه دوم کپی شود؛ قبل از تغییر کد، Agent باید تغییرات پیشنهادی را توضیح دهد و منتظر تأیید بماند؛ رفتار `credit_card`، `paypal` و `bitcoin` باید حفظ شود؛ پس از تغییرات، `python -m store.main` اجرا شود؛ Refactoring نامرتبط با feature در مرحله افزودن Cash انجام نشود.

این فایل کمک کرد قوانین آزمایش فقط داخل یک Prompt باقی نمانند و در تمام مراحل به‌عنوان context ثابت پروژه در دسترس Agent باشند.

---

# بخش دوم — بررسی نسخه اولیه

## 6. اجرای baseline و مشاهده رفتار پروژه

پروژه اولیه از داخل هر پوشه با دستور زیر اجرا می‌شود:


</div>

<div dir="ltr" align="left">

```powershell
python -m store.main
```

</div>

<div dir="rtl" align="right">


خروجی baseline در `evidence/original-baseline.txt` ذخیره شده است.

دو مشاهده مهم در baseline وجود داشت:

### سفارش عادی شماره 101


</div>

<div dir="ltr" align="left">

```text
Subtotal = $1024.99
Discount = $205.00
Shipping = $0.00
Total    = $819.99
```

</div>

<div dir="rtl" align="right">


این رفتار پس از Refactoring نیز باید حفظ می‌شد.

### Bundle شماره 103

در نسخه اولیه خروجی Bundle به صورت زیر بود:


</div>

<div dir="ltr" align="left">

```text
Subtotal = $0.00
Discount = $0.00
Shipping = $5.00
Total    = $5.00
```

</div>

<div dir="rtl" align="right">


این نتیجه از رفتار `BundleOrder` ناشی می‌شد. کلاس مذکور از `Order` ارث می‌برد، اما در سازنده‌ی parent مقدار `items=[]` قرار می‌داد. بنابراین propertyهای inherited مثل `subtotal` و `item_count` محتوای واقعی سفارش‌های داخلی را نمی‌دیدند. این رفتار در ادامه به‌عنوان شاهد اصلی نقض LSP استفاده شد.

---

# بخش سوم — گام اول آزمایش: افزودن Cash بدون اصلاح SOLID

## 7. هدف این مرحله

در این مرحله عمداً معماری اصلاح نشد. هدف این بود که مشخص شود اگر سیستم در طراحی اولیه باقی بماند، افزودن یک روش پرداخت جدید دقیقاً کدام قسمت‌های موجود را مجبور به تغییر می‌کند.

قید اصلی برای Agent این بود:

> Cash را با کمترین تغییر لازم اضافه کن؛ هیچ Refactoring یا بهبود SOLID در `01-Without-OOD-Principles` انجام نده و قبل از تغییر، فایل‌های لازم را مشخص کن.

---

## 8. تغییرات لازم برای Cash در نسخه اولیه

### 8.1 تغییر `PaymentProcessor`

در `01-Without-OOD-Principles/store/payment.py` روش پرداخت توسط یک زنجیره `if/elif` انتخاب می‌شود. برای Cash لازم شد همان متد موجود ویرایش شود:


</div>

<div dir="ltr" align="left">

```python
elif method == "cash":
    print(f"[payment] Cash payment received: {amount:.2f}")
    return f"paid_by_cash:{amount:.2f}"
```

</div>

<div dir="rtl" align="right">


این تغییر مهم‌ترین شاهد تجربی OCP در این آزمایش است: هر روش پرداخت جدید باعث اضافه‌شدن branch دیگری به منطق مرکزی موجود می‌شود.

### 8.2 تغییر Demo در `main.py`

برای مشاهده قابلیت جدید، سفارش 104 ساخته شد:


</div>

<div dir="ltr" align="left">

```python
cash_order = Order(
    id=104,
    customer=regular,
    payment_method="cash",
    items=[OrderItem(5, "Notebook", 15.00, 1)],
)
```

</div>

<div dir="rtl" align="right">


و سپس توسط `OrderService` پردازش شد.

---

## 9. جدول تغییرات گام اول

| ردیف | کلاس / فایل تغییر یافته | نوع تغییر | توضیح تغییر و علت ضرورت |
|---:|---|---|---|
| 1 | `store/payment.py` / `PaymentProcessor.process()` | تغییر منطق موجود + افزودن branch | بدون ویرایش `PaymentProcessor` امکان شناسایی `cash` وجود نداشت؛ یک `elif` جدید اضافه شد. |
| 2 | `store/main.py` | تغییر Demo | یک سفارش Cash برای نمایش و بررسی قابلیت جدید ساخته و اجرا شد. |

### اندازه تغییر بر اساس Git

Diff بین tagهای `baseline` و `without-ood-cash` فقط برای فایل‌های منبع:


</div>

<div dir="ltr" align="left">

```text
2 files changed, 14 insertions(+), 2 deletions(-)
```

</div>

<div dir="rtl" align="right">


جزئیات:


</div>

<div dir="ltr" align="left">

```text
main.py     +10 / -2
payment.py  +4  / -0
```

</div>

<div dir="rtl" align="right">


مهم‌تر از تعداد خط‌ها این است که فایل مرکزی پرداخت (`payment.py`) مجبور به تغییر شد.

---

## 10. خروجی Cash در نسخه اولیه

سفارش Cash دارای یک Notebook به قیمت 15 دلار است. با توجه به قانون ارسال، چون subtotal کمتر از 100 دلار است، 5 دلار هزینه ارسال اضافه می‌شود:


</div>

<div dir="ltr" align="left">

```text
Subtotal = $15.00
Discount = $0.00
Shipping = $5.00
Total    = $20.00
Payment  = paid_by_cash:20.00
```

</div>

<div dir="rtl" align="right">


اجرای نهایی نسخه اول این خروجی را تأیید می‌کند.

---

# بخش چهارم — گام دوم: تحلیل اصول SOLID

## 11. جمع‌بندی تحلیل

تحلیل روی نسخه دوم و قبل از Refactoring انجام شد. جدول زیر نتیجه نهاییِ بازبینی‌شده را نشان می‌دهد:

| اصل | رعایت شده؟ | محل اصلی در پروژه | توضیح کوتاه |
|---|---|---|---|
| SRP | خیر | `store/order_service.py` / `OrderService` | اعتبارسنجی، pricing، shipping، payment، persistence، notification و receipt در یک workflow متمرکز شده‌اند. |
| OCP | خیر | `store/payment.py` و `store/pricing.py` | افزودن روش پرداخت یا rule تخفیف جدید نیازمند ویرایش زنجیره شرط‌های موجود است. |
| LSP | خیر | `store/models.py` / `BundleOrder` | subtype مانند `Order` عادی رفتار نمی‌کند؛ subtotal و item_count آن عملاً صفر می‌شوند. |
| ISP | خیر | `store/notification.py` / `SmsOnlyNotifier` | notifier فقط-SMS مجبور به داشتن متدهای email و push شده و برای آن‌ها exception می‌دهد. |
| DIP | خیر | `store/order_service.py` / `OrderService.__init__()` | سرویس سطح بالا concrete dependencyهای خود را مستقیماً می‌سازد. |

---

## 12. SRP — Single Responsibility Principle

### علت نقض

`OrderService.process_order()` در نسخه اولیه چند وظیفه مستقل را انجام می‌دهد:

بررسی معتبر بودن سفارش؛ محاسبه subtotal؛ محاسبه تخفیف؛ محاسبه shipping؛ اجرای payment؛ تغییر status و persistence؛ ارسال email و SMS؛ فرمت و چاپ receipt.

در نتیجه تغییر قوانین اعتبارسنجی، قیمت‌گذاری، notification یا format receipt همگی می‌توانند باعث تغییر همان کلاس شوند؛ یعنی کلاس بیش از یک reason to change دارد.

### روش اصلاح

در نسخه Refactorشده مسئولیت‌ها به componentهای تخصصی منتقل شدند:

`OrderValidator` در `validators.py`؛ `PricingService` در `pricing_service.py`؛ `DiscountCalculator` و Ruleهای مستقل؛ `PaymentProcessor`؛ Repository؛ notification senderها؛ `ReceiptFormatter` در `receipt.py`.

`OrderService` باقی ماند، اما نقش آن به orchestration محدود شد.

### دلیل انتخاب راهکار

حذف کامل `OrderService` منطقی نبود؛ هماهنگ‌کردن مراحل checkout خود یک مسئولیت معتبر است. بنابراین به جای شکستن workflow به چند orchestrator مصنوعی، منطق تخصصی به collaboratorها منتقل شد و سرویس اصلی فقط ترتیب اجرا را کنترل می‌کند.

---

## 13. OCP — Open/Closed Principle

### 13.1 Payment

#### علت نقض

در baseline، `PaymentProcessor.process()` شامل branchهای زیر بود:


</div>

<div dir="ltr" align="left">

```text
credit_card
paypal
bitcoin
```

</div>

<div dir="rtl" align="right">


برای Cash نیز مجبور شدیم `elif` چهارم اضافه کنیم. بنابراین extension مستقیم به modification منجر شد.

#### روش اصلاح

در نسخه دوم، رفتار پرداخت به Strategyهای مستقل منتقل شد:


</div>

<div dir="ltr" align="left">

```text
CreditCardStrategy
PayPalStrategy
BitcoinStrategy
CashStrategy   ← بعداً اضافه شد
```

</div>

<div dir="rtl" align="right">


`PaymentProcessor` یک mapping از key روش پرداخت به Strategy دریافت می‌کند و دیگر منطق اختصاصی card/PayPal/Bitcoin را در `process()` ندارد.

#### دلیل انتخاب

Strategy برای این مسئله ساده و مستقیم است؛ هر نوع پرداخت رفتار مستقل دارد و dispatch از implementation جدا می‌شود. برای اضافه‌کردن Cash پس از SOLID، `PaymentProcessor.process()` تغییر نکرد.

### 13.2 Discount

#### علت نقض

`DiscountCalculator.calculate()` نیز یک زنجیره شرط برای VIP، تعداد آیتم و coupon داشت. اضافه‌کردن rule جدید مستلزم تغییر همان الگوریتم بود.

#### روش اصلاح

سه rule مستقل ایجاد شدند:

`VipDiscountRule`؛ `VolumeDiscountRule`؛ `CouponDiscountRule`.

`DiscountCalculator` آن‌ها را به ترتیب بررسی می‌کند و اولین تخفیف غیرصفر را بازمی‌گرداند.

#### دلیل انتخاب

این مدل ضمن افزایش توسعه‌پذیری، رفتار قبلی را هم حفظ می‌کند. ترتیب قواعد همچنان:

VIP → 20%؛ Volume (`item_count >= 10`) → 10%؛ `WELCOME10` → 10%؛ در غیر این صورت صفر.

است؛ بنابراین Refactoring باعث ترکیب ناخواسته چند discount نشده است.

---

## 14. LSP — Liskov Substitution Principle

### علت نقض

در baseline:


</div>

<div dir="ltr" align="left">

```python
class BundleOrder(Order):
    def __init__(self, id, customer, orders):
        super().__init__(id=id, customer=customer, items=[])
        self.orders = orders
```

</div>

<div dir="rtl" align="right">


هر کدی که یک `Order` دریافت می‌کند انتظار دارد `subtotal` و `item_count` نماینده آیتم‌های واقعی سفارش باشند. ولی جایگزین‌کردن `Order` با `BundleOrder` این فرض را می‌شکند.

شاهد رفتاری آن output واقعی baseline است:


</div>

<div dir="ltr" align="left">

```text
Bundle subtotal = 0.00
Bundle total    = 5.00
```

</div>

<div dir="rtl" align="right">


همچنین در validation یک special case وجود داشت:


</div>

<div dir="ltr" align="left">

```python
if not order.items and not isinstance(order, BundleOrder):
```

</div>

<div dir="rtl" align="right">


یعنی client برای کارکردن با subtype مجبور بود نوع خاص آن را بشناسد.

### روش اصلاح

در نسخه جدید `BundleOrder` دیگر از `Order` ارث نمی‌برد و از composition استفاده می‌کند. هر دو نوع از طریق قرارداد ساختاری `OrderLike` قابل استفاده‌اند. Bundle آیتم‌ها، subtotal و تعداد آیتم‌های child orderها را تجمیع می‌کند.

### دلیل انتخاب

مسئله اصلی یک رابطه inheritance نامعتبر بود. composition صادقانه‌تر از «is-a Order» قبلی است و protocol اجازه می‌دهد `OrderService` همچنان با هر دو نوع به یک شکل کار کند.

### نتیجه واقعی پس از اصلاح

در `evidence/02-after-solid.txt`، Bundle شماره 103 چنین محاسبه می‌شود:


</div>

<div dir="ltr" align="left">

```text
Subtotal = $1194.99
Discount = $239.00
Shipping = $0.00
Total    = $955.99
```

</div>

<div dir="rtl" align="right">


تغییر از 5 دلار به 955.99 دلار regression ناخواسته نیست؛ 5 دلار نتیجه defect طراحی baseline بود.

---

## 15. ISP — Interface Segregation Principle

### علت نقض

در نسخه اولیه:


</div>

<div dir="ltr" align="left">

```text
NotificationService
├── send_email
├── send_sms
└── send_push
```

</div>

<div dir="rtl" align="right">


اما `SmsOnlyNotifier` فقط SMS را پشتیبانی می‌کرد و برای دو متد دیگر `NotImplementedError` ایجاد می‌کرد. این یعنی implementation مجبور به قبول interfaceای بزرگ‌تر از نیاز خود شده بود.

### روش اصلاح

در `ports.py` قراردادهای کوچک جدا تعریف شدند:


</div>

<div dir="ltr" align="left">

```text
EmailSender
SmsSender
PushSender
```

</div>

<div dir="rtl" align="right">


و `SmsOnlyNotifier` در نسخه جدید فقط `send_sms` دارد و دیگر متدهای غیرقابل پشتیبانی را به ارث نمی‌برد.

### دلیل انتخاب

به جای ایجاد interface واحد و fat، هر client فقط operation مورد نیازش را می‌بیند. همچنین `OrderService` فقط `EmailSender` و `SmsSender` را دریافت می‌کند؛ Push به آن تحمیل نشده است.

---

## 16. DIP — Dependency Inversion Principle

### علت نقض

در نسخه اولیه `OrderService.__init__()` مستقیماً concreteها را می‌سازد:


</div>

<div dir="ltr" align="left">

```python
self.discount_calculator = DiscountCalculator()
self.payment_processor = PaymentProcessor()
self.notification = NotificationService()
self.database = MySqlDatabase()
```

</div>

<div dir="rtl" align="right">


در نتیجه high-level workflow با انتخاب implementationهای low-level درهم تنیده شده است.

### روش اصلاح

در نسخه دوم dependencyها از constructor وارد می‌شوند:


</div>

<div dir="ltr" align="left">

```text
validator
pricing
payment
email_sender
sms_sender
repository
receipt_formatter
```

</div>

<div dir="rtl" align="right">


ساخت concreteها در `main.py` انجام می‌شود که نقش Composition Root را دارد.

### دلیل انتخاب

این روش وابستگی high-level code را به contract کاهش می‌دهد و امکان جایگزینی implementationها و نوشتن fake/stub برای تست را بیشتر می‌کند. در عین حال برای پروژه کوچک، نیازی به Service Locator یا framework DI ایجاد نشده است.

---

# بخش پنجم — بازبینی تحلیل OpenCode

## 17. چرا تحلیل اولیه Agent بدون اصلاح پذیرفته نشد؟

در این مرحله فقط به تحلیل Agent اکتفا نکردم. OpenCode چند مورد را درست تشخیص داده بود، اما در تحلیل اولیه بعضی design smellها را بیش از حد به اصول SOLID نسبت می‌داد. چند نمونه از خروجی آن این‌ها بودند:

دسترسی `PaymentProcessor` به `order.customer.credit_card` به‌عنوان DIP گزارش شده بود؛ دسترسی `DiscountCalculator` به `order.customer.is_vip` نیز DIP تلقی شده بود؛ `PaymentProcessor` به دلیل monolithic بودن به ISP نسبت داده شده بود؛ وجود اطلاعات payment در `Customer` به‌عنوان SRP violation قطعی در نظر گرفته شده و استخراج `Wallet` پیشنهاد شده بود.

این موارد نیاز به اصلاح داشتند، چون:

direct property access می‌تواند coupling یا Law of Demeter concern باشد، اما به‌تنهایی DIP نیست؛ بزرگ‌بودن یک کلاس به‌تنهایی ISP را اثبات نمی‌کند؛ entity دارای چند data field لزوماً SRP را نقض نمی‌کند؛ `SmsOnlyNotifier` شاهد بسیار روشن‌تری برای ISP است؛ concrete construction داخل `OrderService` شاهد اصلی DIP است.

به Agent Prompt اصلاحی داده شد تا از تعریف سخت‌گیرانه‌تر SOLID استفاده کند و design smell را از confirmed SOLID violation جدا نماید. همین تجربه مستقیماً در طراحی Skill مرحله بعد استفاده شد.

---

# بخش ششم — گام سوم: طراحی Skill

## 18. Skill با نام `solid-review`

مسیر Skill پروژه:


</div>

<div dir="ltr" align="left">

```text
.opencode/skills/solid-review/SKILL.md
```

</div>

<div dir="rtl" align="right">


### 18.1 هدف Skill چیست؟

هدف `solid-review` ایجاد یک workflow تکرارپذیر بود تا Agent قبل از هر Refactoring:

پروژه را بخواند؛ هر یک از پنج اصل را جداگانه تحلیل کند؛ به جای مثال‌های textbook، evidence واقعی کد ارائه کند؛ دقیقاً فایل، کلاس و متد را مشخص کند؛ راهکار حداقلی پیشنهاد دهد؛ و بدون تأیید کاربر وارد implementation نشود.

### 18.2 چه اطلاعاتی در اختیار Agent قرار می‌دهد؟

Skill شامل موارد زیر است:

تعریف دقیق SRP/OCP/LSP/ISP/DIP؛ معیارهایی برای تشخیص هر اصل؛ فرمت ثابت خروجی شامل Location، Evidence، Consequence، Refactoring، Benefit و Confidence؛ قاعده جداسازی smell از SOLID violation؛ catalogue کوچک از الگوهای مناسب مثل Strategy، constructor injection، composition و interface segregation؛ checklist بررسی رفتار پس از Refactoring؛ Approval Gate برای جلوگیری از edit بدون تأیید.

یکی از مهم‌ترین قواعد Skill که مستقیماً از خطای تحلیل اولیه Agent به دست آمد این است:

> direct property access لزوماً DIP نیست، large class لزوماً SRP/ISP نیست و data-rich entity لزوماً SRP را نقض نمی‌کند.

### 18.3 چرا این ساختار انتخاب شد؟

اگر Skill فقط تعریف SOLID را می‌گفت، Agent همچنان می‌توانست پاسخ‌های عمومی تولید کند. بنابراین ساختار آن طوری طراحی شد که Agent مجبور باشد reasoning خود را به یک بخش واقعی از کد وصل کند. همچنین approval gate از این جلوگیری می‌کند که یک تشخیص اشتباه مستقیماً به تغییر معماری تبدیل شود.

### 18.4 یک محدودیت کوچک Skill نهایی

در فایل نهایی یک ناسازگاری متنی کوچک باقی مانده است: در یک بخش، استفاده از mapping ساده Strategy مجاز دانسته شده، ولی در انتهای Constraints یک خط قدیمی هنوز «registries» را به‌طور مطلق منع می‌کند. implementation واقعی از mapping ساده استفاده کرده و آزمایش مختل نشده است، اما در تکرار بعدی بهتر است این خط تکراری حذف شود تا دستورها کاملاً سازگار باشند.

---

# بخش هفتم — گام چهارم: تولید و بازبینی Plan

## 19. Plan اولیه OpenCode

OpenCode برای اصلاح پنج اصل، Plan چندمرحله‌ای پیشنهاد کرد که در مجموع شامل این جهت‌ها بود:

تعریف Protocolها و constructor injection؛ جداکردن validation، pricing و receipt از `OrderService`؛ تبدیل payment به Strategy؛ تبدیل discountها به Rule chain؛ تفکیک notification interfaceها؛ جایگزینی inheritance نامناسب `BundleOrder` با composition.

فایل‌های جدید پیشنهادی شامل `ports.py`، `validators.py`، `pricing_service.py`، `receipt.py`، `strategies.py` و `discount_rules.py` بودند؛ این جهت کلی در implementation نهایی نیز دیده می‌شود.

---

## 20. بازبینی انسانی Plan و اصلاحات پیشنهادی

Plan بدون بررسی تأیید نشد. موارد زیر به Agent بازخورد داده شد:

### 20.1 ترتیب Stepها

در Plan اولیه، Step اول قرار بود `OrderService` به `OrderValidator`، `PricingService` و `ReceiptFormatter` تزریق شود، در حالی که این کلاس‌ها تازه در Step بعدی ایجاد می‌شدند. بنابراین ادعای «runnable بودن بعد از هر Step» سازگار نبود. پیشنهاد شد DIP و SRP در یک مرحله منسجم ترکیب یا ترتیب آن‌ها اصلاح شود.

### 20.2 default dependencyها

Agent پیشنهاد داده بود `PaymentProcessor()` و `DiscountCalculator()` برای backward compatibility در صورت نبود آرگومان، strategy/ruleهای concrete را خودشان بسازند. به Agent توضیح داده شد که این کار بخشی از concrete construction را دوباره داخل componentها قرار می‌دهد و composition root را تضعیف می‌کند.

### 20.3 نام Protocol و concrete

استفاده از نام یکسان برای `ports.PaymentProcessor` و کلاس concrete `payment.PaymentProcessor` باعث ابهام می‌شود. پیشنهاد شد نام abstractionها واضح‌تر باشند.

### 20.4 پیچیدگی غیرضروری `OrderLike`

در Plan، متدهای wrapper مثل `get_items()`، `get_subtotal()` و `get_item_count()` پیشنهاد شده بودند. پیشنهاد شد در صورت امکان protocol با shape طبیعی domain model هماهنگ باشد و wrapperهای صرفاً برای protocol اضافه نشوند.

### 20.5 `customer_data: dict`

در Plan، Strategy پرداخت یک `dict` بدون type مشخص دریافت می‌کرد. پیشنهاد شد از `Customer` موجود استفاده شود، چون تبدیل domain object به dictionary برای حل SOLID لازم نیست.

### 20.6 Repository contract

پروژه اولیه متدهای `save_order` و `load_order` داشت، ولی Plan متدهای جدید `save`/`load` پیشنهاد کرد. درخواست شد contract حداقلی و مطابق نیاز client باشد.

### 20.7 Verification

اجرای `store.main` به‌تنهایی PayPal و Bitcoin را واقعاً process نمی‌کرد. بنابراین درخواست شد verification صریح برای `credit_card`، `paypal`، `bitcoin` و unknown method انجام شود.

برای من کاربرد اصلی Plan mode همین بود: قبل از اینکه فایلی تغییر کند، می‌شد طرح Agent را بررسی کرد، ایرادهایش را دید و بعد درباره اجرای آن تصمیم گرفت.

---

## 21. کدام اصلاحات در implementation نهایی کامل نشدند؟

بازبینی نهایی کد نشان می‌دهد جهت کلی Plan اصلاح شد، ولی همه نکات پیشنهادی بالا به‌طور کامل در کد نهایی اعمال نشده‌اند. برای مثال:

`PaymentProcessor` هنوز در صورت `strategies=None` از `build_payment_strategies()` استفاده می‌کند؛ `DiscountCalculator` نیز default rule builder دارد؛ نام برخی Protocolها با concreteها یکسان است؛ `OrderLike` همچنان متدهای `get_*` دارد؛ `PaymentStrategy` هنوز `customer_data: dict` می‌گیرد؛ Repository علاوه بر متدهای اصلی، wrapperهای `save/load` دارد.

این موارد باعث از کار افتادن پروژه نشده‌اند و بخش اصلی Refactoring درست انجام شده است، اما نشان می‌دهند حتی بعد از یک Plan خوب هم نمی‌شود code review نهایی را کنار گذاشت.

---

# بخش هشتم — گام پنجم: اعمال Refactoring در Build mode

## 22. تغییرات معماری نسخه دوم

پس از تأیید جهت Plan، تغییرات در نسخه `02-Applied-OOD-Principles` اعمال شدند.

Diff source-only بین `baseline` و tag `with-ood-refactor`:


</div>

<div dir="ltr" align="left">

```text
13 files changed, 358 insertions(+), 108 deletions(-)
```

</div>

<div dir="rtl" align="right">


شش فایل source جدید اضافه شدند:

`discount_rules.py`؛ `ports.py`؛ `pricing_service.py`؛ `receipt.py`؛ `strategies.py`؛ `validators.py`.

و هفت فایل موجود تغییر کردند:

`main.py`؛ `models.py`؛ `notification.py`؛ `order_service.py`؛ `payment.py`؛ `pricing.py`؛ `storage.py`.

### 22.1 `OrderService` به orchestrator تبدیل شد

نسخه نهایی به جای ساخت concreteها، dependencyها را در constructor دریافت می‌کند و `process_order` مراحل زیر را هماهنگ می‌کند:


</div>

<div dir="ltr" align="left">

```text
validate
  ↓
calculate pricing
  ↓
payment
  ↓
persist
  ↓
notify
  ↓
receipt
```

</div>

<div dir="rtl" align="right">


### 22.2 Payment Strategy

`PaymentProcessor` دیگر branch اختصاصی credit card/PayPal/Bitcoin ندارد و Strategy مناسب را از mapping پیدا می‌کند.

### 22.3 Discount Rule chain

قواعد تخفیف به سه کلاس جدا تبدیل شدند و ترتیب قبلی حفظ شد.

### 22.4 Bundle composition

`BundleOrder` از inheritance نامناسب خارج شد و اطلاعات child orderها را از طریق composition تجمیع می‌کند.

### 22.5 Notification segregation

`SmsOnlyNotifier` دیگر از service دارای email/push ارث نمی‌برد و فقط قابلیت واقعی خود را ارائه می‌کند.

### 22.6 Composition Root

تمام concrete dependencyها در `main.py` ساخته و به `OrderService` تزریق می‌شوند.

---

## 23. Verification پس از Refactoring

پس از Refactoring و قبل از اضافه‌کردن Cash، tag `with-ood-refactor` ثبت شد. خروجی آن در `evidence/02-after-solid.txt` نگهداری شده است.

نتایج کلیدی:

| رفتار | baseline | بعد از Refactoring |
|---|---:|---:|
| Order 101 total | `$819.99` | `$819.99` |
| Bundle 103 subtotal | `$0.00` | `$1194.99` |
| Bundle 103 total | `$5.00` | `$955.99` |

رفتار Order 101 حفظ شد و تغییر Bundle دقیقاً همان defect مورد نظر LSP را اصلاح کرد.

پروژه test suite خودکار ندارد، بنابراین verification عمدتاً با اجرای demo و smoke test انجام شده است. در بازبینی نهایی گزارش، هر چهار payment method (`credit_card`, `paypal`, `bitcoin`, `cash`) و حالت unknown به‌صورت مستقیم اجرا شدند؛ نتیجه در `evidence/final-verification.txt` ثبت شده و هر چهار روش receipt صحیح تولید می‌کنند و unknown method همچنان `ValueError` می‌دهد.

---

# بخش نهم — افزودن دوباره Cash پس از SOLID

## 24. تغییرات لازم در نسخه Refactorشده

پس از ثبت tag `with-ood-refactor`، همان قابلیت Cash دوباره اضافه شد.

در این مرحله دیگر نیازی نبود `PaymentProcessor.process()` تغییر کند. رفتار جدید در Strategy مستقل اضافه شد:


</div>

<div dir="ltr" align="left">

```python
class CashStrategy:
    def process(self, customer_data: dict, amount: float) -> str:
        print(f"[payment] Cash payment received: {amount:.2f}")
        return f"paid_by_cash:{amount:.2f}"
```

</div>

<div dir="rtl" align="right">


سپس این Strategy در mapping موجود ثبت شد:


</div>

<div dir="ltr" align="left">

```python
"cash": CashStrategy(),
```

</div>

<div dir="rtl" align="right">


و همان Demo سفارش 104 به `main.py` اضافه شد.

---

## 25. جدول تغییرات Cash بعد از SOLID

| ردیف | کلاس / فایل تغییر یافته | نوع تغییر | توضیح |
|---:|---|---|---|
| 1 | `store/strategies.py` / `CashStrategy` | افزودن implementation مستقل + registration | رفتار Cash بدون تغییر `PaymentProcessor.process()` اضافه شد. |
| 2 | `store/main.py` | تغییر Demo | سفارش Cash برای مشاهده قابلیت نهایی ایجاد و اجرا شد. |

Diff بین `with-ood-refactor` و `with-ood-cash` فقط برای source:


</div>

<div dir="ltr" align="left">

```text
2 files changed, 17 insertions(+), 2 deletions(-)
```

</div>

<div dir="rtl" align="right">


جزئیات:


</div>

<div dir="ltr" align="left">

```text
main.py       +10 / -2
strategies.py +7  / -0
```

</div>

<div dir="rtl" align="right">


نکته مهم این است که تعداد فایل‌های production لمس‌شده نسبت به نسخه اولیه کمتر نشده است؛ در هر دو حالت دو فایل تغییر کرده‌اند. حتی تعداد خط‌های افزوده‌شده در نسخه SOLID کمی بیشتر است. بهبود اصلی در نوع تغییر است، نه صرفاً تعداد خطوط.

---

# بخش دهم — مقایسه کمی و کیفی دو نسخه

## 26. مقایسه Cash قبل و بعد از SOLID

| معیار | بدون SOLID | بعد از SOLID |
|---|---|---|
| فایل‌های source تغییرکرده | 2 | 2 |
| Insertions / Deletions | `+14 / -2` | `+17 / -2` |
| تغییر `PaymentProcessor.process()` | بله | خیر |
| افزودن branch جدید به dispatch مرکزی | بله، یک `elif` | خیر |
| رفتار Cash در کلاس مستقل | خیر | بله، `CashStrategy` |
| تغییر Demo | بله | بله |
| تغییر registration/wiring | ساختار registry وجود نداشت | بله، یک entry در mapping |
| ریسک اثر روی منطق روش‌های قبلی | بیشتر | کمتر |
| محل اصلی توسعه feature | داخل processor موجود | کنار Strategyهای مستقل |

### تفسیر نتیجه

اگر فقط line count معیار باشد، نمی‌توان نتیجه گرفت نسخه SOLID «کوچک‌تر» است؛ چون در این پروژه افزودن Cash پس از Refactoring حتی 3 insertion بیشتر دارد. اما معیار معماری مهم‌تر چنین است:

#### قبل از SOLID


</div>

<div dir="ltr" align="left">

```text
Add Cash
   ↓
Open PaymentProcessor.process()
   ↓
Edit existing if/elif dispatch
   ↓
Central payment algorithm changes
```

</div>

<div dir="rtl" align="right">


#### بعد از SOLID


</div>

<div dir="ltr" align="left">

```text
Add Cash
   ↓
Add CashStrategy
   ↓
Register strategy
   ↓
PaymentProcessor.process() remains unchanged
```

</div>

<div dir="rtl" align="right">


بنابراین اثر اصلی SOLID در این آزمایش کاهش modification pressure روی منطق پایدار است.

### محدودیت OCP در نسخه نهایی

نسخه دوم هنوز برای ثبت strategy جدید، تابع `build_payment_strategies()` را ویرایش می‌کند. بنابراین معماری را نمی‌توان «کاملاً بدون modification» دانست؛ بلکه dispatch algorithm بسته به تغییر شده و wiring هنوز صریح است. برای پروژه آموزشی کوچک این trade-off قابل قبول است و از ایجاد framework/registry پیچیده جلوگیری می‌کند.

---

# بخش یازدهم — ارزیابی عملکرد OpenCode

## 27. OpenCode چه بخش‌هایی را به‌درستی تحلیل کرد؟

بر اساس خروجی‌های Agent و implementation نهایی، موارد زیر به‌درستی شناسایی یا پیشنهاد شدند:

تشخیص این‌که `OrderService` مسئولیت‌های متعددی دارد و باید به orchestrator سبک‌تری تبدیل شود؛ شناسایی زنجیره `if/elif` در `PaymentProcessor` به‌عنوان مشکل توسعه روش‌های پرداخت؛ پیشنهاد Strategy برای payment؛ شناسایی conditional chain در Discount و پیشنهاد Ruleهای مستقل؛ تشخیص مشکل رفتاری `BundleOrder` و ارتباط آن با substitutability؛ تشخیص مشکل `SmsOnlyNotifier` که متدهای غیرقابل پشتیبانی به ارث می‌برد؛ شناسایی concrete construction در `OrderService` و پیشنهاد constructor injection؛ پیشنهاد composition root در `main.py`؛ توجه به حفظ اولویت ruleهای تخفیف و رفتار paymentهای قبلی.

این بخش‌ها مستقیماً با ساختار نهایی کد و خروجی‌های baseline/refactored قابل بررسی‌اند.

---

## 28. در کدام قسمت‌ها پاسخ Agent نیاز به اصلاح داشت؟

چند نمونه مهم:

### 28.1 over-classification در SOLID analysis

Agent در تحلیل اولیه direct property access را DIP و monolithic بودن PaymentProcessor را ISP در نظر گرفت. این دسته‌بندی‌ها اصلاح شدند تا smell و violation از هم تفکیک شوند.

### 28.2 Refactoring غیرضروری Customer

استخراج `Wallet/PaymentMethod` از `Customer` صرفاً به دلیل وجود fieldهای payment پیشنهاد شده بود. این پیشنهاد رد شد، چون چند data field به‌تنهایی SRP violation را ثابت نمی‌کند و برای هدف آزمایش scope اضافی ایجاد می‌کرد.

### 28.3 اشکال در dependency order Plan

Step اول Plan به کلاس‌هایی وابسته بود که قرار بود Step بعد ساخته شوند. ترتیب plan نیاز به بازبینی داشت.

### 28.4 backward compatibility بیش از نیاز

default ساختن concrete strategy/rule داخل componentها پیشنهاد شد؛ این تصمیم با هدف composition root تعارض نسبی داشت.

### 28.5 طراحی بیش از حد انتزاعی در برخی قراردادها

نام‌های یکسان برای Protocol/concrete، `get_*` wrapperها و `customer_data: dict` مواردی بودند که در review انسانی به‌عنوان پیچیدگی یا typing ضعیف‌تر مطرح شدند.

### 28.6 Verification ناقص با demo

Agent در Plan گفته بود هر سه payment قبلی با اجرای demo تأیید می‌شوند، در حالی که demo اصلی PayPal و Bitcoin را واقعاً process نمی‌کرد. بنابراین smoke-test مستقیم لازم بود.

در مجموع، Agent جهت کلی معماری را خوب پیدا کرد، اما نتیجه زمانی قابل اعتمادتر شد که Promptها دقیق‌تر شدند و خروجی آن با code review انسانی بررسی شد.

---

## 29. بهترین Promptهای استفاده‌شده چه ویژگی‌ای داشتند؟

Promptهای مؤثر این آزمایش چند ویژگی مشترک داشتند:

scope دقیق، مثلاً فقط `02-Applied-OOD-Principles`؛ تفکیک «تحلیل» از «ویرایش»؛ ذکر صریح اینکه Cash هنوز نباید اضافه شود؛ درخواست evidence شامل file/class/method؛ درخواست حفظ رفتارهای قبلی؛ درخواست minimal refactoring و جلوگیری از overengineering؛ تعیین approval gate.

نمونه‌ی Prompt مؤثر برای تحلیل:


</div>

<div dir="ltr" align="left">

```text
Analyze SRP, OCP, LSP, ISP and DIP separately.
For every confirmed violation give the exact file, class/method,
concrete evidence, practical consequence and minimal refactoring.
Separate design smells from actual SOLID violations.
Do not modify files and do not add cash yet.
```

</div>

<div dir="rtl" align="right">


نمونه‌ی Prompt مؤثر برای Plan:


</div>

<div dir="ltr" align="left">

```text
Use the solid-review Skill.
Create a minimal ordered refactoring plan for the confirmed violations.
Preserve credit_card, paypal and bitcoin behavior and discount priority.
Keep OrderService as an orchestrator.
Do not implement anything until I approve the plan.
```

</div>

<div dir="rtl" align="right">


نمونه‌ی Prompt مؤثر برای افزودن Cash پس از SOLID:


</div>

<div dir="ltr" align="left">

```text
Add the same cash payment capability using the existing extension points.
Do not add an if/elif branch to PaymentProcessor.
Do not redesign the architecture.
List changed existing files and new classes before implementation.
```

</div>

<div dir="rtl" align="right">


در مقابل، Prompt عمومی مانند «SOLID problems را fix کن» کنترل کافی روی scope، رفتار و معیار قبول/رد نمی‌دهد.

---

## 30. طراحی Skill چه تأثیری بر کیفیت پاسخ‌ها داشت؟

تأثیر اصلی Skill این بود که خطاهای تحلیل اولیه به ruleهای پایدار تبدیل شدند. برای مثال Skill صریحاً می‌گوید:

direct property access به‌تنهایی DIP نیست؛ large class به‌تنهایی SRP/ISP را ثابت نمی‌کند؛ data-rich entity به‌تنهایی SRP violation نیست؛ برای هر finding باید evidence و location واقعی ارائه شود؛ implementation بدون approval انجام نشود.

در عمل، Skill قرار نبود جواب SOLID را از قبل به Agent بدهد؛ بیشتر نقش یک چارچوب تحلیل را داشت تا پاسخ‌ها قابل پیگیری و بازبینی باشند و Agent برای هر ادعا به بخش مشخصی از کد اشاره کند.

با این حال، Skill جای code review را نگرفت. باقی‌ماندن برخی compromiseها در کد نهایی و تناقض کوچک Constraint مربوط به registry نشان می‌دهد حتی یک Skill خوب هم تضمین‌کننده design بی‌نقص نیست.

---

## 31. اگر آزمایش را دوباره انجام دهم، چه چیزی را تغییر می‌دهم؟

در اجرای مجدد، این تغییرات را اعمال می‌کنم:

از ابتدا `__pycache__/` و `*.pyc` را در `.gitignore` قرار می‌دهم تا تاریخچه و آمار diff آلوده نشوند؛ قبل از Build، Plan نهایی را به یک فایل مستقل مثل `REFACTORING_PLAN.md` ذخیره می‌کنم تا تفاوت Plan اولیه، اصلاحات انسانی و Plan نهایی دقیق‌تر قابل ردیابی باشد؛ همه sessionهای موفق OpenCode را همان لحظه export می‌کنم؛ در repository فعلی فقط session اولیه شامل خطاهای 403 موجود است؛ به جای اتکا به demo، از ابتدا چند تست/Smoke test مستقل برای credit card، PayPal، Bitcoin، unknown method، discount priority و Bundle می‌نویسم؛ بعد از Plan اصلاح‌شده، یک review صریح انجام می‌دهم تا اطمینان حاصل شود مواردی مثل default concrete builder، `customer_data: dict` و protocol naming واقعاً قبل از Build اصلاح شده‌اند؛ در Skill، Constraint تکراری مربوط به registry را حذف می‌کنم؛ قرارداد `ReceiptFormatter` را با استفاده واقعی `OrderService` هماهنگ می‌کنم؛ در وضعیت فعلی Protocol فقط `format()` را تعریف می‌کند در حالی که `OrderService` روی dependency خود `print()` را صدا می‌زند.

این موارد دقیقاً از مشکلات واقعی مشاهده‌شده در این آزمایش استخراج شده‌اند، نه از توصیه‌های عمومی.

---

# بخش دوازدهم — ارزیابی کیفیت خروجی نهایی

## 32. نقاط قوت نسخه Refactorشده

`OrderService` دیگر concrete dependencyها را نمی‌سازد؛ validation و receipt از workflow اصلی جدا شده‌اند؛ payment behavior به Strategyهای مستقل منتقل شده است؛ discount ruleها مستقل شده و ترتیب قبلی حفظ شده است؛ `BundleOrder` دیگر inheritance معیوب ندارد و total واقعی تولید می‌کند؛ `SmsOnlyNotifier` فقط operation قابل پشتیبانی خود را ارائه می‌کند؛ Cash بدون تغییر `PaymentProcessor.process()` اضافه شده است؛ خروجی Order 101 قبل و بعد برابر باقی مانده است؛ هر چهار payment method در smoke-test نهایی کار می‌کنند.

## 33. محدودیت‌ها و موارد قابل بهبود

test suite خودکار در نسخه تحویلی وجود ندارد؛ برخی abstractionها از حداقل لازم پیچیده‌ترند؛ default builderها بخشی از concrete knowledge را داخل Payment/Discount نگه داشته‌اند؛ `PaymentStrategy` از dictionary استفاده می‌کند که type safety کمتری از domain object دارد؛ `ports.py` هم contract و هم بعضی data classها را در خود نگه می‌دارد که separation تمیزتری می‌تواند داشته باشد؛ Protocol `ReceiptFormatter` با متدی که `OrderService` واقعاً فراخوانی می‌کند کاملاً هم‌راستا نیست؛ فایل‌های bytecode در Git track شده‌اند و باید در آینده حذف شوند.

این محدودیت‌ها نتیجه اصلی آزمایش را از بین نمی‌برند، اما باعث می‌شوند ادعا نشود که نسخه دوم «معماری کامل و بی‌نقص» است.

---

# بخش سیزدهم — شواهد و قابلیت بازتولید

## 34. فایل‌های Evidence

| فایل | کاربرد |
|---|---|
| `evidence/original-baseline.txt` | خروجی پروژه پیش از Refactoring |
| `evidence/01-cash-changes.diff` | diff مرحله Cash در نسخه اول |
| `evidence/02-after-solid.txt` | خروجی نسخه SOLID پیش از Cash |
| `evidence/02-cash-changes.diff` | diff Cash در نسخه Refactorشده |
| `evidence/source-only-stats.txt` | آمار source-only برای مقایسه منصفانه |
| `evidence/final-verification.txt` | اجرای نهایی دو Demo و smoke-test paymentها |
| `evidence/git-history.txt` | تاریخچه checkpointهای Git |
| `evidence/opencode-sessions/session-01.json` | session export موجود از OpenCode؛ شامل تلاش‌های اولیه مدل و خطاهای 403 |

---

## 35. دستورات اجرای نسخه‌ها

### نسخه بدون SOLID


</div>

<div dir="ltr" align="left">

```powershell
cd .\01-Without-OOD-Principles
python -m store.main
```

</div>

<div dir="rtl" align="right">


### نسخه SOLID


</div>

<div dir="ltr" align="left">

```powershell
cd .\02-Applied-OOD-Principles
python -m store.main
```

</div>

<div dir="rtl" align="right">


---

# بخش چهاردهم — نتیجه‌گیری

## 36. جمع‌بندی نهایی

در نسخه اولیه، برای اضافه‌کردن یک روش پرداخت جدید مجبور بودم مستقیماً `PaymentProcessor.process()` را تغییر بدهم و یک شاخه دیگر به زنجیره `if/elif` اضافه کنم. بررسی همان نسخه چند مشکل دیگر را هم روشن کرد؛ از جمله تمرکز چند مسئولیت در `OrderService`، شرط‌های ثابت Discount، inheritance نامناسب `BundleOrder`، interface بزرگ Notification و ساخت مستقیم dependencyهای concrete در سرویس سطح بالا.

پس از Refactoring، مسئولیت‌ها بهتر تفکیک شدند، `OrderService` نقش orchestrator گرفت، Payment بر اساس Strategy کار کرد، Discount بر اساس Ruleها توسعه‌پذیر شد، Bundle با composition رفتار صحیح پیدا کرد و dependencyها از Composition Root تزریق شدند.

مقایسه Cash نتیجه جالبی داشت: تعداد فایل‌ها و حتی تعداد خطوط تغییرکرده در نسخه SOLID کمتر نشد. در نسخه اولیه `14+ / 2-` و در نسخه SOLID `17+ / 2-` ثبت شد. با این حال تفاوت معماری مهم این است که در حالت دوم برای Cash منطق مرکزی `PaymentProcessor.process()` تغییر نکرد و behavior جدید در کلاس مستقلی قرار گرفت. بنابراین SOLID در این مثال بیشتر از اینکه حجم کدنویسی را کاهش دهد، محل اثر تغییر و coupling را محدود کرد.

از طرف دیگر، OpenCode برای پیدا کردن مسیر کلی Refactoring و ساخت Plan کمک زیادی کرد، اما تحلیل اولیه‌اش چند دسته‌بندی اشتباه داشت و خود Plan هم بدون بازبینی قابل اجرا نبود. Skill سفارشی باعث شد تحلیل‌ها منظم‌تر و قابل بررسی‌تر شوند، ولی همچنان code review انسانی لازم بود. تجربه این آزمایش برای من این بود که AI Coding Agent زمانی بیشترین ارزش را دارد که نقش دستیار تحلیل و اجرا را داشته باشد، نه اینکه تصمیم‌های طراحی بدون بررسی به آن واگذار شوند.

---

## 37. چک‌لیست تطابق با صورت آزمایش

موارد انجام‌شده در این آزمایش شامل دو نسخه مستقل از پروژه اولیه ایجاد شد؛ Cash ابتدا روی نسخه بدون SOLID اضافه شد؛ تمام فایل‌های تغییرکرده در مرحله اول ثبت و مقایسه شدند؛ هر پنج اصل SRP، OCP، LSP، ISP و DIP تحلیل شدند؛ برای موارد نقض، علت، روش اصلاح و دلیل انتخاب راهکار توضیح داده شد؛ Skill اختصاصی برای تحلیل SOLID طراحی شد؛ هدف Skill، اطلاعاتی که به Agent می‌دهد و دلیل ساختار آن توضیح داده شد؛ Plan قبل از Refactoring تهیه و بازبینی شد؛ موارد نیازمند اصلاح در تحلیل و Plan Agent مستند شدند؛ Refactoring نسخه دوم در checkpoint جدا ثبت شد؛ Cash پس از Refactoring دوباره اضافه شد؛ تغییرات Cash در دو نسخه به‌صورت کمی و کیفی مقایسه شدند؛ عملکرد OpenCode، خطاهای آن، Promptهای مؤثر و اثر Skill ارزیابی شدند؛ پیشنهادهای مشخص برای اجرای بهتر آزمایش در تکرار بعدی ارائه شد؛ خروجی‌ها و diffهای اصلی در پوشه `evidence` نگهداری شده‌اند است.


</div>
