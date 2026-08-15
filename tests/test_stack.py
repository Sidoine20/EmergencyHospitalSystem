"""
Unit tests for Stack (LIFO) data structure.
"""

from models.patient import Patient
from data_structures.stack import Stack


def test_empty_stack():
    s = Stack[str]()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    assert s.peek() is None
    assert s.pop() is None
    assert s.top is None


def test_push_and_lifo_order():
    s = Stack[str]()
    s.push("Check-in at reception")
    s.push("Triage assigned: Medium")
    s.push("Vitals recorded: BP 120/80")

    assert s.is_empty() is False
    assert s.size() == 3
    assert s.peek() == "Vitals recorded: BP 120/80"

    # LIFO Pop order
    assert s.pop() == "Vitals recorded: BP 120/80"
    assert s.size() == 2
    assert s.peek() == "Triage assigned: Medium"

    assert s.pop() == "Triage assigned: Medium"
    assert s.size() == 1

    assert s.pop() == "Check-in at reception"
    assert s.size() == 0
    assert s.is_empty() is True
    assert s.top is None


def test_patient_state_undo_workflow():
    # Stack used to save previous states of a patient for Rollback/Undo
    undo_stack = Stack[dict]()

    patient = Patient(101, "John Doe", 28, "O+", "Medium")

    # Step 1: Save state before 1st edit
    undo_stack.push(patient.to_dict())

    # Nurse changes priority to High
    patient.update_details(priority="High")
    assert patient.priority == "High"

    # Step 2: Save state before 2nd edit
    undo_stack.push(patient.to_dict())

    # Doctor accidentally changes name and age
    patient.update_details(name="Wrong Name", age=99)
    assert patient.name == "Wrong Name"

    # UNDO action 1 (revert doctor mistake)
    previous_state = undo_stack.pop()
    assert previous_state is not None
    patient.update_details(
        name=previous_state["name"],
        age=previous_state["age"],
        priority=previous_state["priority"],
    )
    assert patient.name == "John Doe"
    assert patient.age == 28
    assert patient.priority == "High"

    # UNDO action 2 (revert priority back to Medium)
    original_state = undo_stack.pop()
    assert original_state is not None
    patient.update_details(
        name=original_state["name"],
        age=original_state["age"],
        priority=original_state["priority"],
    )
    assert patient.priority == "Medium"
    assert undo_stack.is_empty() is True


if __name__ == "__main__":
    test_empty_stack()
    test_push_and_lifo_order()
    test_patient_state_undo_workflow()
    print("All Stack unit tests passed successfully!")
