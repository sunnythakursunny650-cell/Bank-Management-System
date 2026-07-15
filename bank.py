class Bank:

    def __init__(self, account_no, name, mobile, balance):
        self.account_no = account_no
        self.name = name
        self.mobile = mobile
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False