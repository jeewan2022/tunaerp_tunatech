// Copyright (c) 2022, tuna-technology and contributors
// For license information, please see license.txt

frappe.ui.form.on('IRD Nepal Settings', {
    onload: function (frm) {
        frappe.call({
            method: "tuna_technology.tuna_technology.doctype.ird_nepal_settings.ird_nepal_settings.return_naming_series",
            args: {
                "doc": "Purchase Invoice"
            },
            callback: function (r) {
                frm.set_df_property('purchase_import_naming_series', 'options', [""].concat(r.message));
            }
        });
    }
});
