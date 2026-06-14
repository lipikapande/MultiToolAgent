 
_STUDENTS = {
    "S001": {"name": "Alice", "age": 20, "course": "B.Tech", "year": 2},
    "S002": {"name": "Bob", "age": 21, "course": "B.Sc", "year": 3},
    "S003": {"name": "Charlie", "age": 19, "course": "B.Com", "year": 1},
}


def student_info_tool(student_id: str) -> dict:
    """Retrieve student information from an internal dictionary.

    Returns dict like: {"status":"success","student_id":"S001","name":"Alice",...}
    """
    sid = str(student_id).strip()
    info = _STUDENTS.get(sid)
    if info is None:
        return {"status": "error", "message": f"Student id {sid} not found"}

    return {"status": "success", "student_id": sid, **info}

