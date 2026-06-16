# ml/features/feature_engineering.py

import pandas as pd


def create_time_series_features(
    df: pd.DataFrame
):
    """
    Membuat fitur forecasting
    dari dataset pengeluaran harian.

    Input:
    -----------------------
    date
    amount

    Output:
    -----------------------
    date
    amount
    lag_1
    lag_3
    lag_7
    lag_14
    lag_30
    rolling_mean_7
    rolling_mean_14
    rolling_mean_30
    rolling_std_7
    rolling_std_30
    day_of_week
    month
    day_of_month
    is_weekend
    """

    if df.empty:

        return df

    df = df.copy()

    # =====================================
    # SORT
    # =====================================

    df = df.sort_values(
        "date"
    ).reset_index(
        drop=True
    )

    # =====================================
    # PASTIKAN DATETIME
    # =====================================

    df["date"] = pd.to_datetime(
        df["date"]
    )

    # =====================================
    # LAG FEATURES
    # =====================================

    lag_days = [
        1,
        3,
        7,
        14,
        30
    ]

    for lag in lag_days:

        df[
            f"lag_{lag}"
        ] = df["amount"].shift(
            lag
        )

    # =====================================
    # ROLLING MEAN
    # =====================================

    rolling_windows = [
        7,
        14,
        30
    ]

    for window in rolling_windows:

        df[
            f"rolling_mean_{window}"
        ] = (
            df["amount"]
            .shift(1)
            .rolling(window)
            .mean()
        )

    # =====================================
    # ROLLING STD
    # =====================================

    std_windows = [
        7,
        30
    ]

    for window in std_windows:

        df[
            f"rolling_std_{window}"
        ] = (
            df["amount"]
            .shift(1)
            .rolling(window)
            .std()
        )

    # =====================================
    # DATE FEATURES
    # =====================================

    df["day_of_week"] = (
        df["date"]
        .dt.dayofweek
    )

    df["day_of_month"] = (
        df["date"]
        .dt.day
    )

    df["month"] = (
        df["date"]
        .dt.month
    )

    # =====================================
    # WEEKEND FLAG
    # =====================================

    df["is_weekend"] = (
        df["day_of_week"]
        >= 5
    ).astype(int)

    # =====================================
    # HAPUS NAN
    # =====================================

    df = df.dropna().reset_index(
        drop=True
    )

    return df