from constant import BASE_URL
from tests.conftest import booking_data_change


class TestBookings:
    """
    Класс для тестирования функциональности бронирования.

    Содержит методы для проверки создания, обновления (PUT, PATCH) и удаления бронирований,
    а также проверки получения бронирований по различным критериям.
    """

    def test_create_booking(self, booking_data, auth_session):
        """
        Тестирует процесс создания, получения и удаления бронирования.

        Шаги теста:
          - Создание бронирования с использованием данных booking_data.
          - Проверка, что бронирование успешно создано (статус 200) и получен корректный booking_id.
          - Получение созданного бронирования и проверка соответствия данных (firstname, lastname, totalprice, depositpaid, bookingdates).
          - Удаление бронирования и проверка, что бронирование удалено (статус 201 и последующий статус 404 при попытке получить его).

        Аргументы:
            booking_data (dict): Словарь с данными для создания бронирования.
            auth_session: Сессия авторизованного пользователя для отправки HTTP запросов.
        """
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID букинга не найден в ответе"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200

        booking_data_response = get_booking.json()
        assert booking_data_response['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_data['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"

    def test_put_patch_getnoid(self, booking_data, booking_data_change, booking_data_patch, auth_session):
        """
        Тестирует обновление бронирования с использованием методов PUT и PATCH, а также получение бронирований без указания ID.

        Шаги теста:
          - Создание нового бронирования с данными booking_data.
          - Обновление бронирования через PUT с данными booking_data_change и проверка соответствия обновлённых данных.
          - Попытка обновления через PUT без обязательных полей; ожидается статус 400.
          - Попытка обновления через PUT с неверными типами данных; ожидается статус 500.
          - Обновление бронирования через PATCH с данными booking_data_patch и проверка соответствия обновлённых данных.
          - Выполнение PATCH запроса с пустым телом, данные должны остаться без изменений.
          - Выполнение PATCH запроса с несуществующими данными, проверка, что данные не изменились.
          - Получение списка бронирований без указания ID и с фильтрацией по firstname и lastname.

        Аргументы:
            booking_data (dict): Словарь с начальными данными бронирования.
            booking_data_change (dict): Словарь с данными для обновления через PUT.
            booking_data_patch (dict): Словарь с данными для обновления через PATCH.
            auth_session: Сессия авторизованного пользователя для отправки HTTP запросов.
        """
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        booking_id = create_booking.json().get("bookingid")
        # Проверка обновления данных через PUT
        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=booking_data_change)
        assert put_booking.status_code == 200
        get_put_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        booking_data_response = get_put_booking.json()
        assert booking_data_response['firstname'] == booking_data_change['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data_change['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_data_change['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_data_change['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_data_change['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_data_change['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

        # Проверка обновления данных через PUT без обязательных полей
        put_booking_again = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json={
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
})
        assert put_booking_again.status_code == 400

        # Проверка обновления данных через PUT с неверными типами данных
        put_booking_again = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json={"firstname": "Richard",
        "lastname": 2,
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        })
        assert put_booking_again.status_code == 500


        #Проверка PATCH
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=booking_data_patch)
        assert patch_booking.status_code == 200
        get_patch_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        booking_data_response = get_patch_booking.json()
        assert booking_data_response['firstname'] == booking_data_patch['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data_patch['lastname'], "Фамилия не совпадает с заданной"

        # Проверка PATCH с пустым телом (данные должны остаться без изменения)
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json={})
        assert patch_booking.status_code == 200
        get_patch_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_patch_booking.json() == {'firstname': 'Richard', 'lastname': 'Gentle', 'totalprice': 999, 'depositpaid': True, 'bookingdates': {'checkin': '2024-04-05', 'checkout': '2024-04-08'}, 'additionalneeds': 'Dinner'}

        #Проверка PATCH с не существующими данными
        patch_booking = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json={"proverka": 345})
        assert patch_booking.status_code == 200
        assert get_patch_booking.json() == {'firstname': 'Richard', 'lastname': 'Gentle', 'totalprice': 999,
                                            'depositpaid': True,
                                            'bookingdates': {'checkin': '2024-04-05', 'checkout': '2024-04-08'},
                                            'additionalneeds': 'Dinner'}

        #Проверка Get (без ID)
        getnoid_booking = auth_session.get(f"{BASE_URL}/booking/")
        assert getnoid_booking.status_code == 200
        #Проверка Get с ключами
        getnoidkey_booking = auth_session.get(f"{BASE_URL}/booking/?firstname={booking_data_response['firstname']}&lastname={booking_data_response['lastname']}")
        assert getnoidkey_booking.status_code == 200
