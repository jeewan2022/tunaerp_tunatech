# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt


import frappe


def execute(filters=None):
	columns = [
		{
		"fieldname":"Particular",
		"fieldtype":"Data",
		"label":("Particular"),
		"options":"Sales Invoice",
		"width":"300",
		},
		{
			
		"fieldname":"total",
		"fieldtype":"Data",
		"label":("Transaction Value"),
		"options":"Sales Invoice",
		"width":"200"
		},
		{
			
		"fieldname":"Paid",
		"fieldtype":"Data",
		"label":("Tax Paid On Purchase"),
		"options":"Purchase Invoice",
		"width":"200"
		},
		{
			
		"fieldname":"Collection",
		"fieldtype":"Data",
		"label":("Tax Collection from Sales"),
		"options":"Sales Invoice",
		"width":"200"
		},
		{
			
		"fieldname":"Remark",
		"fieldtype":"Data",
		"label":("Remark"),
		"options":"Sales Invoice",
		"width":"200"
		},
	]
	data = get_data(filters)
	
	return columns, data

def get_data(filters):
	conditions = ""
	conditionss = ""

	if filters.get("companies"):
			conditions += 'and sinv.company={}'.format(
			    frappe.db.escape(filters.get('companies')))

	if filters.get("companies"):
			conditionss += 'and pinv.company={}'.format(
			    frappe.db.escape(filters.get('companies')))

	if filters.get("fiscal_year"):
			conditions += "and sinv.posting_date={}".format(frappe.db.escape(filters.get("fiscal_year")))						

	if filters.get("month"):
		conditions += "and monthname(posting_date)={}".format(frappe.db.escape(filters.get("month")))	
			
	sales = frappe.db.sql("""select count(sinv.name), sum(sinv.grand_total), sum(sinv.total), sum(sinv.is_return), sum(sinv.total_taxes_and_charges)
	from `tabSales Invoice` sinv  where sinv.docstatus=1 {conditions}""".format(conditions=conditions), as_dict=1)

	purchase = frappe.db.sql("""select count(pinv.name), sum(pinv.is_return),  sum(pinv.grand_total), sum(pinv.total), sum(pinv.total_taxes_and_charges)
	 from `tabPurchase Invoice` pinv where pinv.docstatus=1  {conditions}""".format(conditions=conditionss), as_dict=1)				
	dictionary = [
		{"Particular":"Taxable Sales",
		"total":sales[0]['sum(sinv.total)'],
		"Collection":sales[0]['sum(sinv.total_taxes_and_charges)']},
		{"Particular":"Export"},
		{"Particular":"Exempted Sales"},
		{"Particular":"Taxable Purchase",
		"total":purchase[0]['sum(pinv.total)'],
		"Paid":purchase[0]['sum(pinv.total_taxes_and_charges)']
		},
		{"Particular":"Exempted Import"},
		{"Particular":"Other Adjustment/Sales returned/Cr.Note"},
		{"Particular":"Other Adjustment/Purchase retunred/Dr.note"},
		{"Particular":"Total",
		"Remark":sales[0]['sum(sinv.grand_total)']},
		{"Particular":"Debit/Credit"},
		{"Particular":"Vat to be adjusted from Last month"},
		{"Particular":"Net Tax Payable"},
		{"Particular":"Amt.requested for tax refund from Govt."},
		{"Particular":"Total Payment",
		"Collection":purchase[0]['sum(pinv.grand_total)']},
		{"Particular":"Number Of purchase Invoice",
		"Remark":purchase[0]['count(pinv.name)']},
		{"Particular":"Number Of credit Note",
		"Remark":purchase[0]['sum(pinv.is_return)']},
		{"Particular":"Number Of debit Note",
		"Remark":sales[0]['sum(sinv.is_return)']},
		{"Particular":"Number Of Credit Advice"},
		{"Particular":"Number Of Debit Advice"},
		{"Particular":"Number Of Sales Invoice",
		"Remark":sales[0]['count(sinv.name)']}

	]
	return dictionary
