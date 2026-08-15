"""
Unit tests for HospitalService orchestration layer.
"""

from services.hospital_service import HospitalService


def test_hospital_service_workflows():
    # Use isolated in-memory service without touching shared SQLite DB
    service = HospitalService(use_db=False)

    # 1. Register patients
    p1 = service.register_patient(
        101, "Alice Walker", 29, "O+", "Low", department="Outpatient"
    )
    p2 = service.register_patient(
        102, "Bob Vance", 58, "A+", "Critical", department="Emergency"
    )
    p3 = service.register_patient(
        103, "Charlie Day", 36, "B-", "High", department="Emergency"
    )

    stats = service.get_dashboard_statistics()
    assert stats["total_patients"] == 3
    assert stats["emergency_queue_size"] == 2
    assert stats["outpatient_queue_size"] == 1

    # 2. Binary search lookup
    found = service.get_patient_by_id_binary_search(102)
    assert found is not None
    assert found.name == "Bob Vance"

    # 3. Emergency Treatment (must treat Critical before High)
    treated_1 = service.treat_next_emergency_patient()
    assert treated_1 is not None
    assert treated_1.patient_id == 102
    assert treated_1.priority == "Critical"
    assert treated_1.status == "In Treatment (ER)"

    # 4. Outpatient Consultation (FIFO)
    outpatient_1 = service.call_next_outpatient()
    assert outpatient_1 is not None
    assert outpatient_1.patient_id == 101
    assert outpatient_1.status == "In Consultation"

    # 5. Patient Update and Undo Rollback
    service.update_patient_details(101, name="Alice Walker-Smith", age=30)
    p1_updated = service.get_patient_by_id(101)
    assert p1_updated.name == "Alice Walker-Smith"
    assert p1_updated.age == 30

    # Rollback update
    service.rollback_last_action()
    p1_reverted = service.get_patient_by_id(101)
    assert p1_reverted.name == "Alice Walker"
    assert p1_reverted.age == 29


if __name__ == "__main__":
    test_hospital_service_workflows()
    print("All HospitalService unit tests passed successfully!")
