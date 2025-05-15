import frappe

def validate(doc, method):
    if doc.personal_email:
        existing_user = frappe.db.exists("User", {"email": doc.personal_email})

        if not existing_user:
            new_user = frappe.new_doc("User")
            new_user.email = doc.personal_email
            new_user.first_name = doc.first_name
            new_user.last_name = doc.last_name
            new_user.enabled = 1
            new_user.save(ignore_permissions = True)

            frappe.msgprint(f"A new user hass been created with email {doc.personal_email}")
