from datetime import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        date_time = datetime.now()
        str_time = date_time.strftime('%d-%m-%Y \nВремя вызова функции %H:%M:%S')
        function_name = old_function.__name__
        result = old_function(*args, **kwargs)
        with open('test3.log', 'a', encoding='utf-8') as file:
            file.write(f'\nДата вызова функции: {str_time}\n'
                       f'имя функции: {function_name}\n'
                       f'Аргументы: {args, kwargs}\n'
                       f'Возвращаемое значение - {result}\n'
                       f'{"-" * 85}'
                       )
        return result

    return new_function


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.item = []
        self.next_list = iter(self.list_of_list)
        return self

    def __next__(self):
        while True:
            try:
                self.next_element = next(self.next_list)  # получение следующего элемента
            except StopIteration:
                if not self.item:
                    raise StopIteration  # завершение цикла при отсутствии элементов в текущем итераторе
                else:
                    self.next_list = self.item.pop()  # итератор из очереди
                    continue
            if isinstance(self.next_element, list):
                # делаем следующий элемент текущим итератором, а текущий итератор становится в очередь
                self.item.append(self.next_list)
                self.next_list = iter(self.next_element)
            else:
                return self.next_element  # возвращаем элемент, если он не является списком


@logger
def test():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    return list(FlatIterator(list_of_lists_2))


if __name__ == '__main__':
    test()
