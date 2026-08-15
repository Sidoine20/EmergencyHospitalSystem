"""
SQLite Persistence Layer for Emergency Hospital System.

Serves as the durable on-disk backing store.
When the application boots, patients are hydrated from SQLite into our in-memory
Data Structures (Binary Max-Heap, FIFO Queue, Dynamic Array, Undo Stack).
"""

import sqlite3
import os
from typing import List, Optional
from models.patient import Patient

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hospital.db"
)


def init_db(db_path: str = DB_PATH) -> None:
    """Creates the SQLite database tables if they do not exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            blood_group TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Waiting',
            department TEXT NOT NULL DEFAULT 'Outpatient',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def save_patient(patient: Patient, department: str = "Outpatient", db_path: str = DB_PATH) -> None:
    """Inserts or updates a patient in the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO patients (patient_id, name, age, blood_group, priority, status, department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(patient_id) DO UPDATE SET
            name = excluded.name,
            age = excluded.age,
            blood_group = excluded.blood_group,
            priority = excluded.priority,
            status = excluded.status,
            department = excluded.department
    """,
        (
            patient.patient_id,
            patient.name,
            patient.age,
            patient.blood_group,
            patient.priority,
            patient.status,
            department,
        ),
    )
    conn.commit()
    conn.close()


def load_all_patients(db_path: str = DB_PATH) -> List[dict]:
    """Loads all patient records from SQLite."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY patient_id ASC")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result


def delete_patient_db(patient_id: int, db_path: str = DB_PATH) -> bool:
    """Deletes a patient record from SQLite."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM patients WHERE patient_id = ?", (patient_id,)
    )
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0
