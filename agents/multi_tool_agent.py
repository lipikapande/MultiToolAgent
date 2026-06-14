import json

from schemas.tool_schemas import multi_tool_schema
from utils.groq_client import MODEL, client
from utils.tool_map import TOOL_MAP


SYSTEM_PROMPT = """
You are a college assistant. Analyse the user's request and call exactly
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
    """Route a user question to the correct tool via the Groq client and return a final answer."""
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

    if finish_reason == "tool_calls" and msg.tool_calls:
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

        final = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=300,
        )
        final_answer = final.choices[0].message.content
    else:
        final_answer = msg.content

    if verbose:
        print(f"\nSTEP 5 - Final Answer: {final_answer}\n")

    return final_answer
