// Copyright (c) 2022, tuna-technology and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Balance Confirmation"] = {
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
            fieldname: "party_type",
            label: __('Party type'),
            fieldtype: 'Link',
            options:"Party Type"
        },
		{
            fieldname: "party",
            label: __('Party'),
            fieldtype: 'Link',
            options:"Customer"
        },
        {
            fieldname: "include_detail",
            label: __('Include Detail ledger'),
            fieldtype: 'Check',
            options:"Customer"
        },
	]
};
