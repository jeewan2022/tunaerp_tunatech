// Copyright (c) 2022, tuna-technology and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['IRD Sales Register Summary-Date Wise'] = {
  filters: [
    {
      fieldname: 'companies',
      label: __('Companies'),
      fieldtype: 'Link',
      options: 'Company',
      default: frappe.defaults.get_user_default('company'),
    },
    {
      fieldname: 'fiscal_year',
      label: __('Fiscal Year'),
      fieldtype: 'Link',
      options: 'Fiscal Year',
    },
    {
      fieldname: 'fiscal_year',
      label: __('From Date'),
      fieldtype: 'Date',
      options: 'Sales Invoice',
    },
    {
      fieldname: 'fiscal_year',
      label: __('To Date'),
      fieldtype: 'Date',
      options: 'Sales Invoice',
    },
  ],
};
