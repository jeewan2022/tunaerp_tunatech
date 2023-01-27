# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"fieldname":"posting_date",
			"fieldtype":"Date",
			"label":("date"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"invoice_number",
			"fieldtype":"Link",
			"label":("Bil No."),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"customer_name",
			"fieldtype":"Link",
			"label":("Buyer's Name"),
			"options":"Customer",
		},
		{
			"fieldname":"tax_id",
			"fieldtype":"Data",
			"label":("Buyer's Pan"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"items",
			"fieldtype":"Data",
			"label":("Name of Items"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"total_qty",
			"fieldtype":"Data",
			"label":("Quantity of Item"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"uom",
			"fieldtype":"Data",
			"label":("UOM"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"total",
			"fieldtype":"Data",
			"label":("Sales Amount"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"tax",
			"fieldtype":"Data",
			"label":("Non Vat Sales"),
			"options":"Sales Invoice",
		},
		
		{
			"fieldname":"taxes",
			"fieldtype":"Data",
			"label":("Vat Amount"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"zero",
			"fieldtype":"Link",
			"label":("Export Zero Rated"),
			"options":"Sales Invoice",
		},
		{
			"fieldname":"",
			"fieldtype":"Data",
			"label":("Export Documnet Number"),
			"options":"Sales Invoice",
		},
	]
	conditions = ""
	if filters.get('from_date'):
		if (len('from_date') >= 0 and len('to_date') >= 0):
			conditions += ' and sinv.posting_date between {0} and {1}'.format(frappe.db.escape(filters.get('from_date')), frappe.db.escape(filters.get('to_date')))
	if filters.get("companies"):
		conditions += 'and sinv.company={}'.format(frappe.db.escape(filters.get('companies')))
	if filters.get("fiscal_year"):
			conditions += "and sinv.posting_date={}".format(frappe.db.escape(filters.get("fiscal_year")))
	
	
	data =  frappe.db.sql("""select sinv.name from `tabSales Invoice` sinv where sinv.status='return' {conditions}"""
	.format(conditions=conditions), as_dict=1)
	
	add = frappe.db.sql("""select country from `tabAddress` """, as_dict=1)
	data_array = []
	for d in data:
		invoice = frappe.get_doc("Sales Invoice", d)
		items = ""
		for item in invoice.items:
			items = items + item.item_name	
		vat = ""
		for tax in invoice.taxes:
			vat = vat + str(tax.tax_amount)
		units = ""
		for un in invoice.items:
			units = units + un.uom	
		
		dictioanry = {
			"posting_date": invoice.posting_date,
			"customer_name": invoice.customer_name,
			"tax_id": invoice.tax_id,
			"items": items,
			"total_qty":invoice.total_qty,
			"total":invoice.total,
			"base_grand_total":invoice.base_grand_total,
			"invoice_number":invoice.name,
			"taxes":vat,
			"uom":units,
			"zero":invoice.total
		}

		data_array.append(dictioanry)
	return columns, data_array




		
