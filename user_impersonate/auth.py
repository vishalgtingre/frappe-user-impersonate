# Copyright (c) 2022, Vishal Tingre and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import datetime


import frappe
from frappe.utils import today
from frappe.sessions import delete_session


@frappe.whitelist()
def can_impersonate(username):
	#Permission.validate_authorized_user(dt, 'impersonate')
	if frappe.session.user == 'Administrator' and username != 'Administrator':
		return True
	if frappe.session.user == username or frappe.session.user == "Guest" or username == "Guest": 
		return False
	
	todaysdate = today()
	role_profile_name = frappe.db.get_value('User',username,fieldname='role_profile_name')
	if (frappe.db.count('User Impersonate Mapping', {'role_profile_name': role_profile_name,'impersonating_user':frappe.session.user,'end_time': [">=", todaysdate] }, ['username']) <= 0):
		return False
	if is_impersonated():
		return False
	user_roles = frappe.get_roles(frappe.session.user)
	if 'Impersonate User' in user_roles: 
		hasImpersonateRole = True
		return True
	return False

@frappe.whitelist()
def can_impersonate_userlist():
	try:
		impersonate_userlist = frappe.db.sql("""SELECT
													tuil.`user`,
													tu.full_name ,
													tu.mobile_no ,
													tuim.impersonating_user ,
													tuim.role_profile_name ,
													tuil.description
												FROM
													`tabUser Impersonate List` tuil,
													`tabUser Impersonate Mapping` tuim,
													`tabUser` tu
												WHERE
													tuil.parent = tuim.name
													and tuil.`user` = tu.name
													and tuim.end_time > CURDATE()
													and tu.role_profile_name = tuim.role_profile_name
													and tuim.impersonating_user =%s""", 
								frappe.session.user, as_dict=True)
		if impersonate_userlist: 
			return impersonate_userlist
	except:
		return False
	return False


@frappe.whitelist(allow_guest=True)
def is_impersonated():

	print(frappe.session.isimpersonated)
	print(frappe.session.impersonatedby)
	try:
		#impersonatedusersession = frappe.db.get_value('User Impersonate Session', {'usersid': frappe.session.sid}, ['username','mobile_no','impersonatinguser'], as_dict=1)
		
		impersonatedusersession = frappe.db.sql("""SELECT
														tuil.`user`,
														tu.full_name,
														tu.mobile_no,
														tuim.impersonating_user,
														tuim.role_profile_name,
														tuil.description
													FROM
														`tabUser Impersonate List` tuil,
														`tabUser Impersonate Mapping` tuim,
														`tabUser` tu,
														`tabUser Impersonate Session` tuis
													WHERE
														tuis.username = tuil.`user`
														AND tuis.impersonatinguser = tuim.impersonating_user
														AND tuil.parent = tuim.name
														AND tuil.`user` = tu.name
														AND tuis.usersid =%s""", 
									frappe.session.sid,as_dict=1)
	except:
		return False
	if impersonatedusersession: return impersonatedusersession[0]
	return False

@frappe.whitelist()
def users_list_by_role_profile(role_profile_name):
	users = frappe.get_all('User', filters={'role_profile_name': role_profile_name})
	return users


@frappe.whitelist()
def impersonate(username):
	if frappe.local.request.method != 'POST':
		frappe.throw("Method not supported")
		return False

	frappe.local.session.isimpersonated = "False"
	try:
		if can_impersonate(username):
			impersonatingsid = frappe.session.sid
			impersonatinguser = frappe.session.user
			#status, device, ipaddress = frappe.db.get_value('Sessions', {'usersid': impersonatingsid}, ['status','device','ipaddress'])
			#To Do replace frappe.db.sql with frappe.db.get_value
			user_details = frappe.db.sql("""select status, device, ipaddress from tabSessions where sid=%s""", impersonatingsid, as_dict=True)
			if user_details: 
				status = user_details[0].get("status")
				device = user_details[0].get("device")
				ipaddress = user_details[0].get("ipaddress")
			delete_session(frappe.session.sid, frappe.session.user, reason="Session cleared as "+ frappe.session.user + " Impersonated user :" + username)
			frappe.local.login_manager.login_as(username)
			frappe.local.session.isimpersonated = "True"
			frappe.local.session.impersonatedby = impersonatinguser
			add_User_Impersonate_Session (frappe.session.user, frappe.session.sid, ipaddress, device, status, impersonatinguser, impersonatingsid)
			return True
		else:
			return False
	except:
		return False

def successful_impersonate(login_manager):
	if frappe.local.session.isimpersonated:
		frappe.local.session.isimpersonated = "True"


@frappe.whitelist()
def stop_impersonate():
	username = frappe.session.user
	usersid = frappe.session.sid
	try:
		impersonatesession = frappe.db.get_value('User Impersonate Session', {'usersid': usersid}, ['name','impersonatinguser'],as_dict=1)
		if impersonatesession:
			impersonatinguser = impersonatesession.impersonatinguser
			frappe.db.set_value('User Impersonate Session', impersonatesession.name, 'endtime', datetime.now())
			delete_session(frappe.session.sid, frappe.session.user, reason="Impersonated Session stopped for "+ username + " by user :" + impersonatinguser)
			frappe.local.login_manager.login_as(impersonatinguser)
			frappe.local.session.isimpersonated = "False"
			#frappe.cache().hset('redirect_after_login', impersonatinguser, "/blog")
			return True
		else:
			return False
	except:
		return False

def add_User_Impersonate_Session(username, usersid, ipaddress, device, status, impersonatinguser, impersonatingsid):
	UserImpersonateSession = frappe.get_doc({
		"doctype": "User Impersonate Session",
		"username": username,
		"status": status,
		"usersid": usersid,
		"ipaddress": ipaddress,
		"device": device,
		"impersonatinguser": impersonatinguser,
		"impersonatingsid": impersonatingsid,
		"starttime": datetime.now()
	})
	UserImpersonateSession.insert(ignore_permissions=True, ignore_links=True)

@frappe.whitelist()
def user_roleprofile_list_query(doctype, txt, searchfield, start, page_len, filters):
	if not filters:
		return
	return frappe.db.sql("""
		SELECT name, full_name, email
		FROM
			`tabUser`
		WHERE
			role_profile_name = %(role_profile_name)s
			AND lower(name) like %(txt)s
		LIMIT
			%(start)s, %(page_len)s
	""", {
		'role_profile_name': filters.get('role_profile_name'),
		'txt': "%%%s%%" % txt.lower(),
		'start': start,
		'page_len': page_len,
	})

@frappe.whitelist()
def impersonated_user_list_query(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
		from tabUser u, `tabHas Role` r
		where u.name = r.parent and r.role = 'Impersonate User' 
		and u.enabled = 1 and u.name like %s""", ("%" + txt + "%"))


def boot_session(bootinfo):
	bootinfo.impersonatedby = ""
	bootinfo.isimpersonated = ""
	if is_impersonated(): 
		bootinfo.isimpersonated = "True"
	else: 
		bootinfo.isimpersonated = "False"