import streamlit as st
import pandas as pd
import os
import time

# Konfigurasi Halaman Web
st.set_page_config(page_title="Dashboard Sensor Mesh", layout="wide")
st.title("📡 Live Dashboard Sensor Mesh")

OUTPUT_DIR = 'data_sensor'

# Cek apakah folder data ada
if not os.path.exists(OUTPUT_DIR):
    st.warning(f"Menunggu data... Pastikan logger.py sedang berjalan dan folder '{OUTPUT_DIR}' ada.")
    st.stop()

# Mengambil daftar file CSV (daftar Node)
csv_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.csv')]

if not csv_files:
    st.info("Belum ada data dari Node yang masuk. Menunggu...")
    st.stop()

# Membuat Dropdown Menu di Sidebar untuk memilih Node
st.sidebar.header("Pilih Perangkat")
selected_file = st.sidebar.selectbox("Daftar Node Aktif", csv_files)

# Tempat (Placeholder) untuk grafik agar bisa di-update secara real-time
placeholder = st.empty()

# Tombol untuk menghentikan live update jika ingin melihat data diam
live_update = st.sidebar.checkbox("Aktifkan Live Update", value=True)

# Loop untuk Real-Time GUI
while True:
    file_path = os.path.join(OUTPUT_DIR, selected_file)
    
    # Membaca data CSV menggunakan Pandas
    try:
        df = pd.read_csv(file_path)
        
        # Mengubah kolom 'Waktu_Nyata' menjadi format datetime agar rapi di sumbu-X
        df['Waktu_Nyata'] = pd.to_datetime(df['Waktu_Nyata'])
        df = df.set_index('Waktu_Nyata')
        
        # Buang kolom yang tidak perlu di-plot (seperti Waktu Mesh dan Tipe Sensor)
        kolom_grafik = [col for col in df.columns if col not in ['Waktu_Mesh_us', 'Tipe_Sensor']]

        # Menggambar ulang ke dalam placeholder
        with placeholder.container():
            st.subheader(f"📊 Menampilkan Data: {selected_file}")
            
            # Menampilkan Metrik (Angka Terakhir) di atas grafik
            baris_terakhir = df.iloc[-1]
            kolom_metrik = st.columns(len(kolom_grafik))
            
            for i, col in enumerate(kolom_grafik):
                with kolom_metrik[i]:
                    nilai_terakhir = baris_terakhir[col]
                    st.metric(label=col.upper(), value=f"{nilai_terakhir}")
            
            st.markdown("---")
            
            # Menampilkan Grafik Garis Interaktif
            st.line_chart(df[kolom_grafik])
            
            # (Opsional) Tampilkan tabel mentahnya di bagian bawah
            with st.expander("Lihat Tabel Data Mentah"):
                st.dataframe(df.tail(10)) # Hanya tampilkan 10 baris terakhir

    except Exception as e:
        st.error(f"Gagal membaca data: {e}")
    
    # Jika mode live update dimatikan, keluar dari loop
    if not live_update:
        break
        
    # Jeda 2 detik sebelum memuat ulang CSV (agar CPU tidak kerja terlalu keras)
    time.sleep(2)