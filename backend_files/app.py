import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, jsonify
import io

app = Flask(__name__)

# Load the champion model pipeline
model = joblib.load('superkart_model.joblib')

# Helper function to preprocess incoming data consistently
def preprocess_data(df):
    df_cleaned = df.copy()
    # Fix any potential sugar content inconsistencies
    if 'Product_Sugar_Content' in df_cleaned.columns:
        df_cleaned['Product_Sugar_Content'] = df_cleaned['Product_Sugar_Content'].replace('reg', 'Regular')
    return df_cleaned

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        # Parse json request
        data = request.get_json(force=True)
        df_input = pd.DataFrame([data])
        df_processed = preprocess_data(df_input)

        # Predict using pipeline
        prediction = model.predict(df_processed)[0]
        return jsonify({'Product_Store_Sales_Total_Predicted': float(prediction)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    try:
        # Expecting a file upload under the key 'file'
        file = request.files['file']
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        # Read uploaded CSV
        df_input = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
        df_processed = preprocess_data(df_input)

        # Generate batch predictions
        predictions = model.predict(df_processed)

        # Return indices mapped to predictions
        response_dict = {str(i): float(pred) for i, pred in enumerate(predictions)}
        return jsonify(response_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
