
class Account:
    accounts = []

    def __init__(self, name, email, address, accountType):
        self.name = name
        self.email = email
        self.address = address
        self.accountNo = name + address
        self.accountType = accountType

        self.__balance = 0
        self.__transactions = []
        self.loan_cnt = 0
        self.loan_time = 2
        Account.accounts.append(self)

    def deposit(self, amount):
        if amount >= 0:
            self.__balance += amount
            self.__transactions.append({'type': 'Deposit', 'amount': amount})
            print(f"\nDeposited {amount}. New balance: ${self.__balance}")
        else:
            print("\nInvalid deposit amount")

    def withdraw(self, amount):
        if self.__balance <= 0:
            print("\n---the bank is bankrupt.----")
        else:
            if amount > 0 and amount <= self.__balance:
                self.__balance -= amount
                self.__transactions.append({'type': 'Withdrawal', 'amount': amount})
                print(f"\nWithdrew ${amount}. New balance: ${self.__balance}")
            else:
                print("\n----Withdrawal amount exceeded---")

    def check_balance(self):
        print(f'Your current balance is: ${self.__balance}')

    def transaction_history(self):
        for transaction in self.__transactions:
            print(f"{transaction['type']}: ${transaction['amount']}")

    def loan_taken(self, amount):
        if self.loan_cnt < self.loan_time:
            self.__balance += amount
            self.loan_cnt += 1
            self.__transactions.append({'type': 'Loan', 'amount': amount})
            print(f"\nLoan of ${amount} taken. New balance: ${self.__balance}")
        else:
            print("\nOOOPs!!!! Can't take a loan.")


    def transfer_amount(self, another_account, amount):
        if another_account in Account.accounts:
            if amount >= 0 and amount <= self.__balance:
                self.__balance -= amount
                another_account.__balance += amount
                self.__transactions.append({"type": "Transfer", "amount": amount})
                print(
                    f"\nTransferred ${amount} to {another_account.name}. New balance: ${self.__balance}"
                )
            else:
                print("\nInvalid transfer amount.")
        else:
            print("\nAccount does not exist.")          


class SavingsAccount(Account):
    def __init__(self, name, email, address, accountType, interestRate):
        super().__init__(name, email, address, accountType)
        self.interestRate = interestRate

    def apply_interest(self):
        interest = self.__balance * (self.interestRate / 100)
        print("\n------Interest is applied!!--------")
        self.deposit(interest)


class CurrentAccount(Account):
    def __init__(self, name, email, address, accountType, limit):
        super().__init__(name, email, address, accountType)
        self.limit = limit


    def withdraw(self, amount):
        if self._Account__balance <= 0:
            print("\n---the bank is bankrupt.----")
        else:
            if amount > 0 and amount <= self.limit:
                if amount <= self._Account__balance:
                    self._Account__balance -= amount
                    self._Account__transactions.append({'type': 'Withdrawal', 'amount': amount})
                    print(f"\nWithdraw ${amount}. New balance: ${self._Account__balance}")
                else:
                    print("\nWithdrawal amount exceeded")
            else:
                print("\nInvalid withdrawal amount or exceeded limit")


class Admin(Account):
    def __init__(self, name, email, address):
        super().__init__(name, email, address, 'admin')

    @staticmethod
    def delete_user(accountNo):
        for user in Account.accounts:
            if user.accountNo == accountNo:
                Account.accounts.remove(user)
                print(f"User {user.name} has been deleted.")
                break
        else:
            print("\n------User not found.-----")

    @staticmethod
    def list_users():
        if len(Account.accounts) != 0 :
            for user in Account.accounts:
                if user.name != 'admin':
                    print(f"Name: {user.name}, Email: {user.email}, Address is: {user.address}, Account No: {user.accountNo}, Account type: {user.accountType}")
                else:
                    continue
        else:
            print('\n-------No user found!!!--------')

    @staticmethod
    def total_available_balance():
        total_balance = 0
        for user in Account.accounts:
            total_balance += user._Account__balance
        print(f"-----Total Available Balance: ${total_balance}----")

    @staticmethod
    def total_loan_amount():
        total_loans = 0
        for user in Account.accounts:
            if 'Loan' in [transaction['type'] for transaction in user._Account__transactions]:
                total_loans += sum([transaction['amount'] for transaction in user._Account__transactions if transaction['type'] == 'Loan'])
        print(f"Total Loan Amount: ${total_loans}")


    @staticmethod
    def loan_feature(enable):
        if enable:
            for user in Account.accounts:
                user.loan_time = 2
            print("-------Loan feature has been enabled.-----")
        else:
            for user in Account.accounts:
                user.loan_time = 0
            print("----Loan feature has been disabled.-----")
            


# start program from here

currentUser = None
while True:
    if currentUser == None:
        print('\n-----WELCOME TO BANK MANAGEMENT SYSTEM---------------\n')
        access_person = input('-----Choose admin/user/exit : ').lower()
        if access_person == 'exit':
            break
        if access_person == 'user':
            print("\n--> No user logged in !")
            choice = input("\n--> Register/Login (R/L) : ")
            if choice == "R":
                name = input("Put your name to register: ")
                email = input("Put your email to register: ")
                address = input("Put your address to register: ")
                accountType = input("Savings Account or Special Account (savings/current): ")
                if accountType == "savings":
                    interestRate = int(input("Interest rate: "))
                    currentUser = SavingsAccount(name, email, address, accountType, interestRate)
                    print(f'\n--------------Welcome {currentUser.name}------------')
                    print('Your account created successfully')
                    print(f'Your email: {currentUser.email} and your address: {currentUser.address}')
                    print('-------------Thanks-------------------')
                else:
                    limit = int(input("Overdraft Limit: "))
                    currentUser = CurrentAccount(name, email, address, accountType, limit)
                    print(f'\n--------------Welcome {currentUser.name}------------')
                    print('Your account created successfully')
                    print(f'Your email: {currentUser.email} and your address: {currentUser.address}')
                    print('-------------Thanks-------------------')
            else:
                name = input("Put your name to login: ")
                address = input("Put your address to login: ")
                accountNo = name + address
                userFound = False
                for account in Account.accounts:
                    if account.accountNo == accountNo:
                        currentUser = account
                        userFound = True
                        break
                if userFound:
                    print(f'\n--------------Welcome {currentUser.name}------------')
                    print(f'Your email: {currentUser.email} and your address: {currentUser.address}')
                    print('-------------Thanks-------------------')
                else:
                    print("\n----User Not Found!----\n")

        else:
            admin_op = input("\n------new here???? put new/old : ")
            if admin_op == "new":
                name = input("put name admin:").lower()
                if name == "admin":
                    email = input("Email: ")
                    address = input("Address: ")
                    admin = Admin(name, email, address)
                    currentUser = admin
                    print(f'\n--------------Welcome {currentUser.name}------------')
                    print('Admin account created successfully.')
                    print(f'Your email: {currentUser.email} and your address: {currentUser.address}')
                    print('-------------Thanks-------------------')
                else:
                    print('\n----Try agin name not match----')
            else:
                currentUser = admin  
                print(f'\n--------------Welcome {currentUser.name}------------')
                print(f'Your email: {currentUser.email} and your address: {currentUser.address}')
                print('-------------Thanks-------------------')                 


    else:
        if currentUser.name == "admin":
            print("\n-----Options------:\n")
            print("1: Create an Account")
            print("2: Delete User")
            print("3: All Users List")
            print("4: Total Available Balance")
            print("5: Total Loan")
            print("6: Loan Feature active/inactive")
            print("7: Logout")

            ch = int(input("Choose option: "))
            if ch == 1:
                name = input("Put your name to register: ")
                email = input("Put your email to register: ")
                address = input("Put your address to register: ")
                accountType = input("Choose which account you want to create (savings/current): ")
                if accountType == "savings":
                    interestRate = int(input("Interest rate: "))
                    SavingsAccount(name, email, address, accountType, interestRate)
                    print(f'\n--------------Welcome To Our Bank------------')
                    print('Your account created successfully')
                    print('-------------Thanks-------------------')
                else:
                    limit = int(input("Overdraft Limit: "))
                    CurrentAccount(name, email, address, accountType, limit)
                    print(f'\n--------------Welcome To Our Bank------------')
                    print('Your account created successfully')
                    print('-------------Thanks-------------------')

            elif ch == 2:
                name = input("Name: ")
                address = input('Address: ')
                accountNo = name + address
                Admin.delete_user(accountNo)

            elif ch == 3:
                Admin.list_users()

            elif ch == 4:
                Admin.total_available_balance()

            elif ch == 5:
                Admin.total_loan_amount()

            elif ch == 6:
                enable = input("Enable or Disable Loan Feature (Y/N): ").lower()
                Admin.loan_feature(enable == 'y')
            elif ch == 7:
                currentUser = None
                print("Logged out.")
            else:
                print("Choose Valid Option!!")


        else:
            if currentUser.accountType == "savings":
                print("-----------------------------------")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check balance")
                print("4. Check Transaction History")
                print("5. Take Loan")
                print("6. Transfer Money")
                print("7. Logout")
                print("-----------------------------------\n")

                op = int(input("Choose Option: "))

                if op == 1:
                    amount = int(input("Enter deposit amount: "))
                    currentUser.deposit(amount)

                elif op == 2:
                    amount = int(input("Enter withdrawal amount: "))
                    currentUser.withdraw(amount)

                elif op == 3:
                    currentUser.check_balance()

                elif op == 4:
                    currentUser.transaction_history()

                elif op == 5:
                    amount = int(input("Give the loan amount: "))
                    currentUser.loan_taken(amount)

                elif op == 6:
                    name = input("Provide name: ")
                    email = input("Provide Email: ")
                    amount = int(input("Enter amount to transfer: "))
                    send_account = None
                    for account in Account.accounts:
                        if (
                            account.name == name
                            and account.email == email
                        ):
                            send_account = account
                            break
                    if send_account is not None:
                        currentUser.transfer_amount(send_account, amount)
                    else:
                        print("Account does not exist.")

                elif op == 7:
                    currentUser = None
                    print("Logged out.")

                else:
                    print("Choose Valid Option!!")

            else:
                print("-----------------------------------")
                print("1. Deposit")
                print("2. Withdraw")
                print("3. Check balance")
                print("4. Check Transaction History")
                print("5. Take Loan")
                print("6. Transfer Money")
                print("7. Logout")
                print("-----------------------------------\n")

                op = int(input("Choose Option: "))

                if op == 1:
                    amount = int(input("Enter deposit amount: "))
                    currentUser.deposit(amount)

                elif op == 2:
                    amount = int(input("Enter withdrawal amount: "))
                    currentUser.withdraw(amount)

                elif op == 3:
                    currentUser.check_balance()

                elif op == 4:
                    currentUser.transaction_history()

                elif op == 5:
                    amount = int(input("Give the loan amount: "))
                    currentUser.loan_taken(amount)

                elif op == 6:
                    name = input("Provide name: ")
                    email = input("Provide Email: ")
                    amount = int(input("Enter amount to transfer: "))
                    send_account = None
                    for account in Account.accounts:
                        if (
                            account.name == name
                            and account.email == email
                        ):
                            send_account = account
                            break
                    if send_account is not None:
                        currentUser.transfer_amount(send_account, amount)
                    else:
                        print("Account does not exist.")

                elif op == 7:
                    currentUser = None
                    print("Logged out.")

                else:
                    print("Choose Valid Option!!")