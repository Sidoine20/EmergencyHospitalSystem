from models.patient import Patient
from algorithms.selection_sort import SelectionSort

class PatientList:
    """
    Stores and manages all patients using a dynamic array (Python list).
    """

    def __init__(self):
        self.patients = []

    def add_patient(self, patient):
        """
        Adds a new patient to the registry.

        Time Complexity:
            Average: O(1)
        """
        self.patients.append(patient)

    def get_all_patients(self):
        """
        Returns all registered patients.

        Time Complexity:
            O(1)
        """
        return self.patients

    def find_patient(self, patient_id):
        """
        Searches for a patient using Linear Search.

        Time Complexity:
            Worst Case: O(n)
        """
        for patient in self.patients:
            if patient.patient_id == patient_id:
                return patient

        return None

    def update_patient(self, patient_id, **kwargs):
        """
        Updates an existing patient's information.

        Time Complexity:
            O(n)
        """
        patient = self.find_patient(patient_id)

        if patient:
            patient.update_details(**kwargs)
            return True

        return False

    def remove_patient(self, patient_id):
        """
        Removes a patient from the registry.

        Time Complexity:
            O(n)
        """
        patient = self.find_patient(patient_id)

        if patient:
            self.patients.remove(patient)
            return True

        return False

    def display_patients(self):
        """
        Displays every patient.

        Time Complexity:
            O(n)
        """
        if not self.patients:
            print("No patients registered.")
            return

        for patient in self.patients:
            print(patient)
            print("-" * 40)

    def selection_sort_by_patient_id(self):
        """
        Returns patients sorted by Patient ID.

        using Selection Sort.
        """
        return SelectionSort.sort_by_patient_id(self.patients)