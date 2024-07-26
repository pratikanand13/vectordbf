import streamlit as st
import requests

st.title("Upload CSV to MongoDB")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

organization_name = st.text_input("Enter MongoDB organization (database) name")
intent_name = st.text_input("Enter intent (collection) name")

if st.button("Upload"):
    if uploaded_file is not None and organization_name and intent_name:
        files = {'file': uploaded_file}
        data = {
            'organization_name': organization_name,
            'intent_name': intent_name
        }
        try:
            response = requests.post("http://127.0.0.1:5000/upload", files=files, data=data)
            if response.status_code == 200:
                st.success("File successfully uploaded and data stored in MongoDB!")
            else:
                st.error("Failed to upload file.")
                st.error(response.json())
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload a file and enter both the organization and intent names.")
