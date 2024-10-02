import streamlit as st
import pandas as pd
import requests
import base64
from io import BytesIO
from PIL import Image
from collections import OrderedDict
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="CSV File Reader", layout="wide")
st.header("Single File Reader")

upload_file = st.file_uploader("Upload your CSV file", type="csv")

if 'image' not in st.session_state:
    st.session_state['image'] = None
if 'modelStats' not in st.session_state:
    st.session_state['modelStats'] = pd.DataFrame()
if 'response_df' not in st.session_state:
    st.session_state['response_df'] = pd.DataFrame()

if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.session_state['df'] = df
    st.subheader("Original Data")
    st.dataframe(st.session_state['df'], width=1800, height=200)

    st.subheader("Data Preprocessing")
    option = st.selectbox("Select the output column: ", st.session_state['df'].columns)

    if st.button("Preprocess Data"):
        payload = {
            "selected_option": option,
            "data": [OrderedDict(row) for row in st.session_state['df'].to_dict(orient='records')]
        }
        response = requests.post("http://datapreprocessing:5001/process", json=payload)

        if response.status_code == 200:
            response_data = response.json()
            st.session_state['response_df'] = pd.DataFrame(response_data)
            st.success("Data Preprocessing Complete")
        else:
            st.error("Error in backend processing")

    if not st.session_state['response_df'].empty and not st.session_state['response_df'].equals(st.session_state['df']):
        st.subheader("Preprocessed Data")
        st.dataframe(st.session_state['response_df'], width=1800, height=200)

    st.subheader("Data Visualization")

    if 'visualization_option' not in st.session_state:
        st.session_state.visualization_option = None

    visualization_list = ["Histogram", "Box Plot", "Pair Plot", "Correlation Matrix"]
    selected_option = st.selectbox("Select the visualization graph: ", visualization_list)

    if st.button("Select Visualization"):
        st.session_state.visualization_option = selected_option
    if st.session_state.visualization_option is not None:
        with st.form(key='visualization_form'):
            if st.session_state.visualization_option == "Correlation Matrix":
                st.write("Displaying Correlation Matrix")
                submit_button = st.form_submit_button("Visualize Data")

                if submit_button:
                    payload = {
                        "selected_option": selected_option,
                        "data": [OrderedDict(row) for row in st.session_state['df'].to_dict(orient='records')]
                    }
                    response = requests.post("http://visualisation:5002/visualisation", json=payload)

                    if response.status_code == 200:
                        img_data = response.json()['image']
                        st.session_state['image'] = Image.open(BytesIO(base64.b64decode(img_data)))

            elif st.session_state.visualization_option in ["Histogram", "Box Plot"]:
                feature = st.selectbox("Select the feature: ", st.session_state['df'].columns)
                submit_button = st.form_submit_button("Visualize Data")

                if submit_button:
                    payload = {
                        "selected_option": selected_option,
                        "feature": feature,
                        "data": [OrderedDict(row) for row in st.session_state['df'].to_dict(orient='records')]
                    }
                    response = requests.post("http://visualisation:5002/visualisation", json=payload)

                    if response.status_code == 200:
                        img_data = response.json()['image']
                        st.session_state['image'] = Image.open(BytesIO(base64.b64decode(img_data)))

            elif st.session_state.visualization_option == "Pair Plot":
                feature1 = st.selectbox("Select feature 1: ", st.session_state['df'].columns)
                feature2 = st.selectbox("Select feature 2: ", st.session_state['df'].columns)
                submit_button = st.form_submit_button("Visualize Data")

                if submit_button:
                    payload = {
                        "selected_option": selected_option,
                        "feature1": feature1,
                        "feature2": feature2,
                        "data": [OrderedDict(row) for row in st.session_state['df'].to_dict(orient='records')]
                    }
                    response = requests.post("http://visualisation:5002/visualisation", json=payload)

                    if response.status_code == 200:
                        img_data = response.json()['image']
                        st.session_state['image'] = Image.open(BytesIO(base64.b64decode(img_data)))

    if st.session_state['image'] is not None:
        st.image(st.session_state['image'], use_column_width=True)
    if not st.session_state['response_df'].empty:
        X = st.session_state['response_df'].drop(columns=[option])
        y = st.session_state['response_df'][option]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    st.subheader("Model Training")
    if st.button("Train Model"):
        payload = {
            "X_train": X_train.to_dict(orient='records'),
            "X_test": X_test.to_dict(orient='records'),
            "y_train": y_train.tolist(),
            "y_test": y_test.tolist(),
            "outputColumn": option
        }
        response = requests.post("http://modeltraining:5003/train-model", json=payload)
        if response.status_code == 200:
            model_results = response.json()
            st.subheader("Model Training Results")
            st.session_state['modelStats'] = pd.DataFrame(model_results)
            st.session_state['modelStats'] = st.session_state['modelStats'][['Model', 'Accuracy', 'Precision', 'Recall', 'F1 Score']]
        else:
            st.error("Error in model training")

    if not st.session_state['modelStats'].empty:
        st.dataframe(st.session_state['modelStats'], use_container_width=True)

    st.subheader("Hyperparameters Tuning")
    if not st.session_state['modelStats'].empty:
        with st.form(key="hyperparameter_tuning_form"):
            # Select the model for hyperparameter tuning
            hyperParameterTuningModel = st.selectbox(
                "Select the model for hyperparameter tuning: ",
                st.session_state['modelStats']['Model'].unique()
            )
            # Confirm button for form submission inside the form context
            submit_hyperparameter = st.form_submit_button("Confirm")

        if submit_hyperparameter:
            payload = {
                "X_train": X_train.to_dict(orient='records'),
                "X_test": X_test.to_dict(orient='records'),
                "y_train": y_train.tolist(),
                "y_test": y_test.tolist(),
                "model": hyperParameterTuningModel
            }
            response = requests.post("http://hyperparametertuning:5004/hyper-parameterTuning", json=payload)
            if response.status_code == 200:
                results = response.json()
                st.subheader(f"Best Hyperparameters for {results['Model']}")
                st.markdown(f"**Best Score:** `{results['Score']}`")
                st.markdown("### Best Parameters")
                params = results['Params']
                param_df = pd.DataFrame(list(params.items()), columns=["Hyperparameter", "Value"])
                st.table(param_df)

            else:
                st.error("Error in hyperparameter tuning")


else:
    st.write("Please upload a CSV file to proceed.")
