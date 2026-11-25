import csv
import os

NAMA_FILE = r"C:\Users\USER\Downloads\Mini Project_6D\data_transportasi_publik_jakarta.csv"

KOLOM_WAJIB = ["trip_id", "transit_mode", "origin_station", "destination_station","scheduled_duration_minutes", "actual_duration_minutes",
    "delay_minutes", "ticket_fare_idr", "peak_hour_category","transit_efficiency_index", "crowding_discomfort_score","fare_to_speed_ratio", "service_reliability_tier"]

KOLOM_ANGKA = ["scheduled_duration_minutes", "actual_duration_minutes","delay_minutes", "ticket_fare_idr","transit_efficiency_index", "crowding_discomfort_score","fare_to_speed_ratio"]

KRITERIA = {"1": ("Waktu perjalanan", "actual_duration_minutes", "cost"),"2": ("Biaya perjalanan", "ticket_fare_idr", "cost"),"3": ("Keterlambatan", "delay_minutes", "cost"),"4": ("Efisiensi transportasi", "transit_efficiency_index", "benefit"),"5": ("Kenyamanan/kepadatan", "crowding_discomfort_score", "cost")}

akun = {"username": "", "password": ""}
sudah_register = False

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

        kolom_hilang = [k for k in KOLOM_WAJIB if k not in pembaca.fieldnames]
        if kolom_hilang:
            print("Kolom CSV tidak lengkap:", ", ".join(kolom_hilang))
            return None

        data = list(pembaca)

    if not data:
        print("Tidak ada data pada file CSV.")
        return None

    return data

def validasi_data(data):
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
        return False
    print("Seluruh data dinyatakan valid.")
    return True

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

