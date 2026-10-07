import frappe
from frappe.permissions import add_permission, update_permission_property


def execute():

	doctype = "Sales Invoice"
	role = "Student"
	permlevel = 0
	ptype = ["read", "write", "print"]

	try:
		add_permission(doctype, role, permlevel)
	except Exception:
		pass

	for p in ptype:
		try:
			update_permission_property(doctype, role, permlevel, p, 1)
		except Exception:
			pass

	frappe.db.commit()
