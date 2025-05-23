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
    def __init__(self, memberId, name):
        self.id = memberId
        self.name = name
        self.borrowedBooks = []

class Library:
    def __init__(self):
        self.books = {}
        self.members = {}

    def addBook(self, isbn, title, author):
        if isbn in self.books:
            print("Book with this ISBN already exists.")
            return
        self.books[isbn] = Book(isbn, title, author)
        print(f"Book '{title}' added successfully.")

    def registerMember(self, memberId, name):
        if memberId in self.members:
            print("Member already registered.")
            return
        self.members[memberId] = Member(memberId, name)
        print(f"Member '{name}' registered successfully.")

    def borrowBook(self, memberId, isbn):
        if memberId not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        book = self.books[isbn]
        member = self.members[memberId]

        if not book.available:
            print("Book is currently not available.")
            return

        book.available = False
        borrowDate = date.today().isoformat()
        member.borrowedBooks.append({"isbn": isbn, "borrowDate": borrowDate})

        print(f"Book '{book.title}' borrowed by member '{member.name}' on {borrowDate}.")

    def returnBook(self, memberId, isbn):
        if memberId not in self.members:
            print("Member not found.")
            return
        if isbn not in self.books:
            print("Book not found.")
            return

        member = self.members[memberId]
        book = self.books[isbn]

        borrowedEntry = None
        for entry in member.borrowedBooks:
            if entry['isbn'] == isbn:
                borrowedEntry = entry
                break

        if not borrowedEntry:
            print("This member did not borrow this book.")
            return

        returnDate = date.today()
        borrowDate = datetime.strptime(borrowedEntry['borrowDate'], '%Y-%m-%d').date()
        daysBorrowed = (returnDate - borrowDate).days

        if daysBorrowed > 7:
            lateFee = daysBorrowed - 7
            print(f"Book returned late by {lateFee} days. Late fee is ${lateFee}.")
        else:
            print("Book returned on time. No late fee.")

        book.available = True
        member.borrowedBooks.remove(borrowedEntry)

        print(f"Book '{book.title}' returned by member '{member.name}'.")

    def viewAvailableBooks(self):
        print("Available books:")
        for book in self.books.values():
            if book.available:
                print(f"ISBN: {book.isbn}, Title: {book.title}, Author: {book.author}")

    def viewMemberHistory(self, memberId):
        if memberId not in self.members:
            print("Member not found.")
            return
        member = self.members[memberId]
        if not member.borrowedBooks:
            print(f"Member '{member.name}' has no borrowed books currently.")
        else:
            print(f"Borrowed books for member '{member.name}':")
            for entry in member.borrowedBooks:
                print(f"ISBN: {entry['isbn']}, Borrow Date: {entry['borrowDate']}")

    def loadData(self):
        if os.path.exists("books.json"):
            with open("books.json", "r") as f:
                booksData = json.load(f)
                for book in booksData:
                    self.books[book['isbn']] = Book(
                        isbn=book['isbn'],
                        title=book['title'],
                        author=book['author'],
                        available=book['available']
                    )

        if os.path.exists("members.json"):
            with open("members.json", "r") as f:
                membersData = json.load(f)
                for member in membersData:
                    m = Member(member['id'], member['name'])
                    m.borrowedBooks = member.get('borrowedBooks', [])
                    self.members[member['id']] = m

    def saveData(self):
        booksData = [
            {
                "isbn": b.isbn,
                "title": b.title,
                "author": b.author,
                "available": b.available
            }
            for b in self.books.values()
        ]

        membersData = [
            {
                "id": m.id,
                "name": m.name,
                "borrowedBooks": m.borrowedBooks
            }
            for m in self.members.values()
        ]

        with open("books.json", "w") as f:
            json.dump(booksData, f, indent=2)

        with open("members.json", "w") as f:
            json.dump(membersData, f, indent=2)

    def searchBooks(self, keyword):
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
