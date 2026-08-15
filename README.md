# 🏥 Emergency Hospital Patient Management System
### *A Practical Full-Stack & CLI Healthcare Architecture Grounded in Core Data Structures & Algorithms*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Tests](https://img.shields.io/badge/Tests-25%20Passing%20(100%25)-brightgreen.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![WSGI](https://img.shields.io/badge/Production%20WSGI-Waitress-orange.svg)](https://docs.pylonsproject.org/projects/waitress/)
[![DSA](https://img.shields.io/badge/Algorithms-Binary%20Heap%20%7C%20MergeSort%20%7C%20BinarySearch-purple.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🌟 Executive Overview

The **Emergency Hospital Patient Management System** is an engineering project designed to bridge the gap between **theoretical Computer Science (Data Structures & Algorithms)** and **real-world backend systems architecture**.

Rather than relying on high-level Python standard abstractions (`collections.deque`, `heapq`, `list.sort`), every critical operational pipeline is **engineered from first principles**:
- **Triage Acuity Sorting:** Custom Complete Binary Max-Heap with arrival tie-breaking.
- **Fair Walk-In Admissions:** Custom dual-pointer FIFO Linked Queue.
- **Clinical Undo & Rollbacks:** Custom single-pointer LIFO Linked Stack.
- **Urgent Zero-Shift Admissions:** Custom Singly Linked List with head pointer rewiring.
- **Instant Patient Lookups:** Logarithmic $\mathcal{O}(\log_2 n)$ Binary Search with statistical comparison tracking.
- **Stable Clinical Reports:** Guaranteed $\Theta(n \log_2 n)$ Merge Sort and in-place Quick Sort.

The system is deployed as a **unified multi-device web platform** (accessible via desktop, phone, or tablet over LAN) as well as an **interactive terminal command hub**.

---

## 🏛️ Architectural Mapping: Features vs. Custom DSA

```
+---------------------------------------------------------------------------------------------------------------+
|                                      FLASK WEB DASHBOARD & REST API                                           |
|                            (http://localhost:5000/ • /api/stats • /api/patients)                              |
+---------------------------------------------------------------------------------------------------------------+
                                                       |
                                                       v
+---------------------------------------------------------------------------------------------------------------+
|                                          HOSPITAL SERVICE LAYER                                               |
|                                     (services/hospital_service.py)                                            |
+---------------------------------------------------------------------------------------------------------------+
          |                         |                        |                      |                   |
          v                         v                        v                      v                   v
+--------------------+   +--------------------+   +--------------------+   +------------------+   +-------------+
|    MASTER LIST     |   |  EMERGENCY TRIAGE  |   |     OUTPATIENT     |   |   AUDIT TRAIL    |   | PERSISTENCE |
|   (Dynamic Array)  |   | (Binary Max-Heap)  |   |    (FIFO Queue)    |   |   (LIFO Stack)   |   |  (SQLite)   |
|  data_structures/  |   |  data_structures/  |   |  data_structures/  |   | data_structures/ |   |   models/   |
|  patient_list.py   |   | priority_queue.py  |   |      queue.py      |   |     stack.py     |   | database.py |
+--------------------+   +--------------------+   +--------------------+   +------------------+   +-------------+
          |                                                                         |
          v                                                                         v
+--------------------------------------------------------------------+    +-------------------+
|                       ALGORITHMS ENGINE                            |    |   UNDO/ROLLBACK   |
|   • Binary Search (O(log n))   • Merge Sort (Stable O(n log n))    |    |  O(1) pop & state |
|   • Quick Sort (O(n log n))    • Bubble & Selection Sort (O(n²))   |    |    restoration    |
+--------------------------------------------------------------------+    +-------------------+
```

---

## 📐 Formal Asymptotic & Mathematical Analysis

| Component | Mathematical Model / Recurrence | Best Case | Average Case | Worst Case | Space Complexity | Real-World Hospital Mapping |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Dynamic Array** | $\text{Addr}(i) = \text{Base} + i \cdot \text{Size}$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(n)$ | Master Registry Random Access Lookup |
| **Singly Linked List** | $\text{Node} = (\text{data}, \text{next})$ | $\Theta(1)$ | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | $\Theta(n)$ | Zero-Shift Urgent Patient Prepending |
| **FIFO Queue** | Dual-pointer chain ($\text{front}, \text{rear}$) | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(n)$ | Outpatient Arrival Order Triage Line |
| **LIFO Stack** | Single-pointer chain ($\text{top}$) | $\Theta(1)$ | $\Theta(1)$ | $\Theta(1)$ | $\Theta(n)$ | Clinical Snapshot Undo & Audit Trail |
| **Binary Max-Heap** | Height $h = \lfloor \log_2 n \rfloor$ | $\Theta(1)$ (peek) | $\Theta(\log_2 n)$ | $\mathcal{O}(\log_2 n)$ | $\Theta(1)$ aux | Emergency Acuity Priority Dispatch |
| **Binary Search** | $T(n) = T(\lfloor n/2 \rfloor) + \Theta(1)$ | $\Omega(1)$ | $\Theta(\log_2 n)$ | $\mathcal{O}(\log_2 n)$ | $\Theta(1)$ | $10,000\text{ records} \rightarrow \mathbf{\le 14\text{ comparisons}}$ |
| **Merge Sort** | $T(n) = 2T(n/2) + \Theta(n)$ | $\Omega(n \log_2 n)$ | $\Theta(n \log_2 n)$ | $\mathcal{O}(n \log_2 n)$ | $\Theta(n)$ | Stable Clinical Reporting |
| **Quick Sort** | $T(n) = 2T(n/2) + \Theta(n)$ | $\Omega(n \log_2 n)$ | $\Theta(n \log_2 n)$ | $\mathcal{O}(n^2)$ | $\mathcal{O}(\log_2 n)$ stack | High-Throughput In-Place Sorting |
| **Bubble Sort** | $\sum_{i=1}^{n-1} (n - i) = \frac{n^2 - n}{2}$ | $\Omega(n)$ (flag) | $\Theta(n^2)$ | $\mathcal{O}(n^2)$ | $\Theta(1)$ | Algorithmic Baseline Benchmark |
| **Selection Sort** | $\sum_{i=1}^{n-1} (n - i) = \frac{n^2 - n}{2}$ | $\Omega(n^2)$ | $\Theta(n^2)$ | $\mathcal{O}(n^2)$ | $\Theta(1)$ | Minimum Data Movement ($\le n-1$ swaps) |

---

## ⚡ Empirical Benchmarking Results

Our built-in benchmarking engine measures exact comparison counts and wall-clock execution timings:

### **Search Benchmark ($N = 10,000$ Patients)**
```text
Target Patient ID: 10,000 (Worst-Case Search at End of Dataset)
-----------------------------------------------------------------
Linear Search (Unsorted) :  10,000 comparisons | Time: 0.3092 ms | Complexity: O(n)
Binary Search (Ordered)  :      14 comparisons | Time: 0.0112 ms | Complexity: O(log2 n)
-----------------------------------------------------------------
Speedup Factor           :  714x fewer operations!
```

### **Sorting Benchmark (Runtime in Milliseconds)**
```text
Dataset Size (N)   | Bubble Sort  | Selection Sort | Merge Sort (Stable) | Quick Sort (In-Place)
-------------------------------------------------------------------------------------------------
N = 500            |     7.52 ms  |       4.45 ms  |            0.69 ms  |              0.39 ms
N = 1,000          |    32.24 ms  |      17.43 ms  |            2.15 ms  |              0.88 ms
N = 2,000          |   137.80 ms  |      66.06 ms  |            3.01 ms  |              2.06 ms
```

> **Key Insight:** As $N$ doubles from $1,000 \rightarrow 2,000$, $\mathcal{O}(n^2)$ algorithms scale quadratically ($4.3\times$ increase), whereas Merge Sort and Quick Sort scale quasi-linearly ($\approx 1.4\times$ increase).

---

## 📂 Project Directory Structure

```
EmergencyHospitalSystem/
├── app.py                      # Unified Deployment Hub (CLI & Multi-Device WSGI Server)
├── wsgi.py                     # Production WSGI entrypoint for Cloud
├── start.bat                   # Windows One-Click Double-Click Launcher
├── Dockerfile                  # Containerized deployment manifest
├── Procfile                    # Render / Railway / Heroku deployment manifest
├── requirements.txt            # Python dependencies (Flask, Waitress, Pytest)
├── hospital.db                 # SQLite backing database
│
├── models/
│   ├── patient.py              # Patient entity model
│   └── database.py             # SQLite persistence & data structure hydration
│
├── data_structures/
│   ├── linked_list.py          # Singly Linked List (Node, LinkedList)
│   ├── patient_list.py         # Dynamic Array patient management
│   ├── queue.py                # FIFO Linked-Node Queue
│   ├── stack.py                # LIFO Linked-Node Stack
│   └── priority_queue.py       # Complete Binary Max-Heap & EmergencyPriorityQueue
│
├── algorithms/
│   ├── binary_search.py        # O(log n) iterative binary search with stats
│   ├── merge_sort.py           # O(n log n) stable merge sort
│   ├── quick_sort.py           # O(n log n) in-place Lomuto quick sort
│   ├── bubble_sort.py          # Adaptive O(n²) comparison sort
│   ├── selection_sort.py       # O(n²) minimum swap sort
│   └── benchmark.py            # Automated empirical runtime benchmark
│
├── services/
│   └── hospital_service.py     # Orchestration service bridging DSA with UI & DB
│
├── routes/
│   ├── api_routes.py           # REST API endpoints (/api/*)
│   └── web_routes.py           # Web Dashboard endpoints (/, /benchmarks, /learn, /tests)
│
├── templates/
│   ├── base.html               # Responsive Bootstrap 5 layout & navigation
│   ├── index.html              # Interactive Hospital Triage Dashboard
│   ├── benchmarks.html         # Live Empirical Speed Benchmark UI
│   ├── learn.html              # Mathematical & Structural Walkthrough
│   └── tests.html              # Web-based pytest execution console
│
├── static/
│   └── css/style.css           # Custom medical styling
│
└── tests/
    ├── test_linked_list.py     # Linked List unit tests
    ├── test_queue.py           # FIFO Queue unit tests
    ├── test_stack.py           # LIFO Stack unit tests
    ├── test_priority_queue.py  # Binary Max-Heap & tie-break tests
    ├── test_algorithms.py      # Searching & Sorting algorithmic tests
    ├── test_service.py         # Hospital service integration tests
    └── test_routes.py          # Flask Web & REST API tests
```

---

## 🚀 Quick Start Guide

### 1. Installation & Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/EmergencyHospitalSystem.git
cd EmergencyHospitalSystem

# Create and activate virtual environment
python -m venv .venv

# On Windows:
.\.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 2. Running via Interactive Terminal Hub

```bash
python app.py
```
*(On Windows, you can also double-click **`start.bat`**).*

Presents an interactive menu:
```text
===========================================================================
EMERGENCY HOSPITAL PATIENT MANAGEMENT SYSTEM (UNIFIED DSA HUB)
===========================================================================
  [1] Start Multi-Device Web Server (http://localhost:5000/)
  [2] Run Terminal DSA Learning Walkthrough
  [3] Run Algorithmic Speed Benchmarks
  [4] Run Automated Test Suite (pytest)
  [5] All-in-One: Run Verification Tests & Launch Server
  [0] Exit
===========================================================================
Enter option [0-5]: 
```

---

### 3. Direct CLI Command Flags

```bash
# Start multi-device web server directly
python app.py --serve

# Start server on custom port/host
python app.py --serve --port 8080 --host 0.0.0.0

# Run terminal DSA walkthrough
python app.py --cli

# Run empirical algorithm benchmarks
python app.py --benchmark

# Run automated pytest suite
python app.py --test

# Run tests, benchmarks, walkthrough, and start server
python app.py --all
```

---

## 📱 Multi-Device LAN Access (Phones, Tablets, Laptops)

When starting the server (`python app.py --serve`), the application binds to `0.0.0.0` and detects your local IPv4 address:

```text
===========================================================================
EMERGENCY HOSPITAL SYSTEM: MULTI-DEVICE SERVER
===========================================================================
  * This Computer (Localhost) : http://127.0.0.1:5000/
  * Multiple Devices (LAN/WiFi): http://192.168.1.15:5000/
  * Speed Benchmarking Engine  : http://192.168.1.15:5000/benchmarks
  * Mathematical Walkthrough   : http://192.168.1.15:5000/learn
  * Automated Test Suite       : http://192.168.1.15:5000/tests
===========================================================================
```

1. Connect your **phone, tablet, or another laptop** to the **same Wi-Fi network**.
2. Open your mobile browser and enter: **`http://<YOUR_LAN_IP>:5000/`**.
3. Enjoy full interactive access on mobile!

---

## 🧪 Testing & Quality Assurance

Run the automated test suite covering all 25 unit and integration tests:

```bash
pytest -v
```

### **Test Suite Summary:**
- `tests/test_algorithms.py`: Verified Binary Search bounds, Merge Sort stability, Quick Sort partitioning.
- `tests/test_linked_list.py`: Verified head prepends, pointer rewiring, linear deletions.
- `tests/test_priority_queue.py`: Verified Max-Heap invariants and FIFO tie-breaking on identical acuity.
- `tests/test_queue.py`: Verified FIFO arrival ordering and empty-state resilience.
- `tests/test_stack.py`: Verified LIFO clinical state undo and rollback workflows.
- `tests/test_service.py`: Verified cross-module orchestration and statistics.
- `tests/test_routes.py`: Verified REST API responses and Web view rendering.

---

## 🌐 REST API Reference

| Method | Endpoint | Description | Sample Parameters / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/stats` | Retrieve real-time hospital KPIs & queue counts | None |
| `GET` | `/api/patients?sort_by=name` | Retrieve all patients sorted by key | `sort_by` (`id`, `name`, `age`) |
| `POST` | `/api/patients` | Register new patient into triage | `{"patient_id": 106, "name": "...", "age": 30, "blood_group": "O+", "priority": "High", "department": "Emergency"}` |
| `GET` | `/api/patients/search?id=102` | Search patient using Binary Search | `id` or `name`, `method=binary` |
| `POST` | `/api/emergency/treat-next` | Treat highest priority ER patient via Binary Max-Heap | None |
| `POST` | `/api/outpatient/call-next` | Call next outpatient via FIFO Queue | None |
| `POST` | `/api/audit/rollback` | Rollback most recent clinical action via LIFO Stack | None |
| `GET` | `/api/benchmark/run` | Trigger empirical speed benchmark | `size=1000&search_size=10000` |
| `POST` | `/api/tests/run` | Trigger live pytest execution | None |

---

## 📄 License

This project is open-source and available under the **MIT License**.
