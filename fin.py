import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.title("CSV File Uploader")
uploaded_file = st.file_uploader("Choose a excel file", type="xlsx")
data = pd.read_excel(uploaded_file)

data.dropna(axis='columns',how='all',inplace=True)
data1=data.iloc[:,0:4]
data1['Unnamed: 0'].ffill(inplace=True)
data1.dropna(axis='rows',how='all',inplace=True)
data1.drop(columns=['Unnamed: 1'],inplace=True)
data1.dropna(subset='Unnamed: 2',inplace=True)
clients=pd.pivot(data1,index='Unnamed: 0',columns='Unnamed: 3',values='Unnamed: 2')
clients.reset_index(inplace=True)
clients.rename(columns={'Unnamed: 0':'رقم الطلب'},inplace=True)
data2 = data.iloc[:, [0] + list(range(4, data.shape[1]))]
data2.iloc[:,[0,8]]=data2.iloc[:,[0,8]].fillna(method='ffill')
data2.dropna(subset=['Unnamed: 4'],inplace=True)
data2.columns=data2.iloc[0,:]
data2=data2.where(data2['النوع']!='النوع').dropna()
data2.rename(columns={data2.columns[0]:'رقم الطلب'},inplace=True)
data2['التاريخ']=pd.to_datetime(data2['التاريخ'])
Sales=data2
data=pd.merge(Sales,clients,how='inner',on='رقم الطلب')
st.dataframe(data)
