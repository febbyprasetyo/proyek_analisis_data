import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
sns.set(style='dark')

# Create pastel color palette
pastel_palette = sns.color_palette("pastel")

# Judul Dashboard
st.title('Bike Sharing Dashboard 🚲')

# Memuat data
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/febbyprasetyo/proyek_analisis_data/main/dashboard/day_done.csv?token=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")
    return data

days_df = load_data()

# Filter Tanggal di Bawah Data Mentah di Sidebar
st.sidebar.subheader('Filter Data')
min_date = pd.to_datetime(days_df['dteday'].min())
max_date = pd.to_datetime(days_df['dteday'].max())
date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date))
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Filter Data Berdasarkan Tanggal
filtered_df = days_df[(pd.to_datetime(days_df['dteday']) >= start_date) & (pd.to_datetime(days_df['dteday']) <= end_date)]

# Statistik Total Sewa Sepeda per Bulan
st.subheader('Statistik Total Sewa Sepeda per Bulan')

# Mengekstrak bulan dari kolom 'dteday' dan mempersingkat nama bulan menjadi 3 huruf
days_df['month'] = pd.to_datetime(days_df['dteday']).dt.month_name().str.slice(stop=3)

# Menghitung total sewa sepeda per bulan
total_bike_sharing_per_month = days_df.groupby('month')['cnt'].sum()

# Membuat plot garis
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=total_bike_sharing_per_month.index, y=total_bike_sharing_per_month.values, marker='o', color='skyblue', ax=ax)
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Penyewaan Sepeda')
ax.set_title('Total Penyewaan Sepeda per Bulan')

# Menambahkan garis kisi
plt.grid(True)

st.pyplot(fig)

# Total Penyewaan Sepeda
total_bike_sharing = days_df['cnt'].sum()
st.write(f"Total Penyewaan Sepeda: {total_bike_sharing}")

# Pesanan Data Harian
st.subheader('Pesanan Data Harian')
st.write(filtered_df)

# Visualisasi 1: Korelasi antara Kondisi Cuaca dan Tingkat Sewa Sepeda
st.subheader('Korelasi antara Kondisi Cuaca dan Tingkat Sewa Sepeda')

# Memilih kondisi cuaca menggunakan kotak pilih
selected_weather = st.selectbox('Select Weather Condition:', ['weather_Clear', 'weather_Mist + Cloudy', 'weather_Light Snow'])

# Pengelompokan data berdasarkan kondisi cuaca yang dipilih dan menghitung rata-rata tingkat sewa sepeda
filtered_data = filtered_df.groupby(selected_weather)['cnt'].mean()
filtered_data.index = ['Holiday' if index == 0 else 'Working Day' for index in filtered_data.index]

# Membuat diagram batang
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=filtered_data.index, y=filtered_data.values, palette=pastel_palette, ax=ax)
ax.set_xlabel('Hari')
ax.set_ylabel('Rata-rata Penggunaan Sewa Sepeda')
ax.set_title('Rata-rata Sewa Sepeda Berdasarkan Kondisi Cuaca')

# Adding annotations to the bars
for index, value in enumerate(filtered_data):
    plt.text(index, value, str(round(value, 2)), ha='center', va='bottom', fontsize=10)

# Displaying the plot
st.pyplot(fig)

# Visualisasi 2: Jumlah Sewa Sepeda per Musim
st.subheader('Jumlah Sewa Sepeda per Musim')

# Jumlah sewa Sepeda per Musim
season_counts = filtered_df['season'].value_counts()

# Membuat diagram batang
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=season_counts.index, y=season_counts.values, palette=pastel_palette, ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Jumlah')
ax.set_title('Jumlah Sewa Sepeda per Musim')

# Menampilkan jumlah setiap musim di bawah plot
for i, count in enumerate(season_counts.values):
    plt.text(i, count, str(count), ha='center', va='bottom', fontsize=10)

st.pyplot(fig)

# Visualisasi 3: Rata-rata Penyewaan Sepeda Berdasarkan Hari Kerja atau Hari Libur
st.subheader('Rata-rata Penyewaan Sepeda Berdasarkan Hari Kerja atau Hari Libur')

# Menghitung Rata-rata Penyewaan Sepeda Berdasarkan Hari Kerja atau Hari Libur
workingday_avg = filtered_df.groupby('workingday')['cnt'].mean()

# Membuat diagram batang
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=workingday_avg.index, y=workingday_avg.values, palette=pastel_palette, ax=ax)
ax.set_xlabel('Hari Kerja')
ax.set_ylabel('Rata-Rata Penyewaan Sepeda')
ax.set_title('Rata-rata Sewa Sepeda Berdasarkan Hari Kerja atau Hari Libur')

# Menambahkan anotasi ke bilah
for index, value in enumerate(workingday_avg):
    plt.text(index, value, str(round(value, 2)), ha='center', va='bottom', fontsize=10)

#Menampilkan plot
st.pyplot(fig)

