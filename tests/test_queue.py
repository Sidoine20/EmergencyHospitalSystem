"""
Unit tests for the Queue (FIFO) data structure.
"""

from models.patient import Patient
from data_structures.queue import Queue


def test_empty_queue():
    q = Queue()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    assert q.peek() is None
    assert q.dequeue() is None
    assert q.front is None
    assert q.rear is None


def test_enqueue_and_fifo_order():
    q = Queue()
    p1 = Patient(101, "Alice", 25, "O+", "Low")
    p2 = Patient(102, "Bob", 40, "A-", "Medium")
    p3 = Patient(103, "Charlie", 60, "B+", "Critical")

    q.enqueue(p1)
    assert q.is_empty() is False
    assert q.size() == 1
    assert q.front.data.patient_id == 101
    assert q.rear.data.patient_id == 101

    q.enqueue(p2)
    q.enqueue(p3)
    assert q.size() == 3
    assert q.front.data.patient_id == 101
    assert q.rear.data.patient_id == 103

    # Peek should show front without removing
    assert q.peek().patient_id == 101
    assert q.size() == 3

    # Dequeue in FIFO order
    served_1 = q.dequeue()
    assert served_1.patient_id == 101
    assert q.size() == 2
    assert q.peek().patient_id == 102

    served_2 = q.dequeue()
    assert served_2.patient_id == 102
    assert q.size() == 1
    assert q.peek().patient_id == 103
    assert q.front == q.rear

    served_3 = q.dequeue()
    assert served_3.patient_id == 103
    assert q.size() == 0
    assert q.is_empty() is True
    assert q.front is None
    assert q.rear is None
    assert q.dequeue() is None


def test_interleaved_enqueue_dequeue():
    q = Queue()
    p1 = Patient(1, "P1", 20, "O+", "Low")
    p2 = Patient(2, "P2", 21, "O+", "Low")
    p3 = Patient(3, "P3", 22, "O+", "Low")

    q.enqueue(p1)
    q.enqueue(p2)
    assert q.dequeue().patient_id == 1

    q.enqueue(p3)
    assert q.size() == 2
    assert q.dequeue().patient_id == 2
    assert q.dequeue().patient_id == 3
    assert q.is_empty() is True


if __name__ == "__main__":
    test_empty_queue()
    test_enqueue_and_fifo_order()
    test_interleaved_enqueue_dequeue()
    print("All Queue unit tests passed successfully!")
