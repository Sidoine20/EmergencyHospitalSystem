"""
Selection Sort implementation for Patient records.

Mathematical Analysis:
    1. Total Comparisons:
       Sum_{i=1}^{n-1} (n - i) = ((n - 1) * n) / 2 = Theta(n²) comparisons in ALL cases.

    2. Total Swaps (Data Movements):
       At most (n - 1) swaps = O(n) memory writes.

    3. Asymptotic Bounds:
       - Best-Case Time Complexity:    Omega(n²)
       - Average-Case Time Complexity: Theta(n²)
       - Worst-Case Time Complexity:   O(n²)
       - Auxiliary Space Complexity:   Theta(1) (in-place)
       - Stability: Unstable (long-range swaps can alter relative order of equal keys)
"""

from typing import List
from models.patient import Patient


class SelectionSort:
    @staticmethod
    def sort_by_patient_id(patients: List[Patient]) -> List[Patient]:
        """
        Sort patients by unique integer ID using Selection Sort.
        """
        sorted_patients: List[Patient] = patients.copy()
        n: int = len(sorted_patients)

        for i in range(n - 1):
            min_index: int = i

            for j in range(i + 1, n):
                if (
                    sorted_patients[j].patient_id
                    < sorted_patients[min_index].patient_id
                ):
                    min_index = j

            if min_index != i:
                sorted_patients[i], sorted_patients[min_index] = (
                    sorted_patients[min_index],
                    sorted_patients[i],
                )

        return sorted_patients