# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _


def execute(filters=None):
    columns = [
        {

            "fieldname": "fiscal_year",
            "fieldtype": "Data",
            "label": ("Fiscal Year"),
            "options": "Fiscal Year",

        },
        {

            "fieldname": "invoice_number",
            "fieldtype": "Link",
            "label": ("Bill no."),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "customer_name",
            "fieldtype": "Link",
            "label": ("Customer Name"),
            "options": "Customer",

        },
        {

            "fieldname": "tax_id",
            "fieldtype": "Data",
            "label": ("Customer pan"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": ("Bill Date"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "total",
            "fieldtype": "Data",
            "label": ("Amount"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "discount",
            "fieldtype": "Data",
            "label": ("Discount"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "taxable",
            "fieldtype": "Date",
            "label": ("Taxable Amount"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "tax",
            "fieldtype": "Data",
            "label": ("Tax Amount"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "grand_total",
            "fieldtype": "Data",
            "label": ("Total Sales Amount"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "synced_with_ird",
            "fieldtype": "int",
            "label": ("Sync With IRD"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "print_date",
            "fieldtype": "Datatime",
            "label": ("Is-Printed Time"),
            "options": "Sales Invoice",
            "width": "150",

        },
        {

            "fieldname": "",
            "fieldtype": "Data",
            "label": ("Is Bill Printed"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "print_date",
            "fieldtype": "Date",
            "label": ("Print Date"),
            "options": "Sales Invoice",
            "width": "150",

        },
        {

            "fieldname": "user",
            "fieldtype": "Link",
            "label": ("Entered By"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "synced_in_realtime",
            "fieldtype": "Data",
            "label": ("Is Real-Time"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "fiscal_year",
            "fieldtype": "Date",
            "label": ("Payment Method"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "is_return",
            "fieldtype": "Data",
            "label": ("Is Return"),
            "options": "Sales Invoice",

        },
        {

            "fieldname": "fiscal_year",
            "fieldtype": "Data",
            "label": ("Transaction ID"),
            "options": "Fiscal Year",

        }
    ]
    conditions = ""
    if filters.get('from_date'):
        if (len('from_date') >= 0 and len('to_date') >= 0):
            conditions += "and sinv.posting_date between {0} and {1}".format(
                frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))

    if filters.get("companies"):
        conditions += "and sinv.company={}".format(
            frappe.db.escape(filters.get("companies")))

    if filters.get("fiscal_year"):
        conditions += "and Year(sinv.posting_date)={}".format(
            frappe.db.escape("fiscal_year"))                    
    
    data = frappe.db.sql(
        """select sinv.name
         from `tabSales Invoice` sinv
         where sinv.status='Overdue' {conditions}""".format(conditions=conditions), as_dict=1)
    data_array = []
    for d in data:
        invoice = frappe.get_doc("Sales Invoice", d)

        fiscal = frappe.get_all("Fiscal Year")
        for fi in fiscal:
            year = frappe.get_doc("Fiscal Year", fi)

        dictionary = {
            "fiscal_year": year,
            "invoice_number": invoice.name,
            "customer_name": invoice.customer_name,
            "tax_id": invoice.tax_id,
            "posting_date": invoice.posting_date,
            "total": invoice.total,
            "discount": invoice.discount_amount,
            "tax": invoice.total_taxes_and_charges,
            "grand_total": invoice.grand_total,
            "synced_with_ird": invoice.synced_with_ird,
            "print_date": invoice.print_date,
            "user": invoice.owner,
            "synced_in_realtime": invoice.synced_in_realtime,
            "is_return": invoice.is_return,

        }

        if invoice.synced_with_ird == 1:
            dictionary["synced_with_ird"] = "Yes"
        else:
            dictionary["synced_with_ird"] = "No"

        if invoice.synced_in_realtime == 1:
            dictionary["synced_in_realtime"] = "Yes"
        else:
            dictionary["synced_in_realtime"] = "No"

        if invoice.is_return == 1:
            dictionary["is_return"] = "Yes"
        else:
            dictionary["is_return"] = "No"
      
        data_array.append(dictionary)
    return columns, data_array

