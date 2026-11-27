#Sistem Rekomendasi Transportasi Publik di Jakarta Berdasarkan Stasiun Asal dan Tujuan Menggunakan Python)


## Daftar Isi

1. [Latar Belakang](#latar-belakang)
2. [Tujuan](#tujuan)
3. [Fitur Utama](#fitur-utama)
4. [Metodologi](#metodologi)
5. [Struktur Repositori](#struktur-repositori)
6. [Persyaratan Sistem](#persyaratan-sistem)
7. [Cara Menjalankan Program](#cara-menjalankan-program)
8. [Panduan Penggunaan](#panduan-penggunaan)
9. [Format Data](#format-data)
10. Keterbatasan(#keterbatasan)
11. [Tim Pengembang](#tim-pengembang)

1. Latar_Belakang
Transportasi publik menyediakan beberapa pilihan moda dan alternatif perjalanan dengan karakteristik yang berbeda, seperti durasi perjalanan,tarif, keterlambatan, efisiensi, serta tingkat kenyamanan ataukepadatan. Banyaknya pilihan tersebut dapat membuat pengguna kesulitanmenentukan alternatif yang paling sesuai dengan kebutuhannya.

Program ini dibuat untuk mengolah data perjalanan transportasi publik dan menyajikan urutan alternatif berdasarkan kriteria yang dipertimbangkan. Pengguna dapat memilih stasiun asal, stasiun tujuan, serta fokus perjalanan sebelum sistem menampilkan hasil peringkat dan rekomendasi utama.

2. Tujuan
- Membuat program berbasis Python yang dapat membantu pengguna menentukan alternatif rute perjalanan transportasi publik berdasarkan stasiun awal dan stasiun tujuan.
- Menerapkan metode Composite Performance Index (CPI)  untuk melakukan penilaian dan perangkingan terhadap beberapa alternatif rute perjalanan.
- Menyediakan fitur pemilihan prioritas perjalanan agar pengguna dapat menentukan kebutuhan utama, seperti seimbang, waktu tercepat, biaya termurah, atau kenyamanan dan efisiensi. 
- Menghasilkan rekomendasi rute perjalanan terbaik berdasarkan hasil perhitungan metode CPI dengan mempertimbangkan nilai setiap kriteria dan sesuai dengan kebutuhan masing-masing pengguna.
- Mengetahui pengaruh perbedaan bobot kriteria terhadap hasil peringkat       alternatif transportasi publik berdasarkan prioritas perjalanan pengguna.

3. Fitur Utama
- Pengguna dapat membuat akun menggunakan username dan password.
-   Username tidak boleh kosong atau sama dengan username yang sudah
    terdaftar pada sesi program.
-   Password harus memiliki minimal lima karakter.
-   Pengguna harus login sebelum mengakses menu layanan.
-   Menampilkan daftar moda transportasi yang ditemukan pada dataset beserta jumlah data perjalanan untuk setiap moda.
-   Pengguna memilih stasiun asal dan tujuan, kemudian memilih satu ataubeberapa fokus perjalanan. Program menghitung skor CPI untuk setiapalternatif pada rute tersebut, mengurutkan hasil dari skor tertinggi,dan menampilkan rekomendasi utama.
  
4.Metodologi
Program menggunakan metode Composite Performance Index (CPI) untuk mengubah nilai setiap kriteria menjadi indeks, kemudian menggabungkannya menggunakan bobot.
Untuk Tren positif, program menggunakan indeks:

Indeks = (nilai alternatif / nilai minimum kriteria) × 100

Untuk Tren Negatif, program menggunakan indeks berdasarkan perbandingan
nilai minimum dengan nilai alternatif:

Indeks = (nilai minimum kriteria / nilai alternatif) × 100

Skor akhir dihitung dengan menjumlahkan hasil perkalian indeks setiap
kriteria dengan bobotnya:

Skor CPI = Σ (bobot kriteria × indeks kriteria)

Hasil kemudian diurutkan dari skor CPI tertinggi ke terendah. Penanganan
nilai nol mengikuti kondisi yang diterapkan di dalam kode program.

5. Struktur Repository
``` text
project/
├── python_MP_D_6D(1).py
├── data_transportasi_publik_jakarta.csv
└── README.md
```

-   `python_MP_D_6D(1).py`: file program utama.
-   `data_transportasi_publik_jakarta.csv`: dataset perjalanan
    transportasi publik yang dibaca program.
-   `README.md`: dokumentasi yang menjelaskan program.

6. Persyaratan Sistem
-   Python 
-   Dataset berformat CSV.
-   Terminal  untuk menjalankan program.
-   Tidak memerlukan instalasi library eksternal, program menggunakan  modul bawaan Python, yaitu csv dan os.

7. Cara Menjalankan Program
1. Pastikan Python Terinstal.
2.  Simpan file program dan dataset pada lokasi yang mudah diakses.
3.  Sesuaikan variabel NAMA_FILE pada file Python dengan lokasi
    dataset.
4.  Buka terminal atau command prompt pada folder program.
5.  Jalankan perintah

8. Panduan Pengguna
Pengguna akan diberikan tiga pilihan:
1. Registrasi: Membuat akun baru menggunakan username dan password.
2. Masuk: Login menggunakan akun yang telah didaftarkan.
3. Keluar: Mengakhiri program.

Setelah berhasil login, pengguna dapat memilih beberapa layanan:
1. Transportasi yang Tersedia: Menampilkan jenis transportasi publik beserta jumlah data perjalanan.
2. Stasiun Sesuai Transportasi: Menampilkan daftar stasiun asal dan tujuan berdasarkan moda transportasi yang dipilih.
3. Daftar Stasiun Asal: Menampilkan seluruh stasiun asal yang tersedia dalam dataset.
4. Daftar Stasiun Tujuan: Menampilkan seluruh stasiun tujuan yang tersedia dalam dataset.
5. Pilihan Rekomendasi: Menampilkan rekomendasi transportasi berdasarkan metode CPI.
6. Logout: Keluar dari akun dan kembali ke menu utama

Untuk memperoleh rekomendasi transportasi:

1. Pilih menu nomor 5, yaitu Pilihan Rekomendasi.
2. Pilih stasiun asal yang diinginkan.
3. Pilih stasiun tujuan.
4. Pilih fokus perjalanan yang tersedia:
   - Seimbang.
    - Biaya termurah.
    -Waktu tercepat.
     - Kenyamanan.
5. Pengguna juga dapat menggabungkan beberapa fokus perjalanan dengan memisahkan pilihan menggunakan tanda koma, misalnya 2,3.
6. Sistem akan menghitung nilai setiap alternatif menggunakan metode CPI.
7. Program menampilkan hasil pemeringkatan berdasarkan skor CPI tertinggi.
8. Alternatif dengan skor CPI tertinggi akan menjadi rekomendasi utama.

9. Format Data
    Data set yang digunakan  adalah dataset transportasi publik di Jakarta yang diperoleh dari Kaggle dengan nama file data_transportasi_publik_jakarta.csv. Dataset ini terdiri dari 73 data perjalanan dan 13 header yang memuat informasi mengenai jenis transportasi, stasiun asal dan tujuan, waktu tempuh, keterlambatan, biaya perjalanan, indeks efisiensi transportasi, serta tingkat ketidaknyamanan akibat kepadatan penumpang

10. Keterbatasan
 Program hanya mengolah data yang tersedia pada file CSV; program
    tidak mengambil jadwal atau kondisi transportasi secara langsung
    dari layanan transportasi.
-   Rekomendasi hanya dapat diberikan untuk pasangan stasiun asal dan
    tujuan yang memiliki data alternatif di dalam dataset.
-   Akun registrasi hanya tersimpan selama program berjalan.
-   Ketepatan hasil bergantung pada kelengkapan, konsistensi, dan
    kualitas dataset.
-   Lokasi dataset perlu disesuaikan secara manual melalui variabel
    NAMA_FILE sebelum program dijalankan pada komputer lain

11. Pengembang

Kelompok 6D 

Nama                             NIM
  
Farid Rahman                     2610932019
Meisya Khalista Mayari           2610933009
Gallant Habiburrahman Almadina   2610933033
Shaniya Roliya Rizky             2610933045

Asisten Pembimbing:
Kurnia Rahmat Ilahi, Faiza Mumtaz

Dosen Pengampu: Ikhwan Arief, S.T., M.Sc.
Laboratorium Sistem Informasi dan Keputusan
Departemen Teknik Industri
Fakultas Teknik
Universitas Andalas
2026
       
