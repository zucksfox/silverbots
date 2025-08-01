project:
  name: Bot Auto-Claim Cerita SilverQueen
  
features:
  - Looping semua bearer token dari token.txt
  - Auto get cerita dari masing-masing akun
  - Auto klaim cerita oleh akun lain
  - Skip otomatis jika cerita milik sendiri
  - Skip jika sudah diklaim (error: Message has already been claimed)
  - Log aksi setiap klaim

requirements:
  python: ">=3.8"
  dependencies:
    - requests

files:
  - token.txt  # berisi 1 token per baris
  - silver.py    # script utama
  - README.yaml

run:
  command: python main.py

token_format:
  file: token.txt
  content: |
    bearer token...
    ...

output_example: |
  📥 Mendapatkan cerita dari Token 1
  📤 Token 2 mencoba klaim → ✅ Berhasil
  📤 Token 3 mencoba klaim → ❌ Message has already been claimed
  📤 Token 4 mencoba klaim → ✅ Berhasil

handling:
  errors:
    - "You cannot claim your own message" : skip klaim
    - "Message has already been claimed" : lanjut ke cerita berikutnya
    - timeout or connection error : retry / skip

tips:
  - Gunakan max 5 akun per hari agar tidak over-limit
  - Upload cerita baru sebelum menjalankan bot
  - Token bisa diambil dari browser (DevTools → Network → Headers → Authorization)

disclaimer: >
  Script ini dibuat hanya untuk tujuan edukasi.
  Segala penyalahgunaan menjadi tanggung jawab pengguna masing-masing.

author: bawukxfahrur
