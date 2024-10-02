import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, jsonify
from collections import OrderedDict

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process_csv():
    data = request.get_json()
    y_feature = data.get("selected_option")
    df = pd.DataFrame(data.get('data'))
    output_column = df[y_feature]
    oneHotEncodedData = df.copy()

    for i in df.columns:
        if i in oneHotEncodedData.columns and i != y_feature:
            if any([
                i.endswith('id'), i.endswith('Id'), i == 'id', i == 'Id',
                i.startswith('id_'), i.startswith('Id_'),
                i.endswith('id_'), i.endswith('Id_')
            ]):
                oneHotEncodedData = oneHotEncodedData.drop(i, axis=1)

            if df[i].isnull().sum() >= 0.5 * df.shape[0]:
                oneHotEncodedData = oneHotEncodedData.drop(i, axis='columns')

            elif df[i].isnull().sum() > 0:
                oneHotEncodedData.fillna(df[i].mean(), inplace=True)

            if len(df[i].unique()) <= 5:
                oneHotEncodedData = convertToLabels(i, oneHotEncodedData)

            if df[i].dtype == 'object':
                oneHotEncodedData = removeTextualFeatures(i, oneHotEncodedData)

            if i in oneHotEncodedData.columns:
                oneHotEncodedData, output_column = removeOutliers(i, oneHotEncodedData, output_column)

    x, y = xySeparation(y_feature, oneHotEncodedData)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(x)
    scaled_df = pd.DataFrame(scaled_data, columns=x.columns)

    scaled_df[y_feature] = y.reset_index(drop=True)
    result = scaled_df.apply(lambda row: OrderedDict(row), axis=1).to_list()
    return jsonify(result)

def convertToLabels(feature: str, df):
    df = pd.get_dummies(df, columns=[feature], drop_first=True)
    return df

def removeTextualFeatures(feature: str, df):
    return df.drop(feature, axis="columns")

def xySeparation(feature: str, df):
    y = df[feature]
    x = df.drop(feature, axis='columns')
    return x, y

def removeOutliers(feature: str, df, output_column):
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    upper_array = df[df[feature] >= upper].index
    lower_array = df[df[feature] <= lower].index

    df = df.drop(index=upper_array)
    df = df.drop(index=lower_array)
    output_column = output_column.drop(index=upper_array)
    output_column = output_column.drop(index=lower_array)

    return df, output_column


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
