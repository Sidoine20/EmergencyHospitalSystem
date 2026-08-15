"""
Unit tests for Singly Linked List patient data structure.
"""

from models.patient import Patient
from data_structures.linked_list import LinkedList


def test_empty_linked_list():
    ll = LinkedList()
    assert ll.is_empty() is True
    assert ll.size() == 0
    assert len(ll) == 0
    assert ll.head is None
    assert ll.tail is None
    assert ll.search(999) is None
    assert ll.delete(999) is False


def test_prepend():
    ll = LinkedList()
    p1 = Patient(101, "Alice", 30, "A+", "Low")
    p2 = Patient(102, "Bob", 45, "O-", "High")

    ll.prepend(p1)
    assert ll.size() == 1
    assert ll.is_empty() is False
    assert ll.head.data.patient_id == 101
    assert ll.tail.data.patient_id == 101

    ll.prepend(p2)
    assert ll.size() == 2
    assert ll.head.data.patient_id == 102
    assert ll.tail.data.patient_id == 101
    assert ll.head.next.data.patient_id == 101


def test_append():
    ll = LinkedList()
    p1 = Patient(101, "Alice", 30, "A+", "Low")
    p2 = Patient(102, "Bob", 45, "O-", "High")

    ll.append(p1)
    ll.append(p2)
    assert ll.size() == 2
    assert ll.head.data.patient_id == 101
    assert ll.tail.data.patient_id == 102
    assert ll.head.next.data.patient_id == 102


def test_insert_positions():
    ll = LinkedList()
    p1 = Patient(101, "First", 20, "O+", "Low")
    p2 = Patient(102, "Second", 30, "B+", "Medium")
    p3 = Patient(103, "Third", 40, "AB+", "Critical")

    # Insert at 0 (prepend)
    ll.insert(0, p2)  # [102]
    # Insert at tail
    ll.insert(1, p3)  # [102, 103]
    # Insert at head again
    ll.insert(0, p1)  # [101, 102, 103]

    ids = [p.patient_id for p in ll]
    assert ids == [101, 102, 103]
    assert ll.head.data.patient_id == 101
    assert ll.tail.data.patient_id == 103

    # Insert in middle (position 1)
    p_mid = Patient(100, "Middle", 25, "A-", "High")
    ll.insert(1, p_mid)  # [101, 100, 102, 103]
    ids = [p.patient_id for p in ll]
    assert ids == [101, 100, 102, 103]
    assert ll.size() == 4


def test_search():
    ll = LinkedList()
    p1 = Patient(101, "Alice", 30, "A+", "Low")
    p2 = Patient(102, "Bob", 45, "O-", "High")
    ll.append(p1)
    ll.append(p2)

    found = ll.search(102)
    assert found is not None
    assert found.name == "Bob"

    not_found = ll.search(999)
    assert not_found is None


def test_delete_operations():
    ll = LinkedList()
    p1 = Patient(101, "Alice", 30, "A+", "Low")
    p2 = Patient(102, "Bob", 45, "O-", "High")
    p3 = Patient(103, "Charlie", 50, "B-", "Critical")

    ll.append(p1)
    ll.append(p2)
    ll.append(p3)

    # Delete middle (102)
    assert ll.delete(102) is True
    assert ll.size() == 2
    assert [p.patient_id for p in ll] == [101, 103]
    assert ll.head.data.patient_id == 101
    assert ll.tail.data.patient_id == 103

    # Delete tail (103)
    assert ll.delete(103) is True
    assert ll.size() == 1
    assert ll.head.data.patient_id == 101
    assert ll.tail.data.patient_id == 101

    # Delete head / only element (101)
    assert ll.delete(101) is True
    assert ll.size() == 0
    assert ll.is_empty() is True
    assert ll.head is None
    assert ll.tail is None

    # Delete non-existent
    assert ll.delete(999) is False


if __name__ == "__main__":
    test_empty_linked_list()
    test_prepend()
    test_append()
    test_insert_positions()
    test_search()
    test_delete_operations()
    print("All LinkedList unit tests passed successfully!")
