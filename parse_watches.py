import requests
from bs4 import BeautifulSoup
import csv
import time


def get_watch_data(item):
    try:
        # Отримання назви годинника
        name_tag = item.find('a', class_='item-title')
        name = name_tag.get_text(strip=True) if name_tag else 'Невідомо'

        # Отримання характеристик
        specs_tag = item.find('div', class_='specs__text')
        specs = {}
        if specs_tag:
            spec_items = specs_tag.find_all('span', class_='spec-item')
            for spec in spec_items:
                text = spec.get_text(strip=True)
                if 'Годинниковий механізм:' in text:
                    specs['Годинниковий механізм'] = text.split(':')[-1].strip()
                elif 'Матеріал корпусу:' in text:
                    specs['Матеріал корпусу'] = text.split(':')[-1].strip()
                elif 'Скло:' in text:
                    specs['Скло'] = text.split(':')[-1].strip()
                elif 'Розмір корпусу, мм:' in text:
                    specs['Розмір корпусу, мм'] = text.split(':')[-1].strip()
                elif 'Рік' in text:
                    specs['Рік'] = text.replace('Рік', '').strip()

        # Формування результату
        description = f"-- Назва: {name} --"
        for key, value in specs.items():
            if value:
                description += f"{key}: {value}"

        # Надсилання даних на сервер
        data = {
            "name": name,
            "specs": specs
        }
        response = requests.post('https://mockend.com/IuraDemian/scraping2023/Items', json=data)

        if response.status_code == 201:
            print(f"Дані для '{name}' успішно надіслані.")
        else:
            print(f"Помилка при надсиланні даних для '{name}': {response.status_code}")

        return description
    except Exception as e:
        print(f"Помилка при обробці годинника: {e}")
        return None


def main():
    base_url = "https://hotline.ua/watches/naruchnye-chasy/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    for page in range(1, 21):  # Перебір сторінок до 20
        url = f"{base_url}?p={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Знайдемо всі годинники на сторінці
        items = soup.find_all('div', class_='list-item list-item--row')

        if not items:
            break  # Вихід якщо більше немає товарів

        for item in items:
            get_watch_data(item)
            time.sleep(0.5)  # Затримка між запитами для уникнення блокування


if __name__ == "__main__":
    main()
