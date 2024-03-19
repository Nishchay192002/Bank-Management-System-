import mysql.connector
import tkinter as tk
from tkinter import messagebox


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sono2011",
    database="bankdb"
)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INTEGER PRIMARY KEY,
        balance INTEGER
    )
''')
conn.commit()

class BankManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")

        self.acc_label = tk.Label(root, text="Account Number:")
        self.acc_label.grid(row=0, column=0, padx=10, pady=10)
        self.acc_entry = tk.Entry(root)
        self.acc_entry.grid(row=0, column=1, padx=10, pady=10)

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.create_account_button = tk.Button(root, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.deposit_button = tk.Button(root, text="Deposit", command=self.deposit)
        self.deposit_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.withdraw_button = tk.Button(root, text="Withdraw", command=self.withdraw)
        self.withdraw_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.balance_button = tk.Button(root, text="Check Balance", command=self.check_balance)
        self.balance_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.display_all_button = tk.Button(root, text="Display All Accounts", command=self.display_all)
        self.display_all_button.grid(row=6, column=0, columnspan=2, pady=10)

    def create_account(self):
        acc_no = self.acc_entry.get()
        if acc_no.isdigit():
            cursor.execute("INSERT INTO accounts (account_number, balance) VALUES (%s, %s)", (int(acc_no), 0))
            conn.commit()
            messagebox.showinfo("Success", f"Account {acc_no} created successfully!")
        else:
            messagebox.showerror("Error", "Invalid account number!")

    def deposit(self):
        acc_no = self.acc_entry.get()
        amount = self.amount_entry.get()
        if acc_no.isdigit() and amount.isdigit():
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (int(amount), int(acc_no)))
            conn.commit()
            messagebox.showinfo("Success", f"Deposited {amount} into account {acc_no}!")
        else:
            messagebox.showerror("Error", "Invalid account number or amount!")

    def withdraw(self):
        acc_no = self.acc_entry.get()
        amount = self.amount_entry.get()
        if acc_no.isdigit() and amount.isdigit():
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (int(amount), int(acc_no)))
            conn.commit()
            messagebox.showinfo("Success", f"Withdrew {amount} from account {acc_no}!")
        else:
            messagebox.showerror("Error", "Invalid account number or amount!")

    def check_balance(self):
        acc_no = self.acc_entry.get()
        if acc_no.isdigit():
            cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (int(acc_no),))
            result = cursor.fetchone()
            if result:
                balance = result[0]
                messagebox.showinfo("Balance", f"The balance of account {acc_no} is ${balance}")
            else:
                messagebox.showerror("Error", f"Account {acc_no} not found!")
        else:
            messagebox.showerror("Error", "Invalid account number!")

    def display_all(self):
        cursor.execute("SELECT * FROM accounts")
        all_accounts = cursor.fetchall()
        if all_accounts:
            accounts_info = "\n".join([f"Account {acc_no}: ${balance}" for acc_no, balance in all_accounts])
            messagebox.showinfo("All Accounts", accounts_info)
        else:
            messagebox.showinfo("All Accounts", "No accounts found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankManagementSystem(root)
    root.mainloop()


conn.close()
