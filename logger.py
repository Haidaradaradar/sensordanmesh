import serial
import sys
import json
import csv
import os
from datetime import datetime

# ==========================================
# KONFIGURASI
# ==========================================

if len(sys.argv) < 2:
    print("Usage: python logger.py <COM_PORT>")
    sys.exit(1)
    
arg = sys.argv[1]

COM_PORT = arg  
BAUD_RATE = 115200
OUTPUT_DIR = 'data_sensor'

# Buat folder jika belum ada
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"[*] Menunggu data dari {COM_PORT}...")
print(f"[*] CSV akan dipisah per Node dan disimpan di folder '{OUTPUT_DIR}'\n")

try:
    arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)

    while True:
        raw_data = arduino.readline().decode('utf-8').strip()

        if raw_data:
            try:
                data = json.loads(raw_data)

                # Ekstrak metadata
                node_id = data.get("node")
                sensor_type = data.get("type")
                mesh_time = data.get("time")
                
                # Ekstrak data sensor (Dictionary)
                payload = data.get("data", {})

                real_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{real_time}] Menyimpan data dari Node {node_id}...")

                # ==========================================
                # LOGIKA PENYIMPANAN DINAMIS PER NODE
                # ==========================================
                # Nama file berdasarkan ID Node
                csv_filename = os.path.join(OUTPUT_DIR, f"node_{node_id}.csv")
                file_exists = os.path.isfile(csv_filename)

                with open(csv_filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Jika file baru pertama kali dibuat, tulis Headernya!
                    # Header otomatis mengambil Kunci (Keys) dari JSON payload
                    if not file_exists:
                        # Contoh Header: ['Waktu_Nyata', 'Waktu_Mesh_us', 'Tipe_Sensor', 'suhu', 'kelembaban']
                        headers = ['Waktu_Nyata', 'Waktu_Mesh_us', 'Tipe_Sensor'] + list(payload.keys())
                        writer.writerow(headers)

                    # Tulis nilai datanya (Values) berurutan sesuai kolom Header
                    row_data = [real_time, mesh_time, sensor_type] + list(payload.values())
                    writer.writerow(row_data)

            except json.JSONDecodeError:
                pass
            except Exception as e:
                print(f"[!] Terjadi kesalahan pemrosesan: {e}")

except serial.SerialException:
    print(f"[!] ERROR: Gagal membuka port {COM_PORT}.")
except KeyboardInterrupt:
    print("\n[*] Program dihentikan. Semua data aman.")