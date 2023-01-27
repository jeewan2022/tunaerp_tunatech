# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from os import access
from pydoc import resolve
import re
import frappe
from frappe.utils import flt
from frappe import log, msgprint, _
from frappe.model.meta import get_field_precision
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions, get_dimension_with_children
from traitlets import default


def execute(filters=None):
    return _execute(filters)

def _execute(filters, additional_table_columns=None, additional_query_columns=None):
    if not filters:
        filters = frappe._dict({})

    invoice_list = get_invoices(filters, additional_query_columns)
    columns, income_accounts, tax_accounts = get_columns(invoice_list, additional_table_columns)


    if not invoice_list:
        msgprint(_("No record found"))
        return columns, invoice_list






    invoice_income_map = get_invoice_income_map(invoice_list)
    invoice_income_map, invoice_tax_map = get_invoice_tax_map(invoice_list,
            invoice_income_map, income_accounts)
    #Cost Center & Warehouse Map
    invoice_cc_wh_map = get_invoice_cc_wh_map(invoice_list)
    invoice_so_dn_map = get_invoice_so_dn_map(invoice_list)
    company_currency = frappe.get_cached_value('Company',  filters.get("company"),  "default_currency")
    mode_of_payments = get_mode_of_payments([inv.name for inv in invoice_list])



    data = []
    for inv in invoice_list:
        # invoice details
        sales_order = list(set(invoice_so_dn_map.get(inv.name, {}).get("sales_order", [])))
        delivery_note = list(set(invoice_so_dn_map.get(inv.name, {}).get("delivery_note", [])))
        cost_center = list(set(invoice_cc_wh_map.get(inv.name, {}).get("cost_center", [])))
        warehouse = list(set(invoice_cc_wh_map.get(inv.name, {}).get("warehouse", [])))

        invoice_details = frappe.get_doc("Sales Invoice", inv.name)
        fiscal_year = frappe.defaults.get_user_default("fiscal_year")
        customer_details = frappe.get_doc("Customer", inv.customer)
        qty = invoice_details.total_qty

        english_date = invoice_details.posting_date
        english_date = str(english_date).replace("-",".")

        default_country = frappe.db.get_default("country")
    

        export = ""

        is_synced = "No"
        is_realtime = "No"

        if invoice_details.synced_with_ird == 1:
            is_synced = "Yes"

        if invoice_details.is_real_time == 1 or invoice_details.is_real_time == None:
            is_realtime = "Yes"

        return_invoice_date = ""

        if default_country == customer_details.country or customer_details.country == None:
            export = "Local"
        else:
            export = "Export"

        access_log = frappe.get_list("Access Log", filters={
                "reference_document": invoice_details.name, 
                "file_type": "PDF",
                "method": "Print"
                        })
        printed_date = ""
        printed_by = ""
        payment_date=""
        reference_no = ""
        modeOfPayment = "CREDIT"
        allocated_total = 0
        total_amount = 0
        vat_return = ""
        printed_times = 0

        printed_times = len(access_log)
        printed_times= str(printed_times)

        payment_entry_refrence = frappe.get_list("Payment Entry Reference", filters={
                        'reference_name': invoice_details.name
                })



        for payment in payment_entry_refrence:

            ref_payment= frappe.get_doc("Payment Entry Reference", payment.name)
            total_amount = ref_payment.total_amount
            allocated_total += ref_payment.allocated_amount
            payment_date = frappe.utils.format_datetime(ref_payment.creation) 

        if(len(payment_entry_refrence) > 0):
            if(allocated_total >= total_amount):
                modeOfPayment = "CASH"


        # if(invoice_details.status == "Paid"):

        #     if(len(invoice_details.payments) > 0):

        #         payment_detail = invoice_details.payments[0]

        #         payment_date = frappe.utils.format_datetime(payment_detail.modified)



            # if(payment_entry != None):
            #         reference_no = payment_entry.reference_no

            # if(payment_detail.reference_no != None):
            #         reference_no = payment_detail.reference_no


        if(len(access_log)> 0):
            access_log_detail = frappe.get_doc("Access Log",access_log[0].name)
            if access_log_detail.reference_document != None:
                printed_date = str(access_log_detail.timestamp)
                printed_by = access_log_detail.user


        import nepali_datetime

        if(invoice_details.return_against != None):
            return_against_invoice = frappe.get_doc("Sales Invoice", invoice_details.return_against)
            return_invoice_date = return_against_invoice.posting_date
            return_invoice_date = nepali_datetime.date.from_datetime_date(return_invoice_date)
            return_invoice_date = str(return_invoice_date).replace("-",".")

        posting_date = nepali_datetime.date.from_datetime_date(invoice_details.posting_date)
        posting_date = str(posting_date).replace("-",".")

        non_taxable = 0
        taxable = 0

        for item in invoice_details.items:

            if(item.item_tax_template == None):
                non_taxable += item.amount
            else:
                taxable += item.amount


        is_printed = "N"

        if len(access_log) > 0:
            is_printed = "Y"
        else:
            is_printed = "N"


        row = {
                'invoice': inv.name,
                'posting_date': inv.posting_date,
                'customer': inv.customer,
                'customer_name': inv.customer_name,
                'exempted': non_taxable,
                'taxable_value': taxable,
                'fiscal_year': fiscal_year,
                'ref_bill_date': return_invoice_date,
                'is_bill_printed':  is_printed,
                'printed_timestamp': printed_date,
                'entered_by': invoice_details.owner,
                'printed_by': printed_by,
                'payment_date': payment_date,
                'printed_times': printed_times,
                'discount_amount': invoice_details.discount_amount,
                'export': export,
                'is_synced': is_synced,
                'is_realtime': is_realtime,
                'transaction_id': reference_no,
                'modeOfPayment': modeOfPayment,
                'vat_return': vat_return,
                'qty': qty,
                'return_against': invoice_details.return_against,
                'posting_date': posting_date,
                'english_date': english_date
        }

        if additional_query_columns:
            for col in additional_query_columns:
                row.update({
                        col: inv.get(col)
                })

        row.update({
                'customer_group': inv.get("customer_group"),
                'territory': inv.get("territory"),
                'tax_id': inv.get("tax_id"),
                'receivable_account': inv.debit_to,
                'mode_of_payment':  ", ".join(mode_of_payments.get(inv.name, [])),
                'project': inv.project,
                'owner': inv.owner,
                'remarks': inv.remarks,
                'sales_order': ", ".join(sales_order),
                'delivery_note': ", ".join(delivery_note),
                'cost_center': ", ".join(cost_center),
                'warehouse': ", ".join(warehouse),
                'currency': company_currency
        })

        # map income values
        base_net_total = 0
        for income_acc in income_accounts:
            income_amount = flt(invoice_income_map.get(inv.name, {}).get(income_acc))
            base_net_total += income_amount
            row.update({
                    frappe.scrub(income_acc): income_amount
            })

        # net total
        row.update({'net_total': base_net_total or inv.base_net_total})

        # tax account
        total_tax = 0
        for tax_acc in tax_accounts:
            if tax_acc not in income_accounts:
                tax_amount_precision = get_field_precision(frappe.get_meta("Sales Taxes and Charges").get_field("tax_amount"), currency=company_currency) or 2
                tax_amount = flt(invoice_tax_map.get(inv.name, {}).get(tax_acc), tax_amount_precision)
                total_tax += tax_amount
                row.update({
                        frappe.scrub(tax_acc): tax_amount
                })

        # total tax, grand total, outstanding amount & rounded total

        row.update({
                'tax_total': total_tax,
                'grand_total': inv.base_grand_total,
                'rounded_total': inv.base_rounded_total,
                'outstanding_amount': inv.outstanding_amount
        })

        data.append(row)

    return columns, data

def get_columns(invoice_list, additional_table_columns):
    """return columns based on filters"""


    # if additional_table_columns:
    #     columns += additional_table_columns

   
    income_accounts = []
    tax_accounts = []
    income_columns = []
    tax_columns = []

    if invoice_list:
        income_accounts = frappe.db.sql_list("""select distinct income_account
			from `tabSales Invoice Item` where docstatus = 1 and parent in (%s)
			order by income_account""" %
                ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]))

        tax_accounts = frappe.db.sql_list("""select distinct account_head
			from `tabSales Taxes and Charges` where parenttype = 'Sales Invoice'
			and docstatus = 1 and base_tax_amount_after_discount_amount != 0
			and parent in (%s) order by account_head""" %
                ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]))

    for account in income_accounts:
        income_columns.append({
                "label": account,
                "fieldname": frappe.scrub(account),
                "fieldtype": "Currency",
                "options": 'currency',
                "width": 120
        })

    for account in tax_accounts:
        if account not in income_accounts:
            tax_columns.append({
                    "label": account,
                    "fieldname": frappe.scrub(account),
                    "fieldtype": "Currency",
                    "options": 'currency',
                    "width": 120
            })

   

    columns = [
			{
                    'label': _("Bill Date(B.S.)"),
                    'fieldname': 'posting_date',
                    'fieldtype': 'Data',
                    'width': 80
            },
            {
                    'label': _("Bill Date(A.D.)"),
                    'fieldname': 'english_date',
                    'fieldtype': 'Data',
                    'width': 80
            },
			{
                    'label': _("Bill No"),
                    'fieldname': 'invoice',
                    'fieldtype': 'Link',
                    'options': 'Sales Invoice',
                    'width': 120
            },
			{
                    'label': _("Customer Name"),
                    'fieldname': 'customer_name',
                    'fieldtype': 'Data',
                    'width': 120
            },
			{
                    'label': _("Customer PAN"),
                    'fieldname': 'tax_id',
                    'fieldtype': 'Data',
                    'width': 120
            },
			{
                    'label': _("Exempted"),
                    'fieldname': 'exempted',
                    'fieldtype': 'Data',
                    'width': 120
            },
            {
                    'label': _("Taxable value"),
                    'fieldname': 'taxable_value',
                    'fieldtype': 'Data',
                    'width': 120
            },
			{
                    'label': _("Export"),
                    'fieldname': 'export',
                    'fieldtype': 'Data',
                    'width': 120
            },
			{
                    "label": _("VAT"),
                    "fieldname": "tax_total",
                    "fieldtype": "Currency",
                    "options": 'currency',
                    "width": 120
            },

			{
                    "label": _("Grand Total"),
                    "fieldname": "grand_total",
                    "fieldtype": "Currency",
                    "options": 'currency',
                    "width": 120
            },
    ]

    return columns, income_accounts, tax_accounts

def get_conditions(filters):
    conditions = ""

    if filters.get("company"):
        conditions += " and company=%(company)s"
    if filters.get("customer"):
        conditions += " and customer = %(customer)s"

    if filters.get("from_date"):
        conditions += " and posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and posting_date <= %(to_date)s"

    if filters.get("owner"):
        conditions += " and owner = %(owner)s"

    if filters.get("mode_of_payment"):
        conditions += """ and exists(select name from `tabSales Invoice Payment`
			 where parent=`tabSales Invoice`.name
			 	and ifnull(`tabSales Invoice Payment`.mode_of_payment, '') = %(mode_of_payment)s)"""

    if filters.get("cost_center"):
        conditions += """ and exists(select name from `tabSales Invoice Item`
			 where parent=`tabSales Invoice`.name
			 	and ifnull(`tabSales Invoice Item`.cost_center, '') = %(cost_center)s)"""

    if filters.get("warehouse"):
        conditions += """ and exists(select name from `tabSales Invoice Item`
			 where parent=`tabSales Invoice`.name
			 	and ifnull(`tabSales Invoice Item`.warehouse, '') = %(warehouse)s)"""

    if filters.get("brand"):
        conditions += """ and exists(select name from `tabSales Invoice Item`
			 where parent=`tabSales Invoice`.name
			 	and ifnull(`tabSales Invoice Item`.brand, '') = %(brand)s)"""

    if filters.get("item_group"):
        conditions += """ and exists(select name from `tabSales Invoice Item`
			 where parent=`tabSales Invoice`.name
			 	and ifnull(`tabSales Invoice Item`.item_group, '') = %(item_group)s)"""

    accounting_dimensions = get_accounting_dimensions(as_list=False)

    if accounting_dimensions:
        common_condition = """
			and exists(select name from `tabSales Invoice Item`
				where parent=`tabSales Invoice`.name
			"""
        for dimension in accounting_dimensions:
            if filters.get(dimension.fieldname):
                if frappe.get_cached_value('DocType', dimension.document_type, 'is_tree'):
                    filters[dimension.fieldname] = get_dimension_with_children(dimension.document_type,
                            filters.get(dimension.fieldname))

                    conditions += common_condition + "and ifnull(`tabSales Invoice Item`.{0}, '') in %({0})s)".format(dimension.fieldname)
                else:
                    conditions += common_condition + "and ifnull(`tabSales Invoice Item`.{0}, '') in (%({0})s))".format(dimension.fieldname)

    return conditions

def get_invoices(filters, additional_query_columns):
    if additional_query_columns:
        additional_query_columns = ', ' + ', '.join(additional_query_columns)

    conditions = get_conditions(filters)
    return frappe.db.sql("""
		select name, posting_date, creation, debit_to, project, customer,
		customer_name, owner, remarks, territory, tax_id, customer_group,
		base_net_total, base_grand_total, base_rounded_total, outstanding_amount {0}
		from `tabSales Invoice`
		where docstatus = 1 %s order by posting_date desc, name desc""".format(additional_query_columns or '') %
            conditions, filters, as_dict=1)

def get_invoice_income_map(invoice_list):
    income_details = frappe.db.sql("""select parent, income_account, sum(base_net_amount) as amount
		from `tabSales Invoice Item` where parent in (%s) group by parent, income_account""" %
            ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

    invoice_income_map = {}
    for d in income_details:
        invoice_income_map.setdefault(d.parent, frappe._dict()).setdefault(d.income_account, [])
        invoice_income_map[d.parent][d.income_account] = flt(d.amount)

    return invoice_income_map

def get_invoice_tax_map(invoice_list, invoice_income_map, income_accounts):
    tax_details = frappe.db.sql("""select parent, account_head,
		sum(base_tax_amount_after_discount_amount) as tax_amount
		from `tabSales Taxes and Charges` where parent in (%s) group by parent, account_head""" %
            ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

    invoice_tax_map = {}
    for d in tax_details:
        if d.account_head in income_accounts:
            if d.account_head in invoice_income_map[d.parent]:
                invoice_income_map[d.parent][d.account_head] += flt(d.tax_amount)
            else:
                invoice_income_map[d.parent][d.account_head] = flt(d.tax_amount)
        else:
            invoice_tax_map.setdefault(d.parent, frappe._dict()).setdefault(d.account_head, [])
            invoice_tax_map[d.parent][d.account_head] = flt(d.tax_amount)

    return invoice_income_map, invoice_tax_map

def get_invoice_so_dn_map(invoice_list):
    si_items = frappe.db.sql("""select parent, sales_order, delivery_note, so_detail
		from `tabSales Invoice Item` where parent in (%s)
		and (ifnull(sales_order, '') != '' or ifnull(delivery_note, '') != '')""" %
            ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

    invoice_so_dn_map = {}
    for d in si_items:
        if d.sales_order:
            invoice_so_dn_map.setdefault(d.parent, frappe._dict()).setdefault(
                    "sales_order", []).append(d.sales_order)

        delivery_note_list = None
        if d.delivery_note:
            delivery_note_list = [d.delivery_note]
        elif d.sales_order:
            delivery_note_list = frappe.db.sql_list("""select distinct parent from `tabDelivery Note Item`
				where docstatus=1 and so_detail=%s""", d.so_detail)

        if delivery_note_list:
            invoice_so_dn_map.setdefault(d.parent, frappe._dict()).setdefault("delivery_note", delivery_note_list)

    return invoice_so_dn_map

def get_invoice_cc_wh_map(invoice_list):
    si_items = frappe.db.sql("""select parent, cost_center, warehouse
		from `tabSales Invoice Item` where parent in (%s)
		and (ifnull(cost_center, '') != '' or ifnull(warehouse, '') != '')""" %
            ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

    invoice_cc_wh_map = {}
    for d in si_items:
        if d.cost_center:
            invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
                    "cost_center", []).append(d.cost_center)

        if d.warehouse:
            invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
                    "warehouse", []).append(d.warehouse)

    return invoice_cc_wh_map




def get_mode_of_payments(invoice_list):
    mode_of_payments = {}
    if invoice_list:
        inv_mop = frappe.db.sql("""select parent, mode_of_payment
			from `tabSales Invoice Payment` where parent in (%s) group by parent, mode_of_payment""" %
                ', '.join(['%s']*len(invoice_list)), tuple(invoice_list), as_dict=1)

        for d in inv_mop:
            mode_of_payments.setdefault(d.parent, []).append(d.mode_of_payment)

    return mode_of_payments



