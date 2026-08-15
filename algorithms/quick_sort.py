"""
Quick Sort implementation for Patient records.

Mathematical Foundations & Complexity Analysis:
    1. Recurrence Relations:
       - Best & Balanced Partitions (k = n / 2):
         T(n) = 2 * T(n / 2) + Theta(n) ==> Theta(n * log2(n))

       - Worst-Case Degenerate Partitions (k = 0 or k = n - 1):
         T(n) = T(n - 1) + Theta(n) ==> Sum_{i=1}^n i = (n * (n + 1)) / 2 = Theta(n²)

    2. Asymptotic Bounds:
       - Best-Case Time Complexity:    Omega(n * log2(n))
       - Average-Case Time Complexity: Theta(n * log2(n))
       - Worst-Case Time Complexity:   O(n²) (mitigated via middle-element pivot selection)
       - Auxiliary Space Complexity:   O(log2(n)) call-stack frames on average; O(n) worst-case.
       - In-Place Status: In-Place (data mutated inside existing array boundaries).
"""

from typing import List, Callable, Any
from models.patient import Patient


class QuickSort:
    """
    Provides in-place partitioning sorting algorithms for high-throughput patient records.
    """

    @classmethod
    def sort_by_patient_id(cls, patients: List[Patient]) -> List[Patient]:
        """Returns a sorted duplicate array ordered by integer patient_id."""
        arr = patients.copy()
        cls._quicksort(arr, 0, len(arr) - 1, key_func=lambda p: p.patient_id)
        return arr

    @classmethod
    def sort_by_name(cls, patients: List[Patient]) -> List[Patient]:
        """Returns a sorted duplicate array ordered lexicographically by patient name."""
        arr = patients.copy()
        cls._quicksort(arr, 0, len(arr) - 1, key_func=lambda p: p.name.lower())
        return arr

    @classmethod
    def _quicksort(
        cls,
        arr: List[Patient],
        low: int,
        high: int,
        key_func: Callable[[Patient], Any],
    ) -> None:
        """
        Recursive in-place Quick Sort execution.
        """
        if low < high:
            pivot_index: int = cls._partition(arr, low, high, key_func)
            cls._quicksort(arr, low, pivot_index - 1, key_func)
            cls._quicksort(arr, pivot_index + 1, high, key_func)

    @classmethod
    def _partition(
        cls,
        arr: List[Patient],
        low: int,
        high: int,
        key_func: Callable[[Patient], Any],
    ) -> int:
        """
        Lomuto Partitioning scheme with middle-index pivot selection to avoid worst-case
        O(n^2) behavior on pre-sorted distributions.
        """
        mid: int = low + (high - low) // 2
        arr[mid], arr[high] = arr[high], arr[mid]

        pivot_val: Any = key_func(arr[high])
        i: int = low - 1

        for j in range(low, high):
            if key_func(arr[j]) <= pivot_val:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
