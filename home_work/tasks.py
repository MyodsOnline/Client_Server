"""
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
и также проверить тип и содержимое переменных.
"""

strings_list = ['разработка', 'сокет', 'декоратор']
strings_list_unicode = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                        '\u0441\u043e\u043a\u0435\u0442',
                        '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']
strings_dict = {}


def string_checker(str_1, str_2):
    for (i, j) in zip(str_1, str_2):
        print(type(i), type(j), i == j)

    for el in range(len(str_1)):
        strings_dict[str_1[el]] = str_2[el]
    print(strings_dict)


string_checker(strings_list, strings_list_unicode)
