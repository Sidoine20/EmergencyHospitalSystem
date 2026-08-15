"""
Unit tests for Searching and Sorting Algorithms.
"""

from models.patient import Patient
from algorithms.binary_search import BinarySearch
from algorithms.merge_sort import MergeSort
from algorithms.quick_sort import QuickSort
from algorithms.bubble_sort import BubbleSort
from algorithms.selection_sort import SelectionSort


def get_sample_patients():
    return [
        Patient(105, "Zoe Miller", 45, "O+", "Low"),
        Patient(102, "Alice Brown", 30, "A-", "Critical"),
        Patient(108, "David Wilson", 50, "B+", "High"),
        Patient(101, "Charlie Cox", 22, "AB+", "Medium"),
        Patient(104, "Bob Evans", 35, "O-", "High"),
    ]


def test_merge_sort_by_id():
    patients = get_sample_patients()
    sorted_p = MergeSort.sort_by_patient_id(patients)
    ids = [p.patient_id for p in sorted_p]
    assert ids == [101, 102, 104, 105, 108]


def test_merge_sort_by_name():
    patients = get_sample_patients()
    sorted_p = MergeSort.sort_by_name(patients)
    names = [p.name for p in sorted_p]
    assert names == [
        "Alice Brown",
        "Bob Evans",
        "Charlie Cox",
        "David Wilson",
        "Zoe Miller",
    ]


def test_quick_sort_by_id():
    patients = get_sample_patients()
    sorted_p = QuickSort.sort_by_patient_id(patients)
    ids = [p.patient_id for p in sorted_p]
    assert ids == [101, 102, 104, 105, 108]


def test_quick_sort_by_name():
    patients = get_sample_patients()
    sorted_p = QuickSort.sort_by_name(patients)
    names = [p.name for p in sorted_p]
    assert names == [
        "Alice Brown",
        "Bob Evans",
        "Charlie Cox",
        "David Wilson",
        "Zoe Miller",
    ]


def test_binary_search_by_id():
    patients = get_sample_patients()
    sorted_p = MergeSort.sort_by_patient_id(patients)  # [101, 102, 104, 105, 108]

    # Search present IDs
    p1 = BinarySearch.search_by_patient_id(sorted_p, 101)
    assert p1 is not None and p1.name == "Charlie Cox"

    p_mid = BinarySearch.search_by_patient_id(sorted_p, 104)
    assert p_mid is not None and p_mid.name == "Bob Evans"

    p_last = BinarySearch.search_by_patient_id(sorted_p, 108)
    assert p_last is not None and p_last.name == "David Wilson"

    # Search absent ID
    p_none = BinarySearch.search_by_patient_id(sorted_p, 999)
    assert p_none is None


def test_binary_search_by_name():
    patients = get_sample_patients()
    sorted_p = MergeSort.sort_by_name(patients)

    found = BinarySearch.search_by_name(sorted_p, "Alice Brown")
    assert found is not None and found.patient_id == 102

    not_found = BinarySearch.search_by_name(sorted_p, "Nonexistent Person")
    assert not_found is None


def test_binary_search_efficiency():
    """Verify that Binary Search on 1000 items takes at most log2(1000) ~ 10 steps."""
    thousand_patients = [
        Patient(i, f"Patient {i}", 20 + (i % 50), "O+", "Low")
        for i in range(1, 1001)
    ]
    _, comparisons = BinarySearch.search_with_stats(thousand_patients, 777)
    assert comparisons <= 10  # log2(1000) is approx 9.96


if __name__ == "__main__":
    test_merge_sort_by_id()
    test_merge_sort_by_name()
    test_quick_sort_by_id()
    test_quick_sort_by_name()
    test_binary_search_by_id()
    test_binary_search_by_name()
    test_binary_search_efficiency()
    print("All Algorithm unit tests passed successfully!")
