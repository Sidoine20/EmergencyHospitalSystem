"""
Integration tests for Flask Web Routes and REST API endpoints.
"""

import random
from app import create_app
from routes.api_routes import hospital_service


def test_flask_app_routes():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # 1. Test Dashboard Web Page
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Emergency Hospital" in resp.data
    assert b"Master Patient Registry" in resp.data

    # 2. Test REST API Stats
    resp_stats = client.get("/api/stats")
    assert resp_stats.status_code == 200
    json_data = resp_stats.get_json()
    assert json_data["success"] is True
    assert "total_patients" in json_data["data"]

    # 3. Test REST API Register with unique ID
    test_id = random.randint(50000, 99999)
    new_patient = {
        "patient_id": test_id,
        "name": f"Integration Test Patient {test_id}",
        "age": 50,
        "blood_group": "AB+",
        "priority": "Critical",
        "department": "Emergency",
    }
    resp_reg = client.post("/api/patients", json=new_patient)
    assert resp_reg.status_code == 201

    # 4. Test REST API Binary Search
    resp_search = client.get(f"/api/patients/search?id={test_id}&method=binary")
    assert resp_search.status_code == 200
    search_json = resp_search.get_json()
    assert search_json["success"] is True
    assert search_json["data"]["patient_id"] == test_id
    assert "comparisons_made" in search_json

    # 5. Test REST API Treat Emergency (Binary Max-Heap)
    resp_treat = client.post("/api/emergency/treat-next")
    assert resp_treat.status_code == 200

    # 6. Test REST API Undo Rollback (LIFO Stack)
    resp_undo = client.post("/api/audit/rollback")
    assert resp_undo.status_code == 200
    assert resp_undo.get_json()["success"] is True


if __name__ == "__main__":
    test_flask_app_routes()
    print("All Flask Web & API integration tests passed successfully!")
