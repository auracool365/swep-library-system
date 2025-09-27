import datetime
from typing import Dict

# Model represents the structure of data(User and Books) used in the library system

class User:
    # Library user type - represents students, staff, faculty, and alumni
    def __init__(self, user_id: str, name: str, email: str, user_type: str, 
                 department: str = "", phone: str = ""):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.user_type = user_type # e.g., student, faculty, staff, alumni
        self.department = department
        self.phone = phone
        self.registration_date = datetime.datetime.now().isoformat()
        self.status = "active"
    
    # User object needs to first be converted to dictionary so it can be saved to JSON file. You can call it JSON-serializable dictionary
    # I called it convert_to_map because dictionary in python is just map in some other languages. the name map is shorter to write
    def convert_to_map(self) -> Dict:
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'user_type': self.user_type,
            'department': self.department,
            'phone': self.phone,
            'registration_date': self.registration_date,
            'status': self.status
        }


class Book:
    # Book type - represents a book in the library catalog 
    def __init__(self, isbn: str, title: str, author: str, publisher: str = "",
                 publication_year: int = 0, category: str = "", 
                 total_copies: int = 1, shelf_location: str = ""):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.publication_year = publication_year
        self.category = category
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.shelf_location = shelf_location
        self.date_added = datetime.datetime.now().isoformat()
    
    # Convert book object (like user object above) to dictionary for JSON serialization and storage
    def convert_to_map(self) -> Dict:
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'publication_year': self.publication_year,
            'category': self.category,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'shelf_location': self.shelf_location,
            'date_added': self.date_added
        }