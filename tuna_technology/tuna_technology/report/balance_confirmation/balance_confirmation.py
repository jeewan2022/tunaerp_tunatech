# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
from frappe import msgprint, _
import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        _("party") + ":Link/Customer:150",
        _("Taxable Sales") + ":Data:150",
        _("Sales Tax") + ":Data:150",
    ]


def get_data(filters):
    conditions = ""
    if filters.get("companies"):
        conditions += "and sinv.company={}".format(
            frappe.db.escape(filters.get("companies"))
        )
    if filters.get("party"):
        conditions += "and sinv.customer={}".format(frappe.db.escape(filters.get("party")))

    data = frappe.db.sql("""select sinv.customer_name, sum(sinv.total), sum(sinv.total_taxes_and_charges) 

	from 
		
		`tabSales Invoice` sinv

		where sinv.docstatus=1 {conditions}
		group by sinv.customer""".format(conditions=conditions), as_list=1)
    return data
