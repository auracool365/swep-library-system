import datetime
import hashlib
from typing import List, Dict

from file_manager import LibraryFileManager
from models import User, Book

# Library management system  with all the system functionalities (Business logic as it is called)

class LibraryManagementSystem:
    # Initialize the library management system
    def __init__(self):
        self.file_manager = LibraryFileManager()
        self.loan_periods = {
            'student': 14,  # 14 days
            'staff': 30,    # 30 days
            'faculty': 60,   # 60 days
            'alumni' : 80  # 80
        }
        self.fine_per_day = 50.0  # ₦50 per day
        self.next_transaction_id = self._get_next_transaction_id()
        self.next_reservation_id = self._get_next_reservation_id()
    
    # Get next transaction ID
    def _get_next_transaction_id(self) -> int:
        transactions = self.file_manager.read_data(self.file_manager.transactions_file)
        if not transactions:
            return 1
        return max([t.get('transaction_id', 0) for t in transactions]) + 1
    
    # Get next reservation ID
    def _get_next_reservation_id(self) -> int:
        reservations = self.file_manager.read_data(self.file_manager.reservations_file)
        if not reservations:
            return 1
        return max([r.get('reservation_id', 0) for r in reservations]) + 1
    
    # Hash password using SHA-256
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    # User registration
    def register_user(self, user: User, password: str) -> bool:
        try:
            users = self.file_manager.read_data(self.file_manager.users_file)
            
            # Check if user already exists
            for existing_user in users:
                if existing_user['user_id'] == user.user_id or existing_user['email'] == user.email:
                    print(f"Error: User with ID {user.user_id} or email {user.email} already exists!")
                    return False
            
            # Add password hash to user data
            user_data = user.convert_to_map()
            user_data['password_hash'] = self.hash_password(password)
            
            users.append(user_data)
            self.file_manager.write_data(self.file_manager.users_file, users)
            
            print(f"User {user.name} registered successfully!")
            return True
            
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
    
    # Add a new book to catalog
    def add_book(self, book: Book) -> bool:
        try:
            books = self.file_manager.read_data(self.file_manager.books_file)
            
            # Check if book already exists
            for existing_book in books:
                if existing_book['isbn'] == book.isbn:
                    print(f"Error: Book with ISBN {book.isbn} already exists!")
                    return False
            
            books.append(book.convert_to_map())
            self.file_manager.write_data(self.file_manager.books_file, books)
            
            print(f"Book '{book.title}' added successfully!")
            return True
            
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    # Search books by title, author, or ISBN
    def search_books(self, query: str, search_type: str = "title") -> List[Dict]:
        books = self.file_manager.read_data(self.file_manager.books_file)
        results = []
        
        query_lower = query.lower()
        
        for book in books:
            if search_type == "title":
                if query_lower in book.get('title', '').lower():
                    results.append(book)
            elif search_type == "author":
                if query_lower in book.get('author', '').lower():
                    results.append(book)
            elif search_type == "isbn":
                if query == book.get('isbn', ''):
                    results.append(book)
            else:  # Search both title and author
                if (query_lower in book.get('title', '').lower() or 
                    query_lower in book.get('author', '').lower()):
                    results.append(book)
        
        return results
    
    # Borrowing a book
    def borrow_book(self, user_id: str, isbn: str) -> bool:
        try:
            books = self.file_manager.read_data(self.file_manager.books_file)
            users = self.file_manager.read_data(self.file_manager.users_file)
            transactions = self.file_manager.read_data(self.file_manager.transactions_file)
            
            # Find the book and check availability using ISBN, since ISBN is unique for every book
            book_found = False
            for i, book in enumerate(books):
                if book['isbn'] == isbn: 
                    if book['available_copies'] <= 0:
                        print("Book is not available for borrowing!")
                        return False
                    book_found = True
                    books[i]['available_copies'] -= 1
                    break
            
            if not book_found:
                print("Book not found!")
                return False
            
            # Check if user exists and get user type
            user_type = None
            for user in users:
                if user['user_id'] == user_id:
                    user_type = user['user_type']
                    break
            
            if not user_type:
                print("User not found!")
                return False
            
            # Determine loan period and due date based on user type
            loan_days = self.loan_periods.get(user_type, 14)
            transaction_date = datetime.datetime.now()
            due_date = transaction_date + datetime.timedelta(days=loan_days)
            
            # Create transaction record for borrowing the book using unique transaction ID 
            transaction = {
                'transaction_id': self.next_transaction_id,
                'user_id': user_id,
                'isbn': isbn,
                'transaction_type': 'borrow',
                'transaction_date': transaction_date.isoformat(),
                'due_date': due_date.isoformat(),
                'return_date': None,
                'fine_amount': 0,
                'status': 'active'
            }
            
            # Add the transaction and increment transaction ID
            transactions.append(transaction)
            self.next_transaction_id += 1
            
            # Save the updated data
            self.file_manager.write_data(self.file_manager.books_file, books)
            self.file_manager.write_data(self.file_manager.transactions_file, transactions)
            
            print(f"Book borrowed successfully! \nDue date: {due_date.strftime('%Y-%m-%d')}")
            return True
        
        except Exception as e: # Catch any exception that occurs during the borrowing process
            print(f"Error borrowing book: {e}")
            return False
    
    # Returning a book and calculating fines if overdue (if any)
    def return_book(self, user_id: str, isbn: str) -> bool:
        try:
            books = self.file_manager.read_data(self.file_manager.books_file)
            transactions = self.file_manager.read_data(self.file_manager.transactions_file)
            
            # Find active transaction
            transaction_found = False
            for i, transaction in enumerate(transactions):
                if (transaction['user_id'] == user_id and 
                    transaction['isbn'] == isbn and 
                    transaction['status'] == 'active'):
                    
                    due_date = datetime.datetime.fromisoformat(transaction['due_date'])
                    return_date = datetime.datetime.now()
                    
                    # Calculate fine if book is returned late (based on due date)
                    fine_amount = 0
                    if return_date > due_date:
                        days_overdue = (return_date - due_date).days
                        fine_amount = days_overdue * self.fine_per_day
                    
                    # Update transaction record to mark the book as returned and set return date and fine amount 
                    transactions[i]['return_date'] = return_date.isoformat()
                    transactions[i]['fine_amount'] = fine_amount
                    transactions[i]['status'] = 'returned'
                    
                    transaction_found = True
                    break
            
            if not transaction_found: # If no active borrowing record is found for the user and book 
                print("No active borrowing record found!")
                return False
            
            # Update book availability using ISBN 
            for i, book in enumerate(books):
                if book['isbn'] == isbn:
                    books[i]['available_copies'] += 1
                    break
            
            # Save the updated data
            self.file_manager.write_data(self.file_manager.books_file, books)
            self.file_manager.write_data(self.file_manager.transactions_file, transactions)
            
            # Inform user about any fines incurred
            if fine_amount > 0:
                print(f"Book returned with fine: ₦{fine_amount:.2f}")
            else:
                print("Book returned successfully!")
            
            return True
            
        except Exception as e: # Catch any exception that occurs during the return process
            print(f"Error returning book: {e}")
            return False
    
    # Get the user transaction history (using user ID)
    def get_user_transactions(self, user_id: str) -> List[Dict]:
        transactions = self.file_manager.read_data(self.file_manager.transactions_file)
        books = self.file_manager.read_data(self.file_manager.books_file)
        
        # Create a book lookup dictionary
        book_lookup = {book['isbn']: book for book in books}
        
        # Filter transactions for the specific user and enrich with book details
        user_transactions = []
        for transaction in transactions:
            if transaction['user_id'] == user_id:
                book_info = book_lookup.get(transaction['isbn'], {})
                transaction_copy = transaction.copy()
                transaction_copy['book_title'] = book_info.get('title', 'Unknown')
                transaction_copy['book_author'] = book_info.get('author', 'Unknown')
                user_transactions.append(transaction_copy)
        
        # Sort by transaction date (newest first)
        user_transactions.sort(key=lambda x: x['transaction_date'], reverse=True)
        return user_transactions
    
    # Get the list of overdue books with user and book details (using current date) 
    def get_overdue_books(self) -> List[Dict]:
        transactions = self.file_manager.read_data(self.file_manager.transactions_file)
        users = self.file_manager.read_data(self.file_manager.users_file)
        books = self.file_manager.read_data(self.file_manager.books_file)
        
        # Create lookup dictionaries
        user_lookup = {user['user_id']: user for user in users}
        book_lookup = {book['isbn']: book for book in books}
        
        # Get current date
        current_date = datetime.datetime.now().isoformat()
        
        # Initialize overdue books list
        overdue_books = []
        
        # Filter transactions for overdue books and enrich with user and book details
        for transaction in transactions:
            if (transaction['status'] == 'active' and 
                transaction['due_date'] < current_date):
                
                user_info = user_lookup.get(transaction['user_id'], {})
                book_info = book_lookup.get(transaction['isbn'], {})
                
                # Add enriched overdue book info to the list
                overdue_books.append({
                    'transaction_id': transaction['transaction_id'],
                    'user_id': transaction['user_id'],
                    'isbn': transaction['isbn'],
                    'due_date': transaction['due_date'],
                    'user_name': user_info.get('name', 'Unknown'),
                    'user_email': user_info.get('email', 'Unknown'),
                    'book_title': book_info.get('title', 'Unknown'),
                    'book_author': book_info.get('author', 'Unknown')
                })
        
        # Sort by due date (oldest first) to prioritize the most overdue books 
        overdue_books.sort(key=lambda x: x['due_date'])
        return overdue_books
    
    # Library reports
    def generate_reports(self) -> Dict:
        books = self.file_manager.read_data(self.file_manager.books_file)
        users = self.file_manager.read_data(self.file_manager.users_file)
        transactions = self.file_manager.read_data(self.file_manager.transactions_file)
        
        # Initialize reports dictionary
        reports = {}
        
        # Total books
        reports['total_titles'] = len(books)
        reports['total_copies'] = sum(book.get('total_copies', 0) for book in books)
        
        # Total users
        reports['total_users'] = len(users)
        
        # Active borrowings
        reports['active_borrowings'] = len([t for t in transactions if t.get('status') == 'active'])
        
        # Overdue books
        current_date = datetime.datetime.now().isoformat()
        reports['overdue_books'] = len([
            t for t in transactions 
            if t.get('status') == 'active' and t.get('due_date', '') < current_date
        ])
        
        # Total fines collected
        reports['total_fines'] = sum(
            t.get('fine_amount', 0) for t in transactions 
            if t.get('fine_amount', 0) > 0
        )
        
        return reports