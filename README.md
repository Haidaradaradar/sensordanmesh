# ESP32 Sensor Logger

Projek ini ditujukan untuk matakuliah Sensor dan Aktuator FI2271.

Program ini digunakan untuk:
- menerima data mesh dari ESP32
- parsing JSON
- menyimpan data sensor ke file CSV secara otomatis

## Features

- Logging data otomatis
- CSV dipisah per Node
- Mendukung format JSON
- Menggunakan komunikasi serial

## Dependencies

- Python 3
- pyserial

Install dependency:

```bash
pip install pyserial
```

## Cara Menjalankan

```bash
python logger.py COM6
```

## Struktur JSON

Contoh data:

```json
{
  "node": 1,
  "type": "DHT11",
  "time": 123456,
  "data": {
      "souce": "DHT11",
      "temperature": 28
  }
}
```

## Credits

Shoutout untuk painlessMesh:  
https://github.com/gmag11/painlessMesh
