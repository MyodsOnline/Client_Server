"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке
ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с
помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import yaml

test_dict = {
    'Ǎ': ['one', 2, True],
    'Ǽ': 100500,
    'Ⱥ': {'one': 1, 'two': 2, 'three': 3},
}
path = 'data/file.yaml'


def yaml_dict(path, test_dict):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(test_dict, f, default_flow_style=False, allow_unicode=True)

    with open(path, 'r', encoding='utf-8') as f:
        dict_from_yaml = yaml.load(f, Loader=yaml.FullLoader)

    print(f'===Исходные данные===\n{test_dict}\nтип - {type(test_dict)}\n')
    print(f'===Данные из yaml===\n{dict_from_yaml}\nтип - {type(dict_from_yaml)}\n')
    print(f'===Словари совпадают?===\n{dict_from_yaml == test_dict}')


yaml_dict(path, test_dict)
