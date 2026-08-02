import azure.functions as func
import datetime
import json
import logging

from services.payment_service import get_payment_details_service,update_fee_service

app = func.FunctionApp()

@app.route(route="paymentstatus/{studentid}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def payment_status(req: func.HttpRequest) -> func.HttpResponse:
    try:
        student_id = int(req.route_params.get("studentid"))
    except (TypeError, ValueError):
        return func.HttpResponse(json.dumps({"error": "Invalid Student ID"}), mimetype="application/json", 
                                 status_code=400)

    student = get_payment_details_service(student_id)

    if student is None:
        return func.HttpResponse(json.dumps({"error": "Student not found"}), mimetype="application/json",
                                 status_code=404)

    return func.HttpResponse(json.dumps(student), mimetype="application/json",status_code=200)

@app.route(route="updatefee/{studentid}", methods=["PUT"], auth_level=func.AuthLevel.ANONYMOUS)
def update_student_fee(req: func.HttpRequest) -> func.HttpResponse:
    try:
        student_id = int(req.route_params.get("studentid"))
    except (TypeError, ValueError):
        return func.HttpResponse(json.dumps({"error": "Invalid Student ID"}), mimetype="application/json", 
                                 status_code=400)    
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON Body"}), mimetype="application/json",
                                 status_code=400)    
         
    paid_amount = body.get("PaidAmount")

    if paid_amount is None:
        return func.HttpResponse(json.dumps({"error": "Paid Amount is required"}), mimetype="application/json",
                                 status_code=404)   
    
    if not isinstance(paid_amount, (int, float)):
        return func.HttpResponse(
            json.dumps({"error": "PaidAmount must be a number"}),
            mimetype="application/json",
            status_code=400
        )
    
    if paid_amount < 0:
        return func.HttpResponse(
            json.dumps({"error": "PaidAmount cannot be negative"}),
            mimetype="application/json",
            status_code=400
        )
    
    success = update_fee_service(student_id,paid_amount)
    if success:
        return func.HttpResponse(json.dumps({"message": "Fee Status Updated Successfully"}), 
                                 mimetype="application/json",status_code=200)
    else:
        return func.HttpResponse(json.dumps({"error": "Student Not Found"}), 
                                 mimetype="application/json",status_code=404)  
    