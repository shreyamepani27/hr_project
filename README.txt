HR TRAINING MANAGEMENT & ANALYSIS SYSTEM
========================================

Features
--------
1. Add and maintain employee training records.
2. Track Completed, In Progress and Not Started status.
3. Search/filter records.
4. Calculate completion statistics.
5. Compare departments and programs.
6. Use NumPy, Pandas and Python data structures.
7. Persistent CSV file storage.
8. Tkinter GUI.
9. Colorful Matplotlib BAR, PIE and LINE charts.
10. Input validation and exception handling.
11. Separate user-defined modules.
12. Basic automated testing.

Files
-----
main.py              -> Tkinter GUI and application control
record_manager.py    -> CSV file handling, validation, search
analytics.py         -> statistics, Pandas/NumPy analysis
charts.py            -> Bar, Pie and Line visualizations
test_training.py     -> basic tests
training_records.csv -> persistent sample data

Installation
------------
Open terminal in this folder and run:

pip install pandas numpy matplotlib

Run application:
python main.py

Run tests:
python test_training.py

Important
---------
Keep all .py files and training_records.csv in the same folder.
The application automatically saves new records to training_records.csv.

Charts
------
BAR CHART  -> employees/training records by department
PIE CHART  -> completed/in-progress/not-started distribution
LINE CHART -> monthly completed training records
             (or average program score if dates are unavailable)

Project requirements covered:
- Python functions and data structures
- File handling
- 4 user-defined modules
- NumPy
- Pandas
- Tkinter
- Matplotlib
- 3 visualizations
- Input validation
- Exception handling
- Testing and documentation


Dashboard UI Update:
The main window is designed like a simple college-project dashboard, similar to the
provided reference. It includes a blue header, summary cards, Add Training Record
section, Search/Filter section, records table, and separate Bar/Pie/Line chart buttons.
The code remains basic Tkinter and is suitable for 5th-semester viva explanation.


CHARTS:
The project includes three Matplotlib reports:
1. Bar Chart - Average performance by training program.
2. Pie Chart - Training completion status.
3. Line Chart - Training performance trend.

The charts are available from the GUI buttons and use simple, colorful formatting.


The dashboard keeps the Training Analysis Reports buttons visible below the records table: BAR CHART, PIE CHART, LINE CHART and ALL CHARTS.


IMPORTANT - CHART OUTPUT:
The Bar Chart, Pie Chart and Line Chart buttons now use the actual training_records.csv
data. The ALL CHARTS button displays all three charts together in one window.
