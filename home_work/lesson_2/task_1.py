"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""
import csv
import re
import chardet

sources = ['data/info_1.txt', 'data/info_2.txt', 'data/info_3.txt']


def get_data(sources):

    os_list = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    for file in sources:
        with open(file, 'rb') as f:
            f_data = f.read()
            charset = chardet.detect(f_data)['encoding']
            f_text = f_data.decode(encoding=charset)

            el_os_prod_list = re.search(r'Изготовитель ОС:\s+([\w\s]+)\r\n', f_text)
            el_os_name_list = re.search(r'Название ОС:\s+([\w\.\s]+)\r\n', f_text)
            el_os_code_list = re.search(r'Код продукта:\s+([\w\-\s]+)\r\n', f_text)
            el_os_type_list = re.search(r'Тип системы:\s+([\w\-\s]+)\r\n', f_text)

            os_prod_list.append(el_os_prod_list[1])
            os_name_list.append(el_os_name_list[1])
            os_code_list.append(el_os_code_list[1])
            os_type_list.append(el_os_type_list[1])

    for el in range(len(os_prod_list)):
        os_list.append([os_prod_list[el], os_name_list[el], os_code_list[el], os_type_list[el]])

    return os_list


def write_to_csv(file_name, sources):
    data_os_list = get_data(sources)
    with open(file_name, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        f_writer.writerows(data_os_list)


write_to_csv('data/task_1.csv', sources)
