"""
Hospital Management Service Layer with SQLite Persistence Integration.

Architectural Bridge uniting our custom Data Structures & Algorithms with durable storage:
    1. Master Registry: Dynamic Array (PatientList) + Binary Search & Linear Search
    2. Emergency Triage: Priority Queue (Binary Max-Heap)
    3. Routine Outpatient Clinic: FIFO Queue (Linked-Node Queue)
    4. Clinical Audit & Rollback: LIFO Stack (Undo Stack)
    5. Sorting & Analytics: MergeSort (Stable) & QuickSort (In-place)
    6. Durable Storage: SQLite persistence with in-memory hydration
"""

from typing import List, Optional, Dict, Any
from models.patient import Patient
from models.database import init_db, save_patient, load_all_patients, delete_patient_db
from data_structures.patient_list import PatientList
from data_structures.linked_list import LinkedList
from data_structures.queue import Queue
from data_structures.stack import Stack
from data_structures.priority_queue import EmergencyPriorityQueue
from algorithms.binary_search import BinarySearch
from algorithms.merge_sort import MergeSort
from algorithms.quick_sort import QuickSort


class HospitalService:
    """
    Unified Hospital Management Service orchestrating DSA operations and syncing with SQLite.
    """

    def __init__(self, use_db: bool = True) -> None:
        self.use_db = use_db

        # Master Patient Database (Dynamic Array)
        self.patient_registry: PatientList = PatientList()

        # Emergency Department Triage (Binary Max-Heap Priority Queue)
        self.emergency_queue: EmergencyPriorityQueue = EmergencyPriorityQueue()

        # Routine Outpatient Department (FIFO Queue)
        self.outpatient_queue: Queue = Queue()

        # Clinical Audit Trail & Undo History (LIFO Stack)
        self.undo_stack: Stack[Dict[str, Any]] = Stack[Dict[str, Any]]()

        # Transfer / Observation Splicing Chain (Singly Linked List)
        self.transfer_chain: LinkedList = LinkedList()

        if self.use_db:
            init_db()
            self._hydrate_from_db()

    def _hydrate_from_db(self) -> None:
        """Hydrates in-memory data structures from durable SQLite storage on startup."""
        records = load_all_patients()
        for rec in records:
            patient = Patient(
                patient_id=rec["patient_id"],
                name=rec["name"],
                age=rec["age"],
                blood_group=rec["blood_group"],
                priority=rec["priority"],
            )
            patient.status = rec["status"]
            self.patient_registry.add_patient(patient)

            if rec["status"] == "Waiting":
                if (
                    rec["department"] == "Emergency"
                    or rec["priority"] == "Critical"
                ):
                    self.emergency_queue.enqueue(patient)
                else:
                    self.outpatient_queue.enqueue(patient)

    # ------------------------------------------------------------------
    # Patient Registration & Master Database Operations
    # ------------------------------------------------------------------
    def register_patient(
        self,
        patient_id: int,
        name: str,
        age: int,
        blood_group: str,
        priority: str,
        department: str = "Outpatient",
    ) -> Patient:
        """Register a patient in the registry and route to the appropriate clinical queue."""
        existing = self.get_patient_by_id(patient_id)
        if existing:
            raise ValueError(f"Patient with ID {patient_id} already exists.")

        patient = Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            blood_group=blood_group,
            priority=priority,
        )

        # 1. Add to Master Registry (Dynamic Array)
        self.patient_registry.add_patient(patient)

        # 2. Record creation in Audit Stack (LIFO)
        self.undo_stack.push(
            {
                "action": "REGISTER",
                "patient_id": patient.patient_id,
                "snapshot": patient.to_dict(),
                "department": department,
            }
        )

        # 3. Route to proper clinical queue
        if department.lower() == "emergency" or priority == "Critical":
            self.emergency_queue.enqueue(patient)
        else:
            self.outpatient_queue.enqueue(patient)

        # 4. Sync with SQLite
        if self.use_db:
            save_patient(patient, department=department)

        return patient

    def get_patient_by_id(self, patient_id: int) -> Optional[Patient]:
        """Linear search across master registry."""
        return self.patient_registry.find_patient(patient_id)

    def get_patient_by_id_binary_search(
        self, patient_id: int
    ) -> Optional[Patient]:
        """O(log n) Binary Search over sorted records."""
        all_patients = self.patient_registry.get_all_patients()
        if not all_patients:
            return None
        sorted_patients = MergeSort.sort_by_patient_id(all_patients)
        return BinarySearch.search_by_patient_id(sorted_patients, patient_id)

    def get_patient_by_name(self, name: str) -> Optional[Patient]:
        """O(log n) Binary Search by name."""
        all_patients = self.patient_registry.get_all_patients()
        if not all_patients:
            return None
        sorted_by_name = QuickSort.sort_by_name(all_patients)
        return BinarySearch.search_by_name(sorted_by_name, name)

    def update_patient_details(
        self, patient_id: int, **kwargs: Any
    ) -> Optional[Patient]:
        """Update patient with automatic LIFO undo stack snapshot."""
        patient = self.get_patient_by_id(patient_id)
        if not patient:
            return None

        # Save snapshot to Undo Stack (O(1))
        self.undo_stack.push(
            {
                "action": "UPDATE",
                "patient_id": patient.patient_id,
                "snapshot": patient.to_dict(),
            }
        )

        patient.update_details(**kwargs)

        if self.use_db:
            save_patient(patient)

        return patient

    def discharge_patient(self, patient_id: int) -> bool:
        """Mark patient as Discharged and record in Audit Stack."""
        patient = self.get_patient_by_id(patient_id)
        if not patient:
            return False

        self.undo_stack.push(
            {
                "action": "DISCHARGE",
                "patient_id": patient.patient_id,
                "snapshot": patient.to_dict(),
            }
        )

        patient.discharge()

        if self.use_db:
            save_patient(patient)

        return True

    def get_all_patients(self, sort_by: str = "id") -> List[Patient]:
        """Retrieve all patients sorted by specified key ('id', 'name', 'age')."""
        patients = self.patient_registry.get_all_patients()
        if sort_by == "name":
            return QuickSort.sort_by_name(patients)
        elif sort_by == "age":
            return MergeSort.sort_by_age(patients)
        else:  # Default sort by id
            return MergeSort.sort_by_patient_id(patients)

    # ------------------------------------------------------------------
    # Emergency Department (Binary Max-Heap Priority Queue)
    # ------------------------------------------------------------------
    def treat_next_emergency_patient(self) -> Optional[Patient]:
        """Extract highest-priority patient from Emergency Heap in O(log n) time."""
        patient = self.emergency_queue.dequeue()
        if patient:
            patient.status = "In Treatment (ER)"
            self.undo_stack.push(
                {
                    "action": "TREAT_EMERGENCY",
                    "patient_id": patient.patient_id,
                    "snapshot": patient.to_dict(),
                }
            )
            if self.use_db:
                save_patient(patient, department="Emergency")
        return patient

    def peek_next_emergency_patient(self) -> Optional[Patient]:
        """O(1) peek at highest priority ER patient."""
        return self.emergency_queue.peek()

    def get_emergency_patients(self) -> List[Patient]:
        """Return all patients currently in emergency heap."""
        return [item.patient for item in self.emergency_queue.heap.heap]

    # ------------------------------------------------------------------
    # Outpatient Clinic (FIFO Queue)
    # ------------------------------------------------------------------
    def call_next_outpatient(self) -> Optional[Patient]:
        """Call next patient in FIFO arrival order in O(1) time."""
        patient = self.outpatient_queue.dequeue()
        if patient:
            patient.status = "In Consultation"
            self.undo_stack.push(
                {
                    "action": "CALL_OUTPATIENT",
                    "patient_id": patient.patient_id,
                    "snapshot": patient.to_dict(),
                }
            )
            if self.use_db:
                save_patient(patient, department="Outpatient")
        return patient

    def peek_next_outpatient(self) -> Optional[Patient]:
        """O(1) peek at next outpatient."""
        return self.outpatient_queue.peek()

    def get_outpatient_patients(self) -> List[Patient]:
        """Return all patients currently in outpatient queue."""
        return self.outpatient_queue.to_list()

    # ------------------------------------------------------------------
    # Clinical Rollback & Audit History (LIFO Stack)
    # ------------------------------------------------------------------
    def rollback_last_action(self) -> Optional[Dict[str, Any]]:
        """Reverses the most recent clinical action recorded on the Undo Stack in O(1) time."""
        last_entry = self.undo_stack.pop()
        if not last_entry:
            return None

        action = last_entry["action"]
        pid = last_entry["patient_id"]
        snapshot = last_entry["snapshot"]

        patient = self.get_patient_by_id(pid)

        if action in ("UPDATE", "DISCHARGE", "TREAT_EMERGENCY", "CALL_OUTPATIENT"):
            if patient:
                patient.name = snapshot["name"]
                patient.age = snapshot["age"]
                patient.blood_group = snapshot["blood_group"]
                patient.priority = snapshot["priority"]
                patient.status = snapshot["status"]
                if self.use_db:
                    save_patient(patient)
        elif action == "REGISTER":
            if patient:
                self.patient_registry.remove_patient(pid)
                if self.use_db:
                    delete_patient_db(pid)

        return last_entry

    def get_action_history(self) -> List[Dict[str, Any]]:
        """Return full audit trail from TOP to BOTTOM."""
        return self.undo_stack.to_list()

    # ------------------------------------------------------------------
    # Hospital Dashboard Statistics
    # ------------------------------------------------------------------
    def get_dashboard_statistics(self) -> Dict[str, Any]:
        """Computes real-time hospital KPIs across all data structures."""
        all_patients = self.patient_registry.get_all_patients()
        total_registered = len(all_patients)

        waiting = sum(1 for p in all_patients if p.status == "Waiting")
        in_treatment = sum(
            1
            for p in all_patients
            if p.status in ("In Treatment (ER)", "In Consultation")
        )
        discharged = sum(1 for p in all_patients if p.status == "Discharged")

        priority_breakdown = {
            "Critical": sum(
                1 for p in all_patients if p.priority == "Critical"
            ),
            "High": sum(1 for p in all_patients if p.priority == "High"),
            "Medium": sum(1 for p in all_patients if p.priority == "Medium"),
            "Low": sum(1 for p in all_patients if p.priority == "Low"),
        }

        return {
            "total_patients": total_registered,
            "emergency_queue_size": self.emergency_queue.size(),
            "outpatient_queue_size": self.outpatient_queue.size(),
            "undo_stack_depth": self.undo_stack.size(),
            "waiting_count": waiting,
            "in_treatment_count": in_treatment,
            "discharged_count": discharged,
            "priority_breakdown": priority_breakdown,
        }
