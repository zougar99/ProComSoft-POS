# 🏪 ProComSoft POS - نظام إدارة المبيعات

> **Point of Sale** desktop application with AI-powered analytics, built with Python & PyQt5.

![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green?logo=qt)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## ✨ المميزات / Features

### 🛒 نظام نقاط البيع (POS)
| الميزة | Feature |
|--------|---------|
| ✅ بحث سريع عن المنتجات | Fast product search with auto-filter |
| ✅ إضافة منتجات إلى السلة بنقرة مزدوجة | Double-click to add to cart |
| ✅ خصم يدوي على الفاتورة | Manual discount per invoice |
| ✅ ضريبة تلقائية (20%) | Automatic 20% tax calculation |
| ✅ طرق دفع متعددة (نقدي، بطاقة، شيك، تحويل) | Multiple payment methods |
| ✅ إدارة المخزون تلقائياً | Auto inventory deduction on sale |

### 👥 إدارة العملاء (CRM)
- إضافة، تعديل، حذف العملاء مع كود تلقائي (`CUST-00001`)
- معلومات كاملة: الاسم، البريد، الهاتف، العنوان، المدينة
- تتبع الرصيد والحد الائتماني
- بحث وتصفية

### 📦 إدارة المنتجات
- أسماء متعددة اللغات (عربي / فرنسي / إنجليزي)
- كود تلقائي (`PROD-00001`) وباركود
- فئات المنتجات والوحدات
- تتبع المخزون مع حد أدنى وأقصى
- أسعار الشراء والبيع والضريبة

### 🤖 أدوات الذكاء الاصطناعي (AI Tools)
| الأداة | الوصف | الخوارزمية |
|--------|-------|-----------|
| 📈 **التنبؤ بالمبيعات** | توقع الإيرادات لـ30 يوم قادمة | Linear Regression |
| 📊 **تحليل البيانات** | ملخص النمو، أوقات الذروة، مقارنة الفترات | Statistical Analysis |
| 🏆 **أفضل المنتجات** | ترتيب حسب الإيرادات والكمية (آخر 90 يوم) | Aggregation |
| ⚠️ **إعادة الطلب** | كشف المنتجات تحت الحد الأدنى | Threshold Detection |
| 👥 **رؤى العملاء** | تحليل قيمة العملاء ومتوسط الفاتورة | RFM-like Scoring |

### 📊 لوحة التحكم (Dashboard)
- بطاقات إحصائية (قيمة المخزون، الفواتير المتأخرة، الطلبات)
- رسوم بيانية تفاعلية مع **matplotlib**
- جدول الفواتير المتأخرة
- قسم AI كامل مع 5 أدوات ذكية

### 🌐 دعم اللغات
- 🇸🇦 العربية (افتراضي)
- 🇬🇧 English
- 🇫🇷 Français

---

## 🚀 كيفية التشغيل / Quick Start

### المتطلبات / Prerequisites
- Python 3.10+
- pip (مدير الحزم)

### التثبيت والتشغيل
```bash
# 1. استنساخ المشروع
git clone https://github.com/your-org/POS-Desktop-App.git
cd POS-Desktop-App

# 2. تثبيت المتطلبات
pip install -r requirements.txt

# 3. تشغيل التطبيق
python main.py
```

### بيانات الدخول الافتراضية
| الحقل | القيمة |
|-------|--------|
| 👤 اسم المستخدم | `admin` |
| 🔑 كلمة المرور | `admin123` |
| 🎭 الصلاحية | Administrator |

---

## 📁 هيكل المشروع / Project Structure

```
POS-Desktop-App/
│
├── 🚀 main.py                      # نقطة الدخول الرئيسية
├── 📦 requirements.txt             # المكتبات المطلوبة
├── 📖 README.md                    # هذا الملف
│
├── 🐍 python_app/                  # الكود المصدري
│   │
│   ├── 🗄️ database/                # طبقة قاعدة البيانات
│   │   ├── __init__.py
│   │   ├── init.py                 # إدارة الاتصال (Singleton)
│   │   └── schema.py               # إنشاء 20 جدول (DDL)
│   │
│   ├── 🛠️ services/                # منطق الأعمال
│   │   ├── auth_service.py         # تسجيل الدخول + JWT
│   │   ├── user_service.py         # إدارة المستخدمين
│   │   ├── product_service.py      # إدارة المنتجات
│   │   ├── customer_service.py     # إدارة العملاء
│   │   ├── sale_service.py         # المبيعات + المخزون
│   │   ├── dashboard_service.py    # إحصائيات لوحة التحكم
│   │   └── ai_service.py           # 🤖 أدوات الذكاء الاصطناعي
│   │
│   ├── 🖥️ ui/                      # واجهة المستخدم (PyQt5)
│   │   ├── login_window.py         # 🔐 نافذة تسجيل الدخول
│   │   ├── main_window.py          # 🏠 النافذة الرئيسية
│   │   ├── pos_window.py           # 🛒 نقطة البيع
│   │   ├── customers_window.py     # 👥 إدارة العملاء
│   │   └── dashboard_window.py     # 📊 لوحة التحكم + رسوم بيانية
│   │
│   ├── 📂 modules/                  # وحدات القائمة الرئيسية
│   │   ├── sales/
│   │   │   └── invoices.py         # 📄 فواتير المبيعات
│   │   ├── crm/
│   │   │   └── customers.py        # 👤 العملاء
│   │   └── inventory/
│   │       └── products.py         # 📦 المنتجات
│   │
│   └── 🔧 utils/                    # أدوات مساعدة
│       ├── config.py               # الإعدادات
│       ├── i18n.py                 # 🌐 الترجمة (AR/EN/FR)
│       ├── security.py             # 🛡️ التوثيق
│       └── helpers.py              # 🔍 التحقق والتنسيق
│
├── 📂 data/                        # 🗄️ قاعدة البيانات (تُنشأ تلقائياً)
├── 📂 src/                         # (مشروع React قيد التطوير)
└── 📂 electron/                    # (تطبيق Electron قيد التطوير)
```

---

## 🗄️ قاعدة البيانات / Database Schema

20 جدول في SQLite:

| الجدول | الوصف |
|--------|-------|
| `users` | المستخدمين والصلاحيات |
| `customers` | العملاء |
| `products` | المنتجات |
| `categories` | فئات المنتجات |
| `warehouses` | المستودعات |
| `inventory_stock` | المخزون |
| `inventory_movements` | حركات المخزون |
| `sales` | فواتير المبيعات |
| `sale_items` | بنود الفواتير |
| `invoices` | الفواتير |
| `quotes` | عروض الأسعار |
| `quote_items` | بنود عروض الأسعار |
| `suppliers` | الموردين |
| `projects` | المشاريع |
| `project_followups` | متابعات المشاريع |
| `agenda_events` | الأحداث والمواعيد |
| `customer_addresses` | عناوين العملاء |
| `pricing_tariffs` | تعريفات الأسعار |
| `pricing_tariff_items` | بنود التعريفات |
| `audit_logs` | سجل التدقيق |

---

## 🤖 API Reference - AI Service

```python
from services.ai_service import AIService

# 📈 توقع الإيرادات لـ30 يوم
result = AIService.sales_forecast(days=30)
# Returns: { forecast_days, total_forecast, avg_daily_forecast, trend, confidence }

# 🏆 أفضل 10 منتجات مبيعاً
result = AIService.get_top_products(limit=10)
# Returns: [{ id, code, name, total_qty, total_revenue, sale_count }]

# ⏰ تحليل أوقات الذروة
result = AIService.analyze_peak_hours()
# Returns: [{ hour, count, revenue }]

# 👥 رؤى العملاء
result = AIService.get_customer_insights()
# Returns: [{ id, code, name, order_count, total_spent, avg_order_value }]

# ⚠️ اقتراح إعادة الطلب
result = AIService.suggest_reorder_products()
# Returns: [{ id, code, name, current_stock, min_stock, monthly_sales }]

# 📊 ملخص المبيعات مع النمو
result = AIService.get_sales_summary()
# Returns: { current, previous, growth_percent }
```

---

## 🛠️ التطوير / Development

### إضافة وحدة جديدة
1. أنشئ الخدمة في `python_app/services/`
2. أضف الواجهة في `python_app/ui/`
3. سجل الوحدة في `python_app/modules/`
4. أضف الجدول في `python_app/database/schema.py`

### إضافة لغة جديدة
1. أضف الترجمة في `python_app/utils/i18n.py`
2. أضف المفتاح لكل اللغات الموجودة

### أوامر مفيدة
```bash
# تشغيل مع إظهار الأخطاء
python main.py 2>&1

# مسح قاعدة البيانات وإعادة الإنشاء
rm -rf data/ && python main.py

# تشغيل في وضع بدون واجهة (اختبار)
python -c "import sys; sys.path.insert(0, 'python_app'); from database.init import init_database; init_database(); print('OK')"
```

---

## ❓ الأسئلة الشائعة / FAQ

### ❔ لا يشتغل التطبيق؟
```bash
pip install -r requirements.txt
python main.py
```
تأكد أنك في المجلد الصحيح (`POS-Desktop-App/`).

### ❔ الخطأ: `No module named 'PyQt5'`
```bash
pip install PyQt5
```

### ❔ نسيت كلمة السر؟
امسح المجلد `data/` وأعد تشغيل التطبيق:
```bash
Remove-Item -Recurse -Force data/  # Windows
rm -rf data/                        # Linux/Mac
python main.py
```
يعود الـ admin الافتراضي: `admin` / `admin123`

### ❔ كيف نضيف منتجات؟
1. سجل الدخول بـ `admin` / `admin123`
2. افتح **📦 المنتجات** من القائمة
3. استخدم خدمة `ProductService.create()`

---

## 📜 الرخصة / License

MIT License - استخدم، عدل، ووزع بحرية.

---

<div dir="rtl">

## 🤝 المساهمة / Contributing

نرحب بالمساهمات! يرجى فتح **Issue** أو **Pull Request**.

</div>
