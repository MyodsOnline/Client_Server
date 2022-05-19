"""
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json


def write_order_to_json(item, quantity, price, buyer, date):
    file = 'data/orders.json'

    with open(file, encoding='utf-8') as f:
        orders = json.load(f)

        order_data = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date,
        }
        orders['orders'].append(order_data)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(orders, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    write_order_to_json('test_item', 'test_quantity', 'test_price', 'test_buyer', 'test_date')
