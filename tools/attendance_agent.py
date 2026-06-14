from typing import Dict


def attendance_calculator(total_classes: int, attended_classes: int) -> Dict:
    """Calculate attendance percentage and exam eligibility.

    Returns dict like:
    {"status":"success","percentage":72.0,"eligibility":"Eligible for Exam"}
    or on error: {"status":"error","message": "..."}
    """
    try:
        total = int(total_classes)
        attended = int(attended_classes)
        if total <= 0:
            return {"status": "error", "message": "total_classes must be > 0"}
    except Exception as e:
        return {"status": "error", "message": f"Invalid inputs: {e}"}

    percentage = round(attended / total * 100, 2)
    eligibility = "Eligible for Exam" if percentage >= 75 else "Not Eligible for Exam"

    return {
        "status": "success",
        "total_classes": total,
        "attended_classes": attended,
        "percentage": percentage,
        "eligibility": eligibility,
    }
