console.log("User Impersonate module is enabled")
/*frappe.Application = Class.extend({
    set_globals: function() {
        impersonatedsession = frappe.session.isimpersonated 
    }
})*/
//dom ready
var isimpersonated = false;

const li = document.createElement("li");
li.classList.add("Stop_UI");
li.style.backgroundColor='red';
li.innerHTML = '<a onclick="return stop_impersonate();"> Stop Impersonation </a>';


//For Webpage
//class="logged-in"

//let custswitchdesk = document.querySelector(".switch-to-desk")
//custswitchdesk.insertAdjacentElement('beforebegin',li)

var templateStopImp = '<a onclick="return stop_impersonate();"> Stop Impersonation </a>'

document.addEventListener("DOMContentLoaded",(event)=>{
    let custUInavbar = document.querySelector(".navbar-default")
    let custUIdrpdwn = document.querySelector(".dropdown-menu")
    let custswitchdesk = document.querySelector(".switch-to-desk")


    custUInavbar.style.backgroundColor="#fff";
    if (frappe.session.user == "Guest" || frappe.session.user == "" || frappe.session.user == null) {
        console.log("User Not Logged In")
    }
    else {
        console.log("User is Logged In")
        frappe.call({
        method: "user_impersonate.auth.is_impersonated", 
        callback: function(r) {
            console.log(r.message)
            if (r.message == false){
                isimpersonated = false
                }
            else {
                isimpersonated = true
                custUInavbar.style.backgroundColor="red"
                custUIdrpdwn.appendChild(li)
                console.log(frappe.session.isimpersonated)
                custswitchdesk.insertAdjacentElement('beforebegin',li)
                console.log("Impersonated Session is initiated")
                }
            }
        })
    }
});

function stop_impersonate(){
    frappe.call({
        method: "user_impersonate.auth.stop_impersonate",
        freeze: true,
        callback: function(r) {
            location.reload(true);
            frappe.set_route("List","User")
        }
    })
}