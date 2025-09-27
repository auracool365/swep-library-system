import json
import os
from typing import List, Dict

# Handler for file operations in the library system for storing users, books, transactions, and reservations(Basic CRUD operations)

# Library operations type
class LibraryFileManager:
    
    # Initialize file directory in the constructor
    def __init__(self, data_dir: str = "library_data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.books_file = os.path.join(data_dir, "books.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        self.reservations_file = os.path.join(data_dir, "reservations.json")
        self.init_files()
    
    # Initialize data directory and files
    def init_files(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Initialize empty files if they don't exist
        files_to_init = [
            self.users_file, self.books_file, 
            self.transactions_file, self.reservations_file
        ]
        
        # Create empty JSON arrays in files if they don't exist
        for file_path in files_to_init:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
                    
    # Write data to JSON file
    def write_data(self, file_path: str, data: List[Dict]):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    # Read data from JSON file
    def read_data(self, file_path: str) -> List[Dict]:
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []