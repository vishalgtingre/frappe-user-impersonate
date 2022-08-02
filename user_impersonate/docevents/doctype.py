from __future__ import unicode_literals

import frappe
from user_impersonate.auth import is_impersonated

def after_insert(doc, event=None):
    impersonatedusersession = is_impersonated()
    print (impersonatedusersession)
    if impersonatedusersession:
        if doc.ref_doctype == "Communication" or doc.ref_doctype == "Comment":
            print (doc.ref_doctype)
            return
        newdoc = frappe.get_doc(doc.ref_doctype, doc.docname)
        comment = newdoc.add_comment("Comment", "the below change was done in a Impersonated Session by " + impersonatedusersession['impersonating_user'] + " on behalf of " + impersonatedusersession['full_name'] )
        comment.sender_full_name = impersonatedusersession['impersonating_user']
        comment.save()

def before_save(doc,event=None):
    impersonatedusersession = is_impersonated()
    print (impersonatedusersession)
    if impersonatedusersession:
        if doc.ref_doctype == "Communication" or doc.ref_doctype == "Comment":
            return
        usertest = impersonatedusersession['impersonating_user'].replace("@","_") + " As " + impersonatedusersession['full_name']
        print (usertest)
        doc.owner = usertest