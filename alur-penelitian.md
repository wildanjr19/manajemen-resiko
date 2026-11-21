# Alur Replikasi Penelitian
## Simulasi Monte Carlo untuk Menghitung VaR dan CVaR Portofolio Saham

**Mata kuliah:** Manajemen Risiko
**Paper referensi:** Indarwati, E. & Kusumawati, R. (2021). *Aplikasi Metode Simulasi Monte Carlo untuk Menghitung VaR dan CVaR pada Saham PT Bank Negara Indonesia (Persero) Tbk dan PT Bank Tabungan Negara (Persero) Tbk*. Jurnal Matematika, Statistika & Komputasi, Vol. 17 No. 3, 370–380. DOI: 10.20956/j.v17i3.11340

**Rencana data replikasi:** BBCA.JK, BMRI.JK, BBRI.JK; return harian bertanggal 10 November 2025 – 10 November 2026.
**Status:** metodologi v4, dengan pembaruan ruang lingkup pada 16 November 2026: [replikasi_var_cvar.ipynb](notebooks/replikasi_var_cvar.ipynb) hanya menganalisis seluruh return sah **tanpa penyaringan nilai ekstrem**. Analisis tersaring ditunda untuk notebook terpisah. Run menghasilkan 240 return dan 120 hari uji rolling. Satu-satunya folder output aktif adalah `hasil_tanpa_filter/` langsung di root proyek; folder `hasil/` lama tidak lagi berada di root proyek. Telaah rumus dan keterbandingan paper tetap berlaku.
**Prioritas:** selesaikan alur utama terlebih dahulu. Bootstrap, Student-t, dan bobot long-only merupakan analisis tambahan.

---

## 0. Tujuan dan Batas Penelitian

**Usulan judul:** *Replikasi Estimasi VaR dan CVaR Portofolio Saham BBCA, BMRI, dan BBRI Menggunakan Simulasi Monte Carlo pada Data Harian Periode 10 November 2025–10 November 2026*.

Tujuan utama adalah menerapkan pendekatan paper pada objek dan periode berbeda, dengan definisi risiko serta prosedur simulasi yang dapat direproduksi. Pertanyaan penelitian:

1. Berapa VaR dan CVaR satu hari portofolio GMV pada tingkat kepercayaan 90%, 95%, dan 99%?
2. Seberapa stabil estimasi terhadap jumlah skenario, dan seberapa dekat hasil MC dengan solusi analitik dari model normal yang sama?
3. Bagaimana cakupan VaR MC, parametrik normal, dan historis pada data di luar sampel ketika seluruh return ekstrem yang sah tetap disertakan?

BBCA, BMRI, dan BBRI dipilih sebagai tiga objek saham perbankan untuk mempertahankan konteks sektoral paper sekaligus mengganti komposisi portofolio. Ketiganya tidak disebut sebagai kelompok bank BUMN karena BBCA bukan bank BUMN. Pemilihan ini merupakan studi kasus, bukan bukti keterwakilan seluruh pasar atau hasil seleksi portofolio terbaik. Periode 10 November 2025–10 November 2026 ditetapkan sesuai pembaruan pengguna; jangan mengganti saham/periode berdasarkan hasil normalitas atau backtesting.

**Dua keluaran utama dibedakan:** tabel estimasi dari seluruh sampel 10 November 2025–10 November 2026 untuk mereplikasi bentuk hasil paper, serta evaluasi rolling 120 observasi untuk menilai prediksi di luar sampel. Tabel sampel penuh bersifat retrospektif; rolling merupakan pengembangan evaluasi karena pemisahan sampel paper tidak dijelaskan. Keduanya memakai seluruh return sah tanpa penyaringan. Perbandingan dengan hasil tersaring berada di luar cakupan notebook utama dan akan dikerjakan dalam notebook tersendiri.

Tambahan seperti bootstrap, Student-t, GMV long-only, dan return sederhana eksak tidak menjadi syarat penyelesaian replikasi. Penelitian ini mengestimasi risiko; optimasi CVaR dan pengujian kinerja investasi setelah biaya berada di luar cakupan utama.

---

## 1. Ringkasan Paper Referensi

| Aspek | Isi paper |
|---|---|
| Objek | BBNI (BNI) dan BBTN (BTN), dua bank BUMN |
| Periode | 6 Januari 2019 – 30 Desember 2019, sebagaimana tertulis di paper |
| Observasi | Paper menyebut 245 pengamatan setelah penghapusan outlier |
| Sumber | Harga penutupan harian dari Yahoo Finance melalui RStudio |
| Ukuran risiko | VaR dan CVaR pada 90%, 95%, 99%, horizon 1 hari |
| Metode | Monte Carlo; pembanding VaR parametrik dan historis |
| Pembobotan | Disebut MVEP; rumusnya menghasilkan global minimum variance portfolio (GMV) |
| Bobot hasil | BNI sekitar 67%, BTN sekitar 33% |
| Pengulangan | 100 kali, kemudian dirata-ratakan |
| Evaluasi | Backtesting VaR dengan Kupiec |

**Angka yang dilaporkan paper, mengikuti Tabel 3.1–3.2:**

| Tingkat kepercayaan | 90% | 95% | 99% |
|---|---|---|---|
| VaR | 4,85% | 5,69% | 6,77% |
| SE VaR | 0,59% | 0,58% | 0,58% |
| CVaR | 5,82% | 6,39% | 7,10% |
| SE CVaR | 0,58% | 0,59% | 0,59% |

Dengan dana Rp 100.000.000, CVaR tersebut setara Rp 5.820.000 / Rp 6.390.000 / Rp 7.100.000. Interpretasi dalam replikasi adalah **rata-rata kerugian pada ekor terburuk**, bukan batas maksimum kerugian. Kerugian aktual dapat melebihi CVaR.

Tabel 3.3 melaporkan p-value backtesting: parametrik 0 / 0 / 0, historis 0 / 0 / 0, dan Monte Carlo 1 / 1 / 0,9221. Ini hasil yang dilaporkan penulis, bukan target hasil replikasi. Tidak ditolaknya model oleh Kupiec tidak membuktikan akurasi model secara menyeluruh.

**Informasi yang belum memadai:** jumlah skenario per pengulangan, aturan outlier, perhitungan SE, implementasi korelasi simulasi, dan pemisahan estimasi/pengujian. Bagian hasil menyebut Kolmogorov–Smirnov, sedangkan tinjauan pustaka menjelaskan Lilliefors. Pilihan operasional replikasi dijelaskan di §4, bukan dianggap sebagai rincian yang pasti digunakan penulis.

---

## 2. Alur Replikasi Utama (11 Langkah)

Kerangka 11 langkah paper dipertahankan dengan perbaikan notasi dan interpretasi. Urutan bobot dan simulasi ditukar agar dependensi lebih jelas: bobot ditentukan dari data estimasi sebelum digunakan pada skenario. Perubahan objek, keputusan operasional, dan pengembangan evaluasi dijelaskan di §3–4.

**Alur ringkas:** harga dan kualitas data → log return tanpa penyaringan nilai ekstrem → diagnosis distribusi dan waktu → estimasi parameter → bobot GMV → simulasi berkorelasi → loss portofolio → VaR/CVaR dan galat MC → pembanding analitik/historis → backtesting di luar sampel → pembahasan.

**Notasi:** $d=3$ aset, $T$ observasi return, $M$ skenario per pengulangan, $K=100$ pengulangan, $c$ tingkat kepercayaan, dan $p=1-c$ probabilitas pelanggaran. Taraf signifikansi pengujian ditulis $a=0{,}05$ agar tidak tertukar dengan probabilitas ekor.

### Langkah 1 — Menghitung return aset

Hitung log return dari harga yang telah disesuaikan:

$$r_{i,t}=\ln\left(\frac{P_{i,t}}{P_{i,t-1}}\right).$$

Output: matriks $T\times d$, tanggal pada baris dan saham pada kolom. Gunakan interval perdagangan yang sama untuk ketiga saham; penanganan data hilang mengikuti D1.

### Langkah 2 — Diagnosis distribusi dan uji normalitas

Pertahankan seluruh return yang sah, termasuk nilai ekstrem. Tidak ada penghapusan berdasarkan z-score atau keputusan uji normalitas. Koreksi kesalahan data mengikuti pemeriksaan kualitas D1; analisis penyaringan ditunda mengikuti D3.

Lakukan Lilliefors per saham pada seluruh return sah:

$$D=\sup_x|F_N(x)-F_{\hat\mu,\hat\sigma}(x)|.$$

$F_N$ adalah CDF empiris dari $N$ return yang sedang diuji. $H_0$: sampel berasal dari distribusi normal dengan parameter yang diestimasi. Tolak $H_0$ jika p-value $<a$. Gunakan p-value/nilai kritis Lilliefors, bukan tabel KS biasa untuk parameter yang diketahui.

Tidak menolak $H_0$ bukan bukti normalitas. Normalitas marginal setiap saham juga tidak membuktikan normalitas multivariat. Model normal tetap dijalankan sebagai asumsi replikasi dan ketidaksesuaiannya dilaporkan.

**Pada backtesting:** seluruh return sah dalam jendela pelatihan dipakai dan semua tanggal uji yang sah tetap dinilai, termasuk return ekstrem; lihat D3 dan D9.

### Langkah 3 — Mengestimasi parameter risiko

Dari $N$ baris sampel estimasi yang dipakai:

$$\hat\mu_i=\frac{1}{N}\sum_{t=1}^N r_{i,t},\qquad
\hat\Sigma=\frac{1}{N-1}\sum_{t=1}^N(\mathbf r_t-\hat\mu)(\mathbf r_t-\hat\mu)',\qquad
\hat\sigma_i=\sqrt{\hat\Sigma_{ii}}.$$

Output: mean, standar deviasi, matriks kovarian $3\times3$, dan matriks korelasi. Semua parameter memakai satuan harian dan return desimal.

### Langkah 4 — Menentukan bobot portofolio

Gunakan rumus yang disebut MVEP dalam paper:

$$\mathbf w=\frac{\hat\Sigma^{-1}\mathbf1}{\mathbf1'\hat\Sigma^{-1}\mathbf1},\qquad \mathbf1'\mathbf w=1.$$

Secara spesifik, ini bobot **GMV tanpa kendala short selling**, yaitu minimum varians tanpa target return. Bobot negatif dapat muncul pada dua maupun tiga aset.

Bobot dihitung dari sampel estimasi dan tetap untuk seluruh skenario pada satu tanggal prediksi. Parameter dan bobot tidak diestimasi ulang dari setiap sampel simulasi. Pembaruan antarhari mengikuti D6 dan D9.

### Langkah 5 — Simulasi log return multivariat

Bangkitkan:

$$\mathbf r^{(m)}=\hat\mu+L\mathbf z^{(m)},\qquad
\mathbf z^{(m)}\sim N(0,I_d),\qquad LL'=\hat\Sigma.$$

Output: matriks $M\times3$, dengan $M=10.000$. Jika skenario disimpan sebagai baris, implementasinya adalah $ZL'+\hat\mu$. Skenario $m$ saling independen sebagai penarikan dari distribusi prediktif satu hari; $M$ bukan jumlah hari proyeksi dan bukan ukuran sampel pasar tambahan.

Cholesky menjaga kovarian antaraset. Simulasi independen antaraset menghilangkan kovarian dan mengubah risiko; jika semua bobot nonnegatif dan semua kovarian silang positif, mengabaikan kovarian menurunkan varians sehingga dapat meremehkan risiko. Arah perubahan tidak dijamin sama bila ada posisi short atau kovarian negatif.

### Langkah 6 — Menghitung pendekatan return portofolio

Mengikuti bentuk linear paper:

$$\tilde r_p^{(m)}=\mathbf w'\mathbf r^{(m)}.$$

Ini pendekatan terhadap return sederhana portofolio untuk horizon harian, bukan identitas agregasi log return. Return sederhana yang sesuai perubahan nilai portofolio satu hari adalah:

$$R_p^{(m)}=\sum_{i=1}^d w_i\left(e^{r_i^{(m)}}-1\right).$$

Alur utama memakai $\tilde r_p$ secara konsisten untuk ketiga metode serta loss aktual. Konversi rupiahnya juga merupakan pendekatan. Perhitungan dengan $R_p$ dapat ditambahkan sebagai sensitivitas dengan definisi loss yang disesuaikan bersama pada semua metode.

### Langkah 7 — Estimasi VaR

Definisikan loss relatif $\ell^{(m)}=-\tilde r_p^{(m)}$. Untuk $c\in\{0{,}90;0{,}95;0{,}99\}$:

$$\operatorname{VaR}_c=q_c(\ell)=-q_{1-c}(\tilde r_p).$$

Gunakan estimator kuantil sampel dengan interpolasi linear tipe 7 (Hyndman–Fan) yang sama untuk MC dan historis. Ini estimator kuantil populasi, bukan invers CDF empiris bertangga secara literal. VaR adalah ambang kerugian pada probabilitas tertentu, bukan kerugian maksimum mutlak. Nilai disimpan sebagai desimal dan tidak dipaksa positif jika kuantil loss ternyata negatif.

Contoh konvensi: VaR 95% memakai kuantil 95% **loss**, setara negatif kuantil 5% **return**. Kuantil 95% return justru berada di ekor keuntungan; istilah “kuartil” pada uraian paper dibaca sebagai kuantil/persentil sesuai tingkat yang dimaksud.

Untuk pemeriksaan analitik pada model normal linear:

$$\mu_p=\mathbf w'\hat\mu,\qquad \sigma_p=\sqrt{\mathbf w'\hat\Sigma\mathbf w},\qquad
\operatorname{VaR}^{\mathrm{normal}}_c=-\mu_p+\Phi^{-1}(c)\sigma_p.$$

Nilai rupiah pendekatan diperoleh dengan mengalikan $V_0$. Ini turunan model normal, bukan kutipan literal persamaan (2.7.1) paper. Persamaan paper ditulis $W_0R^*\sqrt t$; replikasi menetapkan konvensi tanda loss dan membatasi horizon satu hari.

### Langkah 8 — Estimasi CVaR

Untuk distribusi kontinu yang disimulasikan:

$$\operatorname{CVaR}_c=\mathbb E[\ell\mid\ell\ge\operatorname{VaR}_c],\qquad
\widehat{\operatorname{CVaR}}_c=\frac{1}{N_{\mathrm{ekor}}}\sum_{m:\ell^{(m)}\ge\widehat{\operatorname{VaR}}_c}\ell^{(m)}.$$

CVaR adalah rata-rata loss pada ekor terburuk sebesar $1-c$, bukan batas maksimum. Pemeriksaan analitik model normal linear:

$$\operatorname{CVaR}^{\mathrm{normal}}_c=-\mu_p+\sigma_p\frac{\phi(\Phi^{-1}(c))}{1-c}.$$

$\Phi$ dan $\phi$ adalah CDF dan densitas normal standar. Rata-rata ekor sampel di atas merupakan estimator untuk model kontinu. Dengan $M=10.000$ dan level yang dipilih, jumlah skenario ekor tanpa ties adalah 1.000, 500, dan 100; laporkan jumlah aktual pada tiap perhitungan.

Jika CVaR historis kelak ditambahkan, atau ukuran simulasi diubah sehingga $M(1-c)$ tidak bulat, gunakan expected shortfall empiris dengan massa ekor tepat $1-c$. Untuk $N$ loss terurut dari terbesar $\ell_{[1]}\ge\cdots\ge\ell_{[N]}$, tetapkan $h=N(1-c)$ dan $j=\lfloor h\rfloor$:

$$\widehat{\operatorname{ES}}_c=\frac{\sum_{k=1}^{j}\ell_{[k]}+(h-j)\ell_{[j+1]}}{h}.$$

Jika $h$ bulat, suku pecahan dihilangkan. Pembobotan ini juga menangani nilai berulang di ambang. Sekadar merata-ratakan semua observasi yang melampaui kuantil terinterpolasi tidak selalu menghasilkan ES empiris yang tepat, bahkan tanpa ties bila $h$ tidak bulat. CVaR historis tetap merupakan tambahan; pembanding utama historis pada penelitian ini adalah VaR.

### Langkah 9 — Mengulangi simulasi

Ulangi Langkah 5–8 sebanyak $K=100$ kali dengan parameter dan bobot pada Langkah 3–4 tetap. Setiap pengulangan menggunakan skenario baru. Tetapkan seed sekali di awal dan jangan meresetnya ke nilai sama pada setiap pengulangan. Kuantil dihitung per pengulangan lalu dirata-ratakan; menggabungkan seluruh skenario sebelum mengambil satu kuantil adalah estimator berbeda dan tidak menggantikan hasil utama ini.

### Langkah 10 — Menghitung rata-rata dan galat Monte Carlo

Untuk $\theta$ berupa VaR atau CVaR:

$$\bar\theta=\frac{1}{K}\sum_{k=1}^K\hat\theta_k,\qquad
s_{\mathrm{MC}}=\sqrt{\frac{1}{K-1}\sum_{k=1}^K(\hat\theta_k-\bar\theta)^2},\qquad
SE_{\mathrm{MC}}(\bar\theta)=\frac{s_{\mathrm{MC}}}{\sqrt K}.$$

Laporkan rata-rata, SD antar pengulangan, dan SE rata-rata secara terpisah. SE ini mengukur galat simulasi bersyarat pada parameter estimasi, bukan seluruh ketidakpastian estimator dari data. Definisi SE paper tidak cukup rinci untuk dipastikan identik.

### Langkah 11 — Backtesting VaR dengan Kupiec

Untuk tiap tanggal uji:

$$I_t=\mathbf1\{\ell_t>\widehat{\operatorname{VaR}}_{c,t}\},\qquad x=\sum_{t=1}^n I_t,\qquad p=1-c.$$

$H_0$: probabilitas pelanggaran sama dengan $p$. Statistik:

$$LR_{\mathrm{POF}}=-2\ln\left[\frac{(1-p)^{n-x}p^x}{(1-x/n)^{n-x}(x/n)^x}\right]\xrightarrow{d}\chi^2_1\quad(n\to\infty).$$

Tolak $H_0$ jika p-value $<a=0{,}05$. Hitung melalui log-likelihood, gunakan $0\ln0=0$, serta tangani $x=0$ dan $x=n$ agar tidak menghasilkan NaN. Gunakan bentuk selisih log-likelihood di atas; persamaan (2.10.1) pada PDF mencetak tanda perkalian di antara dua suku log sehingga tidak disalin secara literal.

Kalibrasi likelihood mengasumsikan indikator pelanggaran mengikuti Bernoulli independen dengan peluang tetap $p$ di bawah model acuan. Kupiec menguji cakupan tak bersyarat VaR; statistik ini tidak menguji independensi pelanggaran, besar kerugian ekor, atau validitas CVaR. Ketergantungan pelanggaran dapat memengaruhi kalibrasi p-value. Evaluasi lengkap mengikuti D9.

---

## 3. Cakupan Replikasi dan Pengembangan

| Komponen | Paper | Replikasi |
|---|---|---|
| Objek/periode | BBNI, BBTN tahun 2019 | BBCA, BMRI, BBRI periode 10 November 2025–10 November 2026 |
| Harga | Harga penutupan; penyesuaian tidak dirinci | Adjusted close; perbedaan definisi data dinyatakan |
| Kovarian | $2\times2$ | $3\times3$ |
| Pembobotan | Rumus MVEP/GMV, hasil positif | Rumus sama; bobot negatif dilaporkan jika muncul |
| Outlier | Dihapus, aturan tidak dijelaskan | Seluruh return ekstrem yang sah dipertahankan; penyaringan ditunda ke notebook terpisah |
| Normalitas | Lilliefors di teori, KS di hasil | Lilliefors secara eksplisit |
| Simulasi | Detail korelasi dan jumlah skenario tidak memadai | Normal multivariat via Cholesky, $M=10.000$ |
| Pengulangan | 100 | 100 dengan skenario baru dan parameter tetap |
| VaR/CVaR | Kuantil dan rata-rata ekor | Konvensi loss dan pendekatan return dijelaskan |
| SE | Prosedur tidak dijelaskan memadai | SE Monte Carlo eksplisit; bootstrap opsional |
| Backtesting | Kupiec; pemisahan sampel tidak jelas | Rolling di luar sampel sebagai pengembangan; in-sample deskriptif |

**Inti yang dipertahankan:** log return harian, pembobotan sesuai rumus paper, model normal untuk simulasi Monte Carlo, VaR/CVaR pada 90/95/99%, 100 pengulangan, horizon satu hari, dan evaluasi VaR melalui Kupiec.

Perubahan objek dan pilihan operasional dinyatakan terbuka. Tujuannya mereplikasi pendekatan pada data berbeda dengan prosedur yang dapat direproduksi. Angka maupun urutan kelayakan metode tidak ditargetkan sama dengan paper.

---

## 4. Keputusan Metodologi v4

| Kode | Komponen | Keputusan |
|---|---|---|
| D1 | Data | Adjusted close tiga saham; tanggal return 10 Nov 2025 – 10 Nov 2026 |
| D2 | Return | Log return aset dan pendekatan linear return portofolio |
| D3 | Return ekstrem | Tetap disertakan dalam estimasi dan evaluasi; tanpa penyaringan pada notebook utama |
| D4 | Normalitas | Lilliefors taraf 5%; ketidaksesuaian asumsi dilaporkan |
| D5 | Simulasi | Normal multivariat, 10.000 skenario × 100 pengulangan; cek analitik dan konvergensi |
| D6 | Bobot | GMV tanpa kendala sebagai utama; diperbarui per jendela prediksi |
| D7 | Risiko | Loss desimal; VaR kuantil kanan loss, CVaR rata-rata ekor kontinu |
| D8 | Ketidakpastian | SE rata-rata MC sebagai utama; bootstrap sebagai tambahan |
| D9 | Evaluasi | Kupiec rolling 120 observasi return mentah; in-sample deskriptif |
| D10 | Pelaporan | Rp 100 juta, seed tetap, data/konfigurasi tersimpan, presisi sesuai hasil |

### D1 — Periode, sumber, dan kualitas data

1. Unduh harga dari Yahoo Finance. Simpan data sumber, waktu unduh, definisi kolom, versi alat, dan pengaturan penyesuaian. Pastikan harga tidak disesuaikan dua kali.
2. Targetkan **tanggal return** 10 November 2025 – 10 November 2026. Ambil satu harga pada hari bursa terakhir sebelum awal periode agar return tanggal pertama tersedia. Jika hanya ada $N$ harga di dalam periode, return internal berjumlah $N-1$.
3. Urutkan tanggal; periksa duplikasi, harga tidak positif, data hilang, dan penyesuaian aksi korporasi. Jangan forward fill harga hilang untuk menciptakan return nol.
4. Selaraskan harga terlebih dahulu dan hitung return pada interval perdagangan yang sama. Jika ada kekosongan pada hari bursa untuk satu saham, verifikasi/perbaiki dari sumber. Jika tidak terselesaikan, keluarkan interval terdampak untuk semua saham dan dokumentasikan; jangan menyamarkan return beberapa hari sebagai return satu hari.
5. Laporkan jumlah harga dan return aktual; jangan memaksakan 245 observasi. Rentang satu tahun dipilih agar sebanding, bukan agar jumlah pengamatannya persis sama.

Adjusted close memperhitungkan penyesuaian aksi korporasi. Bila seri mencakup penyesuaian dividen, interpretasi return mengikuti seri tersebut. Perbedaannya dari harga penutupan yang tidak disesuaikan dinyatakan dalam laporan.

### D2 — Return dan pendekatan kerugian

Gunakan log return aset dan $\tilde r_p=\mathbf w'\mathbf r$ pada alur utama. Loss aktual backtesting adalah $\ell_t=-\mathbf w_t'\mathbf r_t$, dengan bobot tersedia sebelum tanggal $t$.

Semua metode memakai definisi tersebut. Pendekatan rupiah $V_0\ell_t$ tidak disebut sebagai perubahan nilai portofolio eksak. Sensitivitas menggunakan return sederhana eksak pada Langkah 6 bersifat tambahan dan harus konsisten pada semua metode.

### D3 — Return ekstrem dan pencegahan kebocoran data

**Estimasi penuh untuk tabel replikasi:** gunakan semua return sah pada periode penelitian tanpa menghapus nilai ekstrem. Hasil estimasi penuh tidak disebut sebagai prediksi di luar sampel. Outlier bukan otomatis kesalahan data; koreksi kualitas data memerlukan kesalahan yang terverifikasi.

**Rolling:** ambil seluruh 120 observasi return sah terakhir sebelum tanggal uji. Mean, kovarian, dan bobot dihitung hanya dari jendela tersebut. Jangan menggunakan statistik seluruh tahun atau membuang tanggal pelatihan maupun tanggal uji berdasarkan besar return atau hasil normalitas.

**Rancangan notebook tersaring untuk tahap berikutnya:** gunakan satu kali aturan $|z|>3$ pada sampel estimasi terkait, keluarkan seluruh baris tanggal yang ditandai, dan hitung ulang parameter serta bobot. Pada rolling, pelajari aturan hanya dari 120 return sebelum tanggal prediksi; tanggal uji tetap utuh. Jangan mengulang penyaringan sampai normalitas diterima. Bandingkan dengan hasil tanpa filter pada tanggal uji yang sama dan laporkan perubahan sampel, parameter, bobot, risiko, serta pelanggaran. Rancangan ini belum menjadi bagian dari eksekusi notebook utama.

### D4 — Diagnosis normalitas

Lakukan Lilliefors per saham pada seluruh return sah, taraf 5%, dilengkapi histogram dan Q–Q plot. Jarque–Bera dapat menjadi pelengkap dengan catatan keterbatasan pendekatan asimtotik pada sampel kecil.

Diagnosis utama disajikan pada sampel penuh; pada rolling, hasil diagnosis tidak dipakai untuk memilih jendela mana yang boleh diuji. Gunakan prosedur yang sama pada seluruh tanggal. Jika alat mengembalikan batas p-value dari tabel Lilliefors, tulis sebagai batas (misalnya $p\le0{,}001$), bukan angka eksak.

Jika normalitas ditolak, jalankan model normal sebagai asumsi replikasi dan laporkan ketidaksesuaian. Normalitas bukan syarat Monte Carlo secara umum. Tidak menolak uji marginal bukan bukti normalitas multivariat. Jika notebook tersaring nanti dibuat, hasil uji setelah penyaringan harus dilabeli eksploratif karena seleksi sampel memengaruhi distribusi dan kalibrasi p-value.

**Diagnosis waktu:** periksa grafik return serta ACF return dan kuadrat return pada seri mentah yang sah dan berurutan. Jangan menghitung ACF seolah tanggal yang dibuang sebagai outlier tetap bersebelahan; jika ada interval data yang hilang, jelaskan penanganannya. Model utama menganggap mean dan kovarian konstan pada setiap sampel/jendela estimasi serta tidak memodelkan dinamika volatilitas secara eksplisit. Autokorelasi atau pengelompokan volatilitas dilaporkan sebagai keterbatasan; uji normalitas saja tidak menilai asumsi tersebut. Penambahan GARCH tidak diwajibkan.

Student-t multivariat merupakan tambahan setelah alur utama selesai. Jika digunakan, tetapkan cara estimasi derajat bebas dan matriks scale. Untuk $\nu>2$, kovarian Student-t adalah $\nu/(\nu-2)$ kali matriks scale; keduanya tidak boleh langsung disamakan.

### D5 — Simulasi dan pemeriksaan hasil

- Gunakan $M=10.000$, $K=100$, horizon satu hari. Parameter dan bobot tetap antar pengulangan pada sampel estimasi yang sama.
- Seed utama 2024. Gunakan aliran acak turunan yang dapat direproduksi untuk pengulangan, tanggal prediksi, dan tambahan; simpan pemetaannya. Jangan mereset seed sama pada tiap pengulangan.
- Periksa mean dan kovarian skenario terhadap input. Pastikan kovarian simetris dan positif definit sebelum Cholesky. Jangan menambah regularisasi atau membuang aset diam-diam; jika diperlukan, dokumentasikan perubahan model.
- Bandingkan $M=1.000$, $10.000$, dan $100.000$ pada estimasi penuh dengan pengulangan independen. Laporkan perubahan estimasi dan SE. Sekitar 100 skenario ekor pada level 99% per pengulangan belum menjamin CVaR stabil.
- Bandingkan rata-rata MC dengan VaR/CVaR analitik Langkah 7–8. Selisih besar dibanding galat MC harus diperiksa sebelum hasil dipakai. Galat MC kecil juga tidak menghilangkan bias estimator kuantil/ekor pada $M$ terbatas.

Normal multivariat dan portofolio linear menghasilkan distribusi risiko yang sama untuk MC dan parametrik. Keduanya seharusnya mendekat saat skenario bertambah. Pelanggaran masih dapat berbeda jika loss aktual dekat ambang; keunggulan sistematis MC tidak diasumsikan.

GBM cukup sebagai konteks teori. Implementasi utama langsung mensimulasikan log return satu hari; jangan menambahkan koreksi drift GBM pada mean log return sampel atau membangun jalur harga yang tidak diperlukan.

### D6 — Bobot dan kebijakan antarhari

Gunakan GMV tanpa kendala short selling sebagai utama. Secara numerik, selesaikan $\hat\Sigma\mathbf v=\mathbf1$, lalu $\mathbf w=\mathbf v/(\mathbf1'\mathbf v)$; invers eksplisit tidak diperlukan.

Untuk tabel penuh, bobot dihitung sekali dari seluruh return sah. Pada rolling, hitung ulang dari jendela pelatihan setiap tanggal dan gunakan untuk prediksi serta loss aktual hari berikutnya. Ketiga metode memakai bobot identik pada setiap tanggal prediksi.

Ini strategi dengan pembaruan bobot harian untuk evaluasi satu hari, bukan buy and hold sepanjang tahun. Pada buy and hold, jumlah saham tetap dan bobot nilai pasar berubah. Biaya transaksi, biaya short selling, dan likuiditas tidak dimodelkan; hasil bukan kinerja neto setelah biaya.

Jika ada bobot negatif, jelaskan posisi short dan eksposur bruto $\sum_i|w_i|$. GMV long-only merupakan tambahan: minimalkan $w'\hat\Sigma w$, dengan $w_i\ge0$ dan $\sum_iw_i=1$.

### D7 — Definisi risiko dan metode pembanding

- **Monte Carlo:** kuantil loss skenario dan rata-rata ekor, dirata-ratakan dari 100 pengulangan.
- **Parametrik normal:** rumus analitik Langkah 7; CVaR analitik untuk pemeriksaan simulasi.
- **Historis:** bentuk loss dari return sampel estimasi dengan bobot prediksi yang sama, lalu ambil kuantil empiris loss.

Pada rolling, semua metode memakai seluruh 120 return sah dalam jendela yang sama, serta definisi loss dan tanggal evaluasi yang sama. Pada level 99% dengan sekitar 120 observasi, kuantil historis ditentukan sangat sedikit titik ekor sehingga interpolasi berpengaruh.

Periksa urutan VaR/CVaR antar tingkat kepercayaan dan $\operatorname{CVaR}_c\ge\operatorname{VaR}_c$. Ini pemeriksaan konsistensi, bukan bukti kesesuaian model dengan data.

### D8 — Galat Monte Carlo dan bootstrap

**Utama:** laporkan $s_{\mathrm{MC}}$ dan $SE_{\mathrm{MC}}(\bar\theta)=s_{\mathrm{MC}}/\sqrt{100}$. Skenario tambahan mengurangi galat simulasi, bukan menambah informasi pasar pada sampel historis.

**Bootstrap tambahan:** gunakan $B=1.000$ resample baris tanggal dengan pengembalian, ketiga saham sekaligus. Untuk ketidakpastian seluruh prosedur estimasi penuh tanpa filter, resample seluruh return sah, lalu estimasi ulang mean, kovarian, dan bobot tanpa penyaringan. Gunakan rumus normal analitik per resample agar galat MC tambahan tidak mencampuri ukuran ini. Jika ditambahkan pada notebook tersaring nanti, penyaringan satu kali diterapkan kembali di dalam setiap resample.

$$SE_{\mathrm{boot}}=\sqrt{\frac{1}{B-1}\sum_{b=1}^B(\hat\theta_b^*-\bar\theta^*)^2}.$$

**Tidak dibagi lagi dengan $\sqrt B$.** Ukuran ini mencakup perubahan bobot, bukan hanya risiko untuk bobot tetap. Resampling baris menjaga pasangan antaraset, tetapi bootstrap iid tidak menjaga ketergantungan waktu; laporkan keterbatasannya dan pertimbangkan block bootstrap bila diperlukan.

Prosedur SE paper tidak cukup rinci untuk memastikan sumber angka sekitar 0,58%. Tidak ada target bahwa SE replikasi atau bootstrap harus mendekatinya.

### D9 — Backtesting di luar sampel

Gunakan rolling window **120 observasi return mentah**. Untuk setiap tanggal $t$ setelah jendela awal:

1. Ambil return $t-120$ sampai $t-1$, tanpa informasi tanggal $t$ atau sesudahnya.
2. Pertahankan seluruh 120 return sah dalam jendela tanpa penyaringan nilai ekstrem, mengikuti D3.
3. Estimasi parameter dan bobot. Periksa ukuran sampel dan kovarian. Jika estimasi gagal, hentikan dan periksa penyebab; jangan melewati tanggal diam-diam.
4. Hitung VaR satu hari dengan parametrik, historis, dan MC. MC memakai 10.000 skenario × 100 pengulangan per tanggal.
5. Hitung loss aktual menggunakan bobot prediksi yang sama. Tanggal uji dengan return ekstrem yang sah tetap dinilai.
6. Catat VaR, loss, indikator pelanggaran, bobot, dan ukuran sampel estimasi. Geser satu tanggal dan ulangi.

Jika tersedia $T$ return sah dan semua prediksi berhasil, jumlah uji $n=T-120$. Laporkan jumlah aktual, bukan menjanjikan tepat 120 hari uji. Semua metode dievaluasi pada tanggal dan loss aktual identik. Dalam pengembangan tersaring nanti, perubahan penyaringan juga dapat mengubah bobot sehingga perbandingan tersebut menilai dua prosedur pembentukan portofolio.

Laporkan per metode dan level pada analisis tanpa filter: $n$, pelanggaran aktual $x$, **jumlah pelanggaran harapan $np$**, proporsi $x/n$, $LR_{\mathrm{POF}}$, p-value, serta keputusan pada taraf 5%.

**In-sample sebagai pembanding:** estimasi penuh dan evaluasi pada seluruh return sah dengan bobot penuh. Labeli sebagai kecocokan dalam sampel, bukan kemampuan prediksi. Kuantil historis yang diuji pada data pembentuknya cenderung memiliki cakupan dekat nominal; ini bukan bukti keunggulan prediksi.

**Batas interpretasi:** pada 99% dan $n\approx120$, pelanggaran harapan sekitar 1,2. Bukti statistik terbatas dan pendekatan chi-square Kupiec asimtotik. Gunakan “tidak menolak kesesuaian frekuensi pelanggaran”, bukan “membuktikan model valid”. Kupiec tidak memvalidasi CVaR atau independensi pelanggaran. Jangan mengurutkan model sebagai paling akurat hanya berdasarkan p-value terbesar; baca juga frekuensi pelanggaran, arah penyimpangan, dan kedekatan MC dengan solusi analitik. Simpulan pada banyak metode/level bersifat eksploratif dan tidak diperlakukan sebagai satu pengujian konfirmatori tunggal.

**Pelengkap opsional:** uji binomial eksak dua sisi pada $x$ dari $n$ dengan peluang $p=1-c$ dapat memperlihatkan sensitivitas keputusan terhadap pendekatan asimtotik, terutama pada 99%. Uji ini tetap mengasumsikan percobaan Bernoulli independen dan tidak mengatasi pelanggaran yang mengelompok. Tampilkan deret waktu loss/VaR dan tanggal pelanggaran; uji independensi Christoffersen dapat ditambahkan bila jumlah transisi memadai. Jika evaluasi 99% ingin diperkuat kelak, perluas periode data sebelum analisis ulang; jangan menganggap simulasi lebih banyak memperbesar jumlah hari uji.

### D10 — Pelaporan dan reproduktibilitas

- Dana awal $V_0=\text{Rp }100.000.000$. Rupiah pendekatan = risiko desimal × $V_0$, atau risiko dalam persen / 100 × $V_0$.
- VaR adalah ambang loss pada tingkat kepercayaan terkait; CVaR adalah rata-rata loss ekor. Jangan menyebut CVaR sebagai jumlah yang tidak mungkin dilampaui.
- Simpan perhitungan dalam presisi penuh. Tampilkan VaR/CVaR dalam persen minimal 2 desimal, SE dalam poin persentase minimal 4 desimal atau notasi ilmiah bila perlu, bobot 4 desimal, dan p-value cukup presisi. Jangan membulatkan SE kecil menjadi nol atau p-value kecil menjadi nol tanpa penjelasan.
- Simpan data sumber dan hasil penyelarasan, konfigurasi, seed, versi dependensi, hasil per pengulangan, dan prediksi per tanggal. Hasil utama berada di `hasil_tanpa_filter/`; daftar outlier dan perbandingan penyaringan disimpan oleh notebook terpisah ketika dibuat nanti. Tentukan satuan pada kolom/tabel.
- Korelasi dan manfaat diversifikasi harus dihitung, bukan diasumsikan hanya karena saham berasal dari sektor sama.

### Catatan keterbandingan dengan paper

Pemeriksaan awal memakai parameter halaman 377 paper: $\mu=[-0{,}001312416;-0{,}00240666]$, kovarian diagonal $0{,}0002255476$ dan $0{,}0003231605$, kovarian silang $0{,}0001269921$, serta bobot $[0{,}6656006;0{,}3343994]$. **Jika ditafsirkan sebagai normal multivariat dan portofolio linear**, diperoleh:

| Tingkat kepercayaan | VaR analitik dari parameter paper | VaR Tabel 3.1 paper |
|---|---|---|
| 90% | sekitar 1,95% | 4,85% |
| 95% | sekitar 2,45% | 5,69% |
| 99% | sekitar 3,40% | 6,77% |

Ini bukan bukti final implementasi penulis salah karena rincian simulasi tidak lengkap. Selisih menunjukkan angka tabel tidak langsung dapat direkonstruksi dari asumsi operasional tersebut. Jangan mengubah skala, definisi, parameter, atau seed untuk memaksa hasil mendekati paper. Pembahasan berfokus pada metode yang dinyatakan, hasil data baru, dan keterbatasan keterbandingan.

---

## 5. Rencana Eksekusi

| Tahap | Pekerjaan | Output |
|---|---|---|
| 0 | Tetapkan konfigurasi D1–D10 dan batas hasil utama/tambahan | Konfigurasi penelitian |
| 1 | Unduh dan periksa harga, termasuk satu harga sebelum periode | Data sumber, metadata, `data/processed/harga_adjusted.csv` |
| 2 | Selaraskan tanggal, hitung seluruh return sah, diagnosis normalitas dan ketergantungan waktu | Return tanpa penyaringan nilai ekstrem, grafik, tabel uji |
| 3 | Estimasi parameter dan GMV tanpa penyaringan | Statistik deskriptif, kovarian, korelasi, bobot |
| 4 | Simulasi utama, pemeriksaan analitik, dan konvergensi | Hasil per pengulangan dan tabel pemeriksaan |
| 5 | Hitung VaR/CVaR 90/95/99, SD pengulangan, dan SE rata-rata MC | Tabel utama dengan definisi SE eksplisit |
| 6 | Rolling ketiga metode tanpa penyaringan | Prediksi per tanggal, pelanggaran, tabel Kupiec |
| 7 | Kecocokan in-sample dan ilustrasi Rp 100 juta | Tabel deskriptif dan interpretasi rupiah |
| 8 | Setelah utama selesai, kerjakan tambahan yang dipilih | Bootstrap, Student-t, long-only, atau return sederhana eksak |
| 9 | Tulis laporan dan keterbatasan | Laporan akhir serta paket reproduksi |

**Alat yang direncanakan:** Python (`pandas`, `numpy`, `scipy`, `statsmodels`, dan pustaka grafik). Alat unduh dan versinya dicatat saat implementasi. RStudio tidak wajib selama metode, data, dan hasil dapat direproduksi.

**Pelaksanaan melalui notebook:** gunakan Python 3.11 dan dependensi dalam `requirements.txt`, lalu jalankan notebook utama dari atas ke bawah. Konfigurasi default mengikuti D1–D10 tanpa penyaringan nilai ekstrem; konvergensi dan rolling merupakan tahap yang lebih lama. `REFRESH_DATA=False` memakai snapshot sumber yang sudah tersimpan dan cocok dengan konfigurasi. Tabel, grafik, metadata eksekusi, dan checkpoint baru disimpan di `hasil_tanpa_filter/` langsung di root proyek. Checkpoint rolling memungkinkan eksekusi dilanjutkan pada konfigurasi/data yang sama. Analisis tersaring ditunda ke notebook terpisah; analisis opsional pada Tahap 8 belum diimplementasikan dalam notebook utama.

---

## 6. Struktur Laporan Akhir

1. **Pendahuluan:** masalah risiko, tujuan replikasi, alasan objek/periode, dan pengembangan evaluasi.
2. **Tinjauan pustaka:** log return, kovarian/korelasi, GMV/MVEP, normal multivariat, MC, VaR/CVaR, dan Kupiec. GBM sebagai konteks bila diperlukan.
3. **Metode:** data dan penyesuaian, 11 langkah, D1–D10, pendekatan linear return, pemisahan sampel, dan keputusan mempertahankan seluruh return ekstrem yang sah.
4. **Hasil dan pembahasan:** kualitas data, diagnosis normalitas, parameter/bobot, VaR/CVaR, pemeriksaan analitik/konvergensi, SE MC, evaluasi di luar sampel tanpa penyaringan, ilustrasi rupiah, serta keterbandingan dengan paper. Analisis tersaring dan tambahan lain ditempatkan terpisah ketika dikerjakan.
5. **Kesimpulan dan saran:** temuan sesuai data, keterbatasan normalitas/pendekatan return, keberadaan return ekstrem, batas ukuran sampel pengujian, dan pengembangan relevan. Jangan menyimpulkan validitas CVaR dari Kupiec.
6. **Daftar pustaka dan lampiran reproduksi:** paper, sumber data, rujukan metode, konfigurasi, dan petunjuk menjalankan analisis.

**Batas kesimpulan:** perbedaan hasil terhadap paper dapat dipengaruhi saham, periode, jumlah aset, definisi harga, serta rincian operasional yang tidak tersedia pada paper. Karena beberapa hal berubah bersamaan, penelitian tidak mengidentifikasi pengaruh kausal satu perubahan tertentu. Temuan satu sektor dan satu tahun juga tidak langsung digeneralisasi ke seluruh pasar atau periode lain.

---

## 7. Rujukan Pendukung Keputusan Operasional

- [Paper referensi lokal](<Paper Referensi/Simulasi Monte Carlo untuk menghitung Var dan CVar.pdf>).
- [SciPy: bootstrap](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html), untuk SE sebagai SD distribusi bootstrap.
- [scikit-learn: common pitfalls dan data leakage](https://scikit-learn.org/stable/common_pitfalls.html), untuk preprocessing yang dipelajari hanya dari pelatihan.
- [NIST: outliers](https://www.itl.nist.gov/div898/handbook/prc/section1/prc16.htm), untuk penyelidikan observasi ekstrem sebelum penghapusan.
- [statsmodels: Lilliefors](https://www.statsmodels.org/stable/_modules/statsmodels/stats/_lilliefors.html), untuk normalitas dengan parameter yang diestimasi.
- [MathWorks: portvrisk](https://www.mathworks.com/help/finance/portvrisk.html) dan [expected shortfall](https://www.mathworks.com/help/risk/expectedshortfall.html), sebagai dokumentasi pendukung risiko distribusi normal.
- [NumPy: quantile](https://numpy.org/doc/stable/reference/generated/numpy.quantile.html), untuk pilihan estimator kuantil linear tipe 7 yang dinyatakan eksplisit.
- [Rockafellar & Uryasev: Conditional Value-at-Risk for General Loss Distributions](https://sites.math.washington.edu/~rtr/papers/rtr187-CVaR2.pdf), untuk CVaR pada distribusi diskrit dan pembobotan massa kuantil.
- [statsmodels: Lilliefors, parameter dan batas p-value](https://www.statsmodels.org/stable/generated/statsmodels.stats.diagnostic.lilliefors.html), untuk pelaporan p-value dari tabel sebagai batas bila relevan.
- [MathWorks: Kupiec POF](https://www.mathworks.com/help/risk/varbacktest.pof.html) dan [independensi pelanggaran](https://www.mathworks.com/help/risk/varbacktest.cci.html), untuk membedakan cakupan dan independensi.
- [SciPy: binomtest](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.binomtest.html), untuk pelengkap uji frekuensi pelanggaran dengan distribusi binomial.
