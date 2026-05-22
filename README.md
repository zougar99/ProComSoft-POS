# 🏪 ProComSoft POS - Desktop Application

> **Point of Sale** desktop application with AI-powered analytics, built with Python & PyQt5.

![Python](https://img.shields.io/badge/Python-3.14+-blue?logo=python)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green?logo=qt)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-orange)

---

## ✨ Features

### 🛒 Point of Sale (POS)
| Feature | Description |
|---------|------------|
| ✅ Fast product search | Real-time auto-filter while typing |
| ✅ Double-click to cart | Quick product addition |
| ✅ Manual discount | Per-invoice discount input |
| ✅ Auto tax calculation | 20% tax on subtotal |
| ✅ Multiple payments | Cash, Card, Check, Transfer |
| ✅ Auto inventory | Stock deducted on sale |

### 👥 Customer Management (CRM)
- Full CRUD with auto code generation (`CUST-00001`)
- Complete profile: name, email, phone, address, city
- Balance and credit limit tracking
- Search and filter

### 📦 Product Management
- Multi-language names
- Auto code (`PROD-00001`) and barcode support
- Categories and units
- Min/max stock tracking
- Buy/sell prices and tax rate

### 🤖 AI Tools
| Tool | Description | Algorithm |
|------|-------------|-----------|
| 📈 **Sales Forecast** | Predict revenue for next 30 days | Linear Regression |
| 📊 **Data Analysis** | Growth summary, peak hours | Statistical Analysis |
| 🏆 **Top Products** | Rank by revenue (last 90 days) | Aggregation |
| ⚠️ **Reorder** | Detect low-stock products | Threshold Detection |
| 👥 **Insights** | Customer value analysis | RFM-like Scoring |

### 📊 Dashboard
- Real-time metric cards (stock value, overdue invoices, orders)
- Interactive matplotlib charts
- Overdue invoices table
- Full AI section with 5 smart tools

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Setup
```bash
# 1. Clone the project
git clone https://github.com/zougar99/ProComSoft-POS.git
cd POS-Desktop-App

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python main.py
```

### Default Login
| Field | Value |
|-------|-------|
| 👤 Username | `admin` |
| 🔑 Password | `admin123` |
| 🎭 Role | Administrator |

---

## 📁 Project Structure

```
POS-Desktop-App/
│
├── 🚀 main.py                      # Entry point
├── 📦 requirements.txt             # Dependencies
├── 📖 README.md                    # This file
│
├── 🐍 python_app/                  # Source code
│   ├── 🗄️ database/
│   │   ├── init.py                 # Connection singleton
│   │   └── schema.py              # 20 tables DDL
│   │
│   ├── 🛠️ services/
│   │   ├── auth_service.py         # Login + JWT
│   │   ├── user_service.py         # User management
│   │   ├── product_service.py      # Product CRUD
│   │   ├── customer_service.py     # Customer CRUD
│   │   ├── sale_service.py         # Sales + inventory
│   │   ├── dashboard_service.py    # Analytics
│   │   └── ai_service.py           # 🤖 AI tools
│   │
│   ├── 🖥️ ui/
│   │   ├── login_window.py         # 🔐 Login
│   │   ├── main_window.py          # 🏠 Main window
│   │   ├── pos_window.py           # 🛒 POS checkout
│   │   ├── customers_window.py     # 👥 Customer mgmt
│   │   └── dashboard_window.py     # 📊 Dashboard
│   │
│   ├── 📂 modules/
│   │   ├── sales/invoices.py       # 📄 Invoices
│   │   ├── crm/customers.py        # 👤 Customers
│   │   └── inventory/products.py   # 📦 Products
│   │
│   └── 🔧 utils/
│       ├── config.py               # Settings
│       ├── i18n.py                 # 🌐 i18n
│       ├── security.py             # 🛡️ Auth helper
│       └── helpers.py              # 🔍 Validators
│
└── 📂 data/                        # SQLite DB (auto)
```

---

## 🤖 AI Service API

```python
from services.ai_service import AIService

# 📈 Forecast revenue
result = AIService.sales_forecast(days=30)
# { forecast_days, total_forecast, avg_daily_forecast, trend, confidence }

# 🏆 Top products
result = AIService.get_top_products(limit=10)
# [{ id, code, name, total_qty, total_revenue, sale_count }]

# ⏰ Peak hours analysis
result = AIService.analyze_peak_hours()
# [{ hour, count, revenue }]

# 👥 Customer insights
result = AIService.get_customer_insights()
# [{ id, code, name, order_count, total_spent, avg_order_value }]

# ⚠️ Reorder suggestions
result = AIService.suggest_reorder_products()
# [{ id, code, name, current_stock, min_stock, monthly_sales }]

# 📊 Sales summary
result = AIService.get_sales_summary()
# { current, previous, growth_percent }
```

---

## 🗄️ Database Tables (20)

| Table | Description |
|-------|-------------|
| `users` | User accounts & roles |
| `customers` | Customers |
| `products` | Products |
| `categories` | Categories |
| `warehouses` | Warehouses |
| `inventory_stock` | Stock |
| `inventory_movements` | Stock movements |
| `sales` | Sales invoices |
| `sale_items` | Invoice items |
| `invoices` | Invoices |
| `quotes` | Quotes |
| `quote_items` | Quote items |
| `suppliers` | Suppliers |
| `projects` | Projects |
| `project_followups` | Project follow-ups |
| `agenda_events` | Calendar events |
| `customer_addresses` | Customer addresses |
| `pricing_tariffs` | Price tariffs |
| `pricing_tariff_items` | Tariff items |
| `audit_logs` | Audit trail |

---

## 🛠️ Development

### Add a new module
1. Create service in `python_app/services/`
2. Create UI in `python_app/ui/`
3. Register in `python_app/modules/`
4. Add table to `python_app/database/schema.py`

### Add a new language
1. Add translations in `python_app/utils/i18n.py`
2. Add key for all existing languages

### Useful commands
```bash
# Run with debug output
python main.py 2>&1

# Reset database
Remove-Item -Recurse -Force data/  # Windows
rm -rf data/                        # Linux/Mac
python main.py
```

---

## ❓ FAQ

### ❔ App won't start?
```bash
pip install -r requirements.txt
python main.py
```
Make sure you're in the `POS-Desktop-App/` directory.

### ❔ `No module named 'PyQt5'`?
```bash
pip install PyQt5
```

### ❔ Forgot password?
Delete `data/` folder and restart:
```bash
Remove-Item -Recurse -Force data/  # Windows
python main.py
```
Default admin is restored: `admin` / `admin123`

### ❔ How to add products?
1. Login as `admin` / `admin123`
2. Open **📦 Products** from menu
3. Use `ProductService.create()`

---

## 📜 License

MIT License - Free to use, modify, and distribute.

---

## 🤝 Contributing

Pull requests and issues are welcome!
