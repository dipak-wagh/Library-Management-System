from datetime import date, datetime
import json
import os

class Book:
    def __init__(self, isbn, title, author, available=True):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = available

class Member:
    def __init__(self, member_id, name):
        self.id = member_id
        self.name = name
        self.borrowed_books = []  

class Library:
    def __init__(self):
        self.books = {}  
        self.members = {} 

    def add_book(self, isbn, title, author):
        if isbn in self.books:
            print("Book with this ISBN already exists.")
            return
        self.books[isbn] = Book(isbn, title, author)
        print(f"Book '{title}' added successfully.")

    def register_member(self, member_id, name):
        if member_id in self.members:
            print("Member already registered.")
            return
        self.members[member_id] = Member(member_id, name)
        print(f"Member '{name}' registered successfully.")

    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        book = self.books[isbn]
        member = self.members[member_id]

        if not book.available:
            print("Book is currently not available.")
            return

       
        book.available = False

        borrow_date = date.today().isoformat() 
        member.borrowed_books.append({"isbn": isbn, "borrow_date": borrow_date})

        print(f"Book '{book.title}' borrowed by member '{member.name}' on {borrow_date}.")

    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        member = self.members[member_id]
        book = self.books[isbn]

       
        borrowed_entry = None
        for entry in member.borrowed_books:
            if entry['isbn'] == isbn:
                borrowed_entry = entry
                break

        if not borrowed_entry:
            print("This member did not borrow this book.")
            return

      
        return_date = date.today()
        borrow_date = datetime.strptime(borrowed_entry['borrow_date'], '%Y-%m-%d').date()
        days_borrowed = (return_date - borrow_date).days

        if days_borrowed > 7:
            late_fee = days_borrowed - 7
            print(f"Book returned late by {late_fee} days. Late fee is ${late_fee}.")
        else:
            print("Book returned on time. No late fee.")

     
        book.available = True

      
        member.borrowed_books.remove(borrowed_entry)

        print(f"Book '{book.title}' returned by member '{member.name}'.")

    def view_available_books(self):
        print("Available books:")
        for book in self.books.values():
            if book.available:
                print(f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}")

    def view_member_history(self, member_id):
        if member_id not in self.members:
            print("Member not found.")
            return
        member = self.members[member_id]
        if not member.borrowed_books:
            print(f"Member '{member.name}' has no borrowed books currently.")
        else:
            print(f"Borrowed books for member '{member.name}':")
            for entry in member.borrowed_books:
                print(f"ISBN: {entry['isbn']}, Borrow Date: {entry['borrow_date']}")

    def load_data(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as f:
                books_data = json.load(f)
                for book in books_data:
                    self.books[book['isbn']] = Book(
                        isbn=book['isbn'],
                        title=book['title'],
                        author=book['author'],
                        available=book['available']
                    )

        if os.path.exists("members.json"):
            with open("members.json", "r") as f:
                members_data = json.load(f)
                for member in members_data:
                    m = Member(member['id'], member['name'])
                    m.borrowed_books = member.get('borrowed_books', [])
                    self.members[member['id']] = m

    def save_data(self):
        books_data = [
            {
                "isbn": b.isbn,
                "title": b.title,
                "author": b.author,
                "available": b.available
            }
            for b in self.books.values()
        ]

        members_data = [
            {
                "id": m.id,
                "name": m.name,
                "borrowed_books": m.borrowed_books
            }
            for m in self.members.values()
        ]

        with open("books.json", "w") as f:
            json.dump(books_data, f, indent=2)

        with open("members.json", "w") as f:
            json.dump(members_data, f, indent=2)


    def search_books(self, keyword):
        keyword = keyword.lower()
        results = []
        for book in self.books.values():
            if keyword in book.title.lower() or keyword in book.author.lower():
                results.append(book)

        if results:
            print("Search Results:")
            for book in results:
                status = "Available" if book.available else "Borrowed"
                print(f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}, Status: {status}")
        else:
            print("No matching books found.")
