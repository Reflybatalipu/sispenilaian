"""
Sistem Penilaian Mahasiswa
Implementasi Object Oriented Programming

Author: [Nama Mahasiswa]
Version: 1.0.0
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


# ============================================================
# KONSTANTA
# ============================================================

class BobotPenilaian:
    """Konstanta bobot untuk setiap komponen penilaian."""
    TUGAS = 0.30
    UTS = 0.30
    UAS = 0.40


class BatasGrade:
    """Konstanta batas nilai untuk setiap grade."""
    A = 85
    B = 70
    C = 60
    D = 50


class Grade(Enum):
    """Enum untuk grade mahasiswa."""
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"


# ============================================================
# MODEL DATA
# ============================================================

@dataclass
class Mahasiswa:
    """
    Representasi data mahasiswa.

    Attributes:
        nim: Nomor Induk Mahasiswa
        nama: Nama lengkap mahasiswa
        nilai_tugas: Nilai tugas (0-100)
        nilai_uts: Nilai UTS (0-100)
        nilai_uas: Nilai UAS (0-100)
    """
    nim: str
    nama: str
    nilai_tugas: float
    nilai_uts: float
    nilai_uas: float

    def hitung_nilai_akhir(self) -> float:
        """
        Menghitung nilai akhir berdasarkan bobot penilaian.

        Returns:
            Nilai akhir mahasiswa (0-100)
        """
        return (
            self.nilai_tugas * BobotPenilaian.TUGAS
            + self.nilai_uts * BobotPenilaian.UTS
            + self.nilai_uas * BobotPenilaian.UAS
        )

    def tentukan_grade(self) -> Grade:
        """
        Menentukan grade berdasarkan nilai akhir.

        Returns:
            Grade mahasiswa (A/B/C/D/E)
        """
        nilai_akhir = self.hitung_nilai_akhir()

        if nilai_akhir >= BatasGrade.A:
            return Grade.A
        elif nilai_akhir >= BatasGrade.B:
            return Grade.B
        elif nilai_akhir >= BatasGrade.C:
            return Grade.C
        elif nilai_akhir >= BatasGrade.D:
            return Grade.D
        else:
            return Grade.E


# ============================================================
# REPOSITORY
# ============================================================

class MahasiswaRepository:
    """Repository untuk menyimpan dan mengelola data mahasiswa."""

    def __init__(self):
        self._daftar_mahasiswa: List[Mahasiswa] = []

    def tambah(self, mahasiswa: Mahasiswa) -> None:
        """Menambahkan mahasiswa ke dalam daftar."""
        self._daftar_mahasiswa.append(mahasiswa)

    def get_semua(self) -> List[Mahasiswa]:
        """Mengembalikan semua data mahasiswa."""
        return self._daftar_mahasiswa.copy()

    def cari_by_nim(self, nim: str) -> Optional[Mahasiswa]:
        """Mencari mahasiswa berdasarkan NIM."""
        for m in self._daftar_mahasiswa:
            if m.nim == nim:
                return m
        return None


# ============================================================
# VALIDATOR
# ============================================================

class InputValidator:
    """Kelas untuk validasi input pengguna."""

    @staticmethod
    def validasi_nilai(nilai: float) -> bool:
        """Memvalidasi bahwa nilai berada dalam rentang 0-100."""
        return 0 <= nilai <= 100

    @staticmethod
    def validasi_nim(nim: str) -> bool:
        """Memvalidasi bahwa NIM tidak kosong."""
        return bool(nim.strip())

    @staticmethod
    def validasi_nama(nama: str) -> bool:
        """Memvalidasi bahwa nama tidak kosong."""
        return bool(nama.strip())


# ============================================================
# SERVICE (LOGIKA BISNIS)
# ============================================================

class PenilaianService:
    """Kelas yang menangani logika bisnis penilaian."""

    def __init__(self, repository: MahasiswaRepository):
        self._repository = repository

    def tambah_mahasiswa(self, nim: str, nama: str,
                         nilai_tugas: float, nilai_uts: float,
                         nilai_uas: float) -> str:
        """Menambahkan data mahasiswa baru."""
        if not InputValidator.validasi_nim(nim):
            return "Error: NIM tidak boleh kosong"

        if self._repository.cari_by_nim(nim):
            return "Error: NIM sudah terdaftar"

        if not InputValidator.validasi_nama(nama):
            return "Error: Nama tidak boleh kosong"

        for nilai, label in [(nilai_tugas, "Tugas"),
                             (nilai_uts, "UTS"),
                             (nilai_uas, "UAS")]:
            if not InputValidator.validasi_nilai(nilai):
                return f"Error: Nilai {label} harus antara 0-100"

        mahasiswa = Mahasiswa(nim, nama, nilai_tugas, nilai_uts, nilai_uas)
        self._repository.tambah(mahasiswa)
        return "Data berhasil ditambahkan"

    def tampilkan_semua(self) -> List[dict]:
        """Menampilkan semua data mahasiswa beserta hasil penilaian."""
        hasil = []
        for m in self._repository.get_semua():
            hasil.append({
                "nim": m.nim,
                "nama": m.nama,
                "nilai_tugas": m.nilai_tugas,
                "nilai_uts": m.nilai_uts,
                "nilai_uas": m.nilai_uas,
                "nilai_akhir": m.hitung_nilai_akhir(),
                "grade": m.tentukan_grade().value
            })
        return hasil


# ============================================================
# VIEW (TAMPILAN)
# ============================================================

class PenilaianView:
    """Kelas untuk menangani tampilan antarmuka pengguna."""

    GARIS_PEMISAH = "=" * 60
    GARIS_SUB_PEMISAH = "-" * 60

    @staticmethod
    def tampilkan_header() -> None:
        """Menampilkan header aplikasi."""
        print(PenilaianView.GARIS_PEMISAH)
        print("SISTEM PENILAIAN MAHASISWA".center(60))
        print(PenilaianView.GARIS_PEMISAH)

    @staticmethod
    def tampilkan_menu() -> None:
        """Menampilkan menu utama."""
        print("\nMenu:")
        print("1. Tambah Data Mahasiswa")
        print("2. Tampilkan Data Mahasiswa")
        print("3. Keluar")

    @staticmethod
    def tampilkan_data_mahasiswa(mahasiswa: Mahasiswa) -> None:
        """Menampilkan data satu mahasiswa."""
        print(f"NIM         : {mahasiswa.nim}")
        print(f"Nama        : {mahasiswa.nama}")
        print(f"Nilai Tugas : {mahasiswa.nilai_tugas}")
        print(f"Nilai UTS   : {mahasiswa.nilai_uts}")
        print(f"Nilai UAS   : {mahasiswa.nilai_uas}")
        print(f"Nilai Akhir : {mahasiswa.hitung_nilai_akhir():.2f}")
        print(f"Grade       : {mahasiswa.tentukan_grade().value}")
        print(PenilaianView.GARIS_SUB_PEMISAH)

    @staticmethod
    def tampilkan_semua_mahasiswa(daftar: List[Mahasiswa]) -> None:
        """Menampilkan semua data mahasiswa."""
        if not daftar:
            print("Belum ada data mahasiswa.")
            return

        for mahasiswa in daftar:
            PenilaianView.tampilkan_data_mahasiswa(mahasiswa)

    @staticmethod
    def tampilkan_pesan(pesan: str) -> None:
        """Menampilkan pesan informasi."""
        print(pesan)


# ============================================================
# APPLICATION (MAIN)
# ============================================================

class AplikasiPenilaian:
    """Kelas utama aplikasi penilaian mahasiswa."""

    def __init__(self):
        self._repository = MahasiswaRepository()
        self._service = PenilaianService(self._repository)
        self._view = PenilaianView()

    def _proses_tambah_data(self) -> None:
        """Memproses input tambah data mahasiswa."""
        try:
            nim = input("NIM         : ").strip()
            nama = input("Nama        : ").strip()
            nilai_tugas = float(input("Nilai Tugas : "))
            nilai_uts = float(input("Nilai UTS   : "))
            nilai_uas = float(input("Nilai UAS   : "))

            pesan = self._service.tambah_mahasiswa(
                nim, nama, nilai_tugas, nilai_uts, nilai_uas
            )
            self._view.tampilkan_pesan(pesan)

        except ValueError:
            self._view.tampilkan_pesan("Error: Input nilai harus berupa angka!")

    def _proses_tampilkan_data(self) -> None:
        """Memproses tampilan data mahasiswa."""
        daftar = self._repository.get_semua()
        self._view.tampilkan_semua_mahasiswa(daftar)

    def jalankan(self) -> None:
        """Menjalankan aplikasi."""
        self._view.tampilkan_header()

        while True:
            self._view.tampilkan_menu()
            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                self._proses_tambah_data()
            elif pilihan == "2":
                self._proses_tampilkan_data()
            elif pilihan == "3":
                self._view.tampilkan_pesan("Terima kasih!")
                break
            else:
                self._view.tampilkan_pesan("Pilihan tidak valid!")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app = AplikasiPenilaian()
    app.jalankan()