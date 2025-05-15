import frappe

def validate(doc, method):
    standard_working_hour = frappe.db.get_single_value("HR Settings", "standard_working_hours")
    working_hour = float(standard_working_hour)
    worked_hours = (doc.working_hours)
    
    if worked_hours is not None:
        if (worked_hours >= working_hour):
            overtime = float(worked_hours) - working_hour
            doc.custom_overtime = round(overtime,2)
        else:
            doc.custom_overtime = 0
    else:
        doc.custom_overtime = 0
        # pass

    if doc.custom_overtime > 0:
        new_overtime_request = frappe.new_doc("Overtime Request")
        new_overtime_request.employee = doc.employee
        new_overtime_request.employee_name = doc.employee_name
        new_overtime_request.overtime = doc.custom_overtime
        new_overtime_request.date = doc.attendance_date
        new_overtime_request.submit()
        new_overtime_request.save(ignore_permissions = True)

        frappe.msgprint(f"New Overtime request is formed for {doc.employee_name} of {doc.custom_overtime} hours.")