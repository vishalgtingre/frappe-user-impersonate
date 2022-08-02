// Copyright (c) 2022, Vishal Tingre and contributors
// For license information, please see license.txt

frappe.ui.form.on('User Impersonate Mapping', {
	refresh: function(frm) {
		set_user_list_filter(frm)
		get_impersonate_users(frm)
	},
	onload: function(frm) {
		set_user_list_filter(frm)
		get_impersonate_users(frm)
	},
	role_profile_name: function(frm) {
		set_user_list_filter(frm)
	}
});

function set_user_list_filter(frm) {
	if(frm.doc.role_profile_name){	
	frm.fields_dict['user_list'].grid.get_field('user').get_query = function(doc, cdt, cdn) {
		let d = locals[cdt][cdn];
		return {
			query: "user_impersonate.auth.user_roleprofile_list_query",
			filters: {'role_profile_name': frm.doc.role_profile_name}
		}
	}
	}
}

function get_impersonate_users(frm) {
	frm.set_query("impersonating_user", function() {
		return {
			query: "user_impersonate.auth.impersonated_user_list_query"
		};
	});
}