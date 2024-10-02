import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)


@app.route('/hyper-parameterTuning', methods=['POST'])
def hyperParameterTuning():
    data = request.get_json()
    X_train = pd.DataFrame(data.get('X_train'))
    X_test = pd.DataFrame(data.get('X_test'))
    y_train = pd.Series(data.get('y_train'))  # Convert to Series, not DataFrame
    y_test = pd.Series(data.get('y_test'))  # Convert to Series, not DataFrame
    model = data.get('model')

    # Call hyperparameter tuning function
    result = hyperparameter_tuning(model, X_train, y_train)

    return jsonify(result)


model_hyperparameters = {
    "LogisticRegression": {
        "C": [0.1, 1.0, 10.0],
        "solver": ["liblinear", "newton-cg", "lbfgs"],
        "max_iter": [50, 100, 200]
    },
    "KNeighborsClassifier": {
        "n_neighbors": [3, 5, 7, 9],
        "weights": ["uniform", "distance"],
        "algorithm": ["auto", "ball_tree", "kd_tree", "brute"]
    },
    "DecisionTreeClassifier": {
        "criterion": ["gini", "entropy"],
        "max_depth": [None, 5, 10, 20],
        "min_samples_split": [2, 5, 10, 15, 20]
    },
    "SVC": {
        "C": [0.1, 1.0, 3.0, 5.0, 10.0, 15.0],
        "kernel": ["linear", "poly", "rbf", "sigmoid"],
        "gamma": ["scale", "auto", 0.1, 0.25, 0.5, 0.75, 1.0]
    },
    "GaussianNB": {
        "var_smoothing": [1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4]
    },
    "RandomForestClassifier": {
        "n_estimators": [10, 25, 50, 75, 100, 125, 200],
        "criterion": ["gini", "entropy"],
        "max_depth": [None, 5, 10, 15, 20]
    },
    "GradientBoostingClassifier": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 0.2, 0.3, 0.4, 0.5],
        "max_depth": [3, 5, 7]
    },
    "AdaBoostClassifier": {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.1, 1.0],
        "algorithm": ["SAMME", "SAMME.R"]
    }
}

model_class = {
    "LogisticRegression": LogisticRegression,
    "KNeighborsClassifier": KNeighborsClassifier,
    "DecisionTreeClassifier": DecisionTreeClassifier,
    "GaussianNB": GaussianNB,
    "RandomForestClassifier": RandomForestClassifier,
    "GradientBoostingClassifier": GradientBoostingClassifier,
    "AdaBoostClassifier": AdaBoostClassifier,
    "SVC": SVC
}


def hyperparameter_tuning(model_name, X_train, y_train):
    hyperparameters = model_hyperparameters[model_name]
    model = model_class[model_name]()
    grid_search = GridSearchCV(estimator=model, param_grid=hyperparameters)
    grid_search.fit(X_train, y_train)

    return {
        "Model": model_name,
        "Score": grid_search.best_score_,
        "Params": grid_search.best_params_
    }


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5004)
