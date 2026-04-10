# AgriScan+ System Documentation

> System Name: AgriScan+
>
> Version: 1.6.0
>
> Scope: Django web platform for rice disease detection, yield prediction, and farm operations management.

---

## 1. Executive Summary

AgriScan+ is a web-based agricultural decision support system built for rice production workflows. It combines:

- AI-assisted disease detection from leaf images
- Yield prediction using planting and field context
- Field, planting, harvest, and seasonal activity management
- Role-based operations for administrators, technicians, and farmers
- Notifications, announcements, and reporting support

The system is designed for practical deployment in local government or extension settings while retaining structured records suitable for research and model improvement.

---

## 2. Objectives of the Study

The purpose of this study is to develop AgriScan+, a CNN-powered, mobile-responsive web decision-support system for early rice leaf disease detection and yield prediction for the Department of Agriculture - San Teodoro.

### Specific objectives

Specifically, this study aims to:

1. Design and implement mobile-responsive workflows that allow farmers and agricultural staff to capture or upload rice leaf images using smartphone and desktop browsers for disease screening.
2. Implement and integrate a Convolutional Neural Network (CNN)-based disease detection pipeline that classifies common rice leaf diseases with usable confidence outputs.
3. Develop and integrate a yield prediction and analytics module with support for both Linear Regression and CNN models, combining detection outcomes, planting context, and historical farm records for decision support.
4. Build a centralized database for user, field, planting, detection, prediction, harvest, and notification records to ensure traceability and longitudinal analysis.
5. Evaluate the system using technical and user-centered criteria, including model performance, usability, reliability, operational efficiency, and mobile usability through user testing and expert validation.

### Scope alignment note

- The current implementation follows an intentional web-first, mobile-responsive deployment strategy to maximize accessibility, faster rollout, lower maintenance cost, and cross-device compatibility, while fully operationalizing role-based modules for Admin, Technician, and Farmer users with end-to-end support for disease detection, hybrid-model yield prediction, and crop-cycle record management.

---

## 3. Users and Access Model

AgriScan+ uses three role classes defined in profile records:

- Admin (Administrator or DA Officer): full access, system settings, user and content administration.
- Technician (Field Technician): cross-farmer operational support, scans, records, and advisories.
- Farmer: own farm records, detections, predictions, and personal reporting views.

### Permission intent

| Action | Admin | Technician | Farmer |
|---|---|---|---|
| Manage users and system settings | Yes | Limited | No |
| Manage farmer operational records | Yes | Yes | Own only |
| Run disease scans and predictions | Yes | Yes | Yes |
| View analytics and exports | Yes | Yes | Personal scope |

---

## 4. High-Level Architecture

### Application layers

1. Presentation layer
   - Django templates and JavaScript-based UX.
2. Business layer
   - Django views, forms, services, decorators, and model-level validation.
3. AI inference layer
   - TensorFlow or TFLite model artifacts for disease and yield logic.
4. Data layer
   - Relational database via Django ORM and media storage for uploaded files.

### Runtime flow

Client request -> Django routing and auth -> business validation -> DB read or write -> optional model inference -> persisted result -> rendered response.

---

## 5. Technology Stack

### Core

- Python 3.8+
- Django 5.x
- MySQL via mysqlclient
- TensorFlow and TensorFlow Lite artifacts

### Data and ML utilities

- numpy
- pandas
- scikit-learn
- pillow
- opencv-python

### Reporting and tools

- reportlab
- matplotlib
- seaborn
- jupyter

---

## 6. Functional Modules

### 6.1 Authentication and Profiles

Responsibilities:

- Login and session management
- Role assignment through profile records
- User-specific data scoping and access checks

Key model entities:

- Profile

### 6.2 System Configuration and Audit

Responsibilities:

- Global settings such as allowed past planting days
- Detection confidence threshold
- Business toggles managed in admin UI
   - enable or disable outgoing email notifications
   - enable or disable user-facing CNN yield mode
- Change logging for auditability

Key model entities:

- SiteSetting
- SiteSettingAudit

### 6.3 Field and Variety Management

Responsibilities:

- Field registration with area and location context
- Rice variety catalog with agronomic and resistance metadata
- Soft-delete archival while preserving historical integrity

Key model entities:

- Field
- RiceVariety

### 6.4 Planting and Seasonal Operations

Responsibilities:

- Planting cycle tracking
- Crop stage and season journaling
- Agronomic activity history per cycle

Key model entities:

- PlantingRecord
- SeasonLog

### 6.5 Disease Detection and Recommendation

Responsibilities:

- Image-based disease classification tracking
- Confidence and severity storage
- Treatment and knowledge linkage
- Model version traceability

Key model entities:

- DiseaseType
- DetectionRecord
- TreatmentRecommendation
- KnowledgeBaseEntry
- ModelVersion

### 6.6 Yield and Harvest Management

Responsibilities:

- Predicted yield storage in tons per hectare
- Total production estimation
- Actual harvest capture and synchronization
- Dual-model inference routing
   - Linear Regression path for tabular agronomic inputs
   - CNN path for canopy image-based prediction

Key model entities:

- YieldPrediction
- HarvestRecord

### 6.7 Notification and Announcements

Responsibilities:

- In-app alerting for key events
- Broadcast or targeted advisories
- Read-state tracking per user

Key model entities:

- Notification
- Announcement
- UserNotification

---

## 7. Data Model Overview

### Core relationship map

- User -> Profile (one-to-one)
- Profile -> Field (one-to-many)
- Field -> PlantingRecord (one-to-many)
- PlantingRecord -> DetectionRecord (one-to-many)
- PlantingRecord -> YieldPrediction (one-to-many)
- PlantingRecord -> HarvestRecord (one-to-one)
- DiseaseType -> TreatmentRecommendation (one-to-many)
- DiseaseType -> DetectionRecord (one-to-many)
- Announcement -> UserNotification (one-to-many)

### Data integrity patterns

- Widespread soft-delete behavior through is_active or archive flags.
- Validation guards at model level for area and date constraints.
- Derived values auto-computed on save (example: total production, yield conversions).

---

## 8. Main System Workflows

### Workflow A: Disease Detection

1. User selects or confirms planting context.
2. User uploads or captures leaf image.
3. Backend performs inference and maps disease class.
4. Detection record is stored with confidence and severity.
5. Treatment and knowledge recommendations are presented.

### Workflow B: Yield Prediction

1. User opens prediction flow from planting or detection context.
2. User selects model mode (Linear Regression or CNN Yield).
3. System reads field and planting metadata.
4. Model-specific validation is applied.
   - CNN requires canopy image and quality checks.
   - Linear Regression validates tabular core fields.
5. Selected model returns predicted tons per hectare.
6. System computes total production estimate.
7. Prediction is saved for historical reporting.

### Workflow C: Harvest Finalization

1. User records actual harvest output.
2. System computes actual tons per hectare.
3. Planting status is synchronized to harvested.
4. Historical datasets become available for analytics and retraining.

---

## 9. Security and Governance

### Authentication and authorization

- Django authentication and session controls.
- Role-based restrictions through profile role checks and decorators.

### Data protection

- Validate uploads by type and size.
- Keep secrets in environment variables.
- Enforce HTTPS and secure host configuration in production.

### Settings governance pattern

- Admin business toggles are DB-backed via `SiteSetting`.
   - `email_enabled`
   - `yield_cnn_enabled`
- Environment toggles are fallback-only when `SiteSetting` is unavailable.
   - `EMAIL_ENABLED`
   - `YIELD_CNN_ENABLED`
- SMTP credentials and model runtime values remain environment-managed.

### Audit and traceability

- Settings audit logs available via SiteSettingAudit.
- Model version linkage for detection records supports reproducibility.

---

## 10. Deployment and Operations Notes

### Baseline setup

1. Create and activate virtual environment.
2. Install dependencies from requirements.txt.
3. Apply migrations.
4. Create superuser.
5. Run server and validate module access by role.

### Suggested production improvements

- Add asynchronous workers for heavy inference.
- Move media files to object storage with backups.
- Add scheduled jobs for reporting and maintenance tasks.
- Implement centralized logging and monitoring.

---

## 11. Testing Strategy

Minimum recommended test coverage:

- Role access checks for all major views.
- Model validations for planting dates and area boundaries.
- End-to-end detection save path with treatment retrieval.
- Yield prediction save and unit conversion consistency.
- Harvest synchronization effects on planting status.

---

## 12. Known Constraints

- AI output quality depends on model quality and input image quality.
- Offline-first sync strategy exists at record level but can be expanded.
- Some advanced integrations (email automation, richer API layer) are staged for future hardening.

---

## 13. Roadmap

- Expose stable API endpoints for mobile clients.
- Add model performance dashboard and drift monitoring.
- Integrate weather and geospatial signals for better forecasting.
- Formalize retraining pipeline with validated harvest labels.

---

## 14. Conclusion

AgriScan+ provides a complete digital workflow for rice disease and yield decision support. Its current implementation already combines practical field operations with structured, research-grade data capture. The architecture is modular and suitable for phased scaling in local agricultural programs.

---

Document owner: AgriScan+ Development Team  
Last updated: 2026-04-01
