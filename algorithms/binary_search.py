"""
Binary Search implementation for sorted Patient datasets.

Mathematical Foundations & Asymptotic Analysis:
    1. Recurrence Relation:
       T(n) = T(floor(n / 2)) + Theta(1) for n > 1
       T(1) = Theta(1)

    2. Closed-Form Maximum Comparison Bound:
       C_max(n) = floor(log2(n)) + 1 comparisons
       For n = 10,000:
       C_max(10,000) = floor(13.2877) + 1 = 14 comparisons

    3. Asymptotic Bounds:
       - Best-Case Time Complexity:    Omega(1) (target element resides at exact initial median)
       - Average-Case Time Complexity: Theta(log2(n))
       - Worst-Case Time Complexity:   O(log2(n))
       - Auxiliary Space Complexity:   Theta(1) (iterative pointer interval refinement)
"""

from typing import List, Optional, Tuple
from models.patient import Patient


class BinarySearch:
    """
    Provides iterative binary search operations on strictly ordered patient lists.
    """

    @staticmethod
    def search_by_patient_id(
        sorted_patients: List[Patient], target_id: int
    ) -> Optional[Patient]:
        """
        Locates a patient record by unique identifier in an ascending ordered array.

        Time Complexity:
            Best:    Omega(1)
            Average: Theta(log2(n))
            Worst:   O(log2(n))
        Space Complexity:
            O(1) auxiliary space.
        """
        low: int = 0
        high: int = len(sorted_patients) - 1

        while low <= high:
            # Midpoint calculation preventing arithmetic integer overflow
            mid: int = low + (high - low) // 2
            mid_id: int = sorted_patients[mid].patient_id

            if mid_id == target_id:
                return sorted_patients[mid]
            elif mid_id < target_id:
                low = mid + 1
            else:
                high = mid - 1

        return None

    @staticmethod
    def search_with_stats(
        sorted_patients: List[Patient], target_id: int
    ) -> Tuple[Optional[Patient], int]:
        """
        Performs binary search while accumulating exact loop iteration counts (comparisons).
        """
        low: int = 0
        high: int = len(sorted_patients) - 1
        comparisons: int = 0

        while low <= high:
            comparisons += 1
            mid: int = low + (high - low) // 2
            mid_id: int = sorted_patients[mid].patient_id

            if mid_id == target_id:
                return sorted_patients[mid], comparisons
            elif mid_id < target_id:
                low = mid + 1
            else:
                high = mid - 1

        return None, comparisons

    @staticmethod
    def search_by_name(
        sorted_patients: List[Patient], target_name: str
    ) -> Optional[Patient]:
        """
        Locates a patient record by full name in a lexicographically ordered array.
        """
        low: int = 0
        high: int = len(sorted_patients) - 1
        target_normalized: str = target_name.strip().lower()

        while low <= high:
            mid: int = low + (high - low) // 2
            mid_normalized: str = sorted_patients[mid].name.strip().lower()

            if mid_normalized == target_normalized:
                return sorted_patients[mid]
            elif mid_normalized < target_normalized:
                low = mid + 1
            else:
                high = mid - 1

        return None
