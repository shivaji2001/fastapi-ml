import streamlit as st
import requests
API_URL="http://localhost:8000/predict"
st.title('Insurance Premium Prediction App')
st.markdown("Enter the details below")

# Input fields
age=st.number_input("Age",min_value=1,max_value=119,value=30)
weight=st.number_input("Weight in (kgs)",min_value=1,value=65)
height=st.number_input('Height in meters',min_value=1,max_value=2,value=2)
income_lpa=st.number_input('Income in year(in lpa)',min_value=1,value=5)
smoker=st.selectbox("Are you a smoker",options=[True,False])
city=st.text_input("City",value="Mumbai")
occupation=st.selectbox('Occupation',["retired","freelancer","student","government_job","business_owner","unemployed","private_job"])

if st.button("Predict Premium Category"):
    input_data={
        "age":age,
        "weight":weight,
        "height":height,
        "income_lpa":income_lpa,
        "smoker":smoker,
        "city":city,
        "occupation":occupation
    }
    try:
        response=requests.post(API_URL,json=input_data)
        if response.status_code==200:
            result=response.json()
            st.success(f"Predicted premium insurance category:{result['predicted_category']}")
        else:
            st.error(f"API Error:{response.status_code},{response.text}")
    except requests.exceptions.ConnectionError:
        st.error('Could not connect to FASTAPI Server. make sure it is running on port 8000')
