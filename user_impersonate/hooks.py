# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

import frappe as _frappe

app_name = "user_impersonate"
app_title = "User Impersonate"
app_publisher = "Vishal Tingre"
app_description = "App for User Impersonation "
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "vishal.tingre@elastic.run"
app_license = "MIT"
error_report_email = "engg.support@with.run"

# Includes in <head>
# ------------------
# include js, css files in header of desk.html
# app_include_css = "/assets/user_impersonate/css/user_impersonate.css"
# app_include_js = "/assets/user_impersonate/js/user_impersonate.js"
app_include_js = "/assets/user_impersonate/js/user_impersonate.js"
# include js, css files in header of web template
# web_include_css = "/assets/user_impersonate/css/user_impersonate.css"
web_include_js = "/assets/user_impersonate/js/user_impersonate.js"
# include js in page
page_js = {"page" : "/assets/user_impersonate/js/user_impersonate.js"}
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"User": "public/js/user.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
on_login = 'user_impersonate.auth.successful_impersonate'
#on_session_creation = 'app.overrides.allocate_free_credits'
#on_logout = 'user_impersonate.auth.stop_impersonate'
extend_bootinfo = "user_impersonate.auth.boot_session"

doc_events = {
     "Version": {
        #"on_update": "user_impersonate.docevents.doctype.on_update",
        "before_save":"user_impersonate.docevents.doctype.before_save",
        "after_insert":"user_impersonate.docevents.doctype.after_insert"
        #"on_cancel": "user_impersonate.docevents.doctype.on_cancel",
        #"on_trash": "user_impersonate.docevents.doctype.on_trash"
    }
}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "user_impersonate.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "user_impersonate.install.before_install"
# after_install = "user_impersonate.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "user_impersonate.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"user_impersonate.tasks.all"
# 	],
# 	"daily": [
# 		"user_impersonate.tasks.daily"
# 	],
# 	"hourly": [
# 		"user_impersonate.tasks.hourly"
# 	],
# 	"weekly": [
# 		"user_impersonate.tasks.weekly"
# 	]
# 	"monthly": [
# 		"user_impersonate.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "user_impersonate.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "user_impersonate.event.get_events"
# }

