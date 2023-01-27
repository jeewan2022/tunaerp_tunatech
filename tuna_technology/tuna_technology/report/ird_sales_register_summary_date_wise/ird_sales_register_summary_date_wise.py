# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

import frappe
import nepali_datetime


def execute(filters=None):
		get_conditions(filters)
		columns = [
			{
				"fieldname":"posting_date",
				"fieldtype":"Data",
				"label":("Date(B.S.)"),
				"options":"Sales Invoice",
			},
			{
				"fieldname":"english_date",
				"fieldtype":"Data",
				"label":("Date(A.D.)"),
				"options":"Sales Invoice",
			},
			{
				"fieldname":"invoice_number",
				"fieldtype":"Link",
				"label":("Inv. No"),
				"options":"Sales Invoice"
			},
			{
				"fieldname":"customer_name",
				"fieldtype":"Link",
				"label":("Customer Name"),
				"options":"Customer",
			},
			{
				"fieldname":"tax_id",
				"label":("Customer PAN"),
				"fieldtype":"Data"
			},
			{
				"fieldname":"total_qty",
				"fieldtype":"Data",
				"label":("Qty"),
				"options":"Sales Invoice",
				"width": 80,
			},
			{
				"fieldname":"total",
				"fieldtype":"Link",
				"label":("B. Amt"),
				"options":"Sales Invoice",
			},
			{
				"fieldname":"taxes",
				"fieldtype":"Data",
				"label":("Vat"),
				"options":"Sales Invoice",
				"width": 80,
			},
			{
				"fieldname":"grand_total",
				"fieldtype":"Data",
				"label":("Total Amount"),
				"options":"Sales Invoice",
			},
			{
				"fieldname":"credits",
				"fieldtype":"Link",
				"label":("Cash/Credit"),
				"options":"Sales Invoice",
			},
		]
		data = frappe.get_all("Sales Invoice",filters={})
		data_array = []
		for d in data: 
			invoice = frappe.get_doc("Sales Invoice", d)
			modeOfPayment = "CREDIT"
			allocated_total = 0
			total_amount = 0
			invoice_details = frappe.get_doc("Sales Invoice", d.name)
			
			payment_entry_refrence = frappe.get_list("Payment Entry Reference", filters={
                        'reference_name': invoice.name
                })



			for payment in payment_entry_refrence:

				ref_payment= frappe.get_doc("Payment Entry Reference", payment.name)
				total_amount = ref_payment.total_amount
				allocated_total += ref_payment.allocated_amount
				payment_date = frappe.utils.format_datetime(ref_payment.creation) 

			if(len(payment_entry_refrence) > 0):
				if(allocated_total >= total_amount):
					modeOfPayment = "CASH"

			items = ""
			for item in invoice.items:
				items = items + item.item_name	
			Ss = ""

			if(d.status != "Cancelled"):
				for vat in invoice.taxes:
					Ss = Ss + str(vat.tax_amount)
			units = ""
			for un in invoice.items:
				units = units + un.uom
			tax_exemption = "0.0"
			ex = 0
			for tax_exem in invoice.taxes:
				tax_exemption = str(tax_exemption)
			english_date = invoice_details.posting_date
			english_date = str(english_date).replace("-",".")
			
			posting_date = nepali_datetime.date.from_datetime_date(invoice_details.posting_date)
			posting_date = str(posting_date).replace("-",".")

			data1 = {
				"posting_date": posting_date,
				"customer_name": invoice.customer_name,
				"tax_id": invoice.tax_id,
				"items": items,
				"total_qty":invoice.total_qty,
				"total":invoice.total,
				"total":invoice.total,
				"grand_total":invoice.grand_total,
				"invoice_number":invoice.name,
				"taxes":invoice.total_taxes_and_charges,
				"tax_exemption":tax_exemption,
				"total":invoice.total,
				"uom":units,
				"english_date":english_date,
				"credits":modeOfPayment
			}
			
			data_array.append(data1)
		return columns, data_array
def get_conditions(filters):
    conditions = ""
    if filters.get("company"): conditions += " and company=%(company)s"
    if filters.get("customer"): conditions += " and customer = %(customer)s"
    if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
    if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"
    return conditions		