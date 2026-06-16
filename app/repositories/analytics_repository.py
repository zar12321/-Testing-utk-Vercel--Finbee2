# app/database/analytics_repository.py

from sqlalchemy import text
from sqlalchemy.orm import Session


# =====================================================
# BUILD FILTER SQL
# =====================================================

def build_filter_query(
    query,
    params,
    filters
):

    if filters.get("category"):

        query += """
            AND transaction_type = :category
        """

        params["category"] = (
            filters["category"]
        )

    if filters.get("subcategory_id"):

        query += """
            AND category_id = :subcategory_id
        """

        params["subcategory_id"] = (
            filters["subcategory_id"]
        )

    if filters.get("month"):

        query += """
            AND EXTRACT(
                MONTH FROM tanggal_transaksi
            ) = :month
        """

        params["month"] = int(
            filters["month"]
        )

    if filters.get("year"):

        query += """
            AND EXTRACT(
                YEAR FROM tanggal_transaksi
            ) = :year
        """

        params["year"] = int(
            filters["year"]
        )

    if filters.get("period"):

        period_map = {
            "today": "0 days",
            "7days": "7 days",
            "30days": "30 days",
            "90days": "90 days",
            "365days": "365 days"
        }

        if filters["period"] in period_map:

            query += f"""
                AND tanggal_transaksi >=
                    CURRENT_DATE -
                    INTERVAL '{period_map[filters["period"]]}'
            """

    return query, params


# =====================================================
# LINE CHART
# CASHFLOW TREND
# =====================================================

def get_cashflow_trend(
    db: Session,
    user_id: int,
    filters: dict
):

    query = """
        SELECT
            DATE(tanggal_transaksi) AS date,

            SUM(
                CASE
                    WHEN transaction_type='income'
                    THEN amount
                    ELSE 0
                END
            ) AS income,

            SUM(
                CASE
                    WHEN transaction_type='expense'
                    THEN amount
                    ELSE 0
                END
            ) AS expense,

            SUM(
                CASE
                    WHEN transaction_type='topup'
                    THEN amount
                    ELSE 0
                END
            ) AS topup

        FROM transactions

        WHERE user_id = :user_id
    """

    params = {
        "user_id": user_id
    }

    query, params = build_filter_query(
        query,
        params,
        filters
    )

    print("FILTERS =", filters)
    print("PARAMS =", params)

    query += """
        GROUP BY DATE(tanggal_transaksi)
        ORDER BY DATE(tanggal_transaksi)
    """

    result = db.execute(
        text(query),
        params
    )

    return [
        dict(row._mapping)
        for row in result
    ]


# =====================================================
# BAR CHART
# BREAKDOWN
# =====================================================

def get_breakdown_chart(
    db: Session,
    user_id: int,
    filters: dict
):

    params = {
        "user_id": user_id
    }

    # =====================================
    # LEVEL 1
    # BELUM PILIH KATEGORI
    # TAMPILKAN:
    # expense | income | topup
    # =====================================

    if (
        not filters.get("category")
        and not filters.get("subcategory_id")
    ):

        query = """
            SELECT
                case 
                    when transaction_type = 'expense'
                        then 'Pengeluaran'
                    when transaction_type = 'income'
                        then 'Pemasukan'
                    when transaction_type = 'topup'
                        then 'Topup'

                    else transaction_type
                
                end as label,
                sum(amount) as total

            FROM transactions

            WHERE user_id = :user_id
        """

        query, params = build_filter_query(
            query,
            params,
            filters
        )

        query += """
            GROUP BY transaction_type
            ORDER BY total DESC
        """

    # =====================================
    # LEVEL 2
    # SUDAH PILIH KATEGORI
    # BELUM PILIH SUBKATEGORI
    # TAMPILKAN:
    # Food | Transport | dll
    # =====================================

    elif (
        filters.get("category")
        and not filters.get("subcategory_id")
    ):

        query = """
            SELECT
                c.category_name AS label,
                SUM(t.amount) AS total

            FROM transactions t

            JOIN categories c
                ON c.category_id =
                t.category_id

            WHERE t.user_id = :user_id
        """

        query, params = build_filter_query(
            query,
            params,
            filters
        )

        query += """
            GROUP BY c.category_name
            ORDER BY total DESC
            LIMIT 10
        """

    # =====================================
    # LEVEL 3
    # SUDAH PILIH SUBKATEGORI
    # TAMPILKAN:
    # tujuan_transaksi
    # =====================================

    elif filters.get("subcategory_id"):

        query = """
            SELECT
                tujuan_transaksi AS label,
                SUM(amount) AS total

            FROM transactions

            WHERE user_id = :user_id
        """

        query, params = build_filter_query(
            query,
            params,
            filters
        )

        query += """
            GROUP BY tujuan_transaksi
            ORDER BY total DESC
            LIMIT 10
        """

    result = db.execute(
        text(query),
        params
    )

    return [
        dict(row._mapping)
        for row in result
    ]

# ===================================
# GET BREAKDOWN PREVIEW
# ===================================
def get_breakdown_preview(
    db: Session,
    user_id: int,
    filters: dict
):

    params = {
        "user_id": user_id
    }

    # ===================================
    # MODE 1
    # CATEGORY -> TUJUAN TRANSAKSI
    # ===================================

    if not filters.get("subcategory_id"):

        query = """
            SELECT
                c.category_name AS parent,

                t.tujuan_transaksi AS label,

                SUM(t.amount) AS total

            FROM transactions t

            JOIN categories c
                ON c.category_id =
                   t.category_id

            WHERE t.user_id = :user_id
        """

        query, params = build_filter_query(
            query,
            params,
            filters
        )

        query += """
            GROUP BY
                c.category_name,
                t.tujuan_transaksi

            ORDER BY
                c.category_name,
                total DESC
        """

    # ===================================
    # MODE 2
    # TUJUAN TRANSAKSI -> KETERANGAN
    # ===================================

    else:

        query = """
            SELECT
                tujuan_transaksi AS parent,

                COALESCE(
                    NULLIF(
                        keterangan,
                        ''
                    ),
                    'Tidak ada detail'
                ) AS label,

                SUM(amount) AS total

            FROM transactions

            WHERE user_id = :user_id
        """

        query, params = build_filter_query(
            query,
            params,
            filters
        )

        query += """
            GROUP BY
                tujuan_transaksi,
                label

            ORDER BY
                tujuan_transaksi,
                total DESC
        """

    result = db.execute(
        text(query),
        params
    ).fetchall()

    preview = {}

    for row in result:

        row = dict(
            row._mapping
        )

        parent = row["parent"]

        if parent not in preview:

            preview[parent] = []

        preview[parent].append(
            {
                "label": row["label"],
                "total": float(
                    row["total"]
                )
            }
        )

    return preview

# =====================================================
# PAYMENT ANALYTICS
# =====================================================

def get_payment_method_chart(
    db: Session,
    user_id: int,
    filters: dict
):

    query = """
        SELECT
            payment_method AS label,
            SUM(amount) AS total

        FROM transactions

        WHERE user_id = :user_id
    """

    params = {
        "user_id": user_id
    }

    query, params = build_filter_query(
        query,
        params,
        filters
    )

    query += """
        GROUP BY payment_method
        ORDER BY total DESC
    """

    result = db.execute(
        text(query),
        params
    )

    return [
        dict(row._mapping)
        for row in result
    ]