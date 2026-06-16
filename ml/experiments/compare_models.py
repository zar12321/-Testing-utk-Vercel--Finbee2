# ml/experiments/compare_models.py

import pandas as pd

import json

import joblib

from pathlib import Path

from sklearn.model_selection import (
    train_test_split
)

from ml.datasets.daily_expense_dataset import (
    build_daily_expense_dataset
)

from ml.datasets.feature_engineering import (
    create_time_series_features
)

from ml.models.linear_regression_model import (
    train_linear_regression
)

from ml.models.random_forest_model import (
    train_random_forest
)

from ml.models.gradient_boosting_model import (
    train_gradient_boosting
)

from ml.models.xgboost_model import (
    train_xgboost
)

from ml.evaluation.metrics import (
    calculate_metrics
)


# ==========================================
# COMPARE MODELS
# ==========================================

def compare_models(
    db,
    user_id: int,
    save_path: str = (
        "D:/Studi Independen/Celerates/Final Project/FinBee/Taro ke Github Sendiri/[Testing utk Vercel] Finbee2/ml/results/model_comparison.csv"
    )
):

    # ======================================
    # BUILD DATASET
    # ======================================

    df_daily = build_daily_expense_dataset(
        db=db,
        user_id=user_id
    )

    if df_daily.empty:

        raise ValueError(
            "Dataset kosong."
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
            "Dataset feature kosong."
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

    X = df_feature[
        feature_columns
    ]

    y = df_feature[
        "amount"
    ]

    # ======================================
    # TRAIN TEST SPLIT
    # ======================================

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )

    # ======================================
    # TRAIN MODELS
    # ======================================

    linear_model = (
        train_linear_regression(
            X_train,
            y_train
        )
    )

    rf_model = (
        train_random_forest(
            X_train,
            y_train
        )
    )

    gb_model = (
        train_gradient_boosting(
            X_train,
            y_train
        )
    )

    xgb_model = (
        train_xgboost(
            X_train,
            y_train
        )
    )

    # ======================================
    # MODEL COLLECTION
    # ======================================

    models = {

        "Linear Regression":
            linear_model,

        "Random Forest":
            rf_model,

        "Gradient Boosting":
            gb_model,

        "XGBoost":
            xgb_model
    }

    # ======================================
    # EVALUATION
    # ======================================

    results = []

    for (
        model_name,
        model
    ) in models.items():

        y_pred = model.predict(
            X_test
        )

        metric_result = (
            calculate_metrics(
                y_test,
                y_pred
            )
        )

        results.append({

            "model":
                model_name,

            "r2":
                metric_result["r2"],

            "mse":
                metric_result["mse"],

            "rmse":
                metric_result["rmse"],

            "mae":
                metric_result["mae"],

            "mape":
                metric_result["mape"]
        })

    # ======================================
    # RESULT DATAFRAME
    # ======================================

    result_df = pd.DataFrame(
        results
    )

    result_df = (
        result_df
        .sort_values(
            by="rmse",
            ascending=True
        )
        .reset_index(
            drop=True
        )
    )

    # ======================================
    # SAVE ALL MODELS
    # ======================================

    model_dir = Path(
        "ml/saved_models"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        linear_model,
        model_dir / "linear_regression.pkl"
    )

    joblib.dump(
        rf_model,
        model_dir / "random_forest.pkl"
    )

    joblib.dump(
        gb_model,
        model_dir / "gradient_boosting.pkl"
    )

    joblib.dump(
        xgb_model,
        model_dir / "xgboost.pkl"
    )

    # ======================================
    # SAVE BEST MODEL
    # ======================================

    best_model_name = result_df.iloc[0][
        "model"
    ]

    best_model_map = {

        "Linear Regression":
            linear_model,

        "Random Forest":
            rf_model,

        "Gradient Boosting":
            gb_model,

        "XGBoost":
            xgb_model
    }

    best_model = best_model_map[
        best_model_name
    ]

    joblib.dump(
        best_model,
        model_dir / "best_model.pkl"
    )

    # ======================================
    # SAVE RESULT
    # ======================================

    print(result_df)

    print(
        "Jumlah baris:",
        len(result_df)
    )

    print(
        "Save ke:",
        save_path
    )
    result_df.to_csv(
        save_path,
        index=False
    )

    # ======================================
    # SAVE BEST MODEL INFO
    # ======================================

    best_info = {

        "best_model":
            best_model_name,

        "r2":
            float(
                result_df.iloc[0]["r2"]
            ),

        "mse":
            float(
                result_df.iloc[0]["mse"]
            ),

        "rmse":
            float(
                result_df.iloc[0]["rmse"]
            ),

        "mae":
            float(
                result_df.iloc[0]["mae"]
            ),

        "mape":
            float(
                result_df.iloc[0]["mape"]
            )
    }

    with open(
        "ml/results/best_model_info.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            best_info,
            f,
            indent=4
        )
    

    return result_df

if __name__ == "__main__":

    print(
        "COMPARE MODEL START"
    )

    if __name__ == "__main__":

        print(
            "COMPARE MODEL START"
        )

        from app.database.connection import (
            SessionLocal
        )

        db = SessionLocal()

        result = compare_models(
            db=db,
            user_id=36
        )

        print(result)

        db.close()