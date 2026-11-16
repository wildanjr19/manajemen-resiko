# Outline Artikel TBP Manajemen Risiko — IJAS (v0.3)

**Status:** rancangan kerja yang disepakati untuk arah penelitian; detail tabel/gambar masih dapat disesuaikan.  
**Judul sementara:** *Estimasi VaR dan CVaR Portofolio Saham Perbankan melalui Simulasi Monte Carlo dan Backtesting*  
**Fokus:** replikasi pendekatan Monte Carlo normal dari Indarwati & Kusumawati (2021) pada BBCA, BMRI, dan BBRI. Metode parametrik normal dan historis hanya **pembanding**, bukan fokus yang setara.  
**Data/model:** return harian 10 November 2025–10 November 2026 (240 observasi sah); log return tanpa menghapus nilai ekstrem yang sah; portofolio GMV; Monte Carlo normal multivariat, 10.000 skenario × 100 pengulangan; VaR/CVaR 90%, 95%, 99%; rolling backtesting Kupiec (window 120 hari, 120 prediksi di luar sampel).

## Bagian awal artikel

- **Judul, penulis, afiliasi, corresponding author.** Ikuti format IJAS.
- **Abstrak (Indonesia dan Inggris).** Masing-masing satu paragraf, 150–250 kata; tujuan → metode → temuan utama → kesimpulan. **Ditulis terakhir.**
- **Kata kunci/Keywords.** 3–5 frasa per bahasa. Bagian *How to Cite* mengikuti template IJAS.

## 1. PENDAHULUAN

**Tanpa subbab; diusulkan enam paragraf yang saling mengalir.**

1. **Latar belakang:** investasi saham perbankan, fluktuasi return, dan kebutuhan pengukuran risiko portofolio.
2. **Ukuran risiko:** VaR sebagai ambang kerugian dan CVaR sebagai rata-rata kerugian pada ekor distribusi.
3. **Pemilihan metode:** konsep dan relevansi simulasi Monte Carlo; asumsi distribusi dapat membatasi pengukuran risiko ekstrem.
4. **Penelitian terdahulu:** ringkasan studi Indarwati & Kusumawati (2021), objek, tahapan, dan hasil yang relevan.
5. **Posisi penelitian:** tiga saham/periode berbeda; return ekstrem yang sah dipertahankan; backtesting rolling di luar sampel. **Jangan mengklaim metode baru.**
6. **Tujuan:** mengestimasi VaR/CVaR dengan Monte Carlo normal dan mengevaluasi estimasi VaR melalui pembanding serta uji Kupiec.

**Tabel/gambar:** tidak direncanakan; fokus pada argumen dan sitasi literatur.

## 2. METODE

### 2.1 Data Penelitian
- **Bahas:** BBCA.JK, BMRI.JK, BBRI.JK; Yahoo Finance (*Adj Close*); periode; penyelarasan tanggal; pemeriksaan data hilang; 240 return sah; nilai ekstrem yang valid tidak dihapus.
- **Tabel/gambar:** tidak wajib; karakteristik numerik disajikan pada Hasil 3.1.

### 2.2 Return dan Statistik Deskriptif
- **Bahas:** rumus log return; expected return, variansi, simpangan baku, kovarian, korelasi; satuan harian.
- **Tabel/gambar:** hasilnya masuk **Tabel 1** dan **Tabel 2** di bagian Hasil.

### 2.3 Diagnosis Distribusi Return
- **Bahas:** Lilliefors (α = 5%); Q–Q plot; ACF return/kuadrat return; konsekuensi penggunaan model normal ketika normalitas empiris ditolak.
- **Tabel/gambar:** hasil uji dalam **Tabel 1**; Q–Q plot/ACF dipertimbangkan sebagai visual tambahan bila diperlukan.

### 2.4 Pembentukan Portofolio
- **Bahas:** bobot *Global Minimum Variance* (GMV) berbasis invers matriks kovarian, tanpa kendala *short selling*; return dan variansi portofolio. Jelaskan perbedaan istilah GMV dengan MVEP pada paper acuan.
- **Tabel/gambar:** hasil masuk **Tabel 2**.

### 2.5 Simulasi Monte Carlo
- **Bahas:** pembangkitan log return normal multivariat berkorelasi (kovarian/Cholesky), return dan *loss* portofolio, horizon satu hari; 10.000 skenario per pengulangan dan 100 pengulangan; parameter dan bobot tetap pada sampel estimasi yang sama.
- **Tabel/gambar:** cukup persamaan dan uraian tahapan; alur visual opsional jika ruang tersedia.

### 2.6 Estimasi VaR dan CVaR
- **Bahas:** definisi *loss* sebagai negatif return log portofolio tertimbang; VaR sebagai kuantil *loss*; CVaR sebagai rata-rata ekor; rata-rata hasil 100 pengulangan, SD/SE Monte Carlo; ilustrasi Rp100 juta sebagai pendekatan linear.
- **Tabel/gambar:** hasil masuk **Tabel 3** dan **Gambar 2**.

### 2.7 Evaluasi dan Backtesting
- **Bahas:** konvergensi jumlah skenario (1.000/10.000/100.000); pembanding analitik normal dan historis; rolling window 120 observasi; prediksi satu hari ke depan; pelanggaran saat *loss aktual > VaR*; statistik dan keputusan uji Kupiec.
- **Tabel/gambar:** hasil masuk **Tabel 4–5** serta **Gambar 3–4**.

## 3. HASIL DAN PEMBAHASAN

### 3.1 Karakteristik Data dan Distribusi Return
- **Bahas:** ringkasan return tiap saham; volatilitas, skewness/kurtosis, fluktuasi ekstrem; hasil Lilliefors dan implikasi penolakan normalitas. Tambahkan hasil Q–Q/ACF secara selektif.
- **Tabel 1 — Statistik return dan diagnosis normalitas.** Usulan kolom: `Saham | Mean | Variansi | SD | Skewness | Excess kurtosis | Statistik Lilliefors | p-value`.
- **Gambar 1 —** deret waktu return BBCA, BMRI, dan BBRI (panel terpisah agar terbaca). **Opsional:** Q–Q plot bila perlu memperkuat pembahasan ekor distribusi.

### 3.2 Pembentukan dan Karakteristik Portofolio
- **Bahas:** struktur korelasi/kovarian; bobot GMV tiap saham; expected return, variansi, dan SD portofolio; interpretasi komposisi bobot.
- **Tabel 2 — Bobot GMV dan ukuran risiko portofolio.** Usulan format: `Saham | Bobot GMV (%)` dengan baris ringkasan terpisah untuk `Expected return portofolio | Variansi portofolio | SD portofolio` (atau ringkas di teks agar tabel tidak terlalu lebar).
- **Gambar:** tidak wajib.

### 3.3 Estimasi VaR dan CVaR melalui Simulasi Monte Carlo — **hasil utama**
- **Bahas:** estimasi 90%, 95%, 99%; kenaikan risiko menurut tingkat kepercayaan; perbedaan VaR dengan CVaR; ketidakpastian Monte Carlo; ilustrasi nominal Rp100 juta.
- **Tabel 3 — Estimasi risiko Monte Carlo.** Usulan kolom: `Tingkat kepercayaan | VaR (%) | CVaR (%) | SE VaR | SE CVaR`. SD antar-pengulangan dapat dijelaskan di teks atau ditambahkan bila ruang cukup.
- **Gambar 2 —** distribusi *loss* simulasi dengan ambang VaR (dan penanda/area CVaR jika terbaca jelas).

### 3.4 Konvergensi dan Perbandingan Estimasi
- **Bahas:** kestabilan hasil ketika skenario bertambah; kedekatan Monte Carlo dengan parametrik normal pada asumsi yang sama; perbedaan dari VaR historis sebagai pembanding empiris. **Tidak** menjadikan perbandingan tiga metode sebagai fokus utama.
- **Tabel 4 — Perbandingan VaR.** Usulan kolom: `Tingkat kepercayaan | VaR Monte Carlo (%) | VaR Parametrik Normal (%) | VaR Historis (%)`.
- **Gambar 4 (pendukung) —** konvergensi VaR/CVaR menurut jumlah skenario atau SE Monte Carlo. Jika ruang terbatas, cukup dinarasikan.

### 3.5 Evaluasi Backtesting Menggunakan Uji Kupiec — **hasil utama**
- **Bahas:** 120 tanggal evaluasi di luar sampel; jumlah pelanggaran aktual vs harapan; failure rate, statistik LR, p-value, keputusan Kupiec; hasil 90%/95%/99% dan keterbatasan evaluasi tail 99%. Kupiec **menguji VaR, bukan CVaR**.
- **Tabel 5 — Backtesting rolling out-of-sample.** Usulan kolom: `Metode | Tingkat kepercayaan | Jumlah uji (n) | Pelanggaran (x) | Ekspektasi pelanggaran | Failure rate | LR Kupiec | p-value | Keputusan`.
- **Gambar 3 —** deret waktu *loss* aktual versus VaR rolling (utamakan level 95% agar tidak padat); tandai tanggal pelanggaran.

### 3.6 Sintesis Temuan dan Keterbatasan
- **Bahas:** keterkaitan penolakan normalitas, hasil VaR/CVaR, perbandingan, dan Kupiec; posisi hasil terhadap studi acuan; keterbatasan asumsi normal, satu sektor, satu periode, horizon harian, dan sedikitnya pelanggaran yang diharapkan pada 99%. **Jangan menyimpulkan hubungan sebab-akibat tanpa pengujian.**
- **Tabel/gambar:** tidak perlu; sintesis naratif dari Tabel 1–5 dan Gambar 1–4.

## 4. KESIMPULAN

- **Paragraf 1:** jawaban atas tujuan estimasi VaR/CVaR dan interpretasi utama risiko ekor.
- **Paragraf 2:** hasil evaluasi Kupiec, batas penggunaan model normal, serta saran operasional yang didukung temuan.
- **Tabel/gambar:** tidak ada. Ditulis naratif, **maksimal 300 kata**.

## DAFTAR PUSTAKA

- Gaya sitasi **IEEE**; minimal **15 referensi**, sedikitnya **50%** dari 10 tahun terakhir; seluruh sitasi harus tercantum dalam daftar pustaka.

---

**Catatan penulisan IJAS:** naskah utama minimal 3.500 kata (di luar abstrak dan referensi); caption tabel di atas, caption gambar di bawah; semua tabel/gambar harus dirujuk dan diinterpretasikan. Penomoran tabel/gambar di atas bersifat sementara dan diperbarui sesuai output yang akhirnya dipilih.

**Status keputusan:** arah penelitian dan prinsip tanpa penghapusan return ekstrem **disepakati**; judul, jumlah visual, format tabel final, dan narasi tiap bagian **masih dapat diiterasi**.
