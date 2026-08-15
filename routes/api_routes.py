import time
import subprocess
import sys
from flask import Blueprint, jsonify, request
from services.hospital_service import HospitalService
from algorithms.benchmark import generate_random_patients, BinarySearch, MergeSort, QuickSort, BubbleSort, SelectionSort

api_bp = Blueprint("api", __name__, url_prefix="/api")

# Shared singleton service instance
hospital_service = HospitalService()


# Pre-populate with sample patients for immediate interactive demo
def seed_sample_data():
    if hospital_service.patient_registry.get_all_patients():
        return
    hospital_service.register_patient(
        101, "John Doe", 28, "O+", "High", "Outpatient"
    )
    hospital_service.register_patient(
        102, "Sarah Smith", 42, "A-", "Critical", "Emergency"
    )
    hospital_service.register_patient(
        103, "David Brown", 35, "B+", "Medium", "Outpatient"
    )
    hospital_service.register_patient(
        104, "Emma Watson", 19, "AB-", "Critical", "Emergency"
    )
    hospital_service.register_patient(
        105, "Michael Scott", 45, "O-", "Low", "Outpatient"
    )


seed_sample_data()


@api_bp.route("/stats", methods=["GET"])
def get_stats():
    """Returns hospital KPIs and queue counts."""
    stats = hospital_service.get_dashboard_statistics()
    return jsonify({"success": True, "data": stats})


@api_bp.route("/patients", methods=["GET"])
def list_patients():
    """
    Get all patients sorted by specified algorithm/key.
    Query param: sort_by (id, name, age)
    """
    sort_by = request.args.get("sort_by", "id")
    patients = hospital_service.get_all_patients(sort_by=sort_by)
    return jsonify(
        {
            "success": True,
            "count": len(patients),
            "sort_applied": f"MergeSort/QuickSort by '{sort_by}'",
            "data": [p.to_dict() for p in patients],
        }
    )


@api_bp.route("/patients", methods=["POST"])
def register_patient():
    """Register a new patient."""
    data = request.get_json() or {}
    required = ["patient_id", "name", "age", "blood_group", "priority"]
    for field in required:
        if field not in data:
            return jsonify(
                {"success": False, "error": f"Missing field: {field}"}
            ), 400

    try:
        pid = int(data["patient_id"])
        age = int(data["age"])
        dept = data.get("department", "Outpatient")
        patient = hospital_service.register_patient(
            patient_id=pid,
            name=str(data["name"]),
            age=age,
            blood_group=str(data["blood_group"]),
            priority=str(data["priority"]),
            department=dept,
        )
        return (
            jsonify(
                {
                    "success": True,
                    "message": f"Patient {patient.name} registered into {dept}.",
                    "data": patient.to_dict(),
                }
            ),
            201,
        )
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400


@api_bp.route("/patients/search", methods=["GET"])
def search_patient():
    """Search for a patient using Binary Search (O(log n)) or Linear Search (O(n))."""
    pid = request.args.get("id")
    name = request.args.get("name")
    method = request.args.get("method", "binary")

    if pid:
        target_id = int(pid)
        if method == "binary":
            all_patients = (
                hospital_service.patient_registry.get_all_patients()
            )
            from algorithms.merge_sort import MergeSort
            from algorithms.binary_search import BinarySearch

            sorted_p = MergeSort.sort_by_patient_id(all_patients)
            found, comparisons = BinarySearch.search_with_stats(
                sorted_p, target_id
            )
            if found:
                return jsonify(
                    {
                        "success": True,
                        "algorithm": "Binary Search (O(log n))",
                        "comparisons_made": comparisons,
                        "data": found.to_dict(),
                    }
                )
        else:
            found = hospital_service.get_patient_by_id(target_id)
            if found:
                return jsonify(
                    {
                        "success": True,
                        "algorithm": "Linear Search (O(n))",
                        "data": found.to_dict(),
                    }
                )

        return jsonify(
            {"success": False, "error": f"Patient ID {pid} not found."}
        ), 404

    elif name:
        found = hospital_service.get_patient_by_name(name)
        if found:
            return jsonify(
                {
                    "success": True,
                    "algorithm": "Binary Search by Name (O(log n))",
                    "data": found.to_dict(),
                }
            )
        return jsonify(
            {"success": False, "error": f"Patient '{name}' not found."}
        ), 404

    return jsonify({"success": False, "error": "Specify ?id= or ?name="}), 400


@api_bp.route("/patients/<int:patient_id>", methods=["PATCH", "PUT"])
def update_patient(patient_id: int):
    """Update patient with automatic LIFO undo stack snapshot."""
    data = request.get_json() or {}
    updated = hospital_service.update_patient_details(patient_id, **data)
    if updated:
        return jsonify(
            {
                "success": True,
                "message": "Patient updated and saved to undo stack.",
                "data": updated.to_dict(),
            }
        )
    return jsonify(
        {"success": False, "error": f"Patient {patient_id} not found."}
    ), 404


@api_bp.route("/emergency/treat-next", methods=["POST"])
def treat_emergency():
    """Treat next highest-urgency patient from Binary Max-Heap."""
    patient = hospital_service.treat_next_emergency_patient()
    if patient:
        return jsonify(
            {
                "success": True,
                "message": f"Calling Critical/Urgent patient {patient.name} (Priority: {patient.priority}).",
                "data": patient.to_dict(),
            }
        )
    return jsonify(
        {
            "success": False,
            "message": "No patients currently waiting in Emergency Queue.",
        }
    ), 200


@api_bp.route("/outpatient/call-next", methods=["POST"])
def call_outpatient():
    """Call next patient from FIFO Outpatient Queue."""
    patient = hospital_service.call_next_outpatient()
    if patient:
        return jsonify(
            {
                "success": True,
                "message": f"Calling next outpatient {patient.name} (Arrival sequence).",
                "data": patient.to_dict(),
            }
        )
    return jsonify(
        {
            "success": False,
            "message": "No patients currently waiting in Outpatient Queue.",
        }
    ), 200


@api_bp.route("/audit/rollback", methods=["POST"])
def rollback_action():
    """Rollback most recent action from LIFO Stack."""
    result = hospital_service.rollback_last_action()
    if result:
        return jsonify(
            {
                "success": True,
                "message": f"Rolled back action: {result['action']} on Patient {result['patient_id']}.",
                "reverted_snapshot": result["snapshot"],
            }
        )
    return jsonify(
        {"success": False, "message": "Undo Stack is empty. Nothing to undo."}
    ), 200


@api_bp.route("/audit/history", methods=["GET"])
def get_audit_history():
    """Get full LIFO history of clinical events."""
    history = hospital_service.get_action_history()
    return jsonify({"success": True, "depth": len(history), "data": history})


# ------------------------------------------------------------------
# Live Benchmarking & Automated Test Suite Endpoints
# ------------------------------------------------------------------
@api_bp.route("/benchmark/run", methods=["GET", "POST"])
def run_benchmark_api():
    """Runs a live empirical speed benchmark and returns execution timings."""
    size = int(request.args.get("size", 1000))
    search_size = int(request.args.get("search_size", 10000))

    # 1. Search Benchmark
    from models.patient import Patient

    search_data = [
        Patient(i, f"Patient_{i}", 30, "O+", "Medium")
        for i in range(1, search_size + 1)
    ]
    target_id = search_size

    # Linear Search
    t0 = time.perf_counter()
    lin_comps = 0
    for p in search_data:
        lin_comps += 1
        if p.patient_id == target_id:
            break
    linear_ms = (time.perf_counter() - t0) * 1000

    # Binary Search
    t0 = time.perf_counter()
    _, bin_comps = BinarySearch.search_with_stats(search_data, target_id)
    binary_ms = (time.perf_counter() - t0) * 1000

    # 2. Sorting Benchmark
    patients = generate_random_patients(size)

    # Bubble Sort
    t0 = time.perf_counter()
    BubbleSort.sort_by_patient_id(patients)
    bubble_ms = (time.perf_counter() - t0) * 1000

    # Selection Sort
    t0 = time.perf_counter()
    SelectionSort.sort_by_patient_id(patients)
    selection_ms = (time.perf_counter() - t0) * 1000

    # Merge Sort
    t0 = time.perf_counter()
    MergeSort.sort_by_patient_id(patients)
    merge_ms = (time.perf_counter() - t0) * 1000

    # Quick Sort
    t0 = time.perf_counter()
    QuickSort.sort_by_patient_id(patients)
    quick_ms = (time.perf_counter() - t0) * 1000

    return jsonify(
        {
            "success": True,
            "dataset_size_sorting": size,
            "dataset_size_searching": search_size,
            "search_benchmark": {
                "linear_search": {
                    "comparisons": lin_comps,
                    "time_ms": round(linear_ms, 4),
                    "complexity": "O(n)",
                },
                "binary_search": {
                    "comparisons": bin_comps,
                    "time_ms": round(binary_ms, 4),
                    "complexity": "O(log n)",
                },
                "speedup_factor": (
                    lin_comps // bin_comps if bin_comps > 0 else 1
                ),
            },
            "sorting_benchmark": {
                "bubble_sort": {
                    "time_ms": round(bubble_ms, 2),
                    "complexity": "O(n²)",
                },
                "selection_sort": {
                    "time_ms": round(selection_ms, 2),
                    "complexity": "O(n²)",
                },
                "merge_sort": {
                    "time_ms": round(merge_ms, 2),
                    "complexity": "O(n log n)",
                    "stable": True,
                },
                "quick_sort": {
                    "time_ms": round(quick_ms, 2),
                    "complexity": "O(n log n)",
                    "in_place": True,
                },
            },
        }
    )


@api_bp.route("/tests/run", methods=["POST", "GET"])
def run_tests_api():
    """Triggers the pytest test runner and returns summary output."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return jsonify(
            {
                "success": result.returncode == 0,
                "output": result.stdout,
                "errors": result.stderr,
                "return_code": result.returncode,
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
