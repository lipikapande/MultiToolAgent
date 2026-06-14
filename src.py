import os
import re
import json
from typing import Any, Dict, List

from dotenv import load_dotenv
from groq import Groq

# Load environment and initialize Groq client
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"


# ---------------------- Tools (single-file versions) ----------------------

def attendance_calculator(total_classes: int, attended_classes: int) -> Dict:
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


def result_calculator(marks: List[float]) -> Dict:
    try:
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


def fee_balance_calculator(total_course_fee: float, amount_paid: float) -> Dict:
    try:
        total = float(total_course_fee)
        paid = float(amount_paid)
        if total < 0 or paid < 0:
            return {"status": "error", "message": "Amounts must be non-negative"}
    except Exception as e:
        return {"status": "error", "message": f"Invalid numeric inputs: {e}"}

    pending = round(max(0.0, total - paid), 2)
    return {"status": "success", "total_fee": total, "paid": paid, "pending_fee": pending}


def library_fine_calculator(delayed_days) -> Dict:
    try:
        if delayed_days is None:
            return {"status": "error", "message": "delayed_days is required"}
        days = int(float(delayed_days))
        if days < 0:
            return {"status": "error", "message": "delayed_days must be >= 0"}
    except (ValueError, TypeError) as e:
        return {"status": "error", "message": f"Invalid input for delayed_days: {e}"}

    rate_per_day = 5
    fine = rate_per_day * days
    fine_display = f"₹{fine}"

    return {
        "status": "success",
        "delayed_days": days,
        "fine_amount": fine,
        "fine_display": fine_display,
        "explicit_response_text": f"The library fine for {days} delayed days is {fine_display} (calculated at ₹{rate_per_day} per day).",
    }


def hostel_fee_calculator(monthly_hostel_fee: float, months_stayed: int) -> Dict:
    try:
        monthly = float(monthly_hostel_fee)
        months = int(months_stayed)
        if months < 0:
            return {"status": "error", "message": "months_stayed must be >= 0"}
    except Exception as e:
        return {"status": "error", "message": f"Invalid inputs: {e}"}

    total = round(monthly * months, 2)
    return {"status": "success", "monthly_fee": monthly, "months": months, "total_hostel_fee": total}


# small in-file student DB
_STUDENTS = {
    "S001": {"name": "Alice", "age": 20, "course": "B.Tech", "year": 2},
    "S002": {"name": "Bob", "age": 21, "course": "B.Sc", "year": 3},
    "S003": {"name": "Charlie", "age": 19, "course": "B.Com", "year": 1},
}


def student_info_tool(student_id: str) -> Dict:
    sid = str(student_id).strip()
    info = _STUDENTS.get(sid)
    if info is None:
        return {"status": "error", "message": f"Student id {sid} not found"}
    return {"status": "success", "student_id": sid, **info}


# ---------------------- Function-style tool schema ----------------------

multi_tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "attendance_calculator",
            "description": "Calculate attendance percentage and exam eligibility (≥75% → eligible).",
            "parameters": {
                "type": "object",
                "properties": {
                    "total_classes": {"type": "integer", "description": "Total number of classes scheduled (integer > 0)."},
                    "attended_classes": {"type": "integer", "description": "Number of classes attended (integer ≥ 0)."},
                },
                "required": ["total_classes", "attended_classes"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "result_calculator",
            "description": "Compute average, grade and pass/fail from a list of subject marks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "marks": {"type": "array", "items": {"type": "number"}, "minItems": 1},
                },
                "required": ["marks"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fee_balance_calculator",
            "description": "Compute pending course fee given total fee and amount paid.",
            "parameters": {
                "type": "object",
                "properties": {
                    "total_course_fee": {"type": "number"},
                    "amount_paid": {"type": "number"},
                },
                "required": ["total_course_fee", "amount_paid"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "library_fine_calculator",
            "description": "Calculate library fine at a rate of ₹5 per delayed day.",
            "parameters": {
                "type": "object",
                "properties": {"delayed_days": {"type": "integer"}},
                "required": ["delayed_days"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "hostel_fee_calculator",
            "description": "Calculate total hostel fee from monthly fee and months stayed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_hostel_fee": {"type": "number"},
                    "months_stayed": {"type": "integer"},
                },
                "required": ["monthly_hostel_fee", "months_stayed"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "student_info_tool",
            "description": "Retrieve student details by Student ID from the internal store.",
            "parameters": {"type": "object", "properties": {"student_id": {"type": "string"}}, "required": ["student_id"]},
        },
    },
]


# ---------------------- Tool map ----------------------
TOOL_MAP = {
    "attendance_calculator": attendance_calculator,
    "result_calculator": result_calculator,
    "fee_balance_calculator": fee_balance_calculator,
    "library_fine_calculator": library_fine_calculator,
    "hostel_fee_calculator": hostel_fee_calculator,
    "student_info_tool": student_info_tool,
}


# ---------------------- Groq-driven agent ----------------------

SYSTEM_PROMPT = """
You are LPGIC's college assistant. Analyse the user's request and call exactly
the relevant tool when the request is about attendance, results, fees,
library fines, hostel fees, or student information.

Use `attendance_calculator` for attendance questions.
Use `result_calculator` for marks and grade questions.
Use `fee_balance_calculator` for pending fee calculations.
Use `library_fine_calculator` for library fine calculations (₹5 per delayed day).
Use `hostel_fee_calculator` for hostel fee computations.
Use `student_info_tool` for student lookup by ID.

If the user asks for something outside these tools, answer briefly and explain
which requests you can handle.
"""


def multi_tool_agent(user_question: str, verbose: bool = True) -> str:
    if verbose:
        print(f"\n{'=' * 55}")
        print(f"STEP 1 - User Input: {user_question}")
        print(f"{'=' * 55}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=multi_tool_schema,
        max_tokens=300,
    )

    msg = response.choices[0].message
    finish_reason = response.choices[0].finish_reason

    if verbose:
        print(f"\nSTEP 2 - Model Decision: finish_reason = '{finish_reason}'")

    if finish_reason == "tool_calls" and getattr(msg, "tool_calls", None):
        messages.append(msg)

        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            if verbose:
                print(f"STEP 3 - Tool Invoked: {tool_name}")
                print(f"Arguments: {tool_args}")

            tool = TOOL_MAP.get(tool_name)
            if tool is None:
                tool_result = {"status": "error", "message": f"Unknown tool: {tool_name}"}
            else:
                tool_result = tool(**tool_args)

            if verbose:
                print(f"\nSTEP 4 - Tool Result: {tool_result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result),
            })

        final = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=300)
        final_answer = final.choices[0].message.content
    else:
        final_answer = getattr(msg, "content", str(msg))

    if verbose:
        print(f"\nSTEP 5 - Final Answer: {final_answer}")

    return final_answer


# ---------------------- Demo runner ----------------------

TEST_QUERIES = [
    "I attended 72 classes out of 90. Am I eligible for exams?",
    "My marks are 95, 90, 88, 91 and 87. What is my grade?",
    "My course fee is 50000 and I have paid 35000. How much fee is pending?",
    "I returned a library book 8 days late. What is the fine amount?",
    "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
    "I attended 80 classes out of 100.My marks are 90, 85, 88, 92 and 95.My course fee is 60000 and I paid 45000.Provide:1. Attendance Status2. Grade3. Pending Fee",
]


def run_tests():
    for q in TEST_QUERIES:
        print("\nQuery:", q)
        resp = multi_tool_agent(q)
        print("Response:", resp)


if __name__ == "__main__":
    run_tests()

## to run this- demo

from agents.multi_tool_agent import multi_tool_agent

TEST_QUERIES = [
	"I attended 72 classes out of 90. Am I eligible for exams?",
	"My marks are 95, 90, 88, 91 and 87. What is my grade?",
	"My course fee is 50000 and I have paid 35000. How much fee is pending?",
	"I returned a library book 8 days late. What is the fine amount?",
	"Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
	"I attended 80 classes out of 100.My marks are 90, 85, 88, 92 and 95.My course fee is 60000 and I paid 45000.Provide:1. Attendance Status2. Grade3. Pending Fee",
]

def run_tests():
	for q in TEST_QUERIES:
		print("\nQuery:", q)
		resp = multi_tool_agent(q)
		print("Response:", resp)

if __name__ == "__main__":
	run_tests()
