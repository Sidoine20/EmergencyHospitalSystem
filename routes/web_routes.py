from flask import Blueprint, render_template, request, redirect, url_for, flash
import subprocess
import sys
from routes.api_routes import hospital_service

web_bp = Blueprint("web", __name__)


@web_bp.route("/")
def index():
    """Renders the comprehensive Hospital DSA Dashboard."""
    sort_by = request.args.get("sort_by", "id")
    patients = hospital_service.get_all_patients(sort_by=sort_by)
    emergency_list = hospital_service.get_emergency_patients()
    outpatient_list = hospital_service.get_outpatient_patients()
    audit_history = hospital_service.get_action_history()
    stats = hospital_service.get_dashboard_statistics()

    # Search result if provided
    search_query = request.args.get("search_query", "").strip()
    search_result = None
    search_stats = None

    if search_query:
        if search_query.isdigit():
            # Perform Binary Search by ID
            from algorithms.merge_sort import MergeSort
            from algorithms.binary_search import BinarySearch

            sorted_by_id = MergeSort.sort_by_patient_id(
                hospital_service.patient_registry.get_all_patients()
            )
            found, comparisons = BinarySearch.search_with_stats(
                sorted_by_id, int(search_query)
            )
            search_result = found
            search_stats = {
                "algorithm": "Binary Search (O(log n))",
                "comparisons": comparisons,
            }
        else:
            # Perform Binary Search by Name
            search_result = hospital_service.get_patient_by_name(search_query)
            search_stats = {"algorithm": "Binary Search by Name (O(log n))"}

    return render_template(
        "index.html",
        active_tab="dashboard",
        patients=patients,
        emergency_list=emergency_list,
        outpatient_list=outpatient_list,
        audit_history=audit_history,
        stats=stats,
        current_sort=sort_by,
        search_query=search_query,
        search_result=search_result,
        search_stats=search_stats,
    )


@web_bp.route("/benchmarks")
def benchmarks():
    """Renders the interactive Algorithmic Benchmarking page."""
    return render_template("benchmarks.html", active_tab="benchmarks")


@web_bp.route("/learn")
def learn():
    """Renders the Interactive DSA Walkthrough & Architecture visualizer."""
    return render_template("learn.html", active_tab="learn")


@web_bp.route("/tests")
def tests_view():
    """Renders the Automated Test Suite page."""
    return render_template("tests.html", active_tab="tests")


@web_bp.route("/register", methods=["POST"])
def register():
    """Handle HTML form patient registration."""
    try:
        pid = int(request.form["patient_id"])
        name = request.form["name"].strip()
        age = int(request.form["age"])
        blood = request.form["blood_group"]
        priority = request.form["priority"]
        dept = request.form.get("department", "Outpatient")

        hospital_service.register_patient(
            patient_id=pid,
            name=name,
            age=age,
            blood_group=blood,
            priority=priority,
            department=dept,
        )
        flash(f"Patient {name} registered successfully into {dept}!", "success")
    except Exception as e:
        flash(f"Error registering patient: {str(e)}", "danger")

    return redirect(url_for("web.index"))


@web_bp.route("/emergency/treat", methods=["POST"])
def treat_emergency():
    """Treat next patient from Emergency Max-Heap."""
    patient = hospital_service.treat_next_emergency_patient()
    if patient:
        flash(
            f"Treated Emergency Patient: {patient.name} (Priority: {patient.priority})",
            "warning",
        )
    else:
        flash("Emergency Queue is currently empty.", "info")
    return redirect(url_for("web.index"))


@web_bp.route("/outpatient/call", methods=["POST"])
def call_outpatient():
    """Call next patient from FIFO Outpatient Queue."""
    patient = hospital_service.call_next_outpatient()
    if patient:
        flash(f"Calling Outpatient: {patient.name}", "primary")
    else:
        flash("Outpatient Queue is currently empty.", "info")
    return redirect(url_for("web.index"))


@web_bp.route("/audit/undo", methods=["POST"])
def undo():
    """Undo most recent clinical action from Stack."""
    reverted = hospital_service.rollback_last_action()
    if reverted:
        flash(
            f"Successfully rolled back action: {reverted['action']} on Patient #{reverted['patient_id']}",
            "success",
        )
    else:
        flash("Undo stack is empty.", "info")
    return redirect(url_for("web.index"))


@web_bp.route("/patients/<int:patient_id>/discharge", methods=["POST"])
def discharge(patient_id: int):
    """Discharge patient."""
    success = hospital_service.discharge_patient(patient_id)
    if success:
        flash(f"Patient #{patient_id} has been discharged.", "secondary")
    return redirect(url_for("web.index"))
