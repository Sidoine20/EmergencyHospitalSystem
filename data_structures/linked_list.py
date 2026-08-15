"""
Singly Linked List implementation for Patient records.

A Linked List is a linear data structure where elements are NOT stored
in contiguous memory locations. Instead, each element (called a Node)
contains:
    1. data: A reference to the payload (here: a Patient object).
    2. next: A reference (pointer) to the next Node in the sequence (or None).

Structure diagram:
    +---------------+      +---------------+      +---------------+
    | Patient (101) | ---> | Patient (102) | ---> | Patient (103) | ---> None
    +---------------+      +---------------+      +---------------+
         ^                                             ^
       head                                           tail
"""

from typing import Optional, Iterator
from models.patient import Patient


class Node:
    """
    A single node in the singly linked list.

    Attributes:
        data (Patient): The patient record stored in this node.
        next (Optional[Node]): Pointer/reference to the next node in the chain.
    """

    def __init__(self, data: Patient) -> None:
        self.data: Patient = data
        self.next: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node(patient_id={self.data.patient_id}, name='{self.data.name}')"

    def __str__(self) -> str:
        return str(self.data)


class LinkedList:
    """
    Singly Linked List of Patient records.

    Maintains:
        - head: Reference to the first Node (None if empty).
        - tail: Reference to the last Node (None if empty) for O(1) appends.
        - _size: Integer keeping track of the total number of nodes for O(1) size lookups.
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # State Inspection
    # ------------------------------------------------------------------
    def is_empty(self) -> bool:
        """
        Check if the linked list contains zero elements.

        Time Complexity: O(1) - Constant time check of the head pointer.
        Space Complexity: O(1)
        """
        return self.head is None

    def size(self) -> int:
        """
        Return the total number of patient nodes in the list.

        Time Complexity: O(1) - Cached count maintained during insertions and deletions.
        Space Complexity: O(1)
        """
        return self._size

    def __len__(self) -> int:
        """Enables Python's built-in len(linked_list) syntax."""
        return self._size

    # ------------------------------------------------------------------
    # Insertion Operations
    # ------------------------------------------------------------------
    def prepend(self, data: Patient) -> None:
        """
        Insert a new patient at the beginning (head) of the list.

        Steps:
            1. Create a new Node with the patient data.
            2. Point new_node.next to the current head.
            3. Update head to be new_node.
            4. If the list was empty, tail also points to new_node.
            5. Increment size.

        Time Complexity: O(1) - No traversal needed.
        Space Complexity: O(1) auxiliary space (one new Node allocated).
        """
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node

        self._size += 1

    def append(self, data: Patient) -> None:
        """
        Insert a new patient at the end (tail) of the list.

        Steps:
            1. Create a new Node with the patient data.
            2. If empty, both head and tail point to new_node.
            3. If not empty, link current tail.next -> new_node, and update tail.
            4. Increment size.

        Time Complexity: O(1) - Maintained by tracking the tail pointer.
        Space Complexity: O(1) auxiliary space.
        """
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            # We know self.tail is not None since is_empty() is False
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node

        self._size += 1

    def insert(self, position: int, data: Patient) -> None:
        """
        Insert a patient at a specific 0-based index.

        position = 0          -> Prepend at head.
        position = self._size -> Append at tail.
        0 < position < size   -> Traverse to (position - 1) and rewire pointers.

        Time Complexity:
            - Best Case: O(1) when inserting at position 0 or position == size (at tail).
            - Worst/Average Case: O(k) where k is the position (traversing k nodes).
        Space Complexity: O(1) auxiliary space.
        """
        if position < 0 or position > self._size:
            raise IndexError(
                f"Position {position} is out of bounds for list of size {self._size}."
            )

        if position == 0:
            self.prepend(data)
            return

        if position == self._size:
            self.append(data)
            return

        # Inserting in the middle: traverse to the node just BEFORE insertion point
        new_node = Node(data)
        previous = self._node_at(position - 1)
        assert previous is not None

        # Rewire references:
        # 1. new_node points to the node currently after `previous`
        # 2. previous points to `new_node`
        new_node.next = previous.next
        previous.next = new_node

        self._size += 1

    # ------------------------------------------------------------------
    # Search Operation
    # ------------------------------------------------------------------
    def search(self, patient_id: int) -> Optional[Patient]:
        """
        Search for a patient by their unique patient_id using linear traversal.

        Steps:
            1. Start at head node.
            2. Inspect current.data.patient_id.
            3. If match found, return the Patient object.
            4. Otherwise, advance to current.next until reaching None.

        Time Complexity:
            - Best Case: O(1) if target is at the head node.
            - Worst Case: O(n) if target is at the tail or not present.
            - Average Case: O(n) requiring ~n/2 comparisons.
        Space Complexity: O(1) auxiliary space.
        """
        current = self.head
        while current is not None:
            if current.data.patient_id == patient_id:
                return current.data
            current = current.next
        return None

    # ------------------------------------------------------------------
    # Deletion Operation
    # ------------------------------------------------------------------
    def delete(self, patient_id: int) -> bool:
        """
        Delete the first patient node matching patient_id from the chain.

        Pointer rewiring logic:
            - If target is head: move head = head.next. If head becomes None, tail = None.
            - If target is middle/tail: previous.next = current.next. If current was tail, tail = previous.

        Returns:
            bool: True if patient was found and removed, False otherwise.

        Time Complexity:
            - Best Case: O(1) if patient is at the head.
            - Worst/Average Case: O(n) to traverse and find the matching node.
        Space Complexity: O(1) auxiliary space.
        """
        if self.is_empty():
            return False

        previous: Optional[Node] = None
        current: Optional[Node] = self.head

        while current is not None:
            if current.data.patient_id == patient_id:
                # Case 1: Deleting the head node
                if previous is None:
                    self.head = current.next
                    if self.head is None:
                        # List became completely empty
                        self.tail = None
                # Case 2: Deleting a node after head
                else:
                    previous.next = current.next
                    if current.next is None:
                        # Deleted node was the tail, so update tail to previous
                        self.tail = previous

                self._size -= 1
                return True

            previous = current
            current = current.next

        return False

    # ------------------------------------------------------------------
    # Traversal & Display
    # ------------------------------------------------------------------
    def display(self) -> None:
        """
        Traverse the list from head to tail and print each patient record.

        Time Complexity: O(n) - Must visit all n nodes.
        Space Complexity: O(1)
        """
        if self.is_empty():
            print("Linked List is empty. No patients registered.")
            return

        current = self.head
        position = 0
        while current is not None:
            print(f"[Node Index: {position}]")
            print(current.data)
            print("-" * 40)
            current = current.next
            position += 1

    def to_list(self) -> list[Patient]:
        """
        Convert the linked list nodes into a standard Python list of Patient objects.

        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        result: list[Patient] = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __iter__(self) -> Iterator[Patient]:
        """Allows direct iteration over patients: `for patient in linked_list:`"""
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    # ------------------------------------------------------------------
    # Internal Helper
    # ------------------------------------------------------------------
    def _node_at(self, position: int) -> Node:
        """
        Traverse the chain to retrieve the Node instance at `position` (0-indexed).

        Time Complexity: O(position)
        """
        if position < 0 or position >= self._size:
            raise IndexError(
                f"Position {position} is out of bounds for list of size {self._size}."
            )

        current = self.head
        assert current is not None

        for _ in range(position):
            assert current.next is not None
            current = current.next

        return current
