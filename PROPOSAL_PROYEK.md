# PROPOSAL PROYEK PERANGKAT LUNAK

## SISTEM INFORMASI PRESENSI SISWA BERBASIS RFID DAN PENGENALAN WAJAH (*FACE RECOGNITION*)
**Studi Kasus: Madrasah Tsanawiyah (MTs) Al-Ittihad Purabaya, Kabupaten Sukabumi, Jawa Barat**

---

Diajukan untuk memenuhi Proyek Tahap Awal  
Mata Kuliah: **Manajemen Proyek Perangkat Lunak**

**Disusun oleh: Kelompok Pengembang**
* **Khairino Rizky Putra D** (Manajer Proyek & Lead Developer)
* **Ahmad Fauzi** (Hardware & Embedded System Specialist)
* **Siti Nurhaliza** (Analis Sistem & Desainer UI/UX)
* **Budi Santoso** (Quality Assurance & Dokumentasi)

**PROGRAM STUDI SISTEM INFORMASI / TEKNIK INFORMATIKA**  
**FAKULTAS TEKNOLOGI INFORMASI**  
**2026**

---

## KATA PENGANTAR

Puji syukur kehadirat Allah SWT, Tuhan Yang Maha Esa, atas limpahan rahmat dan hidayah-Nya sehingga penyusunan Dokumen Proposal Proyek Perangkat Lunak dengan judul **“Sistem Informasi Presensi Siswa Berbasis RFID dan Pengenalan Wajah (*Face Recognition*) pada MTs Al-Ittihad Purabaya Kabupaten Sukabumi”** dapat diselesaikan dengan baik. Proposal ini disusun untuk memenuhi tugas Proyek Tahap Awal pada mata kuliah Manajemen Proyek Perangkat Lunak.

Proposal ini menguraikan rencana perancangan, pengembangan, dan penerapan sistem presensi digital terpadu yang memadukan teknologi pembacaan kartu pintar *Radio Frequency Identification* (RFID) dengan biometrik *Face Recognition* berbasis kecerdasan buatan (*computer vision*). Kehadiran sistem ini ditujukan untuk memodernisasi tata kelola madrasah, mencegah praktik titip presensi (*buddy punching*), meningkatkan kedisiplinan peserta didik, dan mempercepat rekapitulasi data kehadiran harian secara *real-time*.

Kami menyadari bahwa proposal ini masih memerlukan evaluasi dan saran yang konstruktif. Kritik serta masukan yang membangun sangat kami harapkan guna penyempurnaan sistem pada tahap pengujian dan implementasi di lapangan. Semoga proposal ini memberikan kontribusi nyata bagi kemajuan teknologi dan efisiensi manajemen di lingkungan MTs Al-Ittihad Purabaya.

Sukabumi, November 2026  

**Tim Penyusun**

---

## DAFTAR ISI

* KATA PENGANTAR
* RINGKASAN EKSEKUTIF
* BAB I PENDAHULUAN
  * 1.1 Latar Belakang
  * 1.2 Permasalahan
  * 1.3 Tujuan dan Manfaat
  * 1.4 Ruang Lingkup
* BAB II RENCANA PROYEK PERANGKAT LUNAK
  * 2.1 Profil Objek Riset (MTs Al-Ittihad Purabaya)
  * 2.2 Kebutuhan Fungsional dan Non-Fungsional Perangkat Lunak
  * 2.3 Rencana Kerja & Jadwal Proyek (WBS & Gantt Chart)
  * 2.4 Struktur Organisasi & Sumber Daya Manusia (SDM)
  * 2.5 Estimasi Anggaran Biaya Proyek
  * 2.6 Analisis Asumsi, Batasan, dan Manajemen Risiko
* BAB III PENUTUP
  * 3.1 Kesimpulan
  * 3.2 Saran Rekomendasi
* LAMPIRAN

---

## DAFTAR TABEL

* **Tabel 1.** Kebutuhan Fungsional Sistem Presensi Digital MTs Al-Ittihad
* **Tabel 2.** Kebutuhan Non-Fungsional dan Spesifikasi Perangkat Keras/Lunak
* **Tabel 3.** Sumber Daya Manusia dan Pembagian Peran Tim Pengembang
* **Tabel 4.** Estimasi Anggaran Biaya Proyek
* **Tabel 5.** Matriks Identifikasi Risiko dan Mitigasi Proyek

---

## RINGKASAN EKSEKUTIF

**Madrasah Tsanawiyah (MTs) Al-Ittihad Purabaya** yang berlokasi di Kecamatan Purabaya, Kabupaten Sukabumi, merupakan institusi pendidikan formal di bawah naungan Kementerian Agama dengan status Akreditasi A dan nomor identitas **NPSN 20277882**. Hingga saat ini, proses presensi kehadiran siswa masih didominasi oleh metode konvensional, yakni pemanggilan nama per kelas menggunakan buku absensi kertas. Metode ini menyita 10–15 menit jam pelajaran efektif di setiap kelas, rentan terhadap kehilangan arsip fisik, menyulitkan pihak guru piket dalam merekap kehadiran tepat waktu, dan membuka celah kecurangan.

Menjawab tantangan tersebut, tim pengembang merancang solusi otomasi cerdas: **Sistem Presensi Siswa Terintegrasi Berbasis RFID dan Pengenalan Wajah (*Dual-Factor Authentication*)**. Sistem bekerja secara sinergis melalui mikrokontroler (ESP32 + RC522) yang membaca UID kartu pintar siswa, diikuti verifikasi cepat wajah melalui kamera webcam menggunakan model *Histogram of Oriented Gradients* (HOG) dan *face landmark encoding* berbasis Flask Python. Sistem dilengkapi fitur penanganan kasus alternatif (apabila kartu tertinggal), deteksi ganda di hari yang sama, sinkronisasi *Server-Sent Events* (SSE) secara *real-time*, serta dasbor administrasi bernuansa islami ramah pengguna.

Proyek dijadwalkan selesai dalam kurun waktu **40 hari kerja (± 8 minggu)** dengan estimasi total alokasi anggaran sebesar **Rp 9.850.000,-**. Target keberhasilan proyek meliputi otomasi pencatatan kehadiran kurang dari 3 detik per siswa, eliminasi manipulasi kehadiran hingga 99%, dan penyediaan rekap data kehadiran instan untuk staf madrasah dan wali santri.

---

## BAB I PENDAHULUAN

### 1.1 Latar Belakang
Madrasah Tsanawiyah (MTs) Al-Ittihad Purabaya yang berlokasi di Jl. Purabaya Km. 36, Desa Purabaya, Kecamatan Purabaya, Kabupaten Sukabumi, Jawa Barat, menaungi ratusan peserta didik tingkat menengah pertama. Sebagai madrasah yang terus bertransformasi menuju era digitalisasi madrasah (*Madrasah Digital/Smart Madrasah*), pengelolaan administrasi siswa yang efektif menjadi pilar penunjang keberhasilan kegiatan belajar mengajar.

Presensi merupakan salah satu indikator vital dalam memantau disiplin santri/siswa, mengevaluasi partisipasi akademik, dan menjadi acuan laporan berkala kepada orang tua serta pengawas madrasah. Namun, sistem presensi manual berbasis lembaran kertas atau buku folio yang berjalan selama ini menghadapi kendala nyata:
1. Memakan waktu pengajar di jam pelajaran pertama hanya untuk mengecek nama siswa.
2. Sering terjadi selisih antara siswa yang hadir di madrasah dengan catatan di meja piket madrasah.
3. Lambatnya integrasi data kehadiran ketika wali kelas atau kepala madrasah memerlukan laporan rekap bulanan untuk evaluasi dan akreditasi madrasah.

Penerapan teknologi RFID (*Radio Frequency Identification*) menawarkan kecepatan transaksi tap kartu dalam hitungan milidetik. Namun, kartu RFID memiliki kelemahan mendasar: kartu dapat dipinjamkan atau dititipkan kepada teman sekelas (*buddy punching*). Oleh karena itu, diperlukan validasi lapis kedua (*two-factor verification*) menggunakan pengenalan biometrik wajah (*Face Recognition*) secara otomatis sesaat setelah kartu ditempelkan. Integrasi ini memastikan bahwa siswa yang menempelkan kartu benar-benar pemilik sah kartu tersebut tanpa menghambat alur masuk siswa di pagi hari.

### 1.2 Permasalahan
Berdasarkan analisis kebutuhan di MTs Al-Ittihad Purabaya, permasalahan yang dihadapi dirumuskan sebagai berikut:
1. **Ketidakefisienan Waktu:** Presensi konvensional memakan waktu 10 hingga 15 menit setiap jam awal masuk, mengurangi waktu interaksi belajar mengajar.
2. **Kelemahan Validitas (Titip Absen):** Belum adanya mekanisme verifikasi identitas fisik secara otomatis yang mencegah siswa menitipkan absensi.
3. **Risiko Kerusakan dan Kehilangan Arsip:** Buku presensi fisik mudah kotor, sobek, terselip, atau rusak akibat penyimpanan jangka panjang.
4. **Keterlambatan Pelaporan:** Rekapitulasi presensi mingguan atau bulanan membutuhkan perhitungan manual oleh staf tata usaha, sehingga rentan kesalahan kalkulasi.
5. **Penanganan Kasus Kartu Tertinggal:** Belum tersedianya prosedur sistematis yang mencatat siswa yang sah hadir namun lupa membawa kartu identitas.

### 1.3 Tujuan dan Manfaat

#### 1.3.1 Tujuan Proyek
1. Membangun sistem perangkat lunak terintegrasi berbasis web (Flask) dan perangkat keras IoT (ESP32 RFID) untuk pencatatan presensi siswa secara terkomputerisasi.
2. Mengimplementasikan algoritma pengenalan wajah (*face encoding cosine/euclidean distance verification*) sebagai otentikasi lapis kedua pendamping RFID.
3. Menyediakan antarmuka dasbor madrasah interaktif dengan visualisasi *real-time stream* dan status kehadiran yang mudah dipahami oleh petugas madrasah.
4. Menyediakan mekanisme identifikasi alternatif bagi siswa yang tidak membawa kartu serta pencegahan absensi ganda pada hari yang sama.

#### 1.3.2 Manfaat Proyek
* **Bagi Madrasah (MTs Al-Ittihad Purabaya):** Meningkatkan citra modernitas madrasah, mendukung standardisasi akreditasi A, serta mewujudkan tertib administrasi peserta didik.
* **Bagi Guru & Petugas Piket:** Memangkas beban administrasi rekapitulasi kehadiran sehingga guru dapat langsung fokus pada materi pengajaran.
* **Bagi Siswa:** Membiasakan budaya tertib waktu, mandiri, dan melek teknologi digital.
* **Bagi Pengembang:** Mengaplikasikan integrasi *Computer Vision*, *Internet of Things* (IoT), dan *Software Engineering* pada permasalahan riil di dunia pendidikan.

### 1.4 Ruang Lingkup

#### a. Ruang Lingkup yang Dikerjakan (*In-Scope*)
1. **Modul Autentikasi Petugas:** Sistem hak akses (*session-based*) aman menggunakan enkripsi kata sandi *Bcrypt* untuk operator/petugas piket madrasah.
2. **Modul Manajemen Siswa:** Pendataan Nomor Induk Siswa (NIS), nama lengkap, kelas madrasah (7A, 8B, 9A, dst.), dan status keaktifan.
3. **Modul Registrasi Biometrik Wajah:** Ekstraksi *facial embeddings* (vektor 128-dimensi) dari tangkapan kamera langsung (*live capture*) dan penyimpanan terenkripsi/terserialisasi di database.
4. **Modul Pengikatan (*Binding*) Kartu RFID:** Pemasangan kode UID kartu fisik (8–14 karakter heksadesimal) ke profil data siswa.
5. **Modul Presensi Otomatis (Dual-Factor):** Integrasi pembacaan RFID via port serial mikrokontroler dengan verifikasi wajah instan melalui ambang batas (*threshold distance* $\le 0.5$).
6. **Modul Presensi Alternatif (Darurat):** Pindaian wajah murni (*1-to-N matching*) disertai konfirmasi petugas bagi siswa yang kartu RFID-nya tertinggal atau rusak.
7. **Modul Pencegahan Kehadiran Ganda (*Duplicate Entry Prevention*):** Pengecekan status kehadiran per tanggal untuk mencegah tap berulang di hari yang sama.
8. **Dasbor Real-Time:** Pemanfaatan *Server-Sent Events* (SSE) untuk memperbarui status presensi di layar secara seketika (*instant feedback*).
9. **Antarmuka Khas Madrasah:** Desain antarmuka responsif bernuansa hijau islami, memuat logo resmi dan identitas MTs Al-Ittihad Purabaya Kabupaten Sukabumi.

#### b. Ruang Lingkup yang Tidak Dikerjakan (*Out-of-Scope*)
1. Integrasi SMS/WhatsApp *Gateway* otomatis berbayar ke nomor orang tua siswa.
2. Sistem penggajian atau penghitungan tunjangan kinerja guru/staf madrasah.
3. Pengadaan gerbang putar fisik (*turnstile tripod gate* otomatis).

---

## BAB II RENCANA PROYEK PERANGKAT LUNAK

### 2.1 Profil Objek Riset
* **Nama Satuan Pendidikan:** Madrasah Tsanawiyah (MTs) Al-Ittihad Purabaya
* **NPSN:** 20277882
* **Akreditasi:** A (Unggul)
* **Status Lembaga:** Swasta di bawah pembinaan Kementerian Agama RI
* **Alamat Lembaga:** Jl. Purabaya Km. 36, Desa Purabaya, Kecamatan Purabaya, Kabupaten Sukabumi, Provinsi Jawa Barat (Kode Pos 43187)
* **Sponsor / Penanggung Jawab Lapangan:** Kepala Madrasah & Tim Kesiswaan MTs Al-Ittihad
* **Jam Operasional KBM:** Senin – Sabtu (07.00 – 14.30 WIB)

### 2.2 Kebutuhan Perangkat Lunak

#### 2.2.1 Kebutuhan Fungsional
**Tabel 1. Kebutuhan Fungsional Sistem Presensi Digital MTs Al-Ittihad**
| Kode | Modul | Deskripsi Kebutuhan Fungsional |
| :--- | :--- | :--- |
| **FR-01** | Autentikasi | Petugas melakukan login dengan username & password terenkripsi untuk mengamankan operasional sistem. |
| **FR-02** | Manajemen Data Siswa | Tambah data siswa baru (NIS, Nama Lengkap, Kelas), perbarui profil, dan tampilkan data siswa terdaftar. |
| **FR-03** | Pendaftaran Wajah | Mengambil frame gambar siswa dari webcam secara langsung, mengekstraksi vektor 128 fitur wajah, dan menyimpannya dalam basis data. |
| **FR-04** | Pemasangan Kartu RFID | Memetakan kode unik kartu fisik (UID) dengan ID siswa yang terdaftar. |
| **FR-05** | Presensi RFID + Wajah | Menangkap sinyal pembacaan UID dari ESP32, mengecek pemilik kartu, mengambil tangkapan webcam, membandingkan wajah dengan template, dan mencatat absensi jika cocok (jarak $\le 0.5$). |
| **FR-06** | Presensi Alternatif (Manual Scan) | Mengidentifikasi wajah siswa tanpa kartu dengan mencocokkan ke seluruh basis data wajah terdaftar dan meminta konfirmasi petugas piket. |
| **FR-07** | Simulasi Tap Kartu | Memungkinkan operator menguji proses presensi dengan memasukkan UID manual tanpa modul pembaca fisik. |
| **FR-08** | Monitoring Real-time & Audio Visual | Menampilkan status presensi secara instan (Berhasil, Gagal, Wajah Tidak Cocok, Sudah Absen) via Server-Sent Events (SSE). |
| **FR-09** | Riwayat & Laporan Harian | Menyajikan daftar siswa yang hadir pada hari aktif lengkap dengan waktu kedatangan, kelas, dan metode presensi. |

#### 2.2.2 Kebutuhan Non-Fungsional
**Tabel 2. Spesifikasi Teknis Perangkat Lunak & Keras**
| Parameter | Spesifikasi Minimum / Penjelasan |
| :--- | :--- |
| **Arsitektur Aplikasi** | Web Application Micro-Framework (Python Flask 3.0, Multithreaded Engine) |
| **Computer Vision Engine** | OpenCV 4.10, dlib / face_recognition (Model HOG 68-landmarks) |
| **Database Management** | SQLite 3 dengan dukungan foreign key cascading dan indexing query cepat |
| **Perangkat Keras IoT** | Modul Mikrokontroler ESP32 Dev Kit V1 + RFID Reader RC522 (Frekuensi 13.56 MHz) |
| **Kamera Pemindai** | USB HD Webcam 720p / 1080p dengan koreksi horizontal flip (tampilan natural) |
| **Kompatibilitas Layar** | Responsive Web Interface (Dukungan desktop PC, laptop piket, dan tablet madrasah) |

### 2.3 Rencana Kerja dan Jadwal Proyek (WBS & Gantt Chart)

Struktur rincian pekerjaan disusun dalam 5 tahapan utama *Work Breakdown Structure* (WBS):
```
1.0 SISTEM PRESENSI RFID & FACE RECOGNITION MTS AL-ITTIHAD
├── 1.1 Inisiasi & Analisis Kebutuhan
│   ├── 1.1.1 Observasi Alur Kedatangan Siswa di MTs Al-Ittihad
│   └── 1.1.2 Wawancara Kepala Madrasah & Petugas Piket
├── 1.2 Perancangan Sistem & Arsitektur
│   ├── 1.2.1 Desain Skema Database Relasional (SQLite)
│   ├── 1.2.2 Desain Alur Verifikasi Dual-Factor (Flowchart & State)
│   └── 1.2.3 Desain Antarmuka Pengguna Khas Madrasah (UI/UX)
├── 1.3 Pengembangan Perangkat Keras & Lunak
│   ├── 1.3.1 Perakitan & Pemrograman ESP32 RFID (C++/Arduino)
│   ├── 1.3.2 Pengembangan Engine Pengenalan Wajah & Serial Listener
│   ├── 1.3.3 Pembuatan API Back-End Flask & Database Handler
│   └── 1.3.4 Implementasi Front-End Dasbor & Pemutakhiran Real-Time
├── 1.4 Pengujian & Evaluasi
│   ├── 1.4.1 Pengujian Unit Algoritma & Akurasi Jarak Wajah
│   └── 1.4.2 User Acceptance Test (UAT) Simulasi Presensi Massal Siswa
└── 1.5 Implementasi & Pelatihan
    ├── 1.5.1 Instalasi Unit Perangkat di Meja Piket Madrasah
    ├── 1.5.2 Perekaman Data Wajah & Kartu Siswa Percontohan
    └── 1.5.3 Pelatihan Petugas / Guru Piket Madrasah
```

#### Rincian Waktu Pelaksanaan (Total 40 Hari Kerja / 8 Minggu)
* **Minggu 1 (5 hari):** Analisis Kebutuhan, Studi Literatur, dan Observasi Lapangan di MTs Al-Ittihad Purabaya.
* **Minggu 2–3 (10 hari):** Perancangan Sistem, Skema Basis Data, Skematik Elektronik IoT, dan Desain UI/UX.
* **Minggu 4–6 (15 hari):** Pengerjaan Kode Program (Back-end Flask, Serial Thread, Face Engine, dan Integrasi Tampilan).
* **Minggu 7 (6 hari):** Pengujian Komprehensif (Black-box testing, stress test serial, dan UAT akurasi pencahayaan).
* **Minggu 8 (4 hari):** Instalasi Perangkat Keras, Perekaman Sampel Wajah Siswa, dan Pelatihan Petugas Madrasah.

---

### 2.4 Struktur Organisasi dan Sumber Daya Manusia (SDM)

**Tabel 3. Sumber Daya Manusia dan Pembagian Peran Tim Pengembang**
| Nama Mahasiswa | Peran Proyek | Tugas dan Tanggung Jawab Utama |
| :--- | :--- | :--- |
| **Khairino Rizky Putra D** | Manajer Proyek & Lead Developer | Mengoordinasikan seluruh fase proyek, mengembangkan arsitektur back-end Flask, mengintegrasikan thread worker serial & SSE, serta mengawasi kualitas deliverables. |
| **Ahmad Fauzi** | IoT & Hardware Engineer | Merakit dan memprogram modul pembaca kartu ESP32 RC522, pengujian komunikasi Serial USB UART, serta kalibrasi penempatan sensor RFID. |
| **Siti Nurhaliza** | UI/UX Designer & Analis Sistem | Mengumpulkan kebutuhan madrasah, merancang visual antarmuka bertema islami MTs Al-Ittihad, membuat stylesheet CSS responsif, dan merancang skema ERD. |
| **Budi Santoso** | QA Tester & Dokumentator | Menguji akurasi jarak pencocokan wajah (*distance threshold*), menyusun skenario pengujian UAT, menyusun manual book (buku panduan pengguna), dan menyusun laporan akhir. |

---

### 2.5 Estimasi Anggaran Biaya Proyek

Penyusunan anggaran menggunakan pendekatan rincian kebutuhan riil pengadaan perangkat keras prototipe, pengembangan perangkat lunak, dan operasional implementasi di lapangan:

**Tabel 4. Estimasi Anggaran Biaya Proyek**
| No | Item Rincian Pembiayaan | Volume / Satuan | Biaya Satuan (Rp) | Subtotal (Rp) |
| :---: | :--- | :---: | :---: | :---: |
| **1** | **Honorarium Tim Pengembang (4 Mahasiswa × 2 Bulan)** | 1 Paket | 6.000.000 | 6.000.000 |
| **2** | **Perangkat Keras IoT:** | | | |
| | - Modul Mikrokontroler ESP32 Dev Kit V1 USB Type-C | 1 Unit | 95.000 | 95.000 |
| | - Sensor RFID MFRC522 + Antena SPI | 1 Unit | 45.000 | 45.000 |
| | - Kartu Pintar RFID Mifare 13.56MHz (Paket Sampel Siswa) | 50 Pcs | 4.000 | 200.000 |
| | - Kabel Jumper, Enclosure Case Akrilik, & Dudukan Sensor | 1 Set | 110.000 | 110.000 |
| **3** | **Perangkat Kamera & Visual:** | | | |
| | - Webcam USB HD Wide-Angle Auto-Focus (Pikatan Wajah) | 1 Unit | 450.000 | 450.000 |
| | - Tripod Meja Fleksibel untuk Webcam | 1 Unit | 75.000 | 75.000 |
| **4** | **Operasional & Implementasi Lapangan:** | | | |
| | - Transportasi & Koordinasi Lapangan ke Purabaya Sukabumi | 1 Paket | 850.000 | 850.000 |
| | - Pencetakan Buku Panduan, Poster Alur Presensi, & ATK | 1 Paket | 350.000 | 350.000 |
| | - Sosialisasi & Pelatihan Petugas Piket Madrasah | 1 Sesi | 500.000 | 500.000 |
| **5** | **Biaya Tak Terduga / Cadangan Risiko (Contingency 15%)** | 1 Paket | 1.175.000 | 1.175.000 |
| **TOTAL** | **ESTIMASI ANGGARAN PROYEK** | | | **Rp 9.850.000** |

---

### 2.6 Analisis Asumsi, Batasan, dan Manajemen Risiko

**Tabel 5. Matriks Identifikasi Risiko dan Mitigasi Proyek**
| Identifikasi Risiko | Kategori | Tingkat Dampak | Strategi Mitigasi Terencana |
| :--- | :---: | :---: | :--- |
| **Intensitas cahaya ruangan piket berubah drastis (silau/gelap) saat scan wajah.** | Risiko Teknis | Sedang | Menyesuaikan orientasi webcam membelakangi jendela dan menyediakan lampu pengisi mini (*fill light LED*) di meja presensi. |
| **Kartu RFID siswa hilang atau tertinggal di rumah saat jam masuk madrasah.** | Risiko Operasional | Sedang | Disediakannya fitur **Scan Alternatif Wajah** di dasbor dengan otorisasi konfirmasi oleh guru piket sehingga siswa tetap tercatat hadir. |
| **Siswa mencoba menempelkan kartu dua kali berturut-turut pada hari yang sama.** | Risiko Logika | Rendah | Sistem memiliki validasi integritas database SQLite `UNIQUE(id_siswa, tanggal)` dan *debounce timer* 3 detik pada *serial listener*. |
| **Port Serial USB terlepas atau gagal terhubung saat komputer menyala.** | Risiko Perangkat Keras | Sedang | Thread `SerialListener` dirancang dengan fitur *auto-reconnect* tiap 2 detik tanpa membuat server aplikasi web mengalami *crash*. |
| **Guru piket belum terbiasa mengoperasikan antarmuka berbasis web.** | Risiko Pengguna | Rendah | Antarmuka dirancang sederhana, status hasil tap berukuran besar dengan kode warna kontras (Hijau = Sukses, Merah = Salah, Kuning = Duplikat), serta disediakan buku petunjuk ringkas. |

---

## BAB III PENUTUP

### 3.1 Kesimpulan
1. Implementasi Sistem Informasi Presensi Siswa Berbasis RFID dan Pengenalan Wajah di MTs Al-Ittihad Purabaya Kabupaten Sukabumi merupakan solusi tepat guna untuk mengatasi keterbatasan presensi manual yang rawan kecurangan, lambat, dan memboroskan kertas.
2. Kombinasi metode *two-factor verification* (kartu RFID + wajah) menjamin keabsahan kehadiran peserta didik secara akurat dan tidak dapat dimanipulasi dengan titip kartu.
3. Arsitektur sistem yang ringan (Flask + SQLite + OpenCV) dapat dioperasikan secara lokal di lingkungan madrasah tanpa ketergantungan mutlak pada biaya sewa server komputasi awan yang mahal.
4. Total masa pengerjaan proyek diproyeksikan selama 40 hari kerja dengan alokasi anggaran Rp 9.850.000,- yang menghasilkan sistem fungsional siap pakai di meja piket madrasah.

### 3.2 Saran Rekomendasi
1. Pihak madrasah disarankan mengalokasikan satu unit PC/laptop operasional khusus di dekat pintu masuk atau pos piket dengan posisi pencahayaan yang stabil.
2. Untuk pengembangan jangka panjang, sistem ini dapat diintegrasikan dengan modul WhatsApp API guna mengirimkan notifikasi otomatis ke nomor orang tua/wali saat siswa berhasil melakukan presensi masuk.
3. Kartu RFID siswa dapat dikembangkan sekaligus menjadi Kartu Tanda Pelajar (KTPel) multifungsi untuk peminjaman buku perpustakaan madrasah.

---

## LAMPIRAN

*(Dokumen pelengkap yang dilampirkan pada berkas fisik pengumpulan):*
1. **Lampiran 1:** Surat Pengantar dan Izin Observasi Proyek Lapangan di MTs Al-Ittihad Purabaya.
2. **Lampiran 2:** Foto Dokumentasi Fisik Prototipe Alat (ESP32 + RC522 Reader) dan Antarmuka Dasbor Web.
3. **Lampiran 3:** Transkrip Wawancara Kebutuhan Sistem dengan Pengelola Madrasah.
4. **Lampiran 4:** Berita Acara & Lembar Pembagian Kerja Anggota Kelompok.
5. **Lampiran 5:** Panduan Ringkas Pengoperasian (*Quick Start Guide*) untuk Operator Piket.
