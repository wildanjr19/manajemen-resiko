# Hasil penelitian tanpa filter

Folder ini berisi output aktif dari [`replikasi_var_cvar.ipynb`](../replikasi_var_cvar.ipynb).
Seluruh return sah dipakai dalam estimasi dan evaluasi, termasuk nilai ekstrem.
Tidak ada penyaringan outlier pada alur utama.

| Lokasi | Isi |
|---|---|
| [`grafik/`](grafik/) | Grafik harga/return, normalitas, ACF, bobot, loss simulasi, konvergensi, dan backtesting |
| [`tabel/`](tabel/) | Hasil perhitungan, pengulangan MC, prediksi rolling, dan uji Kupiec |
| [`konfigurasi_eksekusi.json`](konfigurasi_eksekusi.json) | Parameter penelitian, sumber data, versi dependensi, dan status eksekusi |
| `checkpoint/` | Kemajuan rolling untuk melanjutkan run; diabaikan Git |

Data sumber tetap berada di `data/raw/`. Harga adjusted dan seluruh return sah
tersimpan di `data/processed/`. Nama `return_mentah.csv` berarti return tanpa
penyaringan nilai ekstrem.

Jalankan notebook dari root proyek untuk memperbarui output ini. Gunakan
`REFRESH_DATA=False` untuk memakai snapshot data yang tersimpan. Analisis
tersaring ditunda ke notebook terpisah. Folder `hasil/` dari skema sebelumnya
tidak lagi digunakan.
