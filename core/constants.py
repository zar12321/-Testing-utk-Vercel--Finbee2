# =====================================================
# APPLICATION
# =====================================================

APP_NAME = "FinBee"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "Personal Finance Management Platform"
)

DEBUG = False


# =====================================================
# TRANSACTION
# =====================================================

TRANSACTION_TYPE_INCOME = "income"
TRANSACTION_TYPE_EXPENSE = "expense"
TRANSACTION_TYPE_TOPUP = "topup"

SUPPORTED_TRANSACTION_TYPES = [
    TRANSACTION_TYPE_INCOME,
    TRANSACTION_TYPE_EXPENSE,
    TRANSACTION_TYPE_TOPUP
]


# =====================================================
# CATEGORY
# =====================================================

DEFAULT_CATEGORY = "Other"

CATEGORY_TOPUP = "Topup"
CATEGORY_SALARY = "Salary"
CATEGORY_ALLOWANCE = "Allowance"
CATEGORY_FOOD = "Food"
CATEGORY_TRANSPORT = "Transport"
CATEGORY_BILLS = "Bills"
CATEGORY_SHOPPING = "Shopping"
CATEGORY_EDUCATION = "Education"
CATEGORY_HEALTH = "Health"
CATEGORY_ENTERTAINMENT = "Entertainment"

SUPPORTED_CATEGORIES = [
    CATEGORY_TOPUP,
    CATEGORY_SALARY,
    CATEGORY_ALLOWANCE,
    CATEGORY_FOOD,
    CATEGORY_TRANSPORT,
    CATEGORY_BILLS,
    CATEGORY_SHOPPING,
    CATEGORY_EDUCATION,
    CATEGORY_HEALTH,
    CATEGORY_ENTERTAINMENT,
    DEFAULT_CATEGORY
]


# =====================================================
# PAYMENT
# =====================================================

DEFAULT_PAYMENT_METHOD = "Unknown"


# =====================================================
# IMPORT FILE
# =====================================================

SUPPORTED_IMPORT_EXTENSIONS = [
    ".csv",
    ".xlsx",
    ".xls"
]

MAX_IMPORT_FILE_SIZE_MB = 10


# =====================================================
# AI
# =====================================================

AI_PROVIDER_GEMINI = "Gemini"
AI_PROVIDER_OPENROUTER = "OpenRouter"
AI_PROVIDER_GROQ = "Groq"
AI_PROVIDER_OLLAMA = "Ollama Local"

SUPPORTED_AI_PROVIDERS = [
    AI_PROVIDER_GEMINI,
    AI_PROVIDER_OPENROUTER,
    AI_PROVIDER_GROQ,
    AI_PROVIDER_OLLAMA
]

DEFAULT_AI_PROVIDER = AI_PROVIDER_GEMINI

FINANCIAL_AI_SYSTEM_PROMPT = """
Kamu adalah FinBee AI Assistant.

Kamu hanya membantu pengguna terkait:

- Keuangan pribadi
- Pengeluaran
- Pemasukan
- Tabungan
- Budgeting
- Cashflow
- Transaksi
- Analisis data keuangan
- Prediksi keuangan
- Insight dari dashboard FinBee

Kamu memiliki akses terhadap data transaksi,
hasil analisis, dashboard, dan prediksi milik pengguna.

ATURAN PENTING:

1. Jika pertanyaan berhubungan dengan data keuangan pengguna,
gunakan data yang diberikan sebagai sumber utama jawaban.

2. Jika data yang tersedia tidak cukup,
jelaskan keterbatasan data dan minta informasi tambahan.

3. Jika pertanyaan masih berkaitan dengan edukasi keuangan umum,
kamu boleh menjawab secara informatif.

4. Jika pertanyaan sama sekali tidak berkaitan dengan keuangan,
transaksi, budgeting, investasi, tabungan,
atau fitur FinBee, maka tolak dengan sopan.

Contoh:

User:
"Siapa presiden Indonesia?"

Jawaban:
"Maaf, saya dirancang untuk membantu analisis dan pengelolaan keuangan pada FinBee sehingga saya tidak dapat membantu pertanyaan tersebut."

User:
"Bagaimana cara menghemat uang bulanan?"

Jawaban:
Boleh dijawab.

User:
"Berapa total pengeluaran saya bulan ini?"

Jawaban:
Gunakan data yang tersedia.

Gunakan bahasa Indonesia yang profesional,
ramah, dan mudah dipahami.
""".strip()


# =====================================================
# PREDICTION
# =====================================================

MIN_MONTHS_FOR_REGRESSION = 3

PREDICTION_METHOD_AVERAGE = (
    "Rata-rata pengeluaran bulanan"
)

PREDICTION_METHOD_LINEAR_REGRESSION = (
    "Linear Regression sederhana"
)


# =====================================================
# DASHBOARD
# =====================================================

DEFAULT_TOP_TRANSACTION_LIMIT = 5


# =====================================================
# DATE FORMAT
# =====================================================

DEFAULT_DATE_FORMAT = "%Y-%m-%d"

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_MONTH_FORMAT = "%Y-%m"

SUPPORTED_DATE_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%Y/%m/%d",
    "%Y-%m-%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S"
]


# =====================================================
# CURRENCY
# =====================================================

CURRENCY_SYMBOL = "Rp"


# =====================================================
# VALIDATION
# =====================================================

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

MAX_NAME_LENGTH = 100
MAX_LOGIN_IDENTIFIER_LENGTH = 50


# =====================================================
# PAGINATION
# =====================================================

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# =====================================================
# SESSION
# =====================================================

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24