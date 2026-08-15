"""
Stack (LIFO - Last In, First Out) implementation for Hospital Action History & Undo Logs.

In an emergency medical system, doctors and triage nurses perform sequential
actions (vital checks, medication changes, triage priority adjustments).
A Stack ensures that the most recent action is always at the top:
    1. Undo / Rollback: If a nurse makes an accidental change or an adverse drug reaction occurs,
       the most recent action is popped and reversed first.
    2. Audit Trail: Investigating a patient's recent medical events in reverse chronological order.

Structure diagram:
                    push() / pop() / peek()
                              |
                              v (TOP)
                     +-----------------+
                     | Action 3 (New)  |  <--- top (Last In, First Out)
                     +-----------------+
                              | next
                              v
                     +-----------------+
                     |    Action 2     |
                     +-----------------+
                              | next
                              v
                     +-----------------+
                     | Action 1 (Old)  |
                     +-----------------+
                              | next
                              v
                            None (BOTTOM)
"""

from typing import Any, Optional, Iterator, Generic, TypeVar

T = TypeVar("T")


class StackNode(Generic[T]):
    """
    A single node in the Stack.

    Attributes:
        data (T): The payload stored (e.g., Patient, MedicalAction, or State dictionary).
        next (Optional[StackNode]): Pointer to the node immediately below this one.
    """

    def __init__(self, data: T) -> None:
        self.data: T = data
        self.next: Optional["StackNode[T]"] = None

    def __repr__(self) -> str:
        return f"StackNode(data={self.data})"

    def __str__(self) -> str:
        return str(self.data)


class Stack(Generic[T]):
    """
    Stack data structure implemented using a Singly Linked Chain with a Top pointer.

    Invariants:
        - `top`: points to the most recently pushed node.
        - `_size`: tracks the total number of items in the stack.

    Time Complexity:
        - push:     O(1)
        - pop:      O(1)
        - peek:     O(1)
        - is_empty: O(1)
        - size:     O(1)
    """

    def __init__(self) -> None:
        self.top: Optional[StackNode[T]] = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # State Inspection
    # ------------------------------------------------------------------
    def is_empty(self) -> bool:
        """
        Check if the stack contains no elements.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self.top is None

    def size(self) -> int:
        """
        Return the number of elements in the stack.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        return self._size

    def __len__(self) -> int:
        return self._size

    # ------------------------------------------------------------------
    # Core Stack Operations
    # ------------------------------------------------------------------
    def push(self, data: T) -> None:
        """
        Push a new element onto the top of the stack.

        Steps:
            1. Allocate a new StackNode with `data`.
            2. Point `new_node.next` to the current `self.top`.
            3. Update `self.top` to be `new_node`.
            4. Increment `_size` by 1.

        Time Complexity: O(1) - Direct pointer update at top.
        Space Complexity: O(1) auxiliary space (one node allocated).
        """
        new_node = StackNode(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self) -> Optional[T]:
        """
        Remove and return the element at the top of the stack (most recently pushed).

        Steps:
            1. If empty, return None (or raise IndexError).
            2. Extract `data` from `self.top`.
            3. Advance `self.top = self.top.next`.
            4. Decrement `_size` by 1.
            5. Return the extracted data.

        Time Complexity: O(1) - Direct pointer update at top.
        Space Complexity: O(1) auxiliary space.
        """
        if self.is_empty():
            return None

        assert self.top is not None
        popped_data = self.top.data
        self.top = self.top.next
        self._size -= 1
        return popped_data

    def peek(self) -> Optional[T]:
        """
        Return the element at the top without removing it.

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.is_empty():
            return None
        assert self.top is not None
        return self.top.data

    # ------------------------------------------------------------------
    # Traversal & Utility
    # ------------------------------------------------------------------
    def display(self) -> None:
        """
        Print stack contents from TOP (most recent) to BOTTOM (oldest).

        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if self.is_empty():
            print("Stack is empty. No history records.")
            return

        current = self.top
        depth = 1
        print(f"--- STACK HISTORY (Top to Bottom | Depth: {self._size}) ---")
        while current is not None:
            tag = " [TOP (MOST RECENT)]" if depth == 1 else ""
            print(f"Level #{depth}{tag}:")
            print(f"  {current.data}")
            print("-" * 40)
            current = current.next
            depth += 1

    def to_list(self) -> list[T]:
        """Convert stack elements to a list ordered from TOP to BOTTOM."""
        result: list[T] = []
        current = self.top
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __iter__(self) -> Iterator[T]:
        """Iterate from TOP to BOTTOM without popping elements."""
        current = self.top
        while current is not None:
            yield current.data
            current = current.next
