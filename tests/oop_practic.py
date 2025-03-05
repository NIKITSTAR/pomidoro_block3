class BankAccount:
    """
    Класс, представляющий банковский счет.

    Атрибуты:
        owner (str): Владелец счета.
        __balance (float): Текущий баланс счета (закрытый атрибут).
    """
    def __init__(self, owner: str, balance: float = 0) -> None:
        """
        Инициализирует банковский счет с заданным владельцем и начальным балансом.

        Args:
            owner (str): Имя владельца счета.
            balance (float, optional): Начальный баланс счета. По умолчанию 0.
        """
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount: float) -> None:
        """
        Вносит депозит на счет.

        Args:
            amount (float): Сумма депозита. Должна быть положительной.

        Raises:
            ValueError: Если сумма депозита не является положительной.
        """
        if amount <= 0:
            raise ValueError("Сумма для депозита должна быть положительной!")
        self.__balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Снимает указанную сумму со счета, если хватает средств.

        Args:
            amount (float): Сумма для снятия. Должна быть положительной.

        Raises:
            ValueError: Если сумма для снятия не положительная
                        или если недостаточно средств.
        """
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной!")
        if amount > self.__balance:
            raise ValueError("Недостаточно средств!")
        self.__balance -= amount

    def get_balance(self) -> float:
        """
        Возвращает текущий баланс счета.

        Returns:
            float: Текущий баланс счета.
        """
        return self.__balance


class SavingsAccount(BankAccount):
    """
    Класс сберегательного счета, наследующийся от BankAccount.

    Атрибуты:
        interest_rate (float): Процентная ставка (5% годовых по умолчанию).
    """
    interest_rate = 0.05  # 5% годовых

    def apply_interest(self) -> None:
        """
        Применяет процентную ставку к текущему балансу счета.
        Баланс увеличивается пропорционально interest_rate.
        """
        current_balance = self.get_balance()
        # доступ к приватному атрибуту через _BankAccount__balance
        self._BankAccount__balance = current_balance * (1 + self.interest_rate)


class CheckingAccount(BankAccount):
    """
    Класс текущего счета, наследующийся от BankAccount, с модифицированным методом снятия.
    """
    def withdraw(self, amount: float) -> None:
        """
        Снимает указанную сумму со счета без проверки достаточности средств.

        Args:
            amount (float): Сумма для снятия. Должна быть положительной.

        Raises:
            ValueError: Если сумма для снятия не положительная.
        """
        if amount <= 0:
            raise ValueError("Сумма для снятия должна быть положительной!")
        self._BankAccount__balance -= amount


def test_bank() -> None:
    """
    Тест функциональности сберегательного счета (SavingsAccount).
    Проверяет внесение депозита, снятие средств, начисление процентов и итоговый баланс.
    """
    savings_account = SavingsAccount("Никита", 0)
    savings_account.deposit(500)
    savings_account.withdraw(100)
    savings_account.apply_interest()
    assert savings_account.get_balance() > 0
    print(f"Баланс счета: {savings_account.get_balance()}")
