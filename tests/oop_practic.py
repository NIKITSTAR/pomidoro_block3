class BankAccount:
    """
    Класс, представляющий банковский счет.

    Атрибуты:
        owner (str): Владелец счета.
        __balance (int, float): Текущий баланс счета (закрытый атрибут).
    """
    def __init__(self, owner, balance=0):
        """
        Инициализирует банковский счет с заданным владельцем и начальным балансом.

        args:
            owner (str): Имя владельца счета.
            balance (int, float, optional): Начальный баланс счета. По умолчанию 0.
        """
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        """
        Вносит депозит на счет.

        args:
            amount (int, float): Сумма депозита. Должна быть положительной.

        Возбуждает:
            ValueError: Если сумма депозита не является положительной.
        """
        if amount > 0:
            self.__balance += amount
        else:
            raise ValueError("Сумма для депозита должна быть положительной!")

    def withdraw(self, amount):
        """
        Снимает указанную сумму со счета, если хватает средств.

        args:
            amount (int, float): Сумма для снятия. Должна быть положительной.

        Возбуждает:
            ValueError: Если сумма для снятия не положительная или если недостаточно средств.
        """
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной!")
        if amount > self.__balance:
            raise ValueError("Недостаточно средств!")
        self.__balance -= amount

    def get_balance(self):
        """
        Возвращает текущий баланс счета.

        Возвращает:
            int, float: Текущий баланс счета.
        """
        return self.__balance


class SavingsAccount(BankAccount):
    """
    Класс сберегательного счета, наследующийся от BankAccount.

    Атрибуты:
        interest_rate (float): Процентная ставка (5% годовых по умолчанию).
    """
    interest_rate = 0.05  # 5% годовых

    def apply_interest(self):
        """
        Применяет процентную ставку к текущему балансу счета, увеличивая его.
        """
        current_balance = self.get_balance()
        self._BankAccount__balance = current_balance * (1 + self.interest_rate)


class CheckingAccount(BankAccount):
    """
    Класс текущего счета, наследующийся от BankAccount, с модифицированным методом снятия.
    """
    def withdraw(self, amount):
        """
        Снимает указанную сумму со счета без проверки достаточности средств.

        args:
            amount (int, float): Сумма для снятия. Должна быть положительной.

        Возбуждает:
            ValueError: Если сумма для снятия не положительная.
        """
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной!")
        self._BankAccount__balance -= amount

def test_bank():
    """
    Тестирует функциональность сберегательного счета:
      - Создает счет SavingsAccount.
      - Вносит депозит, снимает средства и применяет процентную ставку.
      - Проверяет, что итоговый баланс больше 0.
      - Выводит итоговый баланс.
    """
    savings_account = SavingsAccount("Никита", 0)
    savings_account.deposit(500)
    savings_account.withdraw(100)
    savings_account.apply_interest()
    assert savings_account.get_balance() > 0
    print(f"Баланс счета {savings_account.get_balance()}")


