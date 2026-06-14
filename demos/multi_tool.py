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
