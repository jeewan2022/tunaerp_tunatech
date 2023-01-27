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
				"fieldname": "invoice_number",
				"fieldtype": "Link",
				"label": ("Bill No."),
				"options": "Sales Invoice"
			},
			{
				"fieldname": "customer_name",
				"fieldtype": "Link",
				"label": ("Buyer's Name"),
				"options": "Customer",
			},
			{
				"fieldname": "tax_id",
				"fieldtype": "Data",
				"label": ("Buyer's Pan"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "items",
				"fieldtype": "Data",
				"label": ("Name of Items"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "total_qty",
				"fieldtype": "Link",
				"label": ("Quantity of Item"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "uom",
				"fieldtype": "Data",
				"label": ("UOM"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "total",
				"fieldtype": "Data",
				"label": ("Sales Amount"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "total",
				"fieldtype": "Data",
				"label": ("Non Vat Sales"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "taxes",
				"fieldtype": "Data",
				"label": ("Vat Amount"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "value",
				"fieldtype": "Link",
				"label": ("Export Zero Rated"),
				"options": "Sales Invoice",
			},
			{
				"fieldname": "Export",
				"fieldtype": "Link",
				"label": ("Export Document No."),
				"options": "Sales Invoice",
			},
		]
		conditions = ""
		if filters.get("companies"):
			conditions += 'and sinv.company={}'.format(
			    frappe.db.escape(filters.get('companies')))
		if filters.get("fiscal_year"):
			conditions += "and Year(sinv.posting_date)={}".format(frappe.db.escape("fiscal_year"))

		if filters.get('from_date'):
			if (len('from_date') >= 0 and len('to_date') >= 0):
				conditions += ' and sinv.posting_date between {0} and {1}'.format(frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))
		

		data = frappe.db.sql("""select sinv.name from `tabSales Invoice` sinv where sinv.status='overdue' 
		{conditions}""".format(conditions=conditions), as_dict=1)
		

		data_array = []
		for d in data:
			invoice = frappe.get_doc("Sales Invoice", d)
			items = ""
			for item in invoice.items:
				items = items + item.item_name
			Ss = ""
			for vat in invoice.taxes:
				Ss = Ss + str(vat.tax_amount)
			units = ""
			for un in invoice.items:
				units = units + un.uom
			
			zero_rated = ""
			for tax in invoice.taxes:
				zero_rated = zero_rated + str(tax.tax_amount)

			add = frappe.db.sql("""select country from `tabAddress` """, as_dict=1)	
			
			dictionary = {
				"posting_date": invoice.posting_date,
				"customer_name": invoice.customer_name,
				"tax_id": invoice.tax_id,
				"items": items,
				"total_qty": invoice.total_qty,
				"total": invoice.total,
				"invoice_number": invoice.name,
				"taxes": Ss,
				"total": invoice.total,
				"uom": units,
				"total":invoice.total,
				"value":zero_rated,
			}
			data_array.append(dictionary)
		return columns, data_array
