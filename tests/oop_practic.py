
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Сумма для депозита должна быть положительной!")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной!")
        if amount > self.__balance:
            raise ValueError("Недостаточно средств!")
        self.__balance -= amount

    def get_balance(self):
        return self.__balance


class SavingsAccount(BankAccount):
    interest_rate = 0.05  # 5% годовых

    def apply_interest(self):
        current_balance = self.get_balance()
        self._BankAccount__balance = current_balance * (1 + self.interest_rate)


class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной!")
        self._BankAccount__balance -= amount

def test_bank():
    savings_account = SavingsAccount("Никита", 0)
    savings_account.deposit(500)
    savings_account.withdraw(100)
    savings_account.apply_interest()
    assert savings_account.get_balance() > 0
    print(f"Баланс счета {savings_account.get_balance()}")

