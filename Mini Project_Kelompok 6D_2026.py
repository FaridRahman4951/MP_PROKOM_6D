import csv
import os

NAMA_FILE = r"C:\Users\USER\Downloads\Tugas Farid\data_transportasi_publik_jakarta.csv"

KOLOM_WAJIB = ["trip_id", "transit_mode", "origin_station", "destination_station","scheduled_duration_minutes", "actual_duration_minutes",
    "delay_minutes", "ticket_fare_idr", "peak_hour_category","transit_efficiency_index", "crowding_discomfort_score","fare_to_speed_ratio", "service_reliability_tier"]

KOLOM_ANGKA = ["scheduled_duration_minutes", "actual_duration_minutes","delay_minutes", "ticket_fare_idr","transit_efficiency_index", "crowding_discomfort_score","fare_to_speed_ratio"]

KRITERIA = {"1": ("Waktu perjalanan", "actual_duration_minutes", "cost"),"2": ("Biaya perjalanan", "ticket_fare_idr", "cost"),"3": ("Keterlambatan", "delay_minutes", "cost"),"4": ("Efisiensi transportasi", "transit_efficiency_index", "benefit"),"5": ("Kenyamanan/kepadatan", "crowding_discomfort_score", "cost")}

def baca_file():
    if not os.path.exists(NAMA_FILE):
        print("File tidak ditemukan. Periksa kembali lokasi file.")
        return None
    if not os.path.isfile(NAMA_FILE) or not os.access(NAMA_FILE, os.R_OK):
        print("File tidak dapat dibaca.")
        return None
    with open(NAMA_FILE, "r", newline="", encoding="utf-8-sig") as file:
        pembaca = csv.DictReader(file)
        if not pembaca.fieldnames:
            print("File kosong atau tidak memiliki header.")
            return None
        hilang = [k for k in KOLOM_WAJIB if k not in pembaca.fieldnames]
        if hilang:
            print("Kolom CSV tidak lengkap:", ", ".join(hilang))
            return None
        data = list(pembaca)
    if not data:
        print("Tidak ada data pada file CSV.")
        return None

    masalah = []
    id_ditemukan = set()
    for nomor, baris in enumerate(data, start=2):
        for kolom in KOLOM_WAJIB:
            if not str(baris.get(kolom, "")).strip():
                masalah.append(f"Baris {nomor}: {kolom} kosong.")
        trip_id = str(baris.get("trip_id", "")).strip()
        if trip_id in id_ditemukan:
            masalah.append(f"Baris {nomor}: trip_id duplikat.")
        elif trip_id:
            id_ditemukan.add(trip_id)
        for kolom in KOLOM_ANGKA:
            nilai = angka(baris.get(kolom, ""))
            if nilai is None:
                masalah.append(f"Baris {nomor}: {kolom} bukan angka valid.")
            elif nilai < 0:
                masalah.append(f"Baris {nomor}: {kolom} tidak boleh negatif.")
        for kolom in ["transit_efficiency_index", "crowding_discomfort_score"]:
            nilai = angka(baris.get(kolom, ""))
            if nilai is not None and not 0 <= nilai <= 10:
                masalah.append(f"Baris {nomor}: {kolom} harus bernilai 0-10.")
        jadwal = angka(baris.get("scheduled_duration_minutes", ""))
        aktual = angka(baris.get("actual_duration_minutes", ""))
        terlambat = angka(baris.get("delay_minutes", ""))
        if None not in (jadwal, aktual, terlambat):
            if round(aktual - jadwal, 2) != round(terlambat, 2):
                masalah.append(f"Baris {nomor}: nilai delay tidak sesuai.")

    if masalah:
        print("Data belum valid. Ditemukan", len(masalah), "masalah:")
        for item in masalah[:25]:
            print("-", item)
        if len(masalah) > 25:
            print("Masih ada", len(masalah) - 25, "masalah lainnya.")
        return None
    print("Seluruh data valid.")
    return data

def angka(nilai):
    teks = str(nilai).strip()
    if not teks:
        return None
    bersih = teks[1:] if teks.startswith("-") else teks
    if not bersih or bersih.count(".") > 1:
        return None
    if not bersih.replace(".", "").isdigit():
        return None
    return float(teks)

def pilih_item(daftar, judul):
    if not daftar:
        print("Pilihan tidak tersedia.")
        return None
    print("\n" + judul)
    for nomor, item in enumerate(daftar, start=1):
        print(f"{nomor}. {item}")
    while True:
        pilihan = input("Pilih nomor: ").strip()
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar):
            return daftar[int(pilihan) - 1]
        print("Input tidak valid. Silakan pilih nomor yang tersedia.")

def pilih_fokus_dan_bobot():
    daftar_bobot = {
        "1": {"1": 0.20, "2": 0.20, "3": 0.20, "4": 0.20, "5": 0.20},
        "2": {"1": 0.15, "2": 0.50, "3": 0.15, "4": 0.10, "5": 0.10},
        "3": {"1": 0.50, "2": 0.15, "3": 0.20, "4": 0.10, "5": 0.05},
        "4": {"1": 0.10, "2": 0.10, "3": 0.10, "4": 0.35, "5": 0.35}}
    
    print("PILIH FOKUS PERJALANAN (boleh memilih lebih dari satu)")
    print("1. Seimbang")
    print("2. Biaya termurah")
    print("3. Waktu tercepat")
    print("4. Kenyamanan")
    print("Contoh pilihan gabungan: 2,3")
    while True:
        masukan = input("Pilihan: ").strip().replace(" ", "")
        pilihan = masukan.split(",")
        if pilihan and all(p in ["1", "2", "3", "4"] for p in pilihan):
            fokus = list(dict.fromkeys(pilihan))
            bobot = {
                k: sum(daftar_bobot[f][k] for f in fokus) / len(fokus)
                for k in KRITERIA
            }
            return fokus, bobot
        print("Pilihan salah. Masukkan nomor 1-4 dan pisahkan dengan koma.")

def rekomendasi(data):
    asal_list = sorted({b["origin_station"].strip() for b in data})
    asal = pilih_item(asal_list, "PILIH STASIUN ASAL")
    if asal is None:
        return
    tujuan_list = sorted({
        b["destination_station"].strip() for b in data
        if b["origin_station"].strip() == asal
    })
    tujuan = pilih_item(tujuan_list, "PILIH STASIUN TUJUAN")
    if tujuan is None:
        return
    alternatif = [
        b for b in data
        if b["origin_station"].strip() == asal
        and b["destination_station"].strip() == tujuan]
    if not alternatif:
        print("Tidak ditemukan alternatif pada rute tersebut.")
        return
    
    fokus, bobot = pilih_fokus_dan_bobot()
    pilihan = list(KRITERIA.keys())

    nilai_data = []
    for baris in alternatif:
        nilai = {k: angka(baris[KRITERIA[k][1]]) for k in pilihan}
        if any(v is None for v in nilai.values()):
            print("Ada nilai kriteria yang tidak dapat dihitung.")
            return
        nilai_data.append((baris, nilai))

    minimum = {k: min(n[k] for _, n in nilai_data) for k in pilihan}
    hasil = []
    for baris, nilai in nilai_data:
        skor = 0
        for k in pilihan:
            sekarang = nilai[k]
            nilai_min = minimum[k]
            if KRITERIA[k][2] == "benefit":
                if nilai_min == 0:
                    print("Nilai minimum kriteria", KRITERIA[k][0],
                          "adalah 0; CPI tidak dapat dihitung.")
                    return
                indeks = sekarang / nilai_min * 100
            else:
                indeks = (100 if sekarang == 0 and nilai_min == 0
                          else 0 if sekarang == 0
                          else nilai_min / sekarang * 100)
            skor += bobot[k] * indeks
        hasil.append((skor, baris))
    hasil.sort(key=lambda x: x[0], reverse=True)
    nama_fokus = {
        "1": "Seimbang", "2": "Biaya termurah",
        "3": "Waktu tercepat", "4": "Kenyamanan"}
    
    fokus_terpilih = " + ".join(nama_fokus[f] for f in fokus)
    print("FOKUS PERJALANAN:", fokus_terpilih)
    print("BOBOT DAN TREN KRITERIA")

    for k in pilihan:
        tren = "Positif" if KRITERIA[k][2] == "benefit" else "Negatif"
        print(f"- {KRITERIA[k][0]}: {bobot[k] * 100:.1f}% | {tren}")
    print("HASIL PERINGKAT METODE CPI")
    print("-" * 75)
    print(f"{'Rank':<7}{'Moda transportasi':<25}{'Durasi':>12}{'Tarif':>13}{'CPI':>12}")
    print("-" * 75)
    for rank, (skor, baris) in enumerate(hasil, start=1):
        durasi = angka(baris["actual_duration_minutes"])
        tarif = angka(baris["ticket_fare_idr"])
        print(f"{rank:<7}{baris['transit_mode']:<25}{durasi:>12.0f}"
              f"{tarif:>13,.0f}{skor:>12.2f}")
        
    skor, terbaik = hasil[0]
    print("REKOMENDASI UTAMA")
    print("Moda:", terbaik["transit_mode"])
    print(f"Rute: {asal} -> {tujuan}")
    print("Skor CPI:", round(skor, 2))

class SistemTransportasi:
    def __init__(self, data):
        self.data = data
        self.akun = {}
        
    def registrasi(self):
        print("===== REGISTRASI =====")
        username = input("Buat username: ").strip()
        if not username:
            print("Username tidak boleh kosong.")
            return
        if username in self.akun:
            print("Username sudah digunakan.")
            return
        while True:
            password = input("Buat password (minimal 5 karakter): ")
            if len(password) >= 5:
                break
            print("Password terlalu pendek.")
        self.akun[username] = password
        print("Registrasi berhasil. Silakan masuk.")

    def login(self):
        if not self.akun:
            print("Belum ada akun. Silakan registrasi terlebih dahulu.")
            return False
        print("===== MASUK =====")
        username = input("Username: ").strip()
        password = input("Password: ")
        if self.akun.get(username) == password:
            print("Selamat datang,", username)
            return True
        print("Username atau password salah.")
        return False
    
    def informasi_transportasi(self, tampilkan_stasiun=False):
        moda = sorted({
            b["transit_mode"].strip() for b in self.data
            if b.get("transit_mode", "").strip()
        })
        if not tampilkan_stasiun:
            print("===== TRANSPORTASI YANG TERSEDIA =====")
            for nomor, nama in enumerate(moda, start=1):
                jumlah = sum(1 for b in self.data
                             if b["transit_mode"].strip() == nama)
                print(f"{nomor}. {nama} ({jumlah} data perjalanan)")
            print("Total jenis transportasi:", len(moda))
            return

        print("===== STASIUN SESUAI TRANSPORTASI =====")
        pilihan = pilih_item(moda, "PILIH TRANSPORTASI")
        if pilihan is None:
            return
        for kolom, judul in [
            ("origin_station", "Stasiun asal"),
            ("destination_station", "Stasiun tujuan")
        ]:
            daftar = sorted({
                b[kolom].strip() for b in self.data
                if b["transit_mode"].strip() == pilihan
                and b[kolom].strip()
            })
            print("" + judul + ":")
            for nomor, nama in enumerate(daftar, start=1):
                print(f"{nomor}. {nama}")

    def daftar_stasiun(self, jenis):
        kolom = "origin_station" if jenis == "asal" else "destination_station"
        judul = "ASAL" if jenis == "asal" else "TUJUAN"
        daftar = sorted({
            b[kolom].strip() for b in self.data
            if b.get(kolom, "").strip()
        })
        print(f"===== DAFTAR STASIUN {judul} =====")
        for nomor, nama in enumerate(daftar, start=1):
            print(f"{nomor}. {nama}")
        if not daftar:
            print("Data stasiun belum tersedia.")

    def menu_masuk(self):
        while True:
            print("" + "=" * 44)
            print("       MENU LAYANAN TRANSPORTASI")
            print("=" * 44)
            print("1. Transportasi yang Tersedia")
            print("2. Stasiun Sesuai Transportasi")
            print("3. Daftar Stasiun Asal")
            print("4. Daftar Stasiun Tujuan")
            print("5. Pilihan Rekomendasi")
            print("6. Logout")
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "1":
                self.informasi_transportasi()
            elif pilihan == "2":
                self.informasi_transportasi(True)
            elif pilihan == "3":
                self.daftar_stasiun("asal")
            elif pilihan == "4":
                self.daftar_stasiun("tujuan")
            elif pilihan == "5":
                rekomendasi(self.data)
            elif pilihan == "6":
                print("Anda telah logout.")
                break
            else:
                print("Pilihan tidak tersedia. Masukkan nomor 1-6.")
    def menu_utama(self):
        while True:
            print("" + "=" * 44)
            print("   SISTEM REKOMENDASI TRANSPORTASI")
            print("=" * 44)
            print("1. Registrasi")
            print("2. Masuk")
            print("3. Keluar")
            pilihan = input("Pilih menu: ").strip()
            if pilihan == "1":
                self.registrasi()
            elif pilihan == "2":
                if self.login():
                    self.menu_masuk()
            elif pilihan == "3":
                print("Terima kasih")
                break
            else:
                print("Pilihan tidak tersedia. Masukkan nomor 1-3.")

def main():
    data = baca_file()
    if data is None:
        return
    aplikasi = SistemTransportasi(data)
    aplikasi.menu_utama()


if __name__ == "__main__":
    main()
