## Лабораторная работа 10

### A.Реализация Stack и Queue
```python
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

```
### Результат вывода

![struc](/scr/lab10/img/structures_img.png)

### Реализовать SinglyLinkedList 

```python
from typing import Any, Iterator, Optional


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value: Any, next: Optional["Node"] = None) -> None:
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        return f"Node({self.value!r})"


class SinglyLinkedList:
    """Односвязный список.

    Атрибуты:
      - head, tail, _size

    Методы:
      - append(value)       O(1)
      - prepend(value)      O(1)
      - insert(idx, value)  O(min(idx, n)) — проход от головы
      - remove(value)       O(n) — 
      - remove_at(idx)      O(n) — 
      - __iter__, __len__, __repr__, __str__
    """

    __slots__ = ("head", "tail", "_size")

    def __init__(self, iterable=None) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0
        if iterable:
            for v in iterable:
                self.append(v)

    def append(self, value: Any) -> None:
        """Добавить в конец — O(1)."""
        node = Node(value)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        self._size += 1

    def prepend(self, value: Any) -> None:
        """Добавить в начало — O(1)."""
        node = Node(value, next=self.head)
        self.head = node
        if self._size == 0:
            self.tail = node
        self._size += 1

    def insert(self, idx: int, value: Any) -> None:
        """Вставить по индексу. Допускаются idx==0 и idx==len."""
        if idx < 0 or idx > self._size:
            raise IndexError("insert index out of range")
        if idx == 0:
            self.prepend(value)
            return
        if idx == self._size:
            self.append(value)
            return

        prev = self.head
        for _ in range(idx - 1):
            assert prev is not None
            prev = prev.next
        assert prev is not None
        node = Node(value, next=prev.next)
        prev.next = node
        self._size += 1

    def remove(self, value: Any) -> None:
        """Удалить первое вхождение value. Если не найдено — ValueError."""
        prev: Optional[Node] = None
        cur = self.head
        idx = 0
        while cur:
            if cur.value == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                if cur is self.tail:
                    self.tail = prev
                self._size -= 1
                return
            prev, cur = cur, cur.next
            idx += 1
        raise ValueError("remove: value not found in SinglyLinkedList")

    def remove_at(self, idx: int) -> None:
        """Удалить элемент по индексу. Возбуждает IndexError при неверном индексе."""
        if idx < 0 or idx >= self._size:
            raise IndexError("remove_at index out of range")
        prev: Optional[Node] = None
        cur = self.head
        for _ in range(idx):
            prev, cur = cur, cur.next  # type: ignore
        assert cur is not None
        if prev is None:
            self.head = cur.next
        else:
            prev.next = cur.next
        if cur is self.tail:
            self.tail = prev
        self._size -= 1

    def __iter__(self) -> Iterator[Any]:
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"SinglyLinkedList([{', '.join(repr(x) for x in self)}])"

    def __str__(self) -> str:
        parts = []
        cur = self.head
        while cur:
            parts.append(f"[{cur.value!s}]")
            cur = cur.next
        parts.append("None")
        return " -> ".join(parts)

sll = SinglyLinkedList()
print(f'Длина нашего односвязанного списка : {len(sll)}')

sll.append(1)
sll.append(2)
sll.prepend(0)
print(f'Наша ныняшняя длина списка после добавления эллементов : {len(sll)}') 
print(f'Односвязаный список : {list(sll)}')

sll.insert(1, 0.5)
print(f'Длина списка после добавления на 1 индекс числа 0.5 : {len(sll)}')
print(f'Односвязаный список : {list(sll)}')
sll.append(52)
print(f'Односвязанный список после добавления числа в конец : {list(sll)}')

print(sll) 

```

### Результат вывода

![link](/scr/lab10/linked_list.py)


### Теория
 #### Стек (Stack)
Принцип: LIFO — Last In, First Out.
Операции:
push(x) — положить элемент сверху;
pop() — снять верхний элемент;
peek() — посмотреть верхний, не снимая.
Типичные применения:
история действий (undo/redo);
обход графа/дерева в глубину (DFS);
парсинг выражений, проверка скобок.

Асимптотика (при реализации на массиве / списке):
push — O(1) амортизированно;
pop — O(1);
peek — O(1);
проверка пустоты — O(1).
Очередь (Queue)
Принцип: FIFO — First In, First Out.

Операции:
enqueue(x) — добавить в конец;
dequeue() — взять элемент из начала;
peek() — посмотреть первый элемент, не удаляя.

Типичные применения:
обработка задач по очереди (job queue);
обход графа/дерева в ширину (BFS);
буферы (сетевые, файловые, очереди сообщений).

В Python:
обычный list плохо подходит для реализации очереди:
удаление с начала pop(0) — это O(n) (все элементы сдвигаются);
collections.deque даёт O(1) операции по краям:
append / appendleft — O(1);
pop / popleft — O(1).

Асимптотика (на нормальной очереди):
enqueue — O(1);
dequeue — O(1);
peek — O(1).
Односвязный список (Singly Linked List)

Структура:
состоит из узлов Node;
каждый узел хранит:
value — значение элемента;
next — ссылку на следующий узел или None (если это последний).

Основные идеи:
элементы не хранятся подряд в памяти, как в массиве;
каждый элемент знает только «следующего соседа».

Плюсы:
вставка/удаление в начало списка за O(1):
если есть ссылка на голову (head), достаточно перенаправить одну ссылку;
при удалении из середины не нужно сдвигать остальные элементы:
достаточно обновить ссылки узлов;
удобно использовать как базовый строительный блок для других структур (например, для очередей, стеков, хеш-таблиц с цепочками).
Минусы:

доступ по индексу i — O(n):
чтобы добраться до позиции i, нужно пройти i шагов от головы;
нет быстрого доступа к предыдущему элементу:
чтобы удалить узел, нужно знать его предыдущий узел → часто нужен дополнительный проход.
Типичные оценки:

prepend (добавить в начало) — O(1);
append:
при наличии tail — O(1),
без tail — O(n), т.к. требуется пройти до конца;
поиск по значению — O(n).
Двусвязный список (Doubly Linked List)
Структура:

также состоит из узлов DNode;
каждый узел хранит:
value — значение элемента;
next — ссылку на следующий узел;
prev — ссылку на предыдущий узел.
Основные идеи:

можно двигаться как вперёд, так и назад по цепочке узлов;
удобно хранить ссылки на оба конца: head и tail.
Плюсы по сравнению с односвязным:

удаление узла по ссылке на него — O(1):
достаточно «вытащить» его, перенастроив prev.next и next.prev;
не нужно искать предыдущий узел линейным проходом;
эффективен для структур, где часто нужно удалять/добавлять элементы в середине, имея на них прямые ссылки (например, реализация LRU-кэша);
можно легко идти в обе стороны:
прямой и обратный обход списка.

Минусы:
узел занимает больше памяти:
нужно хранить две ссылки (prev, next);
код более сложный:
легко забыть обновить одну из ссылок и «сломать» структуру;
сложнее отлаживать.

Типичные оценки (при наличии head и tail):
вставка/удаление в начале/конце — O(1);
вставка/удаление по ссылке на узел — O(1);
доступ по индексу — O(n) (нужно идти от головы или хвоста);
поиск по значению — O(n).

Пример текстовой визуализации:
None <- [A] <-> [B] <-> [C] -> None