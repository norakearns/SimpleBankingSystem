#!/usr/bin/env python
import sys
import tty
import termios
import json

class Account:
    def __init__(self, owner: str, name: str, starting_balance: float = 0.0):
        self.owner = owner
        self.name = name
        self._balance = starting_balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        print(f"{self.owner} has successfully deposited ${amount}")
        print(f"✅ Deposited ${str_amount} into {account.name} for {account.owner}.")

    def withdraw(self, amount: float):
        if amount <=0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds to withdraw that amount")
        self._balance -= amount
        print(f"{self.owner} has successfully withdrawn ${amount}")

    def check_balance(self):
        return f"{self._balance}"
    
    def check_owner(self):
        return f"{self.owner}"
        
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
   
#         "       (C) Check account balance\n"
# "       (D) Deposit funds\n" \
#         "       (W) Withdraw funds\n" \
#         "       (Q) Quit program\n"
#         "       (X) Quit program without saving."
account_list = []

if __name__ == "__main__":
    running = True

    while running:
        print("Press the appropriate key\n" \
        "       (A) Add new account\n" \
        "       (D) Deposit funds\n" \
        "       (L) List existing accounts\n" \
        "       (Q) Quit program")
        key = getch().lower()
        if key == "a":
            # keep prompting until we get a unique (owner,name)
            while True:
                owner = input("Account owner name: ")
                name  = input("Enter a nickname for the account: ")
                starting_balance = float(input("Deposit a starting balance: "))

                # check for duplicates
                duplicate = any(
                    acc.owner == owner and acc.name == name
                    for acc in account_list
                )
                if duplicate:
                    print("❗ That owner/name combo already exists. Please try again.\n")
                else:
                    break

            # at this point owner/name are unique
            new_account = Account(owner=owner, name=name, starting_balance=starting_balance)
            account_list.append(new_account)
            print(f"✅ Created account “{name}” for {owner}.\n")

        if key == "d":
            while True:
                owner = input("Account owner name: ")
                name  = input("Account nickname: ")
                # try to find the matching account (or get None)
                account = next(
                    (acc for acc in account_list
                    if acc.owner == owner and acc.name == name),
                    None
                )
                if account is None:
                    print("❗ That owner/name combo does not exist. Please try again.\n")
                else:
                    amount = float(input("Amount to deposit: "))
                    account.deposit(amount)
                    str_amount = str(amount)
                    print(f"✅ Deposited ${str_amount} into {account.name} for {account.owner}.")
                    break

        if key == "l":
            for account in account_list:
                print(f"{account.owner}: {account.name}")

        elif key == "q":
            running = False

