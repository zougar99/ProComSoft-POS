# ProComSoft POS - نظام إدارة المبيعات

Point of Sale desktop application built with Python, PyQt5, and AI-powered analytics.

## Features

### Core POS
- **Point of Sale** - Fast checkout with product search, cart management, and multiple payment methods
- **Customer Management** - Full CRUD with address, contact, and credit limit tracking
- **Product Management** - Multi-language names (AR/FR/EN), barcode, categories, inventory tracking
- **Sales Invoices** - Complete sales history with filtering and search

### AI Tools (مدمجة)
- **Sales Forecasting** - Linear regression prediction for 30-day revenue forecast
- **Data Analysis** - Sales summary, growth metrics, peak hours analysis
- **Top Products** - Best-selling products ranked by revenue (last 90 days)
- **Reorder Suggestions** - Auto-detect products below minimum stock
- **Customer Insights** - Customer value analysis with order patterns

### Dashboard
- Real-time metrics (stock value, overdue invoices, orders)
- Interactive charts with matplotlib (revenue, profit, monthly orders)
- Overdue invoices monitoring

## Tech Stack

| Layer | Technology |
|-------|-----------|
| GUI | PyQt5 |
| Database | SQLite |
| AI/ML | NumPy (linear regression) |
| Charts | matplotlib |
| Auth | bcrypt + JWT |
| i18n | Arabic / English / French |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Default login: `admin` / `admin123`

## Project Structure

```
POS-Desktop-App/
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── python_app/
│   ├── database/              # Database layer (SQLite)
│   │   ├── init.py            # Connection singleton
│   │   └── schema.py          # Table creation DDL
│   ├── services/              # Business logic
│   │   ├── auth_service.py    # Authentication + JWT
│   │   ├── user_service.py    # User management
│   │   ├── product_service.py # Product CRUD
│   │   ├── customer_service.py# Customer CRUD
│   │   ├── sale_service.py    # Sales + inventory
│   │   ├── dashboard_service.py# Analytics
│   │   └── ai_service.py      # AI tools
│   ├── ui/                    # PyQt5 Windows
│   │   ├── login_window.py    # Login screen
│   │   ├── main_window.py     # Main window shell
│   │   ├── pos_window.py      # POS checkout
│   │   ├── customers_window.py# Customer management
│   │   └── dashboard_window.py# Dashboard + charts
│   ├── modules/               # Main window sub-modules
│   │   ├── sales/invoices.py
│   │   ├── crm/customers.py
│   │   └── inventory/products.py
│   └── utils/                 # Utilities
│       ├── config.py          # App configuration
│       ├── i18n.py            # Translations
│       ├── security.py        # Auth helpers
│       └── helpers.py         # Validators
└── data/                      # SQLite database (auto-created)
```

## AI Methods

The `AIService` class provides these AI-powered tools:

| Method | Description | Algorithm |
|--------|-------------|-----------|
| `sales_forecast(days)` | Predict future revenue | Linear regression |
| `get_top_products(limit)` | Best-selling products | Aggregation + sort |
| `analyze_peak_hours()` | Peak business hours | Time-based grouping |
| `get_customer_insights()` | Customer value analysis | RFM-like scoring |
| `suggest_reorder_products()` | Auto reorder detection | Threshold comparison |
| `get_sales_summary()` | Period-over-period growth | Comparative analysis |

## License

MIT
