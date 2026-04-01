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

## 2. Objectives

### Primary objectives

- Detect likely rice diseases quickly from uploaded images.
- Estimate expected yield per hectare and total projected production.
- Maintain complete crop-cycle records from planting to harvest.

### Secondary objectives

- Provide traceable historical data for analytics and policy decisions.
- Support extension staff workflows across multiple farmers and fields.
- Build a clean data foundation for future model retraining.

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
2. System reads field and planting metadata.
3. Model returns predicted tons per hectare.
4. System computes total production estimate.
5. Prediction is saved for historical reporting.

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
