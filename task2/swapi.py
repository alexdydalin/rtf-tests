import time
import os
import requests
import openpyxl


# Функция для получения всех персонажей
def get_all_characters():
    start_time = time.time()  # Начало измерения времени для данной функции

    all_characters = []
    url = 'https://swapi.dev/api/people/' # Начальная точка запроса

    # Данный цикл выполняется пока есть следующая страница с данными
    while True:
        response = requests.get(url) # Получение всех персонажей на текущей странице
        data = response.json()

        # Добавляем полученные персонажи в список
        all_characters.extend(data['results'])

        # Проверка на наличие следующей страницы
        if data['next']:
            url = data['next']
        else:
            break

    end_time = time.time()  # Окончание измерения времени
    print(f"Время выполнения функции get_all_characters: {end_time - start_time:.2f} секунд")

    return all_characters


# Функция для сохранения данных в Excel
def save_to_excel(characters, filename='characters.xlsx'):
    start_time = time.time()  # Начало измерения времени

    # Создание нового Excel файла и листа для записи
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Заголовки столбцов
    headers = ['Name', 'Height', 'Mass', 'Hair Color', 'Skin Color', 'Eye Color', 'Birth Year', 'Gender', 'Homeworld']
    sheet.append(headers)

    # Функция для получения названия планеты по ссылке из ответа API, время работы примерно 25 секунд для всех персонажей
    '''
    def get_planet_name(homeworld_url):
        try:
            response = requests.get(homeworld_url)
            planet_data = response.json()
            return planet_data.get("name", "Планета неизвестна")
        except:
            return "Ошибка :("
    '''


    # Заполнение строк данными
    for character in characters:
        # homeworld_name = get_planet_name(character['homeworld'])
        row_data = [
            character['name'],
            character['height'],
            character['mass'],
            character['hair_color'],
            character['skin_color'],
            character['eye_color'],
            character['birth_year'], # у.е. это BBY (Before the Battle of Yavin)
            character['gender'],
            character['homeworld'] # homeworld_name
        ]
        sheet.append(row_data)

    # Проверка существования файла с таким же именем и переименование если оно требуется
    if os.path.exists(filename):
        i = 1
        while os.path.exists(f'{filename[:-5]}_{i}.xlsx'):
            i += 1
        filename = f'{filename[:-5]}_{i}.xlsx'

    # Сохранение файла
    workbook.save(filename)

    end_time = time.time()  # Окончание измерения времени
    print(f"Время выполнения функции save_to_excel: {end_time - start_time:.2f} секунд")


if __name__ == "__main__":
    start_time_total = time.time()  # Начало измерения времени для данной функции

    characters = get_all_characters()[:82]  # Получение первых 82 персонажей
    save_to_excel(characters)

    end_time_total = time.time()  # Окончание общего измерения времени

    # Воемя работы программы в среднем составляет примерно 4.6 секунды
    print(f"Общее время выполнения программы: {end_time_total - start_time_total:.2f} секунд")