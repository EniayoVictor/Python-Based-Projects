import mysql.connector as connector
import datetime as dt

global Date
global Time
DateTime = dt.datetime.now()
Date = DateTime.strftime("%a") + "," + DateTime.strftime("%d") + "-" + DateTime.strftime("%b") + "-" + DateTime.strftime("%Y")
Time = DateTime.strftime("%I") + ":" + DateTime.strftime("%M") + DateTime.strftime("%p")
print (Time, Date)

def Other_Transactions_Function():
    print("""Would you like to perform another transaction?
    1. Yes
    2. No""")
    Other_Transactions = input("Select Option: ")
    if Other_Transactions == "1":
        print("""
    1. Log in to an existing account
    2. Create a new account""")
        options = input("Select Option: ")
        if options == "1":
            Log_In_Function()
        elif options == "2":
            New_Account_Function()
    elif Other_Transactions == "2":
        print("Thank you for banking with us. See you soon.")
    else:
        print("Invalid Selection! Please try again.")
        Other_Transactions_Function()

def Database_Update():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    query = "INSERT INTO users(First_Name, Middle_Name, Last_Name, Username, Email, Password) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (First_Name, Middle_Name, Last_Name, Username, Email, Password)
    cursor.execute(query, values)
    database.commit()

def Password_Confirmation():
    global Password
    Password = input("Enter your desired password: ")
    Password_Confirmation = input("Confirm your password: ")
    if Password_Confirmation == Password:
        Database_Update()
    else:
        print("Your passwords don't match please try again")
        Password_Confirmation()

def Withdrawal_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()

    amount_to_be_withdrawn = input("How much would you like to withdraw? ")

    query = "SELECT Balance FROM users WHERE User_ID = %s and Username = %s"
    values = (User_ID, Log_In_Username)
    cursor.execute(query, values)
    init_balance = cursor.fetchone()
    initial_balance = init_balance[0]
    
    if (int(initial_balance)) > (int(amount_to_be_withdrawn)):
        final_balance = (int(initial_balance)) - (int(amount_to_be_withdrawn))

        database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
        cursor = database.cursor()
        query = "INSERT INTO transactions( User_ID, Credit_Debit_Status, Transaction_Performed, Date, Time, Initial_Balance, Final_Balance, Amount, Transaction_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (User_ID, "Debit", "Withdraw", str(Date), str(Time), initial_balance, final_balance, amount_to_be_withdrawn, "Successful")
        cursor.execute(query,values)
        database.commit()
        print(final_balance)
        
        database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
        cursor = database.cursor()
        query = "UPDATE users SET Balance =%s WHERE User_ID = %s and Username = %s"
        values = (final_balance, User_ID, Log_In_Username)
        cursor.execute(query,values)
        database.commit()

        Other_Transactions_Function()
    else:
        print("Your balance is insufficient!")

        database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
        cursor = database.cursor()
        query = "INSERT INTO transactions(User_ID, Credit_Debit_Status, Transaction_Performed, Amount, Transaction_Status) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (User_ID, "Debit", "Withdraw", amount_to_be_withdrawn, "Unsuccessful")
        cursor.execute(query, values)
        database.commit()
       
def Transfer_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()

    amount_to_transfer = input("How much do you want to transfer? ") 
    receivers_id = input("Enter the Receiver's ID: ")
    receivers_username = input("Enter the Receiver's Username: ")

    query = "SELECT * FROM users where User_ID = %s and Username = %s"
    values = (receivers_id, receivers_username)
    cursor.execute(query, values)
    receivers_id_crosscheck = cursor.fetchall()

    if len(receivers_id_crosscheck) <= 0:
        print("User not found. Please try again.")
        Transfer_Function()
    else:      
        query = "SELECT Balance FROM users where User_ID = %s and Username = %s"
        values = (User_ID, Log_In_Username)
        cursor.execute(query, values)
        init_balance = cursor.fetchone()
        initial_balance = init_balance[0]
        
        if (int(initial_balance)) > (int(amount_to_transfer)):
            final_balance = (int(initial_balance)) - (int(amount_to_transfer))

            database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
            cursor = database.cursor()
            query = "INSERT INTO transactions(User_ID, Credit_Debit_Status, Transaction_Performed, Date, Time, Initial_Balance, Final_Balance, Amount, Receivers_ID, Receivers_Username, Transaction_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (User_ID, "Debit", "Transfer", str(Date), str(Time), initial_balance, final_balance, amount_to_transfer, receivers_id, receivers_username, "Successful")
            cursor.execute(query,values)
            database.commit()
            print(final_balance)

            query = "UPDATE users SET Balance = %s WHERE User_ID = %s and Username = %s"
            values = (final_balance, User_ID, Log_In_Username)
            cursor.execute(query,values)
            database.commit()  

            query = "SELECT Balance FROM users WHERE User_ID = %s and Username = %s"
            values = (receivers_id, receivers_username)
            cursor.execute(query, values)
            receivers = cursor.fetchone()
            receivers_balance = receivers[0]

            receivers_final_balance = (int(amount_to_transfer)) + (int(receivers_balance)) 

            query = "UPDATE users SET Balance = %s WHERE User_ID = %s and Username = %s"
            values = (receivers_final_balance, receivers_id, receivers_username)
            cursor.execute(query, values)
            database.commit()     

            query = "INSERT INTO transactions(User_ID, Credit_Debit_Status, Transaction_Performed, Initial_Balance, Final_Balance, Amount, Senders_ID, Senders_Username, Transaction_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (receivers_id, "Credit", "Transfer", receivers_balance, receivers_final_balance, amount_to_transfer, User_ID, Log_In_Username, "Successful")
            cursor.execute(query,values)
            database.commit()
            print(final_balance)  

            Other_Transactions_Function()
        else:
            print("Your balance is insufficient!")

            database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
            cursor = database.cursor()
            query = "INSERT INTO transactions(User_ID, Credit_Debit_Status, Transaction_Performed, Amount, Transaction_Status) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (User_ID, "Debit", "Transfer", amount_to_transfer, "Unsuccessful")
            cursor.execute(query, values)
            database.commit()

def Deposit_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()

    amount_to_deposit = input("How much would you like to deposit? ")

    query = "SELECT Balance FROM users WHERE User_ID = %s and Username = %s"
    values = (User_ID, Log_In_Username)
    cursor.execute(query, values)
    init_balance = cursor.fetchone()
    initial_balance = init_balance[0]
    
    final_balance = (int(initial_balance)) + (int(amount_to_deposit))

    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    query = "INSERT INTO transactions( User_ID, Credit_Debit_Status, Transaction_Performed, Date, Time, Initial_Balance, Final_Balance, Amount, Transaction_Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (User_ID, "Credit", "Deposit", str(Date), str(Time), initial_balance, final_balance, amount_to_deposit, "Successful")
    cursor.execute(query,values)
    database.commit()
    print(final_balance)
        
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    query = "UPDATE users SET Balance =%s WHERE User_ID = %s and Username = %s"
    values = (final_balance, User_ID, Log_In_Username)
    cursor.execute(query,values)
    database.commit()

    Other_Transactions_Function()
    
def Balance_Inquiry_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    query = "SELECT Balance, First_Name FROM users where User_ID = %s and Username = %s"
    values = (User_ID, Log_In_Username)
    cursor.execute(query, values)
    MyBalance = cursor.fetchone()
    Balance = MyBalance[0]
    first_name = MyBalance[1]

    print(str(first_name) + ", You have " + str(Balance) + " left in your account.")
    Other_Transactions_Function()

def Change_Pin_Function():
    previous_password = input("Enter your current password: ")

    if previous_password == Log_In_Password:
        new_password = input("Enter your new password: ")
        confirm_new_password = input("Confirm your new password: ")
        if new_password == confirm_new_password:
            database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
            cursor = database.cursor()
            query = "UPDATE users SET Password = %s WHERE User_ID = %s and Username = %s"
            values = (new_password, User_ID, Log_In_Username)
            cursor.execute(query, values)
            database.commit()

            print("You have successfully changed your password. Your new password is " + new_password)
            Other_Transactions_Function()
        else:
            print("Your passwords don't match. Try again.")
            Change_Pin_Function()

def Transactions():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    query = "SELECT First_Name FROM users WHERE Username = %s and User_Id = %s"
    values = (Log_In_Username, User_ID)
    cursor.execute(query, values)
    First_Name = cursor.fetchone()  

    print("Welcome back " + First_Name[0]) 
    print("""What would you like to do?
    1. Withdraw Cash
    2. Transfer Money
    3. Deposit Cash
    4. Airtime Top-Up
    5. Check Balance
    6. Change PIN""") 
    transaction_selection = input("Select Option: ")
    if transaction_selection == "1":
        Withdrawal_Function()
    elif transaction_selection == "2":
        Transfer_Function()
    elif transaction_selection == "3":
        Deposit_Function()
    elif transaction_selection == "5":
        Balance_Inquiry_Function()
    elif transaction_selection == "6":
        Change_Pin_Function()

def New_Account_Function():
    global First_Name
    global Middle_Name
    global Last_Name
    global Username
    global Email
    First_Name = input("Enter your First Name: ")
    Middle_Name = input("Enter your Middle Name: ")
    Last_Name = input("Enter your Last Name: ")
    Username = input("Enter your desired Username: ")
    Email = input("Enter your Email Address: ")

    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()   
    query = "SELECT * FROM users WHERE Username = %s and Email = %s"
    values = (Username, Email)
    cursor.execute(query, values)
    Username_crosscheck = cursor.fetchall()
    if len(Username_crosscheck) > 0:
        print("This username has been taken. Please try another username.")
        New_Account_Function()
    else:
        Password_Confirmation()
        print("You have successfully created a new account. Your Username is " + Username + " and your Password is " + Password + " Please save these details as they would be required of you to access your account and perform other transactions." )
        Other_Transactions_Function()

def Log_In_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    global Log_In_Username
    global Log_In_Password
    Log_In_Username = input("Enter your username: ")
    Log_In_Password = input("Enter you password: ")

    query = "SELECT * FROM users WHERE Username = %s and Password = %s"
    values = (Log_In_Username, Log_In_Password)
    cursor.execute(query, values)
    Log_In_Confirmation = cursor.fetchall()
    if len(Log_In_Confirmation) <= 0:
        print("Invalid Log-In details! Try again.")
        Log_In_Function()
    else:
        query = "SELECT User_ID FROM users WHERE Username = %s and Password = %s"
        values = (Log_In_Username, Log_In_Password)
        cursor.execute(query, values)
        global User_ID
        User = cursor.fetchone()
        User_ID = User[0]
        Transactions()

def Welcome_Function():
    print("""Welcome to MY BANK
    What would you like to do?
    1. Log in to an existing account.
    2. Create a new account.""")
    welcome_selection = input("Your Selection: ")
    if welcome_selection == "1":
        Log_In_Function()
    elif welcome_selection == "2":
        New_Account_Function()

Welcome_Function()