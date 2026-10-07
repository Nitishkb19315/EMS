import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.permissions import add_permission, update_permission_property


def after_install():
	setup_fixtures()
	create_student_role()
	create_parent_assessment_group()
	create_invoice_permissions()
	create_custom_fields(get_custom_fields())
	create_permissions(get_permissions())


def setup_fixtures():
	# Party Type Records
	if not frappe.db.exists("Party Type", "Student"):
		try:
			frappe.get_doc(
				{
					"doctype": "Party Type",
					"party_type": "Student",
					"account_type": "Receivable",
				}
			).insert(ignore_permissions=True)
		except Exception:
			pass

	# Item Group Records
	if not frappe.db.exists("Item Group", "Fee Component"):
		try:
			parent_item_group = (
				frappe.db.get_value(
					"Item Group", {"is_group": 1, "parent_item_group": ("in", ["", None])}, "name"
				)
				or "All Item Groups"
			)
			if not frappe.db.exists("Item Group", parent_item_group):
				parent_item_group = frappe.db.get_value("Item Group", {"is_group": 1}, "name")

			frappe.get_doc(
				{
					"doctype": "Item Group",
					"item_group_name": "Fee Component",
					"parent_item_group": parent_item_group,
					"is_group": 0,
				}
			).insert(ignore_permissions=True)
		except Exception:
			pass

	# Customer Group Records
	if not frappe.db.exists("Customer Group", "Student"):
		try:
			parent_customer_group = (
				frappe.db.get_value(
					"Customer Group", {"is_group": 1, "parent_customer_group": ("in", ["", None])}, "name"
				)
				or "All Customer Groups"
			)
			if not frappe.db.exists("Customer Group", parent_customer_group):
				parent_customer_group = frappe.db.get_value("Customer Group", {"is_group": 1}, "name")

			frappe.get_doc(
				{
					"doctype": "Customer Group",
					"customer_group_name": "Student",
					"parent_customer_group": parent_customer_group,
					"is_group": 0,
				}
			).insert(ignore_permissions=True)
		except Exception:
			pass


def create_parent_assessment_group():
	if not frappe.db.exists("Assessment Group", "All Assessment Groups"):
		frappe.get_doc(
			{
				"doctype": "Assessment Group",
				"assessment_group_name": "All Assessment Groups",
				"is_group": 1,
			}
		).insert(ignore_mandatory=True)


def create_student_role():
	if not frappe.db.exists("Role", "Student"):
		frappe.get_doc({"doctype": "Role", "role_name": "Student", "desk_access": 0}).save()


def create_invoice_permissions():
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


def get_permissions():
	return [
		{
			"doctype": "Sales Invoice",
			"role": "Student",
			"permlevel": 0,
			"ptype": ["read", "write", "print"],
		},
		{
			"doctype": "User",
			"role": "Academics User",
			"permlevel": 0,
			"ptype": ["read", "write", "create"],
		},
		{
			"doctype": "Customer",
			"role": "Academics User",
			"permlevel": 0,
			"ptype": ["read", "write", "create"],
		},
	]


def create_permissions(doctype_permissions):
	for doctype_permission in doctype_permissions:
		doctype = doctype_permission.get("doctype")
		role = doctype_permission.get("role")
		permlevel = doctype_permission.get("permlevel")
		ptype = doctype_permission.get("ptype")
		try:
			add_permission(doctype, role, permlevel)
		except Exception:
			pass
		for p in ptype:
			try:
				update_permission_property(doctype, role, permlevel, p, 1)
			except Exception:
				pass


def get_custom_fields():
	"""SyncEdx specific custom fields that needs to be added to the Sales Invoice DocType."""
	return {
		"Sales Invoice": [
			{
				"fieldname": "student_info_section",
				"fieldtype": "Section Break",
				"label": "Student Info",
				"collapsible": 1,
				"insert_after": "ignore_pricing_rule",
			},
			{
				"fieldname": "student",
				"fieldtype": "Link",
				"label": "Student",
				"options": "Student",
				"insert_after": "student_info_section",
			},
			{
				"fieldname": "column_break_ejcc",
				"fieldtype": "Column Break",
				"insert_after": "student",
			},
			{
				"fieldname": "fee_schedule",
				"fieldtype": "Link",
				"label": "Fee Schedule",
				"options": "Fee Schedule",
				"insert_after": "column_break_ejcc",
			},
		],
		"Sales Order": [
			{
				"fieldname": "student_info_section",
				"fieldtype": "Section Break",
				"label": "Student Info",
				"collapsible": 1,
				"insert_after": "ignore_pricing_rule",
			},
			{
				"fieldname": "student",
				"fieldtype": "Link",
				"label": "Student",
				"options": "Student",
				"insert_after": "student_info_section",
			},
			{
				"fieldname": "column_break_ejcc",
				"fieldtype": "Column Break",
				"insert_after": "student",
			},
			{
				"fieldname": "fee_schedule",
				"fieldtype": "Link",
				"label": "Fee Schedule",
				"options": "Fee Schedule",
				"insert_after": "column_break_ejcc",
			},
		],
	}
