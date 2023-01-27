# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from dataclasses import dataclass
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns = get_column()
    data = get_data(filters)
    return columns, data


def get_column():
    return[
        _("Bill Date") + ":Date:150",
        _("Supplier Name") + ":Link/Supplier:100",
        _("Supplier Pan") + ":Data:150",
        _("Taxable Purchase") + ":Data:150",
        _("Local Tax") + ":Data:150",
        _("Taxable Import") + ":Data:150",
        _("Import Tax") + ":Data:150",
        _("No.Of Bills ")+"Data:150"
    ]


def get_data(filters):
    conditions = ""
 
    if filters.get("companies"):
        conditions += "and pinv.company={}".format(
            frappe.db.escape(filters.get("companies")))
            
    if filters.get('from_date'):
        if (len('from_date') >= 0 and len('to_date') >= 0):
            conditions += ' and pinv.posting_date between {0} and {1}'.format(
                frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))

    if filters.get("fiscal_year"):
        conditions += "and Year(pinv.posting_date)={}".format(
            frappe.db.escape("Fiscal Year"))

    data = frappe.db.sql("""select pinv.posting_date, pinv.supplier_name,
		pinv.tax_id,sum(pinv.total), sum(pinv.total_taxes_and_charges), sum(pinv.total_taxable_import_company_currency),
		sum(pinv.total_import_tax_company_currency), count(pinv.name)

			from `tabPurchase Invoice` pinv

		where pinv.docstatus=1 {conditions}
		group by pinv.supplier""".format(conditions=conditions), as_list=1)
    if filters.get("include_all"):
        return data

    return data

