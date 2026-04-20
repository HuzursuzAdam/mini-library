#!/usr/bin/env python3
import sys
import os
import datetime

DIR_NAME = ".minilibrary"
BOOKS_FILE = os.path.join(DIR_NAME, "books.dat")
REQUESTS_FILE = os.path.join(DIR_NAME, "requests.dat")
BORROWERS_FILE = os.path.join(DIR_NAME, "borrowers.dat")
BLACKLIST_FILE = os.path.join(DIR_NAME, "blacklist.dat")

def check_initialized():
    if not os.path.exists(DIR_NAME):
        print("Not initialized. Run: python minilibrary.py init")
        sys.exit(1)

def get_today():
    return datetime.date.today()

# --- Veri Okuma / Yazma Yardımcı Fonksiyonları ---

def read_books():
    books = []
    if not os.path.exists(BOOKS_FILE): return books
    with open(BOOKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|')
            if len(parts) == 7:
                books.append({
                    'id': int(parts[0]),
                    'title': parts[1],
                    'author': parts[2],
                    'status': parts[3],
                    'added_date': parts[4],
                    'borrow_date': parts[5],
                    'borrower': parts[6]
                })
    return books

def write_books(books):
    with open(BOOKS_FILE, 'w', encoding='utf-8') as f:
        for b in books:
            f.write(f"{b['id']}|{b['title']}|{b['author']}|{b['status']}|{b['added_date']}|{b['borrow_date']}|{b['borrower']}\n")

def read_borrowers():
    borrowers = {}
    if not os.path.exists(BORROWERS_FILE): return borrowers
    with open(BORROWERS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                person, count = line.strip().split('|')
                borrowers[person] = int(count)
    return borrowers

def write_borrowers(borrowers):
    with open(BORROWERS_FILE, 'w', encoding='utf-8') as f:
        for person, count in borrowers.items():
            f.write(f"{person}|{count}\n")

def read_blacklist():
    blacklist = set()
    if not os.path.exists(BLACKLIST_FILE): return blacklist
    with open(BLACKLIST_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                blacklist.add(line.strip())
    return blacklist

def write_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w', encoding='utf-8') as f:
        for person in blacklist:
            f.write(f"{person}\n")

def read_requests():
    reqs = {}
    if not os.path.exists(REQUESTS_FILE): return reqs
    with open(REQUESTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                title, author, count = line.strip().split('|')
                reqs[(title, author)] = int(count)
    return reqs

def write_requests(reqs):
    with open(REQUESTS_FILE, 'w', encoding='utf-8') as f:
        for (title, author), count in reqs.items():
            f.write(f"{title}|{author}|{count}\n")

# --- Komut İşlevleri ---

def cmd_init():
    if os.path.exists(DIR_NAME):
        print("Already initialized")
        sys.exit(0)
    
    os.makedirs(DIR_NAME)
    open(BOOKS_FILE, 'w').close()
    open(REQUESTS_FILE, 'w').close()
    open(BORROWERS_FILE, 'w').close()
    open(BLACKLIST_FILE, 'w').close()
    print(f"Initialized empty mini-library in {DIR_NAME}/")
    sys.exit(0)

def cmd_add(title, author):
    check_initialized()
    books = read_books()
    new_id = max([b['id'] for b in books], default=0) + 1
    today = get_today().isoformat()
    
    books.append({
        'id': new_id, 'title': title, 'author': author,
        'status': 'AVAILABLE', 'added_date': today,
        'borrow_date': '', 'borrower': ''
    })
    write_books(books)
    print(f"Book #{new_id} added.")

def cmd_list():
    check_initialized()
    books = read_books()
    if not books:
        print("No books in the library.")
        return
    for b in books:
        print(f"{b['id']}|{b['title']}|{b['author']}|{b['status']}|{b['added_date']}|{b['borrow_date']}|{b['borrower']}")

def cmd_borrow(book_id_str, person):
    check_initialized()
    try:
        book_id = int(book_id_str)
    except ValueError:
        print("Invalid book ID.")
        sys.exit(1)

    blacklist = read_blacklist()
    if person in blacklist:
        print(f"User is blacklisted: {person}")
        sys.exit(1)

    books = read_books()
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        print(f"Book #{book_id} not found.")
        sys.exit(1)

    if book['status'] == 'BORROWED':
        print(f"Book #{book_id} is already borrowed.")
        sys.exit(1)

    today = get_today()
    due_date = today + datetime.timedelta(days=14)
    
    book['status'] = 'BORROWED'
    book['borrow_date'] = today.isoformat()
    book['borrower'] = person

    write_books(books)
    print(f"Book #{book_id} borrowed. Due date: {due_date.isoformat()}")

def cmd_return(book_id_str):
    check_initialized()
    try:
        book_id = int(book_id_str)
    except ValueError:
        print("Invalid book ID.")
        sys.exit(1)

    books = read_books()
    book = next((b for b in books if b['id'] == book_id), None)

    if not book:
        print(f"Book #{book_id} not found.")
        sys.exit(1)

    if book['status'] != 'BORROWED':
        print(f"Book #{book_id} is not borrowed.")
        sys.exit(0)

    borrow_date = datetime.date.fromisoformat(book['borrow_date'])
    due_date = borrow_date + datetime.timedelta(days=14)
    today = get_today()

    if today > due_date:
        person = book['borrower']
        borrowers = read_borrowers()
        borrowers[person] = borrowers.get(person, 0) + 1
        write_borrowers(borrowers)

        if borrowers[person] >= 3:
            blacklist = read_blacklist()
            if person not in blacklist:
                blacklist.add(person)
                write_blacklist(blacklist)

    book['status'] = 'AVAILABLE'
    book['borrow_date'] = ''
    book['borrower'] = ''

    write_books(books)
    print(f"Book #{book_id} returned.")

def cmd_delete(book_id_str):
    check_initialized()
    try:
        book_id = int(book_id_str)
    except ValueError:
        print("Invalid book ID.")
        sys.exit(1)

    books = read_books()
    new_books = [b for b in books if b['id'] != book_id]
    
    if len(books) == len(new_books):
        print(f"Book #{book_id} not found.")
        sys.exit(1)
        
    write_books(new_books)
    print(f"Book #{book_id} deleted.")

def cmd_request(title, author):
    check_initialized()
    reqs = read_requests()
    key = (title, author)
    reqs[key] = reqs.get(key, 0) + 1
    write_requests(reqs)
    print(f"Request added for '{title}' by {author}.")

def cmd_listrequests():
    check_initialized()
    reqs = read_requests()
    if not reqs:
        print("No requests.")
        return
    for (title, author), count in reqs.items():
        print(f"{title}|{author}|{count}")

def cmd_blacklist():
    check_initialized()
    blacklist = read_blacklist()
    if not blacklist:
        print("No blacklisted users.")
        sys.exit(0)
    for person in blacklist:
        print(person)

def cmd_listborrowers():
    check_initialized()
    borrowers = read_borrowers()
    if not borrowers:
        print("No borrower records.")
        sys.exit(0)
    for person, count in borrowers.items():
        print(f"{person} - {count}")

# --- Ana Çalıştırma Bloğu ---

def main():
    if len(sys.argv) < 2:
        print("Usage: minilibrary <command> [args]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "add" and len(sys.argv) == 4:
        cmd_add(sys.argv[2], sys.argv[3])
    elif cmd == "list":
        cmd_list()
    elif cmd == "borrow" and len(sys.argv) == 4:
        cmd_borrow(sys.argv[2], sys.argv[3])
    elif cmd == "return" and len(sys.argv) == 3:
        cmd_return(sys.argv[2])
    elif cmd == "delete" and len(sys.argv) == 3:
        cmd_delete(sys.argv[2])
    elif cmd == "request" and len(sys.argv) == 4:
        cmd_request(sys.argv[2], sys.argv[3])
    elif cmd == "listrequests":
        cmd_listrequests()
    elif cmd == "blacklist":
        cmd_blacklist()
    elif cmd == "listborrowers":
        cmd_listborrowers()
    else:
        print("Invalid command or arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()
