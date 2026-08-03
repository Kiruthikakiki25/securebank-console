from src.bank import Bank
from src.exceptions import AccountNotFoundError, InsufficientFundsError, AccountClosedError

def run():
    bank = Bank()
    while True:
        print("\n1.Create  2.Deposit  3.Withdraw  4.Transfer  5.Reverse  6.Find by Name  0.Exit")
        choice = input("> ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            acc = bank.create_account(name)
            print(f"Created: {acc.account_id} | {acc.owner_name} | {acc.balance}")

        elif choice == "2":
            aid = input("ID: ").strip()
            amt = float(input("Amount: "))
            try:
                acc = bank.deposit(aid, amt)
                print(f"Balance: {acc.balance}")
            except (AccountNotFoundError, AccountClosedError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "3":
            aid = input("ID: ").strip()
            amt = float(input("Amount: "))
            try:
                acc = bank.withdraw(aid, amt)
                print(f"Balance: {acc.balance}")
            except (AccountNotFoundError, AccountClosedError, InsufficientFundsError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            fid = input("From ID: ").strip()
            tid = input("To ID: ").strip()
            amt = float(input("Amount: "))
            try:
                txn = bank.transfer(fid, tid, amt)
                print(f"Transfer done. TXN ID: {txn.transaction_id}")
            except (AccountNotFoundError, AccountClosedError, InsufficientFundsError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "5":
            aid = input("Account ID to reverse last transaction: ").strip()
            try:
                bank.reverse_last_transaction(aid)
                print(f"Last transaction reversed.")
            except (AccountNotFoundError, ValueError) as e:
                print(f"Error: {e}")

        elif choice == "6":
            name = input("Name to search: ").strip()
            accounts = bank.find_by_name(name)
            if not accounts:
                print("No accounts found.")
            for acc in accounts:
                print(f"{acc.account_id} | {acc.owner_name} | {acc.balance}")

        elif choice == "0":
            break