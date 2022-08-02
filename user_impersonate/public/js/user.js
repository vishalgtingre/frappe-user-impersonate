frappe.ui.form.on('User', {
  refresh: function (frm) {
    var doc = frm.doc;
    var can_impersonate = false;
    frappe.call({
      method: "user_impersonate.auth.can_impersonate", 
      args: { "username": frm.doc.name},
      freeze: true,
      callback: function(r) {
        if (r.message == true) {
          can_impersonate = true;
        }
        if (can_impersonate == true && !frm.is_new()) {
          frm.add_custom_button(__("Impersonate User"), function () {
            frappe.call({
              method: "user_impersonate.auth.impersonate",
              args: { "username": frm.doc.name},
              freeze: true,
              callback: function (r) {
                location.reload(true);
                frappe.route();
                window.location.href = '/blog'
              } 
            })
          });
        }
      }
    })
  },
})

function has_access_to_edit_user() {
	return has_common(frappe.user_roles, get_roles_for_editing_user());
}

function get_roles_for_editing_user() {
	return frappe.get_meta('User').permissions
		.filter(perm => perm.permlevel >= 1 && perm.write)
		.map(perm => perm.role) || ['System Manager'];
}