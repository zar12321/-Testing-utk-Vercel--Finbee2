# ml/prediction/forecast_expense.py

import pandas as pd

from sqlalchemy.orm import Session

from ml.datasets.daily_expense_dataset import (
    build_daily_expense_dataset
)

from ml.datasets.feature_engineering import (
    create_time_series_features
)

from ml.models.gradient_boosting_model import (
    train_gradient_boosting
)


# ==========================================
# FORECAST EXPENSE
# ==========================================

def forecast_expense(
    db: Session,
    user_id: int,
    days: int = 30,
    category_id: int | None = None
):
    """
    Forecast pengeluaran user
    berdasarkan histori transaksi.

    Parameters
    ----------
    db : Session

    user_id : int

    days : int
        7 / 14 / 30

    category_id : int | None
        Filter subkategori

    Return
    ----------
    {
        "forecast_days": 30,
        "category_id": 5,
        "predictions": [...]
    }
    """

    # ======================================
    # BUILD DAILY DATASET
    # ======================================

    df_daily = (
        build_daily_expense_dataset(
            db=db,
            user_id=user_id,
            category_id=category_id
        )
    )

    print(df_daily.tail(20))

    print(
        "Jumlah hari:",
        len(df_daily)
    )

    print(
        "Hari amount > 0:",
        len(
            df_daily[
                df_daily["amount"] > 0
            ]
        )
    )

    print(
        "Persen nol:",
        round(
            (
                len(
                    df_daily[
                        df_daily["amount"] == 0
                    ]
                )
                /
                len(df_daily)
            ) * 100,
            2
        ),
        "%"
    )

    # ======================================
    # VALIDASI DATA
    # ======================================

    if df_daily.empty:

        raise ValueError(
            "Dataset pengeluaran kosong."
        )
    
    active_days = len(
        df_daily[
            df_daily["amount"] > 0
        ]
    )

    if active_days < 90:

        raise ValueError(
            (
                "Minimal diperlukan "
                "90 hari aktif transaksi "
                "untuk menggunakan "
                "fitur prediksi."
            )
        )

    # ======================================
    # FEATURE ENGINEERING
    # ======================================

    df_feature = (
        create_time_series_features(
            df_daily
        )
    )

    if df_feature.empty:

        raise ValueError(
            "Feature engineering gagal."
        )

    # ======================================
    # FEATURE & TARGET
    # ======================================

    feature_columns = [

        col

        for col
        in df_feature.columns

        if col not in [
            "date",
            "amount"
        ]
    ]

    X_train = df_feature[
        feature_columns
    ]

    y_train = df_feature[
        "amount"
    ]

    # ======================================
    # TRAIN MODEL
    # ======================================

    model = (
        train_gradient_boosting(
            X_train,
            y_train
        )
    )

    # ======================================
    # FUTURE DATAFRAME
    # ======================================

    future_df = (
        df_daily.copy()
    )

    predictions = []

    # ======================================
    # RECURSIVE FORECAST
    # ======================================

    for _ in range(days):

        feature_df = (
            create_time_series_features(
                future_df
            )
        )

        latest_row = (
            feature_df
            .iloc[-1:]
        )

        X_future = latest_row[
            feature_columns
        ]

        prediction = float(
            model.predict(
                X_future
            )[0]
        )

        prediction = max(
            prediction,
            0
        )

        next_date = (
            future_df["date"].max()
            +
            pd.Timedelta(days=1)
        )

        predictions.append(
            {
                "date":
                    next_date.strftime(
                        "%Y-%m-%d"
                    ),

                "predicted_amount":
                    round(
                        prediction,
                        2
                    )
            }
        )

        future_df.loc[
            len(future_df)
        ] = [
            next_date,
            prediction
        ]
    
    # ======================================
    # HISTORY 30 HARI TERAKHIR
    # ======================================

    history_df = (
        df_daily
        .tail(30)
        .copy()
    )

    history = []

    for _, row in history_df.iterrows():

        history.append(
            {
                "date":
                    row["date"].strftime(
                        "%Y-%m-%d"
                    ),

                "amount":
                    float(
                        row["amount"]
                    )
            }
        )

    # ======================================
    # RESPONSE
    # ======================================

    return {
        "forecast_days":
            days,

        "category_id":
            category_id,

        "history_days":
            len(df_daily),

        "history":
            history,

        "predictions":
            predictions
    }