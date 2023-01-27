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
    return [_("Date") + ":Date:150",
            _("Customer Name") + ":Link/Customer:150",
            _("Customer PAN") + ":Data:150",
            _("Total Sale") + ":Data:150",
            _("Non Vat Sales") + ":Data:150",
            _("Taxable Sales") + ":Data:150",
            _("Vat Amount") + ":currency:150",
            _("No of Bill") + ":int:150"]


def get_data(filters):
    conditions = ""
    if filters.get("companies"):
        conditions += "and sinv.company={}".format(frappe.db.escape(filters.get("companies")))
    
    if filters.get('from_date'):
        if (len('from_date') >= 0 and len('to_date') >= 0):
            conditions += ' and sinv.posting_date between {0} and {1}'.format(frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))
    if filters.get("fiscal_year"):
        conditions += "and Year(sinv.posting_date)={}".format(frappe.db.escape("Fiscal Year"))

    data = frappe.db.sql("""select sinv.posting_date, sinv.customer_name,
		sinv.tax_id, sum(sitem.amount),sum(sinv.total), sum(sinv.total),
        sum(stax.tax_amount),count(sinv.name)
        

			from `tabSales Invoice` sinv, `tabSales Invoice Item` sitem,
		`tabSales Taxes and Charges` stax 

		where sitem.parent=sinv.name and stax.parent=sinv.name {conditions}
		group by sinv.customer_name""".format(conditions=conditions), as_list=1)
    if filters.get("include_all"):
        return data
        
    return data
