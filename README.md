# 🧠 SilverQueen Auto Bawuk

---

## 📌 Fitur

- 🔐 Menggunakan hingga 10 akun dari `token.txt`
- 📥 Mengambil ID cerita dari setiap akun
- 🤖 Klaim cerita akun lain secara otomatis
- 🚫 Melewati cerita jika:
  - Sudah diklaim
  - Dicoba klaim oleh pemilik cerita sendiri
- 🔁 Proses berulang per cerita dan akun
- 📋 Logging interaktif di terminal

---

## ⚙️ Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/namamu/botsilver.git
   cd botsilver
    ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Tambahkan token**
   Buat file `token.txt` dan isi dengan 1 token Bearer per baris:

   ```bash
   bearer 1292...
   ```

---

## 🚀 Cara Menjalankan

```bash
python silver.py
```

> Bot akan mulai mengambil cerita dari masing-masing token, lalu token lain akan mencoba mengklaimnya. Proses ini diulang hingga seluruh cerita diproses.

---

## 📌 Catatan Penting

* Token harus valid dan aktif.
* Pastikan tidak mencantumkan token pribadi jika membagikan proyek ini.
* Tidak mendukung login Google — hanya token Bearer.

---

## ⚠️ Disclaimer

Script ini hanya untuk **penelitian dan pembelajaran pribadi**. Tidak disarankan digunakan untuk aktivitas yang melanggar **Terms of Service** dari situs terkait.

---

## 📄 Lisensi

[MIT License](LICENSE)

