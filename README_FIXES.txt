GATHERUP FIX PATCH
==================

This patch was built against the uploaded GatherUp project.

FIXED
-----
1. Persistent chat notifications are created for every other member of the group.
2. Dashboard Quick Actions now ask which group to use instead of silently using the first group.
3. Dashboard WORKSPACE navigation now opens a group picker for group-scoped features.
4. Email ownership verification was added. Registration sends a real verification email; login is blocked until verification.
5. Poll result response schemas were corrected to match the frontend and database, fixing result loading/voting.
6. Group page now honors dashboard action links such as #events, #expenses, #polls, #tasks, #food and #gallery.
7. The service worker is now served at /service-worker.js and the cache version was bumped.

EMAIL SETUP
-----------
Copy the SMTP settings from .env.example into your existing .env and fill them with
your own SMTP provider credentials.

For Gmail SMTP:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your Gmail address
SMTP_PASSWORD=your Gmail App Password
SMTP_FROM=your Gmail address

Do NOT use your normal Gmail password. Use a Google App Password.

PUBLIC_BASE_URL should be the address users can open from the verification email.
For local testing on the same computer:
PUBLIC_BASE_URL=http://127.0.0.1:8000

DATABASE
--------
No existing database table is deleted or modified.
On application startup, GatherUp creates the new email_verifications table if it
does not already exist.

The existing database.py and .env are intentionally NOT included in this patch,
so your database password and JWT secret remain untouched.

INSTALL
-------
1. Stop Uvicorn.
2. Extract this patch into the existing GatherUp folder and allow the listed files
   to replace their current versions.
3. Add the SMTP variables from .env.example to your existing .env.
4. Start Uvicorn again:
   uvicorn backend.main:app --reload
5. Hard-refresh the browser with Ctrl+Shift+R.

IMPORTANT FOR EXISTING USERS
----------------------------
Existing accounts that have never been email-verified will be blocked from login
until they use the verification flow. The verification page includes a resend
button, so an existing account can request a new verification email.

No existing chat, event, expense, task, food, gallery or group data is deleted.
