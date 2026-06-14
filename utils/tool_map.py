from tools.attendance_agent import attendance_calculator
from tools.result_agent import result_calculator
from tools.fee_balance_agent import fee_balance_calculator
from tools.library_fine_agent import library_fine_calculator
from tools.hostel_fee_agent import hostel_fee_calculator
from tools.student_info_agent import student_info_tool

TOOL_MAP = {
	"attendance_calculator": attendance_calculator,
	"result_calculator": result_calculator,
	"fee_balance_calculator": fee_balance_calculator,
	"library_fine_calculator": library_fine_calculator,
	"hostel_fee_calculator": hostel_fee_calculator,
	"student_info_tool": student_info_tool,
}
