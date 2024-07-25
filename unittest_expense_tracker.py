import unittest
import sqlite3
import os
from category import Category
from expense import Expense

class TestCategory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_name = 'test_expense_db.db'
        cls.category = Category(cls.test_db_name)
        print(f"Creating database: {cls.test_db_name}", end=' ')
        cls.category.create_table() # Category.create_table

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_name):
            os.remove(cls.test_db_name)
            print(f"Deleted database: {cls.test_db_name}", end=' ')

    def setUp(self):
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Categories')
        conn.commit()
        conn.close()

    def test_add_category(self): # Category.add_category
        category_id, category_name = self.category.add_category('Test Category')
        self.assertEqual(category_name, 'Test Category')
        self.assertIsInstance(category_id, int)

    def test_get_all_categories(self): # Category.get_all_categories
        self.category.add_category('Test Category 1')
        self.category.add_category('Test Category 2')
        categories = self.category.get_all_categories()
        self.assertIsNotNone(categories)
        self.assertEqual(len(categories), 2)
        category_names = [row[1] for row in categories]
        self.assertIn('Test Category 1', category_names)
        self.assertIn('Test Category 2', category_names)

    def test_get_category(self): # Category.get_category
        category_id, _ = self.category.add_category('Test Category')
        retrieved_category = self.category.get_category(category_id)
        self.assertIsNotNone(retrieved_category)
        self.assertEqual(retrieved_category[0], category_id)
        self.assertEqual(retrieved_category[1], 'Test Category')
        self.assertEqual(retrieved_category[2], 0)

    def test_soft_delete_category(self): # soft_delete_category
        category_id, _ = self.category.add_category('Test Category')
        deleted_id = self.category.soft_delete_category(category_id)
        self.assertEqual(deleted_id, category_id)
        retrieved_category = self.category.get_category(category_id)
        self.assertIsNone(retrieved_category, "Category should not be retrievable after soft deletion")


class TestExpense(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_db_name = 'test_expense_db.db'
        cls.category = Category(cls.test_db_name)
        cls.expense = Expense(cls.test_db_name)
        print(f"Creating database: {cls.test_db_name}", end=' ')
        cls.category.create_table() # Category.create_table
        cls.expense.create_table() # Expense.create_table
    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_name):
            os.remove(cls.test_db_name)
            print(f"Deleted database: {cls.test_db_name}", end=' ')

    def setUp(self):
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Categories')
        cursor.execute('DELETE FROM Expenses')
        conn.commit()
        conn.close()

    def test_get_all_expenses(self): # Expense.get_all_expenses
        # Add a category
        category_id, _ = self.category.add_category('Test Category')

        # Add some expenses
        expense_obj1 = {
            "category_id": category_id,
            "amount": 50.0,
            "date": "2024-07-24",
            "description": "Expense 1"
        }
        expense_obj2 = {
            "category_id": category_id,
            "amount": 150.0,
            "date": "2024-07-25",
            "description": "Expense 2"
        }
        self.expense.add_expenses(expense_obj1)
        self.expense.add_expenses(expense_obj2)

        # Retrieve all expenses
        expenses = self.expense.get_all_expenses()
        
        # Check if expenses are retrieved
        self.assertIsNotNone(expenses, "Expenses should be retrievable from the database")
        
        # Check the number of expenses
        self.assertEqual(len(expenses), 2)

        # Verify the first expense
        expense_data1 = expenses[0]
        self.assertEqual(expense_data1[1], "2024-07-24")  # Check date for expense 1
        self.assertEqual(expense_data1[2], category_id)    # Check category_id for expense 1
        self.assertEqual(expense_data1[3], 'Test Category') # Check category_name for expense 1
        self.assertEqual(expense_data1[4], "Expense 1")     # Check description for expense 1
        self.assertEqual(expense_data1[5], 50.0)            # Check amount for expense 1

        # Verify the second expense
        expense_data2 = expenses[1]
        self.assertEqual(expense_data2[1], "2024-07-25")  # Check date for expense 2
        self.assertEqual(expense_data2[2], category_id)    # Check category_id for expense 2
        self.assertEqual(expense_data2[3], 'Test Category') # Check category_name for expense 2
        self.assertEqual(expense_data2[4], "Expense 2")     # Check description for expense 2
        self.assertEqual(expense_data2[5], 150.0)           # Check amount for expense 2

    def test_add_expenses(self): # Expense.add_expenses
        category_id, _ = self.category.add_category('Test Category')
        expense_obj = {
            "category_id": category_id,
            "amount": 100.0,
            "date": "2024-07-24",
            "description": "Test Expense"
        }
        expense_id, amount = self.expense.add_expenses(expense_obj)
        self.assertIsInstance(expense_id, int)
        self.assertEqual(amount, 100.0)

        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Expenses WHERE expense_id = ?
        ''', (expense_id,))
        expense_data = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(expense_data)
        self.assertEqual(expense_data[1], category_id)
        self.assertEqual(expense_data[2], 100.0)
        self.assertEqual(expense_data[3], "2024-07-24")
        self.assertEqual(expense_data[4], "Test Expense")
    
    def test_get_expense(self): # Expense.get_expense
        # Add a category
        category_id, _ = self.category.add_category('Test Category')
        
        # Add an expense
        expense_obj = {
            "category_id": category_id,
            "amount": 100.0,
            "date": "2024-07-24",
            "description": "Test Expense"
        }
        expense_id, _ = self.expense.add_expenses(expense_obj)
        
        # Retrieve the expense by ID
        retrieved_expense = self.expense.get_expense(expense_id)
        # Check if the retrieved expense is not None
        self.assertIsNotNone(retrieved_expense, "Expense should be retrievable by its ID")
        
        # Verify the expense data
        self.assertEqual(retrieved_expense[0], expense_id)          # Check expense_id
        self.assertEqual(retrieved_expense[1], category_id)         # Check category_id
        self.assertEqual(retrieved_expense[2], expense_obj["amount"]) # Check amount
        self.assertEqual(retrieved_expense[3], expense_obj["date"]) # Check date
        self.assertEqual(retrieved_expense[4], expense_obj["description"]) # Check description
        self.assertEqual(retrieved_expense[5], 0) # Check if_deleted (should be 0)

    def test_get_expenses_by_date(self): # Expense.get_expenses_by_date
        # Add a category
        category_id, _ = self.category.add_category('Test Category')
        
        # Add some expenses
        expense_entry1 = {
            "category_id": category_id,
            "amount": 100.0,
            "date": "2024-07-10",
            "description": "Expense 1"
        }
        expense_entry2 = {
            "category_id": category_id,
            "amount": 200.0,
            "date": "2024-07-20",
            "description": "Expense 2"
        }
        self.expense.add_expenses(expense_entry1)
        self.expense.add_expenses(expense_entry2)
        
        # Define the date range
        date_range = {"From": "2024-07-01", "To": "2024-07-31"}
        
        # Retrieve expenses within the date range
        expenses = self.expense.get_expenses_by_date(date_range)
        
        # Expected results: Adjusted order based on the result from get_expenses_by_date
        expected_results = [
            (expense_entry1["date"], 'Test Category', expense_entry1["description"], expense_entry1["amount"]),
            (expense_entry2["date"], 'Test Category', expense_entry2["description"], expense_entry2["amount"])
        ]
        
        # Check if retrieved expenses match expected results
        self.assertEqual(len(expenses), 2, "There should be 2 expenses in the result")
        
        # Convert results to a set for comparison
        results_set = set((exp[1], exp[2], exp[3], exp[4]) for exp in expenses)
        expected_results_set = set(expected_results)
        
        self.assertEqual(results_set, expected_results_set, "The retrieved expenses do not match the expected results")

    def test_get_expenses_by_category(self): # Expense.get_expenses_by_category
        # Add a category
        category_id, _ = self.category.add_category('Test Category')
        
        # Add expenses associated with the category
        expense_entry1 = {
            "category_id": category_id,
            "amount": 50.0,
            "date": "2024-07-10",
            "description": "Expense 1"
        }
        expense_entry2 = {
            "category_id": category_id,
            "amount": 75.0,
            "date": "2024-07-15",
            "description": "Expense 2"
        }
        expense_entry3 = {
            "category_id": category_id,
            "amount": 100.0,
            "date": "2024-07-20",
            "description": "Expense 3"
        }
        self.expense.add_expenses(expense_entry1)
        self.expense.add_expenses(expense_entry2)
        self.expense.add_expenses(expense_entry3)
        
        # Add another category with an expense
        other_category_id, _ = self.category.add_category('Other Category')
        other_expense = {
            "category_id": other_category_id,
            "amount": 200.0,
            "date": "2024-07-25",
            "description": "Other Expense"
        }
        self.expense.add_expenses(other_expense)
        
        # Retrieve expenses by category ID
        expenses = self.expense.get_expenses_by_category(category_id)
        
        # Expected results
        expected_results = [
            (expense_entry1["date"], category_id, 'Test Category', expense_entry1["description"], expense_entry1["amount"]),
            (expense_entry2["date"], category_id, 'Test Category', expense_entry2["description"], expense_entry2["amount"]),
            (expense_entry3["date"], category_id, 'Test Category', expense_entry3["description"], expense_entry3["amount"])
        ]
        
        # Check if retrieved expenses match expected results
        self.assertEqual(len(expenses), 3, "There should be 3 expenses for the specified category")
        
        # Convert results to a set for comparison
        results_set = set((exp[1], exp[2], exp[3], exp[4], exp[5]) for exp in expenses)
        expected_results_set = set(expected_results)
        
        self.assertEqual(results_set, expected_results_set, "The retrieved expenses do not match the expected results")

    def test_soft_delete_expense(self): # Expense.soft_delete_expense
        # Add a category
        category_id, _ = self.category.add_category('Test Category')
        
        # Add an expense
        expense_obj = {
            "category_id": category_id,
            "amount": 100.0,
            "date": "2024-07-24",
            "description": "Test Expense"
        }
        expense_id, _ = self.expense.add_expenses(expense_obj)
        
        # Soft delete the expense
        self.expense.soft_delete_expense(expense_id)
        
        # Check if the expense is marked as deleted
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT is_deleted FROM Expenses WHERE expense_id = ?
        ''', (expense_id,))
        is_deleted = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(is_deleted, "Expense data should be retrievable after soft delete")
        self.assertEqual(is_deleted[0], 1, "Expense should be marked as deleted (is_deleted = 1)")

if __name__ == '__main__':
    unittest.main(verbosity=2)
