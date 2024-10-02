import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/train-model', methods=['POST'])
def train_model():
    data = request.get_json()
    y_feature = data.get("outputColumn")

    X_train = pd.DataFrame(data.get('X_train'))
    X_test = pd.DataFrame(data.get('X_test'))
    y_train = pd.Series(data.get('y_train'))
    y_test = pd.Series(data.get('y_test'))

    models_list = [
        LogisticRegression,
        KNeighborsClassifier,
        DecisionTreeClassifier,
        SVC,
        GaussianNB,
        RandomForestClassifier,
        GradientBoostingClassifier,
        AdaBoostClassifier
    ]

    model_stats = []

    for model_class in models_list:
        try:
            model = model_class()
            if model_class == LogisticRegression and y_train.nunique() == 2:
                model = model_class()
                stats = multiple_model(X_train, X_test, y_train, y_test, model)
                model_stats.append({"Model": model_class.__name__, **stats})
            elif model_class == AdaBoostClassifier:
                model = model_class(algorithm='SAMME')
                stats = multiple_model(X_train, X_test, y_train, y_test, model)
                model_stats.append({"Model": model_class.__name__, **stats})
            else:
                stats = multiple_model(X_train, X_test, y_train, y_test, model)
                model_stats.append({"Model": model_class.__name__, **stats})
        except Exception as e:
            print(f"Error with model {model_class.__name__}: {e}")

    formatted_stats = [{"Model": stat["Model"],
                        "Accuracy": f"{stat['accuracy']:.2f}",
                        "Precision": f"{stat['precision']:.2f}",
                        "Recall": f"{stat['recall']:.2f}",
                        "F1 Score": f"{stat['f1_score']:.2f}"} for stat in model_stats]

    return jsonify(formatted_stats)


def multiple_model(X_train, X_test, y_train, y_test, model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
