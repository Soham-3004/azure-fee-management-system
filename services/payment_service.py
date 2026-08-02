from datetime import date
from services.database import execute_query, execute_non_query

GET_STUDENT_QUERY = """
SELECT
    StudentID,
    Name,
    TotalFee,
    PaidAmount,
    DueDate
FROM dbo.Students
WHERE StudentID = ?;
"""

UPDATE_FEE_QUERY = """
UPDATE dbo.Students
SET PaidAmount = ?
WHERE StudentID = ?;
"""

def get_student(student_id):
    return execute_query(GET_STUDENT_QUERY,[student_id])

def determine_payment_status(student):
    total_fee = student.TotalFee
    paid_amount = student.PaidAmount
    due_date = student.DueDate

    if paid_amount >= total_fee:
        return "Paid"

    elif due_date < date.today():
        return "Overdue"

    return "Partially Paid"

def get_payment_details_service(student_id):
    student = get_student(student_id)

    if student is None:
        return None
    
    return {
        "StudentID": student.StudentID,
        "Name": student.Name,
        "TotalFee": float(student.TotalFee),
        "PaidAmount": float(student.PaidAmount),
        "DueDate": str(student.DueDate),
        "OutstandingAmount": float(student.TotalFee - student.PaidAmount),
        "PaymentStatus": determine_payment_status(student)
    }

def update_fee_service(student_id, paid_amount):
    rows_affected = execute_non_query(UPDATE_FEE_QUERY,[paid_amount, student_id])
    return rows_affected > 0
