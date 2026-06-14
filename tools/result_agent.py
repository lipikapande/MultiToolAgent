from typing import List, Dict


def result_calculator(marks: List[float]) -> Dict:
    """Calculate average, grade and pass/fail from a list of marks.

    Returns dict like:
    {"status":"success","average":90,"grade":"A","result":"Pass"}
    or on error: {"status":"error","message":"..."}
    """
    try:
        # accept list-like input
        numbers = [float(m) for m in marks]
        if len(numbers) == 0:
            return {"status": "error", "message": "No marks provided"}
    except Exception as e:
        return {"status": "error", "message": f"Invalid marks: {e}"}

    avg = sum(numbers) / len(numbers)
    avg_rounded = round(avg, 2)

    if avg_rounded >= 90:
        grade = "A"
    elif 75 <= avg_rounded <= 89:
        grade = "B"
    elif 60 <= avg_rounded <= 74:
        grade = "C"
    else:
        grade = "D"

    result_status = "Pass" if avg_rounded >= 50 else "Fail"

    return {
        "status": "success",
        "marks": numbers,
        "average": avg_rounded,
        "grade": grade,
        "result": result_status,
    }
