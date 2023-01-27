from . import __version__ as app_version

app_name = "tuna_technology"
app_title = "Tuna Technology"
app_publisher = "tuna-technology"
app_description = "Tuna Technology"
app_email = "tuna-technology@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/tuna_technology/css/jquery.calendars.picker.css",
    "/assets/tuna_technology/css/nepali-date.css"]

app_include_js = [
    "/assets/tuna_technology/js/jquery.plugin.js",
    "/assets/tuna_technology/js/jquery.calendars.js",
    "/assets/tuna_technology/js/jquery.calendars.nepali.js",
    "/assets/tuna_technology/js/jquery.calendars.picker.js",
    "/assets/tuna_technology/js/jquery.calendars.plus.js",
    "/assets/tuna_technology/js/tuna_technology.js"]

# include js, css files in header of web template
# web_include_css = "/assets/tuna_technology/css/tuna_technology.css"
# web_include_js = "/assets/tuna_technology/js/tuna_technology.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tuna_technology/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tuna_technology.utils.jinja_methods",
# 	"filters": "tuna_technology.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tuna_technology.install.before_install"
# after_install = "tuna_technology.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tuna_technology.uninstall.before_uninstall"
# after_uninstall = "tuna_technology.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tuna_technology.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

#doc_events = {
 #   "Sales Invoice": {
  #      "on_submit": "tuna_technology.hook.sales_invoice.on_submit"
   # }
#}



# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tuna_technology.tasks.all"
# 	],
# 	"daily": [
# 		"tuna_technology.tasks.daily"
# 	],
# 	"hourly": [
# 		"tuna_technology.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tuna_technology.tasks.weekly"
# 	],
# 	"monthly": [
# 		"tuna_technology.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "tuna_technology.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tuna_technology.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tuna_technology.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tuna_technology.auth.validate"
# ]

# Translation
# --------------------------------

# Make link fields search translated document names for these DocTypes
# Recommended only for DocTypes which have limited documents with untranslated names
# For example: Role, Gender, etc.
# translated_search_doctypes = []
fixtures=[
{
	"dt":"Custom Field",
	"filters":[["name", "in", ['Sales Invoice-print_count', 'Sales Invoice-print_by', 'Sales Invoice-print_date', 'Sales Invoice-synced_with_ird','Sales Invoice-synced_in_realtime', 'Sales Invoice-synced_datetime','Purchase Invoice-pragyapan_no','Purchase Invoice-total_taxable_import_company_currency', 'Purchase Invoice-pragyapan_date', 'Purchase Invoice-customs_clearance_point', 'Purchase Invoice-total_import_tax_company_currency' ]]]
}
]