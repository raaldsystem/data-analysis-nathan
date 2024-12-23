# -*- coding: utf-8 -*-
"""youtube-performance_analysis-nathangerald.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RR0KNxWtjC7LLCyoxJ1gdzDTKyuXRfUa

**Purpose** : Mengetahui bagaimana youtube dapat menghasilkan uang

**Question** :
1. Durasi video yang paling banyak menghasilkan revenue?
2. Pada hari apa traffic orang paling banyak buka youtube?
3. Berapa rata-rata pendapatan yang bisa dihasilkan dari membuat video youtube?
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

"""**Gathering Data**"""

sheet_url = "https://docs.google.com/spreadsheets/d/1N0YTx714CMGU5DPTRUaNCY-qnbThz6slEG6eqImXxak/export?format=csv&gid=74239411"

yta_df = pd.read_csv(sheet_url)
yta_df.head()

"""**Assesing Data**"""

yta_df.info()

yta_df.isna().sum()

yta_df.describe()

"""insight

* video publish time = harusnya date_stamp
* hapus column 18-27 ; 35-39 ; 56-59 ;
* column 51 = float
* column 54 = float
* colum 65 = float
* column 61 cuman ada 3 data rows

**CLEANING DATA**
"""

datetime_columns = ["Video Publish Time"]

for column in datetime_columns:
    yta_df[column] = pd.to_datetime(yta_df[column], errors="coerce")

yta_df.info()

columns_to_drop = list(range(18, 27)) + list(range(35, 39)) + list(range(56, 59))
yta_df = yta_df.drop(yta_df.columns[columns_to_drop], axis=1)

columns_to_drop = [18, 26, 43]
yta_df = yta_df.drop(yta_df.columns[columns_to_drop], axis=1)

"""**EXPLORATORY DATA ANALYSIS**"""

yta_df.describe(include="all")

yta_df['Watch Time (hours)'] = pd.to_numeric(yta_df['Watch Time (hours)'], errors='coerce')
watch_time_by_day = yta_df.groupby('Day of Week')['Watch Time (hours)'].sum().sort_values(ascending=False)
highest_watch_time_day = watch_time_by_day.idxmax()
print(f"Day with the highest watch time: {highest_watch_time_day}")
print(watch_time_by_day)

views_by_duration = yta_df.groupby('Video Duration')['Views'].sum().sort_values(ascending=False)
most_watched_duration = views_by_duration.idxmax()
print(f"Video duration with the highest views: {most_watched_duration}")
print(views_by_duration)

yta_df['Revenue per 1000 Views (USD)'] = pd.to_numeric(yta_df['Revenue per 1000 Views (USD)'], errors='coerce')
yta_df['Video Duration'] = pd.to_numeric(yta_df['Video Duration'], errors='coerce')
yta_df['Total Revenue'] = yta_df['Revenue per 1000 Views (USD)'] * yta_df['Views'] / 1000
grouped = yta_df.groupby('Video Duration').agg(
    avg_revenue=('Total Revenue', 'mean'),
    avg_shares=('Shares', 'mean')
).sort_values(by='avg_revenue', ascending=False)
highest_revenue_duration = grouped.iloc[0]
print(f"Video duration with the highest average revenue: {grouped.index[0]} seconds")
print(f"Average revenue: ${highest_revenue_duration['avg_revenue']:.2f}")
print(f"Average shares: {highest_revenue_duration['avg_shares']:.2f}")
grouped.head()

impressions_per_duration = yta_df.groupby('Video Duration')['Impressions'].sum().sort_values(ascending=False)
highest_impressions_duration = impressions_per_duration.idxmax()
highest_impressions_value = impressions_per_duration.max()

print(f"Durasi video dengan impresi tertinggi adalah {highest_impressions_duration} detik dengan total impresi {highest_impressions_value:,}.")

average_revenue_per_video = yta_df['Estimated Revenue (USD)'].mean()
average_revenue_per_view = yta_df['Estimated Revenue (USD)'].sum() / yta_df['Views'].sum()

print(f"Rata-rata pendapatan yang dihasilkan dari membuat video YouTube adalah ${average_revenue_per_video:.2f} per video.")
print(f"Rata-rata pendapatan per tayangan adalah ${average_revenue_per_view:.6f} per view.")

"""* hari yang paling banyak orang nonton = sabtu
* durasi video yang paling banyak nonton = 530 detik (8 menitan)
* rata-rata pendapatan tertinggi, durasi video = 639 detik (10 menitan) dengan impresi tertinggi juga
* rata-rata pendapatan = $103.33
* rata-rata share = 4190 kali dishare

* rata-rata pendapatan per view adalah $0.000069
"""

yta_df['Watch Time (hours)'] = pd.to_numeric(yta_df['Watch Time (hours)'], errors='coerce')
watch_time_per_day = yta_df.groupby('Day of Week')['Watch Time (hours)'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=watch_time_per_day.index, y=watch_time_per_day.values, palette="viridis")
plt.title("Total Watch Time by Day of the Week", fontsize=16)
plt.xlabel("Day of the Week", fontsize=12)
plt.ylabel("Total Watch Time (hours)", fontsize=12)
plt.xticks(rotation=45)
plt.show()

views_per_duration = yta_df.groupby('Video Duration')['Views'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=views_per_duration.index, y=views_per_duration.values, palette="rocket")
plt.title("Top 10 Video Durations with Highest Views", fontsize=16)
plt.xlabel("Video Duration (seconds)", fontsize=12)
plt.ylabel("Total Views", fontsize=12)
plt.xticks(rotation=45)
plt.show()

yta_df['Total Revenue'] = yta_df['Revenue per 1000 Views (USD)'] * yta_df['Views'] / 1000
revenue_per_duration = yta_df.groupby('Video Duration')['Total Revenue'].mean().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=revenue_per_duration.index, y=revenue_per_duration.values, palette="coolwarm")
plt.title("Top 10 Video Durations with Highest Average Revenue", fontsize=16)
plt.xlabel("Video Duration (seconds)", fontsize=12)
plt.ylabel("Average Revenue (USD)", fontsize=12)
plt.xticks(rotation=45)
plt.show()

"""Rekomendasi
* Upload video dengan durasi 8-10 menit
* traffic terbanyak terjadi pada hari sabtu, sehingga disarankan **"upload video hari SABTU"**
* rata-rata pendapatan yang bisa didapatkan adalah $0.000069 per view (IDR 1.09/view)
"""