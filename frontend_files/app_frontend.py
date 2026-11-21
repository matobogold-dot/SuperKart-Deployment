import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="SuperKart Sales Forecaster", layout="wide")

st.title("🛒 SuperKart Sales Forecasting Dashboard")
st.write("Real-time and batch predictive analytics powered by Decoupled Machine Learning Service APIs.")

# Define the API URL pointing to the backend container service
BACKEND_URL = "http://backend-service:7860"

tab1, tab2 = st.tabs(["🎯 Real-Time Prediction", "📂 Batch CSV Prediction"])

with tab1:
    st.header("Single Item Sales Estimator")
    st.write("Fill out the product and store attributes to forecast sales totals.")
    
    col1, col2 = st.columns(2)
    with col1:
        product_weight = st.number_input("Product Weight", min_value=1.0, max_value=50.0, value=12.5)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        allocated_area = st.number_input("Product Allocated Area Ratio", min_value=0.0, max_value=1.0, value=0.06)
        product_mrp = st.number_input("Product Maximum Retail Price (MRP)", min_value=5.0, max_value=500.0, value=147.0)
        product_type = st.selectbox("Product Category", ["Consumables", "Non Consumables", "Perishables", "Non Perishables"])
        
    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Food Mart", "Departmental Store"])
        store_age = st.number_input("Store Age (Years)", min_value=0, max_value=100, value=15)
        product_id_char = st.selectbox("Product ID Characters", ["FD", "DR", "NC"])

    if st.button("Predict Store Sales Total"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar,
            "Product_Allocated_Area": allocated_area,
            "Product_MRP": product_mrp,
            "Store_Size": store_size,
            "Store_Location_City_Type": city_type,
            "Store_Type": store_type,
            "Product_Id_char": product_id_char,
            "Store_Age_Years": store_age,
            "Product_Type_Category": product_type
        }
        
        try:
            response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                predicted_sales = result.get("Product_Store_Sales_Total_Predicted", 0.0)
                st.success(f"💰 Predicted Store Sales Total: **${predicted_sales:,.2f}**")
            else:
                st.error(f"Error: Recieved status code {response.status_code} from Backend. Detail: {response.text}")
        except Exception as e:
            st.error(f"Could not connect to backend server: {str(e)}")

with tab2:
    st.header("Bulk Inference Portal")
    st.write("Upload a CSV file containing batch store records to obtain predictions immediately.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df_input = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded data:")
        st.dataframe(df_input.head(5))
        
        if st.button("Run Batch Forecast"):
            # Reset pointer and prepare payload
            uploaded_file.seek(0)
            files = {'file': (uploaded_file.name, uploaded_file.read(), 'text/csv')}
            
            try:
                response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
                if response.status_code == 200:
                    predictions = response.json()
                    # Map predictions back to DataFrame
                    df_input['Predicted_Sales_Total'] = df_input.index.map(lambda x: predictions.get(str(x)))
                    st.success("🎉 Batch Forecasting completed successfully!")
                    st.dataframe(df_input)
                    
                    # Enable download of results as CSV
                    csv_buffer = io.StringIO()
                    df_input.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="📥 Download Predicted Results as CSV",
                        data=csv_buffer.getvalue(),
                        file_name="SuperKart_Batch_Forecasts.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Batch Error: Recieved status {response.status_code} from Backend. Detail: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to backend server: {str(e)}")
