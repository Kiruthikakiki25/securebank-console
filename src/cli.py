from src.bank import Bank
from src.exceptions import (
    AccountNotFoundError,
    InsufficientFundsError,
    AccountClosedError,
)

def run():
    bank = Bank()

    menu = """
=== SecureBank ===
1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. Close Account
6. List Accounts
0. Exit
> """

    while True:
        choice = input(menu).strip()

        if choice == "1":
            name = input("Owner name: ").strip()
            amt = float(input("Initial deposit (0 for none): "))
            acc = bank.create_account(name, amt)
            print(f"Created: {acc.account_id} | {acc.owner_name} | ₹{acc.balance:.2f}")

        elif choice == "2":
            aid = input("Account ID: ").strip()
            amt = float(input("Amount: "))
            try:
                acc = bank.deposit(aid, amt)
                print(f"Deposited. New balance: ₹{acc.balance:.2f}")
            except (AccountNotFoundError, AccountClosedError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "3":
            aid = input("Account ID: ").strip()
            amt = float(input("Amount: "))
            try:
                acc = bank.withdraw(aid, amt)
                print(f"Withdrawn. New balance: ₹{acc.balance:.2f}")
            except (AccountNotFoundError, AccountClosedError,
                    InsufficientFundsError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            aid = input("Account ID: ").strip()
            try:
                bal = bank.get_balance(aid)
                print(f"Balance: ₹{bal:.2f}")
            except (AccountNotFoundError, AccountClosedError) as e:
                print(f"Error: {e}")

        elif choice == "5":
            aid = input("Account ID: ").strip()
            try:
                acc = bank.close_account(aid)
                print(f"Account {acc.account_id} closed.")
            except (AccountNotFoundError, AccountClosedError) as e:
                print(f"Error: {e}")

        elif choice == "6":
            accounts = bank.list_accounts()
            if not accounts:
                print("No accounts.")
            for acc in accounts:
                status = "ACTIVE" if acc.is_active else "CLOSED"
                print(f"{acc.account_id} | {acc.owner_name} | ₹{acc.balance:.2f} | {status}")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")