#!/usr/bin/env python
import sys
import tty
import termios
import json

class Account:
    def __init__(self, owner: str, name: str, starting_balance: float = 0.0):
        self.__owner = owner
        self.__name = name
        self.__balance = starting_balance
        self.data_dict = self.make_data_dict()

    def describe(self):
        print(f"Account: {self.__name} | Owner: {self.__owner}")

    def is_a_match(self, owner: str, name: str):
        if self.__owner == owner and self.__name == name:
            return True
        else:
            return False

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        str_amount = str(amount)
        print(f"✅ Deposited ${str_amount} into {self.__name} for {self.__owner}.")

    def withdraw(self, amount: float):
        if amount <=0:
            raise ValueError("Withdraw amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds to withdraw that amount")
        self.__balance -= amount
        str_amount = str(amount)
        print(f"✅ Withdrew ${str_amount} from {self.__name}.")
        print(f"Remaining balance is: ${self.__balance}")

    def check_balance(self):
        return f"{self.__balance}"
    
    def check_owner(self):
        return f"{self.__owner}"
    
    def make_data_dict(self):
        data_dict = {"Name": self.__name, "Owner": self.__owner, "Balance": self.__balance}
        return data_dict
        
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def read_from_json():
    try:
        with open("accounts.json", "r") as file:
            data = json.load(file)
            for item in data:
                account = Account(name=item['Name'], owner=item['Owner'], starting_balance=item['Balance'])
                account_list.append(account)
    except FileNotFoundError:
        print("Note: accounts.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format for accounts.json file.")

def write_to_json():
    with open("accounts.json", "wt") as fh:
        entries = [account.data_dict for account in account_list]
        json.dump(entries, fh, indent=4)
    fh.close()

   
#         "       (C) Check account balance\n"
# "       (D) Deposit funds\n" \
#         "       (W) Withdraw funds\n" \
#         "       (Q) Quit program\n"
#         "       (X) Quit program without saving."
account_list = []

if __name__ == "__main__":
    read_from_json()

    running = True

    while running:
        print("Press the appropriate key\n" \
        "       (A) Add new account\n" \
        "       (D) Deposit funds\n" \
        "       (L) List existing accounts\n" \
        "       (W) Withdraw\n" \
        "       (Q) Quit program and save account changes\n"
        "       (X) Exit without saving changes to accounts")
        key = getch().lower()
        if key == "a":
            # keep prompting until we get a unique (owner,name)
            while True:
                owner = input("Account owner name: ")
                name  = input("Enter a nickname for the account: ")

                # check for duplicates
                duplicate = any(
                    acc.is_a_match(owner, name)
                    for acc in account_list
                )
                if duplicate:
                    print("❗ That owner/name combo already exists. Please try again.\n")
                else:
                    break
            starting_balance = float(input("Deposit a starting balance: "))
            # at this point owner/name are unique
            new_account = Account(owner=owner, name=name, starting_balance=starting_balance)
            account_list.append(new_account)
            print(f"✅ Created account “{name}” for {owner}.\n")

        elif key == "d":
            while True:
                print("#### DEPOSITING FUNDS #####")
                owner = input("Account owner name: ")
                name  = input("Account nickname: ")
                # try to find the matching account (or get None)
                account = next(
                    (acc for acc in account_list
                    if acc.is_a_match(owner, name)),
                    None
                )
                if account is None:
                    print("❗ That owner/name combo does not exist. Please try again.\n")
                else:
                    amount = float(input("Amount to deposit: "))
                    account.deposit(amount)
                    str_amount = str(amount)
                    #print(f"✅ Deposited ${str_amount} into {account.name} for {account.owner}.")
                    break
        
        elif key == "w":
            while True:
                print("#### WITHDRAWING FUNDS #####")
                owner = input("Account owner name: ")
                name  = input("Account nickname: ")
                
                account = next(
                    (acc for acc in account_list
                    if acc.is_a_match(owner, name)),
                    None
                )
                if account is None:
                    print("❗ That owner/name combo does not exist. Please try again.\n")
                else:
                    amount = float(input("Amount to withdraw: "))
                    account.withdraw(amount)
                    str_amount = str(amount)
                    #print(f"✅ Withdrew ${str_amount} from {account.name} for {account.owner}.")
                    break
        
        elif key == "l":
            print("#### ACCOUNTS ####")
            for account in account_list:
                account.describe()

        elif key == "q":
            running = False
            write_to_json()

        elif key == "x":
            running = False

        else:
            print("Invalid character entered")