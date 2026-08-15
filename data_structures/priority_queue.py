"""
Emergency Priority Queue backed by a Complete Binary Max-Heap.

Mathematical Foundations & Structural Invariants:
    1. Complete Binary Tree Properties:
       For a 0-indexed array representation storing n elements:
       - Height of Tree:        h = floor(log2(n))
       - Parent of node i:      floor((i - 1) / 2)
       - Left Child of node i:  2 * i + 1
       - Right Child of node i: 2 * i + 2
       - Leaf Nodes range:      indices floor(n / 2) to n - 1
       - Internal Nodes range:  indices 0 to floor(n / 2) - 1

    2. Max-Heap Structural Invariant:
       For every node i > 0: heap[parent(i)].priority >= heap[i].priority

    3. Asymptotic Complexities:
       - Peek Root:             Theta(1)
       - Sift-Up (Insert):      O(h) = O(log2(n))
       - Sift-Down (Extract):   O(h) = O(log2(n))
       - Total Auxiliary Space: Theta(1) additional memory over continuous array.
"""

from typing import Optional, List, Dict
from models.patient import Patient


# Priority weighting for emergency triage
PRIORITY_WEIGHTS: Dict[str, int] = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


class PriorityItem:
    """
    Encapsulates a Patient record with integer priority weights and monotonic arrival counters.
    """

    def __init__(self, patient: Patient, arrival_index: int) -> None:
        self.patient: Patient = patient
        self.priority_weight: int = PRIORITY_WEIGHTS.get(patient.priority, 1)
        self.arrival_index: int = arrival_index

    def has_higher_priority_than(self, other: "PriorityItem") -> bool:
        """
        Determines strict total order:
        1. Clinical Urgency Weight (Descending)
        2. Arrival Sequence Index (Ascending - FIFO tie-breaking)
        """
        if self.priority_weight != other.priority_weight:
            return self.priority_weight > other.priority_weight

        return self.arrival_index < other.arrival_index

    def __repr__(self) -> str:
        return (
            f"PriorityItem(id={self.patient.patient_id}, "
            f"priority='{self.patient.priority}', weight={self.priority_weight}, "
            f"arrival={self.arrival_index})"
        )


class BinaryMaxHeap:
    """
    Array-backed Complete Binary Max-Heap with O(log n) mutation bounds.
    """

    def __init__(self) -> None:
        self.heap: List[PriorityItem] = []

    def is_empty(self) -> bool:
        """Theta(1) check."""
        return len(self.heap) == 0

    def size(self) -> int:
        """Theta(1) cached count."""
        return len(self.heap)

    def peek(self) -> Optional[PriorityItem]:
        """
        Inspect root without extraction.
        Complexity: Theta(1)
        """
        if self.is_empty():
            return None
        return self.heap[0]

    def insert(self, item: PriorityItem) -> None:
        """
        Insert new element into heap.
        Time Complexity: O(log2(n))
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self) -> Optional[PriorityItem]:
        """
        Extract root and restore max-heap invariant.
        Time Complexity: O(log2(n))
        """
        if self.is_empty():
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        max_item: PriorityItem = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)

        return max_item

    # ------------------------------------------------------------------
    # Index Arithmetic
    # ------------------------------------------------------------------
    @staticmethod
    def parent_index(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def left_child_index(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def right_child_index(i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, index: int) -> None:
        """
        Restores max-heap invariant upward toward root.
        Time Complexity: O(log2(n))
        """
        current: int = index
        while current > 0:
            parent: int = self.parent_index(current)
            if self.heap[current].has_higher_priority_than(self.heap[parent]):
                self.heap[current], self.heap[parent] = (
                    self.heap[parent],
                    self.heap[current],
                )
                current = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        """
        Restores max-heap invariant downward toward leaves.
        Time Complexity: O(log2(n))
        """
        size: int = len(self.heap)
        current: int = index

        while True:
            left: int = self.left_child_index(current)
            right: int = self.right_child_index(current)
            highest_priority_idx: int = current

            if (
                left < size
                and self.heap[left].has_higher_priority_than(
                    self.heap[highest_priority_idx]
                )
            ):
                highest_priority_idx = left

            if (
                right < size
                and self.heap[right].has_higher_priority_than(
                    self.heap[highest_priority_idx]
                )
            ):
                highest_priority_idx = right

            if highest_priority_idx == current:
                break

            self.heap[current], self.heap[highest_priority_idx] = (
                self.heap[highest_priority_idx],
                self.heap[current],
            )
            current = highest_priority_idx


class EmergencyPriorityQueue:
    """
    Hospital Triage Priority Queue managing patients via BinaryMaxHeap with arrival counters.
    """

    def __init__(self) -> None:
        self.heap: BinaryMaxHeap = BinaryMaxHeap()
        self._arrival_counter: int = 0

    def is_empty(self) -> bool:
        return self.heap.is_empty()

    def size(self) -> int:
        return self.heap.size()

    def __len__(self) -> int:
        return self.heap.size()

    def enqueue(self, patient: Patient) -> None:
        """
        Enqueue a patient with their clinical priority.
        Time Complexity: O(log2(n))
        """
        self._arrival_counter += 1
        item = PriorityItem(patient, self._arrival_counter)
        self.heap.insert(item)

    def dequeue(self) -> Optional[Patient]:
        """
        Extract highest priority patient in emergency ward.
        Time Complexity: O(log2(n))
        """
        extracted = self.heap.extract_max()
        if extracted is None:
            return None
        return extracted.patient

    def peek(self) -> Optional[Patient]:
        """
        View highest priority patient.
        Time Complexity: Theta(1)
        """
        top_item = self.heap.peek()
        if top_item is None:
            return None
        return top_item.patient

    def display(self) -> None:
        if self.is_empty():
            print("Emergency Priority Queue is empty. No emergency patients.")
            return

        print(f"--- EMERGENCY TRIAGE HEAP (Total: {self.size()} patients) ---")
        for idx, item in enumerate(self.heap.heap):
            p = item.patient
            print(
                f"[Heap Index: {idx}] Priority: {p.priority:<8} | "
                f"ID: {p.patient_id} | Name: {p.name:<18} | Arrival #{item.arrival_index}"
            )
        print("-" * 60)
