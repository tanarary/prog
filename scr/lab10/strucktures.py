from collections import deque
from typing import Any, Optional


class Stack:
    """Стек (LIFO) на базе list.

    Операции:
      - push(item)      O(1) amortized добавление в стек
      - pop()           O(1) удаление из стека
      - peek()          O(1) (возврат None, если пуст)
      - is_empty()      O(1) проверка на пустоту
      - __len__()       O(1)
    """

    __slots__ = ("_data",)

    def __init__(self, iterable=None) -> None:
        self._data: list[Any] = list(iterable) if iterable is not None else []

    def push(self, item: Any) -> None: 
        self._data.append(item)

    def pop(self) -> Any:
        if not self._data:
            raise IndexError("pop from empty Stack")
        return self._data.pop()

  # Метод просмотра верхнего элемента без удаления
    def peek(self) -> Optional[Any]:
        return self._data[-1] if self._data else None

    # Метод проверки стека на пустоту
    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"


class Queue:
    """Очередь (FIFO) на базе collections.deque.

    Операции:
      - enqueue(item)   O(1)  Добавление в очередь
      - dequeue()       O(1) Удаление из очереди
      - peek()          O(1) (возврат None, если пуст)  Просмотр первого элемента
      - is_empty()      O(1)  Проверка на пустоту
      - __len__()       O(1)
    """

    __slots__ = ("_data",)

    def __init__(self, iterable=None) -> None:
        self._data: deque[Any] = deque(iterable) if iterable is not None else deque()

    def enqueue(self, item: Any) -> None:
        self._data.append(item)

    def dequeue(self) -> Any:
        if not self._data:
            raise IndexError("dequeue from empty Queue")
        return self._data.popleft()

    def peek(self) -> Optional[Any]:
        return self._data[0] if self._data else None

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({list(self._data)!r})"

print('Stack')

stack = Stack([1,2,3,4])
print(f'Снятие верхнего элемента стека : {stack.pop()}')
print(f'Пустой ли стек? {stack.is_empty()}')
print(f'Число сверху : {stack.peek()}')
stack.push(1)
print(f'Значение сверху после добавления числа в стек : {stack.peek()}')
print(f'Длина стека : {len(stack)}')
print(f'Стек : {stack._data}')

print('Deque')

q = Queue([1,2,3,4])

print(f'Значение первого эллемента : {q.peek()}')
q.dequeue()
print(f'Значение первого эллемента после удаления числа : {q.peek()}')
q.enqueue(52)
print(f'Значение первого эллемента после добавления числа : {q.peek()}')
print(f'Пустая ли очередь? {q.is_empty()}')
print(f'Количество элементов в очереди : {len(q)}')