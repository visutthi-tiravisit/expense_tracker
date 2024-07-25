import sqlite3

class Category:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self): # Create Categories table
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT NOT NULL,
                    is_deleted INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating the Categories table: {e}")
        finally:
            conn.close()

    def add_category(self, category_name): # Add row of category
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Categories (category_name) VALUES (?)
            ''', (category_name,))
            conn.commit()
            return (cursor.lastrowid, category_name)
        except sqlite3.IntegrityError:
            print(f"The category '{category_name}' already exists.")
        except sqlite3.Error as e:
            print(f"An error occurred while adding the category '{category_name}': {e}")
        finally:
            conn.close()
        
    def get_all_categories(self): # Get all row of category
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Categories WHERE is_deleted = 0
            ''')
            categories = cursor.fetchall()
            if categories:
                return categories
            else:
                print("There's no category in the table")
                return None
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving categories: {e}")
            return None
        finally:
            conn.close()
          
    def get_category(self, category_id): # Get category by ID
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM Categories WHERE is_deleted = 0 AND category_id = (?)
            ''',(category_id,))
            category = cursor.fetchone()  # Use fetchone() for a single result
            return category  # Returns None if no result is found
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving category: {e}")
            return None
        finally:
            conn.close()
    
    def soft_delete_category(self, category_id): # Soft delete category by ID
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Categories SET is_deleted = 1 WHERE category_id = ?
            ''', (category_id,))
            conn.commit()
            return category_id
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the category with ID {category_id}: {e}")
        finally:
            conn.close()