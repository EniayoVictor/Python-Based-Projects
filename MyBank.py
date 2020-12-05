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
    query = "INSERT INTO users(First_Name, Middle_Name, Last_Name, Username, Email, Phone_Number, Password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (First_Name, Middle_Name, Last_Name, Username, Email, Phone_Number, Password)
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

def Airtime_Top_Up_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    print("Welcome to MyBANK Airtime Top-Up")
    print("""Please select a biller:
    1. MTN
    2. GLO
    3. 9mobile
    4. Airtel""")
    biller_selection = input("Select option: ")
    if biller_selection == "1" or "2" or "3" or "4":
        print("""Who are you recharging for?
    1. Self
    2. 3rd Party""")
        receiver_option = input("Select Option: ")
        if receiver_option == "1":
            query = "SELECT Phone_Number FROM users WHERE Username = %s and User_ID = %s"
            values = (Log_In_Username, User_ID)
            cursor.execute(query, values)
            number = cursor.fetchone()
            user_phone_number = number[0]
            airtime_amount = input("How much airtime would you like to purchase? ")
            if int(airtime_amount) < 100:
                print("The least amount you can purchase is #100. Please try again.")
                Airtime_Top_Up_Function()
            else:
                query = "SELECT Balance FROM users WHERE User_ID = %s and Username = %s"
                values = (User_ID, Log_In_Username)
                cursor.execute(query, values)
                the_balance = cursor.fetchone()
                current_balance = the_balance[0]
                if int(current_balance) > int(airtime_amount):
                    Balance_Update = int(current_balance) - int(airtime_amount)
                    query =  "UPDATE users SET Balance = %s WHERE User_ID = %s and Username = %s"
                    values = (Balance_Update, User_ID, Log_In_Username)
                    cursor.execute(query, values)
                    database.commit()

                    print("Your serice provider with phone number " + str(user_phone_number) + " has successfully been credited with " + str(airtime_amount) + " Thank you for using this service.")
                    Other_Transactions_Function()
        elif receiver_option == "2":
            receivers_phone_number = input("Enter the receiver's phone number: ")
            if len(receivers_phone_number) >= 11:
                airtime_amount = input("How much airtime will you like to send? ")
            if int(airtime_amount) < 100:
                print("The least amount you can purchase is #100. Please try again.")
                Airtime_Top_Up_Function()
            else:
                query = "SELECT Balance FROM users WHERE User_ID = %s and Username = %s"
                values = (User_ID, Log_In_Username)
                cursor.execute(query, values)
                the_balance = cursor.fetchone()
                current_balance = the_balance[0]
                if int(current_balance) > int(airtime_amount):
                    Balance_Update = int(current_balance) - int(airtime_amount)
                    query =  "UPDATE users SET Balance = %s WHERE User_ID = %s and Username = %s"
                    values = (Balance_Update, User_ID, Log_In_Username)
                    cursor.execute(query, values)
                    database.commit()

                    print("You have successfully credited a third party serice provider with phone number " + str(receivers_phone_number) + " with an amount of " + str(airtime_amount) + " Thank you for using this service.")
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

def Update_Bank_Information_Function():
    database = connector.connect(host="localhost", user="root",password = "", database = "mybank_register")
    cursor = database.cursor()
    update_option = input("""What would you like to update?
    1. Name
    2. Email
    3. Password
    4. Phone Number""")
    
    if update_option == "1":
        print("""
    1. First Name
    2. Middle Name
    3. Last Name
    4. Username""")
        name_to_update = input("Update: ")
        if name_to_update == "1":
            new_first_name = input("Update First Name to: ")
            query = "UPDATE users SET First_Name = %s WHERE User_ID = %s and Username = %s"
            values = (new_first_name, User_ID, Log_In_Username)
            cursor.execute(query, values)
            database.commit()
            print("You have succefully updated your first name.")
            Other_Transactions_Function()

        elif name_to_update == "2":
            new_middle_name = input("Update Middle Name to: ")
            query = "UPDATE users SET Middle_Name = %s WHERE User_ID = %s and Username = %s"
            values = (new_middle_name, User_ID, Log_In_Username)
            cursor.execute(query, values)
            database.commit()
            print("You have succefully updated your middle name.")
            Other_Transactions_Function()

        elif name_to_update == "3":
            new_last_name = input("Update Last Name to: ")
            query = "UPDATE users SET Last_Name = %s WHERE User_ID = %s and Username = %s"
            values = (new_last_name, User_ID, Log_In_Username)
            cursor.execute(query, values)
            database.commit()
            print("You have successfully updated your last name.")
            Other_Transactions_Function()

        elif name_to_update == "4":
            new_username = input("Update Username to: ")
            query = "UPDATE users SET Username = %s WHERE User_ID = %s and Username = %s"
            values = (new_username, User_ID, Log_In_Username)
            cursor.execute(query, values)
            database.commit()
            print("You have successfully updated your username. Your new username is " + new_username)
            Other_Transactions_Function()

    elif update_option == "2":
        new_email = input("Enter new email: ")
        query = "UPDATE users SET Email = %s WHERE User_ID = %s and Username = %s"
        values = (new_email, User_ID, Log_In_Username)
        cursor.execute(query, values)
        database.commit()
        print("You have successfully update your Email. Your new Email is " + new_email)
        Other_Transactions_Function()

    elif update_option == "3": 
        previous_password = input("Enter your current password: ")
        if previous_password == Log_In_Password:
            new_password = input("Enter your new password: ")
            confirm_new_password = input("Confirm your new password: ")
            if new_password == confirm_new_password:
                query = "UPDATE users SET Password = %s WHERE User_ID = %s and Username = %s"
                values = (new_password, User_ID, Log_In_Username)
                cursor.execute(query, values)
                database.commit()

                print("You have successfully changed your password. Your new password is " + new_password)
                Other_Transactions_Function()
            else:
                print("Your passwords don't match. Try again.")
                Update_Bank_Information_Function()
        
    elif update_option == "4":
        new_phone_number = input("Enter a new phone number: ")
        new_phone_number_confirmation = input("Confirm your new phone number: ")
        if new_phone_number == new_phone_number_confirmation:
            query = "UPDATE users SET Phone_Number = %s WHERE User_ID = %s and Username = %s"
            values = (new_phone_number, User_ID, Log_In_Username)
            cursor.execute(query, values)
            database.commit() 
            print("You have successfully updated your phone number. Your new phone number is " + new_phone_number)

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
    6. Update Bank Information""") 
    transaction_selection = input("Select Option: ")
    if transaction_selection == "1":
        Withdrawal_Function()
    elif transaction_selection == "2":
        Transfer_Function()
    elif transaction_selection == "3":
        Deposit_Function()
    elif transaction_selection == "4":
        Airtime_Top_Up_Function()
    elif transaction_selection == "5":
        Balance_Inquiry_Function()
    elif transaction_selection == "6":
        Update_Bank_Information_Function()

def New_Account_Function():
    global First_Name
    global Middle_Name
    global Last_Name
    global Username
    global Email
    global Phone_Number
    First_Name = input("Enter your First Name: ")
    Middle_Name = input("Enter your Middle Name: ")
    Last_Name = input("Enter your Last Name: ")
    Username = input("Enter your desired Username: ")
    Email = input("Enter your Email Address: ")
    Phone_Number = input("Enter your Phone Number: ")

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