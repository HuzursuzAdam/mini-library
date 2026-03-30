"""
mini-library SPEC test senaryolari - V1
Ogrenci: Ogrenci Adi (Ogrenci No)
Proje: mini-library

V1 Gorev Listesi:
  1. list komutu implemente edildi (while dongusu ile satir satir okuma)
  2. borrow ve return komutlari implemente edildi (sure takibi ile)
  3. delete komutu implemente edildi
  4. request ve listrequests komutlari implemente edildi
  5. Hata mesajlari iyilestirildi
"""
import subprocess
import os
import shutil


# --- Yardimci Fonksiyon ---
def run_cmd(args):
    """Komutu calistir, stdout dondur."""
    result = subprocess.run(
        ["python", "minilibrary.py"] + args,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def setup_function():
    """Her testten once temiz baslangic."""
    if os.path.exists(".minilibrary"):
        shutil.rmtree(".minilibrary")


# ========================================
# init testleri
# ========================================

def test_init_creates_directory():
    output = run_cmd(["init"])
    assert os.path.exists(".minilibrary"), ".minilibrary dizini olusturulmali"
    assert os.path.exists(".minilibrary/books.dat"), "books.dat dosyasi olusturulmali"
    assert os.path.exists(".minilibrary/requests.dat"), "requests.dat dosyasi olusturulmali"


def test_init_already_exists():
    run_cmd(["init"])
    output = run_cmd(["init"])
    assert "Already initialized" in output


# ========================================
# add testleri
# ========================================

def test_add_single_book():
    run_cmd(["init"])
    output = run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    assert "Added book #1" in output
    assert "The Little Prince" in output


def test_add_multiple_books():
    run_cmd(["init"])
    run_cmd(["add", "Book One", "Author One"])
    output = run_cmd(["add", "Book Two", "Author Two"])
    assert "#2" in output


# ========================================
# list testleri
# ========================================

def test_list_empty():
    run_cmd(["init"])
    output = run_cmd(["list"])
    assert "No books found" in output


def test_list_shows_books():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    output = run_cmd(["list"])
    assert "The Little Prince" in output
    assert "AVAILABLE" in output


def test_list_shows_multiple_books():
    run_cmd(["init"])
    run_cmd(["add", "Book One", "Author One"])
    run_cmd(["add", "Book Two", "Author Two"])
    output = run_cmd(["list"])
    assert "Book One" in output
    assert "Book Two" in output


# ========================================
# borrow testleri
# ========================================

def test_borrow_marks_book():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    output = run_cmd(["borrow", "1"])
    assert "borrowed" in output
    assert "Due date" in output


def test_borrow_nonexistent():
    run_cmd(["init"])
    output = run_cmd(["borrow", "99"])
    assert "not found" in output


def test_borrow_already_borrowed():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    run_cmd(["borrow", "1"])
    output = run_cmd(["borrow", "1"])
    assert "already borrowed" in output


def test_borrow_shows_countdown():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    run_cmd(["borrow", "1"])
    output = run_cmd(["borrow", "1"])
    assert "available in" in output or "overdue" in output


# ========================================
# return testleri
# ========================================

def test_return_marks_book():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    run_cmd(["borrow", "1"])
    output = run_cmd(["return", "1"])
    assert "returned" in output


def test_return_nonexistent():
    run_cmd(["init"])
    output = run_cmd(["return", "99"])
    assert "not found" in output


def test_return_not_borrowed():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    output = run_cmd(["return", "1"])
    assert "not borrowed" in output


# ========================================
# delete testleri
# ========================================

def test_delete_removes_book():
    run_cmd(["init"])
    run_cmd(["add", "The Little Prince", "Antoine de Saint-Exupery"])
    output = run_cmd(["delete", "1"])
    assert "Deleted" in output
    list_output = run_cmd(["list"])
    assert "The Little Prince" not in list_output


def test_delete_nonexistent():
    run_cmd(["init"])
    output = run_cmd(["delete", "99"])
    assert "not found" in output


# ========================================
# request testleri
# ========================================

def test_request_new_book():
    run_cmd(["init"])
    output = run_cmd(["request", "Clean Code", "Robert C. Martin"])
    assert "Request recorded" in output
    assert "1/3" in output


def test_request_increment():
    run_cmd(["init"])
    run_cmd(["request", "Clean Code", "Robert C. Martin"])
    output = run_cmd(["request", "Clean Code", "Robert C. Martin"])
    assert "2/3" in output


def test_request_triggers_order():
    run_cmd(["init"])
    run_cmd(["request", "Clean Code", "Robert C. Martin"])
    run_cmd(["request", "Clean Code", "Robert C. Martin"])
    output = run_cmd(["request", "Clean Code", "Robert C. Martin"])
    assert "Order placed" in output


def test_request_existing_book():
    run_cmd(["init"])
    run_cmd(["add", "Clean Code", "Robert C. Martin"])
    output = run_cmd(["request", "Clean Code", "Robert C. Martin"])
    assert "already exists" in output


# ========================================
# listrequests testleri
# ========================================

def test_listrequests_empty():
    run_cmd(["init"])
    output = run_cmd(["listrequests"])
    assert "No pending requests" in output


def test_listrequests_shows_requests():
    run_cmd(["init"])
    run_cmd(["request", "Clean Code", "Robert C. Martin"])
    output = run_cmd(["listrequests"])
    assert "Clean Code" in output
    assert "1/3" in output


# ========================================
# hata testleri
# ========================================

def test_command_before_init():
    output = run_cmd(["add", "Some Book", "Some Author"])
    assert "Not initialized" in output


def test_unknown_command():
    run_cmd(["init"])
    output = run_cmd(["fly"])
    assert "Unknown command" in output


def test_missing_arguments_add():
    run_cmd(["init"])
    output = run_cmd(["add"])
    assert "Usage" in output
