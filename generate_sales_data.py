import pandas as pd
import numpy as np

np.random.seed(42)
n_rows = 5000

dates = pd.date_range(start='2024-01-01', end='2025-12-31', periods=n_rows)
regions = np.random.choice(['North America', 'Europe', 'Asia Pacific', 'Latin America'], size=n_rows, p=[0.4, 0.3, 0.2, 0.1])
categories = np.random.choice(['Technology', 'Office Supplies', 'Furniture'], size=n_rows, p=[0.35, 0.45, 0.2])
channels = np.random.choice(['Direct Sales', 'Online Marketplace', 'Distributor'], size=n_rows, p=[0.5, 0.35, 0.15])

sales = np.round(np.random.exponential(scale=180, size=n_rows) + 20, 2)
# Маржинальность в зависимости от категории
margin_rates = {'Technology': 0.38, 'Office Supplies': 0.22, 'Furniture': 0.15}
base_margin = [margin_rates[cat] for cat in categories]
noise = np.random.normal(0, 0.05, size=n_rows)
profit = np.round(sales * np.clip(base_margin + noise, 0.05, 0.60), 2)

df = pd.DataFrame({
    'OrderDate': dates,
    'Region': regions,
    'Category': categories,
    'Channel': channels,
    'Revenue': sales,
    'Profit': profit,
    'Quantity': np.random.randint(1, 10, size=n_rows)
})

df.to_csv('sales_data.csv', index=False)
print("Файл sales_data.csv успешно сгенерирован (5,000 записей).")