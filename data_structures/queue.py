"""
Queue (FIFO - First In, First Out) implementation for Patient triage.

In a hospital triage system, standard non-critical patients are served
in the order of their arrival. A Queue ensures fairness:
the first patient who checks in is the first patient called into the doctor's room.

Structure diagram:
                dequeue()                                              enqueue()
                 (Front)                                                (Rear)
                    |                                                     |
                    v                                                     v
            +---------------+      +---------------+      +---------------+
  EXIT <--- | Patient (101) | <--- | Patient (102) | <--- | Patient (103) | <--- ENTER
            +---------------+      +---------------+      +---------------+
                 front                                                  rear
"""

from typing import Optional, Iterator
from models.patient import Patient


class QueueNode:
    """
    A single node in the Queue.

    Attributes:
        data (Patient): The patient object held in this node.
        next (Optional[QueueNode]): Pointer to the next patient in line.
    """

    def __init__(self, data: Patient) -> None:
        self.data: Patient = data
        self.next: Optional["QueueNode"] = None

    def __repr__(self) -> str:
        return f"QueueNode(patient_id={self.data.patient_id}, name='{self.data.name}')"

    def __str__(self) -> str:
        return str(self.data)


class Queue:
    """
    Queue data structure implemented using a Singly Linked List with Front & Rear pointers.

    Invariants:
        - `front`: points to the first patient to be served (dequeue endpoint).
        - `rear`: points to the latest patient who joined the queue (enqueue endpoint).
        - `_size`: tracks number of patients currently in line.

    Time Complexity:
        - enqueue: O(1)
        - dequeue: O(1)
        - peek:    O(1)
        - is_empty: O(1)
        - size:    O(1)
    """

    def __init__(self) -> None:
        self.front: Optional[QueueNode] = None
        self.rear: Optional[QueueNode] = None
        self._size: int = 0

    # ------------------------------------------------------------------
    # State Inspection
    # ------------------------------------------------------------------
    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        Time Complexity: O(1) - Evaluates front pointer.
        Space Complexity: O(1)
        """
        return self.front is None

    def size(self) -> int:
        """
        Return the number of patients currently in the queue.

        Time Complexity: O(1) - Cached integer count.
        Space Complexity: O(1)
        """
        return self._size

    def __len__(self) -> int:
        return self._size

    # ------------------------------------------------------------------
    # Queue Operations
    # ------------------------------------------------------------------
    def enqueue(self, patient: Patient) -> None:
        """
        Add a patient to the end (rear) of the queue.

        Steps:
            1. Wrap patient in a new QueueNode.
            2. If the queue is empty, both `front` and `rear` point to this new node.
            3. If not empty, link `self.rear.next` to the new node, then advance `self.rear`.
            4. Increment size by 1.

        Time Complexity: O(1) - Instant addition at the rear pointer without traversal.
        Space Complexity: O(1) auxiliary space (allocates one Node).
        """
        new_node = QueueNode(patient)

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            assert self.rear is not None
            self.rear.next = new_node
            self.rear = new_node

        self._size += 1

    def dequeue(self) -> Optional[Patient]:
        """
        Remove and return the patient at the front of the queue.

        Steps:
            1. If the queue is empty, return None (or raise exception).
            2. Retrieve the Patient data from `self.front`.
            3. Advance `self.front = self.front.next`.
            4. If `self.front` becomes None (queue is now empty), set `self.rear = None`.
            5. Decrement size by 1.
            6. Return the retrieved patient.

        Time Complexity: O(1) - Pointer update at the front without shifting remaining items.
        Space Complexity: O(1) auxiliary space.
        """
        if self.is_empty():
            return None

        assert self.front is not None
        served_patient = self.front.data

        # Advance front pointer to the next person in line
        self.front = self.front.next
        self._size -= 1

        # If the queue is now empty, reset rear to None
        if self.front is None:
            self.rear = None

        return served_patient

    def peek(self) -> Optional[Patient]:
        """
        Inspect the patient at the front of the queue without removing them.

        Time Complexity: O(1) - Direct read of `self.front.data`.
        Space Complexity: O(1)
        """
        if self.is_empty():
            return None
        assert self.front is not None
        return self.front.data

    # ------------------------------------------------------------------
    # Traversal & Utility
    # ------------------------------------------------------------------
    def display(self) -> None:
        """
        Print all patients in order from front (next to be served) to rear (last arrived).

        Time Complexity: O(n) - Visits each node once.
        Space Complexity: O(1)
        """
        if self.is_empty():
            print("Queue is empty. No patients waiting.")
            return

        current = self.front
        position = 1
        print(f"--- WAITING QUEUE (Total: {self._size} patients) ---")
        while current is not None:
            tag = " [NEXT UP (FRONT)]" if position == 1 else (" [REAR (LAST)]" if current == self.rear else "")
            print(f"Position #{position}{tag}:")
            print(current.data)
            print("-" * 40)
            current = current.next
            position += 1

    def to_list(self) -> list[Patient]:
        """Convert queue elements into a list from front to rear."""
        result: list[Patient] = []
        current = self.front
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __iter__(self) -> Iterator[Patient]:
        """Allows `for patient in queue:` traversal without dequeuing."""
        current = self.front
        while current is not None:
            yield current.data
            current = current.next
