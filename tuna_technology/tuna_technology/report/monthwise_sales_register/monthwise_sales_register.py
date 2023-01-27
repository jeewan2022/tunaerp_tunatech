# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns = get_column()
    data = get_data(filters)
    return columns, data


def get_column():
    return [_("Month") + ":150:Date",
            _("Total Sales") + ":int:150",
            _("Non Vat Sales") + ":Data:150",
            _("Taxable Amount") + ":int:150",
            _("Vat Amount") + ":Int:150",
            _("No. of Bills") + ":int:150"]


def get_data(filters):
    conditions = ""
    if filters.get("companies"):
        conditions += "and sinv.company={}".format(
            frappe.db.escape(filters.get("companies")))
    if filters.get("fiscal_year"):
        conditions += "and Year(sinv.posting_date)={}".format(
            frappe.db.escape("Fiscal year"))      

    data = frappe.db.sql("""select monthname(sinv.posting_date),
		sum(sitem.amount),sum(sinv.grand_total), sum(tax.tax_amount),
        sum(sinv.total), count(sinv.name)

		FROM `tabSales Invoice` sinv, `tabSales Invoice Item` sitem,
                `tabSales Taxes and Charges` tax 

		WHERE sitem.parent = sinv.name and tax.parent=sinv.name {conditions}
                and sinv.docstatus = 1
            group by monthname(sinv.posting_date)""".format(conditions=conditions), as_list=1)

    if filters.get("include_all"):
        return data
        
    return data
