import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pyodbc
st.set_page_config(layout="wide")
st.title('📊 Financial Dashboard')


connection = pyodbc.connect(Driver='SQL Server',
                      Server='DESKTOP-D16NLEO',
                      Database='ALI',
                      Trusted_Connection='yes')
data = pd.read_sql('select * from financials', connection)



data['Date'] = pd.to_datetime(data['Date'])

# Clean column names (strip spaces)
data.columns = data.columns.str.strip()

# Sidebar filters
years = ['All'] + sorted(data['Date'].dt.year.unique().tolist())
countries = ['All'] + sorted(data['Country'].unique().tolist())

st.sidebar.header('Filters')
selected_year = st.sidebar.selectbox('Year', options=years)
selected_country = st.sidebar.selectbox('Country', options=countries)
st.sidebar.image('profit.gif')
st.sidebar.image('ali_the.jpg')

# Filter data
new_data = data.copy()
if selected_year != 'All':
    new_data = new_data[new_data['Date'].dt.year == selected_year]
if selected_country != 'All':
    new_data = new_data[new_data['Country'] == selected_country]

# Tabs
tab1, tab2, tab3 = st.tabs(['Main', 'Summary', 'Trend'])

# --- Main Tab ---
with tab1:
    Sales = np.round(new_data['Sales'].sum() / 1_000_000, 2)
    Profits = np.round(new_data['Profit'].sum() / 1_000_000, 2)
    Units = np.round(new_data['Units_Sold'].sum() / 1_000, 2)
    Discount = np.round(new_data['Discounts'].sum() / 1_000_000, 2)
    profit_pct = np.round((Profits / Sales) * 100, 1) if Sales != 0 else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Total Sales', f"{Sales}M")
    col2.metric('Total Profit', f"{Profits}M")
    col3.metric('Units Sold', f"{Units}K")
    col4.metric('Total Discount', f"{Discount}M")
    col5.metric('Profit %', f"{profit_pct}%")

    d = new_data.groupby(['Segment', 'Country'])['Sales'].sum().reset_index()
    fig1 = px.treemap(d, path=['Country', 'Segment'], values='Sales', title='Sales by Segment & Country')
    fig1.update_traces(textinfo='label+value')
    st.plotly_chart(fig1, use_container_width=True)

    d1 = new_data.groupby(['Segment', 'Product'])['Sales'].sum().reset_index()
    fig2 = px.sunburst(d1, path=['Segment', 'Product'], values='Sales', title='Sales by Product & Segment')
    fig2.update_traces(textinfo='label+value')
    st.plotly_chart(fig2, use_container_width=True)

# --- Summary Tab ---
with tab2:
    d2 = new_data.groupby('Discount_Band')['Discounts'].sum().reset_index()
    fig3 = px.pie(d2, names='Discount_Band', values='Discounts', hole=0.6,
                  title='Discounts by Band')
    fig3.update_traces(textinfo='label+value')
    st.plotly_chart(fig3, use_container_width=True)

    d3 = new_data.groupby('Product')['COGS'].sum().reset_index().sort_values(by='COGS', ascending=False)
    fig4 = px.bar(d3, x='Product', y='COGS', title='COGS by Product', text_auto='.2s')
    st.plotly_chart(fig4, use_container_width=True)

    d4 = new_data.groupby(['Country', 'Product'])['Units_Sold'].sum().reset_index()
    fig5 = px.bar(d4, x='Country', y='Units_Sold', color='Product', barmode='group',
                  title='Units Sold by Country and Product')
    st.plotly_chart(fig5, use_container_width=True)

# --- Trend Tab (optional) ---
with tab3:
    d5=new_data.groupby('Date')['Sales'].sum().reset_index()
    fig6=px.line(d5, x='Date', y='Sales', title='Total Sales by Month')
    st.plotly_chart(fig6,use_container_width=True)
    d6=new_data.groupby('Date')['COGS'].sum().reset_index()
    fig7=px.line(d6, x='Date', y='COGS', title='Total COGS by Month')
    st.plotly_chart(fig7,use_container_width=True)
    d7=new_data.groupby('Date')['Profit'].sum().reset_index()
    fig8=px.line(d7, x='Date', y='Profit', title='Total Profit by Month')
    st.plotly_chart(fig8,use_container_width=True)