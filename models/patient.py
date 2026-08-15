class Patient:
    """
    Represents a single patient in the hospital.
    """

    def __init__(self, patient_id, name, age, blood_group, priority):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.blood_group = blood_group
        self.priority = priority
        self.status = "Waiting"

    def update_details(self, name=None, age=None, blood_group=None, priority=None):
        """
        Update patient information.
        Only the provided values will be changed.
        """
        if name is not None:
            self.name = name

        if age is not None:
            self.age = age

        if blood_group is not None:
            self.blood_group = blood_group

        if priority is not None:
            self.priority = priority

    def discharge(self):
        """Marks the patient as discharged."""
        self.status = "Discharged"

    def to_dict(self):
        """
        Returns the patient information as a dictionary.
        Useful later for APIs and JSON responses.
        """
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "age": self.age,
            "blood_group": self.blood_group,
            "priority": self.priority,
            "status": self.status
        }

    def __str__(self):
        return (
            f"Patient ID : {self.patient_id}\n"
            f"Name       : {self.name}\n"
            f"Age        : {self.age}\n"
            f"Blood Group: {self.blood_group}\n"
            f"Priority   : {self.priority}\n"
            f"Status     : {self.status}"
        )