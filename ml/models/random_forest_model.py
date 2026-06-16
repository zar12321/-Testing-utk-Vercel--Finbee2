# ml/models/random_forest_model.py

from sklearn.ensemble import (
    RandomForestRegressor
)


def train_random_forest(
    X_train,
    y_train
):

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    return model