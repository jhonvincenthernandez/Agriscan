from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    # ============================================================================
    # AUTHENTICATION & USER MANAGEMENT
    # ============================================================================
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # ============================================================================
    # DASHBOARD & REPORTS
    # ============================================================================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    
    # ============================================================================
    # CORE FEATURES - DISEASE DETECTION
    # ============================================================================
    path('scan/', views.scan, name='scan'),
    path('camera/', views.camera_capture, name='camera_capture'),
    path('detections/', views.detections_list, name='detections_list'),
    path('detections/bulk-delete/', views.detections_bulk_delete, name='detections_bulk_delete'),
    path('detections/<int:pk>/', views.detections_detail, name='detections_detail'),
    path('detections/<int:pk>/edit/', views.detections_edit, name='detections_edit'),
    path('detections/<int:pk>/delete/', views.detections_delete, name='detections_delete'),
    
    # ============================================================================
    # CORE FEATURES - YIELD PREDICTION
    # ============================================================================
    path('yield-prediction/', views.yield_prediction, name='yield_prediction'),
    path('yield-records/', views.yield_records_list, name='yield_records_list'),
    path('yield-records/bulk-delete/', views.yield_records_bulk_delete, name='yield_records_bulk_delete'),
    path('yield-records/<int:pk>/edit/', views.yield_record_edit, name='yield_record_edit'),
    path('yield-records/<int:pk>/delete/', views.yield_record_delete, name='yield_record_delete'),
    
    # ============================================================================
    # EXPORT FUNCTIONALITY
    # ============================================================================
    path('detections/export/csv/', views.export_detections_csv, name='export_detections_csv'),
    path('detections/export/pdf/', views.export_detections_pdf, name='export_detections_pdf'),
    path('yield-records/export/csv/', views.export_yields_csv, name='export_yields_csv'),
    path('yield-records/export/pdf/', views.export_yields_pdf, name='export_yields_pdf'),
    
    # ============================================================================
    # FIELD MANAGEMENT
    # ============================================================================
    path('fields/', views.fields_list, name='fields_list'),
    path('fields/create/', views.field_create, name='field_create'),
    path('fields/<int:pk>/edit/', views.field_edit, name='field_edit'),
    path('fields/<int:pk>/delete/', views.field_delete, name='field_delete'),
    
    # ============================================================================
    # PLANTING RECORD MANAGEMENT
    # ============================================================================
    path('plantings/', views.plantings_list, name='plantings_list'),
    path('plantings/create/', views.planting_create, name='planting_create'),
    path('plantings/<int:pk>/edit/', views.planting_edit, name='planting_edit'),
    path('plantings/<int:pk>/delete/', views.planting_delete, name='planting_delete'),

    # ============================================================================
    # HARVEST RECORD MANAGEMENT
    # ============================================================================
    path('harvests/', views.harvests_list, name='harvests_list'),
    path('harvests/create/', views.harvest_create, name='harvest_create'),
    path('harvests/<int:pk>/edit/', views.harvest_edit, name='harvest_edit'),
    path('harvests/<int:pk>/archive/', views.harvest_archive, name='harvest_archive'),
    path('harvests/<int:pk>/delete/', views.harvest_hard_delete, name='harvest_hard_delete'),

    # ============================================================================
    # ADMIN - USER MANAGEMENT
    # ============================================================================
    path('manage-users/', views.admin_users_list, name='admin_users_list'),
    path('manage-users/create/', views.admin_user_create, name='admin_user_create'),
    path('manage-users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('manage-users/<int:pk>/toggle-active/', views.admin_user_toggle_active, name='admin_user_toggle_active'),
    path('manage-users/<int:pk>/approve/', views.admin_user_approve, name='admin_user_approve'),
    path('manage-users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('system-settings/audit/', views.system_settings_audit_list, name='system_settings_audit_list'),
    path('system-settings/audit/<int:pk>/revert/', views.system_settings_audit_revert, name='system_settings_audit_revert'),
    path('system-settings/audit/<int:pk>/archive/', views.system_settings_audit_archive, name='system_settings_audit_archive'),
    path('system-settings/audit/bulk-archive/', views.system_settings_audit_bulk_archive, name='system_settings_audit_bulk_archive'),

    # Knowledge Base (Pests/Diseases/Nutrient Deficiencies)
    path('knowledge/', views.knowledge_list, name='knowledge_list'),
    path('knowledge/<int:pk>/', views.knowledge_detail, name='knowledge_detail'),
    path('knowledge/manage/', views.knowledge_admin_list, name='knowledge_admin_list'),
    path('knowledge/manage/create/', views.knowledge_create, name='knowledge_create'),
    path('knowledge/manage/<int:pk>/edit/', views.knowledge_edit, name='knowledge_edit'),
    path('knowledge/manage/<int:pk>/archive/', views.knowledge_archive, name='knowledge_archive'),
    path('knowledge/<int:pk>/export/pdf/', views.knowledge_export_pdf, name='knowledge_export_pdf'),
    path('knowledge/<int:pk>/export/csv/', views.knowledge_export_csv, name='knowledge_export_csv'),

    # ============================================================================
    # ADMIN/TECHNICIAN - TREATMENT MANAGEMENT
    # ============================================================================
    path('treatments/', views.treatments_list, name='treatments_list'),
    path('treatments/create/', views.treatments_create, name='treatments_create'),
    path('treatments/<int:pk>/edit/', views.treatments_edit, name='treatments_edit'),
    path('treatments/<int:pk>/delete/', views.treatments_delete, name='treatments_delete'),
    
    # ============================================================================
    # ANNOUNCEMENT SYSTEM
    # ============================================================================
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/create/', views.announcement_create, name='announcement_create'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement_edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement_delete'),
    path('announcements/<int:pk>/mark-read/', views.announcement_mark_read, name='announcement_mark_read'),
    
    # ============================================================================
    # SYSTEM NOTIFICATIONS (Disease / Yield Drop / Announcement Alerts)
    # ============================================================================
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/mark-all-read/', views.notification_mark_all_read, name='notification_mark_all_read'),
    path('notifications/<int:pk>/mark-read/', views.notification_mark_read, name='notification_mark_read'),
    
    # ============================================================================
    # RICE VARIETY MANAGEMENT
    # ============================================================================
    path('varieties/', views.varieties_list, name='varieties_list'),
    path('varieties/create/', views.variety_create, name='variety_create'),
    path('varieties/<int:pk>/edit/', views.variety_edit, name='variety_edit'),
    path('varieties/<int:pk>/delete/', views.variety_delete, name='variety_delete'),
    path('varieties/<int:pk>/restore/', views.variety_restore, name='variety_restore'),

    # ============================================================================
    # TRASH / ARCHIVE MANAGEMENT
    # ============================================================================
    path('trash/', views.trash_management, name='trash_management'),

    # ============================================================================
    # API ENDPOINTS
    # ============================================================================
    path('api/planting/<int:pk>/', views.api_planting_data, name='api_planting_data'),

    # ============================================================================
    # SEASON FARM LOG — Farmer activity journal & history
    # static paths first, then parameterised
    # ============================================================================
    path('season-log/', views.season_log_list, name='season_log_list'),
    path('season-log/create/', views.season_log_create, name='season_log_create'),
    path('season-log/barangay-stats/', views.season_log_barangay_stats, name='season_log_barangay_stats'),
    path('season-log/activity/<int:pk>/edit/', views.activity_edit, name='activity_edit'),
    path('season-log/activity/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    path('season-log/<int:pk>/', views.season_log_detail, name='season_log_detail'),
    path('season-log/<int:pk>/edit/', views.season_log_edit, name='season_log_edit'),
    path('season-log/<int:pk>/delete/', views.season_log_delete, name='season_log_delete'),
    path('season-log/<int:season_pk>/activity/add/', views.activity_create, name='activity_create'),
]