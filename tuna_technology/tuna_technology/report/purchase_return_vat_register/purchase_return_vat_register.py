# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

import frappe


import fractions


def execute(filters=None):
    columns = [
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": ("date"),
            "options": "Purchase invoice",
        },

        {
            "fieldname": "invoice_number",
            "fieldtype": "Link",
            "label": ("Bill No."),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "supplier_name",
            "fieldtype": "Link",
            "label": ("Bil No."),
            "options": "Supplier",
        },
        {
            "fieldname": "tax_id",
            "fieldtype": "Data",
            "label": ("Bil No."),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "items",
            "fieldtype": "Data",
            "label": ("Bil No."),
            "options": "Purchase invoice",
        },
        {
            "fieldname": "total_qty",
            "fieldtype": "Data",
            "label": ("Bil No."),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "uom",
            "fieldtype": "Data",
            "label": ("UOM"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "total",
            "fieldtype": "Data",
            "label": ("Total Purchase Amount"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "base_grand_total",
            "fieldtype": "Data",
            "label": ("Taxable Sales"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "taxes",
            "fieldtype": "Data",
            "label": ("Vat Amount"),
            "options": "Purchase Invoice",
        },

        {
            "fieldname": "tax",
            "fieldtype": "Data",
            "label": ("Export Zero Rated"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "",
            "fieldtype": "Data",
            "label": ("Export document No"),
            "options": "Purchase Invoice",
        },
    ]
    conditions = ""
    if filters.get("companies"):
        conditions += "and pinv.company={}".format(
            frappe.db.escape(filters.get("companies")))

    if filters.get("fiscal_year"):
        conditions += "and Year(pinv.posting_date)={}".format(
            frappe.db.escape("Fiscal Year"))

    if filters.get('from_date'):
        if (len('from_date') >= 0 and len('to_date') >= 0):
            conditions += ' and pinv.posting_date between {0} and {1}'.format(
                frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))

    data = frappe.db.sql(
        """select pinv.name from `tabPurchase Invoice` pinv where pinv.status='Return' {conditions}""".format(conditions=conditions), as_dict=1)
    data_array = []
    for d in data:
        invoice = frappe.get_doc("Purchase Invoice", d)
        items = ""
        for item in invoice.items:
            items = items + item.item_name
        units = ""
        for un in invoice.items:
            units = units + un.uom
        taxes = ""
        for vat in invoice.taxes:
            taxes = taxes + str(vat.tax_amount)
        dictionary = {
            "posting_date": invoice.posting_date,
            "invoice_number": invoice.name,
            "supplier_name": invoice.supplier_name,
            "tax_id": invoice.tax_id,
            "items": items,
            "total_qty": invoice.total_qty,
            "uom": units,
            "total": invoice.total,
            "taxes": taxes,
            "base_grand_total": invoice.base_grand_total,
            "tax":taxes
        }
        data_array.append(dictionary)
    return columns, data_array
