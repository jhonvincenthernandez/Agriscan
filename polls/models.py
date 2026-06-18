"""Core data models for AgriScan+ application.

These models implement the functional requirements you listed:

MAJOR FEATURES MAPPING:
 - Crop Health Detection (CNN-based): DiseaseType, TreatmentRecommendation, DetectionRecord, ModelVersion
 - Yield Prediction: RiceVariety, PlantingRecord, YieldPrediction (stores predicted sacks/ha)
 - DA Web Dashboard: Aggregations will query DetectionRecord, YieldPrediction, Field, Barangay
 - Mobile App Offline Capture: DetectionRecord.has_synced flag & source field; PlantingRecord.has_synced
 - Notifications: Notification (disease / yield_drop / announcement bell alerts)
 - Reports & Analytics: Historical data in DetectionRecord & YieldPrediction

Functional roles handled via Profile.role (admin, technician, farmer). For more granular permissions you can later use Django Groups.
"""

from decimal import Decimal

from django.db import models
from django.db.models.deletion import ProtectedError
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError


class SoftDeleteQuerySet(models.QuerySet):
    """Custom queryset for soft delete handling."""
    def delete(self):
        # Soft-delete behavior: mark is_active false and set deleted_at.
        return self.update(is_active=False, deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def active(self):
        return self.filter(is_active=True)

    def archived(self):
        return self.filter(is_active=False)


class SoftDeleteManager(models.Manager):
    """Manager that excludes archived records by default."""
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_active=True)

    def all_objects(self):
        return SoftDeleteQuerySet(self.model, using=self._db)

    def archived(self):
        return self.all_objects().filter(is_active=False)


class SoftDeleteModel(models.Model):
    """Abstract mixin for soft-delete fields and methods."""
    deleted_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when record was archived")

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False, hard=False):
        if hard:
            return super().delete(using=using, keep_parents=keep_parents)

        self.is_active = False
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_active', 'deleted_at'])

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        self.is_active = True
        self.deleted_at = None
        self.save(update_fields=['is_active', 'deleted_at'])

User = get_user_model()


class SiteSetting(models.Model):
    """Global/system-wide configuration for AgriScan+.

    Tagalog summary:
    - Dito puwedeng i-configure ng admin ang ilang araw pabalik
      na puwedeng i-encode na `planting_date` sa buong system.
    """

    allowed_past_days_planting = models.PositiveIntegerField(
        default=30,
        help_text=(
            "Ilang araw pabalik ang pinapayagan para sa planting date. "
            "Halimbawa, kung 30: puwedeng mag-encode hanggang 30 araw na nakalipas. "
            "0 = ngayong araw lang ang puwedeng i-save."
        ),
    )

    detection_confidence_threshold = models.PositiveSmallIntegerField(
        default=75,
        help_text=(
            "Minimum confidence percentage required for the AI model to accept "
            "a detection as valid. Lower values make the model less strict; "
            "higher values make it more likely to return 'Unknown/Not Rice'."
        ),
    )

    yield_cnn_enabled = models.BooleanField(
        default=False,
        help_text=(
            "Enable or disable CNN yield prediction in the user-facing Yield Tool. "
            "When disabled, only Linear Regression is selectable."
        ),
    )

    email_enabled = models.BooleanField(
        default=False,
        help_text=(
            "Enable or disable outgoing email notifications globally. "
            "SMTP credentials are still read from environment variables."
        ),
    )

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self) -> str:
        return (
            "Global Settings (allowed past days: {allowed}, confidence threshold: {threshold}, cnn: {cnn}, email: {email})"
        ).format(
            allowed=self.allowed_past_days_planting,
            threshold=self.detection_confidence_threshold,
            cnn="enabled" if self.yield_cnn_enabled else "disabled",
            email="enabled" if self.email_enabled else "disabled",
        )

    def clean(self):
        """Basic validation para maiwasan ang sobrang laking value."""

        if self.allowed_past_days_planting > 365 * 5:  # max 5 years pabalik
            raise ValidationError(
                {
                    "allowed_past_days_planting": (
                        "Maximum na 1825 araw (5 taon) lang ang pinapayagan "
                        "para sa setting na ito."
                    )
                }
            )

        if self.detection_confidence_threshold is not None:
            if not (0 <= self.detection_confidence_threshold <= 100):
                raise ValidationError(
                    {
                        "detection_confidence_threshold": (
                            "Ang threshold ay dapat na nasa pagitan ng 0 at 100 percent."
                        )
                    }
                )


class SiteSettingAudit(SoftDeleteModel, models.Model):
    """Audit log of changes to `SiteSetting`.

    Stores who changed what and when.
    """

    site_setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, related_name="audits")
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="site_setting_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="False = archived/soft-deleted (visible in Trash & Archive)",
    )

    class Meta:
        ordering = ["-changed_at"]
        verbose_name = "Site Setting Change Log"
        verbose_name_plural = "Site Setting Change Logs"

    def __str__(self):
        user = self.changed_by.get_username() if self.changed_by else "(system)"
        return f"{self.changed_at.isoformat()} by {user}"




class TimeStampedModel(models.Model):
    """Abstract base adding created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class KnowledgeBaseEntry(SoftDeleteModel, TimeStampedModel):
    """Knowledge base entries .

    Ginagamit para sa AgriScan Knowledge Base module:
      - Farmers can browse published entries (view-only)
      - Admins/Technicians can create/edit/archive entries

    Each entry consists of symptoms, causes, and prevention steps.
    """

    CATEGORY_CHOICES = [
        ('disease',        'Disease'),
        ('pest',           'Pest'),
        ('crop_nutrition', 'Crop Nutrition & Fertilizer'),
        ('irrigation',     'Irrigation & Water Management'),
        ('soil',           'Soil Management'),
        ('post_harvest',   'Post-Harvest & Storage'),
    ]

    name = models.CharField(max_length=200, help_text="Pangalan ng sakit/peste/deficiency")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="disease")
    description = models.TextField(help_text="Maikling overview ng kondisyon")
    symptoms = models.TextField(help_text="Ano ang makikita sa tanim")
    causes = models.TextField(blank=True, help_text="Mga posibleng sanhi")
    prevention = models.TextField(blank=True, help_text="Paano maiiwasan ang kondisyon")
    image = models.ImageField(
        upload_to="knowledge_images/",
        blank=True,
        null=True,
        help_text="Opsyonal: upload ng larawan ng sintomas",
    )
    is_published = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Kapag naka-check, lalabas ang entry para sa mga magsasaka."
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="knowledge_entries",
        help_text="Admin/technician na gumawa ng entry",
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this knowledge entry has been viewed (for trends/analytics)",
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="False = archived/soft-deleted (visible in Trash & Archive)",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Knowledge Base Entry"
        verbose_name_plural = "Knowledge Base Entries"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Profile(TimeStampedModel):
    ROLE_CHOICES = (
        ("admin", "Administrator / DA Officer"),
        ("technician", "Field Technician"),
        ("farmer", "Farmer"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="farmer")
    phone = models.CharField(max_length=32, blank=True)
    location = models.CharField(max_length=128, blank=True)
    farm_size_ha = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True,
        editable=False,  # Auto-computed, not manually editable
        help_text="Auto-computed from total field area"
    )
    notes = models.TextField(blank=True)
    
    # BEST PRACTICE: Account approval system
    is_approved = models.BooleanField(
        default=True,  # Auto-approve by default (can change to False for manual approval)
        help_text="Admin must approve before user can login"
    )

    def __str__(self):
        return f"{self.user.get_username()} ({self.role})"
    
    def update_farm_size(self):
        """
        BEST PRACTICE: Auto-compute farm_size_ha from sum of all fields owned by this user.
        Call this method after creating/updating/deleting fields.
        """
        from django.db.models import Sum
        total = self.fields.aggregate(total=Sum('area_hectares'))['total']
        self.farm_size_ha = total or 0
        self.save(update_fields=['farm_size_ha'])


class Field(SoftDeleteModel, TimeStampedModel):
    """Represents a specific agricultural field owned/managed by a farmer.

    Tagalog:
    - Ito ang lugar kung saan nag-tatanim ang farmer.
    - Kinakailangan para sa yield prediction, field planning, at reporting.
    - Hindi tinatanggal (soft-delete lang gamit `is_active`) para may history ang mga planting records.
    """

    SOIL_TYPE_CHOICES = [
        ('', 'Unknown   '),
        ('clay', 'Clay'),
        ('loam', 'Loam'),
        ('sandy', 'Sandy'),
        ('silt', 'Silt'),
        ('clay_loam', 'Clay Loam'),
        ('sandy_loam', 'Sandy Loam'),
        ('peaty', 'Peaty'),
        ('mixed', 'Mixed'),
        ('other', 'Other'),
    ]

    ECOSYSTEM_TYPE_CHOICES = [
        ('', 'Unknown'),
        ('irrigated', 'Irrigated'),
        ('rainfed_lowland', 'Rainfed Lowland'),
        ('upland', 'Upland'),
        ('flood_prone', 'Flood Prone'),
        ('saline', 'Saline / Coastal'),
        ('other', 'Other'),
    ]

    # Field ownership and identification
    owner = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="fields")
    name = models.CharField(max_length=100)

    # Location details
    barangay = models.CharField(max_length=100, null=True, blank=True, default='', help_text="Barangay name")
    municipality = models.CharField(max_length=100, blank=True, default='',help_text="Municipality")
    province = models.CharField(max_length=100, blank=True, default='', help_text="Province")

    # Area & GPS (optional)
    area_hectares = models.DecimalField(max_digits=7, decimal_places=2)
    gps_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    gps_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Agronomic attributes used for yield prediction / analytics
    soil_type = models.CharField(
        max_length=50,
        choices=SOIL_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Primary soil type of this field",
    )
    ecosystem_type = models.CharField(
        max_length=50,
        choices=ECOSYSTEM_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Ecosystem classification for this field",
    )
    flood_prone = models.BooleanField(
        default=False,
        help_text="Mark if this field is prone to seasonal flooding",
    )

    # Soft delete for audit history (plantings should remain intact)
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="False = archived/soft-deleted (visible in Trash & Archive)",
    )

    class Meta:
        unique_together = ("owner", "name")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.area_hectares} ha)"

    def purge(self):
        """Permanently delete this field and dependent plantings."""
        from .models import PlantingRecord

        # Permanently delete associated planting cycles first
        for planting in PlantingRecord.all_objects.filter(field=self):
            if hasattr(planting, 'purge'):
                planting.purge()
            else:
                planting.delete()

        # Now delete field record
        super().hard_delete()


class RiceVariety(SoftDeleteModel, models.Model):
    """
    Rice variety — kumpletong impormasyon tungkol sa bawat uri ng palay.
    Mula sa basic identity hanggang pest resistance at management recommendations.
    """

    # ── Mga choice constants ─────────────────────────────────────────────
    class VarietyType(models.TextChoices):
        INBRED           = 'inbred',       'Inbred'
        HYBRID           = 'hybrid',       'Hybrid'
        TRADITIONAL      = 'traditional',  'Traditional / Local'
        SPECIALTY        = 'specialty',    'Specialty'
        STRESS_TOLERANT  = 'stress',       'Stress-Tolerant'

    class ClimateType(models.TextChoices):
        IRRIGATED    = 'irrigated',    'Irrigated'
        RAINFED      = 'rainfed',      'Rainfed Lowland'
        UPLAND       = 'upland',       'Upland'
        FLOOD_PRONE  = 'flood_prone',  'Flood-Prone / Submergence-Tolerant'
        SALINE       = 'saline',       'Saline-Prone'

    class ResistanceLevel(models.TextChoices):
        RESISTANT            = 'R',  'Resistant'
        MODERATELY_RESISTANT = 'MR', 'Moderately Resistant'
        SUSCEPTIBLE          = 'S',  'Susceptible'
        HIGHLY_SUSCEPTIBLE   = 'HS', 'Highly Susceptible'
        UNKNOWN              = 'U',  'Unknown'

    class CertificationLevel(models.TextChoices):
        BREEDER    = 'breeder',    'Breeder Seed'
        FOUNDATION = 'foundation', 'Foundation Seed'
        REGISTERED = 'registered', 'Registered Seed'
        CERTIFIED  = 'certified',  'Certified Seed'
        LOCAL      = 'local',      'Truthfully Labeled / Local Seed'

    # ── 1. Variety Identification ─────────────────────────────────────────
    # Pangunahing pagkakakilanlan ng variety
    code = models.CharField(
        max_length=20, unique=True,
        help_text="Natatanging code ng variety (hal. RC222, NSIC Rc222)"
    )
    name = models.CharField(
        max_length=120,
        help_text="Buong pangalan ng rice variety"
    )
    variety_type = models.CharField(
        max_length=12, choices=VarietyType.choices,
        default=VarietyType.INBRED,
        help_text="Uri ng variety: Inbred, Hybrid, Traditional, Specialty, o Stress-Tolerant"
    )
    release_year = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="Taon na inilabas ang variety (hal. 2012)"
    )
    developer = models.CharField(
        max_length=200, blank=True,
        help_text="Nagpapalaki/nagde-develop ng variety (hal. PhilRice, IRRI)"
    )

    # ── 2. Agronomic Characteristics ─────────────────────────────────────
    # Biological traits ng variety
    average_growth_days = models.PositiveIntegerField(
        help_text="Average araw mula tanim hanggang ani"
    )
    plant_height_cm = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="Karaniwang taas ng halaman (cm)"
    )
    tillering_capacity = models.CharField(
        max_length=50, blank=True,
        help_text="Kakayahang mag-tiller (hal. High, Moderate, Low)"
    )
    grain_type = models.CharField(
        max_length=100, blank=True,
        help_text="Uri ng butil (hal. Long slender, Medium bold)"
    )
    lodging_resistance = models.CharField(
        max_length=50, blank=True,
        help_text="Resistansya sa pagliliko ng halaman (hal. Good, Moderate)"
    )

    # ── 3. Environmental Adaptation ──────────────────────────────────────
    # Kung saan environment pinaka-angkop ang variety
    climate_type = models.CharField(
        max_length=20, choices=ClimateType.choices,
        default=ClimateType.IRRIGATED,
        help_text="Uri ng klima na angkop sa variety"
    )
    soil_type_compatibility = models.CharField(
        max_length=200, blank=True,
        help_text="Uri ng lupa na angkop (hal. Clay loam, Sandy loam)"
    )
    flood_tolerance = models.CharField(
        max_length=50, blank=True,
        help_text="Toleransya sa baha (hal. Tolerant, Susceptible)"
    )
    drought_tolerance = models.CharField(
        max_length=50, blank=True,
        help_text="Toleransya sa tagtuyot"
    )
    temperature_tolerance = models.CharField(
        max_length=100, blank=True,
        help_text="Toleransya sa temperatura (hal. Tolerant to high temperature)"
    )

    # ── 4. Yield Characteristics ─────────────────────────────────────────
    # Performance ng variety
    average_yield_t_ha = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Karaniwang ani (tonelada/ektarya)"
    )
    potential_yield_t_ha = models.DecimalField(
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Pinakamataas na posibleng ani (tonelada/ektarya)"
    )
    grain_quality = models.CharField(
        max_length=100, blank=True,
        help_text="Kalidad ng butil (hal. Premium, Good milling quality)"
    )

    # ── 5. Pest and Disease Resistance ───────────────────────────────────
    # Resistansya sa bawat sakit na kinikilala ng CNN scanner (12 classes)
    blast_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Leaf Blast (Pyricularia oryzae — leaf stage)"
    )
    neck_blast_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Neck Blast (Pyricularia oryzae — panicle stage)"
    )
    blight_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Bacterial Leaf Blight (Xanthomonas oryzae pv. oryzae)"
    )
    brown_spot_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Brown Spot (Bipolaris oryzae)"
    )
    false_smut_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="False Smut (Ustilaginoidea virens)"
    )
    leaf_scald_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Leaf Scald (Microdochium oryzae)"
    )
    leaf_smut_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Leaf Smut (Entyloma oryzae)"
    )
    narrow_brown_spot_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Narrow Brown Spot (Cercospora janseana)"
    )
    rice_hispa_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Rice Hispa (Dicladispa armigera — insect pest)"
    )
    sheath_blight_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Sheath Blight (Rhizoctonia solani)"
    )
    tungro_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Tungro Virus Disease (RTSV + RTBV)"
    )
    unhealthy_flowers_resistance = models.CharField(
        max_length=2, choices=ResistanceLevel.choices,
        default=ResistanceLevel.UNKNOWN, blank=True,
        help_text="Unhealthy Flowers / Panicle abnormality (CNN class: unhealthy_flowers)"
    )

    # ── 6. Seed Management ────────────────────────────────────────────────
    # Impormasyon tungkol sa binhi
    seed_source = models.CharField(
        max_length=200, blank=True,
        help_text="Pinagmulan ng binhi (hal. PhilRice, DA-RFU)"
    )
    seed_certification = models.CharField(
        max_length=20, choices=CertificationLevel.choices,
        blank=True,
        help_text="Antas ng sertipikasyon ng binhi"
    )
    germination_rate_pct = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="Porsyento ng pagsisibol ng binhi (0-100%)"
    )

    # ── 7. Management Recommendations ────────────────────────────────────
    # Gabay para sa mga magsasaka
    fertilizer_schedule = models.TextField(
        blank=True,
        help_text="Inirerekomendang iskedyul ng pataba"
    )
    water_management = models.CharField(
        max_length=200, blank=True,
        help_text="Paraan ng pamamahala ng tubig"
    )
    plant_spacing_cm = models.CharField(
        max_length=50, blank=True,
        help_text="Inirerekomendang distansya ng pagtatanim (hal. 20x20 cm)"
    )
    planting_season = models.CharField(
        max_length=100, blank=True,
        help_text="Angkop na panahon ng pagtatanim (hal. Wet season, Dry season)"
    )

    # ── Status ────────────────────────────────────────────────────────────
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="I-uncheck para i-archive ang variety. Naiingatan ang existing plantings.",
    )
    notes = models.TextField(
        blank=True,
        help_text="Karagdagang notes o obserbasyon"
    )

    class Meta:
        verbose_name = "Rice Variety"
        verbose_name_plural = "Rice Varieties"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}" if self.name else self.code

    def purge(self):
        """Permanently delete this variety and dependent planting cycles."""
        from .models import PlantingRecord

        for planting in PlantingRecord.all_objects.filter(variety=self):
            if hasattr(planting, 'purge'):
                planting.purge()
            else:
                planting.delete()

        super().hard_delete()


class DiseaseType(models.Model):
    """Supported rice leaf diseases the CNN can classify."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    # Tagalog: Primary knowledge link (canonical na KnowledgeBaseEntry para sa sakit na ito)
    primary_knowledge = models.ForeignKey(
        'KnowledgeBaseEntry',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='primary_for_diseases',
        help_text=(
            "Opsyonal: i-link ang disease type sa primary na Knowledge base record. "
            "Ginagamit kapag walang per-treatment KB mapping na na-set."
        ),
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TreatmentRecommendation(SoftDeleteModel, TimeStampedModel):
    """Practical recommendation mapped to a disease type with comprehensive treatment information."""
    disease = models.ForeignKey(DiseaseType, on_delete=models.CASCADE, related_name="treatments")

    # Basic treatment information
    short_text = models.CharField(max_length=200, help_text="Quick summary for mobile/dashboard")
    detailed_text = models.TextField(blank=True, help_text="Full detailed treatment instructions")

    # Symptoms and identification (deprecated in UI; canonical source is KnowledgeBaseEntry)
    symptoms = models.TextField(
        blank=True,
        help_text=(
            "(Deprecated) Key symptoms/identification markers. "
            "Use `KnowledgeBaseEntry` for production data (symptoms/causes/prevention)."
        )
    )

    # Contributing factors
    factors_favoring = models.TextField(blank=True, help_text="Environmental/agronomic factors that favor disease")

    # Link to knowledge entries containing canonical symptoms, causes, prevention.
    # Tagalog: DITO ilagay ang canonical na Knowledge items. TreatmentRecommendation
    #       ang operational metadata (factors, IPM steps, severity escalation).
    knowledge_entries = models.ManyToManyField(
        'KnowledgeBaseEntry',
        blank=True,
        related_name='treatments',
        help_text=(
            "Pumili ng isa o higit pang Knowledge Base entry na naglalaman ng "
            "symptoms/causes/prevention.  Ang Treatment form ay magre-relay sa KB."
        ),
    )

    # Per-factor quick actions — stored as JSON lines, one per factor row.
    # Each line in factors_favoring maps 1-to-1 with one line here.
    # Format: one action per line, in the same order as factors_favoring lines.
    # Leave a line blank to fall back to the generic urgency message.
    # Example (Brown Spot):
    #   Apply urea or ammonium sulfate at recommended rate
    #   Improve field drainage; avoid prolonged flooding
    #   Reduce plant spacing to improve air circulation
    factor_actions = models.TextField(
        blank=True,
        help_text=(
            "Per-factor quick action — one line per factor, same order as Factors Favoring Disease. "
            "Leave blank lines to use the generic urgency message."
        )
    )

    # Per-factor expected results — one line per factor, same order as factors_favoring.
    # Describes what outcome the farmer can expect if the quick action is followed.
    # Example (Brown Spot):
    #   Reduced lesion spread within 7-10 days
    #   Drier soil reduces fungal spore germination; slows disease spread
    #   Improved airflow lowers humidity around leaves by 10-15%
    factor_expected_results = models.TextField(
        blank=True,
        help_text=(
            "Expected result if the quick action is followed — one line per factor, "
            "same order as Factors Favoring Disease. Leave blank lines if not applicable."
        )
    )

    # Best practice management strategies
    cultural_practices = models.TextField(blank=True, help_text="Cultural/agronomic management practices")
    chemical_control = models.TextField(blank=True, help_text="Fungicide/pesticide recommendations if applicable")

    # Prevention now lives in KnowledgeBaseEntry, not in TreatmentRecommendation.
    preventive_measures = models.TextField(
        blank=True,
        help_text=(
            "(Deprecated) Prevention strategies. "
            "Set these in linked KnowledgeBaseEntry entries instead."
        )
    )

    # Severity escalation — DA/IPM technician sets the threshold and message.
    # When detection severity_pct >= severity_threshold, the severity_high_msg
    # is appended to the Quick Recommendation card (below the factor actions).
    # Below the threshold, factor checkboxes alone are sufficient (IPM principle).
    severity_threshold = models.PositiveSmallIntegerField(
        default=70,
        help_text=(
            "Severity % at which cultural IPM alone is no longer sufficient. "
            "When detection severity ≥ this value, the Escalation Message below "
            "is shown alongside the Quick Recommendation. "
            "Set based on IPM principles (e.g. 40 for high-priority diseases, 70 for low-priority)."
        )
    )
    severity_high_msg = models.TextField(
        blank=True,
        help_text=(
            "IPM-curated escalation message shown when detection severity ≥ threshold. "
            "Write this based on IPM principles — what action is needed when cultural "
            "control alone is no longer sufficient. Leave blank to hide the severity line."
        )
    )

    # Severity-based application
    severity_min = models.PositiveSmallIntegerField(default=0, help_text="Min severity % for applicability")
    severity_max = models.PositiveSmallIntegerField(default=100, help_text="Max severity % for applicability")

    # Additional metadata
    priority = models.PositiveSmallIntegerField(default=5, help_text="Display priority: 1-10 scale (1=least critical, 10=most severe/critical)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["disease", "-priority", "severity_min", "-pk"]
        indexes = [
            models.Index(fields=["disease", "is_active"]),
        ]

    def __str__(self):
        return f"{self.disease.name}: {self.short_text}"[:80]

    def get_knowledge_entries(self):
        """Return the authoritative published knowledge entries for this treatment.

        - Primary: directly linked `knowledge_entries` that are both active and published.
        - Fallback: `disease.primary_knowledge` only if active and published.

        Tagalog: Ang draft ng Knowledge ay hindi dapat i-link o i-display sa farmer-facing result.
        """
        kb_qs = self.knowledge_entries.filter(is_active=True, is_published=True)
        if kb_qs.exists():
            return list(kb_qs)

        if self.disease and getattr(self.disease, 'primary_knowledge', None):
            pk = self.disease.primary_knowledge
            if pk.is_active and pk.is_published:
                return [pk]

        return []

    def get_aggregated_text(self, field_name: str) -> str:
        """Combine text from linked knowledge entries for display."""
        entries = self.get_knowledge_entries()
        if not entries:
            return getattr(self, field_name, '') or ''

        parts = []
        for entry in entries:
            value = getattr(entry, field_name, '')
            if value and value.strip():
                parts.append(value.strip())
        return '\n\n'.join(parts)

    def get_formatted_treatment(self) -> dict:
        """Return structured treatment data for display."""
        # Parse factors_favoring into a list of clean strings for checkbox rendering
        factors_lines = []
        if self.factors_favoring:
            for raw in self.factors_favoring.splitlines():
                # Strip bullet chars (•, ·, *, -, –) and whitespace
                cleaned = raw.strip().lstrip('•·*-–➤▸▪▸►◆◇').strip()
                if cleaned:
                    factors_lines.append(cleaned)

        # Parse factor_actions into a parallel list (same index as factors_lines)
        factor_action_lines: list[str] = []
        if self.factor_actions:
            factor_action_lines = [line.strip() for line in self.factor_actions.splitlines()]

        # Parse factor_expected_results into a parallel list
        factor_result_lines: list[str] = []
        if self.factor_expected_results:
            factor_result_lines = [line.strip() for line in self.factor_expected_results.splitlines()]

        # Pad both parallel lists to match factors_lines length
        while len(factor_action_lines) < len(factors_lines):
            factor_action_lines.append('')
        factor_action_lines = factor_action_lines[:len(factors_lines)]

        while len(factor_result_lines) < len(factors_lines):
            factor_result_lines.append('')
        factor_result_lines = factor_result_lines[:len(factors_lines)]

        # Build a list of {factor, action, expected_result} dicts consumed by JS
        factors_with_actions = [
            {
                'factor':           f,
                'action':           factor_action_lines[i],
                'expected_result':  factor_result_lines[i],
            }
            for i, f in enumerate(factors_lines)
        ]

        # Pull canonical symptoms/causes/prevention from linked Knowledge entries.
        # Treatment model itself keeps these fields for backward compatibility during migration,
        # but UI should show KB content only (as per requirement).
        knowledge_entries = self.get_knowledge_entries()
        knowledge_payload = [
            {
                'name': entry.name,
                'category': entry.category,
                'description': entry.description,
                'symptoms': entry.symptoms,
                'causes': entry.causes,
                'prevention': entry.prevention,
                'pk': entry.pk,
            }
            for entry in knowledge_entries
        ]

        return {
            'short_text': self.short_text,
            'detailed_text': self.detailed_text,
            'symptoms': self.get_aggregated_text('symptoms'),
            'factors_favoring': self.factors_favoring,
            'factors_favoring_lines': factors_lines,
            'factors_with_actions': factors_with_actions,
            'cultural_practices': self.cultural_practices,
            'chemical_control': self.chemical_control,
            'preventive_measures': self.get_aggregated_text('prevention'),
            'knowledge_entries': knowledge_payload,
            'severity_range': f"{self.severity_min}-{self.severity_max}%",
            'treatment_pk': self.pk,
            'priority': self.priority,
            # Severity escalation — used by detail.html JS to append escalation message
            'severity_threshold': self.severity_threshold,
            'severity_high_msg':  self.severity_high_msg,
        }

    def get_urgency_levels(self) -> list:
        """Return urgency level config for the JS factor-checkbox feature.

        The Quick Recommendation card changes colour and message based on how
        many Factors Favoring Disease the farmer checks.  Thresholds and
        messages are derived from this treatment's ``priority`` so that
        high-priority diseases (e.g. Neck Blast P=9) escalate faster than
        low-priority ones (e.g. Leaf Scald P=3).

        Returns a list of dicts (index 0 = "0 checked", 1 = first threshold …)
        consumed by the detail.html <script> block.
        """
        p = self.priority or 5

        # High-priority disease: escalate at 1, 2, 3+ factors
        if p >= 8:
            return [
                None,  # 0 checked — default blue card
                {
                    'label':  '⚠️ 1 risk factor present — High-priority disease, stay alert!',
                    'detail': 'Monitor daily. High-priority diseases spread rapidly under favorable conditions.',
                    'bg':     'from-yellow-500 to-amber-600',
                },
                {
                    'label':  '🚨 2 risk factors — Immediate action required!',
                    'detail': 'Apply recommended cultural practices NOW. Do not wait for further spread.',
                    'bg':     'from-orange-500 to-red-600',
                },
                {
                    'label':  '🚨 Multiple risk factors — CRITICAL risk!',
                    'detail': 'All risk conditions are present. Implement full IPM protocol immediately and contact a DA technician.',
                    'bg':     'from-red-600 to-rose-800',
                },
            ]
        # Medium-priority disease: escalate at 2, 3, 4+ factors
        elif p >= 4:
            return [
                None,
                {
                    'label':  '⚠️ 1 risk factor present — Monitor closely',
                    'detail': 'One risk condition is present. Inspect your field regularly for early symptoms.',
                    'bg':     'from-blue-500 to-indigo-600',
                },
                {
                    'label':  '⚠️ 2 risk factors — Apply preventive measures',
                    'detail': 'Conditions are becoming favorable. Apply cultural practices to prevent spread.',
                    'bg':     'from-yellow-500 to-amber-600',
                },
                {
                    'label':  '🚨 Multiple risk factors — High risk! Take action now.',
                    'detail': 'Multiple favorable conditions detected. Follow the full treatment recommendation above.',
                    'bg':     'from-red-500 to-rose-700',
                },
            ]
        # Low-priority disease: only escalate at 3+ factors
        else:
            return [
                None,
                {
                    'label':  'ℹ️ 1 risk factor noted',
                    'detail': 'Mild disease risk. Continue good agronomic practices and monitor weekly.',
                    'bg':     'from-blue-500 to-indigo-600',
                },
                {
                    'label':  '⚠️ 2 risk factors — Increase monitoring frequency',
                    'detail': 'Some favorable conditions present. Consider applying preventive cultural measures.',
                    'bg':     'from-blue-600 to-indigo-700',
                },
                {
                    'label':  '⚠️ Multiple risk factors — Apply preventive treatment',
                    'detail': 'Several risk conditions are present. Apply cultural practices as described above.',
                    'bg':     'from-yellow-500 to-amber-600',
                },
            ]

    def get_section_status(self) -> dict:
        """Return per-section fill status and overall completeness for list display."""
        sections = {
            'symptoms':      bool(self.get_aggregated_text('symptoms').strip()),
            'factors':       bool(self.factors_favoring and self.factors_favoring.strip()),
            'cultural':      bool(self.cultural_practices and self.cultural_practices.strip()),
            'chemical':      bool(self.chemical_control and self.chemical_control.strip()),
            'prevention':    bool(self.get_aggregated_text('prevention').strip()),
            'severity_esc':  bool(self.severity_high_msg and self.severity_high_msg.strip()),
        }
        filled = sum(sections.values())
        total = len(sections)
        pct = round(filled / total * 100)
        priority = self.priority or 5
        if priority >= 8:
            priority_level = 'High'
            priority_color = 'red'
        elif priority >= 4:
            priority_level = 'Med'
            priority_color = 'amber'
        else:
            priority_level = 'Low'
            priority_color = 'blue'
        return {
            **sections,
            'filled': filled,
            'total': total,
            'pct': pct,
            'priority_level': priority_level,
            'priority_color': priority_color,
        }


class ModelVersion(TimeStampedModel):
    """Tracks deployed CNN / ML model versions for audits."""
    version = models.CharField(max_length=40, unique=True)
    description = models.TextField(blank=True)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    file_path = models.CharField(max_length=255, blank=True, help_text="Path to .h5 or .tflite")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.version


class DetectionRecord(SoftDeleteModel, TimeStampedModel):
    """Each disease detection from an uploaded/captured image.
    
    Note: Field is accessed via planting.field relationship to avoid redundancy
    and maintain data normalization (3NF).
    """
    planting = models.ForeignKey('PlantingRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name="detections", help_text="Link to specific planting cycle (field derived from this)")
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="detections")
    image_path = models.CharField(max_length=255, blank=True)  # store relative or cloud URL
    disease = models.ForeignKey(DiseaseType, on_delete=models.SET_NULL, null=True, blank=True)
    confidence_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    severity_pct = models.PositiveSmallIntegerField(null=True, blank=True)  # computed/entered
    treatment_text = models.CharField(max_length=200, blank=True)
    model_version = models.ForeignKey(ModelVersion, on_delete=models.SET_NULL, null=True, blank=True)
    source = models.CharField(max_length=20, default="web", help_text="web|mobile|api")
    has_synced = models.BooleanField(default=True, help_text="False if stored offline awaiting sync")
    is_active = models.BooleanField(default=True, db_index=True, help_text="False = soft-deleted/archived")

    class Meta:
        indexes = [
            models.Index(fields=["disease"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["planting"]),
        ]
    
    @property
    def field(self):
        """Access field through planting relationship."""
        return self.planting.field if self.planting else None

    def __str__(self):
        return f"Detection {self.pk} - {self.disease or 'Unknown'} ({self.confidence_pct}%)"

    def purge(self):
        """Permanently delete this detection record."""
        super().hard_delete()


class PlantingRecord(SoftDeleteModel, TimeStampedModel):
    """Planting metadata per field.

    This is the central link between Field → Detection → Yield Prediction.

    Tagalog:
    - Dito nakatala ang cycle ng tanim, kung kailan pinatanim, anong variety, at status.
    - Ang `cropping_cycle` ay awtomatikong kinakalkula (bilang ng planting para sa taon).
    - Hindi nilalagyan ng actual yield (nasa HarvestRecord o YieldPrediction).
    """

    SEASON_CHOICES = [
        ('wet', 'Wet Season'),
        ('dry', 'Dry Season'),
    ]

    PLANTING_METHOD_CHOICES = [
        ('direct_seeding', 'Direct Seeding'),
        ('transplanting',  'Transplanting'),
    ]

    STATUS_CHOICES = [
        ('planned',   'Planned'),
        ('ongoing',   'Ongoing'),
        ('harvested', 'Harvested'),
        ('failed',    'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    field = models.ForeignKey(Field, on_delete=models.PROTECT, related_name="plantings")
    variety = models.ForeignKey(RiceVariety, on_delete=models.PROTECT, null=True, blank=True, related_name="plantings")

    # Core cycle fields
    planting_date = models.DateField(default=timezone.now)
    expected_harvest_date = models.DateField(null=True, blank=True)
    actual_harvest_date = models.DateField(null=True, blank=True)

    # Seasonal & management
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, default='wet')
    cropping_cycle = models.PositiveIntegerField(
        null=True, blank=True, editable=False,
        help_text="Auto-computed cycle number for this field/year",
    )
    planting_method = models.CharField(max_length=50, choices=PLANTING_METHOD_CHOICES, default='direct_seeding')

    # Area & agronomic inputs (used downstream for yield prediction)
    area_planted_ha = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    seed_rate_kg_per_ha = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    # Lifecycle tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True, help_text="False = soft-deleted/archived")

    # Legacy fields (for backward compatibility with older reports)
    average_growth_duration_days = models.PositiveIntegerField(
        help_text="Number of days until harvest (typically 90-150 days)",
        null=True, blank=True
    )

    def clean(self):
        """Model-level validation para sa planting record."""
        super().clean()

        # Ensure planted area is positive and within the field size
        if self.area_planted_ha is not None and self.field and self.field.area_hectares:
            if self.area_planted_ha <= 0:
                raise ValidationError({'area_planted_ha': 'Area planted must be greater than zero.'})
            if self.area_planted_ha > self.field.area_hectares:
                raise ValidationError({'area_planted_ha': 'Area planted cannot exceed the field size.'})

        # Ensure expected harvest date makes sense
        if self.planting_date and self.expected_harvest_date:
            if self.expected_harvest_date <= self.planting_date:
                raise ValidationError({'expected_harvest_date': 'Expected harvest date must be after planting date.'})

        # Ensure planting date is not too far in the past (based on system setting)
        if self.planting_date:
            from . import services  # local import to avoid circular dependencies

            today = timezone.now().date()
            allowed_days = services.get_allowed_past_days_for_planting()
            if allowed_days < 0:
                allowed_days = 0

            min_allowed_date = today - timezone.timedelta(days=allowed_days)
            if self.planting_date < min_allowed_date:
                raise ValidationError(
                    {
                        'planting_date': (
                            'Planting date is too far in the past. ' 
                            f'Admin allows only up to {allowed_days} day(s) back from today.'
                        )
                    }
                )

    def save(self, *args, **kwargs):
        """Auto-compute derived fields and validate before saving."""
        self.full_clean()

        # Compute cropping cycle (count of ALL plantings for the same field/year)
        # NOTE: We count archived/soft-deleted and failed/cancelled plantings too so
        #       cycle numbers remain stable and we do not create gaps.
        #
        # IMPORTANT: Only assign the cycle number once (when the record is created).
        #            Do NOT recompute on updates to avoid renumbering existing records.
        if self.field and self.planting_date and self.pk is None:
            year = self.planting_date.year

            # Count existing planting records for this field/year (all statuses, even archived)
            existing_count = PlantingRecord.objects.filter(
                field=self.field,
                planting_date__year=year,
            ).count()

            # Enforce realistic maximum: 3 crops per year (Dry/Wet/3rd crop in PH rice farming)
            if existing_count >= 3:
                raise ValidationError({
                    'planting_date': (
                        f"There are already {existing_count} planting cycles recorded for {year}. "
                        "Maximum is 3 crops per year."
                    )
                })

            # Assign the next sequential cycle number (1..3)
            self.cropping_cycle = existing_count + 1

        # Maintain expected harvest date when average growth duration is set
        if self.planting_date and self.average_growth_duration_days and not self.expected_harvest_date:
            self.expected_harvest_date = self.planting_date + timezone.timedelta(days=self.average_growth_duration_days)

        # NOTE: Historical yield is now sourced from HarvestRecord history via
        # get_historical_yield_data(). The legacy PlantingRecord fields are no longer
        # used for historical yield calculations.
        super().save(*args, **kwargs)

    def __str__(self):
        variety_label = "Unknown Variety"
        try:
            if self.variety_id:
                variety_label = str(self.variety)
        except RiceVariety.DoesNotExist:
            variety_label = "Unknown Variety"

        field_label = str(self.field) if self.field_id else "Unknown Field"
        return f"Planting {variety_label} @ {field_label} ({self.planting_date:%Y-%m-%d})"

    def purge(self):
        """Permanently delete this planting and dependent records."""
        from .models import YieldPrediction, HarvestRecord, DetectionRecord, SeasonLog

        for y in YieldPrediction.all_objects.filter(planting=self):
            if hasattr(y, 'purge'):
                y.purge()
            else:
                y.delete()

        for h in HarvestRecord.all_objects.filter(planting=self):
            if hasattr(h, 'purge'):
                h.purge()
            else:
                h.delete()

        for d in DetectionRecord.all_objects.filter(planting=self):
            d.delete()

        for s in SeasonLog.all_objects.filter(planting=self):
            s.delete()

        super().hard_delete()


class YieldPrediction(SoftDeleteModel, TimeStampedModel):
    """Stores output of yield estimation model.
    
    New structure based on tons/ha (industry standard) instead of sacks/ha.
    Links to planting record for complete historical tracking and ML training.
    """

    planting = models.ForeignKey(
        PlantingRecord,
        on_delete=models.CASCADE,
        related_name="yield_predictions",
        null=True,
        blank=True,
    )
    detection = models.ForeignKey(
        DetectionRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="yield_predictions",
    )
    
    # Predicted outputs (in tons/ha - industry standard)
    predicted_yield_tons_per_ha = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="Predicted yield in tons per hectare",
        null=True, blank=True
    )
    predicted_total_production_tons = models.DecimalField(
        max_digits=9, decimal_places=2,
        help_text="Total production = yield/ha × area",
        null=True, blank=True
    )
    
    # Model metadata
    confidence_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    model_version = models.CharField(max_length=120, blank=True, help_text="Model identifier/version")
    
    # Yield readiness / maturity prediction
    READINESS_CHOICES = (
        ('early', 'Early Stage (0-40 days)'),
        ('vegetative', 'Vegetative (41-65 days)'),
        ('reproductive', 'Reproductive (66-85 days)'),
        ('ripening', 'Ripening (86-100 days)'),
        ('harvest_ready', 'Harvest Ready (100+ days)'),
    )
    yield_readiness = models.CharField(
        max_length=20, choices=READINESS_CHOICES,
        help_text="Crop maturity stage based on growth duration",
        null=True, blank=True
    )
    
    # Harvest timing
    estimated_harvest_date = models.DateField(
        null=True, blank=True,
        help_text="Predicted harvest date = planting_date + growth_duration"
    )
    actual_harvest_date = models.DateField(
        null=True, blank=True,
        help_text="Actual harvest date (for training accuracy)"
    )
    
    # Legacy fields (for backward compatibility)
    predicted_sacks_per_ha = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text="Legacy: sacks per hectare (1 sack ≈ 50kg)",
        null=True, blank=True
    )
    area_hectares = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    total_sacks = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    total_tons = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    harvest_date = models.DateField(null=True, blank=True)
    model_meta = models.CharField(max_length=120, blank=True, help_text="Deprecated: use model_version")
    is_active = models.BooleanField(default=True, db_index=True, help_text="False = soft-deleted/archived")

    class Meta:
        indexes = [models.Index(fields=["created_at"])]

    def save(self, *args, **kwargs):
        # Auto-calculate total production if area is available
        if self.predicted_yield_tons_per_ha and self.planting and self.planting.field:
            area = self.planting.field.area_hectares
            self.predicted_total_production_tons = self.predicted_yield_tons_per_ha * area
            self.area_hectares = area
        
        # Convert to sacks for backward compatibility (1 ton ≈ 20 sacks @ 50kg each)
        if self.predicted_yield_tons_per_ha:
            self.predicted_sacks_per_ha = self.predicted_yield_tons_per_ha * 20  # 1 ton = 20 sacks
            if self.predicted_total_production_tons:
                self.total_sacks = self.predicted_total_production_tons * 20
                self.total_tons = self.predicted_total_production_tons
        elif self.predicted_sacks_per_ha:
            # Legacy: convert from sacks to tons
            self.predicted_yield_tons_per_ha = self.predicted_sacks_per_ha / 20
            if self.area_hectares:
                self.predicted_total_production_tons = self.predicted_yield_tons_per_ha * self.area_hectares
        
        # Sync harvest dates
        if self.estimated_harvest_date and not self.harvest_date:
            self.harvest_date = self.estimated_harvest_date
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Yield {self.predicted_yield_tons_per_ha} tons/ha ({self.yield_readiness or 'N/A'})"

    def purge(self):
        """Permanently delete this yield prediction."""
        super().hard_delete()


class HarvestRecord(SoftDeleteModel, models.Model):
    """Actual harvest results recorded after harvest.

    This is separate from YieldPrediction (which stores model estimates).
    It is the single source of truth for actual harvested yield and is used
    for model training and historical yield calculations.

    Tagalog:
    - Dito ini-encode ang aktwal na ani pagkatapos anihin.
    - Ang `yield_tons_per_ha` ay awtomatikong kinakalkula mula sa ani at area.
    """

    GRAIN_QUALITY_CHOICES = [
        ('',               'Not assessed'),
        ('premium',        'Premium'),
        ('well_milled',    'Well Milled'),
        ('regular_milled', 'Regular Milled'),
        ('under_grade',    'Under Grade'),
        ('other',          'Iba pa'),
    ]

    planting = models.OneToOneField(
        'PlantingRecord',
        on_delete=models.PROTECT,
        related_name='harvest_record'
    )
    harvest_date = models.DateField()
    actual_yield_tons = models.DecimalField(max_digits=8, decimal_places=2)
    area_harvested_ha = models.DecimalField(max_digits=6, decimal_places=2)
    yield_tons_per_ha = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    grain_quality = models.CharField(
        max_length=50,
        choices=GRAIN_QUALITY_CHOICES,
        null=True,
        blank=True,
    )
    notes = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="False = archived/soft-deleted (not used for historical averages)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['harvest_date']), models.Index(fields=['is_active'])]

    def save(self, *args, **kwargs):
        # Auto-calculate yield per hectare (tons/ha).
        if self.area_harvested_ha and self.area_harvested_ha != 0:
            self.yield_tons_per_ha = Decimal(self.actual_yield_tons) / Decimal(self.area_harvested_ha)
        else:
            self.yield_tons_per_ha = Decimal('0')

        super().save(*args, **kwargs)

        # Sync planting status and harvest date.
        # Tagalog: Gamitin ang QuerySet update() para
        # direktang i-update ang status at actual_harvest_date
        # nang hindi dinadaan sa full_clean() ng PlantingRecord.
        # Kailangan ito dahil ang planting_date validation
        # ay magfa-fail kapag ang planting ay matagal na —
        # hindi dapat hadlangan ang pag-update ng status.
        PlantingRecord.objects.filter(
            pk=self.planting_id,
        ).update(
            status='harvested',
            actual_harvest_date=self.harvest_date,
        )

        # Sync actual harvest date with yield predictions for training
        from .models import YieldPrediction  # local import to avoid circular
        YieldPrediction.objects.filter(planting=self.planting).update(actual_harvest_date=self.harvest_date)

    def purge(self):
        """Permanently delete this harvest record."""
        super().hard_delete()

    def __str__(self):
        return f"Harvest {self.harvest_date} ({self.yield_tons_per_ha} t/ha)"


class Notification(TimeStampedModel):
    """Real-time alerts (disease detection, yield drop, announcement bell alerts)."""
    TYPE_CHOICES = (
        ("disease", "Disease Detected"),
        ("yield_drop", "Yield Decrease"),
        ("advisory", "New Announcement"),
        ("knowledge", "New Knowledge Entry"),
        ("treatment", "New Treatment Recommendation"),
        ("system", "System Setting Update"),
    )
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="system_notifications")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=140)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_detection = models.ForeignKey(DetectionRecord, on_delete=models.SET_NULL, null=True, blank=True)
    related_yield = models.ForeignKey(YieldPrediction, on_delete=models.SET_NULL, null=True, blank=True)
    related_announcement = models.ForeignKey(
        'Announcement', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bell_notifications',
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.type}: {self.title}"[:50]


class Announcement(TimeStampedModel):
    """System announcements and crop advisories (NO INTERNET REQUIRED).
    
    Supports local in-app notifications with optional email integration.
    Admin/Technicians can create targeted announcements for farmers.
    """
    
    AUDIENCE_CHOICES = [
        ('all', 'All Users'),
        ('farmers', 'All Farmers'),
        ('technicians', 'All Technicians'),
        ('barangay', 'Specific Barangay'),
        ('user', 'Specific User'),
    ]
    
    PRIORITY_CHOICES = [
        ('info', '📘 Information'),
        ('advisory', '📗 Announcement'),
        ('warning', '📙 Warning'),
        ('urgent', '📕 URGENT'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'General Announcement'),
        ('pest', 'Pest/Disease Alert'),
        ('weather', 'Weather Advisory'),
        ('harvest', 'Harvest Reminder'),
        ('training', 'Training/Seminar'),
        ('government', 'Government Program'),
        ('system', 'System Update'),
    ]
    
    # Content
    title = models.CharField(max_length=200, help_text="Announcement title")
    content = models.TextField(help_text="Full announcement message")
    created_by = models.ForeignKey(
        Profile, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_announcements',
        limit_choices_to={'role__in': ['admin', 'technician']},
        help_text="Admin or Technician who created this"
    )
    
    # Targeting
    target_audience = models.CharField(
        max_length=20, 
        choices=AUDIENCE_CHOICES, 
        default='all',
        help_text="Who should see this announcement"
    )
    target_barangay = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Barangay name (if target_audience='barangay')"
    )
    target_user = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
        related_name='targeted_announcements',
        help_text="Specific user (if target_audience='user')"
    )
    
    # Classification
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='info',
        help_text="Urgency level"
    )
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='general',
        help_text="Type of announcement"
    )
    
    # Status & Scheduling
    is_active = models.BooleanField(
        default=True,
        help_text="Active announcements are visible to users"
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="True = soft-deleted / in Trash"
    )
    published_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When to publish (null = immediate)"
    )
    expires_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Auto-hide after this date"
    )
    
    # Email Integration (FUTURE USE)
    send_email = models.BooleanField(
        default=False,
        help_text="[FUTURE] Send email notification (requires internet)"
    )
    email_sent = models.BooleanField(
        default=False,
        help_text="[FUTURE] Track if email was sent"
    )
    email_sent_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="[FUTURE] When email was sent"
    )

    class Meta:
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['target_audience', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['priority', 'is_active']),
        ]
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        priority_emoji = dict(self.PRIORITY_CHOICES).get(self.priority, '')
        return f"{priority_emoji} {self.title}"
    
    def is_visible(self):
        """Check if announcement should be visible now."""
        from django.utils import timezone
        now = timezone.now()
        
        if not self.is_active:
            return False
        
        if self.published_at and self.published_at > now:
            return False
        
        if self.expires_at and self.expires_at < now:
            return False
        
        return True
    
    def get_target_users(self):
        """Get list of Profile objects that should see this announcement."""
        from django.db.models import Q
        
        if self.target_audience == 'all':
            return Profile.objects.all()
        elif self.target_audience == 'farmers':
            return Profile.objects.filter(role='farmer')
        elif self.target_audience == 'technicians':
            return Profile.objects.filter(role='technician')
        elif self.target_audience == 'barangay' and self.target_barangay:
            # Get farmers in the specified barangay
            return Profile.objects.filter(
                role='farmer',
                fields__barangay=self.target_barangay
            ).distinct()
        elif self.target_audience == 'user' and self.target_user:
            return Profile.objects.filter(pk=self.target_user.pk)
        
        return Profile.objects.none()
    
    # FUTURE: Email integration method (ready to use)
    def send_email_notification(self):
        """[FUTURE] Send email to target users (requires internet & SMTP config)."""
        if not self.send_email or self.email_sent:
            return
        
        # Uncomment when ready to enable email
        """
        from django.core.mail import send_mass_mail
        from django.template.loader import render_to_string
        
        target_users = self.get_target_users()
        emails = []
        
        for user in target_users:
            if user.user.email:
                subject = f"[AgriScan+] {self.title}"
                message = render_to_string('emails/announcement.html', {
                    'announcement': self,
                    'user': user,
                })
                emails.append((subject, message, 'noreply@agriscan.ph', [user.user.email]))
        
        if emails:
            send_mass_mail(emails, fail_silently=True)
            self.email_sent = True
            self.email_sent_at = timezone.now()
            self.save()
        """
        pass


class UserNotification(models.Model):
    """Track which users have read which announcements (NO INTERNET REQUIRED).
    
    Used for:
    - Showing unread badge count
    - Marking announcements as read
    - Analytics on announcement reach
    """
    user = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    announcement = models.ForeignKey(
        Announcement, 
        on_delete=models.CASCADE,
        related_name='user_notifications'
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Has user viewed this announcement?"
    )
    read_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When user read the announcement"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'announcement']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['announcement']),
        ]
        verbose_name = "User Notification"
        verbose_name_plural = "User Notifications"

    def __str__(self):
        status = "✓ Read" if self.is_read else "○ Unread"
        return f"{self.user.user.username} - {self.announcement.title[:30]} [{status}]"


# ============================================================================
# SEASON FARM LOG — Farmer activity journal per planting cycle
# ============================================================================

class SeasonLog(SoftDeleteModel, TimeStampedModel):
    """One season journal per planting record.
    
    Captures the full story of a single rice crop cycle:
    - What was planted, on what area, in which season
    - What activities were done (land prep → planting → fertilizing → harvest)
    - What problems were encountered and how they were resolved
    - What was the actual harvest (sacks/tons + income)
    
    This becomes a searchable, filterable history that lets farmers
    compare seasons and lets DA officers see variety adoption per barangay.
    """

    SEASON_CHOICES = [
        ('dry',   '☀️ Dry Season / 1st Crop (Enero–Mayo)'),
        ('wet',   '🌧️ Wet Season / 2nd Crop (Hunyo–Oktubre)'),
        ('3rd',   '🌾 3rd Crop (Nobyembre–Disyembre)'),
    ]

    STAGE_CHOICES = [
        ('planning',     '📋 Planning'),
        ('land_prep',    '🚜 Land Preparation'),
        ('planting',     '🌱 Planting'),
        ('growing',      '🌾 Growing / Maintenance'),
        ('harvest_ready','✅ Harvest Ready'),
        ('harvested',    '🎉 Harvested'),
    ]

    # ── Core links ─────────────────────────────────────────────────────────
    farmer      = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                    related_name='season_logs',
                                    limit_choices_to={'role': 'farmer'})
    planting    = models.OneToOneField(PlantingRecord, on_delete=models.CASCADE,
                                       related_name='season_log',
                                       null=True, blank=True,
                                       help_text="Optional link to existing planting record")

    # ── Season identification ──────────────────────────────────────────────
    season_year = models.PositiveSmallIntegerField(
        help_text="Crop year (e.g. 2025)")
    season_type = models.CharField(max_length=10, choices=SEASON_CHOICES,
                                   default='dry')
    field       = models.ForeignKey(Field, on_delete=models.CASCADE,
                                    related_name='season_logs')
    variety     = models.ForeignKey(RiceVariety, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='season_logs')

    # ── Key dates ─────────────────────────────────────────────────────────
    date_started     = models.DateField(help_text="Start of season / land prep date")
    date_planted     = models.DateField(null=True, blank=True)
    date_harvested   = models.DateField(null=True, blank=True)

    # ── Harvest outcome ───────────────────────────────────────────────────
    actual_yield_sacks   = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Actual harvest in sacks (50 kg each)")
    actual_yield_tons    = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Actual harvest in metric tons (auto-calculated if blank)")
    price_per_sack       = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Selling price per sack (PHP)")
    gross_income         = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Total income = sacks × price (auto-calculated)")
    total_expenses       = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Total season expenses (inputs + labor + misc)")
    net_income           = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Net income = gross - expenses (auto-calculated)")

    # ── Status & notes ────────────────────────────────────────────────────
    current_stage = models.CharField(max_length=20, choices=STAGE_CHOICES,
                                     default='planning')
    summary_notes = models.TextField(blank=True,
                                     help_text="Overall notes for this season")
    is_active     = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-season_year', '-date_started']
        unique_together = [('farmer', 'field', 'season_year', 'season_type')]
        indexes = [
            models.Index(fields=['farmer', 'season_year']),
            models.Index(fields=['field', 'season_year']),
            models.Index(fields=['variety', 'season_year']),
        ]
        verbose_name = "Season Log"
        verbose_name_plural = "Season Logs"

    def save(self, *args, **kwargs):
        # Auto-calc tons from sacks (1 sack = 50 kg = 0.05 tons) — always recalculate
        if self.actual_yield_sacks:
            self.actual_yield_tons = self.actual_yield_sacks * 50 / 1000
        else:
            self.actual_yield_tons = None

        # Auto-calc gross income — always recalculate
        if self.actual_yield_sacks and self.price_per_sack:
            self.gross_income = self.actual_yield_sacks * self.price_per_sack
        else:
            self.gross_income = None

        # Auto-calc net income — always recalculate
        if self.gross_income is not None and self.total_expenses is not None:
            self.net_income = self.gross_income - self.total_expenses
        elif self.gross_income is not None:
            self.net_income = self.gross_income
        else:
            self.net_income = None

        super().save(*args, **kwargs)

    @property
    def yield_per_ha(self):
        """Sacks per hectare for comparison across farmers."""
        if self.actual_yield_sacks and self.field and self.field.area_hectares:
            try:
                return round(float(self.actual_yield_sacks) / float(self.field.area_hectares), 1)
            except (ZeroDivisionError, TypeError):
                return None
        return None

    @property
    def cost_per_sack(self):
        """Total expenses ÷ sacks harvested — how much it cost to produce one sack."""
        if self.total_expenses and self.actual_yield_sacks:
            try:
                return round(float(self.total_expenses) / float(self.actual_yield_sacks), 2)
            except (ZeroDivisionError, TypeError):
                return None
        return None

    @property
    def net_per_sack(self):
        """Net income ÷ sacks harvested — how much profit per sack."""
        if self.net_income is not None and self.actual_yield_sacks:
            try:
                return round(float(self.net_income) / float(self.actual_yield_sacks), 2)
            except (ZeroDivisionError, TypeError):
                return None
        return None

    @property
    def season_label(self):
        labels = {'dry': 'Dry Season', 'wet': 'Wet Season', '3rd': '3rd Crop'}
        return f"{labels.get(self.season_type, self.season_type)} {self.season_year}"

    def __str__(self):
        return f"{self.farmer} — {self.season_label} @ {self.field}"


class FarmActivity(TimeStampedModel):
    """Individual activity log entry within a SeasonLog.
    
    Records every significant farm action the farmer took:
    - Land preparation (plowing, harrowing, leveling)
    - Fertilizer application (kind, amount, cost)
    - Pesticide/fungicide spraying (product, dosage, target pest/disease)
    - Irrigation events
    - Scouting / disease observation
    - Harvest activities
    - Problems encountered + what was done
    
    This feeds:
    1. Farmer's personal history/journal
    2. DA analytics — what practices farmers actually follow
    3. Cost-of-production tracking
    4. Season comparison across years
    """

    ACTIVITY_CHOICES = [
        ('🌱 Crop Establishment', [
            ('land_prep',     '🚜 Land Preparation (Plowing/Harrowing)'),
            ('seedbed',       '🌱 Seedbed / Nursery Preparation'),
            ('transplanting', '🌾 Transplanting / Direct Seeding'),
        ]),
        ('💧 Water Management', [
            ('irrigation',    '💧 Irrigation'),
            ('drainage',      '🏔️ Drainage'),
        ]),
        ('🌿 Crop Nutrition', [
            ('fertilizer',    '🌿 Fertilizer Application'),
            ('foliar',        '🍃 Foliar / Micronutrient Spray'),
        ]),
        ('🐛 Crop Protection', [
            ('pesticide',     '🐛 Pesticide / Insecticide Application'),
            ('fungicide',     '🍄 Fungicide Application'),
            ('herbicide',     '🌿 Herbicide / Weeding'),
        ]),
        ('🔍 Monitoring', [
            ('scouting',      '🔍 Field Scouting / Crop Inspection'),
            ('disease_obs',   '🦠 Disease / Pest Observation'),
        ]),
        ('🎉 Harvest & Post-Harvest', [
            ('harvest',       '🎉 Harvest'),
            ('drying',        '☀️ Drying'),
            ('milling',       '⚙️ Milling'),
            ('selling',       '💰 Selling / Marketing'),
        ]),
        ('👷 General', [
            ('labor',         '👷 Labor / Hired Help'),
            ('equipment',     '🔧 Equipment Use / Repair'),
            ('other',         '📝 Other'),
        ]),
    ]

    PROBLEM_SEVERITY = [
        ('none',    'No Problem'),
        ('minor',   'Minor'),
        ('moderate','Moderate'),
        ('severe',  'Severe'),
    ]

    # ── Link ──────────────────────────────────────────────────────────────
    season_log      = models.ForeignKey(SeasonLog, on_delete=models.CASCADE,
                                        related_name='activities')

    # ── Activity details ──────────────────────────────────────────────────
    activity_date   = models.DateField()
    activity_type   = models.CharField(max_length=30, choices=ACTIVITY_CHOICES)
    title           = models.CharField(max_length=160,
                                       help_text="Short summary (e.g. 'Applied Urea 45-0-0, 1 bag/ha')")
    description     = models.TextField(blank=True,
                                       help_text="Detailed notes, observations, dosage, etc.")

    # ── Cost tracking ─────────────────────────────────────────────────────
    input_cost      = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=True, blank=True,
                                          help_text="Cost of materials/inputs (PHP)")
    labor_cost      = models.DecimalField(max_digits=10, decimal_places=2,
                                          null=True, blank=True,
                                          help_text="Labor cost (PHP)")

    # ── Problem tracking ──────────────────────────────────────────────────
    problem_observed     = models.CharField(max_length=200, blank=True,
                                             help_text="What problem was seen (pest, disease, etc.)")
    problem_severity     = models.CharField(max_length=10, choices=PROBLEM_SEVERITY,
                                             default='none')
    action_taken         = models.TextField(blank=True,
                                             help_text="What was done to address the problem")
    detection_record     = models.ForeignKey(DetectionRecord, on_delete=models.SET_NULL,
                                              null=True, blank=True,
                                              related_name='farm_activities',
                                              help_text="Link to AI scan if available")

    # ── Workers ───────────────────────────────────────────────────────────
    workers_count   = models.PositiveSmallIntegerField(default=0,
                                                        help_text="Number of laborers/workers")

    class Meta:
        ordering = ['activity_date']
        indexes = [
            models.Index(fields=['season_log', 'activity_date']),
            models.Index(fields=['activity_type']),
        ]
        verbose_name = "Farm Activity"
        verbose_name_plural = "Farm Activities"

    @property
    def total_cost(self):
        ic = float(self.input_cost or 0)
        lc = float(self.labor_cost or 0)
        return ic + lc if (ic or lc) else None

    def __str__(self):
        return f"[{self.activity_date}] {self.get_activity_type_display()} — {self.title[:60]}"


# FUTURE EXTENSIONS (placeholders):
# - AccuracyMetrics model for CNN evaluation over time.
# - ExportJob model for tracking generated CSV/PDF reports.
# - APIKey model for external system integrations.



