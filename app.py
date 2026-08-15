"""
Emergency Hospital Patient Management System - Unified Deployment Hub.

Multi-Device Network Deployment & CLI DSA Hub:
1. Production Multi-Threaded WSGI Server (Waitress) + Multi-Device LAN Access
2. Interactive Web Dashboard & REST API
3. Terminal DSA Educational Walkthrough
4. Algorithmic Speed Benchmarks
5. Automated Test Suite (pytest)
"""

import sys
import socket
import argparse
import subprocess
import os
from flask import Flask
from routes.api_routes import api_bp
from routes.web_routes import web_bp


def get_local_ip() -> str:
    """Detects the host machine's primary Local Area Network (LAN) IPv4 address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"


def create_app() -> Flask:
    """Flask Application Factory."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "dev-emergency-hospital-dsa-secret-key"
    )

    # Register Blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    return app


def run_web_server(
    host: str = "0.0.0.0", port: int = 5000, use_production_wsgi: bool = True
) -> None:
    """
    Starts the multi-device web server.
    Binds to 0.0.0.0 so phones, tablets, and computers on the same network can connect.
    """
    local_ip = get_local_ip()
    app = create_app()

    print("=" * 75)
    print("EMERGENCY HOSPITAL SYSTEM: MULTI-DEVICE SERVER")
    print("=" * 75)
    print(f"  * This Computer (Localhost) : http://127.0.0.1:{port}/")
    print(f"  * Multiple Devices (LAN/WiFi): http://{local_ip}:{port}/")
    print(f"  * REST API Base Endpoint     : http://{local_ip}:{port}/api/")
    print(f"  * Speed Benchmarking Engine  : http://{local_ip}:{port}/benchmarks")
    print(f"  * Mathematical Walkthrough   : http://{local_ip}:{port}/learn")
    print(f"  * Automated Test Suite       : http://{local_ip}:{port}/tests")
    print("-" * 75)
    print(
        f"  [!] To open on your PHONE or TABLET: Connect to the same Wi-Fi and open:"
    )
    print(f"      👉 http://{local_ip}:{port}/")
    print("=" * 75)
    print("Press CTRL + C to stop the server.\n")

    if use_production_wsgi:
        try:
            from waitress import serve

            print(
                f"[WSGI] Running Waitress Production Server (Multi-Threaded)..."
            )
            serve(app, host=host, port=port, threads=8)
            return
        except ImportError:
            print(
                "[WSGI] Waitress not installed, falling back to standard server..."
            )

    app.run(host=host, port=port, debug=False)


def run_cli_walkthrough() -> None:
    """Runs the terminal DSA walkthrough demonstrating all 5 data structures & algorithms."""
    from models.patient import Patient
    from data_structures.patient_list import PatientList
    from data_structures.linked_list import LinkedList
    from data_structures.queue import Queue
    from data_structures.stack import Stack
    from data_structures.priority_queue import EmergencyPriorityQueue
    from algorithms.merge_sort import MergeSort
    from algorithms.binary_search import BinarySearch

    print("=" * 75)
    print("TERMINAL DSA WALKTHROUGH & ARCHITECTURAL VERIFICATION")
    print("=" * 75)

    # 1. Dynamic Array
    print("\n[1] Dynamic Array (PatientList - Master Registry):")
    registry = PatientList()
    registry.add_patient(Patient(101, "John Doe", 28, "O+", "High"))
    registry.add_patient(Patient(102, "Sarah Smith", 42, "A-", "Critical"))
    registry.display_patients()

    # 2. Singly Linked List
    print("\n[2] Singly Linked List (LinkedList - Zero-Shift Prepend):")
    ll = LinkedList()
    ll.append(Patient(101, "John Doe", 28, "O+", "High"))
    ll.prepend(Patient(104, "Emergency Arrival - Emma", 19, "AB-", "Critical"))
    ll.display()

    # 3. FIFO Queue
    print("\n[3] FIFO Triage Queue (Queue - Outpatient Arrival Sequence):")
    tq = Queue()
    tq.enqueue(Patient(101, "John Doe", 28, "O+", "High"))
    tq.enqueue(Patient(103, "David Brown", 35, "B+", "Medium"))
    served = tq.dequeue()
    print(f"  Called next outpatient [Theta(1)]: {served.name}")

    # 4. LIFO Stack
    print("\n[4] LIFO Action History & Undo Stack (Stack - Clinical Rollback):")
    st = Stack[dict]()
    p = Patient(101, "John Doe", 28, "O+", "Medium")
    st.push(p.to_dict())
    p.update_details(priority="High")
    reverted = st.pop()
    print(f"  Reverted priority from High back to: {reverted['priority']}")

    # 5. Complete Binary Max-Heap
    print("\n[5] Emergency Priority Queue (Binary Max-Heap - Urgent Triage):")
    er = EmergencyPriorityQueue()
    er.enqueue(Patient(201, "Low Flu", 24, "O+", "Low"))
    er.enqueue(Patient(204, "Critical Trauma", 62, "O-", "Critical"))
    er.enqueue(Patient(203, "High Asthma", 55, "B-", "High"))
    print("  Treating patients in clinical acuity order [O(log2 n)]:")
    while not er.is_empty():
        item = er.dequeue()
        print(f"    [{item.priority:<8}] ID: #{item.patient_id} - {item.name}")

    # 6. Sorting & Binary Search
    print("\n[6] MergeSort (Stable Theta(n log n)) & Binary Search (O(log2 n)):")
    records = [
        Patient(305, "Zoe Miller", 45, "O+", "Low"),
        Patient(302, "Alice Brown", 30, "A-", "Critical"),
        Patient(301, "Charlie Cox", 22, "AB+", "Medium"),
    ]
    sorted_p = MergeSort.sort_by_patient_id(records)
    found, comps = BinarySearch.search_with_stats(sorted_p, 302)
    print(
        f"  Binary Search found '{found.name}' in {comps} comparison(s) out of {len(sorted_p)} records."
    )
    print("=" * 75)


def run_benchmarks() -> None:
    """Runs empirical speed benchmarks."""
    from algorithms.benchmark import benchmark_search, benchmark_sorting

    benchmark_search(10000)
    benchmark_sorting((500, 1000, 2000))


def run_test_suite() -> int:
    """Runs automated pytest test suite."""
    print("=" * 75)
    print("RUNNING AUTOMATED PYTEST SUITE")
    print("=" * 75)
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"])
    return result.returncode


def interactive_terminal_menu() -> None:
    """Presents an interactive terminal choice menu."""
    local_ip = get_local_ip()
    while True:
        print("\n" + "=" * 75)
        print("EMERGENCY HOSPITAL PATIENT MANAGEMENT SYSTEM (UNIFIED DSA HUB)")
        print("=" * 75)
        print(f"  [1] Start Multi-Device Web Server (http://{local_ip}:5000/)")
        print("  [2] Run Terminal DSA Learning Walkthrough")
        print("  [3] Run Algorithmic Speed Benchmarks")
        print("  [4] Run Automated Test Suite (pytest)")
        print("  [5] All-in-One: Run Verification Tests & Launch Server")
        print("  [0] Exit")
        print("=" * 75)

        try:
            choice = input("Enter option [0-5]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if choice == "1":
            run_web_server()
            break
        elif choice == "2":
            run_cli_walkthrough()
        elif choice == "3":
            run_benchmarks()
        elif choice == "4":
            run_test_suite()
        elif choice == "5":
            code = run_test_suite()
            if code == 0:
                print("\nAll tests verified! Starting multi-device server...")
                run_web_server()
                break
            else:
                print("\nTests failed. Please check errors above.")
        elif choice in ("0", "exit", "quit", "q"):
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1, 2, 3, 4, 5, or 0.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Emergency Hospital Patient Management System - Unified Multi-Device Deployment Hub"
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Start the multi-device web server directly",
    )
    parser.add_argument(
        "--cli",
        "--walkthrough",
        action="store_true",
        help="Run the terminal DSA walkthrough",
    )
    parser.add_argument(
        "--benchmark", action="store_true", help="Run algorithmic benchmarks"
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the automated pytest test suite",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run tests, benchmarks, walkthrough, and start multi-device server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port for the web server (default: 5000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host address (default: 0.0.0.0 for all network interfaces)",
    )

    args = parser.parse_args()

    if args.serve:
        run_web_server(host=args.host, port=args.port)
    elif args.cli:
        run_cli_walkthrough()
    elif args.benchmark:
        run_benchmarks()
    elif args.test:
        sys.exit(run_test_suite())
    elif args.all:
        code = run_test_suite()
        run_benchmarks()
        run_cli_walkthrough()
        if code == 0:
            run_web_server(host=args.host, port=args.port)
    else:
        interactive_terminal_menu()


if __name__ == "__main__":
    main()
