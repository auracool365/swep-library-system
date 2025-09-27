### Library System Features:
    # User registration and authentication
    # Book catalog management
    # Book borrowing and returning
    # Automatic fine calculation
    # Search functionality
    # Transaction tracking
    # Overdue book monitoring
    # JSON file-based storage
    
from library_management import LibraryManagementSystem
from models import User, Book

# Main() with the driver code to test the system 
def main():
    library = LibraryManagementSystem()
    
    print("\nLibrary Book Borrowing and Returning System\n")
    
    # Sample data
    print("Registering users...")
    
    # Register sample users
    student = User("CSCstu01", 
                   "Cornelius Mamman", 
                   "comamman@student.lautech.edu.ng", 
                   "student", 
                   "Computer Science",
                   "081********"
            )
    library.register_user(student, "123abc456")
    
    staff = User("CSC001", 
                 "Dr. John Doe", 
                 "Doe@lautech.edu.ng", 
                 "faculty", 
                 "Computer Science",
                 "080********"
            )
    library.register_user(staff, "987654321")
    
    print("\nAdding books...")
    
    # Adding books (These are some of my favorite books)
    book_1 = Book("0-226-50040-3", 
                 "Art of War", 
                 "Niccolo Machiavelli", 
                 "University of Chicago Press", 
                 1521, 
                 "Military Strategy/Political Philosophy", 
                 1, 
                 "MS-001"
            )
    library.add_book(book_1)
    
    book_2 = Book("0-671-65991-x", 
                 "Diplomacy", 
                 "Henry Kissinger", 
                 "Simon & Schuster", 
                 1994, 
                 "Foreign Relations", 
                 2, 
                 "FR-002"
            )
    library.add_book(book_2)
    
    book_3 = Book("978-1-449-34418-4", 
                 "Understanding and Using C Pointers", 
                 "Richard Reese", 
                 "O'Reilly", 
                 2013, 
                 "Computer Programming", 
                 1, 
                 "CP-003"
            )
    library.add_book(book_3)
    
    book_4 = Book("0099922800", 
                  "Brothers Karamazov", 
                  "Fyodor Dostoevsky", 
                  "Penguin Classics", 
                  1880, 
                  "Fiction", 
                  1, 
                  "FIC-004"
            )
    library.add_book(book_4)
    
    # Search book
    print("\nSearching for fictional books:")
    fictional_books = library.search_books("Brothers", "title")
    
    # Display search results
    for book in fictional_books:
        print(f"- {book['title']} by {book['author']} (Available: {book['available_copies']})")
    
    # Borrow a book
    print(f"\n{student.name} borrowing 'Brothers Karamazov':")
    library.borrow_book("CSCstu01", "0099922800")
    
    # Check updated availability
    print("\nUpdated availability for 'Brothers Karamazov':")
    updated_books = library.search_books("0099922800", "isbn")
    
    # Display updated book info
    for book in updated_books:
        print(f"- {book['title']} (Available: {book['available_copies']}/{book['total_copies']})")
    
    # View user transactions
    print(f"\nTransaction history for {student.name}:")
    transactions = library.get_user_transactions("CSCstu01")
    for transaction in transactions:
        print(f"- {transaction['book_title']} - {transaction['transaction_type']} "
              f"on {transaction['transaction_date'][:10]} "
              f"(Due: {transaction['due_date'][:10]})")
    
    # Generate reports
    print("\n=== Library Reports ===")
    reports = library.generate_reports()
    print(f"Total book titles: {reports['total_titles']}")
    print(f"Total book copies: {reports['total_copies']}")
    print(f"Total registered users: {reports['total_users']}")
    print(f"Active borrowings: {reports['active_borrowings']}")
    print(f"Overdue books: {reports['overdue_books']}")
    print(f"Total fines collected: ₦{reports['total_fines']:.2f}")

if __name__ == "__main__":
    main()