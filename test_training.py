from record_manager import validate_record
from analytics import completion_statistics

def test_validation():
    good = {"Employee ID":"E999","Employee Name":"Test","Department":"HR",
            "Program":"Python","Status":"Completed","Score":"90","Date":"2026-10-01"}
    validate_record(good)

def test_invalid_date():
    bad = {"Employee ID":"E998","Employee Name":"Test","Department":"HR",
           "Program":"Python","Status":"Completed","Score":"90","Date":"2026-02-31"}
    try:
        validate_record(bad)
        assert False, "Invalid date should be rejected"
    except ValueError as e:
        assert "Date must be valid" in str(e)

def test_statistics():
    records = [
        {"Status":"Completed"}, {"Status":"In Progress"}, {"Status":"Completed"}
    ]
    s = completion_statistics(records)
    assert s["total"] == 3
    assert s["completed"] == 2
    assert s["rate"] == 2/3*100

if __name__ == "__main__":
    test_validation()
    print("TC01 Valid date: PASS")
    test_invalid_date()
    print("TC02 Invalid date: PASS")
    test_statistics()
    print("TC03 Statistics: PASS")
    print("All tests passed successfully.")
