# Expense Tracker CLI
# -----------------------------------
# Features:
# 1. Add Income/Expense
# 2. View Transactions
# 3. Monthly Summary
# 4. Export Monthly Report CSV
# 5. Generate Expense Chart
# -----------------------------------

import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import os

FILE_NAME = "expenses.csv"


# -----------------------------------
# Create CSV File if Not Exists
# -----------------------------------
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Category", "Amount"])


# -----------------------------------
# Add Income or Expense
# -----------------------------------
def add_entry():

    date = input("Enter date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format!")
        return

    entry_type = input("Enter type (Income/Expense): ").capitalize()

    if entry_type not in ["Income", "Expense"]:
        print("Invalid type!")
        return

    category = input("Enter category: ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount!")
        return

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, entry_type, category, amount])

    print("Entry Added Successfully!\n")


# -----------------------------------
# View All Transactions
# -----------------------------------
def view_transactions():

    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)

        print("\n===== ALL TRANSACTIONS =====")

        for row in reader:
            print(row)

        print()


# -----------------------------------
# Monthly Summary
# -----------------------------------
def monthly_summary():

    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    total_income = 0
    total_expense = 0

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:

            transaction_date = datetime.strptime(row["Date"], "%Y-%m-%d")

            if (
                transaction_date.month == int(month)
                and transaction_date.year == int(year)
            ):

                amount = float(row["Amount"])

                if row["Type"] == "Income":
                    total_income += amount

                elif row["Type"] == "Expense":
                    total_expense += amount

    balance = total_income - total_expense

    print("\n===== MONTHLY SUMMARY =====")
    print(f"Total Income  : ₹{total_income}")
    print(f"Total Expense : ₹{total_expense}")
    print(f"Balance       : ₹{balance}\n")


# -----------------------------------
# Export Monthly Report
# -----------------------------------
def export_report():

    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    report_file = f"report_{month}_{year}.csv"

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        with open(report_file, mode='w', newline='') as report:
            writer = csv.writer(report)

            writer.writerow(["Date", "Type", "Category", "Amount"])

            for row in reader:

                transaction_date = datetime.strptime(
                    row["Date"], "%Y-%m-%d"
                )

                if (
                    transaction_date.month == int(month)
                    and transaction_date.year == int(year)
                ):
                    writer.writerow([
                        row["Date"],
                        row["Type"],
                        row["Category"],
                        row["Amount"]
                    ])

    print(f"Report Exported Successfully as {report_file}\n")


# -----------------------------------
# Generate Expense Chart
# -----------------------------------
def generate_chart():

    category_totals = defaultdict(float)

    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:

            if row["Type"] == "Expense":
                category = row["Category"]
                amount = float(row["Amount"])

                category_totals[category] += amount

    if not category_totals:
        print("No expense data available!")
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(7, 7))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%')

    plt.title("Expense Distribution")

    chart_file = "expense_chart.png"
    plt.savefig(chart_file)

    print(f"Chart Saved as {chart_file}\n")


# -----------------------------------
# Main Menu
# -----------------------------------
def main():

    initialize_file()

    while True:

        print("===== EXPENSE TRACKER =====")
        print("1. Add Entry")
        print("2. View Transactions")
        print("3. Monthly Summary")
        print("4. Export Report")
        print("5. Generate Chart")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_entry()

        elif choice == '2':
            view_transactions()

        elif choice == '3':
            monthly_summary()

        elif choice == '4':
            export_report()

        elif choice == '5':
            generate_chart()

        elif choice == '6':
            print("Thank You!")
            break

        else:
            print("Invalid Choice!\n")


# -----------------------------------
# Run Program
# -----------------------------------
if __name__ == "__main__":
    main()