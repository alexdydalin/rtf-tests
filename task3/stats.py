import pandas as pd
import numpy as np

# Чтение данных из файла предыдущего задания
df = pd.read_excel("characters.xlsx")

# Преобразуем высоту и массу в числовые значения, игнорируя недопустимые значения
# errors='coerce' заменят то что нельзя преобразовать в значениена на nan
df["Height"] = pd.to_numeric(df["Height"], errors='coerce')
df["Mass"] = pd.to_numeric(df["Mass"], errors='coerce')

# Удаляем строки с пропущенными значениями для высоты и массы
df.dropna(subset=["Height", "Mass"], inplace=True)

# 1 Максимальный, минимальный и средний элемент высоты
max_height = df["Height"].max()
min_height = df["Height"].min()
avg_height = df["Height"].mean()

# 2 Максимальный, минимальный и средний элемент массы
max_mass = df["Mass"].max()
min_mass = df["Mass"].min()
avg_mass = df["Mass"].mean()

# 3 Наиболее популярный цвет волос
popular_hair_color = df["Hair Color"].value_counts().index[0]
if str(popular_hair_color) == 'none':
    popular_hair_color = df["Hair Color"].value_counts().index[1]

# 4 Наименее популярный цвет кожи
least_popular_skin_color = df["Skin Color"].value_counts().tail(1).index[0]
if str(least_popular_skin_color) == 'none':
    least_popular_skin_color = df["Skin Color"].value_counts().tail(2).index[-1]

# 5. Количество персонажей по цвету глаз
eyes_count = df["Eye Color"].value_counts()

# 6. Самый высокий персонаж среди женщин
female_df = df.query("Gender == 'female'")
if len(female_df) > 0 and "Height" in female_df.columns:
    tallest_female = female_df.sort_values(by="Height", ascending=False)["Name"].values[0]
else:
    tallest_female = "Нет данных"


# 7 Самый старый персонаж среди мужчин
male_df = df.query("Gender == 'male' & `Birth Year` != 'unknown'")

if len(male_df) > 0 and "Birth Year" in male_df.columns:
    # Очищаем строку от 'BBY' и приводим к float
    male_df.loc[:, 'Birth Year'] = male_df['Birth Year'].str.replace('BBY', '').astype(float)

    # Проверяем есть ли данные после сортировки, учитываем что год рождения до определенного события поэтому сортируем в обратном порядке
    sorted_males = male_df.sort_values(by="Birth Year", ascending=False)
    oldest_male = sorted_males["Name"].values[0]
else:
    oldest_male = "Нет данных"


# 8 Наиболее популярная планета рождения персонажей
most_popular_birth_planet = df["Homeworld"].value_counts().index[0]

# Выведем результаты
print(f"Максимальная высота: {max_height}")
print(f"Минимальная высота: {min_height}")
print(f"Средняя высота: {avg_height:.2f}")

print(f"Максимальная масса: {max_mass}")
print(f"Минимальная масса: {min_mass}")
print(f"Средняя масса: {avg_mass:.2f}")

print(f"Наиболее популярный цвет волос: {popular_hair_color}")
print(f"Наименее популярный цвет кожи: {least_popular_skin_color}")

print("\nКоличество персонажей по цвету глаз:")
for eye_color, count in eyes_count.items():
    print(f"{eye_color}: {count}")

print(f"\nСамый высокий женский персонаж: {tallest_female}")
print(f"Самый старый мужской персонаж: {oldest_male}")

print(f"Наиболее популярная планета рождения: {most_popular_birth_planet}")