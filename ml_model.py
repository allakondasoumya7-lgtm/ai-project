import numpy as np
from sklearn.linear_model import LinearRegression


def predict_score(
    current_score,
    study_hours,
    difficulty
):

    training_X = np.array([
        [40, 2, 9],
        [45, 3, 8],
        [50, 4, 7],
        [55, 5, 7],
        [60, 5, 6],
        [65, 6, 5],
        [70, 6, 5],
        [75, 7, 4],
        [80, 8, 3],
        [90, 9, 2]
    ])

    training_y = np.array([
        43,
        50,
        56,
        61,
        66,
        71,
        76,
        81,
        87,
        94
    ])

    model = LinearRegression()

    model.fit(
        training_X,
        training_y
    )

    X = np.array([
        [
            current_score,
            study_hours,
            difficulty
        ]
    ])

    prediction = model.predict(X)[0]

    return round(
        max(
            0,
            min(
                100,
                prediction
            )
        ),
        2
    )
