import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Executive Sales & Margin Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df['OrderDate'] = pd.to_datetime(df['OrderDate'])
    df['YearMonth'] = df['OrderDate'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Сайдбар с фильтрами
st.sidebar.title("Dashboard Filters")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[(df['Region'].isin(selected_region)) & (df['Category'].isin(selected_category))]

# Шапка
st.title("📈 Executive Sales & Margin Performance Dashboard")
st.markdown("Commercial analysis tracking revenue velocity, product contribution margins, and regional growth.")

# KPI карточки
total_rev = filtered_df['Revenue'].sum()
total_profit = filtered_df['Profit'].sum()
margin_pct = (total_profit / total_rev * 100) if total_rev > 0 else 0
avg_ticket = filtered_df['Revenue'].mean() if len(filtered_df) > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Revenue", f"${total_rev:,.0f}")
kpi2.metric("Gross Profit", f"${total_profit:,.0f}")
kpi3.metric("Profit Margin", f"{margin_pct:.1f}%")
kpi4.metric("Avg Order Value", f"${avg_ticket:,.2f}")

st.markdown("---")

# Графики: Сетка 2x2
col1, col2 = st.columns(2)

with col1:
    # Динамика выручки по месяцам
    monthly_trend = filtered_df.groupby('YearMonth')[['Revenue', 'Profit']].sum().reset_index()
    fig_trend = px.line(monthly_trend, x='YearMonth', y=['Revenue', 'Profit'],
                        labels={'value': 'USD ($)', 'YearMonth': 'Month'},
                        title="Revenue & Profit Monthly Trajectory",
                        color_discrete_sequence=['#2b6cb0', '#2c7a7b'])
    fig_trend.update_layout(legend_title_text='Metric')
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    # Выручка и маржа по категориям
    cat_summary = filtered_df.groupby('Category')[['Revenue', 'Profit']].sum().reset_index()
    fig_cat = px.bar(cat_summary, x='Category', y='Revenue', color='Category',
                     title="Revenue by Product Category",
                     color_discrete_sequence=px.colors.sequential.Blues_r)
    st.plotly_chart(fig_cat, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    # Доли регионов в продажах
    region_pie = px.pie(filtered_df, values='Revenue', names='Region',
                        title="Regional Revenue Contribution",
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(region_pie, use_container_width=True)

with col4:
    # Каналы продаж vs Маржа
    channel_summary = filtered_df.groupby('Channel')[['Revenue', 'Profit']].sum().reset_index()
    channel_summary['MarginPct'] = channel_summary['Profit'] / channel_summary['Revenue'] * 100
    fig_channel = px.bar(channel_summary, x='Channel', y='MarginPct',
                         title="Profit Margin % by Acquisition Channel",
                         labels={'MarginPct': 'Margin (%)'},
                         color='Channel',
                         color_discrete_sequence=['#319795', '#4299e1', '#2b6cb0'])
    st.plotly_chart(fig_channel, use_container_width=True)