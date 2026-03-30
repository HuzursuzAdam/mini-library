"""
mini-library v0 — Basitlestirilmis implementasyon
Ogrenci: Muhammed Mustafa Aydemir 251478095

Kapsam: Sadece init ve add komutlari.
Sinirlamalar: Dongu ve liste henuz kullanilmadi.
  - list komutu sadece dosya icerigini yazdiriyor (formatsiz)
  - borrow/return/delete henuz implemente edilmedi
"""
import sys
import os


# Kitaplarin kaydedilecegi dizin ve dosya yolu
DATA_DIR = ".minilibrary"
DATA_FILE = ".minilibrary/books.dat"


def initialize():
    """Kutuphane dizinini ve bos books.dat dosyasini olusturur."""
    if os.path.exists(DATA_DIR):
        return "Already initialized"
    os.mkdir(DATA_DIR)
    f = open(DATA_FILE, "w")
    f.close()
    return "Initialized empty mini-library in .minilibrary/"


def check_initialized():
    """Kutuphane dizininin var olup olmadigini kontrol eder."""
    if not os.path.exists(DATA_DIR):
        return False
    return True


def add_book(title, author):
    """Yeni kitap ekler. Basit ID hesabi: dosyadaki satir sayisi + 1."""
    if not check_initialized():
        return "Not initialized. Run: python minilibrary.py init"
    # Dosyayi oku ve mevcut satir sayisindan ID hesapla
    f = open(DATA_FILE, "r")
    content = f.read()
    f.close()
    # Dongu kullanmadan basit ID hesabi
    book_id = content.count("\n") + 1
    # Tarih icin sabit deger (datetime modulu henuz gosterilmedi)
    date = "2026-03-16"
    # Kitabi dosyaya yaz
    f = open(DATA_FILE, "a")
    f.write(str(book_id) + "|" + title + "|" + author + "|AVAILABLE|" + date + "\n")
    f.close()
    return "Added book #" + str(book_id) + ": " + title + " by " + author


def show_not_implemented(command_name):
    """Henuz implemente edilmemis komutlar icin bilgi mesaji dondurur."""
    return "Command '" + command_name + "' will be implemented in future weeks."


# --- Ana Program ---
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
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    else:
        print(show_not_implemented("list"))
elif sys.argv[1] == "borrow":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    else:
        print(show_not_implemented("borrow"))
elif sys.argv[1] == "return":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    else:
        print(show_not_implemented("return"))
elif sys.argv[1] == "delete":
    if not check_initialized():
        print("Not initialized. Run: python minilibrary.py init")
    else:
        print(show_not_implemented("delete"))
else:
    print("Unknown command: " + sys.argv[1])
