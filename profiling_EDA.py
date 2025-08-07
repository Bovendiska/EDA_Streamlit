import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import csv
def introduction():
    st.title("📌 Introduction")
    st.write(
        """
        **Selamat datang di aplikasi Exploratory Data Analysis (EDA) dengan Streamlit!**  
        Aplikasi ini dibuat untuk membantu teman-teman dalam menganalisis dataset dengan cepat dan interaktif.  
        
        ### 🔹 **Fitur Utama**
        - **📁Data Preparation** → Melihat informasi dasar dataset
        - **📊EDA** → Analisis statistik, missing values, dan korelasi data
        - **📈Data Visualization** → Visualisasi interaktif
        - **📜Evaluation** → Profiling dataset secara otomatis

        ---
        **👨‍💻 Tentang Saya**  
        - **Nama:** Bonaventura Dimas S.K  
        - **Universitas:** Gunadarma University  
        - **Keahlian:** Python, Machine Learning, Streamlit, NLP, SQL, Excel, Tableu/Looker Studio  
        - **Deskripsi:** Saya merupakan data antusias dan juga machine learning antusias
        ---

        *Hubungi saya di [LinkedIn](https://www.linkedin.com/in/bonaventura-dimas-sakti-karunia-b2b091224/)!*
        """
    )

def upload_file():
    """Fungsi untuk mengunggah file CSV atau Excel dengan deteksi separator otomatis."""
    uploaded_file = st.file_uploader("Unggah dataset Anda", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                # --- NEW: Logika untuk deteksi separator otomatis ---
                # Mengintip baris pertama untuk mendeteksi delimiter
                sample = uploaded_file.read(1024).decode('ISO-8859-1')
                uploaded_file.seek(0) # Kembali ke awal file setelah membaca sample

                try:
                    # Menggunakan Sniffer untuk menemukan delimiter
                    dialect = csv.Sniffer().sniff(sample, delimiters=',;')
                    separator = dialect.delimiter
                except csv.Error:              
                return pd.read_csv(uploaded_file, encoding="ISO-8859-1", sep=separator)
            else:
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Terjadi error saat membaca file: {e}")
    return None
        
def profiling(df):
    st.subheader("📊 Profiling")
    st.write("**Generating Profiling Report...**")
    if df.shape[0] > 10000:
        st.warning("Dataset terlalu besar untuk profiling. Disarankan menggunakan dataset di bawah 10.000 baris.")
    else:
        profile = ProfileReport(df, explorative=True)
        st_profile_report(profile)

def basic_info(df):
    st.subheader("📊 Informasi Dataset")
    st.write(df.head())
    st.write(f"Dataset yang anda unggah/upload terdiri dari {df.shape[0]} baris dan {df.shape[1]} kolom.")

def describe_stats(df):
    st.subheader("📈 Statistik Deskriptif")
    st.write(df.describe())

def missing_val(df):
    st.subheader("❗ Missing Values")

    miss_val = df.isnull().sum()
    missing_data = miss_val[miss_val > 0]
    

    if not missing_data.empty:
        st.write("Terdapat missing values pada kolom-kolom berikut:")
        st.write(missing_data)
    else:
        st.write("Tidak terdapat missing values pada dataset.")
    

    st.write(f"Berdasarkan dataset yang diunggah, terdapat missing value pada kolom-kolom berikut: {', '.join(missing_data.index)}")

def distribution(df):
    st.subheader("📊 Distribusi Data Numerik")
    numeric_columns = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns
    for column in numeric_columns:
        st.write(f"Distribusi untuk {column}:")
        fig, ax = plt.subplots()
        sns.histplot(df[column], kde=True, ax=ax)
        st.pyplot(fig)

def tampilkan_corr(df):
    st.subheader("🔥 Heatmap Korelasi")
    numeric_df = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32'])
    
    corr_matrix = numeric_df.corr()

    np.fill_diagonal(corr_matrix.values, np.nan)

    max_corr = corr_matrix.unstack().idxmax()
    max_corr_value = corr_matrix.max().max()

    fig, ax = plt.subplots()
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.write(f"Korelasi tertinggi ditemukan antara kolom **{max_corr[0]}** dan **{max_corr[1]}** dengan nilai korelasi **{max_corr_value: .2f}**.")

def data_visualization(df):
    st.subheader("📊 Data Visualization")
    column = st.selectbox("Pilih kolom numerik untuk visualisasi:", df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns)
    plot_type = st.radio("Pilih Jenis Plot", ["Histogram", "Boxplot"])
    fig, ax = plt.subplots()
    sns.histplot(df[column], kde=True, ax=ax) if plot_type == "Histogram" else sns.boxplot(y=df[column], ax=ax)
    st.pyplot(fig)

def main():
    
    st.set_page_config(layout="wide", page_title="EDA dengan Streamlit")
    
    # Menambahkan CSS untuk centering konten
    st.markdown(
        """
        <style>
        .reportview-container {
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100vh;
            width: 100%;
        }
        .block-container {
            width: 80%;  /* Menentukan lebar konten, bisa disesuaikan */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.title("🔎 Navigasi")
    menu = st.sidebar.selectbox("Pilih menu:", ["Introduction", "Data Preparation", "EDA", "Data Visualization", "Evaluation"])
    
    df = None

    if menu != "Introduction":
        df = upload_file()
    
    if menu == "Introduction":
        introduction()

    elif df is not None:
        if menu == "Data Preparation":
            basic_info(df)
        elif menu == "EDA":
            analysis_option = st.selectbox("Pilih analisis yang ingin ditampilkan:", ["Statistik Deskriptif", "Missing Value", "Persebaran Data", "Heatmap Korelasi"])
            if analysis_option == "Statistik Deskriptif":
                describe_stats(df)
            elif analysis_option == "Missing Value":
                missing_val(df)
            elif analysis_option == "Persebaran Data":
                distribution(df)
            elif analysis_option == "Heatmap Korelasi":
                tampilkan_corr(df)
        elif menu == "Data Visualization":
            data_visualization(df)
        elif menu == "Evaluation":
            profiling(df)
    else:
        st.write("Silakan unggah file untuk memulai.")

if __name__ == "__main__":
    main()





