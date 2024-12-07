# Импортируем модуль sender_stand_request, содержащий функции для отправки HTTP-запросов к API.
import sender_stand_request

# Импортируем модуль data, в котором определены данные, необходимые для HTTP-запросов.
import data

# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1


# Функция для негативной проверки
def negative_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert user_response.status_code == 400

    # Строка, которая должна быть в ответе
    str_user = {"code": 400,
                "message": "Имя пользователя введено некорректно. Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
    }

    assert user_response.json() == str_user

# Функция 2 для негативной проверки
def negative_assert_no_parametr(first_name):
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(data.user_body_no_first_name)

    # Проверяется, что код ответа равен 400
    assert user_response.status_code == 400

    # Строка, которая должна быть в ответе
    str_user = {"code": 400,
                "message": "Не все необходимые параметры были переданы"
    }

    assert user_response.json() == str_user
    print (user_response.json())
    print (data.user_body_no_first_name)

# Функция 3 для негативной проверки
def negative_assert_null_parametr(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert user_response.status_code == 400

    # Строка, которая должна быть в ответе
    str_user = {"code": 400,
                "message": "Не все необходимые параметры были переданы"
    }

    assert user_response.json() == str_user
    print (user_response.json())
    print (user_body)

# Функция 4 для негативной проверки
def negative_assert_type(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert user_response.status_code == 400

    print (user_response.json())
    print (user_body)

# Тест 1. Успешное создание пользователя
# Параметр firstName состоит из 2 символов

#@pytest.mark.parametrize ('first_name', [
 #   pytest.param("Aa", id='2 символа'),
  #  pytest.param("Ааааааааааааааа", id='15 символов')
#])

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. Успешное создание пользователя
# Параметр firstName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

# Тест 3. Неуспешное создание пользователя
# Парамер firstName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_no_success_response():
    negative_assert("А")


# Тест 4. Неуспешное создание пользователя
# Парамер firstName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_no_success_response():
    negative_assert("Аааааааааааааааа")

# Тест 5. Успешное создание пользователя
# Параметр firstName состоит из английских букв
def test_create_user_en_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Успешное создание пользователя
# Параметр firstName состоит из русских букв
def test_create_user_ru_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Неуспешное создание пользователя
# Парамер firstName содержит пробелы
def test_create_user_probel_in_first_name_get_no_success_response():
    negative_assert("Человек и Ко")

# Тест 8. Неуспешное создание пользователя
# Парамер firstName содержит символы
def test_create_user_symbol_in_first_name_get_no_success_response():
    negative_assert("№%@")

# Тест 9. Неуспешное создание пользователя
# Парамер firstName содержит цифры
def test_create_user_number_in_first_name_get_no_success_response():
    negative_assert("123")

# Тест 10. Неуспешное создание пользователя
# Парамер firstName отсутствует
def test_create_user_no_first_name_get_no_success_response():
    negative_assert_no_parametr('')

# Тест 11. Неуспешное создание пользователя
# Парамер firstName содержит пустое значение
def test_create_user_null_first_name_get_no_success_response():
    negative_assert_null_parametr('')

# Тест 12. Неуспешное создание пользователя
# Парамер firstName другого типа
def test_create_user_type_first_name_get_no_success_response():
    negative_assert_type(12)