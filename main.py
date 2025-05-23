from library import Library

def displayMenu():
    print("\nLibrary Management System")
    print("1. Register Member")
    print("2. Add Book")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Available Books")
    print("6. View Member History")
    print("7. Search Books")
    print("8. Exit")

def main():
    library = Library()
    library.loadData()

    while True:
        displayMenu()
        choice = input("Enter your choice: ")

        if choice == '1':
            memberId = input("Enter Member ID: ")
            name = input("Enter Member Name: ")
            library.registerMember(memberId, name)

        elif choice == '2':
            isbn = input("Enter ISBN: ")
            title = input("Enter Book Title: ")
            author = input("Enter Author Name: ")
            library.addBook(isbn, title, author)

        elif choice == '3':
            memberId = input("Enter Member ID: ")
            isbn = input("Enter ISBN: ")
            library.borrowBook(memberId, isbn)

        elif choice == '4':
            memberId = input("Enter Member ID: ")
            isbn = input("Enter ISBN: ")
            library.returnBook(memberId, isbn)

        elif choice == '5':
            library.viewAvailableBooks()

        elif choice == '6':
            memberId = input("Enter Member ID: ")
            library.viewMemberHistory(memberId)

        elif choice == '7':
            keyword = input("Enter title or author keyword: ")
            library.searchBooks(keyword)

        elif choice == '8':
            library.saveData()
            print("Library data saved. Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
