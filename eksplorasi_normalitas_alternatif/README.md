# Uji normalitas alternatif

Analisis ini hanya menjadi diagnosis eksploratif tambahan. Script tidak mengubah
notebook utama, data sumber, atau output di `hasil_tanpa_filter/`.

Input mengikuti konfigurasi run notebook utama: BBCA.JK, BMRI.JK, dan BBRI.JK,
tanggal return 10 November 2025–10 November 2026. Seluruh 240 return sah
digunakan tanpa filtering, transformasi tambahan, atau penghapusan nilai ekstrem.
Script memeriksa kembali return terhadap log rasio harga adjusted yang sama.

Jalankan dari root proyek:

```powershell
python eksplorasi_normalitas_alternatif/uji_normalitas_alternatif.py
```

Hasil disimpan di folder ini:

- `hasil_uji.csv`: statistik, p-value atau nilai kritis, serta keputusan setiap uji per saham.
- `konfigurasi_uji.json`: periode, ukuran sampel, taraf uji, hash input/script, dan versi dependensi.

Pada seluruh uji, H0 menyatakan bahwa sampel berasal dari distribusi normal.
Taraf pengujian mengikuti notebook, yaitu 5%. Shapiro–Wilk dan D’Agostino–Pearson
menolak H0 jika p-value < 0,05. Anderson–Darling menolak H0 jika statistik A²
lebih besar daripada nilai kritis 5%. Fungsi Anderson–Darling pada SciPy 1.16.3
tidak mengembalikan p-value; kolom tersebut sengaja kosong untuk uji ini.

Tidak menolak H0 tidak membuktikan normalitas. Hasil tambahan tidak dipakai untuk
memilih uji yang memberikan keputusan paling diinginkan atau mengganti Lilliefors
pada alur utama. Pengujian ini bersifat marginal per saham, tidak membuktikan
normalitas multivariat. Kalibrasi standar pengujian mengasumsikan sampel independen;
ketergantungan waktu pada return perlu dibaca bersama diagnosis ACF notebook.
Hasil beberapa uji dilaporkan sebagai eksplorasi, tanpa klaim pengujian konfirmatori gabungan.

Rujukan fungsi, dokumentasi SciPy seri 1.16:

- [Shapiro–Wilk](https://docs.scipy.org/doc/scipy-1.16.0/reference/generated/scipy.stats.shapiro.html).
- [D’Agostino–Pearson](https://docs.scipy.org/doc/scipy-1.16.0/reference/generated/scipy.stats.normaltest.html).
- [Anderson–Darling](https://docs.scipy.org/doc/scipy-1.16.0/reference/generated/scipy.stats.anderson.html).
