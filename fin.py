import streamlit as st
import pandas as pd
import numpy as np

st.title("Excel File Uploader")

uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        # Read the Excel file
        data = pd.read_excel(uploaded_file)

        # --- Clean client table ---
        data.dropna(axis='columns', how='all', inplace=True)
        data1 = data.iloc[:, 0:4].copy()

        data1['Unnamed: 0'].ffill(inplace=True)
        data1.dropna(axis='rows', how='all', inplace=True)
        data1.drop(columns=['Unnamed: 1'], inplace=True)
        data1.dropna(subset=['Unnamed: 2'], inplace=True)

        clients = pd.pivot_table(data1, index='Unnamed: 0', columns='Unnamed: 3', values='Unnamed: 2', aggfunc='first')
        clients.reset_index(inplace=True)
        clients.rename(columns={'Unnamed: 0': 'رقم الطلب'}, inplace=True)

        # --- Clean sales table ---
        data2 = data.iloc[:, [0] + list(range(4, data.shape[1]))].copy()
        data2.iloc[:, [0, 8]] = data2.iloc[:, [0, 8]].fillna(method='ffill')
        data2.dropna(subset=['Unnamed: 4'], inplace=True)

        data2.columns = data2.iloc[0, :]
        data2 = data2[1:]  # drop header row

        data2 = data2[data2['النوع'] != 'النوع']
        data2.rename(columns={data2.columns[0]: 'رقم الطلب'}, inplace=True)
        data2['التاريخ'] = pd.to_datetime(data2['التاريخ'], errors='coerce')

        Sales = data2.copy()

        # --- Merge sales with clients ---
        merged_data = pd.merge(Sales, clients, how='inner', on='رقم الطلب')

        st.success("Data loaded and processed successfully!")
        st.dataframe(merged_data)

    except Exception as e:
        st.error(f"⚠️ An error occurred while processing the file: {e}")
else:
    st.info("Please upload an Excel file (.xlsx) to continue.")
