Tentu. Intinya, kita ingin menjawab:

**“Kalau dana dibagi ke saham BBCA, BMRI, dan BBRI, seberapa besar risiko kerugian portofolio tersebut dalam satu hari?”**

Kita mengikuti pendekatan paper, lalu menerapkannya pada saham dan periode yang berbeda.

Sebelum masuk perhitungan, kita mengambil **harga harian ketiga saham selama 2024**. Harga yang digunakan sudah disesuaikan terhadap aksi korporasi. Tanggalnya diselaraskan agar ketiga saham selalu dibandingkan pada hari perdagangan yang sama.

Setelah itu, urutannya seperti ini.

1. **Mengubah harga menjadi return**

   Return menunjukkan perubahan harga dari hari perdagangan sebelumnya. Misalnya, harga naik dari Rp10.000 menjadi Rp10.100, berarti keuntungan hariannya sekitar 1%.

   Kita menggunakan **log return**, mengikuti pendekatan paper. Hasilnya berupa tabel return harian BBCA, BMRI, dan BBRI.

2. **Memeriksa return ekstrem dan bentuk distribusi data**

   Kita mencari hari dengan perubahan harga yang sangat besar, lalu memeriksa apakah return mendekati distribusi normal.

   Ada dua perlakuan yang dibandingkan: **data dengan penyaringan outlier** untuk mengikuti paper, dan **data tanpa membuang return ekstrem yang sah**. Perbandingan ini penting karena kejadian ekstrem justru berhubungan dengan risiko.

   Jika normalitas ditolak, penelitian tetap dilanjutkan dengan model normal sebagai asumsi replikasi, lalu keterbatasannya dijelaskan.

3. **Menghitung karakteristik masing-masing saham**

   Dari return historis, kita menghitung:

   - **Mean:** rata-rata return harian.
   - **Standar deviasi:** seberapa besar return berfluktuasi.
   - **Kovarian dan korelasi:** bagaimana ketiga saham bergerak bersama.

   Informasi ini menjadi dasar pembobotan dan simulasi.

4. **Menentukan bobot portofolio**

   Kita menentukan berapa proporsi dana untuk BBCA, BMRI, dan BBRI menggunakan **GMV**, yaitu pembobotan yang meminimalkan varians berdasarkan data estimasi.

   Bobot inilah yang menentukan kontribusi setiap saham terhadap risiko portofolio. Metode utama memungkinkan bobot negatif, yang berarti posisi *short*; jika muncul, hasilnya perlu dijelaskan.

5. **Mensimulasikan banyak kemungkinan return satu hari**

   Berdasarkan mean dan kovarian tadi, Monte Carlo membangkitkan **10.000 skenario** kemungkinan return ketiga saham.

   Setiap skenario berisi satu kemungkinan keadaan BBCA, BMRI, dan BBRI pada hari berikutnya. Hubungan antarsaham tetap diperhitungkan.

   **10.000 skenario berarti 10.000 kemungkinan untuk satu hari, bukan proyeksi 10.000 hari.**

6. **Menggabungkan return saham menjadi return portofolio**

   Pada setiap skenario, return ketiga saham digabungkan menggunakan bobot GMV.

   Kita kemudian mengubahnya menjadi ukuran kerugian: return negatif menjadi loss positif. Sesuai paper, penggabungan log return ini menggunakan pendekatan linear untuk horizon harian.

7. **Menghitung VaR**

   Dari kumpulan loss simulasi, kita mencari ambang kerugian pada tingkat kepercayaan **90%, 95%, dan 99%**.

   Contoh ilustrasi: **VaR 95% sebesar 2%** berarti, menurut model, peluang kerugian melebihi 2% dalam satu hari adalah sekitar 5%.

   VaR bukan batas kerugian yang mustahil dilampaui.

8. **Menghitung CVaR**

   Setelah mengetahui ambang VaR, kita mengambil rata-rata kerugian pada ekor terburuk tersebut.

   Contoh ilustrasi: jika VaR 95% adalah 2% dan CVaR 95% adalah 3%, maka rata-rata kerugian dalam 5% skenario terburuk sekitar 3%.

   Jadi, **VaR menunjukkan ambangnya; CVaR menunjukkan rata-rata kerugian di ekor buruknya.**

9. **Mengulang simulasi sebanyak 100 kali**

   Proses simulasi sampai perhitungan VaR/CVaR diulang menggunakan skenario acak baru.

   Parameter dan bobot tetap sama selama pengulangan pada sampel estimasi yang sama. Tujuannya mengurangi pengaruh kebetulan dari penarikan angka acak.

10. **Merangkum hasil dan memeriksa kestabilannya**

    Kita menghitung rata-rata VaR/CVaR serta galat Monte Carlo untuk melihat variasi hasil antarpengulangan.

    Hasil simulasi juga dibandingkan dengan rumus analitik normal. Dengan asumsi dan bobot yang sama, keduanya seharusnya mendekat ketika jumlah skenario bertambah.

    Nilai risiko kemudian dapat diilustrasikan dalam rupiah untuk dana Rp100 juta.

11. **Menguji prediksi VaR dengan data aktual**

    Kita menggunakan **120 return sebelumnya** untuk memperkirakan risiko hari berikutnya. Setelah return hari berikutnya diketahui, kita memeriksa apakah kerugiannya melewati VaR. Proses ini digeser satu hari dan diulang.

    Monte Carlo dibandingkan dengan metode parametrik normal dan historis menggunakan informasi masa lalu yang sama. Frekuensi pelanggarannya diperiksa melalui **uji Kupiec**. Return ekstrem pada hari pengujian tetap dinilai.

Dokumen kita akhirnya menghasilkan **dua kelompok hasil**: estimasi menggunakan seluruh sampel 2024 untuk mengikuti bentuk penyajian paper, serta backtesting rolling untuk menilai prediksi pada hari yang belum digunakan dalam estimasi.

Bootstrap, Student-t, dan bobot long-only merupakan pengembangan opsional setelah alur utama tersebut selesai.