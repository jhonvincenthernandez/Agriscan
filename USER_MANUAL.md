# AgriScan+ User Manual

Version: 1.6.0
Audience: Farmers, Technicians, and Administrators
System: AgriScan+ rice farm management with disease detection and yield prediction

## 1. What AgriScan+ Does

AgriScan+ is a web system for rice farm work. You can use it on a phone or a computer with a modern browser.

Core tasks supported:

- Register fields and planting cycles
- Scan rice leaves for disease with AI assistance
- Predict yield with three model modes
- Record actual harvests
- Keep season logs for farm activities
- View reports and export data to CSV or PDF
- Read knowledge base articles and treatment guidance
- Receive notifications and announcements

Important rule: predictions are estimates for planning. Reports use actual harvest records as the verified source for production totals.

## 2. User Roles and Access

There are three roles. The menus you see depend on your role.

### Farmer

Daily farm work for your own records:

- Fields, plantings, scans, yield predictions, harvests
- Season logs, reports for personal scope, notifications
- Announcements, knowledge base, profile

### Technician

Support and monitoring across farmers:

- Review detections, plantings, fields, and logs
- Confirm treatment guidance and update records within allowed fields
- Use knowledge base as reference
- View reports and analytics within allowed scope

### Admin

System control and content maintenance:

- Approve users, assign roles, activate or deactivate accounts
- Manage system settings, thresholds, and toggles
- Manage knowledge base, varieties, treatments, announcements
- Review audit logs and archived records
- View system wide reports

If you cannot find a menu, it is often a role restriction. Check the section for your role before reporting a problem.

## 3. Getting Started

### 3.1 Create an Account

1. Open the application address in your browser.
2. Select Register.
3. Fill in username, password, contact details, and farm location if required. New accounts default to the Farmer role.
4. Submit the form.
5. Wait for admin approval. Accounts remain pending until an admin approves them.

If registration needs approval, you cannot access full features until an admin approves the account.

### 3.2 Log In

1. Open the login page.
2. Enter username and password.
3. Submit.
4. You land on the Dashboard for your role.

### 3.3 Use the Dashboard First

The Dashboard shows:

- Recent activity
- Notifications
- Key farm summaries
- System information including model version and last scan

Open the Dashboard before opening other modules. It helps you see what needs attention.

### 3.4 Open Help Inside the App

1. Select the Help icon in the top navigation bar, or open Help from the user menu.
2. Read the section that matches your current role.
3. Use the Quick Scan Guide and Quick Yield Guide for the two AI tools.
4. Switch language between Tagalog and English with the language buttons at the top of the Help page.

### 3.5 Log Out

Use Logout from the user menu when you finish, especially on a shared device.

## 4. Required Work Order

Follow this order so forms and AI tools work correctly:

Field then Planting then Scan or Yield Prediction then Harvest

Details:

- Create a Field record before creating a Planting record.
- Create an active Planting record before running a Scan.
- Use Scan and Yield Prediction during the active cycle.
- Record Harvest after actual harvest.
- A harvested planting is excluded from new scan selection. Start a new planting cycle for the next season.

## 5. Farmer Guide

### 5.1 First Five Tasks for a New Farmer

1. Create one Field record with name, area, and barangay.
2. Add one Planting record for the current season.
3. Run a Scan when leaf symptoms appear.
4. Check Yield Prediction for planning.
5. Record Harvest after harvest.

### 5.2 Manage Fields

Path: Fields

To create a field:

1. Open Fields.
2. Select Create.
3. Enter field name, area in hectares, barangay, and location notes.
4. Save.

To edit or remove:

- Use Edit to correct area, name, or location.
- Use Delete or Archive to remove the record from active lists. Archived records remain available for history and audit where supported.

Farm size totals update automatically when field records change.

### 5.3 Manage Planting Records

Path: Plantings

To create a planting:

1. Open Plantings.
2. Select Create.
3. Select Field and Rice Variety.
4. Enter planting date, season (wet or dry), ecosystem type, and growth duration if requested.
5. Enter historical production if available. This improves yield confidence.
6. Save.

If you see an error about planting date, check the allowed past days set by the admin. Enter a date inside the allowed range.

### 5.4 Run Disease Scan

Path: Scan or Camera

Steps:

1. Select the correct active Planting cycle in the form.
2. Capture a clear leaf photo with the camera page, or upload an existing photo on the scan page.
3. Select Analyze Image.
4. Wait for the AI result.
5. Review disease label, confidence, severity, and treatment suggestion.
6. Open the detection detail page to read full recommendations and linked knowledge articles.

The scan detail page also provides the option to open Yield Prediction from that detection context. This auto fills relevant context.

### 5.5 Run Yield Prediction

Path: Yield Prediction

Choose one model mode:

- Linear Regression: uses tabular farm data. Best when you have complete planting details.
- CNN Yield: uses a canopy top down image plus area, date, and growth context. Requires the CNN workflow to be enabled by the admin.
- Ensemble: combines CNN and Linear outputs. Requires both canopy image and complete tabular data.

Steps for planting based prediction (recommended):

1. Select a planting record from the dropdown. This auto fills area, variety, dates, and history.
2. Select the model mode.
3. Upload a canopy image if you selected CNN or Ensemble.
4. Review auto filled fields. Correct any missing values.
5. Add historical production in tons if available.
6. Select Calculate Yield Prediction or Predict Yield.
7. Review predicted yield in tons per hectare, total production in tons, sacks equivalent, confidence, and harvest readiness.

Steps for manual prediction:

Fill variety, field area, ecosystem type, season, planting date, growth duration, health status, and historical data. Upload a canopy image for CNN and Ensemble. Then submit.

Prediction results are saved in the Yield Records list. They do not change harvest totals.

### 5.6 Record Harvests

Path: Harvests

1. Open Harvests.
2. Select Create.
3. Select the planting cycle.
4. Enter actual harvested area, actual production in tons, and harvest date.
5. Save.

The system computes actual yield in tons per hectare and updates planting status to harvested.

Use actual harvest records for proof of production. Do not use predictions as harvest proof.

### 5.7 Keep Season Logs

Path: Season Log

1. Open Season Log.
2. Select Create to start a season journal entry.
3. Add activities such as land preparation, transplanting, fertilizer application, irrigation, pest control, and observations.
4. Edit or delete an activity if you entered wrong details.

Season logs help technicians understand the full history when they review your farm.

### 5.8 View Reports

Path: Reports

1. Select a date range.
2. Apply barangay filter if available for your role.
3. Review summary metrics: total harvest records, total harvest area, total production, and average actual yield.
4. Review breakdowns by rice variety, production by barangay, monthly detection totals, disease frequency, and detection details.
5. Export to CSV or PDF when needed.

Report production metrics come from active harvest records only. Disease frequency excludes healthy, unknown, and Unknown or Not Rice records from ranking, while Detection Details retain active records for traceability.

### 5.9 Use Knowledge Base and Treatments

Path: Knowledge

- Open Knowledge to read pest, disease, and nutrient deficiency articles with symptoms and management notes.
- Open the linked treatment suggestion from a detection detail page for the specific recommended action. Treatment management pages are restricted to Technician and Admin roles.
- Ask a technician if the case is severe or unclear.

## 6. Technician Guide

### 6.1 First Five Tasks for a Technician

1. Open Dashboard and check system wide alerts.
2. Filter Detections by location and date.
3. Review a farmer planting and scan history.
4. Update the Detection record within allowed fields or confirm the linked treatment recommendation.
5. Use Knowledge Base articles as reference for farmer advice.

### 6.2 Review Workflow

1. Open Detections.
2. Filter by barangay, date, disease, or severity.
3. Open Detection Detail.
4. Inspect the leaf image and AI output including confidence and severity.
5. Check planting and field context for planting date, variety, and season.
6. Update the Detection record within allowed fields or confirm the linked treatment recommendation.
7. Inform the farmer about next steps.

### 6.3 Field and Log Review

- Check Fields for correct area and location data.
- Check Plantings for correct variety and cycle status.
- Check Season Logs for missing activities or gaps in care.
- Report data errors to the admin when correction needs elevated access.

### 6.4 Knowledge Base Use

Match symptoms and photos to canonical entries. Link the relevant knowledge entry in your note to the farmer. Keep explanations short and action focused: what to apply, when to recheck, and what warning signs need urgent attention.

## 7. Admin Guide

### 7.1 First Five Tasks for an Admin

1. Review pending registrations and approve or decline.
2. Set detection confidence threshold and allowed past planting days.
3. Publish an important announcement when needed.
4. Review audit logs for recent setting changes.
5. Check knowledge base entries and user records.

### 7.2 Manage Users

Path: Manage Users

- Create users with correct roles.
- Edit user details and role assignment.
- Approve new registrations.
- Activate or deactivate accounts.
- Delete or permanently remove accounts only after checking linked records and organizational policy.

### 7.3 System Settings

Path: System Settings

Controls include:

- Allowed past planting days
- Detection confidence threshold
- Email notifications toggle
- CNN yield workflow toggle
- Ensemble calibration fallback where available

Changes are logged in SiteSettingAudit. You can review the audit list, revert a change, or archive audit entries.

Email delivery notes:

- In app notifications work even when email is disabled.
- Outgoing email is skipped when Email Notifications is disabled.
- Immediate announcement publish sends email when email is enabled and SMTP is configured, plus it creates an in app advisory notification.
- Scheduled announcement publish creates the in app advisory notification when the time becomes due. It does not send email under current policy.
- Due scheduled dispatch runs on normal app traffic. With low traffic, delivery can wait until the next request.

### 7.4 Manage Content

Paths: Knowledge Manage, Treatments, Varieties, Announcements

- Knowledge: create, edit, and archive pest and disease articles.
- Treatments: create and maintain severity based recommendations linked to disease types.
- Varieties: create, edit, delete, and restore rice varieties.
- Announcements: create immediate or scheduled announcements for target users.

For announcements:

- Use Immediate Publish for urgent advisories that need email and in app notification.
- Use Scheduled Publish for future advisories that need in app notification only.

### 7.5 Trash and Archive Management

Path: Trash

- Review soft deleted or archived records.
- Restore records when deletion was incorrect.
- Use permanent delete only when allowed by policy. Permanent actions cannot be undone.

## 8. Disease Detection in Detail

### 8.1 Supported Input

- Clear rice leaf photo from upload or camera capture.
- Active planting context selected in the form.
- Good lighting and focused subject.

### 8.2 How to Read the Result

Each detection shows:

- Disease label, for example Leaf Blast, Neck Blast, Bacterial Leaf Blight, Brown Spot, Narrow Brown Spot, Tungro, or Healthy
- Confidence percentage from the model
- Severity level for treatment intensity
- Treatment suggestion and linked knowledge article
- Model version for traceability

If confidence is below the admin configured threshold, commonly 75 percent, the system shows Unknown or Not Rice. This protects you from false diagnosis. Retake the photo and scan again.

### 8.3 Photo Best Practices

- Use daylight or bright even light. Avoid heavy shadows.
- Focus on one leaf. Fill the frame with the affected area.
- Hold the camera steady. Avoid blur.
- Avoid very dark, very bright, or heavily filtered images.
- Capture the symptom clearly: spots, streaks, blight edges, or blast lesions.
- For yield CNN canopy photos, use a top down view about 0.8 to 0.9 meters above the canopy in morning light.

Poor photos cause low confidence or Unknown results.

### 8.4 Detection History

Path: Detections

- List all detections within your access scope.
- Open detail pages for full results and recommendations.
- Edit notes where allowed.
- Delete or bulk delete only when permitted by your role.
- Export detection lists to CSV or PDF for documentation.

## 9. Yield Prediction in Detail

### 9.1 When to Use Each Mode

Use Linear Regression when:

- You have complete tabular data but no canopy photo.
- You need a fast estimate.

Use CNN Yield when:

- You have a good canopy photo plus area, planting date, and growth duration.
- The admin has enabled the CNN workflow and the model file is available.

Use Ensemble when:

- You have both complete tabular data and a good canopy photo.
- You want a blended result from both models.

### 9.2 How to Read the Result

Each prediction shows:

- Predicted yield in tons per hectare
- Total production estimate in tons (area multiplied by predicted yield)
- Sacks equivalent (50 kg sacks, 20 sacks per ton)
- Confidence percentage from 55 to 95 percent
- Crop maturity stage based on growth progress: Early Stage (0 to 40 days), Vegetative (41 to 65 days), Reproductive (66 to 85 days), Ripening (86 to 100 days), or Harvest Ready (100 plus days)
- Harvest date estimate where available

Higher confidence usually means more complete inputs: known planting record, historical yield data, good canopy photo, and recent health status from detection.

If historical data is missing, confidence may be capped near 70 percent. Add past production when possible.

### 9.3 Yield Records

Path: Yield Records

- List saved predictions.
- Edit or delete records within your access scope.
- Export to CSV or PDF.

Predictions remain available through this workflow. They remain separate from harvest totals to prevent double counting and to prevent estimates from being mistaken for verified production.

### 9.4 Common Yield Errors

- CNN yield model is currently disabled: ask the admin to turn on Enable CNN Yield Model in System Settings.
- Ensemble requires CNN to be enabled: the ensemble needs the CNN prediction as one input, so CNN must be on first.
- Canopy image is required: upload a valid image file for CNN and Ensemble.
- Field area must be greater than 0: enter a valid area with a form minimum of 0.01 hectares.
- Missing required fields: select a planting record, or fill variety, area, dates, and growth days manually.

## 10. Harvest Records in Detail

Path: Harvests

Harvest is the verified source for reports.

- Total Harvest Records: count of active harvest rows in the selected period.
- Total Harvest Area: sum of harvested area in hectares.
- Total Production: sum of actual production in tons.
- Average Actual Yield: average of stored yield in tons per hectare.

Keep harvest entries accurate. Correct errors with Edit. Archive old records instead of permanent delete when possible.

## 11. Reports and Analytics in Detail

Path: Reports

Report sections:

- Harvest summary metrics
- Actual yield by rice variety
- Rice production by barangay
- Monthly detection breakdown
- Disease frequency ranking
- Full detection details
- Export to CSV and PDF

Filters:

- Date range
- Barangay filter where permitted
- Role scope applied automatically

Model metadata such as model version, model accuracy, detectable classes, and last scan appears in Dashboard System Information, not in the harvest summary.

## 12. Notifications and Announcements

### 12.1 Notifications

Path: Notifications

Notifications cover disease alerts, yield updates, system changes, and account activity.

- Open Notifications to read new alerts.
- Use Mark as Read for one item.
- Use Mark All as Read to clear the list.

### 12.2 Announcements

Path: Announcements

- Read announcements targeted to your role.
- Open Announcement Detail for full text.
- Use Mark as Read to track what you have seen.

Admins and authorized technicians create announcements. Farmers receive and read them.

## 13. Profile, Password, and Account Safety

Path: Profile

- Review account details.
- Update contact details where allowed.
- Change password from the Change Password page.
- Use a strong password and do not share it.
- Log out on shared devices.

If your account is inactive or pending approval, contact your admin or technician coordinator.

## 14. Troubleshooting

### 14.1 Cannot Log In

1. Confirm username and password are correct.
2. Confirm Caps Lock is off.
3. Confirm the account is active and approved.
4. Reset password if the option is available, or ask the admin.

### 14.2 Page Not Visible

1. Confirm you are logged in with the correct account.
2. Confirm your role has access to that page.
3. Farmer accounts see personal scope only.
4. Ask the admin to check role assignment if the page should be visible.

### 14.3 Scan Fails or Shows Unknown

1. Confirm an active planting is selected.
2. Retake the photo with better light and focus.
3. Confirm the image is a rice leaf, not soil, hand, or other background.
4. Confirm the confidence threshold in System Settings if you are an admin.
5. Try again with a clearer photo.

### 14.4 Camera Does Not Work

1. Allow camera permission in the browser.
2. Refresh the page.
3. Try the upload option instead of live capture.
4. Try another supported browser such as current Chrome, Edge, Firefox, or Safari.
5. Check that the device camera works in other apps.

### 14.5 Yield Tool Shows Disabled or Missing Options

1. Confirm planting details are complete.
2. Confirm canopy image is uploaded for CNN and Ensemble.
3. Confirm area is greater than zero.
4. Ask the admin to check Enable CNN Yield Model and model file availability.
5. Check that required runtime dependencies are installed if you manage the server.

### 14.6 Reports Show No Data

1. Confirm the date range includes harvest records.
2. Confirm barangay filter matches the records.
3. Confirm records are active and not archived.
4. Confirm you are viewing harvest based metrics, not predictions. Predictions do not appear in harvest totals.

### 14.7 Email Not Received

1. Confirm Email Notifications is enabled in System Settings.
2. Confirm SMTP is configured on the server.
3. Remember that scheduled announcements create in app notifications only under current policy.
4. Check in app Notifications and Announcements pages even when email is missing.
5. Ask the admin to check server logs for delivery failures.

## 15. Frequently Asked Questions

**Which section should I read first**
Check your role at the top of the Help page. Read the Farmer, Technician, or Admin guide that matches your account.

**How do I read AI confidence**
The result includes a label and a percentage. High confidence means the model found a clear pattern. Low confidence means the photo or data was unclear. Below threshold results show as Unknown or Not Rice.

**Why is scan confidence low**
The most common reasons are blurry photos, dark photos, overexposed photos, or photos that are not rice leaves. Take a clearer photo in good light.

**Can I use predictions as harvest proof**
No. Use Harvest records for verified production. Predictions are planning estimates only.

**What is the difference between Linear, CNN, and Ensemble**
Linear uses farm table data. CNN uses canopy image plus field context. Ensemble blends both outputs with weights based on model error. Lower error gets higher weight.

**What should I send when asking for support**
Send the page name, your role, the exact error message, and what you already tried. This speeds up support.

## 16. Support

For severe infections or unclear treatment advice, consult your local DA field technician for professional guidance.

When contacting support, include:

- Page opened
- Role account used
- Exact error message
- Steps you already tried

For support, use the Contact DA Support button inside the Help page. It opens a prefilled support request. Include page opened, role used, exact error, and steps already tried.

## 17. Responsible Use Notes

- Act early on severe detections. Do not wait for spread.
- Follow label directions for any chemical treatment and local extension advice.
- Keep field, planting, and harvest dates accurate. Poor inputs reduce prediction quality.
- Keep photos clear. The AI result depends on input quality.
- Protect account credentials. Report unauthorized access to your admin promptly.

## 18. Quick Reference Paths

Use the navigation bar first. Use these paths when a link fails, when bookmarking, or when reporting an issue to support. Append each path to the server address, for example https://your-domain.com/login/.

If a path returns permission denied, it usually means the page is outside your role. Farmers see personal scope only.

### Available to all logged in roles with role based scope

- Login: /login/
- Register: /register/
- Dashboard: /dashboard/
- Help: /help/
- Scan: /scan/
- Camera: /camera/
- Detections: /detections/
- Yield Prediction: /yield-prediction/
- Yield Records: /yield-records/
- Fields: /fields/
- Plantings: /plantings/
- Harvests: /harvests/
- Season Log: /season-log/
- Reports: /reports/
- Knowledge: /knowledge/
- Varieties: /varieties/ (view for all roles, manage for Technician and Admin)
- Notifications: /notifications/
- Announcements: /announcements/
- Profile: /profile/
- Change Password: /change-password/

### Restricted by role

- Treatments: /treatments/ (Technician and Admin)
- Trash and Archive: /trash/ (Technician and Admin)
- Manage Users: /manage-users/ (Admin)
- System Settings: /system-settings/ (Admin)
