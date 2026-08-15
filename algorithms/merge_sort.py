"""
Merge Sort implementation for Patient records.

Mathematical Foundations & Complexity Analysis:
    1. Divide-and-Conquer Recurrence:
       T(n) = 2 * T(n / 2) + Theta(n) for n > 1
       T(1) = Theta(1)

    2. Master Theorem Derivation:
       For T(n) = a * T(n / b) + f(n) where a = 2, b = 2, f(n) = Theta(n^d) with d = 1:
       Since log_b(a) = log_2(2) = 1 == d:
       ==> T(n) = Theta(n^(log_b a) * log2(n)) = Theta(n * log2(n))

    3. Asymptotic Bounds:
       - Best-Case Time Complexity:    Omega(n * log2(n))
       - Average-Case Time Complexity: Theta(n * log2(n))
       - Worst-Case Time Complexity:   O(n * log2(n))
       - Auxiliary Space Complexity:   Theta(n) (allocated dynamic merge buffer)
       - Stability: Preserved (strict weak ordering satisfies A[i] <= B[j] preserving arrival order)
"""

from typing import List, Callable, Any
from models.patient import Patient


class MergeSort:
    """
    Provides stable, asymptotically optimal O(n log n) sorting for patient collections.
    """

    @classmethod
    def sort_by_patient_id(cls, patients: List[Patient]) -> List[Patient]:
        """Sort patients by integer patient_id in ascending order."""
        return cls.sort_by_key(patients, key_func=lambda p: p.patient_id)

    @classmethod
    def sort_by_name(cls, patients: List[Patient]) -> List[Patient]:
        """Sort patients in lexicographical order by name."""
        return cls.sort_by_key(patients, key_func=lambda p: p.name.lower())

    @classmethod
    def sort_by_age(cls, patients: List[Patient]) -> List[Patient]:
        """Sort patients in ascending numerical order by age."""
        return cls.sort_by_key(patients, key_func=lambda p: p.age)

    @classmethod
    def sort_by_key(
        cls, patients: List[Patient], key_func: Callable[[Patient], Any]
    ) -> List[Patient]:
        """
        Generic stable Merge Sort implementation parameterized by an extraction key function.

        Time Complexity:  Theta(n log2 n) in all cases.
        Space Complexity: Theta(n) auxiliary allocation.
        """
        if len(patients) <= 1:
            return patients.copy()

        # Step 1: Divide
        mid: int = len(patients) // 2
        left_partition: List[Patient] = cls.sort_by_key(
            patients[:mid], key_func
        )
        right_partition: List[Patient] = cls.sort_by_key(
            patients[mid:], key_func
        )

        # Step 2 & 3: Conquer & Merge
        return cls._merge(left_partition, right_partition, key_func)

    @staticmethod
    def _merge(
        left: List[Patient],
        right: List[Patient],
        key_func: Callable[[Patient], Any],
    ) -> List[Patient]:
        """
        Merges two monotonically sorted sub-lists into a single consolidated sorted list.
        Weak inequality (<=) ensures algorithm stability.
        """
        merged: List[Patient] = []
        i: int = 0
        j: int = 0
        len_left: int = len(left)
        len_right: int = len(right)

        while i < len_left and j < len_right:
            if key_func(left[i]) <= key_func(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        # Append remaining elements in Theta(k) time
        while i < len_left:
            merged.append(left[i])
            i += 1

        while j < len_right:
            merged.append(right[j])
            j += 1

        return merged
