import os
import re
import sys
import json
import math
import time
import random
import shutil
import getpass
import secrets
import hashlib
import textwrap
import subprocess
import urllib.request
import urllib.parse
import urllib.error


# =========================
# COLORS
# =========================

RESET = "\033[0m"

RED = "\033[91m"
DARK_RED = "\033[31m"
WHITE = "\033[97m"
GRAY = "\033[90m"
CYAN = "\033[96m"


# =========================
# ASCII ART
# =========================

ascii_art = [
    "⠀⠀⢀⣀⡀⠘⢀⣀⠀⣀⠀⠀⠀⠀⣠⡀",
    "⠠⡪⠁⠄⢀⠟⠁⠀⠀⠀⠈⠢⠀⠀⠙⠁",
    "⠀⠑⠄⡑⢌⡀⠀⠀⠀⠀⠀⠀⡗⠠⡀⠀",
    "⠀⠀⠀⠈⠒⡬⢐⠢⠄⣀⠀⢠⠃⠱⡈⠢",
    "⠀⠀⠀⠀⠀⠈⠒⠨⠥⠶⠆⠩⠭⠥⠤⠐",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⢰⡧⠀⠀⠀⠀"
]


# =========================
# IYANTOOLS LOGO
# =========================

logo_text = [
    "█ █▄█ ▄▀█ █▄░█ ▀█ █▄░█ █▀█ ▀█▀ █▀▄ █▀▀ █░█",
    "█ ░█░ █▀█ █░▀█ █▄ █░▀█ █▄█ ░█░ █▄▀ ██▄ ▀▄▀"
]


# =========================
# GET PUBLIC IP
# =========================

def get_ip():
    try:
        return urllib.request.urlopen(
            "https://api.ipify.org",
            timeout=5
        ).read().decode()

    except Exception:
        return "Tidak diketahui"


# =========================
# GET TERMUX ID
# =========================

def get_id():
    return os.popen("id").read().strip()


# =========================
# SENSOR ID
# =========================

def sensor(teks, maksimal=30):

    if len(teks) <= maksimal:
        return teks

    kiri = maksimal // 2
    kanan = maksimal - kiri

    return (
        teks[:kiri]
        + "*" * 8
        + teks[-kanan:]
    )


# =========================
# SETTINGS
# =========================

lebar = 80
LEBAR_ISI = lebar - 3   # ruang konten di dalam box, di antara "│ " dan "│"


# =========================
# FITUR
# =========================

fitur = [
    "Cari Sekolah (Nama)",
    "Cari Sekolah (NPSN)",
    "Cek NIK",
    "IP Lookup",
    "Stalker TikTok",
    "Stalker GitHub",
    "Generate Password",
    "Hash Testing",
    "Scrape Website",
    "Cek Kebocoran Email"
]


# =========================
# CEK NIK (URAI STRUKTUR SECARA LOKAL, TANPA API/DATABASE PIHAK KETIGA)
# =========================
#
# Ini HANYA menerjemahkan pola digit NIK itu sendiri (kode wilayah,
# tanggal lahir, jenis kelamin sesuai standar Kemendagri), bukan
# mengambil data pribadi (nama/alamat/dll) dari database kependudukan
# siapa pun. Tidak ada request jaringan sama sekali di fitur ini.

KODE_PROVINSI = {
    "11": "Aceh", "12": "Sumatera Utara", "13": "Sumatera Barat",
    "14": "Riau", "15": "Jambi", "16": "Sumatera Selatan",
    "17": "Bengkulu", "18": "Lampung", "19": "Kepulauan Bangka Belitung",
    "21": "Kepulauan Riau", "31": "DKI Jakarta", "32": "Jawa Barat",
    "33": "Jawa Tengah", "34": "DI Yogyakarta", "35": "Jawa Timur",
    "36": "Banten", "51": "Bali", "52": "Nusa Tenggara Barat",
    "53": "Nusa Tenggara Timur", "61": "Kalimantan Barat",
    "62": "Kalimantan Tengah", "63": "Kalimantan Selatan",
    "64": "Kalimantan Timur", "65": "Kalimantan Utara",
    "71": "Sulawesi Utara", "72": "Sulawesi Tengah",
    "73": "Sulawesi Selatan", "74": "Sulawesi Tenggara",
    "75": "Gorontalo", "76": "Sulawesi Barat", "81": "Maluku",
    "82": "Maluku Utara", "91": "Papua", "92": "Papua Barat",
    "93": "Papua Selatan", "94": "Papua Tengah",
    "95": "Papua Pegunungan", "96": "Papua Barat Daya",
}

BULAN_INDO = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def urai_nik(nik):
    """
    Urai NIK murni dari strukturnya secara lokal.
    Mengembalikan dict hasil urai, atau {'error': pesan} kalau formatnya
    tidak valid.
    """

    if not nik.isdigit() or len(nik) != 16:
        return {"error": "NIK harus terdiri dari 16 digit angka."}

    kode_prov = nik[0:2]
    kode_kab = nik[2:4]
    kode_kec = nik[4:6]
    tgl = int(nik[6:8])
    bln = int(nik[8:10])
    thn = int(nik[10:12])
    urut = nik[12:16]

    valid_bulan = 1 <= bln <= 12
    tgl_asli = tgl - 40 if tgl > 40 else tgl
    valid_tanggal = valid_bulan and 1 <= tgl_asli <= 31

    if not valid_tanggal:
        return {"error": "6 digit tanggal lahir pada NIK ini tidak valid, kemungkinan NIK salah ketik."}

    jenis_kelamin = "Perempuan" if tgl > 40 else "Laki-laki"
    nama_bulan = BULAN_INDO[bln]

    return {
        "error": None,
        "provinsi": KODE_PROVINSI.get(kode_prov, f"Kode {kode_prov} (tidak dikenali)"),
        "kode_kabupaten_kota": f"{kode_kab} (kode mentah, belum di-resolve ke nama)",
        "kode_kecamatan": f"{kode_kec} (kode mentah, belum di-resolve ke nama)",
        "tanggal_lahir": f"{tgl_asli:02d} {nama_bulan} 19{thn:02d} atau 20{thn:02d} (2 digit tahun ambigu)",
        "jenis_kelamin": jenis_kelamin,
        "nomor_urut": urut,
    }


# =========================
# API (SEKOLAH & NIK)
# =========================

API_SEKOLAH = "https://sekolah.devapi.id/sekolah"
API_NIK = "https://danxyofficial-api.vercel.app/tools/nik"
API_GITHUB_STALK = "https://danxyofficial-api.vercel.app/stalk/github"
API_TIKTOK_STALK = "https://danxyofficial-api.vercel.app/stalk/tiktok"
API_IP_LOOKUP = "http://ip-api.com/json"  # tier gratis: HTTP saja, tanpa API key
API_BREACH_EMAIL = "https://api.xposedornot.com/v1/check-email"  # gratis, publik, tanpa API key

FIELDS_IP_LOOKUP = (
    "status,message,continent,country,countryCode,region,regionName,"
    "city,zip,lat,lon,timezone,isp,org,as,asname,mobile,proxy,hosting,query"
)


HEADERS_API = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def ambil_json(url):
    """
    Request GET ke url dengan header standar, kembalikan (data_json, pesan_error).
    Dipakai bareng oleh semua fitur yang manggil API eksternal.
    """

    try:
        req = urllib.request.Request(url, headers=HEADERS_API)

        with urllib.request.urlopen(req, timeout=10) as resp:
            mentah = resp.read().decode()

        return json.loads(mentah), None

    except urllib.error.HTTPError as e:
        if e.code == 403:
            return None, "Akses ditolak server (403). Server kemungkinan memblokir permintaan ini (rate limit/anti-bot)."
        return None, f"Server mengembalikan error HTTP {e.code} ({e.reason})."

    except urllib.error.URLError as e:
        return None, f"Gagal terhubung ke server: {e.reason}"

    except json.JSONDecodeError:
        return None, "Respons server tidak valid (bukan JSON)."

    except Exception as e:
        return None, f"Terjadi kesalahan: {e}"


def ambil_data_sekolah(params):
    """Ambil data dari API sekolah.devapi.id. Mengembalikan (data_json, pesan_error)."""
    query = urllib.parse.urlencode(params)
    return ambil_json(f"{API_SEKOLAH}?{query}")


def ambil_data_nik(nik):
    """Ambil data dari API NIK (danxyofficial-api.vercel.app). Mengembalikan (data_json, pesan_error)."""
    query = urllib.parse.urlencode({"nik": nik})
    return ambil_json(f"{API_NIK}?{query}")


def ambil_data_github(username):
    """Ambil profil publik GitHub via API stalk/github. Mengembalikan (data_json, pesan_error)."""
    query = urllib.parse.urlencode({"username": username})
    return ambil_json(f"{API_GITHUB_STALK}?{query}")


def ambil_data_tiktok(username):
    """Ambil profil publik TikTok via API stalk/tiktok. Mengembalikan (data_json, pesan_error)."""
    query = urllib.parse.urlencode({"username": username})
    return ambil_json(f"{API_TIKTOK_STALK}?{query}")


def ambil_data_ip(target):
    """
    Ambil data geolokasi/ISP dari ip-api.com. target boleh IP, domain,
    atau string kosong (berarti cek IP publik sendiri).
    Mengembalikan (data_json, pesan_error). Beda dengan API lain, di sini
    data_json langsung flat (bukan dibungkus 'result'/'data').
    """
    path = urllib.parse.quote(target) if target else ""
    return ambil_json(f"{API_IP_LOOKUP}/{path}?fields={FIELDS_IP_LOOKUP}")


def ambil_data_breach(email):
    """
    Cek kebocoran email lewat API publik XposedOrNot (gratis, tanpa API key).
    Beda dari API lain: HTTP 404 di sini artinya email AMAN (tidak ditemukan
    di breach manapun) - itu hasil valid, bukan error.

    Mengembalikan (status, data_json, pesan_error):
      status "aman"      -> email tidak ditemukan di breach manapun
      status "ditemukan" -> email ada di satu/lebih breach, lihat data_json
      status "error"     -> gagal cek (jaringan/server), lihat pesan_error
    """
    url = f"{API_BREACH_EMAIL}/{urllib.parse.quote(email)}"

    try:
        req = urllib.request.Request(url, headers=HEADERS_API)
        with urllib.request.urlopen(req, timeout=10) as resp:
            mentah = resp.read().decode()
        return "ditemukan", json.loads(mentah), None

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "aman", None, None
        if e.code == 403:
            return "error", None, "Akses ditolak server (403). Coba lagi beberapa saat lagi."
        if e.code == 429:
            return "error", None, "Terlalu banyak permintaan (429). Tunggu sebentar sebelum cek lagi."
        return "error", None, f"Server mengembalikan error HTTP {e.code} ({e.reason})."

    except urllib.error.URLError as e:
        return "error", None, f"Gagal terhubung ke server: {e.reason}"

    except json.JSONDecodeError:
        return "error", None, "Respons server tidak valid (bukan JSON)."

    except Exception as e:
        return "error", None, f"Terjadi kesalahan: {e}"


def susun_daftar_breach(data):
    """
    Respons /v1/check-email berbentuk nested list: {"breaches": [["Nama1", "Nama2", ...]]}.
    Diratakan jadi satu daftar nama breach yang unik.
    """
    mentah = (data or {}).get("breaches") or []
    nama = []
    for grup in mentah:
        if isinstance(grup, list):
            nama.extend(str(g) for g in grup)
        else:
            nama.append(str(grup))
    return list(dict.fromkeys(nama))


# =========================
# BOX HELPERS
# =========================

def layar_baru():
    print("\033[2J\033[H", end="")


def garis_box(kiri, isi, kanan):
    print(RED + kiri + isi * (lebar - 2) + kanan + RESET)


def judul_box(teks):
    garis_box("┌", "─", "┐")
    print(RED + "│" + WHITE + teks.center(lebar - 2) + RED + "│" + RESET)
    garis_box("├", "─", "┤")


def tutup_box():
    garis_box("└", "─", "┘")


def baris_kv(label, value):
    """
    Cetak satu baris 'label : value' di dalam box.
    Value yang kepanjangan otomatis di-wrap ke baris baru
    dengan hanging indent, supaya kotak tetap rapi/sempurna.
    """

    prefix = f"{label} : "
    lebar_prefix = len(prefix)
    lebar_nilai = LEBAR_ISI - lebar_prefix

    teks = "-" if value in (None, "", [], {}) else str(value)

    if lebar_nilai < 10:
        # label kepanjangan untuk muat di satu kolom rapi,
        # fallback: gabung label+value lalu wrap bareng
        for bagian in (textwrap.wrap(prefix + teks, LEBAR_ISI) or [""]):
            print(RED + "│ " + WHITE + bagian.ljust(LEBAR_ISI) + RED + "│" + RESET)
        return

    potongan = textwrap.wrap(teks, lebar_nilai) or [""]

    for i, bagian in enumerate(potongan):
        depan = prefix if i == 0 else " " * lebar_prefix
        print(
            RED + "│ " +
            GRAY + depan +
            WHITE + bagian.ljust(lebar_nilai) +
            RED + "│" + RESET
        )


def baris_teks(teks, warna=WHITE):
    """Cetak teks bebas (bukan pasangan label:value) di dalam box, dengan word-wrap."""
    for bagian in (textwrap.wrap(str(teks), LEBAR_ISI) or [""]):
        print(RED + "│ " + warna + bagian.ljust(LEBAR_ISI) + RED + "│" + RESET)


def cetak_kotak_data(judul, pasangan, nomor=None, total=None):
    """
    Cetak kotak detail dari pasangan {label: value} yang SUDAH rapi.
    pasangan boleh kosong -> tampil 'Tidak ada data.'
    """
    judul_lengkap = judul
    if nomor and total and total > 1:
        judul_lengkap = f"{judul} ({nomor}/{total})"

    judul_box(judul_lengkap)

    if pasangan:
        for label, value in pasangan.items():
            baris_kv(label, value)
    else:
        baris_kv("Info", "Tidak ada data.")

    tutup_box()


def cetak_box_sekolah(data, nomor=None, total=None):
    if isinstance(data, dict) and data:
        pasangan = {str(k).replace("_", " ").title(): v for k, v in data.items()}
    else:
        pasangan = {}
    cetak_kotak_data("DETAIL SEKOLAH", pasangan, nomor, total)


def susun_tampilan_nik(hasil_json):
    """
    Ubah respons API NIK (danxyofficial) jadi pasangan {label: value} yang
    rapi untuk ditampilkan. Field 'creator' dan 'status' dari API sengaja
    tidak diikutkan.
    """
    r = hasil_json.get("result", {}) or {}
    prov = r.get("provinsi", {}) or {}
    kab = r.get("kotakab", {}) or {}
    kec = r.get("kecamatan", {}) or {}
    tambahan = r.get("tambahan", {}) or {}

    kab_nama = kab.get("nama")
    kab_label = f"{kab_nama} ({kab.get('jenis')})" if kab_nama and kab.get("jenis") else (kab_nama or "-")

    return {
        "NIK": r.get("nik", "-"),
        "Jenis Kelamin": r.get("kelamin", "-"),
        "Tanggal Lahir": r.get("lahir_lengkap") or r.get("lahir") or "-",
        "Provinsi": prov.get("nama", "-"),
        "Kabupaten/Kota": kab_label,
        "Kecamatan": kec.get("nama", "-"),
        "Kode Wilayah": r.get("kode_wilayah", "-"),
        "Nomor Urut": r.get("nomor_urut", "-"),
        "Pasaran": tambahan.get("pasaran", "-"),
        "Usia": tambahan.get("usia", "-"),
        "Kategori Usia": tambahan.get("kategori_usia", "-"),
        "Ultah Berikutnya": tambahan.get("ultah", "-"),
        "Zodiak": tambahan.get("zodiak", "-"),
    }


def susun_tampilan_github(hasil_json):
    """
    Ubah respons API stalk/github (danxyofficial) jadi pasangan {label: value}
    yang rapi untuk ditampilkan. Field 'creator' dan 'status' dari API, serta
    'id'/'nodeId' internal GitHub, sengaja tidak diikutkan.
    """
    r = hasil_json.get("result", {}) or {}

    return {
        "Username": r.get("username", "-"),
        "Nama Tampilan": r.get("nickname") or "-",
        "Bio": r.get("bio") or "-",
        "Tipe Akun": r.get("type", "-"),
        "Perusahaan": r.get("company") or "-",
        "Lokasi": r.get("location") or "-",
        "Blog/Website": r.get("blog") or "-",
        "Email Publik": r.get("email") or "-",
        "Repo Publik": r.get("public_repo", "-"),
        "Gist Publik": r.get("public_gists", "-"),
        "Followers": r.get("followers", "-"),
        "Following": r.get("following", "-"),
        "Akun Dibuat": r.get("ceated_at") or r.get("created_at") or "-",
        "Terakhir Update": r.get("updated_at", "-"),
        "Foto Profil": r.get("profile_pic", "-"),
        "URL Profil": r.get("url", "-"),
    }


def susun_tampilan_tiktok(hasil_json):
    """
    Ubah respons API stalk/tiktok (danxyofficial) jadi pasangan {label: value}
    yang rapi untuk ditampilkan. Field 'creator', 'status', dan 'id'/'avatar'
    mentah sengaja tidak semuanya diikutkan.
    """
    r = hasil_json.get("result", {}) or {}

    return {
        "Username": r.get("uniqueId", "-"),
        "Nama Tampilan": r.get("nickname") or "-",
        "Bio": r.get("signature") or "-",
        "Akun Terverifikasi": "Ya" if r.get("verified") else "Tidak",
        "Following": r.get("following", "-"),
        "Followers": r.get("followers", "-"),
        "Total Suka (Likes)": r.get("likes", "-"),
        "Jumlah Video": r.get("videos", "-"),
        "Foto Profil": r.get("avatar", "-"),
        "URL Profil": f"https://www.tiktok.com/@{r.get('uniqueId', '')}" if r.get("uniqueId") else "-",
    }


def susun_tampilan_ip(data):
    """
    Ubah respons ip-api.com (flat, tanpa nesting) jadi pasangan {label: value}
    yang rapi untuk ditampilkan.
    """
    def ya_tidak(nilai):
        return "Ya" if nilai else "Tidak"

    return {
        "IP/Domain": data.get("query", "-"),
        "Benua": data.get("continent") or "-",
        "Negara": f"{data.get('country', '-')} ({data.get('countryCode', '-')})",
        "Wilayah": data.get("regionName", "-"),
        "Kota": data.get("city", "-"),
        "Kode Pos": data.get("zip") or "-",
        "Latitude": data.get("lat", "-"),
        "Longitude": data.get("lon", "-"),
        "Zona Waktu": data.get("timezone", "-"),
        "ISP": data.get("isp", "-"),
        "Organisasi": data.get("org") or "-",
        "AS/ASN": data.get("as") or "-",
        "Nama ASN": data.get("asname") or "-",
        "Jaringan Mobile": ya_tidak(data.get("mobile")),
        "Proxy/VPN": ya_tidak(data.get("proxy")),
        "Hosting/Datacenter": ya_tidak(data.get("hosting")),
    }


# =========================
# SIMPAN HASIL
# =========================

def buat_nama_file(teks):
    aman = "".join(c if c.isalnum() else "_" for c in str(teks))
    aman = aman.strip("_")[:40]
    return aman or "hasil_sekolah"


def simpan_hasil(data, nama_dasar):
    print()
    jawab = input(
        GRAY + "Simpan hasil ini? (y/n) " + WHITE + "→ " + RESET
    ).strip().lower()

    if jawab != "y":
        return

    print()
    print(RED + "│ " + CYAN + "1." + WHITE + " JSON".ljust(LEBAR_ISI - 2) + RED + "│" + RESET)
    print(RED + "│ " + CYAN + "2." + WHITE + " TXT".ljust(LEBAR_ISI - 2) + RED + "│" + RESET)
    print()

    pilih = input(RED + "Pilih format" + WHITE + " → " + RESET).strip()

    folder = "hasil_sekolah"
    os.makedirs(folder, exist_ok=True)
    nama_file = buat_nama_file(nama_dasar)

    if pilih == "1":
        path = os.path.join(folder, f"{nama_file}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    elif pilih == "2":
        path = os.path.join(folder, f"{nama_file}.txt")
        daftar = data if isinstance(data, list) else [data]

        with open(path, "w", encoding="utf-8") as f:
            for i, item in enumerate(daftar, 1):
                f.write(f"=== Data {i} ===\n")
                if isinstance(item, dict):
                    for k, v in item.items():
                        f.write(f"{k}: {v}\n")
                else:
                    f.write(f"{item}\n")
                f.write("\n")

    else:
        print()
        print(RED + "Format tidak dikenali, dibatalkan." + RESET)
        return

    print()
    print(CYAN + f"Tersimpan di: {path}" + RESET)


# =========================
# FITUR: CARI SEKOLAH
# =========================

def proses_cari_sekolah(mode):
    print()

    if mode == "nama":
        kueri = input(WHITE + "Masukkan nama sekolah" + RESET + " → ").strip()
        param = {"nama": kueri}
    else:
        kueri = input(WHITE + "Masukkan NPSN" + RESET + " → ").strip()
        param = {"npsn": kueri}

    if not kueri:
        print()
        print(RED + "Input tidak boleh kosong." + RESET)
        return

    print()
    print(CYAN + "Mencari data sekolah..." + RESET)

    hasil, error = ambil_data_sekolah(param)

    print()

    if error:
        print(RED + error + RESET)
        return

    if not hasil:
        print(RED + "Gagal mengambil data dari server." + RESET)
        return

    if not hasil.get("success"):
        pesan = hasil.get("message") or "Terjadi kesalahan pada server."
        print(RED + pesan + RESET)
        return

    data_mentah = hasil.get("data")

    if not data_mentah:
        print(RED + "Data sekolah tidak ditemukan." + RESET)
        return

    daftar = data_mentah if isinstance(data_mentah, list) else [data_mentah]

    print()

    for idx, item in enumerate(daftar, 1):
        cetak_box_sekolah(item, idx, len(daftar))
        print()

    simpan_hasil(daftar, kueri)


# =========================
# GENERATE PASSWORD (100% LOKAL, TANPA JARINGAN)
# =========================

LEET_MAP = {
    "a": "@", "A": "@",
    "e": "3", "E": "3",
    "i": "1", "I": "1",
    "o": "0", "O": "0",
    "s": "$", "S": "$",
    "t": "7", "T": "7",
}

KUMPULAN_SIMBOL = "!@#$%^&*-_=+?"
KUMPULAN_DIGIT = "0123456789"
KUMPULAN_TAMBAHAN = KUMPULAN_SIMBOL + KUMPULAN_DIGIT


def skor_kekuatan(pw):
    """
    Estimasi kekuatan password secara lokal (heuristik sederhana berbasis
    perkiraan entropi), BUKAN audit keamanan formal. Mengembalikan (skor 0-100, label).
    """
    if not pw:
        return 0, "Sangat Lemah"

    pool = 0
    if any(c.islower() for c in pw):
        pool += 26
    if any(c.isupper() for c in pw):
        pool += 26
    if any(c.isdigit() for c in pw):
        pool += 10
    if any(not c.isalnum() for c in pw):
        pool += 32
    pool = max(pool, 1)

    entropi_bit = len(pw) * math.log2(pool)
    skor = min(100, round(entropi_bit / 100 * 100))

    karakter_unik = len(set(pw))
    if karakter_unik < len(pw) * 0.5:
        skor = max(0, skor - 15)

    if skor >= 80:
        label = "Sangat Kuat"
    elif skor >= 60:
        label = "Kuat"
    elif skor >= 40:
        label = "Sedang"
    elif skor >= 20:
        label = "Lemah"
    else:
        label = "Sangat Lemah"

    return skor, label


def _acak_string(panjang, kumpulan):
    return "".join(secrets.choice(kumpulan) for _ in range(panjang))


def _terapkan_leetspeak(pw, peluang):
    hasil = []
    for c in pw:
        if c in LEET_MAP and secrets.randbelow(100) < peluang * 100:
            hasil.append(LEET_MAP[c])
        else:
            hasil.append(c)
    return "".join(hasil)


def _acak_kapitalisasi(pw, peluang):
    hasil = []
    for c in pw:
        if c.isalpha() and secrets.randbelow(100) < peluang * 100:
            hasil.append(c.upper() if c.islower() else c.lower())
        else:
            hasil.append(c)
    return "".join(hasil)


def buat_varian_password(pw_asli, jumlah=50):
    """
    Bikin sejumlah varian password yang lebih kuat dari pw_asli, dengan
    kombinasi acak: leetspeak, kapitalisasi acak, dan tambahan
    awalan/sisipan/akhiran simbol+angka. Semua acak pakai modul `secrets`
    (cocok untuk keperluan keamanan, bukan `random` biasa).
    """
    sudah_ada = set()
    hasil = []

    percobaan = 0
    maks_percobaan = jumlah * 25

    while len(hasil) < jumlah and percobaan < maks_percobaan:
        percobaan += 1

        pw = _terapkan_leetspeak(pw_asli, secrets.choice([0.3, 0.5, 0.7]))
        pw = _acak_kapitalisasi(pw, secrets.choice([0.2, 0.35, 0.5]))

        prefiks = _acak_string(secrets.choice([0, 1, 2]), KUMPULAN_TAMBAHAN)
        sisipan = _acak_string(secrets.choice([1, 2, 3]), KUMPULAN_DIGIT)
        sufiks = _acak_string(secrets.choice([2, 3, 4]), KUMPULAN_TAMBAHAN)

        pw_baru = f"{prefiks}{pw}{sisipan}{sufiks}"

        if pw_baru in sudah_ada:
            continue

        sudah_ada.add(pw_baru)
        hasil.append(pw_baru)

    return hasil


# =========================
# HASH TESTING (100% LOKAL, TANPA JARINGAN)
# =========================
#
# Fitur ini HANYA mencocokkan kandidat dari wordlist terhadap sebuah hash
# target (dictionary attack sederhana) - BUKAN decrypt hash, karena hash
# memang tidak bisa didekripsi. Alurnya: kandidat -> di-hash -> dibandingkan.
# Ditujukan untuk testing hash/password milik sendiri, CTF, dan belajar
# cryptographic hashing. TIDAK ada request jaringan, TIDAK ada fitur untuk
# mencoba login/credential stuffing/menyerang service online.

ALGORITMA_HASH = {
    "1": ("MD5", "md5", 32),
    "2": ("SHA-1", "sha1", 40),
    "3": ("SHA-256", "sha256", 64),
    "4": ("SHA-512", "sha512", 128),
}


def is_hex_string(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False


def validasi_hash(target_hash, panjang_valid):
    """
    Validasi format target hash terhadap algoritma yang dipilih.
    Mengembalikan (valid: bool, pesan_error atau None).
    """
    if not target_hash:
        return False, "Target hash tidak boleh kosong."

    if len(target_hash) != panjang_valid:
        return False, (
            f"Panjang hash tidak sesuai untuk algoritma ini. "
            f"Seharusnya {panjang_valid} karakter, yang dimasukkan {len(target_hash)} karakter."
        )

    if not is_hex_string(target_hash):
        return False, "Target hash harus berupa karakter hexadecimal (0-9, a-f)."

    return True, None


def hash_kandidat(password, nama_algoritma):
    """hash = f(password). Selalu pakai hashlib bawaan, tidak ada implementasi sendiri."""
    return hashlib.new(nama_algoritma, password.encode("utf-8")).hexdigest()


def baca_wordlist(path):
    """
    Generator baca wordlist baris demi baris, supaya wordlist besar tidak
    langsung dimuat seluruhnya ke RAM. Baris kosong dilewati.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for baris in f:
            kandidat = baris.rstrip("\r\n")
            if kandidat:
                yield kandidat


def proses_hash_testing(target_hash, nama_algoritma, path_wordlist):
    """
    Jalankan dictionary attack sederhana: baca wordlist satu per satu,
    hash tiap kandidat, bandingkan dengan target_hash (huruf kecil semua).
    Progress ditampilkan di satu baris yang diperbarui (bukan spam per baris).

    Mengembalikan (ditemukan: bool, kandidat_cocok atau None, jumlah_dicoba, pesan_error atau None).
    """
    jumlah = 0

    try:
        for kandidat in baca_wordlist(path_wordlist):
            jumlah += 1

            if hash_kandidat(kandidat, nama_algoritma) == target_hash:
                sys.stdout.write("\r" + " " * 50 + "\r")
                sys.stdout.flush()
                return True, kandidat, jumlah, None

            if jumlah % 500 == 0:
                sys.stdout.write(f"\r{GRAY}Tested: {jumlah} candidates{RESET}")
                sys.stdout.flush()

        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()
        return False, None, jumlah, None

    except FileNotFoundError:
        return False, None, jumlah, f"File wordlist tidak ditemukan: {path_wordlist}"

    except (OSError, PermissionError) as e:
        return False, None, jumlah, f"File wordlist tidak bisa dibaca: {e}"


# =========================
# SCRAPE WEBSITE (BACA KONTEN PUBLIK, TANPA BYPASS APA PUN)
# =========================
#
# Fitur ini HANYA mengambil & membaca konten yang memang disajikan publik
# oleh server ke browser mana pun - persis seperti "View Page Source" di
# browser. Tidak ada bypass login, tidak ada eksploitasi celah keamanan,
# dan tidak melakukan crawling rekursif ke seluruh situs - hanya satu
# halaman yang diminta, plus aset CSS/JS yang ditautkannya secara langsung
# (dibatasi jumlahnya biar tidak bikin banyak request ke server orang).

MAKS_ASET_DIUNDUH = 10  # batas jumlah file CSS/JS yang diunduh isinya


def ambil_teks(url, batas_bita=2_000_000):
    """
    Ambil konten teks (HTML/CSS/JS) dari url, dibatasi ukurannya (default 2MB)
    supaya tidak menyedot file yang kelewat besar. Mengembalikan (teks, pesan_error).
    """
    try:
        req = urllib.request.Request(url, headers=HEADERS_API)

        with urllib.request.urlopen(req, timeout=10) as resp:
            mentah = resp.read(batas_bita)

        return mentah.decode("utf-8", errors="ignore"), None

    except urllib.error.HTTPError as e:
        if e.code == 403:
            return None, "Akses ditolak server (403). Server kemungkinan memblokir permintaan ini."
        return None, f"Server mengembalikan error HTTP {e.code} ({e.reason})."

    except urllib.error.URLError as e:
        return None, f"Gagal terhubung ke server: {e.reason}"

    except Exception as e:
        return None, f"Terjadi kesalahan: {e}"


def ekstrak_npsn(teks):
    """Cari NPSN (8 digit) yang disebut berdekatan dengan kata 'NPSN' di teks."""
    return sorted(set(re.findall(r"NPSN[^0-9]{0,20}(\d{8})", teks, re.IGNORECASE)))


def ekstrak_telepon(teks):
    """
    Cari nomor HP format Indonesia (08xx / +62 8xx / 62 8xx).
    Heuristik sederhana - format landline dengan kode area tidak semuanya tertangkap.
    """
    pola = r"(?<!\d)(?:\+62|62|0)[\s\-]?8\d(?:[\s\-]?\d){7,10}(?!\d)"
    mentah = re.findall(pola, teks)
    bersih = {re.sub(r"[\s\-]", "", t) for t in mentah}
    return sorted(bersih)


def ekstrak_email(teks):
    """Cari semua alamat email di teks (termasuk @gmail.com dan provider lain)."""
    return sorted(set(re.findall(r"[\w.\-+]+@[\w\-]+\.[\w.\-]+", teks)))


def ekstrak_link(html, base_url):
    """Cari semua href di halaman, dijadikan URL absolut, kecuali javascript:/mailto:/tel:/#."""
    mentah = re.findall(r'href=["\']([^"\'#][^"\']*)["\']', html, re.IGNORECASE)
    hasil = set()
    for u in mentah:
        if u.lower().startswith(("javascript:", "mailto:", "tel:")):
            continue
        hasil.add(urllib.parse.urljoin(base_url, u))
    return sorted(hasil)


def ekstrak_aset(html, base_url, pola):
    mentah = re.findall(pola, html, re.IGNORECASE)
    return sorted(set(urllib.parse.urljoin(base_url, u) for u in mentah))


def ekstrak_css(html, base_url):
    """Daftar file CSS (<link rel=stylesheet>) yang ditautkan halaman."""
    return ekstrak_aset(html, base_url, r'<link[^>]+rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']')


def ekstrak_js(html, base_url):
    """Daftar file JS (<script src=...>) yang ditautkan halaman."""
    return ekstrak_aset(html, base_url, r'<script[^>]+src=["\']([^"\']+)["\']')


def ekstrak_api_endpoint(teks):
    """
    Cari POLA teks yang KEMUNGKINAN adalah API endpoint (path /api/, /wp-json/,
    atau target fetch()/axios()) di dalam HTML+JS. Ini dugaan berdasarkan pola
    teks, BUKAN kepastian - perlu dicek manual.
    """
    pola_list = [
        r'["\'](/api/[a-zA-Z0-9_\-/]+)["\']',
        r'["\'](/wp-json/[a-zA-Z0-9_\-/]+)["\']',
        r'["\'](https?://[a-zA-Z0-9.\-]+/api/[a-zA-Z0-9_\-/]*)["\']',
        r'fetch\(\s*["\']([^"\']+)["\']',
        r'axios\.\w+\(\s*["\']([^"\']+)["\']',
    ]
    hasil = set()
    for pola in pola_list:
        hasil.update(re.findall(pola, teks, re.IGNORECASE))
    return sorted(hasil)


def unduh_aset(daftar_url, maks=MAKS_ASET_DIUNDUH):
    """Unduh isi sejumlah aset (CSS/JS), dibatasi jumlahnya. Return list of (url, teks_atau_None)."""
    hasil = []
    for u in daftar_url[:maks]:
        teks, _ = ambil_teks(u)
        hasil.append((u, teks))
    return hasil


def cetak_daftar_box(judul, daftar, maks_tampil=50):
    """Tampilkan daftar sebagai kotak bernomor. Dilewati kalau daftarnya kosong."""
    if not daftar:
        return
    pasangan = {}
    for i, item in enumerate(daftar[:maks_tampil], 1):
        pasangan[f"{i:03d}"] = item
    if len(daftar) > maks_tampil:
        sisa = len(daftar) - maks_tampil
        pasangan[f"{maks_tampil + 1:03d}"] = f"... dan {sisa} lainnya (lengkapnya ada di file simpanan)"
    cetak_kotak_data(f"{judul} ({len(daftar)})", pasangan)
    print()


# =========================
# STARTUP: ANIMASI LOADING (CMATRIX-STYLE) + MUSIK BACKGROUND
# =========================
#
# Dua-duanya jalan SEKALI di awal, sebelum menu utama muncul pertama kali.
# Animasi murni Python (tanpa dependency binary 'cmatrix'). Musik WAJIB
# lewat player command-line yang sudah ada di sistem (Python sendiri tidak
# bisa memutar audio) - kalau tidak ada satupun yang terpasang, cuma
# dikasih tahu, aplikasi tetap jalan normal tanpa musik.

PATH_MUSIK = os.path.join("music", "music-2026-iyantools.mp3")

KARAKTER_MATRIX = (
    "01ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
)


def animasi_loading_matrix(durasi_detik=5):
    """
    Animasi loading gaya 'cmatrix' warna merah selama durasi_detik detik,
    sebelum masuk ke menu utama. Pure Python (modul random/shutil/time saja),
    tidak butuh binary 'cmatrix' terpasang. Aman di-skip dengan Ctrl+C.
    """
    try:
        ukuran = shutil.get_terminal_size(fallback=(lebar, 24))
        lebar_term, tinggi_term = max(10, ukuran.columns), max(5, ukuran.lines)
    except Exception:
        lebar_term, tinggi_term = lebar, 24

    posisi_y = [random.randint(-tinggi_term, 0) for _ in range(lebar_term)]
    kecepatan = [random.choice([1, 1, 2]) for _ in range(lebar_term)]
    panjang_ekor = 3

    layar_baru()
    print("\033[?25l", end="")  # sembunyikan kursor biar animasi bersih

    mulai = time.time()
    try:
        while time.time() - mulai < durasi_detik:
            potongan = []
            for kolom in range(lebar_term):
                y = posisi_y[kolom]

                if 0 <= y < tinggi_term:
                    ch = random.choice(KARAKTER_MATRIX)
                    potongan.append(f"\033[{y + 1};{kolom + 1}H{RED}{ch}{RESET}")

                y_hapus = y - panjang_ekor
                if 0 <= y_hapus < tinggi_term:
                    potongan.append(f"\033[{y_hapus + 1};{kolom + 1}H ")

                posisi_y[kolom] += kecepatan[kolom]
                if posisi_y[kolom] - panjang_ekor > tinggi_term and random.random() < 0.05:
                    posisi_y[kolom] = random.randint(-10, 0)

            sys.stdout.write("".join(potongan))
            sys.stdout.flush()
            time.sleep(0.05)

    except KeyboardInterrupt:
        pass

    finally:
        print("\033[?25h", end="")  # tampilkan lagi kursornya
        layar_baru()


def putar_musik_latar(path_musik):
    """
    Coba putar file musik di BACKGROUND (non-blocking) lewat salah satu
    player command-line yang tersedia di sistem. Python sendiri tidak
    punya kemampuan native memutar audio, jadi ini bergantung pada salah
    satu dari termux-api/mpv/ffplay/mpg123/vlc yang sudah terpasang.

    Mengembalikan objek Popen (biar bisa dihentikan pas keluar aplikasi),
    atau None kalau file tidak ada / tidak ada player yang cocok.
    """
    if not os.path.isfile(path_musik):
        print(GRAY + f"File musik tidak ditemukan: {path_musik} (musik dilewati)." + RESET)
        return None

    kandidat_perintah = [
        ["termux-media-player", "play", path_musik],
        ["mpv", "--no-video", "--really-quiet", path_musik],
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path_musik],
        ["mpg123", "-q", path_musik],
        ["cvlc", "--play-and-exit", "--quiet", path_musik],
    ]

    for perintah in kandidat_perintah:
        if shutil.which(perintah[0]):
            try:
                return subprocess.Popen(
                    perintah,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                continue

    print(
        GRAY +
        "Tidak ada pemutar musik yang terdeteksi (termux-api/mpv/ffplay/mpg123/vlc). "
        "Musik dilewati - install salah satunya (mis. 'pkg install mpv') kalau mau fitur ini aktif." +
        RESET
    )
    return None


# =========================
# LAYAR PER FITUR
# =========================

def fitur_cari_sekolah_nama():
    layar_baru()
    judul_box("CARI SEKOLAH (NAMA)")
    baris_teks("Cari data sekolah berdasarkan nama.")
    tutup_box()
    proses_cari_sekolah("nama")


def fitur_cari_sekolah_npsn():
    layar_baru()
    judul_box("CARI SEKOLAH (NPSN)")
    baris_teks("Cari data sekolah berdasarkan NPSN (Nomor Pokok Sekolah Nasional).")
    tutup_box()
    proses_cari_sekolah("npsn")


def fitur_cek_nik():
    layar_baru()
    judul_box("CEK NIK")
    baris_teks("Cari detail wilayah, tanggal lahir, dan info tambahan dari NIK (KTP).")
    tutup_box()

    print()
    nik = input(WHITE + "Masukkan NIK (16 digit)" + RESET + " → ").strip()

    if not nik:
        print()
        print(RED + "NIK tidak boleh kosong." + RESET)
        return

    if not (nik.isdigit() and len(nik) == 16):
        print()
        print(RED + "NIK harus terdiri dari 16 digit angka." + RESET)
        return

    print()
    print(CYAN + "Mencari data NIK..." + RESET)

    hasil_json, error = ambil_data_nik(nik)

    print()

    if error or not hasil_json or not hasil_json.get("status") or not hasil_json.get("result"):
        if error:
            print(RED + error + RESET)
        else:
            pesan = hasil_json.get("message") if hasil_json else None
            print(RED + (pesan or "NIK tidak ditemukan atau tidak valid.") + RESET)

        # Fallback: urai struktur NIK secara lokal (tanpa jaringan) kalau
        # API gagal dihubungi, supaya fitur tetap berguna secara offline.
        cadangan = urai_nik(nik)
        if not cadangan["error"]:
            print()
            print(GRAY + "Menampilkan hasil urai struktur lokal sebagai cadangan:" + RESET)
            print()
            cetak_kotak_data("HASIL URAI LOKAL (CADANGAN)", {
                "Provinsi": cadangan["provinsi"],
                "Kode Kab/Kota": cadangan["kode_kabupaten_kota"],
                "Kode Kecamatan": cadangan["kode_kecamatan"],
                "Tanggal Lahir": cadangan["tanggal_lahir"],
                "Jenis Kelamin": cadangan["jenis_kelamin"],
                "Nomor Urut": cadangan["nomor_urut"],
            })
        return

    pasangan = susun_tampilan_nik(hasil_json)

    print()
    cetak_kotak_data("HASIL CEK NIK", pasangan)

    simpan_hasil(hasil_json.get("result", {}), nik)


def fitur_stalk_github():
    layar_baru()
    judul_box("STALKER GITHUB")
    baris_teks("Lihat info profil publik GitHub (bio, repo, followers, dll) berdasarkan username.")
    tutup_box()

    print()
    username = input(WHITE + "Masukkan username GitHub" + RESET + " → ").strip()

    if not username:
        print()
        print(RED + "Username tidak boleh kosong." + RESET)
        return

    print()
    print(CYAN + "Mencari profil GitHub..." + RESET)

    hasil_json, error = ambil_data_github(username)

    print()

    if error or not hasil_json or not hasil_json.get("status") or not hasil_json.get("result"):
        if error:
            print(RED + error + RESET)
        else:
            pesan = hasil_json.get("message") if hasil_json else None
            print(RED + (pesan or "Username GitHub tidak ditemukan.") + RESET)
        return

    pasangan = susun_tampilan_github(hasil_json)

    print()
    cetak_kotak_data("HASIL STALKER GITHUB", pasangan)

    simpan_hasil(hasil_json.get("result", {}), username)


def fitur_ip_lookup():
    layar_baru()
    judul_box("IP LOOKUP")
    baris_teks("Cari info geolokasi & ISP dari sebuah alamat IP atau domain (via ip-api.com).")
    baris_teks("Kosongkan lalu Enter untuk cek IP publik milik sendiri.")
    tutup_box()

    print()
    target = input(WHITE + "Masukkan IP atau domain (boleh kosong)" + RESET + " → ").strip()

    print()
    print(CYAN + "Mencari data IP..." + RESET)

    data, error = ambil_data_ip(target)

    print()

    if error:
        print(RED + error + RESET)
        return

    if not data or data.get("status") != "success":
        pesan = (data or {}).get("message") or "Data tidak ditemukan / IP atau domain tidak valid."
        print(RED + pesan + RESET)
        return

    pasangan = susun_tampilan_ip(data)

    print()
    cetak_kotak_data("HASIL IP LOOKUP", pasangan)

    simpan_hasil(data, target or "ip_sendiri")


def fitur_stalk_tiktok():
    layar_baru()
    judul_box("STALKER TIKTOK")
    baris_teks("Lihat info profil publik TikTok (bio, followers, likes, dll) berdasarkan username.")
    tutup_box()

    print()
    username = input(WHITE + "Masukkan username TikTok" + RESET + " → ").strip()

    if not username:
        print()
        print(RED + "Username tidak boleh kosong." + RESET)
        return

    print()
    print(CYAN + "Mencari profil TikTok..." + RESET)

    hasil_json, error = ambil_data_tiktok(username)

    print()

    if error or not hasil_json or not hasil_json.get("status") or not hasil_json.get("result"):
        if error:
            print(RED + error + RESET)
        else:
            pesan = hasil_json.get("message") if hasil_json else None
            print(RED + (pesan or "Username TikTok tidak ditemukan.") + RESET)
        return

    pasangan = susun_tampilan_tiktok(hasil_json)

    print()
    cetak_kotak_data("HASIL STALKER TIKTOK", pasangan)

    simpan_hasil(hasil_json.get("result", {}), username)


def fitur_generate_password():
    layar_baru()
    judul_box("GENERATE PASSWORD")
    baris_teks(
        "Masukkan password yang mau diperkuat. Sistem bikin 50 varian yang "
        "lebih kuat lalu kasih rekomendasi mana yang paling aman dipakai."
    )
    baris_teks(
        "Catatan: ini perkiraan kekuatan lokal (heuristik), bukan audit "
        "keamanan resmi. Semua diproses di HP kamu sendiri, tidak dikirim ke internet."
    )
    tutup_box()

    print()
    try:
        pw_asli = getpass.getpass(
            WHITE + "Masukkan password (ketikan tidak akan tampil)" + RESET + " → "
        )
    except Exception:
        pw_asli = input(WHITE + "Masukkan password" + RESET + " → ")

    if not pw_asli:
        print()
        print(RED + "Password tidak boleh kosong." + RESET)
        return

    print()
    print(CYAN + "Membuat 50 varian password yang lebih kuat..." + RESET)

    skor_asli, label_asli = skor_kekuatan(pw_asli)
    varian = buat_varian_password(pw_asli, jumlah=50)

    if not varian:
        print()
        print(RED + "Gagal membuat varian password, coba lagi." + RESET)
        return

    dinilai = [(pw, *skor_kekuatan(pw)) for pw in varian]
    dinilai.sort(key=lambda x: (x[1], len(x[0])), reverse=True)

    pw_top, skor_top, label_top = dinilai[0]

    print()
    judul_box("REKOMENDASI TERKUAT")
    baris_kv("Password Asli Kamu", f"Skor {skor_asli}/100 ({label_asli})")
    baris_kv("Rekomendasi Terbaik", pw_top)
    baris_kv("Skor Rekomendasi", f"{skor_top}/100 ({label_top})")
    tutup_box()

    print()
    pasangan_daftar = {}
    for i, (pw, skor, label) in enumerate(dinilai, 1):
        tanda = "  <- REKOMENDASI" if i == 1 else ""
        pasangan_daftar[f"{i:02d}"] = f"{pw}  (Skor {skor} - {label}){tanda}"

    cetak_kotak_data("50 KANDIDAT PASSWORD (terkuat > terlemah)", pasangan_daftar)

    print()
    print(GRAY + "Kalau disimpan, filenya berisi password dalam teks biasa - jaga baik-baik." + RESET)

    data_simpan = {
        "skor_password_asli": {"skor": skor_asli, "label": label_asli},
        "rekomendasi_terbaik": {"password": pw_top, "skor": skor_top, "label": label_top},
        "semua_kandidat": [
            {"password": pw, "skor": skor, "label": label} for pw, skor, label in dinilai
        ],
    }
    simpan_hasil(data_simpan, "generate_password")


def fitur_hash_testing():
    layar_baru()
    judul_box("HASH TESTING")
    baris_teks("Cocokkan hash dengan wordlist lokal (dictionary attack) - bukan decrypt hash.")
    baris_teks(
        "Hanya untuk testing hash/password milik sendiri, CTF, dan belajar "
        "cryptographic hashing. 100% lokal, tanpa internet, tanpa fitur login/serang akun."
    )
    tutup_box()

    print()
    target_hash = input(WHITE + "Target Hash" + RESET + " → ").strip()

    if not target_hash:
        print()
        print(RED + "Target hash tidak boleh kosong." + RESET)
        return

    print()
    cetak_kotak_data("PILIH ALGORITMA HASH", {
        "1": "MD5",
        "2": "SHA-1",
        "3": "SHA-256",
        "4": "SHA-512",
    })

    print()
    pilihan_algo = input(WHITE + "Pilih algoritma" + RESET + " → ").strip()

    if pilihan_algo not in ALGORITMA_HASH:
        print()
        print(RED + "Algoritma tidak tersedia. Pilih salah satu dari 1-4." + RESET)
        return

    nama_tampilan, nama_algoritma, panjang_valid = ALGORITMA_HASH[pilihan_algo]

    valid, pesan_error = validasi_hash(target_hash, panjang_valid)
    if not valid:
        print()
        print(RED + pesan_error + RESET)
        return

    target_hash = target_hash.lower()

    print()
    path_wordlist = input(WHITE + "Lokasi wordlist (kosongkan = pw.txt)" + RESET + " → ").strip()
    if not path_wordlist:
        path_wordlist = "pw.txt"

    if not os.path.isfile(path_wordlist):
        print()
        print(RED + f"File wordlist tidak ditemukan: {path_wordlist}" + RESET)
        return

    print()
    print(CYAN + f"Mencocokkan hash pakai wordlist '{path_wordlist}'..." + RESET)
    print()

    ditemukan, kandidat, jumlah, pesan_error = proses_hash_testing(
        target_hash, nama_algoritma, path_wordlist
    )

    if pesan_error:
        print(RED + pesan_error + RESET)
        return

    print()

    if ditemukan:
        judul_box("[MATCH]")
        baris_kv("Password Kandidat", kandidat)
        baris_kv("Algoritma", nama_tampilan)
        baris_kv("Hash", target_hash)
        baris_kv("Total Dicoba", str(jumlah))
        tutup_box()
    else:
        judul_box("[SELESAI]")
        baris_teks("Kandidat tidak ditemukan di wordlist.")
        baris_kv("Total Dicoba", str(jumlah))
        tutup_box()


def fitur_scrape_website():
    layar_baru()
    judul_box("SCRAPE WEBSITE")
    baris_teks("Ambil NPSN, telepon, email, daftar link/CSS/JS, dan dugaan API endpoint dari sebuah URL.")
    baris_teks(
        "Catatan: hanya membaca konten yang memang disajikan publik (sama seperti "
        "'View Page Source' di browser) - tidak bypass login atau apa pun."
    )
    tutup_box()

    print()
    url = input(WHITE + "Masukkan URL" + RESET + " → ").strip()

    if not url:
        print()
        print(RED + "URL tidak boleh kosong." + RESET)
        return

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print()
    print(CYAN + "Mengambil halaman..." + RESET)

    html, error = ambil_teks(url)

    print()

    if error:
        print(RED + error + RESET)
        return

    if not html:
        print(RED + "Halaman kosong atau tidak bisa dibaca." + RESET)
        return

    npsn = ekstrak_npsn(html)
    telepon = ekstrak_telepon(html)
    email = ekstrak_email(html)
    link = ekstrak_link(html, url)
    css_url = ekstrak_css(html, url)
    js_url = ekstrak_js(html, url)

    print(CYAN + f"Memindai isi {min(len(js_url), MAKS_ASET_DIUNDUH)} file JS untuk dugaan API endpoint..." + RESET)
    js_diunduh = unduh_aset(js_url, MAKS_ASET_DIUNDUH)
    teks_js_gabungan = "\n".join(teks for _, teks in js_diunduh if teks)

    api_endpoint = ekstrak_api_endpoint(html + "\n" + teks_js_gabungan)

    print()
    cetak_kotak_data("RINGKASAN SCRAPE", {
        "URL": url,
        "Panjang HTML": f"{len(html)} karakter",
        "NPSN Ditemukan": ", ".join(npsn) if npsn else "-",
        "Jumlah Nomor Telepon": str(len(telepon)),
        "Jumlah Email": str(len(email)),
        "Jumlah Link": str(len(link)),
        "Jumlah File CSS": str(len(css_url)),
        "Jumlah File JS": str(len(js_url)),
        "Dugaan API Endpoint": str(len(api_endpoint)),
    })

    print()
    cetak_daftar_box("NOMOR TELEPON", telepon)
    cetak_daftar_box("EMAIL", email)
    cetak_daftar_box("DUGAAN API ENDPOINT", api_endpoint)
    cetak_daftar_box("LINK DI HALAMAN", link)
    cetak_daftar_box("FILE CSS", css_url)
    cetak_daftar_box("FILE JS", js_url)

    print(GRAY + "Dugaan API endpoint dari pola teks (fetch/axios/path 'api') - bukan kepastian, cek manual." + RESET)

    data_simpan = {
        "url": url,
        "npsn": npsn,
        "nomor_telepon": telepon,
        "email": email,
        "link": link,
        "css": css_url,
        "js": js_url,
        "api_endpoint_dugaan": api_endpoint,
    }
    simpan_hasil(data_simpan, url)

    print()
    jawab_html = input(
        GRAY + "Simpan HTML mentah halaman ini juga? (y/n) " + WHITE + "→ " + RESET
    ).strip().lower()

    if jawab_html == "y":
        folder = "hasil_sekolah"
        os.makedirs(folder, exist_ok=True)
        path_html = os.path.join(folder, buat_nama_file(url) + "_page.html")
        with open(path_html, "w", encoding="utf-8") as f:
            f.write(html)
        print()
        print(CYAN + f"HTML tersimpan di: {path_html}" + RESET)


def fitur_breach_email():
    layar_baru()
    judul_box("CEK KEBOCORAN EMAIL")
    baris_teks("Cek apakah sebuah email pernah muncul di data breach publik, via API XposedOrNot.")
    baris_teks("Gratis, tanpa API key. Hasil bergantung pada database mereka, bukan jaminan 100% lengkap.")
    tutup_box()

    print()
    email = input(WHITE + "Masukkan alamat email" + RESET + " → ").strip()

    if not email:
        print()
        print(RED + "Email tidak boleh kosong." + RESET)
        return

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        print()
        print(RED + "Format email tidak valid." + RESET)
        return

    print()
    print(CYAN + "Mengecek riwayat kebocoran..." + RESET)

    status, data, error = ambil_data_breach(email)

    print()

    if status == "error":
        print(RED + error + RESET)
        return

    if status == "aman":
        judul_box("[AMAN]")
        baris_kv("Email", email)
        baris_teks("Tidak ditemukan di database breach XposedOrNot.")
        tutup_box()

        simpan_hasil({"email": email, "ditemukan": False, "breaches": []}, email)
        return

    daftar_breach = susun_daftar_breach(data)

    judul_box("[TERDETEKSI DI BREACH]")
    baris_kv("Email", email)
    baris_kv("Jumlah Breach", str(len(daftar_breach)))
    tutup_box()

    print()
    cetak_daftar_box("DAFTAR BREACH", daftar_breach)

    print(GRAY + "Saran: ganti password akun terkait, aktifkan 2FA, dan jangan pakai ulang password yang sama di banyak akun." + RESET)

    simpan_hasil({"email": email, "ditemukan": True, "breaches": daftar_breach}, email)


# =========================
# MAIN LOOP
# =========================

proses_musik = putar_musik_latar(PATH_MUSIK)
animasi_loading_matrix(5)

while True:

    # Clear terminal
    layar_baru()

    # =====================
    # HEADER
    # =====================

    for i in range(6):
        kiri = ascii_art[i]

        if i == 2:
            kanan = logo_text[0]
        elif i == 3:
            kanan = logo_text[1]
        else:
            kanan = ""

        print(RED + kiri + RESET + "    " + WHITE + kanan + RESET)

    print()

    # =====================
    # PROFILE
    # =====================

    ip = get_ip()
    id_user = get_id()

    judul_box("PROFILE")

    print(RED + "│ " + GRAY + "IP : " + WHITE + ip.ljust(lebar - 8) + RED + "│" + RESET)
    print(RED + "│ " + GRAY + "ID : " + WHITE + sensor(id_user).ljust(lebar - 8) + RED + "│" + RESET)

    tutup_box()

    print()

    # =====================
    # MENU
    # =====================

    judul_box("IyanTools")

    print(RED + "│" + " " * (lebar - 2) + "│" + RESET)

    for i, item in enumerate(fitur, 1):
        nomor = f"{i:02d}."
        print(RED + "│ " + CYAN + nomor + WHITE + f" {item}".ljust(lebar - 6) + RED + "│" + RESET)

    print(RED + "│ " + DARK_RED + "00." + WHITE + " Exit".ljust(lebar - 6) + RED + "│" + RESET)

    tutup_box()

    # =====================
    # INPUT
    # =====================

    print()

    pilihan = input(RED + "Pilih fitur" + WHITE + " → " + RESET)

    # =====================
    # EXIT
    # =====================

    if pilihan == "00":
        print()
        print(GRAY + "Terima kasih telah menggunakan IyanTools." + RESET)
        if proses_musik:
            proses_musik.terminate()
        break

    # =====================
    # VALIDATION
    # =====================

    if pilihan not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        print()
        print(RED + "Pilihan tidak tersedia." + RESET)
        input(GRAY + "Tekan Enter untuk kembali ke menu..." + RESET)
        continue

    # =====================
    # FEATURES
    # =====================

    if pilihan == "1":
        fitur_cari_sekolah_nama()

    elif pilihan == "2":
        fitur_cari_sekolah_npsn()

    elif pilihan == "3":
        fitur_cek_nik()

    elif pilihan == "4":
        fitur_ip_lookup()

    elif pilihan == "5":
        fitur_stalk_tiktok()

    elif pilihan == "6":
        fitur_stalk_github()

    elif pilihan == "7":
        fitur_generate_password()

    elif pilihan == "8":
        fitur_hash_testing()

    elif pilihan == "9":
        fitur_scrape_website()

    elif pilihan == "10":
        fitur_breach_email()

    # =====================
    # BACK TO MENU
    # =====================

    input(
        "\n" +
        GRAY +
        "Tekan Enter untuk kembali ke menu..." +
        RESET
    )
