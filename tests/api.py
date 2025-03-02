from constant import BASE_URL
from tests.conftest import booking_data_change


class TestBookings:

    def test_create_booking(self, booking_data, auth_session):
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
