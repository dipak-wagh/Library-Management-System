from library import Library

def main():
    library = Library()
    library.load_data()

    while True:
        print("\nLibrary Menu")
        print("1. Register Member")
        print("2. Add Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. View Member History")
        print("6. View Available Books")
        print("7. Search Books by Title or Author")
        print("8. Exit")

        choice = input("Enter any choice: ")

        if choice == "1":
            member_id = input("Enter member ID: ")
            name = input("Enter name: ")
            library.register_member(member_id, name)

        elif choice == "2":
            isbn = input("Enter ISBN: ")
            title = input("Enter title: ")
            author = input("Enter author: ")
            library.add_book(isbn, title, author)

        elif choice == "3":
            member_id = input("Enter member ID: ")
            isbn = input("Enter ISBN of book to borrow: ")
            library.borrow_book(member_id, isbn)

        elif choice == "4":
            member_id = input("Enter member ID: ")
            isbn = input("Enter ISBN of book to return: ")
            library.return_book(member_id, isbn)

        elif choice == "5":
            member_id = input("Enter member ID: ")
            library.view_member_history(member_id)

        elif choice == "6":
            library.view_available_books()

        elif choice == "7":
            keyword = input("Enter keyword to search (title or author): ")
            library.search_books(keyword)

        elif choice == "8":
            print("Saving data")
            library.save_data()
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
