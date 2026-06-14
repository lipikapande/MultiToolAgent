import json


def library_fine_calculator(delayed_days) -> dict:
    """Calculate the library fine based on a fixed rate of ₹5 per delayed day.

    Use this tool whenever the user asks for a library fine calculation.
    Args:
        delayed_days (int/float/str): The number of days the book is overdue.
    Returns:
        dict: A dictionary containing the success status, fine amount, and a
        pre-formatted exact answer string to show the user.
    """
    try:
        if delayed_days is None:
            return {"status": "error", "message": "delayed_days is required"}

        # Normalize input: handles floats (e.g., 8.0) and numeric strings (e.g., "8")
        days = int(float(delayed_days))

        if days < 0:
            return {"status": "error", "message": "delayed_days must be >= 0"}

    except (ValueError, TypeError) as e:
        return {
            "status": "error",
            "message": f"Invalid input for delayed_days: {e}",
        }

    # Calculate fine based on ₹5/day rule
    rate_per_day = 5
    fine = rate_per_day * days
    fine_display = f"₹{fine}"

    return {
        "status": "success",
        "delayed_days": days,
        "fine_amount": fine,
        "fine_display": fine_display,
        # This explicit string forces the LLM to copy-paste the correct answer
        "explicit_response_text": f"The library fine for {days} delayed days is {fine_display} (calculated at ₹{rate_per_day} per day).",
    }


# --- Example Verification ---
if __name__ == "__main__":
    # Simulate Groq calling the function with your exact scenario
    result = library_fine_calculator(8)
    print(json.dumps(result, indent=4, ensure_ascii=False))