# ml/models/gradient_boosting_model.py

from sklearn.ensemble import (
    GradientBoostingRegressor
)


def train_gradient_boosting(
    X_train,
    y_train
):

    model = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    return model