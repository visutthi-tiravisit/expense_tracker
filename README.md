# Expense Tracker

This project is an Expense Tracker application developed for the NIDA University subject CI4003. The application allows users to manage and track their expenses by creating and storing individual expense entries, categorizing them, and generating summary reports.

The project requirements include:
- **Database**: The application uses SQLite3 as the database to store and manage data.
- **User Interface**: It features a user-friendly interface created using ASCII art, making it easy for users to navigate and interact with the application.
- **Testing**: The application includes unit tests to ensure the core functionalities are working correctly.

## Table of Contents

- [Installation](#installation)
- [Version](#version)
- [Usage](#usage)
- [Testing](#testing)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/expense-tracker.git
    cd expense-tracker
    ```

2. **(Optional) Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Version

### Current Features

version 1.0 (25/07/2024)
- Create, manage expenses and categories.
- Add, retrieve, and delete (soft delete) expenses.
- Retrieve expenses by date range and category.
- Plot expenses amount by category using a pie chart.
- Unit tests for core functionalities.

### Future Features

- Hard delete expenses
- Bulk add expenses
- More detailed reports and visualizations.

## Usage
For developers to understand the flow, here are the basic steps to start the app:

1. **Create the database tables:**

    ```python
    from category import Category
    from expense import Expense

    category = Category('expense_db.db')
    expense = Expense('expense_db.db')

    category.create_table()
    expense.create_table()
    ```

2. **Add a category:**

    ```python
    category.add_category('Food')
    ```

3. **Add an expense:**

    ```python
    expense_obj = {
        "category_id": 1,  # Assuming 'Food' has category_id 1
        "amount": 50.0,
        "date": "2024-07-24",
        "description": "Grocery shopping"
    }
    expense.add_expenses(expense_obj)
    ```

4. **Retrieve all expenses:**

    ```python
    all_expenses = expense.get_all_expenses()
    print(all_expenses)
    ```

### Menu Interface

For general users, the application provides a menu interface for managing categories and expenses:

```text
Enter your name as database name: test

==========================================================
                 WELCOME TO EXPENSE TRACKER
==========================================================

Main Menu

Category Manage     Expense Manage       Option
1. Add Category     5. Add Expense       q. Exit
2. Delete Category  6. Delete Expense
3. Show Category    7. Show Expense From-To
4. Show Categories  8. Show Expenses
                    9. Show Expenses by Category
                    10. Pie chart all time expenses by Category

--> Enter your choice:
```

## Testing

1. **Run the unit tests:**

    The unit tests are written using the `unittest` framework. To run the tests, execute the following command:

    ```bash
    python -m unittest discover -s tests
    ```

    This will discover and run all test cases in the `tests` directory.

## Contact

For any inquiries or issues, please contact:

- **Name**: Visutthi
- **Email**: visutthi.tiravisit@gmail.com