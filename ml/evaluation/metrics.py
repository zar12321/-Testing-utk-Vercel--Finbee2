# ml/evaluation/metrics.py

import numpy as np

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)


# ==========================================
# MAPE
# ==========================================

def calculate_mape(
    y_true,
    y_pred
):
    """
    Mean Absolute Percentage Error

    Menggunakan epsilon untuk
    menghindari division by zero.
    """

    y_true = np.array(
        y_true,
        dtype=float
    )

    y_pred = np.array(
        y_pred,
        dtype=float
    )

    epsilon = 1e-8

    return np.mean(
        np.abs(
            (y_true - y_pred)
            /
            np.maximum(
                np.abs(y_true),
                epsilon
            )
        )
    ) * 100


# ==========================================
# METRICS
# ==========================================

def calculate_metrics(
    y_true,
    y_pred
):
    """
    Menghitung seluruh metrik evaluasi.

    Return:
    {
        "r2": ...,
        "mse": ...,
        "rmse": ...,
        "mae": ...,
        "mape": ...
    }
    """

    mse = mean_squared_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(
        mse
    )

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    r2 = r2_score(
        y_true,
        y_pred
    )

    mape = calculate_mape(
        y_true,
        y_pred
    )

    return {
        "r2": round(
            float(r2),
            6
        ),

        "mse": round(
            float(mse),
            6
        ),

        "rmse": round(
            float(rmse),
            6
        ),

        "mae": round(
            float(mae),
            6
        ),

        "mape": round(
            float(mape),
            6
        )
    }