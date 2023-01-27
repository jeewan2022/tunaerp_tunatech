# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
    column = [
        {
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "label": ("Date"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "invoice_number",
            "fieldtype": "Link",
            "label": ("Bill No."),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "pragyapan_no",
            "fieldtype": "Data",
            "label": ("Prgyapan No."),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "supplier_name",
            "fieldtype": "Link",
            "label": ("Supplier's Name"),
            "options": "Supplier",
        },
        {
            "fieldname": "tax_id",
            "fieldtype": "Data",
            "label": ("Supplier's pan"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "items",
            "fieldtype": "Data",
            "label": ("Name of Items"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "total_qty",
            "fieldtype": "Data",
            "label": ("Quantity of Item"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "UOM",
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
            "fieldname": "total",
            "fieldtype": "Data",
            "label": ("Non Vat Amount"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "grand_total",
            "fieldtype": "Data",
            "label": ("Taxable Purchase"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "taxes",
            "fieldtype": "Data",
            "label": ("Purchase Tax"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "total_taxable_import_company_currency",
            "fieldtype": "Data",
            "label": ("Taxable Import"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "total_import_tax_company_currency",
            "fieldtype": "Data",
            "label": ("Import Tax"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "",
            "fieldtype": "Data",
            "label": ("Taxable Assets"),
            "options": "Purchase Invoice",
        },
        {
            "fieldname": "",
            "fieldtype": "Data",
            "label": ("Assets tax"),
            "options": "Purchase Invoice",
        },
    ]
    conditions = ""
    if filters.get("companies"):
        conditions += "and pinv.company={}".format(
            frappe.db.escape(filters.get("companies")))
    if filters.get("fiscal_year"):
        fiscal_date = "2022"
        conditions += "and Year(pinv.posting_date)={}".format(
            frappe.db.escape(fiscal_date))
    if filters.get('from_date') and filters.get('to_date'):
        if (len('from_date') >=0 and len('to_date') >=0):
            conditions += ' and pinv.posting_date between {0} and {1}'.format(
                frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))

    data = frappe.db.sql(
        """select pinv.name from `tabPurchase Invoice` pinv where pinv.status='overdue' {conditions}""".format(conditions=conditions), as_dict=1)
 
    data_array = []
    for d in data:
        invoice = frappe.get_doc("Purchase Invoice", d)
        items = ""
        for item in invoice.items:
            items = items + item.item_name
        units = ""
        for un in invoice.items:
            units = units + un.uom
        vat = ""
        for tax in invoice.taxes:
            vat = vat + str(tax.tax_amount)
      
        dictionary = {
            "posting_date": invoice.posting_date,
            "invoice_number": invoice.name,
            "supplier_name": invoice.supplier_name,
            "tax_id": invoice.tax_id,
            "items": items,
            "total_qty": invoice.total_qty,
            "UOM": units,
            "total": invoice.total,
            "taxes": vat,
            "grand_total": invoice.net_total,
            "pragyapan_no": invoice.pragyapan_no,
            "total_taxable_import_company_currency": invoice.total_taxable_import_company_currency,
            "total_import_tax_company_currency": invoice.total_import_tax_company_currency,
            "total":invoice.total
        }

        data_array.append(dictionary)
    return column, data_array
