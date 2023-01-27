# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = [
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": ("date"),
            "options": "Sales Invoice",
        },
        {
            "fieldname": "Bill",
            "fieldtype": "Data",
            "label": ("Bill No."),
            "options": "Sales Invoice",
        },
        {
            "fieldname": "customer_name",
            "fieldtype": "Link",
            "label": ("Buyer's Name"),
            "options": "Customer",
        },
        {
            "fieldname": "tax_id",
            "fieldtype": "Link",
            "label": ("Buyer's Pan"),
            "options": "Sales Invoice",
        },
        {
            "fieldname": "Reason",
            "fieldtype": "Link",
            "label": ("Cancelled Reason"),
            "options": "Sales Invoice",
        }

    ]
    conditions = ""
    if filters.get('from_date'):
        if (len('from_date') >= 0 and len('to_date') >= 0):
            conditions += ' and sinv.posting_date between {0} and {1}'.format(
                frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))
    if filters.get("companies"):
        conditions += "and sinv.company={}".format(
            frappe.db.escape(filters.get("companies")))
    if filters.get("fiscal_year"):
        conditions += "and Year(sinv.posting_date)={}".format(
            frappe.db.escape("Fiscal Year"))
    data = frappe.db.sql("""SELECT sinv.posting_date, sinv.customer_name, sinv.tax_id, sinv.docstatus FROM `tabSales Invoice` sinv where docstatus=2
	 {conditions}""".format(conditions=conditions), as_dict=1)
    data_array = []
    for d in data:
        data_array.append(d)
    return columns, data_array
