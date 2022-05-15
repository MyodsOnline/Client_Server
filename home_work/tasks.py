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


# string_checker(strings_list, strings_list_unicode)

"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо в автоматическом, а не 
ручном режиме, с помощью добавления литеры b к текстовому значению, (т.е. ни в коем случае не используя методы encode, 
decode или функцию bytes) и определить тип, содержимое и длину соответствующих переменных.
"""
list_2 = ['t_class', 't_function', 't_method']


def str_to_bytes(*args):
    data = ['class', 'function', 'method'] if not args else list(args[0])
    for el in data:
        el = eval("b" + "'" + el + "'")
        print(el, type(el), len(el))


# str_to_bytes(list_2)

"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе. 
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""


def check_str_to_bytes(*args):
    data = ['attribute', 'класс', 'функция', 'type'] if not args else list(args)
    for el in data:
        try:
            el = eval("b" + "'" + el + "'")
            print(el, type(el), len(el))
        except SyntaxError:
            print(f'"{el}" - is not in ASCII. Use .encode()')


# check_str_to_bytes()

"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в 
байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

list_4 = ['разработка', 'администрирование', 'protocol', 'standard']


def list_encode_decode(data):
    def list_encode(elem):
        return str(elem).encode('utf-8')
    encoded_list = (list(map(list_encode, data)))

    def list_decode(elem):
        return elem.decode('utf-8')
    decoded_list = (list(map(list_decode, encoded_list)))

    print(f'Encoding list - {encoded_list}')
    print(f'Decoding list - {decoded_list}')


# list_encode_decode(input('type text with spaces: ').split())
# list_encode_decode(list_4)

"""
5. Написать код, который выполняет пинг веб-ресурсов yandex.ru, youtube.com и преобразовывает результат из байтовового 
типа данных в строковый без ошибок для любой кодировки операционной системы.
"""

"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», 
«декоратор». Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл в 
неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""
