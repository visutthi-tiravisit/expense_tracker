import category as cat
import expense as exp
from datetime import datetime


user_name = str(input('Enter your name as database name: '))
db_name = f'{user_name}.db'
category = cat.Category(db_name)
expense = exp.Expense(db_name)

# Main Menu
def display_main_menu():
    print("\n"+" "*25+"Main Menu")
    print("\nCategory Manage".ljust(20) + "Expense Manage".ljust(30) + "Option".ljust(20))
    print("1. Add Category".ljust(20) + "5. Add Expense".ljust(30) + "q. Exit".ljust(20))
    print("2. Delete Category".ljust(20) + "6. Delete Expense".ljust(30))
    print("3. Show Category".ljust(20) + "7. Show Expense From-To".ljust(30))
    print("4. Show Categories".ljust(20) + "8. Show Expenses".ljust(30))
    print(" ".ljust(20)+"9. Show Expenses by Category".ljust(30))
    print(" ".ljust(20)+"10. Pie chart all time expenses by Category".ljust(30))

# Category Manage
def add_category(category_name): # 1
    category_id, name = category.add_category(category_name)
    if category_id:
        print("\n"+"|"+"-"*58+"|")
        print(" "*25+"Category Added"+"\n")
        print(f"ID: '{category_id}' Category_name: {name}")
        print("\n"+"|"+"_"*58+"|")

def delete_category(category_id): # 2
    deleted_id = category.soft_delete_category(category_id)
    if deleted_id:
        print("\n"+"|"+"-"*58+"|")
        print(" "*25+"Category Deleted"+"\n")
        print(f"Category ID {deleted_id} has been soft deleted")
        print("\n"+"|"+"_"*58+"|")

def show_category(category_id): # 3
    print("\n"+"|"+"-"*58+"|")
    category_data= category.get_category(category_id)
    if not category_data:
        print("No categories found.")
    else:
        print(" "*25+"Category"+"\n")
        print(f"ID: {category_data[0]}, Name: {category_data[1]}")
    print("\n"+"|"+"_"*58+"|")

def show_all_categories(): # 4
    print("\n"+"|"+"-"*58+"|")
    categories = category.get_all_categories()
    if not categories:
        print("No categories found.")
    else:
        print(" "*25+"All Category"+"\n")
        for cat in categories:
            print(f"ID: {cat[0]}, Name: {cat[1]}")
    print("\n"+"|"+"_"*58+"|")

# Expense Manage
def add_expense(cat_id,amount,date,description): # 5
    expense_data = {"category_id":cat_id, "amount":amount, "date":date, "description":description}
    expense_id, amount = expense.add_expenses(expense_data)
    if expense_id:
        print("\n"+"|"+"-"*58+"|")
        print(" "*25+"Expense Added"+"\n")
        print(f"ID: '{expense_id}' Amount: {amount}")
        print("\n"+"|"+"_"*58+"|")

def delete_expense(expense_id): # 6
    deleted_id = expense.soft_delete_expense(expense_id)
    if deleted_id:
        print("\n"+"|"+"-"*58+"|")
        print(" "*25+"Category Deleted"+"\n")
        print(f"Expense ID {deleted_id} has been soft deleted")
        print("\n"+"|"+"_"*58+"|")

def show_expense_from_to(from_date, to_date): # 7
    print("\n"+"|"+"-"*58+"|")
    date = {"From":from_date,"To":to_date}
    data = expense.get_expenses_by_date(date)
    if not data:
        print("No expenses found.")
    else:
        print(" "*5+f"Expense From: {from_date} To: {to_date}"+"\n")
        for exp in data:
            print(f"ID: {exp[0]}, Date: {exp[1]}, Category: {exp[2]}, Description: {exp[3]}, Amount: {exp[4]}")
    print("\n"+"|"+"_"*58+"|")

def show_all_expense(): # 8
    print("\n"+"|"+"-"*58+"|")
    all_expense = expense.get_all_expenses()
    if not all_expense:
        print("No expenses found.")
    else:
        print(" "*25+"All Expense"+"\n")
        for exp in all_expense:
            print(f"ID: {exp[0]}, Date: {exp[1]}, CategoryID: {exp[2]}, CategoryName: {exp[3]}, Description: {exp[4]}, Amount: {exp[5]}")
    print("\n"+"|"+"_"*58+"|")

def show_expense_by_category(category_id): # 9
    print("\n"+"|"+"-"*58+"|")
    print(" "*5+f"Expense from Category: {category_id}"+"\n")
    data = expense.get_expenses_by_category(category_id)
    if not data:
        print("No expenses found.")
    else:
        for exp in data:
            print(f"ID: {exp[0]}, Date: {exp[1]}, CategoryID: {exp[2]}, CategoryName: {exp[3]}, Description: {exp[4]}, Amount: {exp[5]}")
    print("\n"+"|"+"_"*58+"|")

def show_piechart_exp_by_cat(): #10
    print("\n"+"|"+"-"*58+"|")
    expense.plot_expenses_amount_by_category()
    print("\n"+"|"+"_"*58+"|")

# ============================ Controller ============================ #

def main():
    category.create_table()
    expense.create_table()
    print("\n" + "="*60)
    print(" "*20+"WELCOME TO EXPENSE TRACKER")
    print("="*60)
    while True:
        display_main_menu()
        choice = input("\n --> Enter your choice: ").lower()
        match choice:
            case '1': #add_category
                cat_name = input("Enter category name: ")
                add_category(cat_name)
            case '2': #delete_category
                try:
                    cat_id = int(input("Enter category ID to delete: "))
                    delete_category(cat_id)
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
            case '3': #show_category
                try:
                    category_id = int(input('Enter Category ID: '))
                    show_category(category_id)
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
            case '4': #show_all_categories
                show_all_categories()
            case '5': #add_expense
                try:
                    show_all_categories()
                    cat_id = input("Enter category ID for the expense: ")
                    amount = float(input("Enter expense amount: "))
                    date = input("Enter expense date (yyyy-mm-dd): ")
                    datetime.strptime(date, "%Y-%m-%d")
                    description = input("Enter expense description: ")
                    add_expense(cat_id,amount,date,description)
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
            case '6': #delete_expense
                try:
                    expense_id = int(input('\nEnter expense ID to delete: '))
                    delete_expense(expense_id)
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
            case '7': #show_expense_from_to
                try:
                    from_date = input("Enter start date (yyyy-mm-dd): ")
                    to_date = input("Enter end date (yyyy-mm-dd): ")
                    datetime.strptime(from_date, "%Y-%m-%d")
                    datetime.strptime(to_date, "%Y-%m-%d")
                    show_expense_from_to(from_date, to_date)
                except ValueError as ve:
                    print(f"Invalid date format: {ve}")
            case '8': #show_all_expense
                show_all_expense()
            case '9': #show_expense_by_category
                try:
                    show_all_categories()
                    category_id = input("Enter Category ID: ")
                    show_expense_by_category(category_id)
                except ValueError as ve:
                    print(f"Invalid input: {ve}")
            case '10': #how_piechart_exp_by_cat
                show_piechart_exp_by_cat()
            case 'q':
                print("Exiting the application.")
                break
            case _:
                print("Invalid choice. Please try again.")
                print("-"*60)

if __name__ == '__main__':
    main()