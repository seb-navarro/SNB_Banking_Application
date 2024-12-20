# Welcome to the SNB Banking Application!

# Three test accounts have been created for ease of testing, each with two current, two savings, and two mortgage accounts.
# To access these accounts please refer to their customer logins below:
# (Username: customer_one - Password: 1) 
# (Username: customer_two - Password: 2) 
# (Username: customer_three - Password: 3)

# The admin login is: 
# (Username: admin - Password: access)

# Note - Floating point numbers were not used to represent currency because of the rounding errors they produce. Instead pounds and pence are represented as seperate integers which are then correctly formated.

# To skip to the first function that starts the program please go to line number: 760




# 'randint' is imported to generate a random account number for each bank account.
from random import randint
# 'ceil' is imported for use in calculating monthly mortgage repayments
from math import ceil
# 'json' module is imported for handling the import and export of accounts and customer records into and out of the program.
import json




# List of accounts which updates with each account created or deleted and recieves stored accounts from the 'accounts.json' file when the program starts.
accounts_list = []

# Dictionary of customer 'password:username' key:value pairs. Also recives stored logins from the 'customers.json' file when the program starts.
customer_records = {}

# Admin login information stored in the same format as the customer logins. Only one admin login exists but there is potential to add more.
admin_records = {"access": "admin"}

# Attributes that the admin user can change on 'Current' or 'Savings' customer accounts. Labeled as standard, premium or best to relect the effect they would have on an account in the real world.
foreign_exchange_fee_categories = {"standard": 3, "premium": 1, "best": 0}
saving_interest_categories = {"standard": 4, "premium": 5, "best": 7}

# Fixed interest of 5% is assumed for on mortgage accounts in the SNB application.
fixed_mortgage_interest = 1.05




# Account is the base class that all bank accounts at SNB inherit from.
# It includes a unnique 8-digit account number, the customer name and password, the account balance divided in pounds and pence, and the category of account it falls under.
class Account:
    def __init__(self, number, c_name, c_pass, pounds_balance, pence_balance, category):
        self.number = number
        self.c_name = c_name
        self.c_pass = c_pass
        self.pounds_balance = pounds_balance
        self.pence_balance = pence_balance
        self.category = category



    # The '__repr__' method was implemented to represent accounts as their respective unique account number.
    # The '__str__' method was first attempted but this did not represent the accounts as their numbers when in the accounts list so '__repr__' was used instead.
    def __repr__(self):
        return f"{self.number}"
    


    # 'dict' method returns the account object as a dictionary. This is used to perform a dump to a JSON file effectively.
    def dict(self):
        return {"number": self.number, "c_name": self.c_name, "c_pass": self.c_pass, "pounds_balance": self.pounds_balance, "pence_balance": self.pence_balance, "category": self.category}
    


    # Opens the customer account menu for the account object.
    def account_menu(self):
        print("----------")
        # Displays the category of account as well as the account number.
        print(f"You have selected {self.category} account: {self}")
        # Gives 5 options but options 2 and 3 differ depending on whether the object is a 'Current' or 'Savings account or if it is a 'Mortgage' account.
        print("1. View balance")
        # 'Current' and 'Savings' accounts allow the user to deposit or withdraw money from this menu.
        if self.category == "Current" or self.category == "Savings":
            print("2. Deposit money")
            print("3. Withdraw money")
        # 'Mortgage' accounts allow the user to view the months left to pay on the mortgage or to make a monthly payment towards the mortgage.
        elif self.category == "Mortgage":
            print("2. View months left on mortgage")
            print("3. Make a monthly payment")
        print("4. Back to customer menu")
        print("5. Exit SNB Application")
        print("----------")
        choice = input("Please select 1, 2, 3, 4 or 5: ")

        while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "5":
            choice = input("Incorrect input, please state either 1, 2, 3, 4 or 5 (by typing 1, 2, 3, 4 or 5): ")

        # If 1 is selected by the user then the account balance is displayed through the corresponding method.
        if choice == "1":
            print("----------")
            self.show_balance()

        # If choice 2 is selected and the account is not a 'Mortgage' account then the process to deposit money begins.
        elif choice == "2":
            if self.category != "Mortgage":
                print("----------")
                print("How much money would you like to deposit in your account?")
                print("----------")
                # The user is asked how much they would like to deposit and their selected ammount is correctly formated with the 'format_currency' function.
                deposit_ammount = format_currency()
                print("----------")
                # The deposit method is then called passing the pounds and pence values as arguments.
                self.deposit(deposit_ammount[0], deposit_ammount[1])
            # if choice 2 is selected and the account is a 'Mortgage' account then the method to view the months left on the mortgage is called.
            elif self.category == "Mortgage":
                print("----------")
                self.view_months_left()

        # if choice 3 is selected and the account is not a 'Mortgage' account then the process to withdraw money from the account begins.
        elif choice == "3":
            if self.category != "Mortgage":
                print("----------")
                print("How much money would you like to withdraw from your account?")
                print("----------")
                # The user is asked how much they would like to withdraw and their selected ammount is correctly formated with the 'format_currency' function.
                withdraw_ammount = format_currency()
                print("----------")
                # The withdraw method is then called passing the pounds and pence values as arguments.
                self.withdraw(withdraw_ammount[0], withdraw_ammount[1])
            # if choice 3 is selected and the account is a 'Mortgage' account then the method to make a monthly payment is called.
            elif self.category == "Mortgage":
                print("----------")
                self.make_monthly_payment()

        # If choice 4 is selected then the user is taken back to the customer menu.
        elif choice == "4":
            customer_menu()

        # If choice 5 is selected then the user exits the SNB Application.
        elif choice == "5":
            exit()
    


    # Displays the balance in the account object.
    def show_balance(self):
        # Formats the full balance by taking the pounds and pence balance of the object separated by a '.' with a pound sign at the begining.
        full_balance = f"£{self.pounds_balance}.{self.pence_balance:02d}"
        # Displays the formated balance and gives an option to return to the account menu or exit the SNB Application.
        print(f"Account balance is: {full_balance}")
        print("-")
        print("1. Return to account menu")
        print("2. Exit SNB application")
        print("----------")
        balance_choice = input("Please select 1 or 2: ")

        while balance_choice != "1" and balance_choice != "2":
            balance_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if balance_choice == "1":
            self.account_menu()
        elif balance_choice == "2":
            exit()



    # Deposits money into an account object.
    # Assumes that the ammount to deposit has been correctly formatted with the 'format_currency' function and takes the separate pounds and pence ammmounts as arguments.
    def deposit(self, pounds_ammount, pence_ammount):
        # Adds the arguments increasing the pounds and pence balance by however much is being deposited.
        self.pounds_balance += pounds_ammount
        self.pence_balance += pence_ammount

        # If the account object's pence balance becomes higher than 100 then 100 is taken away from the pence balance and 1 is added to the pounds balance.
        # This keeps the currency correct in the account.
        if self.pence_balance >= 100:
            self.pounds_balance += 1
            self.pence_balance -= 100

        # 'full_ammount' and 'full_balance' are variables that store the correctly formated ammount deposited and balance.
        full_ammount = f"£{pounds_ammount}.{pence_ammount:02d}"
        full_balance = f"£{self.pounds_balance}.{self.pence_balance:02d}"

        # Displays the outcome of the deposit.
        print(f"You have deposited {full_ammount} into your account")
        print(f"Your new balance is now: {full_balance}")

        # Saves the state of the account object by exporting the accounts.
        export_accounts()
        print("----------")
        print("1. Return to account menu")
        print("2. Exit SNB application")
        print("----------")
        # Choice to either return to account menu or exit the SNB Application.
        deposit_choice = input("Please select 1 or 2: ")

        while deposit_choice != "1" and deposit_choice != "2":
            deposit_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if deposit_choice == "1":
            self.account_menu()
        elif deposit_choice == "2":
            exit()



    # Withdraws money from an account object.
    # Assumes that the ammount to withdraw has been correctly formatted with the 'format_currency' function and takes the separate pounds and pence ammmounts as arguments.
    def withdraw(self, pounds_ammount, pence_ammount):
        # If the ammount of pounds requested to withdraw is more than the pounds in the account object, then the withdraw is cancelled.
        if pounds_ammount > self.pounds_balance:
            full_balance = f"£{self.pounds_balance}.{self.pence_balance:02d}"
            print("Withdraw unsuccessful, not enough funds in your account")
            print(f"Account balance: {full_balance}")

        # If the pounds ammount and pounds balance is equal, and the pence ammount is greater than the pence balance then the withdraw is cancelled.
        elif pounds_ammount == self.pounds_balance and pence_ammount > self.pence_balance:
            full_balance = f"£{self.pounds_balance}.{self.pence_balance:02d}"
            print("Withdraw unsuccessful, not enough funds in your account")
            print(f"Account balance: {full_balance}")

        # If the pounds ammount is less than the pounds balance and the pence ammount is greater than the pence balance then the transaction goes ahead but the account balance must be correctly formatted.
        elif pounds_ammount < self.pounds_balance and pence_ammount > self.pence_balance:
            # The pounds ammount is subtracted from the pounds balance, then the pounds balance is subtracted 1.
            self.pounds_balance -= pounds_ammount
            self.pounds_balance -= 1
            # The pence balance is subtracted the pence ammount putting it in a negative but then it has 100 added to it.
            # This represents how currency actually works since 100 pence represent 1 pound.
            self.pence_balance -= pence_ammount
            self.pence_balance += 100
            full_ammount = f"£{pounds_ammount}.{pence_ammount:02d}"
            full_balance = f"£{self.pounds_balance}.{self.pence_balance:02d}"
            print(f"Withdraw of {full_ammount} successful")
            print(f"Your new balance is now: {full_balance}")

        # If the pounds ammount is smaller or equal to pounds balance and pence ammount is smaller or equal to pence balance then the transaction goes ahead.
        elif pounds_ammount <= self.pounds_balance and pence_ammount <= self.pence_balance:
            # Pounds and pence ammounts are subtracted from the account object's pounds and pence balance.
            self.pounds_balance -= pounds_ammount
            self.pence_balance -= pence_ammount
            full_ammount = f"£{pounds_ammount}.{pence_ammount:02d}"
            full_balance = f"£{self.pounds_balance}.{self.pence_balance:02d}"
            print(f"Withdraw of {full_ammount} successful")
            print(f"Your new balance is now: {full_balance}")
        
        # Accounts are exported to save changes.
        export_accounts()
        print("----------")
        print("1. Return to account menu")
        print("2. Exit SNB application")
        print("----------")
        # User is given the option to go back to the account menu or exit the SNB Application.
        withdraw_choice = input("Please select 1 or 2: ")

        while withdraw_choice != "1" and withdraw_choice != "2":
            withdraw_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if withdraw_choice == "1":
            self.account_menu()
        elif withdraw_choice == "2":
            exit()



    # Displays the account object's admin menu which is only accessible through logging in as an admin.
    # From here the user has 5 choices but choice 2 differs depending on the account object category.
    def admin_account_menu(self):
        print("----------")
        print(f"You have selected {self.category} account: {self}")
        print("1. View all details")
        # If the object is a 'Current account then the option to alter foreign exchange fees is given.
        if self.category == "Current":
            print("2. Alter foreign currency exchange fees")
        # If the object is a 'Savings' account then the option to alter the interest rate is given.
        elif self.category == "Savings":
            print("2. Alter interest rate")
        # If the object is a 'Mortgage' account then the option to flag or unflag the account for missed payments is given.
        elif self.category == "Mortgage":
            print("2. Flag/unflag account for missed payments")
        print("3. Close account")
        print("4. Back to admin menu")
        print("5. Exit SNB Application")
        print("----------")
        access_choice = input("Please select 1, 2, 3, 4 or 5: ")

        # Depending on the choice the user can view the account information, close the account, return to the admin menu, or exit the SNB Application by calling the corresponding methods.
        # If the user chooses 2 then the method called will depend on the account object category.
        if access_choice == "1":
            self.admin_display_info()
        elif access_choice == "2":
            if self.category == "Current":
                self.admin_alter_foreign_exchange_fees()
            elif self.category == "Savings":
                self.admin_alter_interest_rate()
            elif self.category == "Mortgage":
                self.admin_flag_or_unflag()
        elif access_choice == "3":
            self.admin_close_account()
        elif access_choice == "4":
            admin_menu()
        elif access_choice == "5":
            exit()


    
    # Displays all of the details relating to an account object.
    def admin_display_info(self):
        print("----------")
        print(f"Account number: {self.number}")
        print(f"Customer: {self.c_name}")
        print(f"Balance: £{self.pounds_balance}.{self.pence_balance}")
        print(f"Account category: {self.category}")
        # Depending on the category of account different information will be displayed.
        if self.category == "Current":
            print(f"Foreign exchange fee: {self.foreign_exchange_fee}%")
        elif self.category == "Savings":
            print(f"Interest rate: {self.interest_rate}%")
        elif self.category == "Mortgage":
            print(f"Monthly repayments: {self.months_remaining}")
            print(f"Months remaining: {self.months_remaining}")
            print(f"Flagged for missed payments: {self.flagged_for_missed_payments}")
        print("----------")
        print("1. Return to account menu")
        print("2. Exit SNB Application")
        print("----------")
        # User has the option to return to the admin account menu or exit the SNB Application.
        display_choice = input("Please select 1 or 2: ")

        while display_choice != "1" and display_choice != "2":
            display_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
            
        if display_choice == "1":
            self.admin_account_menu()
        elif display_choice == "2":
            exit()



    # Closes the account object.
    def admin_close_account(self):
        print("----------")
        print("Are you sure you want to close this account?")
        print("Once deletion is confirmed the account cannot be recovered")
        print("1. Delete")
        print("2. Cancel")
        print("----------")
        # Checks if the user definitely wants to delete the bank account and asks for an input to confirm.
        delete_choice = input("Please select either 1 or 2: ")

        while delete_choice != "1" and delete_choice != "2":
            delete_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")

        # If the user chooses to delete the bank account then the bank account is removed from the accounts list.
        if delete_choice == "1":
            accounts_list.remove(self)
            # The accounts list is then exported to save the changes.
            export_accounts()
            print("----------")
            print("Account deleted")
            print("1. Return to admin menu")
            print("2. Exit SNB Application")
            print("----------")
            # User is given the option to return to the admin menu or exit the SNB application.
            remove_choice = input("Please select 1 or 2: ")

            while remove_choice != "1" and remove_choice != "2":
                remove_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")

            if remove_choice == "1":
                admin_menu()
            elif remove_choice == "2":
                exit()
        elif delete_choice == "2":
            self.admin_account_menu()




# Current account is a subclass of Account. It adds the foreign exchange fee attribute which is unique to current accounts at SNB.
class Current(Account):
    def __init__(self, number, c_name, c_pass, pounds_balance, pence_balance, category, foreign_exchange_fee):
        super().__init__(number, c_name, c_pass, pounds_balance, pence_balance, category)
        self.foreign_exchange_fee = foreign_exchange_fee



    # 'dict' in the 'Current' class inherits the dictionary from its parent class and updates that dictionary with its unique foreign exchange fee attribute.
    def dict(self):
        object_dictionary = super().dict()
        object_dictionary.update({"foreign_exchange_fee": self.foreign_exchange_fee})
        return object_dictionary
    


    # 'from_dict' recieves a dictionary, and from that dictionary it creates an instance of the class it is being called from
    # 'from_dict' accesses the dictionary values through the keys specified in the method and passes those values as the data required to create an instance of the class.
    # '@classmethod' is used because this method is tied to the class itself rather than an instance of the class.
    # This is because the method creates the instance of the class, therefore when it is called the instance does not yet exist.
    @classmethod
    def from_dict(cls, data):
        return cls(data["number"], data["c_name"], data["c_pass"], data["pounds_balance"], data["pence_balance"], data["category"], data["foreign_exchange_fee"])
    


    # Alters the foreign exchange fee attribute in a 'Current' account object
    def admin_alter_foreign_exchange_fees(self):
        # List holds the foreign exchange fee categories that are not currently active for the 'Current' account object.
        temp_fef_categories = []

        print("----------")
        # Loops through the dictionary containing all possible foreign exchange fee categories and adds the current foreign exchange fee category to a variable whilst placing the others in a list.
        for i in foreign_exchange_fee_categories:
            if self.foreign_exchange_fee == foreign_exchange_fee_categories[i]:
                current_fef_category = i
            else:
                temp_fef_categories.append(i)
        
        # Displays the current foreign exchange fee category and rate whilst giving the option to alter the rate to another one of the possible foreign exchange fees.
        print(f"Current foreign exchange fee category: {current_fef_category}")
        print(f"Current foreign exchange fee rate: {self.foreign_exchange_fee}%")
        print("Alter to:")
        print(f"1. Foreign exchange fee: {temp_fef_categories[0]} = {foreign_exchange_fee_categories[temp_fef_categories[0]]}%")
        print(f"2. Foreign exchange fee: {temp_fef_categories[1]} = {foreign_exchange_fee_categories[temp_fef_categories[1]]}%")
        print("3. Cancel")
        print("----------")
        # The user can change the foreign exchange fee of the account to one of the two displayed or cancel the change.
        alter_fef_choice = input("Please select either 1, 2 or 3: ")

        while alter_fef_choice != "1" and alter_fef_choice != "2" and alter_fef_choice != "3":
            alter_fef_choice = input("Incorrect input please select either 1, 2 or 3 (by typing 1, 2 or 3): ")

        # Depending on the choice the foreign exchange fee can be changed in the 'Current' account object.
        # A message then displays showing the category as well as the rate as a percentage for the foreign exchange fee once it is changed.
        if alter_fef_choice == "1":
            self.foreign_exchange_fee = foreign_exchange_fee_categories[temp_fef_categories[0]]
            # Accounts are then exported to save the changes made.
            export_accounts()
            print("----------")
            print(f"Foreign exchange fee successfuly altered to '{temp_fef_categories[0]}' rate")
            print(f"New foreign exchange fee: {self.foreign_exchange_fee}%")
            print("----------")
        elif alter_fef_choice == "2":
            self.foreign_exchange_fee = foreign_exchange_fee_categories[temp_fef_categories[1]]
            export_accounts()
            print("----------")
            print(f"Foreign exchange fee successfuly altered to '{temp_fef_categories[1]}' rate")
            print(f"New foreign exchange fee: {self.foreign_exchange_fee}%")
            print("----------")
        elif alter_fef_choice == "3":
            print("----------")
            print("Foreign exchange fee alter cancelled")
            print("----------")

        print("1. Return to account menu")
        print("2. Exit SNB Application")
        print("----------")
        # The user then has the choice of whether to return to the admin account menu or exit the SNB Application.
        f_category_choice = input("Please select 1 or 2: ")

        while f_category_choice != "1" and f_category_choice != "2":
            f_category_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if f_category_choice == "1":
            self.admin_account_menu()
        elif f_category_choice == "2":
            exit()




# Savings account is a subclass of Account. It adds the savings interest rate attribute which all savings accounts at SNB have.
class Savings(Account):
    def __init__(self, number, c_name, c_pass, pounds_balance, pence_balance, category, interest_rate):
        super().__init__(number, c_name, c_pass, pounds_balance, pence_balance, category)
        self.interest_rate = interest_rate
    


    # 'dict' in the 'Savings' class inherits the dictionary from its parent class and updates that dictionary with its unique interest attribute.
    def dict(self):
        object_dictionary = super().dict()
        object_dictionary.update({"interest_rate": self.interest_rate})
        return object_dictionary
    


    # 'from_dict' in the 'Savings' class performs the same function as 'from_dict' in the 'Current' class but recieves slightly different data.
    # The only difference is that instead of passing 'foreign_excxhange_fee' data to the class, 'interest_rate' data is passed to creata an instance of a 'Saving' class.
    @classmethod
    def from_dict(cls, data):
        return cls(data["number"], data["c_name"], data["c_pass"], data["pounds_balance"], data["pence_balance"], data["category"], data["interest_rate"])
    


    # Alters the interest rate attribute in a 'Savings' account object.
    def admin_alter_interest_rate(self):
        # List holds the interest categories that are not currently active for the 'Savings' account object.
        temp_saving_interest_categories = []

        print("----------")
        # Loops through the dictionary containing all possible interest categories and adds the current interest rate category to a variable whilst placing the others in a list.
        for i in saving_interest_categories:
            if self.interest_rate == saving_interest_categories[i]:
                current_interest_category = i
            else:
                temp_saving_interest_categories.append(i)

        # Displays the current interest category and rate whilst giving the option to alter the rate to another one of the possible interest rates.
        print(f"Current interest category: {current_interest_category}")
        print(f"Current interest rate: {self.interest_rate}%")
        print("Alter to:")
        print(f"1. Interest rate: {temp_saving_interest_categories[0]} = {saving_interest_categories[temp_saving_interest_categories[0]]}%")
        print(f"2. Interest rate: {temp_saving_interest_categories[1]} = {saving_interest_categories[temp_saving_interest_categories[1]]}%")
        print("3. Cancel")
        print("----------")
        # The user can change the interest rate of the account to one of the two displayed or cancel the change.
        alter_interest_choice = input("Please select either 1, 2 or 3: ")

        while alter_interest_choice != "1" and alter_interest_choice != "2" and alter_interest_choice != "3":
            alter_interest_choice = input("Incorrect input please select either 1, 2 or 3 (by typing 1, 2 or 3): ")

        # Depending on the choice the interest rate can be changed in the 'Current' account object.
        # A message then displays showing the category as well as the rate as a percentage for the interest once it is changed.
        if alter_interest_choice == "1":
            self.interest_rate = saving_interest_categories[temp_saving_interest_categories[0]]
            # Accounts are exported to save the changes made.
            export_accounts()
            print("----------")
            print(f"Interest successfuly altered to '{temp_saving_interest_categories[0]}' rate")
            print(f"New interest rate: {self.interest_rate}%")
            print("----------")
        elif alter_interest_choice == "2":
            self.interest_rate = saving_interest_categories[temp_saving_interest_categories[1]]
            export_accounts()
            print("----------")
            print(f"Interest successfuly altered to '{temp_saving_interest_categories[1]}' rate")
            print(f"New interest rate: {self.interest_rate}%")
            print("----------")
        elif alter_interest_choice == "3":
            print("----------")
            print("Interest rate alter cancelled")
            print("----------")

        print("1. Return to account menu")
        print("2. Exit SNB Application")
        print("----------")
        # The user then has the choice of whether to return to the admin account menu or exit the SNB Application.
        i_category_choice = input("Please select 1 or 2: ")

        while i_category_choice != "1" and i_category_choice != "2":
            i_category_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if i_category_choice == "1":
            self.admin_account_menu()
        elif i_category_choice == "2":
            exit()




# Mortgage account is a subclass of Account. It adds a monthly repayment divided into pounds and pence, the months remaining until the mortgage is paid off, and whether the account is flagged for a missed payment.
class Mortgage(Account):
    def __init__(self, number, c_name, c_pass, pounds_balance, pence_balance, category, monthly_repayment_pounds, monthly_repayment_pence, months_remaining, flagged_for_missed_payments):
        super().__init__(number, c_name, c_pass, pounds_balance, pence_balance, category)
        self.monthly_repayment_pounds = monthly_repayment_pounds
        self.monthly_repayment_pence = monthly_repayment_pence
        self.months_remaining = months_remaining
        self.flagged_for_missed_payments = flagged_for_missed_payments



    # 'dict' in the 'Mortgage' class inherits the dictionary from its parent class and updates that dictionary with its unique 'Mortgage' class attributes.
    def dict(self):
        object_dictionary = super().dict()
        object_dictionary.update({"monthly_repayment_pounds": self.monthly_repayment_pounds})
        object_dictionary.update({"monthly_repayment_pence": self.monthly_repayment_pence})
        object_dictionary.update({"months_remaining": self.months_remaining})
        object_dictionary.update({"flagged_for_missed_payment": self.flagged_for_missed_payments})
        return object_dictionary
    


    # 'from_dict' in the 'Mortgage' class performs the same function as 'from_dict' in the 'Current' class but again recieves slightly different data.
    # The only difference is that instead of passing 'foreign_excxhange_fee' data to the class, 'monthly_repayment_pounds', 'monthly_repayment_pence', 'months_remaining', and 'flagged_for_missed_payment' data is passed to creata an instance of a 'Mortgage' class.
    @classmethod
    def from_dict(cls, data):
        return cls(data["number"], data["c_name"], data["c_pass"], data["pounds_balance"], data["pence_balance"], data["category"], data["monthly_repayment_pounds"], data["monthly_repayment_pence"], data["months_remaining"], data["flagged_for_missed_payment"])
    


    # Makes a monthly payment into a 'Mortgage' account.
    def make_monthly_payment(self):
        # List will store 'Current' accounts registered to the same user as the 'Mortgage' account that have a balance high enough to make the monthly mortgage payment.
        c_current_accounts = []
        # Indicates whether there are any eligible accounts to make a monthly payment from
        eligible_accounts = False
        # Used to break the while loop when an eligible account number is inputed by the user.
        eligible_inlist = False

        # Checks if there is at least one account registered to the user that is eligible to make the monthly payment (has to be a 'Current' account with a high enough balance to cover the cost of the monthly payment).
        for a in accounts_list:
            if a.c_name == c_username and a.c_pass == c_pword and a.category == "Current" and float(f"{a.pounds_balance}.{a.pence_balance}") > float(f"{self.monthly_repayment_pounds}.{self.monthly_repayment_pence}"):
                eligible_accounts = True
                break
        
        # If an eligible account exists then the monthly mortgage payment is displayed for the 'Mortgage' account as well as a list of accounts that the user is able to make a payment from.
        if eligible_accounts == True:
            print(f"Monthly mortgage payment for Account: {self} is £{self.monthly_repayment_pounds}.{self.monthly_repayment_pence}")
            print("PLease select one of your eligible SNB current accounts to make a monthly mortgage payment from")
            print(f"Eligible current accounts registered to {c_username}:")
            print("-")
            for a in accounts_list:
                if a.c_name == c_username and a.c_pass == c_pword and a.category == "Current" and float(f"{a.pounds_balance}.{a.pence_balance}") >= float(f"{self.monthly_repayment_pounds}.{self.monthly_repayment_pence}"):
                    # All eligible accounts are also added to the 'c_current_accounts' list.
                    c_current_accounts.append(a)
                    # Eligible accounts display their number as well as their balance.
                    print(f"{a}: Balance = £{a.pounds_balance}.{a.pence_balance}")
            print("----------")
            # The user is asked to input one of the 8-digit account numbers displayed from the eligible accounts printed.
            eligible_account_choice = input("Please select the account you want to make a payment from by typing the corresponding account number: ")

            # While loop runs until a match is made between the 'eligible_acount_choice' and an account in the list of eligible accounts stored in 'c_current_accounts'.
            while eligible_inlist == False:
                for ac in c_current_accounts:
                    # If a match is made then the monhtly repayment ammount is subtracted from the chosen 'Current' account balance.
                    if eligible_account_choice == str(ac):
                        ac.pounds_balance -= self.monthly_repayment_pounds
                        ac.pence_balance -= self.monthly_repayment_pence
                        # If after the subtraction the chosen 'Current' account pence balance is less than 0, then pence gets added 100 and the pounds balance gets 1 subtracted.
                        if ac.pence_balance < 0:
                            ac.pence_balance += 100
                            ac.pound_balance -= 1
                        
                        # The 'Mortgage' account balance which represents the ammount left to pay off is also subtracted the monthly payment ammount now that it has been paid.
                        self.pounds_balance -= self.monthly_repayment_pounds
                        self.pence_balance -= self.monthly_repayment_pence
                        # If after the subtraction the 'Mortgage' account pence balance is less than 0, then pence gets added 100 and the pounds balance gets 1 subtracted.
                        if self.pence_balance < 0:
                            self.pence_balance += 100
                            self.pounds_balance -= 1
                        # The months remaining attribute also gets 1 subtracted because there is one less month to pay.
                        self.months_remaining -= 1
                        # Accounts are exported to save the changes made.
                        export_accounts()
                        # Message displays informing the user that the monthly mortgage payment was successfull along with the new 'Current' account balance, the 'Mortgage' account balance left to pay, and the months remaining until the mortgage is fully paid off.
                        print("----------")
                        print("Monthly mortgage payment successfully processed")
                        print(f"Current account balance: £{ac.pounds_balance}.{ac.pence_balance}")
                        print(f"Mortgage account balance left to pay: £{self.pounds_balance}.{self.pence_balance}")
                        print(f"Months remaining until mortgage is fully paid off: {self.months_remaining}")
                        # 'eligible_inlist' is set to True which will exit the while loop.
                        eligible_inlist = True
                        # 'break' is used to exit the for loop
                        break
                    # If a match is not made then 'eligible_inlist' reamins false.
                    else:
                        eligible_inlist = False
                # If there is no match after comparing between the user input and every account in the list, then an error message displays and the user is asked to try another input.
                if eligible_inlist == False:
                    print("Incorrect input")
                    eligible_account_choice = input("Please type one of the 8-digit account numbers displayed from the list above: ")

        # If an eligible account registered to the user does not exist then a message is displayed informing the user that they do not have any eligible accounts.
        elif eligible_accounts == False:
            print("You have no eligible accounts that are able to make this payment")
            print("You need a valid current account registered at SNB with enough funds to cover the cost of the mortgage payment")
            print(f"Your monthly mortgage payment on this account is £{self.monthly_repayment_pounds}.{self.monthly_repayment_pence}")

        # The user is given the option to return to the account menu or exit the SNB Application.
        print("----------")
        print("1. Return to account menu")
        print("2. Exit SNB application")
        print("----------")
        monthly_payment_choice = input("Please select 1 or 2: ")

        while monthly_payment_choice != "1" and monthly_payment_choice != "2":
            monthly_payment_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if monthly_payment_choice == "1":
            self.account_menu()
        elif monthly_payment_choice == "2":
            exit()



    # Displays the months left until the 'Mortgage' account is fully paid off.
    def view_months_left(self):
        print(f"Months remaining until mortgage is paid off: {self.months_remaining}")
        print("----------")
        print("1. Return to account menu")
        print("2. Exit SNB application")
        print("----------")
        # The user is given the option to return to the account menu or exit the SNB Application.
        view_months_choice = input("Please select 1 or 2: ")

        while view_months_choice != "1" and view_months_choice != "2":
            view_months_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        if view_months_choice == "1":
            self.account_menu()
        elif view_months_choice == "2":
            exit()



    # Flags or unflags a 'Mortgage' account for missed payments.
    def admin_flag_or_unflag(self):
        print("----------")
        # Displays a different message depending on whether the 'Mortgage' account is already flagged for missed payments or not.
        # All 'Mortgage' accounts are created with 'flagged_for_missed_payments' set to False.
        if self.flagged_for_missed_payments == False:
            print("Would you like to flag this account for missed payments?")
        elif self.flagged_for_missed_payments == True:
            print("Would you like to unflag this account for missed payments")
        print("1. Yes")
        print("2. No (Back to admin account menu)")
        print("----------")
        # Gives the option to flag or unflag a 'Mortgage' account or go back to the admin account menu.
        flag_choice = input("Please select 1 or 2: ")

        while flag_choice != "1" and flag_choice != "2":
            flag_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
        
        # If user chooses option 1 then if the account is not flagged it will flag the account and set the 'flagged_for_missed_payments' attribute to True.
        if flag_choice == "1":
            if self.flagged_for_missed_payments == False:
                self.flagged_for_missed_payments = True
                # Accounts are exported to save changes made.
                export_accounts()
                print("----------")
                print("Account successfully flagged for missing payments")
            # If the account is flagged it will unflag the account and set the 'flagged_for_missed_payments' attribute to False.
            elif self.flagged_for_missed_payments == True:
                self.flagged_for_missed_payments = False
                # Accounts are exported to save changes made.
                export_accounts()
                print("----------")
                print("Account successfully unflagged for missing payments")

            print("----------")
            print("1. Return to account menu")
            print("2. Exit SNB application")
            print("----------")
            # The user is given the option to return to the admin account menu or exit the SNB Application.
            second_flag_choice = input("Please select 1 or 2: ")

            while second_flag_choice != "1" and second_flag_choice != "2":
                second_flag_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
            
            if second_flag_choice == "1":
                self.admin_account_menu()
            elif second_flag_choice == "2":
                exit()
        # Returns to admin menu.
        elif flag_choice == "2":
            self.admin_account_menu()




# Starts the banking application displaying the starting menu as well as calling the functions to import the customer logins and customer accounts.
def start_banking_app():
    import_accounts()
    import_customer_records()
    print("----------")
    print("Welcome to SNB! The bank ready to meet all your financial needs.")
    print("-")
    print("1. Register as a new customer")
    print("2. Log in to an exising customer account")
    print("3. Admin Login")
    print("4. Exit SNB Application")
    print("---------- ")
    # Displays in the application ask for a number input corresponding to what the user wants to do.
    choice = input("Please select 1, 2 or 3: ")

    # This makes sure that the only input that can be accepted will be one of the numbers displayed.
    while choice != "1" and choice != "2" and choice != "3" and choice != "4":
        choice = input("Incorrect input, please state either 1, 2, 3 or 4 (by typing 1, 2, 3 or 4): ")

    # This takes the input given by the user and matches what the user's choice is with an action corresponding to that choice.
    # In this example each choice corresponds to a different function that performs a different action in the application.
    if choice == "1":
        register_new_customer()
    elif choice == "2":
        customer_login()  
    elif choice == "3":
        admin_login()
    elif choice == "4":
        exit()



# Imports account objects from JSON file.
# All the bank account instances are stored in a JSON file called 'accounts.json'. Each account is a dictionary containing its data in values stored in key:value pairs.
def import_accounts():
    try:
        # Opens and loads the account dictionaries into a list.
        with open("accounts.json", "r", encoding="utf-8") as file:
            accounts_dicts = json.load(file)
    # Error handling displays an error informing the user that the file cannot be located in the roor folder of the project.
    # SystemExit is then raised to exit the program.
    # Accounts are imported at the begining of the program therefore the program will not properly start if this error is present.
    except FileNotFoundError:
        print("----------")
        print("--ERROR--")
        print("Customer bank account records not found")
        print("Please make sure the 'accounts.json' file is located in the same folder as the Python file")
        print("Once this condition is fulfilled try running the application again")
        print("----------")
        raise SystemExit
    # Loops through all the account dictionaries checking if the 'category' value matches 'Current', 'Savings', or 'Mortgage'.
    # If there is a match it will create an instance of the corresponding account type using the 'from_dict' class method and add this instance to the accounts list.
    for accounts in accounts_dicts:
        if accounts["category"] == "Current":
            accounts_list.append(Current.from_dict(accounts))
        elif accounts["category"] == "Savings":
            accounts_list.append(Savings.from_dict(accounts))
        elif accounts["category"] == "Mortgage":
            accounts_list.append(Mortgage.from_dict(accounts))



# Imports customer records (Logins) from JSON file
def import_customer_records():
    try:
        # Customer logins are stored in 'customer_records.json' as password:username pairs.
        # The logins are loaded in from the json file and are used to update the 'customer_records' dictionary.
        # This creates a single dictionary with all the customer logins which is populated at the start of the program.
        with open("customer_records.json", "r", encoding="utf-8") as file:
            customer_records.update(json.load(file))
    # Error handling displays an error if the file is not found in the root folder of the SNB Application. 'SystemExit' is then raised to exit the program.
    except FileNotFoundError:
        print("----------")
        print("--ERROR--")
        print("Customer records not found")
        print("Please make sure the 'customer_records.json' file is located in the same folder as the Python file")
        print("Once this condition is fulfilled try running the application again")
        print("----------")
        raise SystemExit



# Starts the process of registering a new customer to the bank.
def register_new_customer():
    # 'papproved' is a local variable that determines whether the password inputted by the user is valid. It is set to false by default.
    papproved = False
    
    # Takes the first name of the user and makes sure that no spaces are present in the input.
    print("----------")
    fname = input("Please enter your first name: ")
    while " " in fname or fname == "":
        fname = input("Please enter your first name with no spaces: ")
        
    # Takes the last name of the user and makes sure that no spaces are present in the input.
    lname = input ("Please enter your last name: ")
    while " " in lname or lname == "":
        lname = input("Please enter your last name with no spaces: ")
    
    # Combines the user's first and last name separated with an underscore to give a username.
    name = fname + "_" + lname

    print("----------")
    password = input("Please enter a password for banking on this application: ")

    # Checks if the password is valid by ruling out whether the password has any spaces and whether the password is already taken by another customer.
    while papproved == False:
        if " " in password or password == "":
            password = input("Please enter your password with no spaces: ")
        # Password needs to be unique because it is used as the key in the customer records dictionary to store customer logins.
        # The password was chosen as the unique key because realistically a bank can have two customers with exactly the same name.
        elif password in customer_records:
            password = input("Password already in use please enter a different password: ")
        else:
            papproved = True

    # 'customer_records' is updated with the new login and the whole dictionary is exported to the 'customer_records.json' file to fully save the new customer.
    customer_records.update({password: name})
    export_customer_records()

    # Displays the customer username and password so that the user can refer back to this information when they want to log in to their account.
    print("----------")
    print("Customer successfully registered")
    print("-")
    print(f"Your username is: {name}")
    print(f"Your password is: {password}")
    print("Please note these down somewehere safe as they will be used to login to your account")
    print("-")
    
    # The function to open a bank account is called as part of registering a new customer so that the new customer has a bank account to access.
    open_account(name, password)

    # Once the bank account is created the user can choose to either log in to their account or exit the SNB application.
    print("----------")
    print("1. Login to your account")
    print("2. Exit")
    print("----------")
    login_choice = input("Please select 1 or 2: ")

    while login_choice != "1" and login_choice != "2":
        login_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")

    if login_choice == "1":
        customer_login()
    elif login_choice == "2":
        exit()



# Opens a new bank account, taking the user's username and password as arguments.
def open_account(user, passw):
    # Gives the choice between opening one of the three type of accounts available at SNB.
    print("----------")
    print("What type of account are you looking to open:")
    print("1. Current Account")
    print("2. Savings Account")
    print("3. Mortgage Account")
    print("----------")
    account_selection = input("please select 1, 2 or 3: ")

    while account_selection != "1" and account_selection != "2" and account_selection != "3":
        account_selection = input("Incorrect input, please select 1, 2 or 3: ")

    # A unique account number is generated by calling the 'generate_unique_ac_number' function which returns this number. The unique number is then passed to 'account_number'.
    account_number = generate_unique_ac_number()

    # Depending on the user's selection of account type a corresponding account type is created.
    # 'Current' and 'Savings' accounts are created using the unique account number created, customer username and password, a balance of 0 pounds and pence, and their respective category.
    # The final attribute is retrieved from the list of different foreign exchange fee and interest rates. Both types of accounts recieve the 'standard' rate when intially created.
    if account_selection == "1":
        current_account = Current(account_number, user, passw, 0, 0, "Current", foreign_exchange_fee_categories["standard"])
    elif account_selection == "2":
        savings_account = Savings(account_number, user, passw, 0, 0, "Savings", saving_interest_categories["standard"])
    elif account_selection == "3":
        # Creating a 'Mortgage' account requires further inputs by the user which are contained in a separate function called 'open_mortgage'.
        mortgage_account = open_mortgage(user, passw, account_number)

    # Depending on the choice the user made on which type of account to create, the corresponding account object is added to the accounts list.
    if account_selection == "1":
        accounts_list.append(current_account)
    elif account_selection == "2":
        accounts_list.append(savings_account)
    elif account_selection =="3":
        accounts_list.append(mortgage_account)
    # Once the accounts list is updated, the list is exported to save the changes made.
    export_accounts()
    
    # Depending on the choice made by the user, the corresponding account information is displayed which includes the unique account number.
    if account_selection == "1":
        print(f"{current_account.category} account successfully created")
        print(f"{current_account.category} account number: {current_account}")
    elif account_selection == "2":
        print(f"{savings_account.category} account successfully created")
        print(f"{savings_account.category} account number: {savings_account}")
    elif account_selection == "3":
        print(f"{mortgage_account.category} account successfully created")
        print(f"{mortgage_account.category} account number: {mortgage_account}")



# Opens a 'Mortgage' account taking the user's username, password, and unique account number generated as arguments.
def open_mortgage(user, passw, ac_num):
    # The two is_valid variables are used to check for conditions fulfilled in the while loops of the function.
    is_valid = False
    second_is_valid = False

    # To open a 'Mortgage' account first the user must input how much the value of the property they want to purchase is.
    print("----------")
    print("How much do you need to borrow to purchase your property?")
    # The full ammount for the property is inputted and correctly formatted into pounds and pence with the 'format_currency' function.
    # The format currency function returns two values, one is pounds and one is pence, therefore 'borrow_ammount_full' becomes a list.
    borrow_ammount_full = format_currency()
    # The minimum a customer is allowed to borrow for a 'Mortgage' account at SNB is £10,000 so this checks that the pounds value is more than 10,000
    # If the value is less than 10,000 then an error message is displayed and a new ammount is requested.
    while borrow_ammount_full[0] < 10000:
        print("The minimum ammount you can borrow is £10,000")
        borrow_ammount_full = format_currency()
    # Asks the customer to input over how many months they want to pay off their mortgage.
    print("----------")
    print("How long would you like the repayment term to be? (In months)")
    # Mortgage repayment duration must be between 6 and 500 months at SNB.
    # One while loop handles the value error possibility and the nested while loop inside handles the correct input of repayment duration.
    while is_valid == False:
        try:
            while second_is_valid == False:
                repayment_term = int(input("Months: "))
                if repayment_term > 500 or repayment_term < 6:
                    print("repayment terms must range between 6 and 500 months")
                    second_is_valid = False
                else:
                    second_is_valid = True
                    is_valid = True
        except ValueError:
            print("Incorrect input please enter a whole number with no spaces")
    print("----------")
    # Turns the ammount to borrow back into a float and stores it in 'full_ammount_float'.
    full_ammount_float = float(f"{borrow_ammount_full[0]}.{borrow_ammount_full[1]}")
    # 'monthly' is the full ammount divided by the repayment terms, then multiplied by 1.05 to represent interest added on. This interest of 5% is fixed for all mortgage accounts at SNB.
    # 'ceil' function was used instead of the round function to account for fees the bank can charge on top of the fixed interest rate. All monthly payments are rounded to whole pounds.
    monthly = ceil((full_ammount_float / repayment_term) * fixed_mortgage_interest)

    # The full ammount to be paid back to the bank.
    real_full_ammount = monthly * repayment_term

    # Message informing the user about how much they will have to pay and for how long.
    print(f"SNB can offer you a mortgage with monthly repayments of £{monthly} for a term of {repayment_term} months")
    print(f"The full ammount repayable to the bank will be £{real_full_ammount}")
    print("This includes the '5%' fixed interest rate for all SNB mortgage accounts, as well as any added fees")
    print("Would you like to proceed with opening this mortgage account?")
    print("1. Yes")
    print("2. No (Exit SNB Application)")
    print("----------")
    # User has the choice to accept what the bank has offered or exit the SNB Application.
    create_choice = input("Please select 1 or 2: ")

    while create_choice != "1" and create_choice != "2":
        create_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")

    # If the user proceeds with creating the 'Mortgage' account then it is created, setting the balance to the full ammount to be paid back, adding the ammount to be paid monthly, and setting 'flagged_for_missed_payments' to False.
    if create_choice == "1":
        mortgage_account = Mortgage(ac_num, user, passw, real_full_ammount, 0, "Mortgage", monthly, 0, repayment_term, False)
        # The function returns the 'Mortgage' account object if the user chooses to create it.
        return mortgage_account
    elif create_choice == "2":
        exit()



# Generates a unique 8-digit account number for use in creating bank accounts at SNB.
# The account number has to be unique so a customer can refer to their bank account with their unique number.
def generate_unique_ac_number():
    # Temporary list of account numbers is created
    temp_ac_numbers = []
    # The 'randint' function is called to generate a random integer between 10000000 and 99999999.
    account_number = randint(10000000, 99999999)

    # Loops through the list of all bank accounts adding each account number to the temporary account numbers list.
    for a in accounts_list:
        temp_ac_numbers.append(a.number)
    # Checks if the account number generated exists in the temporary list that was just populated.
    # If it is in the list then the function calls itself and the account number becomes the return value of the function called.
    # This creates a recursive function which continues to call itself until a unique number is found.
    if account_number in temp_ac_numbers:
       account_number = generate_unique_ac_number()
    # Once a unique account number is found, the if statement does not run and the function returns the unique account number generated.
    return account_number



# Exports account objects to JSON file
# Bank account instances are saved into the 'acounts.json' file everytime an account is created, a change occurs in an account, or the SNB Application is exited.
def export_accounts():
    # list of all account instances represented as dictionaries is created by looping through the accounts list and calling the 'dict' instance method.
    accounts_dicts = [account.dict() for account in accounts_list]

    # The list of account dictionaries is dumped into the 'acounts.json' file in a format which makes each account easily retrievable by calling the 'import_accounts' function.
    with open("accounts.json", "w", encoding="utf-8") as file:
        json.dump(accounts_dicts, file, indent = 4)



# Exports customer records (Logins) to JSON file
# Because the customer logins are stored in a dictionary they can be dumped straight into the 'customer_records.json' file.
# This function is called everytime a new customer is registered and everytime the SNB Application is exited.
def export_customer_records():
    with open("customer_records.json", "w", encoding="utf-8") as file:
        json.dump(customer_records, file, indent = 4)



# Lets the user attempt to log in to a customer account.
def customer_login():
    # Customer username and customer password entered in the log in are set as global variables to be used in other functions.
    global c_username
    global c_pword
    # 'customer_access' is set to False by default and only turns True when a correct username password combination is inputted.
    customer_access = False
    # 'counter' keeps track of how many attempts remaining a user has to try and log in.
    counter = 4

    # Input is taken for a username and password from the user.
    print("----------")
    print("Please input your username and password")
    c_username = input("Username: ")
    c_pword = input("Password: ")
    print("----------")

    # The username password combination must be correct in 3 attempts following the first wrong attempt.
    # The for loop gives the user 3 more attempts to try and get their username password combination right, otherwise customer access remains 'False'.
    for i in range(3):
        # Checks if the password entered (c_pword) matches a key in the 'customer_records' dictionary and if the username entered (c_username) matches the value in 'customer_records' accessed by using 'c_pword' as the key.
        if c_pword in customer_records and c_username == customer_records[c_pword]:
            # If the condition is met, 'customer_access' is set to True and the for loop breaks.
            customer_access = True
            break
        # If the condition is not met then 'customer_access' remains False and the 'counter' value drops by 1.
        else:
            counter -= 1
            customer_access = False
            # A message displays informing the user that they have inputted incorrect details and the number of attempts they have remaining.
            print("Incorrect username or password, please try again")
            print(f"{counter} attempts remaining")
            # The user is asked to try inputting the username and password again.
            c_username = input("Username: ")
            c_pword = input("Password: ")
            print("----------")
    
    # Once the for loop is exited, if 'customer_access' is now True then the user is granted access to the customer menu.
    if customer_access == True:
        customer_menu()
    # If customer_access remains False then a message displays informing the user that they have exceeded the maximum login attempts and the 'exit' function is called to exit the SNB Application.
    elif customer_access == False:
        print("You have exceeded the maximum number of login attempts.")
        print("The app will now close")
        exit()



# Displays the customer menu giving the option to access a customer's accounts, open a new bank account or exit the SNB Application.
def customer_menu():
        print(f"Welcome {c_username}")
        print("1. Access account(s)")
        print("2. Open a new account")
        print("3. Exit SNB Application")
        print("----------")
        choice = input("Please select 1, 2 or 3: ")

        while choice != "1" and choice != "2" and choice != "3":
            choice = input("Incorrect input, please state either 1, 2 or 3 (by typing 1, 2 or 3): ")
        
        if choice == "1":
            # Calls the 'show_accounts' function which displays all the accounts linked to the specific customer that is logged in.
            show_accounts()
        # Opens another new bank account that will be linked to the logged in customer by passing the customer username and password as arguments.
        elif choice == "2":
            open_account(c_username, c_pword)
            print("----------")
            print("1. Back to customer menu")
            print("2. Exit SNB Application")
            print("----------")
            # Gives the option to return to the customer menu or exit the SNB Application after opening a new bank account.
            oa_choice = input("Please select 1 or 2: ")

            while oa_choice != "1" and choice != "2":
                oa_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")
            
            if oa_choice == "1":
                print("----------")
                customer_menu()
            elif oa_choice == "2":
                exit()
        elif choice == "3":
            exit()



# Displays all the bank accounts linked to the logged in customer.
# From the list of accounts the customer can select which account they want to access by typing the corresponding number.
def show_accounts():
    # List of accounts registered to the specific customer logged in.
    c_accounts = []
    # Used to exit the while loop in this function.
    inlist = False

    print("----------")
    print(f"Accounts registered to {c_username}:")
    print("-")
    # Loops through every account in the accounts list and adds the account to the customer accounts list if the customer name (c_name) and customer password (c_pass) on the account matches the username and password of the logged in customer.
    # It also prints the account if the conditions are fulfilled.
    for a in accounts_list:
        if a.c_name == c_username and a.c_pass == c_pword:
            c_accounts.append(a)
            print(a, a.category)
    print("----------")
    # Takes an input from the user which asks to input the account number of the account they want to access.
    account_choice = input("Please select the account you want to access by typing the corresponding account number: ")

    # Loops until a valid account number is inputted.
    while inlist == False:
        # Checks every account in customer accounts to see if the 'acount_choice' input matches the string representation of each account.
        for ac in c_accounts:
            if account_choice == str(ac):
                # If there is a match the function which opens the account menu for that specific account is called.
                ac.account_menu()
                inlist = True
            else:
                # If no match is made 'inlist' stays false.
                inlist = False
        # If no match is made then a message is displayed informing the user of their incorrect input and they are asked to try again.
        if inlist == False:
            print("Incorrect input")
            account_choice = input("Please type one of the 8-digit account numbers displayed from the list above: ")



# Begins the admin login process.
# Works the same way as the 'customer_login' function but directs the user to the admin menu if the username and password are correct
def admin_login():
    global a_username
    global a_pword
    admin_access = False
    counter = 4

    # Asks for admin username and password to grant admin access to the SNB Application.
    print("----------")
    print("Please input an admin username and password (Clue: It's Username: 'admin', Password: 'access')")
    a_username = input("Username: ")
    a_pword = input("Password: ")
    print("----------")

    # After the initial attempt the user has 3 more attempts at trying to enter the admin username and password.
    for i in range(3):
        # Checks the 'admin_records' dictionary to see if the admin username (a_username) and admin password (a_password) correctly match as a key:value pair.
        if a_pword in admin_records and a_username == admin_records[a_pword]:
            admin_access = True
            break
        else:
            counter -= 1
            admin_access = False
            print("Incorrect username or password, please try again")
            print(f"{counter} attempts remaining")
            a_username = input("Username: ")
            a_pword = input("Password: ")
            print("----------")
    
    # Opens the admin menu if the username and password entered correctly match.
    if admin_access == True:
        admin_menu()
    # Exits the application if tries are exceeded.
    elif admin_access == False:
        print("You have exceeded the maximum number of login attempts.")
        print("The app will now close")
        exit()



# Displays the admin menu allowing the admin to access all active bank accounts at SNB or exit the application.
def admin_menu():
    print("Admin Menu")
    print(f"Welcome {a_username}")
    print("1. Access customer account(s)")
    print("2. Exit SNB Application")
    print("----------")
    admin_choice = input("Please select 1 or 2: ")

    while admin_choice != "1" and admin_choice != "2":
        admin_choice = input("Incorrect input, please state either 1 or 2 (by typing 1 or 2): ")

    # If the user choses option 1, the 'admin_show_accounts' funtion is called which displays all bank accounts at SNB.
    if admin_choice == "1":
        admin_show_accounts()
    #If the user choses option 2 they exit the SNB Application.
    elif admin_choice == "2":
        exit()



# Shows all bank accounts from all customers at SNB.
# Allows the user to select an account and access the admin options for that account.
def admin_show_accounts():
    # 'a_inlist' is used to determine when to break the while loop in this function.
    a_inlist = False

    print("----------")
    print("Customer accounts at SNB:")
    print("-")
    # Loops through all accounts in the accounts list and prints each ones number, category and the name of the customer it belongs to.
    for a in accounts_list:
        print(f"{a} - {a.category} account belonging to {a.c_name}")
    print("----------")
    # Asks the user to select an account by typing the corresponding account number.
    show_choice = input("Please select the account you want to access by typing the corresponding account number: ")

    # While loop makes sure that if the account number inputted does not match any accounts then an error is given and the user is asked to try again.
    while a_inlist == False:
        # Loops through all accounts and if the 'show_choice' input matches a string representation of the account, then the user is taken to the admin account menu for that specific account.
        for a in accounts_list:
            if show_choice == str(a):
                a.admin_account_menu()
                a_inlist = True
            else:
                a_inlist = False
        if a_inlist == False:
            print("Incorrect input")
            show_choice = input("Please type one of the 8-digit account numbers displayed from the list above: ")



# Correctly formats currency inputs into pounds and pence.
def format_currency():
    # Checks for a condition to be met so the while loop can be exited.
    valid = False

    # while makes sure that the ammount entered is more than 0 and is a float value.
    while valid == False:
        # Error handling makes sure the value entered is a float, otherwise an error message is displayed.
        try:
            ammount = float(input("Ammount: £"))
            if ammount > 0:
                valid = True
            else:
                print("Please enter a valid currency input in pounds and pence with no spaces (e.g. 123.45)")
        except ValueError:
            print("Please enter a valid currency input in pounds and pence with no spaces (e.g. 123.45)")

    # The 'ammount value is formated into a string and split where the decimal point appears.
    # This creates a 'seperated' list with index [0] corresponding to the pounds value and index [1] corresponding to the pence value.
    separated = str(ammount).split(".")

    # Checks to see if the length of the pence value is greater than 2 characters, in which case a messsage displays to input a valid currency input.
    # This is because the length of the pence value cannot be greater than 2 so if the user has inputted a float value with more than 2 figures following the decimal point then the value cannot be accepted.
    while len(separated[1]) > 2:
        valid = False
        print("Please enter a valid currency input in pounds and pence with no spaces (e.g. 123.45)")
        while valid == False:
            try:
                ammount = float(input("Ammount: £"))
                if ammount > 0:
                    valid = True
                else:
                    print("Please enter a valid currency input in pounds and pence with no spaces (e.g. 123.45)")
            except ValueError:
                print("Please enter a valid currency input in pounds and pence with no spaces (e.g. 123.45)")

        # The new inputed ammount is separated so that the check on the length of 'separated[1]' (pence value) can take place again.
        separated = str(ammount).split(".")       

    # Once the ammount is valid, it is formated to 2 decimal points.
    # An example of why this is done is so that if a user inputs 10.1 then the 'f_ammount' will format this to 10.10.
    f_ammount = f"{ammount:.2f}"
    # The formated ammount is formated into a string and split at the decimal point giving the final pounds and pence values.
    separated = str(f_ammount).split(".")
        
    # These pounds and pence values are passed to the 'pounds' and 'pence' variables
    pounds = separated[0]
    pence = separated[1]

    # Finally the function returns the pounds and pence variables as two integers.
    return int(pounds), int(pence)



# Exits the SNB Application.
def exit():
    # Prints a goodbye message.
    print("----------")
    print("Goodbye")
    print("----------")
    # Exports all the customer logins and accounts to their relevant JSON files.
    export_customer_records()
    export_accounts()
    # Raises 'SystemExit' to end the program.
    raise SystemExit



# Launches the SNB Application.
start_banking_app()