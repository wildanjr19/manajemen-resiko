# Panduan Proyek

Proyek ini mereplikasi penelitian VaR/CVaR portofolio untuk mata kuliah Manajemen Risiko. Gunakan `alur-penelitian.md` sebagai acuan metodologi dan keputusan penelitian.

## Skill anti-slop

Pengguna memilih **Mo-Awadalla/anti-slop** sebagai panduan penulisan dan pemeriksaan kode proyek ini.

- Sumber: https://github.com/Mo-Awadalla/anti-slop
- Versi terpasang: 2.1.0; commit `b29dfa9695a64fc7f267ead52398fff9ac866037`.
- Panduan lokal: `C:/Users/LENOVO/.codex/skills/anti-slop/SKILL.md`.
- Sebelum menulis atau mengubah kode, baca panduan tersebut dan `references/agent-workflow.md` di direktori skill. Baca `references/evidence-baseline.md` sebelum membuat klaim hasil pemeriksaan. Jika lokasi instalasi berubah, cari skill yang sama di direktori skills Codex.
- Untuk implementasi baru, gunakan mode **Prevent** selama penulisan. Untuk permintaan tinjauan tanpa perubahan, gunakan **Diagnose**. Ikuti ruang lingkup permintaan pengguna untuk refactoring atau perbaikan.
- Gunakan alur kerja agen secara langsung dengan alat yang tersedia. Runner Linux merupakan fasilitas opsional, bukan prasyarat pengerjaan di Windows.

## Penerapan pada notebook

- Gunakan satu notebook utama untuk alur penelitian; analisis pengembangan opsional dapat dipisahkan ke notebook tambahan.
- Susun notebook agar dapat dijalankan berurutan dari atas ke bawah. Pisahkan penjelasan metode, sel kode, hasil, dan interpretasi secara jelas.
- Tambahkan fungsi, dependensi, dan konfigurasi berdasarkan kebutuhan nyata. Hindari lapisan abstraksi atau fitur untuk kebutuhan yang belum ada.
- Pertahankan penjelasan rumus, asumsi, satuan, dan keputusan metodologi yang membantu pembaca memahami analisis. Keringkasan tidak boleh menghilangkan informasi penelitian yang diperlukan.
- Jangan menyembunyikan kegagalan pengambilan data atau perhitungan dengan fallback yang menghasilkan keluaran seolah berhasil.
- Verifikasi perilaku dan hasil perhitungan dengan pemeriksaan yang relevan, termasuk pembanding analitik yang ditetapkan dalam alur penelitian. Bedakan pemeriksaan yang benar-benar dijalankan dari yang belum dijalankan.
- Jangan mengubah parameter atau prosedur untuk memaksa hasil menyamai angka paper. Pertahankan perubahan pengguna yang tidak terkait dengan tugas.
