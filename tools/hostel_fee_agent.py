def hostel_fee_calculator(monthly_hostel_fee: float, months_stayed: int) -> dict:
    """Calculate total hostel fee.

    Returns dict like:
    {"status":"success","monthly_fee":6000,"months":5,"total_hostel_fee":30000}
    """
    try:
        monthly = float(monthly_hostel_fee)
        months = int(months_stayed)
        if months < 0:
            return {"status": "error", "message": "months_stayed must be >= 0"}
    except Exception as e:
        return {"status": "error", "message": f"Invalid inputs: {e}"}

    total = round(monthly * months, 2)
    return {
        "status": "success",
        "monthly_fee": monthly,
        "months": months,
        "total_hostel_fee": total,
    }
