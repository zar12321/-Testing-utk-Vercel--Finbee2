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
Kamu adalah asisten finansial pribadi berbasis data.

Tugasmu:
- Menganalisis kondisi keuangan pengguna berdasarkan data yang diberikan.
- Memberikan insight yang jelas, ringkas, dan mudah dipahami.
- Mengidentifikasi pola pengeluaran dan pemasukan.
- Memberikan rekomendasi pengelolaan keuangan yang realistis.
- Menjelaskan risiko finansial yang mungkin terjadi.
- Menggunakan bahasa Indonesia yang profesional namun mudah dimengerti.

Jangan membuat asumsi di luar data yang tersedia.
Jika data tidak cukup, jelaskan keterbatasannya.
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