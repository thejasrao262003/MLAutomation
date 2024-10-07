from locust import HttpUser, task, between
import pandas as pd
from collections import OrderedDict
import numpy as np

class MyUser(HttpUser):
    wait_time = between(1, 3)  # Wait between tasks

    @task
    def load_frontend(self):
        self.client.get("/frontend/")  # Load the frontend

    @task
    def load_datapreprocessing(self):
        # Create a dummy DataFrame with numerical columns
        num_rows = 100  # Number of rows in the dummy DataFrame
        data = {
            'feature1': np.random.rand(num_rows) * 100,  # Random values for feature1
            'feature2': np.random.rand(num_rows) * 100,  # Random values for feature2
            'feature3': np.random.rand(num_rows) * 100,  # Random values for feature3
            'output_column': np.random.randint(0, 2, num_rows)  # Binary output column (0 or 1)
        }

        # Create the DataFrame and convert to a list of OrderedDicts
        df = pd.DataFrame(data)
        selected_option = 'output_column'  # Column to be used as the output

        # Convert DataFrame to a list of dictionaries
        example_data = df.to_dict(orient='records')

        # Construct the payload
        payload = {
            "selected_option": selected_option,
            "data": [OrderedDict(row) for row in example_data]  # Convert to OrderedDict
        }

        # Send POST request to the /process endpoint
        response = self.client.post("/datapreprocessing/process", json=payload)

        if response.status_code == 200:
            print("Processing successful.")
        else:
            print(f"Failed to process: {response.text}")
