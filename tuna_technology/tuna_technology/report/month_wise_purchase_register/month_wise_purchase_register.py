# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        _("Month") + ":150:Date",
        _("Taxable Purchase") + ":150:Data",
        _("Local Tax") + ":150:Data",
        _("Taxable Import") + ":150:Data",
        _("Import Tax") + ":150:Data",
        _("No. Of Bills") + ":150:Data"
    ]


def get_data(filters):
    conditions = ""
    if filters.get("companies"):
        conditions += "and pinv.company={}".format(
            frappe.db.escape(filters.get("companies")))
	
    data = frappe.db.sql("""select monthname(pinv.posting_date),
			sum(pinv.total), sum(pinv.total_taxes_and_charges), sum(pinv.total_taxable_import_company_currency),
			sum(pinv.total_import_tax_company_currency), COUNT(pinv.name)
			 from
			`tabPurchase Invoice` pinv
			where pinv.docstatus=1 {conditions}
			group by monthname(pinv.posting_date)""" .format(conditions=conditions), as_list=1)
    if filters.get("include_all"):
        return data
    return data
