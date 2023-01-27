// Copyright (c) 2022, tuna-technology and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Materialized Report"] = {
    onload:function(frm){
        frappe.query_report.page.add_inner_button(__("Sync With IRD"),function() {
         frappe.call({
                method:'tuna_technology.hook.sales_invoice.on_synced_with_ird_click',
            })
        });
        
    },
	"filters": [
		{
            fieldname: 'companies',
            label: __('Companies'),
            fieldtype: 'Link',
            options: 'Company',
			default:frappe.defaults.get_user_default("Comapny")
        },
		{
            fieldname: "fiscal_year",
            label: __('Fiscal Year'),
            fieldtype: 'Link',
            options:'Fiscal Year',
        },
		{
            fieldname: 'from_date',
            label: __('From Date'),
            fieldtype: 'Date',
            options:'Purchase Invoice',
        },
        {
            fieldname: 'to_date',
            label: __('To Date'),
            fieldtype: 'Date',
            options:'Sales Invoice',
        },
		{
            fieldname: 'include_return',
            label: __('Includes Sals Return'),
            fieldtype: 'Check',
            options:'Sales Invoice'
        },
		{
            fieldname: 'not_sync',
            label: __('Not Synced With IRD'),
            fieldtype: 'Check',
            options:'Sales Invoice'
        }
	]
	};
    
	
	
