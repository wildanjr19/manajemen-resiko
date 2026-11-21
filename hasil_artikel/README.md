# Keluaran notebook versi artikel

Notebook: [replikasi_var_cvar_artikel.ipynb](../notebooks/replikasi_var_cvar_artikel.ipynb).
Versi ini menyiapkan hasil untuk [outline IJAS v0.3](../struktur-artikel/outline_artikel_menrisk_ijas_v03.md).
Notebook asal dan `hasil_tanpa_filter/` tetap menjadi pembanding.

| Bahan artikel | File |
|---|---|
| Tabel 1: statistik dan normalitas | `tabel/tabel_1_statistik_normalitas.csv` dan `.html` |
| Tabel 2: bobot dan karakteristik portofolio | `tabel/tabel_2_portofolio.csv` dan `.html` |
| Tabel 3: VaR/CVaR Monte Carlo | `tabel/tabel_3_risiko_mc.csv` dan `.html` |
| Tabel 4: pembanding VaR | `tabel/tabel_4_perbandingan_var.csv` dan `.html` |
| Tabel 5: backtesting di luar sampel | `tabel/tabel_5_backtesting_rolling.csv` dan `.html` |
| Gambar 1: tiga panel return | `grafik/gambar_1_return.png` |
| Gambar 2: distribusi loss ilustrasi | `grafik/gambar_2_distribusi_loss.png` |
| Gambar 3: loss dan VaR rolling 95% | `grafik/gambar_3_rolling_var95.png` |
| Gambar 4: konvergensi | `grafik/gambar_4_konvergensi.png` |

CSV menyimpan presisi penuh; HTML menyajikan tabel dengan caption dan pembulatan
untuk dibaca atau disalin ke naskah. Mean, SD, VaR, dan CVaR pada tabel artikel
ditampilkan dalam persen; SE dalam poin persentase; variansi memakai desimal kuadrat.
Failure rate pada Tabel 5 ditampilkan dalam persen.

Git menyimpan Tabel 1–5, Gambar 1–4, konfigurasi, dan petunjuk ini. Salinan data
olahan, tabel rinci perhitungan, serta grafik pendukung yang sudah tersedia pada
versi asal diabaikan Git dan dibuat ulang saat notebook dijalankan.

Jalankan notebook dari root proyek. Data sumber memakai snapshot `data/raw/`
dengan `REFRESH_DATA=False`; data olahan versi artikel disimpan di `data_processed/`.
Checkpoint versi artikel berada di `tmp/checkpoint_artikel/` dan dapat dibuat ulang.
Pada pemeriksaan awal versi ini, checkpoint asal disalin ke lokasi tersebut;
identitas data, konfigurasi, versi pustaka, dan implementasi tetap diperiksa
sebelum cache digunakan. Estimasi sampel penuh dan konvergensi dihitung ulang.

Interpretasi dan sintesis berada di notebook dan dibentuk dari hasil eksekusinya.
Verifikasi kalender BEI secara independen **belum dilakukan**. Diagnosis ACF
bersifat grafis; Kupiec menguji cakupan VaR dan tidak memvalidasi CVaR.
