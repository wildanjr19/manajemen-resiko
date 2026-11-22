# Eksperimen tiga pembobotan

Notebook: [replikasi_var_cvar_artikel_3_pembobotan.ipynb](../notebooks/replikasi_var_cvar_artikel_3_pembobotan.ipynb).

Skema yang dibandingkan adalah GMV tanpa kendala short selling, sama rata, dan
bobot manual BBCA/BMRI/BBRI sebesar 50%/30%/20%. GMV diperbarui dari jendela
120 return sebelum setiap tanggal prediksi. Dua skema lainnya mempertahankan
target bobot harian, dengan penyeimbangan kembali tanpa biaya transaksi.

Ketiganya memakai data dan seed identik. Metode Monte Carlo, normal analitik,
dan historis menggunakan loss yang sama dalam satu skema; loss antarskema
dapat berbeda. Seluruh return ekstrem yang sah tetap digunakan.

- `tabel/tabel_1_*`: statistik aset dan normalitas, sama untuk semua skema.
- `tabel/tabel_2_*`: bobot dan karakteristik portofolio.
- `tabel/tabel_3_*`: risiko MC, SD antarpengulangan, dan SE rata-rata MC.
- `tabel/tabel_4_*`: pembanding normal analitik dan historis.
- `tabel/tabel_5_*`: Kupiec rolling di luar sampel untuk setiap skema dan metode.
- `grafik/`: diagnosis aset, bobot, konvergensi, dan loss/VaR rolling 95%.
- `konfigurasi_eksekusi.json`: parameter, aturan bobot, versi, dan identitas run.

Jalankan seluruh notebook dari root proyek atau `notebooks/`. Secara default,
MC memakai 10.000 skenario dan 100 pengulangan; konvergensi memakai 1.000,
10.000, dan 100.000 skenario. Rincian pengulangan, prediksi, data olahan, dan
checkpoint dibuat saat eksekusi, tetapi tidak dilacak Git. Checkpoint berada di
`tmp/checkpoint_3_pembobotan/`, dipisahkan oleh fingerprint skema dan run.

Angka risiko rinci disimpan dalam desimal. Tabel penyajian menyatakan persen
untuk risiko dan poin persentase untuk SD/SE. Sampel penuh bersifat retrospektif;
Kupiec tidak memvalidasi CVaR dan p-value terbesar bukan penentu skema terbaik.
Kalender BEI belum diverifikasi secara independen.
