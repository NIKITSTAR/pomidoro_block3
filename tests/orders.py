import datetime

OPERATOR = ("mail@mail.ru", "Никита")

orders = {
    "state": 0,
    "data": [
        {
            "_id": "3d8c861f-e2c0-442a-9d82-810ae5eb5f52",
            "count": 1,
            "brand_id": 84375,
            "delay": 1,
            "startedAt": "2024-03-21T16:48:03.513Z",
            "completedAt": "2024-03-21T16:48:03.513Z",
            "completed": 0,
            "wait_refund": 0,
            "refunded": 0
        },
        {
            "_id": "4816385b-a5a5-4341-aedf-6f80bedbdce4",
            "count": 2,
            "brand_id": 88339,
            "delay": 2,
            "startedAt": "2024-03-21T16:27:32.062Z",
            "completedAt": "2024-03-21T16:28:32.062Z",
            "completed": 0,
            "wait_refund": 2,
            "refunded": 0
        },
        {
            "_id": "7e0882b5-38b8-4dcb-9825-625158a92314",
            "count": 16,
            "brand_id": 88339,
            "delay": 3,
            "startedAt": "2024-03-21T16:17:04.723Z",
            "completedAt": "2024-03-21T16:17:04.723Z",
            "completed": 7,
            "wait_refund": 3,
            "refunded": 6
        }
    ]
}

def test_orders():
    """
    Тестирует корректность данных заказов и логику их обработки.

    Шаги тестирования:
      1) Проверяет, что состояние заказов равно 0 и что список заказов не пуст.
      2) Для первых двух заказов проверяет, что разница между временем завершения и начала не превышает 6 часов.
      3) Для третьего заказа проверяет, что сумма выполненных, возвращенных и ожидающих возврата услуг равна общему количеству,
         а также что выполняется хотя бы одно из условий:
           - выполнено не менее половины услуг;
           - количество возвращенных не превышает выполненных, а ожидающих возврата не превышает возвращенных.
      4) Вызывает функцию main() для формирования и вывода отчёта.
    """
    # 1) Проверяем, что заказы есть
    assert orders["state"] == 0
    assert len(orders["data"]) > 0

    # 2) Проверяем время первых двух заказов
    for i in range(min(2, len(orders["data"]))):
        order = orders["data"][i]
        started_at = datetime.datetime.fromisoformat(order["startedAt"].replace('Z', '+00:00'))
        completed_at = datetime.datetime.fromisoformat(order["completedAt"].replace('Z', '+00:00'))
        assert completed_at - started_at <= datetime.timedelta(hours=6)

    # 3) Проверяем третий заказ
    if len(orders["data"]) >= 3:
        third = orders["data"][2]
        c, r, w = third["completed"], third["refunded"], third["wait_refund"]
        assert c + r + w == third["count"], "Не все услуги учтены"
        condition1 = c >= third["count"] / 2
        condition2 = (r <= c) and (w <= r)
        assert condition1 or condition2, "Не выполнено ни одно условие"

    # 4) Вызов main() — чтобы увидеть отчёт при запуске pytest -s
    main()


def main():
    """Формируем и печатаем отчёт."""
    report = make_report()
    print("=== ОТЧЁТ ===")
    print("Оператор:", report["operator"])
    print("ID заказов:", report["order_ids"])
    print("Суммарная статистика услуг:", report["summary"])


def make_report():
    """Генерация финального отчёта."""
    # Собираем ID
    order_ids = [o["_id"] for o in orders["data"]]
    order_ids.append("326b23a1-e6ab-4b4a-84a1-a3ecb33afc97")

    # Считаем суммы
    total_completed = 0
    total_refunded = 0
    total_wait_refund = 0
    for o in orders["data"]:
        total_completed += o["completed"]
        total_refunded += o["refunded"]
        total_wait_refund += o["wait_refund"]

    summary = {
        "completed": total_completed,
        "refunded": total_refunded,
        "wait_refund": total_wait_refund
    }

    return {
        "operator": OPERATOR,
        "order_ids": order_ids,
        "summary": summary
    }


