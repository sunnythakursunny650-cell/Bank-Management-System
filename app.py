import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# DATABASE
# =========================================================

DB_PATH = Path(__file__).parent / "bank.db"


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            account_no INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)

    # -----------------------------------------------------
    # Add new columns to old database safely
    # -----------------------------------------------------

    columns = [
        ("email", "TEXT DEFAULT ''"),
        ("address", "TEXT DEFAULT ''"),
        ("account_type", "TEXT DEFAULT 'Savings'"),
        ("date_created", "TEXT DEFAULT ''")
    ]

    existing_columns = [
        row[1]
        for row in conn.execute(
            "PRAGMA table_info(accounts)"
        ).fetchall()
    ]

    for column_name, column_type in columns:

        if column_name not in existing_columns:

            conn.execute(
                f"ALTER TABLE accounts "
                f"ADD COLUMN {column_name} {column_type}"
            )

    # Add date to old accounts where it is empty
    conn.execute("""
        UPDATE accounts
        SET date_created = ?
        WHERE date_created IS NULL
        OR date_created = ''
    """, (
        datetime.now().strftime("%d-%m-%Y"),
    ))

    conn.commit()

    return conn


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: #777777;
    padding: 20px;
    font-size: 14px;
}

div[data-testid="stMetric"] {
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 12px;
    background: white;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🏦 Bank Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Professional customer account management system'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🏦 Bank Menu")

st.sidebar.write(
    "Manage customer accounts securely."
)

st.sidebar.divider()

option = st.sidebar.radio(
    "Select Operation",
    [
        "🏠 Dashboard",
        "➕ Create Account",
        "👥 View All Accounts",
        "🔍 Search Account",
        "💰 Deposit Money",
        "💸 Withdraw Money",
        "✏️ Update Account",
        "🔄 Change Account Number",
        "🗑️ Delete Account"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Python + SQLite + Streamlit"
)


# =========================================================
# DASHBOARD
# =========================================================

if option == "🏠 Dashboard":

    conn = get_connection()

    total_accounts = conn.execute(
        "SELECT COUNT(*) FROM accounts"
    ).fetchone()[0]

    total_balance = conn.execute(
        "SELECT COALESCE(SUM(balance), 0) FROM accounts"
    ).fetchone()[0]

    highest_balance = conn.execute(
        "SELECT COALESCE(MAX(balance), 0) FROM accounts"
    ).fetchone()[0]

    savings_accounts = conn.execute(
        """
        SELECT COUNT(*)
        FROM accounts
        WHERE account_type = 'Savings'
        """
    ).fetchone()[0]

    recent_accounts = conn.execute("""
        SELECT
            account_no,
            name,
            mobile,
            email,
            account_type,
            balance,
            date_created
        FROM accounts
        ORDER BY account_no DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    # -----------------------------------------------------
    # Dashboard Header
    # -----------------------------------------------------

    st.markdown(
        """
        <h1 style="
            font-size:36px;
            font-weight:800;
            margin-bottom:5px;
        ">
        🏠 Dashboard
        </h1>

        <p style="
            color:#6b7280;
            font-size:17px;
        ">
        Complete overview of your Bank Management System
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👥 Total Accounts",
            total_accounts
        )

    with col2:

        st.metric(
            "💰 Total Balance",
            f"₹{total_balance:,.2f}"
        )

    with col3:

        st.metric(
            "🏆 Highest Balance",
            f"₹{highest_balance:,.2f}"
        )

    with col4:

        st.metric(
            "🏦 Savings Accounts",
            savings_accounts
        )

    st.write("")

    st.divider()

    # -----------------------------------------------------
    # Recent Accounts
    # -----------------------------------------------------

    st.subheader("👥 Recent Accounts")

    if recent_accounts:

        df = pd.DataFrame(
            recent_accounts,
            columns=[
                "Account Number",
                "Customer Name",
                "Mobile",
                "Email",
                "Account Type",
                "Balance",
                "Date Created"
            ]
        )

        df["Balance"] = df["Balance"].apply(
            lambda x: f"₹{x:,.2f}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No accounts available. Create your first account."
        )

    st.write("")

    st.divider()

    # -----------------------------------------------------
    # Quick Actions
    # -----------------------------------------------------

    st.subheader("⚡ Quick Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:

        st.markdown(
            """
            <div style="
                padding:20px;
                text-align:center;
                border:1px solid #e5e7eb;
                border-radius:12px;
                background:#ffffff;
            ">
            <div style="font-size:30px;">➕</div>
            <b>Create Account</b>
            <p style="color:#6b7280;font-size:13px;">
            Add new customer
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with q2:

        st.markdown(
            """
            <div style="
                padding:20px;
                text-align:center;
                border:1px solid #e5e7eb;
                border-radius:12px;
                background:#ffffff;
            ">
            <div style="font-size:30px;">🔍</div>
            <b>Search Account</b>
            <p style="color:#6b7280;font-size:13px;">
            Find customer
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with q3:

        st.markdown(
            """
            <div style="
                padding:20px;
                text-align:center;
                border:1px solid #e5e7eb;
                border-radius:12px;
                background:#ffffff;
            ">
            <div style="font-size:30px;">💰</div>
            <b>Deposit Money</b>
            <p style="color:#6b7280;font-size:13px;">
            Add account balance
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with q4:

        st.markdown(
            """
            <div style="
                padding:20px;
                text-align:center;
                border:1px solid #e5e7eb;
                border-radius:12px;
                background:#ffffff;
            ">
            <div style="font-size:30px;">💸</div>
            <b>Withdraw Money</b>
            <p style="color:#6b7280;font-size:13px;">
            Withdraw balance
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.success(
        "✅ Bank Management System is ready to use."
    )


# =========================================================
# CREATE ACCOUNT
# =========================================================

elif option == "➕ Create Account":

    st.header("➕ Create New Account")

    st.caption(
        "Enter complete customer information to create a professional bank account."
    )

    with st.form("create_account_form"):

        # -------------------------------------------------
        # Basic Information
        # -------------------------------------------------

        st.subheader("👤 Customer Information")

        col1, col2 = st.columns(2)

        with col1:

            account_no = st.number_input(
                "🆔 Account Number",
                min_value=1,
                step=1
            )

            name = st.text_input(
                "👤 Customer Name",
                placeholder="Enter full name"
            )

            mobile = st.text_input(
                "📱 Mobile Number",
                max_chars=10,
                placeholder="10 digit mobile number"
            )

        with col2:

            email = st.text_input(
                "📧 Email Address",
                placeholder="example@gmail.com"
            )

            address = st.text_area(
                "🏠 Address",
                placeholder="Enter customer address"
            )

            account_type = st.selectbox(
                "💳 Account Type",
                [
                    "Savings",
                    "Current"
                ]
            )

        # -------------------------------------------------
        # Financial Information
        # -------------------------------------------------

        st.subheader("💰 Account Information")

        balance = st.number_input(
            "💰 Initial Balance",
            min_value=0.0,
            step=100.0
        )

        submitted = st.form_submit_button(
            "➕ Create Account",
            use_container_width=True
        )

        # -------------------------------------------------
        # CREATE ACCOUNT
        # -------------------------------------------------

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter customer name."
                )

            elif len(mobile) != 10 or not mobile.isdigit():

                st.error(
                    "Mobile number must contain exactly 10 digits."
                )

            elif email and "@" not in email:

                st.error(
                    "Please enter a valid email address."
                )

            elif not address.strip():

                st.error(
                    "Please enter customer address."
                )

            else:

                conn = get_connection()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT *
                    FROM accounts
                    WHERE account_no=?
                    """,
                    (int(account_no),)
                )

                existing = cursor.fetchone()

                if existing:

                    st.error(
                        f"Account number {int(account_no)} "
                        f"already exists ❌"
                    )

                else:

                    date_created = datetime.now().strftime(
                        "%d-%m-%Y"
                    )

                    cursor.execute(
                        """
                        INSERT INTO accounts
                        (
                            account_no,
                            name,
                            mobile,
                            balance,
                            email,
                            address,
                            account_type,
                            date_created
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            int(account_no),
                            name.strip(),
                            mobile,
                            float(balance),
                            email.strip(),
                            address.strip(),
                            account_type,
                            date_created
                        )
                    )

                    conn.commit()

                    st.success(
                        f"Account {int(account_no)} "
                        f"created successfully! ✅"
                    )

                    st.info(
                        f"Account Type: {account_type} | "
                        f"Date Created: {date_created}"
                    )

                conn.close()


# =========================================================
# PART 1 END
# =========================================================

# =========================================================
# VIEW ALL ACCOUNTS
# =========================================================

elif option == "👥 View All Accounts":

    st.header("👥 All Bank Accounts")

    conn = get_connection()

    data = conn.execute("""
        SELECT
            account_no,
            name,
            mobile,
            email,
            address,
            account_type,
            balance,
            date_created
        FROM accounts
        ORDER BY account_no
    """).fetchall()

    conn.close()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "Account Number",
                "Customer Name",
                "Mobile",
                "Email",
                "Address",
                "Account Type",
                "Balance",
                "Date Created"
            ]
        )

        df["Balance"] = df["Balance"].apply(
            lambda x: f"₹{x:,.2f}"
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            f"Total Accounts: {len(data)}"
        )

    else:

        st.warning(
            "No accounts found."
        )


# =========================================================
# SEARCH ACCOUNT
# =========================================================

elif option == "🔍 Search Account":

    st.header("🔍 Search Customer Account")

    search_type = st.selectbox(
        "Search By",
        [
            "Account Number",
            "Customer Name",
            "Mobile Number"
        ]
    )

    # -----------------------------------------------------
    # ACCOUNT NUMBER SEARCH
    # -----------------------------------------------------

    if search_type == "Account Number":

        search_value = st.number_input(
            "Enter Account Number",
            min_value=1,
            step=1
        )

    # -----------------------------------------------------
    # NAME SEARCH
    # -----------------------------------------------------

    elif search_type == "Customer Name":

        search_value = st.text_input(
            "Enter Customer Name",
            placeholder="Enter customer name"
        )

    # -----------------------------------------------------
    # MOBILE SEARCH
    # -----------------------------------------------------

    else:

        search_value = st.text_input(
            "Enter Mobile Number",
            max_chars=10,
            placeholder="Enter 10 digit mobile number"
        )

    if st.button(
        "🔍 Search Account",
        use_container_width=True
    ):

        conn = get_connection()

        # -------------------------------------------------
        # Search Account Number
        # -------------------------------------------------

        if search_type == "Account Number":

            results = conn.execute(
                """
                SELECT
                    account_no,
                    name,
                    mobile,
                    email,
                    address,
                    account_type,
                    balance,
                    date_created
                FROM accounts
                WHERE account_no=?
                """,
                (int(search_value),)
            ).fetchall()

        # -------------------------------------------------
        # Search Name
        # -------------------------------------------------

        elif search_type == "Customer Name":

            results = conn.execute(
                """
                SELECT
                    account_no,
                    name,
                    mobile,
                    email,
                    address,
                    account_type,
                    balance,
                    date_created
                FROM accounts
                WHERE name LIKE ?
                ORDER BY name
                """,
                (f"%{search_value.strip()}%",)
            ).fetchall()

        # -------------------------------------------------
        # Search Mobile
        # -------------------------------------------------

        else:

            results = conn.execute(
                """
                SELECT
                    account_no,
                    name,
                    mobile,
                    email,
                    address,
                    account_type,
                    balance,
                    date_created
                FROM accounts
                WHERE mobile=?
                """,
                (search_value.strip(),)
            ).fetchall()

        conn.close()

        # -------------------------------------------------
        # SHOW RESULTS
        # -------------------------------------------------

        if results:

            st.success(
                f"{len(results)} account(s) found! ✅"
            )

            for account in results:

                with st.container(border=True):

                    st.subheader(
                        f"🏦 Account {account[0]}"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**👤 Customer Name:** "
                            f"{account[1]}"
                        )

                        st.write(
                            f"**📱 Mobile:** "
                            f"{account[2]}"
                        )

                        st.write(
                            f"**📧 Email:** "
                            f"{account[3] or 'Not provided'}"
                        )

                        st.write(
                            f"**🏠 Address:** "
                            f"{account[4] or 'Not provided'}"
                        )

                    with col2:

                        st.write(
                            f"**💳 Account Type:** "
                            f"{account[5]}"
                        )

                        st.write(
                            f"**💰 Balance:** "
                            f"₹{account[6]:,.2f}"
                        )

                        st.write(
                            f"**📅 Date Created:** "
                            f"{account[7]}"
                        )

        else:

            st.error(
                "No matching account found ❌"
            )


# =========================================================
# DEPOSIT MONEY
# =========================================================

elif option == "💰 Deposit Money":

    st.header("💰 Deposit Money")

    account_no = st.number_input(
        "Account Number",
        min_value=1,
        step=1
    )

    amount = st.number_input(
        "Deposit Amount",
        min_value=0.0,
        step=100.0
    )

    if st.button(
        "💰 Deposit Money",
        use_container_width=True
    ):

        if amount <= 0:

            st.error(
                "Deposit amount must be greater than 0."
            )

        else:

            conn = get_connection()

            account = conn.execute(
                """
                SELECT
                    name,
                    balance
                FROM accounts
                WHERE account_no=?
                """,
                (int(account_no),)
            ).fetchone()

            if account:

                customer_name = account[0]
                old_balance = account[1]

                new_balance = old_balance + amount

                conn.execute(
                    """
                    UPDATE accounts
                    SET balance=?
                    WHERE account_no=?
                    """,
                    (
                        new_balance,
                        int(account_no)
                    )
                )

                conn.commit()

                st.success(
                    f"₹{amount:,.2f} deposited successfully! ✅"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Customer",
                        customer_name
                    )

                with col2:

                    st.metric(
                        "Deposited",
                        f"₹{amount:,.2f}"
                    )

                with col3:

                    st.metric(
                        "Updated Balance",
                        f"₹{new_balance:,.2f}"
                    )

            else:

                st.error(
                    "Account not found ❌"
                )

            conn.close()


# =========================================================
# WITHDRAW MONEY
# =========================================================

elif option == "💸 Withdraw Money":

    st.header("💸 Withdraw Money")

    account_no = st.number_input(
        "Account Number",
        min_value=1,
        step=1
    )

    amount = st.number_input(
        "Withdraw Amount",
        min_value=0.0,
        step=100.0
    )

    if st.button(
        "💸 Withdraw Money",
        use_container_width=True
    ):

        if amount <= 0:

            st.error(
                "Withdraw amount must be greater than 0."
            )

        else:

            conn = get_connection()

            account = conn.execute(
                """
                SELECT
                    name,
                    balance
                FROM accounts
                WHERE account_no=?
                """,
                (int(account_no),)
            ).fetchone()

            if account:

                customer_name = account[0]
                balance = account[1]

                if amount <= balance:

                    new_balance = balance - amount

                    conn.execute(
                        """
                        UPDATE accounts
                        SET balance=?
                        WHERE account_no=?
                        """,
                        (
                            new_balance,
                            int(account_no)
                        )
                    )

                    conn.commit()

                    st.success(
                        f"₹{amount:,.2f} withdrawn successfully! ✅"
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.metric(
                            "Customer",
                            customer_name
                        )

                    with col2:

                        st.metric(
                            "Withdrawn",
                            f"₹{amount:,.2f}"
                        )

                    with col3:

                        st.metric(
                            "Remaining Balance",
                            f"₹{new_balance:,.2f}"
                        )

                else:

                    st.error(
                        "Insufficient balance ❌"
                    )

            else:

                st.error(
                    "Account not found ❌"
                )

            conn.close()


# =========================================================
# PART 2 END
# =========================================================



# =========================================================
# UPDATE ACCOUNT
# =========================================================

elif option == "✏️ Update Account":

    st.header("✏️ Update Customer Account")

    account_no = st.number_input(
        "Account Number",
        min_value=1,
        step=1
    )

    st.info(
        "Enter the account number and update customer information."
    )

    # -----------------------------------------------------
    # Find Account
    # -----------------------------------------------------

    if st.button(
        "🔍 Find Account",
        use_container_width=True
    ):

        conn = get_connection()

        account = conn.execute(
            """
            SELECT
                account_no,
                name,
                mobile,
                email,
                address,
                account_type,
                balance,
                date_created
            FROM accounts
            WHERE account_no=?
            """,
            (int(account_no),)
        ).fetchone()

        conn.close()

        if account:

            st.session_state["update_account"] = account

        else:

            st.session_state["update_account"] = None

            st.error(
                "Account not found ❌"
            )

    # -----------------------------------------------------
    # Update Form
    # -----------------------------------------------------

    if "update_account" in st.session_state:

        account = st.session_state["update_account"]

        if account:

            st.success(
                f"Account {account[0]} found! ✅"
            )

            st.subheader("👤 Customer Information")

            with st.form("update_account_form"):

                col1, col2 = st.columns(2)

                with col1:

                    new_name = st.text_input(
                        "👤 Customer Name",
                        value=account[1]
                    )

                    new_mobile = st.text_input(
                        "📱 Mobile Number",
                        value=account[2],
                        max_chars=10
                    )

                    new_email = st.text_input(
                        "📧 Email Address",
                        value=account[3] or ""
                    )

                with col2:

                    new_address = st.text_area(
                        "🏠 Address",
                        value=account[4] or ""
                    )

                    account_types = [
                        "Savings",
                        "Current"
                    ]

                    current_type = (
                        account[5]
                        if account[5] in account_types
                        else "Savings"
                    )

                    new_account_type = st.selectbox(
                        "💳 Account Type",
                        account_types,
                        index=account_types.index(
                            current_type
                        )
                    )

                    st.metric(
                        "💰 Current Balance",
                        f"₹{account[6]:,.2f}"
                    )

                update_button = st.form_submit_button(
                    "💾 Save Changes",
                    use_container_width=True
                )

                if update_button:

                    if not new_name.strip():

                        st.error(
                            "Customer name cannot be empty."
                        )

                    elif (
                        len(new_mobile) != 10
                        or not new_mobile.isdigit()
                    ):

                        st.error(
                            "Mobile number must contain exactly 10 digits."
                        )

                    elif (
                        new_email
                        and "@" not in new_email
                    ):

                        st.error(
                            "Please enter a valid email address."
                        )

                    elif not new_address.strip():

                        st.error(
                            "Address cannot be empty."
                        )

                    else:

                        conn = get_connection()

                        conn.execute(
                            """
                            UPDATE accounts
                            SET
                                name=?,
                                mobile=?,
                                email=?,
                                address=?,
                                account_type=?
                            WHERE account_no=?
                            """,
                            (
                                new_name.strip(),
                                new_mobile,
                                new_email.strip(),
                                new_address.strip(),
                                new_account_type,
                                int(account_no)
                            )
                        )

                        conn.commit()

                        conn.close()

                        st.session_state.pop(
                            "update_account",
                            None
                        )

                        st.success(
                            "Account updated successfully! ✅"
                        )

                        st.rerun()


# =========================================================
# CHANGE ACCOUNT NUMBER
# =========================================================

elif option == "🔄 Change Account Number":

    st.header("🔄 Change Account Number")

    st.info(
        "Change the account number without changing "
        "customer information or balance."
    )

    col1, col2 = st.columns(2)

    with col1:

        old_account_no = st.number_input(
            "Current Account Number",
            min_value=1,
            step=1
        )

    with col2:

        new_account_no = st.number_input(
            "New Account Number",
            min_value=1,
            step=1
        )

    if st.button(
        "🔄 Change Account Number",
        use_container_width=True
    ):

        if old_account_no == new_account_no:

            st.error(
                "New account number must be different."
            )

        else:

            conn = get_connection()

            cursor = conn.cursor()

            # Check old account

            cursor.execute(
                """
                SELECT *
                FROM accounts
                WHERE account_no=?
                """,
                (int(old_account_no),)
            )

            old_account = cursor.fetchone()

            if not old_account:

                st.error(
                    f"Account {int(old_account_no)} not found ❌"
                )

            else:

                # Check new account number

                cursor.execute(
                    """
                    SELECT *
                    FROM accounts
                    WHERE account_no=?
                    """,
                    (int(new_account_no),)
                )

                existing = cursor.fetchone()

                if existing:

                    st.error(
                        f"Account number {int(new_account_no)} "
                        f"already exists ❌"
                    )

                else:

                    cursor.execute(
                        """
                        UPDATE accounts
                        SET account_no=?
                        WHERE account_no=?
                        """,
                        (
                            int(new_account_no),
                            int(old_account_no)
                        )
                    )

                    conn.commit()

                    st.success(
                        f"Account number changed successfully! "
                        f"{int(old_account_no)} → "
                        f"{int(new_account_no)} ✅"
                    )

            conn.close()


# =========================================================
# DELETE ACCOUNT
# =========================================================

elif option == "🗑️ Delete Account":

    st.header("🗑️ Delete Customer Account")

    st.warning(
        "⚠️ Deleting an account is permanent and cannot be undone."
    )

    account_no = st.number_input(
        "Account Number",
        min_value=1,
        step=1
    )

    # -----------------------------------------------------
    # CHECK ACCOUNT
    # -----------------------------------------------------

    if st.button(
        "🔍 Check Account",
        use_container_width=True
    ):

        conn = get_connection()

        account = conn.execute(
            """
            SELECT
                account_no,
                name,
                mobile,
                email,
                address,
                account_type,
                balance,
                date_created
            FROM accounts
            WHERE account_no=?
            """,
            (int(account_no),)
        ).fetchone()

        conn.close()

        if account:

            st.session_state["delete_account"] = account

        else:

            st.session_state["delete_account"] = None

            st.error(
                "Account not found ❌"
            )

    # -----------------------------------------------------
    # SHOW ACCOUNT DETAILS
    # -----------------------------------------------------

    if "delete_account" in st.session_state:

        account = st.session_state["delete_account"]

        if account:

            st.success(
                f"Account {account[0]} found! ✅"
            )

            st.subheader("👤 Account Details")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "🆔 Account Number",
                    account[0]
                )

            with col2:

                st.metric(
                    "👤 Customer",
                    account[1]
                )

            with col3:

                st.metric(
                    "💰 Balance",
                    f"₹{account[6]:,.2f}"
                )

            st.write(
                f"📱 **Mobile:** {account[2]}"
            )

            st.write(
                f"📧 **Email:** "
                f"{account[3] or 'Not provided'}"
            )

            st.write(
                f"🏠 **Address:** "
                f"{account[4] or 'Not provided'}"
            )

            st.write(
                f"💳 **Account Type:** {account[5]}"
            )

            st.write(
                f"📅 **Date Created:** {account[7]}"
            )

            st.divider()

            confirm = st.checkbox(
                "I confirm that I want to permanently delete this account."
            )

            if confirm:

                if st.button(
                    "🗑️ Permanently Delete Account",
                    use_container_width=True,
                    type="primary"
                ):

                    conn = get_connection()

                    cursor = conn.cursor()

                    cursor.execute(
                        """
                        DELETE FROM accounts
                        WHERE account_no=?
                        """,
                        (int(account[0]),)
                    )

                    conn.commit()

                    deleted = cursor.rowcount

                    conn.close()

                    if deleted == 1:

                        deleted_no = account[0]

                        st.session_state.pop(
                            "delete_account",
                            None
                        )

                        st.success(
                            f"Account {deleted_no} "
                            f"deleted successfully! ✅"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Account could not be deleted ❌"
                        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        🏦 <b>Bank Management System</b>

        <br><br>

        Python + SQLite + Streamlit

        <br>

        Secure Customer Account Management

        <br><br>

        Developed by <b>Sunny Thakur</b> 💫

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# END OF APPLICATION
# =========================================================