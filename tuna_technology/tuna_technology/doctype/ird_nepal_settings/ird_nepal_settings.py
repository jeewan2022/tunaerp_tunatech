# Copyright (c) 2022, tuna-technology and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IRDNepalSettings(Document):
    def validate(self):
        self.cbms_last_sync_datetime = frappe.utils.now()


@frappe.whitelist()
def return_naming_series(doc):
    series = frappe.get_meta(doc).get_field("naming_series").options.strip().split("\n")
    return series
