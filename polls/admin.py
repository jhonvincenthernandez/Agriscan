"""
Django Admin Configuration for AgriScan+

IMPORTANT: Treatment Management Permissions
- Admin role: Full acc		("Disease Information", {
			"fields": ("symptoms", "factors_favoring", "factor_actions", "factor_expected_results"),
			"description": (
				"<strong>Factor Actions</strong>: one action per line, same order as Factors. "
				"<strong>Expected Results</strong>: one result per line, same order as Factors."
			),
			"classes": ("collapse",)
		}), add, edit, delete)
- Technician role: Can view, add, edit (but NOT delete)
- Farmer role: No access to admin panel

This is BEST PRACTICE because:
1. DA Technicians know local conditions and can customize treatments
2. Allows quick updates based on field observations
3. Regional adaptation of recommendations
4. Responsive to new research and products
"""

from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "role", "location", "farm_size_ha", "created_at")
	search_fields = ("user__username", "location")
	list_filter = ("role",)


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
	list_display = ("name", "owner", "barangay", "area_hectares")
	list_filter = ("barangay",)
	search_fields = ("name", "owner__user__username")


@admin.register(models.RiceVariety)
class RiceVarietyAdmin(admin.ModelAdmin):
	list_display = ("code", "name", "average_growth_days")
	search_fields = ("code", "name")


@admin.register(models.DiseaseType)
class DiseaseTypeAdmin(admin.ModelAdmin):
	list_display = ("name", "is_active", "primary_knowledge", "description_preview")
	list_filter = ("is_active",)
	search_fields = ("name", "description")
	list_editable = ("is_active",)
	
	def description_preview(self, obj):
		return obj.description[:60] + "..." if len(obj.description) > 60 else obj.description or "—"
	description_preview.short_description = "Description"
	
	def has_module_permission(self, request):
		"""Allow Admin and Technician to access disease type management"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_view_permission(self, request, obj=None):
		"""Admin and Technician can view disease types"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_change_permission(self, request, obj=None):
		"""Admin and Technician can edit disease types"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_add_permission(self, request):
		"""Admin and Technician can add new disease types"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_delete_permission(self, request, obj=None):
		"""Only Admin can delete disease types"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role == 'admin'
		except:
			return False


@admin.register(models.TreatmentRecommendation)
class TreatmentAdmin(admin.ModelAdmin):
	list_display = ("disease", "severity_range", "priority", "short_text_preview", "is_active", "updated_by")
	list_filter = ("disease", "is_active")
	search_fields = ("short_text", "detailed_text", "disease__name")
	list_editable = ("is_active",)
	ordering = ("disease", "priority", "severity_min")
	
	fieldsets = (
		("Basic Information", {
			"fields": ("disease", "priority", "is_active", ("severity_min", "severity_max"))
		}),
		("Treatment Text", {
			"fields": ("short_text", "detailed_text")
		}),
		("Disease Information", {
			"fields": ("knowledge_entries", "factors_favoring", "factor_actions"),
			"description": (
				"<strong>Knowledge Entries</strong>: Link to canonical KnowledgeBase entries for symptoms/causes/prevention. "
				"Treatment recommendations no longer duplicate these sections."
			),
			"classes": ("collapse",)
		}),
		("Management Strategies", {
			"fields": ("cultural_practices", "chemical_control"),
			"classes": ("collapse",)
		}),
		("Severity Escalation", {
			"fields": ("severity_threshold", "severity_high_msg"),
			"description": (
				"<strong>Severity Threshold</strong>: When detection severity ≥ this value, "
				"the Escalation Message is appended to the Quick Recommendation card. "
				"Set based on IPM principles (e.g. 40 for Neck Blast, 70 for Leaf Scald). "
				"<br><strong>Escalation Message</strong>: IPM-curated text explaining what to do "
				"when cultural control alone is insufficient. Leave blank to hide the severity line."
			),
			"classes": ("collapse",)
		}),
	)
	
	def severity_range(self, obj):
		return f"{obj.severity_min}-{obj.severity_max}%"
	severity_range.short_description = "Severity Range"
	
	def short_text_preview(self, obj):
		return obj.short_text[:60] + "..." if len(obj.short_text) > 60 else obj.short_text
	short_text_preview.short_description = "Treatment Summary"
	
	def updated_by(self, obj):
		"""Show last update timestamp"""
		return obj.updated_at.strftime("%Y-%m-%d %H:%M") if obj.updated_at else "—"
	updated_by.short_description = "Last Updated"
	
	def has_module_permission(self, request):
		"""Allow Admin and Technician roles to access treatment management"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_view_permission(self, request, obj=None):
		"""Admin and Technician can view treatments"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_change_permission(self, request, obj=None):
		"""Admin and Technician can edit treatments"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_add_permission(self, request):
		"""Admin and Technician can add new treatments"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role in ('admin', 'technician')
		except:
			return False
	
	def has_delete_permission(self, request, obj=None):
		"""Only Admin can delete treatments (Technicians can only deactivate)"""
		if request.user.is_superuser:
			return True
		try:
			profile = request.user.profile
			return profile.role == 'admin'  # Only admin, not technician
		except:
			return False
	
	def save_model(self, request, obj, form, change):
		"""Track who made changes (optional enhancement for future)"""
		super().save_model(request, obj, form, change)


@admin.register(models.ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
	list_display = ("version", "accuracy", "is_active", "created_at")
	list_filter = ("is_active",)


@admin.register(models.DetectionRecord)
class DetectionAdmin(admin.ModelAdmin):
	list_display = ("created_at", "field", "disease", "confidence_pct", "severity_pct", "source")
	list_filter = ("disease", "source", "created_at")
	search_fields = ("field__name",)


@admin.register(models.PlantingRecord)
class PlantingAdmin(admin.ModelAdmin):
	list_display = ("field", "variety", "planting_date", "expected_harvest_date")
	list_filter = ("variety",)


@admin.register(models.YieldPrediction)
class YieldAdmin(admin.ModelAdmin):
	list_display = ("planting", "predicted_sacks_per_ha", "confidence_pct", "created_at")
	list_filter = ("created_at",)


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ("recipient", "type", "title", "is_read", "created_at")
	list_filter = ("type", "is_read")
	search_fields = ("title", "recipient__user__username")


class UserNotificationInline(admin.TabularInline):
	"""Show read statistics inline on Announcement admin"""
	model = models.UserNotification
	extra = 0
	readonly_fields = ("user", "is_read", "read_at")
	can_delete = False
	
	def has_add_permission(self, request, obj):
		return False  # Only show existing read records


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
	list_display = (
		"title", 
		"priority_icon", 
		"target_audience", 
		"category",
		"is_active", 
		"published_at",
		"read_count"
	)
	list_filter = ("priority", "target_audience", "category", "is_active", "created_at")
	search_fields = ("title", "content", "target_barangay")
	readonly_fields = ("created_at", "updated_at", "created_by", "read_stats")
	date_hierarchy = "published_at"
	inlines = [UserNotificationInline]
	
	fieldsets = (
		("Content", {
			"fields": ("title", "content", "category")
		}),
		("Targeting", {
			"fields": ("target_audience", "target_barangay", "target_user")
		}),
		("Priority & Status", {
			"fields": ("priority", "is_active")
		}),
		("Scheduling", {
			"fields": ("published_at", "expires_at"),
			"description": "Leave published_at empty to publish immediately. Set expires_at to auto-hide announcement after date."
		}),
		("Email (Future Use)", {
			"fields": ("send_email", "email_sent"),
			"classes": ("collapse",),
			"description": "⚠️ Email integration is prepared but commented out. See ANNOUNCEMENT_SYSTEM_IMPLEMENTATION.md to activate."
		}),
		("Metadata", {
			"fields": ("created_by", "created_at", "updated_at", "read_stats"),
			"classes": ("collapse",)
		})
	)
	
	def save_model(self, request, obj, form, change):
		"""Auto-set created_by to current admin user"""
		if not change:  # Only on creation
			obj.created_by = request.user.profile
		super().save_model(request, obj, form, change)
	
	def priority_icon(self, obj):
		"""Show emoji icon for priority"""
		icons = {
			"info": "📘",
			"advisory": "📗", 
			"warning": "📙",
			"urgent": "📕"
		}
		return f"{icons.get(obj.priority, '')} {obj.get_priority_display()}"
	priority_icon.short_description = "Priority"
	
	def read_count(self, obj):
		"""Show read statistics"""
		total = obj.usernotification_set.count()
		read = obj.usernotification_set.filter(is_read=True).count()
		if total == 0:
			return "Not delivered yet"
		return f"{read}/{total} read ({int(read/total*100)}%)"
	read_count.short_description = "Read Status"
	
	def read_stats(self, obj):
		"""Detailed read statistics for detail view"""
		if not obj.pk:
			return "Save to see statistics"
		
		total = obj.usernotification_set.count()
		read = obj.usernotification_set.filter(is_read=True).count()
		unread = total - read
		
		return f"📊 Total Recipients: {total} | ✅ Read: {read} | ⏳ Unread: {unread}"
	read_stats.short_description = "Read Statistics"


@admin.register(models.UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
	list_display = ("user", "announcement_title", "is_read", "read_at", "created_at")
	list_filter = ("is_read", "created_at")
	search_fields = ("user__user__username", "announcement__title")
	readonly_fields = ("user", "announcement", "is_read", "read_at", "created_at")
	
	def announcement_title(self, obj):
		return obj.announcement.title
	announcement_title.short_description = "Announcement"
	
	def has_add_permission(self, request):
		return False  # Auto-created by system
	
	def has_delete_permission(self, request, obj=None):
		return False  # Don't allow deletion


@admin.register(models.SeasonLog)
class SeasonLogAdmin(admin.ModelAdmin):
	list_display = ("farmer", "field", "season_label", "current_stage",
	                "actual_yield_sacks", "gross_income", "created_at")
	list_filter  = ("season_year", "season_type", "current_stage")
	search_fields = ("farmer__user__username", "field__name", "field__barangay",
	                 "variety__code")
	readonly_fields = ("gross_income", "net_income", "actual_yield_tons")

	def season_label(self, obj):
		return obj.season_label
	season_label.short_description = "Season"


@admin.register(models.FarmActivity)
class FarmActivityAdmin(admin.ModelAdmin):
	list_display = ("season_log", "activity_date", "activity_type", "title",
	                "problem_severity", "total_cost")
	list_filter  = ("activity_type", "problem_severity", "activity_date")
	search_fields = ("title", "description", "problem_observed",
	                 "season_log__field__name", "season_log__farmer__user__username")


@admin.register(models.SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
	"""
	Simple admin interface para sa global system settings.

	Tagalog:
	- Dito ise-set ng admin kung ilang araw pabalik ang pinapayagang
	  `planting_date` sa buong system.
	- Normally, isang row lang ang kailangan. Kapag may existing na,
	  hindi na papayagang mag-add pa ng panibago sa admin UI.
	"""

	list_display = ("allowed_past_days_planting",)

	def has_add_permission(self, request):
		"""
		Limitahan sa isang SiteSetting record lang.

		Tagalog:
		- Kung may existing na setting, hindi na kailangan ng second copy,
		  kaya binablock natin ang "Add" button sa admin.
		"""
		if models.SiteSetting.objects.exists():
			return False
		return super().has_add_permission(request)
