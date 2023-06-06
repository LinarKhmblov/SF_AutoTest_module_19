from api import PetFriends
from settings import valid_email, valid_password
import os
import string
import random

#  генерация случайной строки для тестовых данных, param: k= указать длину строки
ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=256))

#  генерация случайной последовательности чисел param, для тестовых данных: range(указать кол-во последовательности)
sequence = int(''.join(random.choice('0123456789') for _ in range(1000)))

pf = PetFriends()


def test_get_api_key_for_invalid_user(email: str = 'if_false@NONE.com', password: str = valid_password):
    """Проверяем запрос с невалидным email и с валидным password.
    Проверяем наличие ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с ожидаемым результатом
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует в ответе'


def test_get_api_key_for_invalid_password(email: str = valid_email, password: str = 'password'):
    """Проверяем запрос с невалидным password и с валидным email.
    Проверяем наличие ключа в ответе"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с ожидаемым результатом
    assert status == 403
    assert 'key' not in result, 'Ключ отсутствует в ответе'

def test_update_self_pet_empty_data(name: any = '', animal_type: any = '', age: any = ''):
    """Проверка негативного сценария.
    Поля для ввода оставляем пустыми."""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом, поля ввода не должны принимать пустые строки
    assert status == 200
    assert result['name'] != '', 'Поле имя не должно быть пустым'
    assert result['animal_type'] != '', 'Поле порода не должно быть пустым'
    assert result['age'] != '', 'Поле возраст не должно быть пустым'

def test_update_self_pet_incorrect_name_str(name: str = ran, animal_type: str = 'Cat', age: int = 5):
    """Проверка негативного сценария.
    Поле имя не должно принимать на ввод более 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['name']) <= 255, 'Допустимая длина строки 255 символов'

    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")


def test_update_self_pet_incorrect_name_int(name: int = 4, animal_type: str = 'Пёс', age: int = 10):
    """Проверка с негативным сценарием.
   Не допустим ввод цифр в поле имя"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, обновляем информацию о питомце: имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200, имя питомца указано в буквенном значении
        assert status == 200
        assert result['name'].isalpha(), 'Имя животного не может быть цифрой'
    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")


def test_update_self_pet_incorrect_animal_type(name: str = 'Борис', animal_type: str = ran, age: int = 15):
    """Проверка с негативным сценарием.
     Поле порода не должно принимать на вход более 255 символов"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['animal_type']) <= 255, 'Допустимая длина строки 255 символов'

    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")


def test_update_self_pet_incorrect_age(name: str = 'Болик', animal_type: str = 'скандинав', age: int = 101):
    """Негативное тестирование поля возраст.
    Поле возраст не должно принимать цифру больше двухзначного значения"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Сверяем полученный ответ с ожидаемым результатом
        assert status == 200
        assert len(result['age']) < 3, 'Возраст животного не может быть трехзначной цифрой'

    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")

def test_update_self_pet_incorrect_animal_type_int(name: str = 'Джейми', animal_type: int = 1, age: int = 1):
    """Проверка негативного сценария.
      Не допустим ввод цифр в поле порода."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список питомцев пустой, на выход получаем исключение с сообщением
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200, вид питомца указан в буквенном значении
        assert status == 200
        assert result['animal_type'].isalpha(), 'Поле порода не должно содержать цифр'
    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")


def test_update_self_pet_photo_txt_format(pet_photo: str = 'images/image.txt'):
    """Проверка негативного сценария.
    При загрузке фото использование файла в формате txt, вместо изображения"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 500, 'Загружен файл в неверном формате'
    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")


def test_update_self_pet_photo_png(pet_photo: str = 'images/ape.png'):
    """Проверка позитивного сценария.
    Возможность обновления фото в формате png"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем что статус ответа = 200
        assert status == 200, 'Формат png не поддерживается'
    else:
        # Если список питомцев пустой, на выход получаем исключение с сообщением
        raise Exception("Нет созданных питомцев")






