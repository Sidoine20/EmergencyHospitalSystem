"""
Unit tests for BinaryMaxHeap and EmergencyPriorityQueue.
"""

from models.patient import Patient
from data_structures.priority_queue import (
    BinaryMaxHeap,
    EmergencyPriorityQueue,
    PriorityItem,
)


def test_empty_priority_queue():
    epq = EmergencyPriorityQueue()
    assert epq.is_empty() is True
    assert epq.size() == 0
    assert len(epq) == 0
    assert epq.peek() is None
    assert epq.dequeue() is None


def test_priority_ordering():
    epq = EmergencyPriorityQueue()

    # Arriving in mixed/reverse priority order:
    p_low = Patient(1, "Low Patient", 25, "O+", "Low")
    p_med = Patient(2, "Med Patient", 30, "A+", "Medium")
    p_high = Patient(3, "High Patient", 45, "B+", "High")
    p_crit = Patient(4, "Critical Patient", 60, "AB+", "Critical")

    epq.enqueue(p_low)
    epq.enqueue(p_med)
    epq.enqueue(p_high)
    epq.enqueue(p_crit)

    assert epq.size() == 4
    assert epq.peek().priority == "Critical"

    # Must dequeue in strict priority order: Critical -> High -> Medium -> Low
    d1 = epq.dequeue()
    assert d1.patient_id == 4 and d1.priority == "Critical"

    d2 = epq.dequeue()
    assert d2.patient_id == 3 and d2.priority == "High"

    d3 = epq.dequeue()
    assert d3.patient_id == 2 and d3.priority == "Medium"

    d4 = epq.dequeue()
    assert d4.patient_id == 1 and d4.priority == "Low"

    assert epq.is_empty() is True


def test_fifo_tie_breaking_for_equal_priorities():
    """
    If multiple patients have the SAME priority (e.g. Critical),
    the one who arrived FIRST should be served first.
    """
    epq = EmergencyPriorityQueue()

    c1 = Patient(101, "First Critical Arrival", 50, "O+", "Critical")
    c2 = Patient(102, "Second Critical Arrival", 40, "A-", "Critical")
    h1 = Patient(103, "First High Arrival", 30, "B+", "High")
    h2 = Patient(104, "Second High Arrival", 35, "O-", "High")

    epq.enqueue(c1)
    epq.enqueue(h1)
    epq.enqueue(c2)
    epq.enqueue(h2)

    # Dequeue order must be: c1 (Critical, arr 1), c2 (Critical, arr 3), h1 (High, arr 2), h2 (High, arr 4)
    res1 = epq.dequeue()
    assert res1.patient_id == 101

    res2 = epq.dequeue()
    assert res2.patient_id == 102

    res3 = epq.dequeue()
    assert res3.patient_id == 103

    res4 = epq.dequeue()
    assert res4.patient_id == 104

    assert epq.is_empty() is True


def test_heap_array_arithmetic():
    assert BinaryMaxHeap.parent_index(1) == 0
    assert BinaryMaxHeap.parent_index(2) == 0
    assert BinaryMaxHeap.parent_index(3) == 1
    assert BinaryMaxHeap.parent_index(4) == 1
    assert BinaryMaxHeap.left_child_index(0) == 1
    assert BinaryMaxHeap.right_child_index(0) == 2


if __name__ == "__main__":
    test_empty_priority_queue()
    test_priority_ordering()
    test_fifo_tie_breaking_for_equal_priorities()
    test_heap_array_arithmetic()
    print("All PriorityQueue and BinaryHeap unit tests passed successfully!")
