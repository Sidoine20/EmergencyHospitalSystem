"""
Bubble Sort implementation for Patient records.

Mathematical Analysis:
    1. Total Comparisons:
       Sum_{i=1}^{n-1} (n - i) = ((n - 1) * n) / 2 = (n² - n) / 2 = Theta(n²)

    2. Asymptotic Bounds:
       - Best-Case Time Complexity:    Omega(n) (achieved via early-termination boolean flag on presorted array)
       - Average-Case Time Complexity: Theta(n²)
       - Worst-Case Time Complexity:   O(n²) (reverse sorted array)
       - Auxiliary Space Complexity:   Theta(1) auxiliary memory.
"""

from typing import List
from models.patient import Patient


class BubbleSort:
    @staticmethod
    def sort_by_patient_id(patients: List[Patient]) -> List[Patient]:
        """
        Sort patients by unique integer ID using adaptive Bubble Sort.
        """
        sorted_patients: List[Patient] = patients.copy()
        n: int = len(sorted_patients)

        for i in range(n):
            swapped: bool = False
            for j in range(0, n - i - 1):
                if sorted_patients[j].patient_id > sorted_patients[j + 1].patient_id:
                    sorted_patients[j], sorted_patients[j + 1] = (
                        sorted_patients[j + 1],
                        sorted_patients[j],
                    )
                    swapped = True

            # Early termination condition (Omega(n) best-case guarantee)
            if not swapped:
                break

        return sorted_patients