"""
Algorithm Benchmarking and Empirical Complexity Analysis.

Compares:
1. Linear Search vs Binary Search (Number of comparisons and time elapsed).
2. O(n²) algorithms (Bubble Sort, Selection Sort) vs O(n log n) algorithms (Merge Sort, Quick Sort).
"""

import time
import random
from typing import List
from models.patient import Patient
from algorithms.bubble_sort import BubbleSort
from algorithms.selection_sort import SelectionSort
from algorithms.merge_sort import MergeSort
from algorithms.quick_sort import QuickSort
from algorithms.binary_search import BinarySearch


def generate_random_patients(count: int) -> List[Patient]:
    """Generate `count` unique random patient objects."""
    blood_types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    priorities = ["Critical", "High", "Medium", "Low"]
    names = ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris", "Pat", "Riley"]

    ids = list(range(1, count + 1))
    random.shuffle(ids)

    patients: List[Patient] = []
    for i, pid in enumerate(ids):
        patients.append(
            Patient(
                patient_id=pid,
                name=f"{random.choice(names)}_{pid}",
                age=random.randint(1, 95),
                blood_group=random.choice(blood_types),
                priority=random.choice(priorities),
            )
        )
    return patients


def benchmark_search(dataset_size: int = 10000):
    print("=" * 65)
    print(f"BENCHMARK: LINEAR SEARCH vs BINARY SEARCH (N = {dataset_size:,} records)")
    print("=" * 65)

    # Sorted dataset for search comparison
    patients = [
        Patient(i, f"Patient_{i}", 30, "O+", "Medium")
        for i in range(1, dataset_size + 1)
    ]
    target_id = dataset_size  # Worst case: target is at the very end

    # 1. Linear Search
    start = time.perf_counter()
    linear_found = None
    linear_comparisons = 0
    for p in patients:
        linear_comparisons += 1
        if p.patient_id == target_id:
            linear_found = p
            break
    linear_time_ms = (time.perf_counter() - start) * 1000

    # 2. Binary Search
    start = time.perf_counter()
    binary_found, binary_comparisons = BinarySearch.search_with_stats(
        patients, target_id
    )
    binary_time_ms = (time.perf_counter() - start) * 1000

    print(f"Target Patient ID: {target_id}")
    print("-" * 65)
    print(
        f"Linear Search : {linear_comparisons:>7} comparisons | Time: {linear_time_ms:0.4f} ms | Complexity: O(n)"
    )
    print(
        f"Binary Search : {binary_comparisons:>7} comparisons | Time: {binary_time_ms:0.4f} ms | Complexity: O(log n)"
    )
    print(
        f"Speedup Factor: {linear_comparisons // binary_comparisons}x fewer operations!"
    )
    print("-" * 65)


def benchmark_sorting(dataset_sizes=(200, 1000, 2500)):
    print("\n" + "=" * 65)
    print("BENCHMARK: SORTING ALGORITHMS EMPIRICAL RUNTIME")
    print("=" * 65)
    print(
        f"{'Dataset Size (N)':<18} | {'Bubble Sort':<12} | {'Selection':<12} | {'Merge Sort':<12} | {'Quick Sort':<12}"
    )
    print("-" * 75)

    for size in dataset_sizes:
        patients = generate_random_patients(size)

        # Bubble Sort
        t0 = time.perf_counter()
        BubbleSort.sort_by_patient_id(patients)
        bubble_time = (time.perf_counter() - t0) * 1000

        # Selection Sort
        t0 = time.perf_counter()
        SelectionSort.sort_by_patient_id(patients)
        selection_time = (time.perf_counter() - t0) * 1000

        # Merge Sort
        t0 = time.perf_counter()
        MergeSort.sort_by_patient_id(patients)
        merge_time = (time.perf_counter() - t0) * 1000

        # Quick Sort
        t0 = time.perf_counter()
        QuickSort.sort_by_patient_id(patients)
        quick_time = (time.perf_counter() - t0) * 1000

        print(
            f"N = {size:<14} | {bubble_time:>8.2f} ms | {selection_time:>8.2f} ms | {merge_time:>8.2f} ms | {quick_time:>8.2f} ms"
        )
    print("-" * 75)


if __name__ == "__main__":
    benchmark_search(10000)
    benchmark_sorting((200, 1000, 2000))
