("""Function-style tool schemas for the multi-tool college assistant.

Each entry follows the OpenAI function-calling style so the agent can
use these schemas when requesting structured tool calls.
""")

multi_tool_schema = [
	{
		"type": "function",
		"function": {
			"name": "attendance_calculator",
			"description": "Calculate attendance percentage and exam eligibility (≥75% → eligible).",
			"parameters": {
				"type": "object",
				"properties": {
					"total_classes": {
						"type": "integer",
						"description": "Total number of classes scheduled (integer > 0).",
					},
					"attended_classes": {
						"type": "integer",
						"description": "Number of classes the student attended (integer ≥ 0).",
					},
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
					"marks": {
						"type": "array",
						"items": {"type": "number"},
						"description": "List/array of numeric marks for subjects (e.g. [95,90,88,91,87]).",
						"minItems": 1,
					}
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
					"total_course_fee": {
						"type": "number",
						"description": "Total course fee (numeric).",
					},
					"amount_paid": {
						"type": "number",
						"description": "Amount already paid (numeric).",
					},
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
				"properties": {
					"delayed_days": {
						"type": "integer",
						"description": "Number of days the book was returned late (integer ≥ 0).",
					}
				},
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
					"monthly_hostel_fee": {
						"type": "number",
						"description": "Monthly hostel fee (numeric).",
					},
					"months_stayed": {
						"type": "integer",
						"description": "Number of months stayed (integer ≥ 0).",
					},
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
			"parameters": {
				"type": "object",
				"properties": {
					"student_id": {
						"type": "string",
						"description": "Student identifier (e.g. 'S001').",
					}
				},
				"required": ["student_id"],
			},
		},
	},
]

