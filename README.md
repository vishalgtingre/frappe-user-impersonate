## User Impersonation 15 Feb 2022

A separate app for User Impersonation on Frappe.

Administrators and Users with impersonate roles can impersonate other active users for testing purposes and view impersonation logs.

When impersonating another user, the Impersonating User (IU) has access to exactly what that user can access in the system, including the same menus and modules. The application views and records (reads, creates, updates and saves) anything the IU does while impersonating another user as having been done by that user except for adding in the Time Line info the tracking information which records the actions along with Impersonating User information

The user account to be impersonated must be active in the System.

The User impersonation can be extended by the apps by using the user impersonate API’s from backend

1. can_impersonate    {True/False}. Checks if the current user can impersonate the user provided in the input   
http://{SITENAME:[PORT]}/api/method/user_impersonate.auth.can_impersonate?username={USERNAME}

2. impersonate  {True/False}. Impersontes (logs in as the user and creates as session with this user)  the user provided in the input.
http://{SITENAME:[PORT]}/api/method/user_impersonate.auth.impersonate?username={USERNAME}

3. stop_impersonate {True/False} Stops or Ends the the current session if its impersonated and goes back to the previous User session 
http://{SITENAME:[PORT]}/api/method/user_impersonate.auth.stop_impersonate

4. can_impersonate_userlist provides the list of the users which the current user can impersonate
http://{SITENAME:[PORT]}/api/method/user_impersonate.auth.can_impersonate_userlist

5. is_impersonated tells if the surrent user session is impersonated.
http://site1.docker:8002/api/method/user_impersonate.auth.is_impersonated

#### License
MIT
