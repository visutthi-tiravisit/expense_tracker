import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class Expense:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self): # Create Expense table
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Expenses (
                    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    amount REAL NOT NULL,
                    date TEXT NOT NULL,
                    description TEXT,
                    is_deleted INTEGER DEFAULT 0,
                    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating the Expenses table: {e}")
        finally:
            conn.close()

    def add_expenses(self, expense_obj): # Add row of expense
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Expenses (category_id, amount, date, description)
                VALUES (?, ?, ?, ?)
            ''', (expense_obj["category_id"], expense_obj["amount"], expense_obj["date"], expense_obj["description"]))
            conn.commit()
            return (cursor.lastrowid, expense_obj["amount"])
        except sqlite3.Error as e:
            print(f"An error occurred while adding the expense: {e}")
        finally:
            conn.close()

    def get_all_expenses(self): # Get all row of expense
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT E.expense_id, E.date, C.category_id, C.category_name, E.description, E.amount
                FROM Expenses E 
                JOIN Categories C ON C.category_id = E.category_id 
                WHERE E.is_deleted = 0 
                ORDER BY E.date
            ''')
            all_expenses = cursor.fetchall()
            return all_expenses
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving expenses: {e}")
            all_expenses = []
        finally:
            conn.close()
    
    def get_expense(self,expense_id): # Get expense by ID
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Expenses WHERE expense_id = ? AND is_deleted = 0', (expense_id,))
            expense = cursor.fetchone()
            return expense
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving the expense with ID {expense_id}: {e}")
            expense = None
        finally:
            conn.close()
    
    def get_expenses_by_date(self, from_to): # Get expenses by From date - To date
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT E.expense_id, E.date, C.category_name, E.description, E.amount
                FROM Expenses E 
                JOIN Categories C ON C.category_id = E.category_id 
                WHERE E.date BETWEEN ? AND ? AND E.is_deleted = 0 
                ORDER BY E.date
            ''', (from_to["From"], from_to["To"]))
            expenses = cursor.fetchall()
            return expenses
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving expenses between {from_to["From"]} and {from_to["To"]}: {e}")
        finally:
            conn.close()

    def get_expenses_by_category(self, category_id): # Get expenses by category ID
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT E.expense_id, E.date, C.category_id, C.category_name, E.description, E.amount
                FROM Expenses E 
                JOIN Categories C ON C.category_id = E.category_id 
                WHERE C.category_id = ? AND E.is_deleted = 0 
                ORDER BY E.date
            ''', (category_id,))
            expenses = cursor.fetchall()
            return expenses
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving expenses for category_id {category_id} : {e}")
        finally:
            conn.close()

    def soft_delete_expense(self, expense_id): # Soft delete expense by ID
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('UPDATE Expenses SET is_deleted = 1 WHERE expense_id = ?', (expense_id,))
            conn.commit()
            return expense_id
        except sqlite3.Error as e:
            print(f"An error occurred while deleting the expense with ID {expense_id}: {e}")
        finally:
            conn.close()

    def plot_expenses_amount_by_category(self): # Display piechart of all time expense by category
        try:
            conn = sqlite3.connect(self.db_name)
            query = '''
                SELECT C.category_name, SUM(E.amount) as total_amount
                FROM Expenses E
                JOIN Categories C ON C.category_id = E.category_id
                WHERE E.is_deleted = 0
                GROUP BY C.category_name
            '''
            df = pd.read_sql_query(query, conn)
            conn.close()

            # Plotting the pie chart using pandas
            df.set_index('category_name', inplace=True)
            def func(pct, allvals):
                absolute = int(pct/100.*np.sum(allvals))
                return "{:.1f}%\n({:d}฿)".format(pct, absolute)

            df.plot.pie(y='total_amount', autopct=lambda pct: func(pct, df['total_amount']),
                        figsize=(10, 6), legend=False)
            plt.title('All time Expenses sum amount by Category')
            plt.ylabel('')  # Hide the y-label
            print("Pie chart is will display on new tab. Close to continue ...")
            plt.show()

        except sqlite3.Error as e:
            print(f"An error occurred while plotting expenses by category: {e}")
