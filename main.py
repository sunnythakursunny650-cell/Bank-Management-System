import sqlite3
from bank import Bank

# Database Connection
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

while True:

    print("\n========== Bank Management System ==========")
    print("1. Create New Account")
    print("2. View All Accounts")
    print("3. Search Account")
    print("4. Deposit Money")
    print("5. Withdraw Money")
    print("6. Update Account")
    print("7. Delete Account")
    print("8. Exit")

    choice = input("Enter your choice: ")

    # ---------------- CREATE ACCOUNT ---------------- #

    if choice == "1":

        try:

            account_no = int(input("Enter Account Number: "))

            cursor.execute(
                "SELECT * FROM accounts WHERE account_no=?",
                (account_no,)
            )

            if cursor.fetchone():
                print("Account Number Already Exists ❌")
                continue

            name = input("Enter Customer Name: ")

            mobile = input("Enter Mobile Number: ")

            if len(mobile) != 10 or not mobile.isdigit():
                print("Invalid Mobile Number! Enter exactly 10 digits. ❌")
                continue

            balance = float(input("Enter Initial Balance: "))

            if balance < 0:
                print("Initial Balance cannot be negative. ❌")
                continue

            account = Bank(account_no, name, mobile, balance)

            cursor.execute("""
            INSERT INTO accounts(account_no, name, mobile, balance)
            VALUES(?, ?, ?, ?)
            """, (
                account.account_no,
                account.name,
                account.mobile,
                account.balance
            ))

            conn.commit()

            print("Account Created Successfully ✅")

        except ValueError:
            print("Invalid Input! Please enter valid numbers. ❌")

    # ---------------- VIEW ACCOUNTS ---------------- #

    elif choice == "2":

        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        if accounts:

            print("\n========== All Bank Accounts ==========")

            for account in accounts:

                print(f"""
Account Number : {account[0]}
Customer Name  : {account[1]}
Mobile Number  : {account[2]}
Balance        : ₹{account[3]}
----------------------------------------
""")

        else:
            print("No Accounts Found!")

    # ---------------- SEARCH ACCOUNT ---------------- #

    elif choice == "3":

        try:

            account_no = int(input("Enter Account Number: "))

            cursor.execute(
                "SELECT * FROM accounts WHERE account_no=?",
                (account_no,)
            )

            account = cursor.fetchone()

            if account:

                print("\n========== Account Details ==========")
                print(f"Account Number : {account[0]}")
                print(f"Customer Name  : {account[1]}")
                print(f"Mobile Number  : {account[2]}")
                print(f"Balance        : ₹{account[3]}")

            else:
                print("Account Not Found ❌")

        except ValueError:
            print("Invalid Account Number ❌")

    # ---------------- DEPOSIT MONEY ---------------- #

    elif choice == "4":

        try:

            account_no = int(input("Enter Account Number: "))
            amount = float(input("Enter Deposit Amount: "))

            if amount <= 0:
                print("Deposit Amount must be greater than 0 ❌")
                continue

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_no=?",
                (account_no,)
            )

            data = cursor.fetchone()

            if data:

                new_balance = data[0] + amount

                cursor.execute(
                    "UPDATE accounts SET balance=? WHERE account_no=?",
                    (new_balance, account_no)
                )

                conn.commit()

                print("Amount Deposited Successfully ✅")
                print(f"Updated Balance : ₹{new_balance}")

            else:
                print("Account Not Found ❌")

        except ValueError:
            print("Invalid Input ❌")

    
    # ---------------- WITHDRAW MONEY ---------------- #

    elif choice == "5":

        try:

            account_no = int(input("Enter Account Number: "))
            amount = float(input("Enter Withdraw Amount: "))

            if amount <= 0:
                print("Withdraw Amount must be greater than 0 ❌")
                continue

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_no=?",
                (account_no,)
            )

            data = cursor.fetchone()

            if data:

                balance = data[0]

                if amount <= balance:

                    new_balance = balance - amount

                    cursor.execute(
                        "UPDATE accounts SET balance=? WHERE account_no=?",
                        (new_balance, account_no)
                    )

                    conn.commit()

                    print("Amount Withdrawn Successfully ✅")
                    print(f"Remaining Balance : ₹{new_balance}")

                else:
                    print("Insufficient Balance ❌")

            else:
                print("Account Not Found ❌")

        except ValueError:
            print("Invalid Input ❌")


    # ---------------- UPDATE ACCOUNT ---------------- #

    elif choice == "6":

        try:

            account_no = int(input("Enter Account Number: "))
            new_name = input("Enter New Customer Name: ")
            new_mobile = input("Enter New Mobile Number: ")

            if len(new_mobile) != 10 or not new_mobile.isdigit():
                print("Invalid Mobile Number ❌")
                continue

            cursor.execute(
                """
                UPDATE accounts
                SET name=?, mobile=?
                WHERE account_no=?
                """,
                (new_name, new_mobile, account_no)
            )

            conn.commit()

            if cursor.rowcount > 0:
                print("Account Updated Successfully ✅")
            else:
                print("Account Not Found ❌")

        except ValueError:
            print("Invalid Input ❌")


    # ---------------- DELETE ACCOUNT ---------------- #

    elif choice == "7":

        try:

            account_no = int(input("Enter Account Number: "))

            cursor.execute(
                "DELETE FROM accounts WHERE account_no=?",
                (account_no,)
            )

            conn.commit()

            if cursor.rowcount > 0:
                print("Account Deleted Successfully ✅")
            else:
                print("Account Not Found ❌")

        except ValueError:
            print("Invalid Account Number ❌")


    # ---------------- EXIT ---------------- #

    elif choice == "8":

        print("\nThank You for Using Bank Management System 😊")
        conn.close()
        break


    # ---------------- INVALID CHOICE ---------------- #

    else:

        print("Invalid Choice! Please Enter 1 to 8 ❌")
