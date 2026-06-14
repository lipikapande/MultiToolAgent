def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> dict:
    """Return pending fee amount.

    Returns dict like:
    {"status":"success","total_fee":50000,"paid":35000,"pending_fee":15000}
    or on error: {"status":"error","message":"..."}
    """
    try:
        total = float(total_course_fee)
        paid = float(amount_paid)
        if total < 0 or paid < 0:
            return {"status": "error", "message": "Amounts must be non-negative"}
    except Exception as e:
        return {"status": "error", "message": f"Invalid numeric inputs: {e}"}

    pending = round(max(0.0, total - paid), 2)
    return {
        "status": "success",
        "total_fee": total,
        "paid": paid,
        "pending_fee": pending,
    }
