// Copyright (c) 2022, tuna-technology and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthwise Sales Register"] = {
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
            fieldname: 'include_all',
            label: __('Including Sales Return'),
            fieldtype: 'Check',
            options:'Sales Invoice'
        }
	]
};
