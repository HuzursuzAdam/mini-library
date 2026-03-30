"""
mini-library v1 — While dongusu ile gelistirilmis versiyon
Ogrenci: Ogrenci Adi (Ogrenci No)
 
V1 Gorev Listesi:
  1. list komutu implemente edildi (while dongusu ile satir satir okuma)
  2. borrow ve return komutlari implemente edildi (14 gun sure takibi)
  3. delete komutu implemente edildi
  4. request ve listrequests komutlari implemente edildi
  5. Hata mesajlari iyilestirildi
 
V0 -> V1 Degisiklikler:
  - V0: Sadece init ve add calisiyordu
  - V1: Tum komutlar while dongusu ile implemente edildi
  - V1: Odunc sure takibi (14 gun) eklendi
  - V1: Kitap talep sistemi (3 istek = siparis) eklendi
  - V1: requests.dat dosyasi eklendi
 
Sinirlamalar: for dongusu ve liste ([]) henuz kullanilmadi.
"""
import sys
import os
import datetime
 
 
# Kitaplarin kaydedilecegi dizin ve dosya yollari
DATA_DIR = ".minilibrary"
BOOKS_FILE = ".minilibrary/books.dat"
REQUESTS_FILE = ".minilibrary/requests.dat"
 
 
def check_initialized():
    """Kutuphane dizininin var olup olmadigini kontrol eder."""
    if os.path.exists(DATA_DIR):
        return True
    return False
 
 
def get_today():
    """Bugunku tarihi YYYY-MM-DD formatinda dondurur."""
    today = datetime.date.today()
    return str(today)
 
 
def count_lines(filepath):
    """Dosyadaki satir sayisini while dongusu ile sayar."""
    f = open(filepath, "r")
    count = 0
    line = f.readline()
    while line != "":
        if line.strip() != "":
            count = count + 1
        line = f.readline()
    f.close()
    return count
 
 
# ========================================
# INIT KOMUTU
# ========================================
 
def initialize():
    """Kutuphane dizinini, books.dat ve requests.dat dosyalarini olusturur."""
    if os.path.exists(DATA_DIR):
        return "Already initialized"
    os.mkdir(DATA_DIR)
    f = open(BOOKS_FILE, "w")
    f.close()
    f = open(REQUESTS_FILE, "w")
    f.close()
    return "Initialized empty mini-library in .minilibrary/"
 
 
# ========================================
# ADD KOMUTU
# ========================================
 
def add_book(title, author):
    """Yeni kitap ekler. ID hesabi satir sayisi + 1."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    book_id = count_lines(BOOKS_FILE) + 1
    today = get_today()
    # Dosyaya yeni kitap satirini ekle
    f = open(BOOKS_FILE, "a")
    f.write(str(book_id) + "|" + title + "|" + author + "|AVAILABLE|" + today + "|\n")
    f.close()
    return "Added book #" + str(book_id) + ": " + title + " by " + author
 
 
# ========================================
# LIST KOMUTU
# ========================================
 
def list_books():
    """Tum kitaplari while dongusu ile satir satir okuyup listeler."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    f = open(BOOKS_FILE, "r")
    line = f.readline()
    found = False
    output = ""
    while line != "":
        if line.strip() != "":
            found = True
            parts = line.strip().split("|")
            book_id = parts[0]
            title = parts[1]
            author = parts[2]
            status = parts[3]
            added_date = parts[4]
            borrow_date = parts[5]
            if status == "BORROWED" and borrow_date != "":
                # Odunc tarihi + 14 gun = iade tarihi
                borrow_parts = borrow_date.split("-")
                b_year = int(borrow_parts[0])
                b_month = int(borrow_parts[1])
                b_day = int(borrow_parts[2])
                due = datetime.date(b_year, b_month, b_day) + datetime.timedelta(days=14)
                output = output + "  [" + book_id + "] [BORROWED] " + title + " - " + author + " (" + added_date + ") [Due: " + str(due) + "]\n"
            else:
                output = output + "  [" + book_id + "] [AVAILABLE] " + title + " - " + author + " (" + added_date + ")\n"
        line = f.readline()
    f.close()
    if not found:
        return "No books found."
    return output.strip()
 
 
# ========================================
# BORROW KOMUTU
# ========================================
 
def borrow_book(book_id_str):
    """Kitabi odunc verir. Sure takibi yapar, countdown gosterir."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    # Dosyayi oku, ilgili satiri bul ve degistir
    f = open(BOOKS_FILE, "r")
    content = ""
    found = False
    result = ""
    line = f.readline()
    while line != "":
        if line.strip() != "":
            parts = line.strip().split("|")
            if parts[0] == book_id_str:
                found = True
                if parts[3] == "BORROWED":
                    # Zaten odunc — kalan gun hesapla
                    borrow_date = parts[5]
                    borrow_parts = borrow_date.split("-")
                    b_year = int(borrow_parts[0])
                    b_month = int(borrow_parts[1])
                    b_day = int(borrow_parts[2])
                    due = datetime.date(b_year, b_month, b_day) + datetime.timedelta(days=14)
                    today = datetime.date.today()
                    remaining = (due - today).days
                    if remaining > 0:
                        result = "Book #" + book_id_str + " is already borrowed. It will be available in " + str(remaining) + " days."
                    else:
                        result = "Book #" + book_id_str + " is overdue. It should be returned immediately."
                    content = content + line
                else:
                    # AVAILABLE -> BORROWED yap
                    today = get_today()
                    due = datetime.date.today() + datetime.timedelta(days=14)
                    content = content + parts[0] + "|" + parts[1] + "|" + parts[2] + "|BORROWED|" + parts[4] + "|" + today + "\n"
                    result = "Book #" + book_id_str + " borrowed. Due date: " + str(due)
            else:
                content = content + line
        line = f.readline()
    f.close()
    if not found:
        return "Book #" + book_id_str + " not found."
    # Dosyayi guncellenmis icerikle yeniden yaz
    f = open(BOOKS_FILE, "w")
    f.write(content)
    f.close()
    return result
 
 
# ========================================
# RETURN KOMUTU
# ========================================
 
def return_book(book_id_str):
    """Odunc alinan kitabi iade eder, borrow_date alanini temizler."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    f = open(BOOKS_FILE, "r")
    content = ""
    found = False
    result = ""
    line = f.readline()
    while line != "":
        if line.strip() != "":
            parts = line.strip().split("|")
            if parts[0] == book_id_str:
                found = True
                if parts[3] == "AVAILABLE":
                    result = "Book #" + book_id_str + " is not borrowed."
                    content = content + line
                else:
                    # BORROWED -> AVAILABLE yap, borrow_date temizle
                    content = content + parts[0] + "|" + parts[1] + "|" + parts[2] + "|AVAILABLE|" + parts[4] + "|\n"
                    result = "Book #" + book_id_str + " returned."
            else:
                content = content + line
        line = f.readline()
    f.close()
    if not found:
        return "Book #" + book_id_str + " not found."
    f = open(BOOKS_FILE, "w")
    f.write(content)
    f.close()
    return result
 
 
# ========================================
# DELETE KOMUTU
# ========================================
 
def delete_book(book_id_str):
    """Kitabi books.dat dosyasindan siler."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    f = open(BOOKS_FILE, "r")
    content = ""
    found = False
    line = f.readline()
    while line != "":
        if line.strip() != "":
            parts = line.strip().split("|")
            if parts[0] == book_id_str:
                found = True
                # Bu satiri ekleme — silmis oluyoruz
            else:
                content = content + line
        line = f.readline()
    f.close()
    if not found:
        return "Book #" + book_id_str + " not found."
    f = open(BOOKS_FILE, "w")
    f.write(content)
    f.close()
    return "Deleted book #" + book_id_str + "."
 
 
# ========================================
# REQUEST KOMUTU
# ========================================
 
def check_book_exists(title, author):
    """Kitabin books.dat icinde olup olmadigini kontrol eder."""
    f = open(BOOKS_FILE, "r")
    line = f.readline()
    while line != "":
        if line.strip() != "":
            parts = line.strip().split("|")
            if parts[1] == title and parts[2] == author:
                f.close()
                return True
        line = f.readline()
    f.close()
    return False
 
 
def request_book(title, author):
    """Kitap talep eder. 3 talebe ulasinca siparis verir."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    # Kitap zaten kutuphanede mi kontrol et
    if check_book_exists(title, author):
        return "Book already exists in library: " + title
    # requests.dat dosyasini oku, ayni kitabi ara
    f = open(REQUESTS_FILE, "r")
    content = ""
    found = False
    new_count = 0
    line = f.readline()
    while line != "":
        if line.strip() != "":
            parts = line.strip().split("|")
            if parts[0] == title and parts[1] == author:
                found = True
                new_count = int(parts[2]) + 1
                if new_count >= 3:
                    # Siparis verildi — bu satiri dosyadan cikar
                    pass
                else:
                    content = content + title + "|" + author + "|" + str(new_count) + "\n"
            else:
                content = content + line
        line = f.readline()
    f.close()
    if not found:
        # Yeni talep ekle
        new_count = 1
        content = content + title + "|" + author + "|1\n"
    # Dosyayi guncelle
    f = open(REQUESTS_FILE, "w")
    f.write(content)
    f.close()
    if new_count >= 3:
        return "Order placed for: " + title + " by " + author
    return "Request recorded for: " + title + " by " + author + " (" + str(new_count) + "/3)"
 
 
# ========================================
# LISTREQUESTS KOMUTU
# ========================================
 
def list_requests():
    """Bekleyen kitap taleplerini listeler."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    f = open(REQUESTS_FILE, "r")
    line = f.readline()
    found = False
    output = ""
    while line != "":
        if line.strip() != "":
            found = True
            parts = line.strip().split("|")
            title = parts[0]
            author = parts[1]
            count = parts[2]
            output = output + "  [" + count + "/3] " + title + " - " + author + "\n"
        line = f.readline()
    f.close()
    if not found:
        return "No pending requests."
    return output.strip()
 
 
# ========================================
# ANA PROGRAM
# ========================================
# Komut satiri argumanlarini kontrol et ve uygun fonksiyonu cagir
 
if len(sys.argv) < 2:
    print("Usage: python minilibrary.py <command> [args]")
elif sys.argv[1] == "init":
    print(initialize())
elif sys.argv[1] == "add":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    elif len(sys.argv) < 4:
        print("Usage: python minilibrary.py add <title> <author>")
    else:
        print(add_book(sys.argv[2], sys.argv[3]))
elif sys.argv[1] == "list":
    print(list_books())
elif sys.argv[1] == "borrow":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    elif len(sys.argv) < 3:
        print("Usage: python minilibrary.py borrow <id>")
    else:
        print(borrow_book(sys.argv[2]))
elif sys.argv[1] == "return":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    elif len(sys.argv) < 3:
        print("Usage: python minilibrary.py return <id>")
    else:
        print(return_book(sys.argv[2]))
elif sys.argv[1] == "delete":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    elif len(sys.argv) < 3:
        print("Usage: python minilibrary.py delete <id>")
    else:
        print(delete_book(sys.argv[2]))
elif sys.argv[1] == "request":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    elif len(sys.argv) < 4:
        print("Usage: python minilibrary.py request <title> <author>")
    else:
        print(request_book(sys.argv[2], sys.argv[3]))
elif sys.argv[1] == "listrequests":
    print(list_requests())
else:
    print("Unknown command: " + sys.argv[1])
 
