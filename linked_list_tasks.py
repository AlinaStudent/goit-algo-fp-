
"""
Завдання 1. Однозв'язний список:
- reverse_in_place(): реверсування списку шляхом зміни посилань між вузлами
- insertion_sort(): сортування вставками
- merge_sorted_lists(): злиття двох ВЖЕ відсортованих списків в один відсортований
Написано на Python 3.10+.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Optional, Iterator, Callable, TypeVar

T = TypeVar("T")

@dataclass
class Node:
    value: T
    next: Optional["Node"] = None

class SinglyLinkedList:
    def __init__(self, iterable: Optional[Iterable[T]] = None) -> None:
        self.head: Optional[Node] = None
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def __iter__(self) -> Iterator[T]:
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    # Утиліти
    def append(self, value: T) -> None:
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def to_list(self) -> list[T]:
        return list(iter(self))

    # 1) Реверсування in-place
    def reverse_in_place(self) -> None:
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    # 2а) Сортування вставками (in-place, стабільне)
    def insertion_sort(self, key: Callable[[T], object] = lambda x: x) -> None:
        sorted_head: Optional[Node] = None

        cur = self.head
        while cur:
            nxt = cur.next
            # Вставляємо cur в правильне місце у відсортованому підсписку
            if sorted_head is None or key(cur.value) < key(sorted_head.value):
                cur.next = sorted_head
                sorted_head = cur
            else:
                s = sorted_head
                while s.next and key(s.next.value) <= key(cur.value):
                    s = s.next
                cur.next = s.next
                s.next = cur
            cur = nxt

        self.head = sorted_head

    # 2б) Сортування злиттям (альтернатива до insertion_sort)
    def merge_sort(self, key: Callable[[T], object] = lambda x: x) -> None:
        def split(head: Optional[Node]) -> tuple[Optional[Node], Optional[Node]]:
            if head is None or head.next is None:
                return head, None
            slow = head
            fast = head.next
            while fast and fast.next:
                slow = slow.next  # type: ignore
                fast = fast.next.next
            middle = slow.next  # type: ignore
            slow.next = None  # type: ignore
            return head, middle

        def merge(a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
            dummy = Node(None)  # type: ignore
            tail = dummy
            while a and b:
                if key(a.value) <= key(b.value):
                    tail.next, a = a, a.next
                else:
                    tail.next, b = b, b.next
                tail = tail.next
            tail.next = a if a else b
            return dummy.next

        def sort(head: Optional[Node]) -> Optional[Node]:
            if head is None or head.next is None:
                return head
            left, right = split(head)
            return merge(sort(left), sort(right))

        self.head = sort(self.head)

    # 3) Злиття двох ВІДсортованих списків в новий відсортований
    @staticmethod
    def merge_sorted_lists(a: "SinglyLinkedList", b: "SinglyLinkedList",
                           key: Callable[[T], object] = lambda x: x) -> "SinglyLinkedList":
        pa, pb = a.head, b.head
        dummy = Node(None)  # type: ignore
        tail = dummy
        while pa and pb:
            if key(pa.value) <= key(pb.value):
                tail.next, pa = pa, pa.next
            else:
                tail.next, pb = pb, pb.next
            tail = tail.next
        tail.next = pa if pa else pb

        out = SinglyLinkedList()
        out.head = dummy.next
        return out


if __name__ == "__main__":
    # Демонстрація
    print("ДЕМОНСТРАЦІЯ ЗАВДАННЯ 1")
    lst = SinglyLinkedList([5, 3, 1, 4, 2])
    print("Початковий:", lst.to_list())
    lst.reverse_in_place()
    print("Після reverse:", lst.to_list())
    lst.insertion_sort()
    print("Після insertion_sort:", lst.to_list())

    a = SinglyLinkedList([1, 3, 5, 7])
    b = SinglyLinkedList([2, 4, 6, 8, 10])
    merged = SinglyLinkedList.merge_sorted_lists(a, b)
    print("Злиття:", merged.to_list())

    # Демонстрація merge_sort
    c = SinglyLinkedList([9, 2, 7, 1, 5, 3])
    c.merge_sort()
    print("Після merge_sort:", c.to_list())
