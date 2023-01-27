from cgitb import text
from datetime import datetime
from xmlrpc.client import DateTime
import frappe
import requests
import json
from erpnext.accounts.utils import get_fiscal_year
from frappe.utils import today


def on_submit(doc, method):
    if doc.is_return == 1:
        return_sales_invoice(doc)
    else:
        sales_invoice(doc)


def sales_invoice(doc):
    ird_settings = frappe.get_doc("IRD Nepal Settings")
    customer_tax_id = frappe.db.get_value("Customer", doc.customer, "tax_id")
    company_tax_id = frappe.db.get_value("Company", doc.company, "tax_id")
    company_name = frappe.db.get_value("Company", doc.company, "name")
    if ird_settings.enable_sync == 1:
        payload = {
            'username': ird_settings.cbms_username,
            'password': ird_settings.cbms_password,
            'invoice_number': doc.name,
            'buyer_name': doc.customer_name,
            'invoice_date': doc.creation.split(" ")[0].replace("-", "."),
            'isrealtime': ird_settings.cbms_realtime,
            'seller_pan': company_tax_id,
            'buyer_pan': customer_tax_id,
            'fiscal_year': get_fiscal_year(today(), company=company_name)[0],
            'total_sales': doc.grand_total,
            'taxable_sales_vat': doc.total,
            'vat': doc.base_total_taxes_and_charges,
            'excisable_amount': 0,
            'excise': 0,
            'taxable_sales_hst': 0,
            'hst': 0,
            'amount_for_esf': 0,
            'esf': 0,
            'export_sales': 0,
            'tax_exempted_sales': 0,
            'datetimeClient': today().replace("-", ".")
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(ird_settings.cbms_server + "/api/bill",
                          data=json.dumps(payload), headers=headers)
        response_dict = json.loads(r.text)
        if response_dict == 101:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Cannot Synced Invoice with CBMS</div> <p><b>Error</b>: Bill Already exists</p> <p>Code: 101</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.save()
        if response_dict == 100:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Cannot Synced Invoice with CBMS</div> <p><b>Error</b>: API credentials do not match(additional:Check tax ID of customer and company too)</p> <p>Code: 100</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.save()
        if response_dict == 104:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Cannot Synced Invoice with CBMS</div> <p><b>Error</b>: Model Invalid</p> <p>Code: 104</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.save()
        if response_dict == 200:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Synced Invoice with CBMS</div> <p><b>Success</b>: Synced</p> <p>Code: 200</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.synced_with_ird = 1
                sales_doc.synced_date = str(datetime.now())
                if(ird_settings.cbms_realtime == 1):
                    sales_doc.is_real_time = 1
                sales_doc.save()
        print("Response", response_dict)


def return_sales_invoice(doc):
    ird_settings = frappe.get_doc("IRD Nepal Settings")
    customer_tax_id = frappe.db.get_value("Customer", doc.customer, "tax_id")
    company_tax_id = frappe.db.get_value("Company", doc.company, "tax_id")
    if ird_settings.enable_sync == 1:
        payload = {'username': ird_settings.cbms_username,
                   'password': ird_settings.cbms_password,
                   'ref_invoice_number': doc.return_against,
                   'credit_note_number': doc.name,
                   'buyer_name': doc.customer_name,
                   'credit_note_date': doc.creation.split(" ")[0].replace("-", "."),
                   'isrealtime': ird_settings.cbms_realtime,
                   'seller_pan': company_tax_id,
                   'buyer_pan': customer_tax_id,
                   'fiscal_year': get_fiscal_year(today(), company="Test PCV Company")[0],
                   'reason_for_return': 'Defect in piece',
                   'total_sales': doc.grand_total,
                   'taxable_sales_vat': doc.total,
                   'vat': doc.base_total_taxes_and_charges,
                   'excisable_amount': 0,
                   'excise': 0,
                   'taxable_sales_hst': 0,
                   'hst': 0,
                   'amount_for_esf': 0,
                   'esf': 0,
                   'export_sales': 0,
                   'tax_exempted_sales': 0,
                   'datetimeClient': today().replace("-", ".")
                   }
        headers = {'content-type': 'application/json'}
        r = requests.post(ird_settings.cbms_server + "/api/billreturn",
                          data=json.dumps(payload), headers=headers)
        response_dict = json.loads(r.text)
        if response_dict == 101:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Cannot Synced Invoice with CBMS</div> <p><b>Error</b>: Bill Already exists</p> <p>Code: 101</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.save()
        if response_dict == 100:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Cannot Synced Invoice with CBMS</div> <p><b>Error</b>: API credentials do not match(additional:Check tax ID of customer and company too)</p> <p>Code: 100</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.save()
        if response_dict == 104:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Cannot Synced Invoice with CBMS</div> <p><b>Error</b>: Model Invalid</p> <p>Code: 104</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.save()
        if response_dict == 200:
            if(doc.doctype == "Sales Invoice"):
                sales_doc = frappe.get_doc("Sales Invoice", doc.name)
                sales_doc.add_comment(
                    'Comment', text=f"<div>Synced Invoice with CBMS</div> <p><b>Success</b>: Synced</p> <p>Code: 200</p> <p><b>URL</b>: {ird_settings.cbms_server}/api/bill </p> <br/> <b>Payload</b> <pre><code>{payload}</code></pre>")
                sales_doc.synced_with_ird = 1
                sales_doc.synced_date = str(datetime.now())
                if(ird_settings.cbms_realtime == 1):
                    sales_doc.is_real_time = 1
                sales_doc.save()
        print("Response", response_dict)

@frappe.whitelist()    
def on_synced_with_ird_click():    
    values = frappe.db.sql("""select sinv.name from `tabSales Invoice` sinv where sinv.synced_with_ird=0 and docstatus !=2;""",debug=True, as_dict=1)
    ird_settings = frappe.get_doc("IRD Nepal Settings")
    ird_settings.cbms_enable_sync=1
    ird_settings.save()
    for value in values:
        doc = frappe.get_doc("Sales Invoice", value["name"])
        data = sales_invoice(doc)

       
    frappe.msgprint(data)     
    ird_settings.cbms_enable_sync=0
    ird_settings.save()