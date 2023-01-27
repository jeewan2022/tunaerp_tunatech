// Copyright (c) 2022, tuna-technology and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Return VAT Register"] = {
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
            options:'Sales Invoice'
        },
        {
            fieldname: 'to_date',
            label: __('To Date'),
            fieldtype: 'Date',
            options:'Sales Invoice'
        },
	]
};
