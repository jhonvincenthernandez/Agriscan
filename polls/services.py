from __future__ import annotations

import json
import importlib
import re
import threading
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone as dt_timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from django.conf import settings
from django.db.utils import OperationalError, ProgrammingError
from django.utils import timezone
from PIL import Image

try:  # TensorFlow is needed for the TFLite interpreter
    import tensorflow as tf
except Exception:  # pragma: no cover - optional dependency at runtime
    tf = None  # type: ignore

try:
    import joblib
except Exception:  # pragma: no cover - optional dependency at runtime
    joblib = None  # type: ignore

try:
    import pandas as pd
except Exception:  # pragma: no cover - optional dependency at runtime
    pd = None  # type: ignore


DATASET_DIR = Path(settings.BASE_DIR) / "dataset"
MODELS_DIR = Path(settings.BASE_DIR) / "models"
DETECTIONS_DIR = Path(settings.MEDIA_ROOT) / "detections"

# Single source of truth for the "unclassified" label.
# All templates and Python code must reference this — never hardcode the string.
UNKNOWN_LABEL = "Unknown/Not Rice"


def get_allowed_past_days_for_planting() -> int:
    """Return the number of days back the user can set their planting date.

    - Admin sets this via `SiteSetting.allowed_past_days_planting`.
    - If the DB isn't ready or the setting isn't configured, fall back to 30.
    """
    try:
        from .models import SiteSetting  # local import para iwas circular import sa startup

        setting = SiteSetting.objects.first()
        if setting and setting.allowed_past_days_planting is not None:
            return int(setting.allowed_past_days_planting)
    except (OperationalError, ProgrammingError):
        # Tagalog: kung hindi pa ready ang DB (migrations, etc), huwag mag-crash.
        # Gumamit lang ng default at hayaan ang system na tumakbo.
        pass

    # Default fallback (30 days pabalik)
    return getattr(settings, "SYSTEM_SETTING_DEFAULTS", {}).get("allowed_past_days_planting", 30)


def get_detection_confidence_threshold() -> int:
    """Return the confidence threshold (%) below which scans are treated as Unknown.

    Admins can configure this via `SiteSetting.detection_confidence_threshold`.
    If the setting is missing or the DB isn't initialized, we fall back to 75%.
    """
    try:
        from .models import SiteSetting  # local import para iwas circular import sa startup

        setting = SiteSetting.objects.first()
        if setting and setting.detection_confidence_threshold is not None:
            return int(setting.detection_confidence_threshold)
    except (OperationalError, ProgrammingError):
        pass

    return getattr(settings, "SYSTEM_SETTING_DEFAULTS", {}).get("detection_confidence_threshold", 75)


def get_yield_cnn_enabled() -> bool:
    """Return whether CNN yield mode is enabled for users.

    Priority:
    1. SiteSetting.yield_cnn_enabled (admin UI)
    2. Env/settings fallback (YIELD_CNN_ENABLED)
    """
    try:
        from .models import SiteSetting

        setting = SiteSetting.objects.first()
        if setting is not None:
            return bool(setting.yield_cnn_enabled)
    except (OperationalError, ProgrammingError):
        pass

    return bool(getattr(settings, "YIELD_CNN_ENABLED", False))


def get_email_enabled() -> bool:
    """Return whether outgoing email notifications are enabled.

    Priority:
    1. SiteSetting.email_enabled (admin UI)
    2. Env/settings fallback (EMAIL_ENABLED)
    """
    try:
        from .models import SiteSetting

        setting = SiteSetting.objects.first()
        if setting is not None:
            return bool(setting.email_enabled)
    except (OperationalError, ProgrammingError):
        pass

    return bool(getattr(settings, "EMAIL_ENABLED", False))

# Cache objects so we do not reload heavy assets on every request
_INTERPRETER: Optional[tf.lite.Interpreter] = None  # type: ignore
_INPUT_DETAILS: Optional[List[Dict[str, Any]]] = None
_OUTPUT_DETAILS: Optional[List[Dict[str, Any]]] = None
_INTERPRETER_LOCK = threading.Lock()

_CLASS_LABELS: Optional[List[str]] = None
_CLASS_LABELS_LOCK = threading.Lock()

_YIELD_MODEL = None
_YIELD_MODEL_LOCK = threading.Lock()
_YIELD_REPORT: Optional[Dict[str, Any]] = None
_YIELD_CNN_MODEL = None
_YIELD_CNN_DEVICE = None
_YIELD_CNN_LOCK = threading.Lock()
_TORCH = None

IMG_SIZE = (224, 224)
DEFAULT_TIPS = (
    "Check fields 7 days after spraying to adjust follow-up treatments.",
    "Combine field scouting with model predictions for higher accuracy.",
    "Record rainfall totals weekly—yield estimates improve with updated data.",
    "Ensure leaf samples are clean and well lit before scanning.",
)
LABEL_DISPLAY_OVERRIDES = {
    "bacterial_leaf_blight": "Bacterial Leaf Blight",
    "brown_spot": "Brown Spot",
    "leaf_blast": "Leaf Blast",
    "leaf_scald": "Leaf Scald",
    "narrow_brown_spot": "Narrow Brown Spot",
    "neck_blast": "Neck Blast",
    "rice_hispa": "Rice Hispa",
    "sheath_blight": "Sheath Blight",
    "tungro": "Tungro",
    "healthy": "Healthy",
    "unknown_not_rice": UNKNOWN_LABEL,
}

DEFAULT_TREATMENTS = {
    "Healthy": "No immediate action required. Continue field monitoring and good agronomic practices.",
    "Bacterial Leaf Blight": "Drain excess water, apply copper-based bactericide, and use resistant seeds next season.",
    "Brown Spot": "Balance nitrogen, remove weeds, and spray triazole fungicide if spreading.",
    "Leaf Blast": "Apply recommended systemic fungicide at booting stage and avoid late nitrogen.",
    "Leaf Scald": "Improve field drainage and remove infected stubbles after harvest.",
    "Narrow Brown Spot": "Spray benzimidazole fungicide when lesions spread fast and maintain potash levels.",
    "Neck Blast": "Spray fungicide at heading and ensure uniform water depth across the field.",
    "Rice Hispa": "Release parasitoids or use light traps; spray insecticide only when populations exceed threshold.",
    "Sheath Blight": "Reduce planting density, improve airflow, and treat with validamycin or propiconazole.",
    "Tungro": "Control leafhopper vectors early and plant tungro-tolerant varieties next cycle.",
    UNKNOWN_LABEL: "Image cannot be classified. Please retake photo with clear rice leaf, good lighting, and proper focus.",
    "Minimal": "Symptoms are minimal. Keep monitoring and maintain field sanitation.",
    "Mild": "Spot-treat affected hills and re-scout in 5 days.",
    "Moderate": "Consider targeted spraying and adjust fertilizer plan.",
    "Severe": "Consult your technician for immediate field intervention.",
}
DEFAULT_VARIETIES = (
    ("Rc222", "Rc222"),
    ("Rc160", "Rc160"),
    ("Rc216", "Rc216"),
)


@dataclass
class LeafPrediction:
    label: str
    confidence_pct: int
    severity_pct: int
    severity_label: str
    treatment: str

    def to_template_dict(self) -> Dict[str, Any]:
        return {
            "disease": self.label,
            "confidence": self.confidence_pct,
            "severity": f"{self.severity_pct}% ({self.severity_label})",
            "treatment": self.treatment,
        }


@dataclass
class YieldPredictionResult:
    tons_per_ha: float
    total_tons: float
    confidence_pct: int
    harvest_date: datetime
    yield_readiness: str
    sacks_per_ha: float  # Legacy compatibility
    total_sacks: float   # Legacy compatibility

    def to_template_dict(self) -> Dict[str, Any]:
        # Tagalog: Isang rounding policy lang para pare-pareho sa card, records, at exports.
        tons = round(self.tons_per_ha, 2)
        total_tons = round(self.total_tons, 2)
        sacks_per_ha = round(tons * 20, 2)
        total_sacks = round(total_tons * 20, 2)
        return {
            "value": tons,
            "value_display": f"{tons} tons/ha",
            "confidence": self.confidence_pct,
            "sacks_per_ha": sacks_per_ha,
            "total_tons": total_tons,
            "total_sacks": total_sacks,
            "harvest_date": self.harvest_date.strftime("%b %d, %Y"),
            "yield_readiness": self.yield_readiness,
            "readiness_display": self._format_readiness(self.yield_readiness),
        }
    
    def _format_readiness(self, readiness: str) -> str:
        """Format readiness stage for display."""
        mapping = {
            'early': '🌱 Early Stage (Vegetative)',
            'vegetative': '🌿 Vegetative Growth',
            'reproductive': '🌾 Reproductive Stage',
            'ripening': '🌾 Ripening',
            'harvest_ready': '✅ Harvest Ready',
        }
        return mapping.get(readiness, readiness)


def _slugify(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", label.lower()).strip("_")


def _pretty_label(label: str) -> str:
    slug = _slugify(label)
    if slug in LABEL_DISPLAY_OVERRIDES:
        return LABEL_DISPLAY_OVERRIDES[slug]
    return re.sub(r"[_]+", " ", label).title()


def _load_class_labels() -> Sequence[str]:
    global _CLASS_LABELS
    if _CLASS_LABELS is None:
        with _CLASS_LABELS_LOCK:
            if _CLASS_LABELS is None:
                class_map = MODELS_DIR / "class_names.json"
                if not class_map.exists():
                    raise FileNotFoundError(
                        "The disease label file (class_names.json) is missing. "
                        "Please contact your administrator to restore the model files."
                    )
                with class_map.open("r", encoding="utf-8") as fp:
                    data = json.load(fp)
                if isinstance(data, dict) and "labels" in data:
                    labels = data["labels"]
                elif isinstance(data, list):
                    labels = data
                else:
                    labels = [label for _, label in sorted((int(k), v) for k, v in data.items())]
                _CLASS_LABELS = list(labels)
    assert _CLASS_LABELS is not None
    return _CLASS_LABELS


def list_detection_classes() -> Sequence[str]:
    """Return all ML detection class names (diseases + Healthy) from class_names.json."""
    try:
        return tuple(_pretty_label(label) for label in _load_class_labels())
    except FileNotFoundError:
        train_dir = DATASET_DIR / "train"
        if not train_dir.exists():
            return ("Diseased", "Healthy")
        labels = sorted(p.name for p in train_dir.iterdir() if p.is_dir())
        return tuple(_pretty_label(lbl) for lbl in labels) or ("Diseased", "Healthy")


def _ensure_tflite_interpreter() -> Tuple[tf.lite.Interpreter, List[Dict[str, Any]], List[Dict[str, Any]]]:  # type: ignore
    if tf is None:
        raise RuntimeError(
            "The AI scanning engine is unavailable. "
            "TensorFlow is not installed on this server. "
            "Please contact your administrator."
        )

    global _INTERPRETER, _INPUT_DETAILS, _OUTPUT_DETAILS
    if _INTERPRETER is None:
        with _INTERPRETER_LOCK:
            if _INTERPRETER is None:
                model_path = MODELS_DIR / "agriscan.tflite"
                if not model_path.exists():
                    raise FileNotFoundError(
                        "The disease detection model (agriscan.tflite) is missing. "
                        "Check the file or name of tflite model in the models directory."
                        "Please contact your administrator to restore the model file."
                    )
                interpreter = tf.lite.Interpreter(model_path=str(model_path))
                interpreter.allocate_tensors()
                _INTERPRETER = interpreter
                _INPUT_DETAILS = interpreter.get_input_details()
                _OUTPUT_DETAILS = interpreter.get_output_details()
    assert _INTERPRETER and _INPUT_DETAILS and _OUTPUT_DETAILS
    _load_class_labels()  # ensure labels are loaded alongside interpreter
    return _INTERPRETER, _INPUT_DETAILS, _OUTPUT_DETAILS


def save_detection_image(uploaded_file) -> Tuple[Path, str]:
    """Persist an uploaded image to media storage."""
    DETECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    suffix = Path(uploaded_file.name or "scan.jpg").suffix or ".jpg"
    filename = f"{timestamp}_{uuid.uuid4().hex}{suffix}"
    destination = DETECTIONS_DIR / filename
    with destination.open("wb") as dest:
        for chunk in uploaded_file.chunks():
            dest.write(chunk)
    rel_path = Path("detections") / filename
    return destination, rel_path.as_posix()


def _severity_bucket(severity_pct: int) -> str:
    if severity_pct >= 75:
        return "Severe"
    if severity_pct >= 45:
        return "Moderate"
    if severity_pct >= 20:
        return "Mild"
    return "Minimal"


def _treatment_for(label: str, severity_pct: int) -> str:
    """Get treatment recommendation based on disease and severity.
    
    Returns formatted treatment text with sections for quick scanning.
    Falls back to DEFAULT_TREATMENTS if database lookup fails.
    """
    try:
        from django.db.models import F
        from .models import DiseaseType

        disease = DiseaseType.objects.filter(name__iexact=label).first()
        if disease:
            # Mirror get_treatment_object() selection logic (short_text-only path)
            match = (
                disease.treatments.filter(
                    severity_min__lte=severity_pct,
                    severity_max__gte=severity_pct,
                    is_active=True,
                ).order_by(
                    F('priority').desc(),      # most critical first
                    F('severity_min').desc(),  # tiebreak: narrower range
                    F('pk').desc(),            # tiebreak: latest added
                ).first()
                or disease.treatments.filter(is_active=True).order_by(
                    F('severity_min').asc(),   # closest to low end (fallback approximation)
                    F('priority').desc(),      # tiebreak: most critical
                    F('pk').desc(),            # tiebreak: latest added
                ).first()
            )
            if match:
                return match.short_text
    except (OperationalError, ProgrammingError):
        pass
    
    # Fallback to default treatments
    key = label.strip().lower()
    for name, text in DEFAULT_TREATMENTS.items():
        if name.lower() == key:
            return text
    return DEFAULT_TREATMENTS.get(
        _severity_bucket(severity_pct),
        "Monitor field conditions and retest in 48 hours.",
    )


def get_treatment_object(label: str, severity_pct: int):
    """Return the best-matching TreatmentRecommendation ORM object (or None).

    Selection logic:
    1. PRIMARY — active treatments whose severity range covers ``severity_pct``
       → tiebreak: highest priority first, then widest min (most specific upper bound)
    2. FALLBACK — no exact range match; pick the closest range by proximity
       → annotate distance = how far severity_pct is from the nearest range edge
       → among equally-close ranges, prefer higher priority
    3. None (caller should fall back to text-only display)
    """
    try:
        from django.db.models import Case, F, IntegerField, Value, When
        from .models import DiseaseType

        disease = DiseaseType.objects.filter(name__iexact=label).first()
        if disease:
            # 1. Exact range match — tiebreak: highest priority → highest pk (latest added)
            exact = (
                disease.treatments.filter(
                    severity_min__lte=severity_pct,
                    severity_max__gte=severity_pct,
                    is_active=True,
                ).order_by(
                    F('priority').desc(),      # most critical first
                    F('severity_min').desc(),  # tiebreak: narrower range
                    F('pk').desc(),            # tiebreak: latest added
                ).first()
            )
            if exact:
                return exact

            # 2. Fallback — closest range by distance to severity_pct edge
            #    distance = how far severity_pct is from the nearest range edge
            #    tiebreak: highest priority → highest pk (latest added)
            return (
                disease.treatments.filter(is_active=True)
                .annotate(
                    distance=Case(
                        When(severity_min__gt=severity_pct,
                             then=F('severity_min') - severity_pct),
                        When(severity_max__lt=severity_pct,
                             then=severity_pct - F('severity_max')),
                        default=Value(0),
                        output_field=IntegerField(),
                    )
                )
                .order_by(
                    F('distance').asc(),   # closest range edge first
                    F('priority').desc(),  # tiebreak: most critical
                    F('pk').desc(),        # tiebreak: latest added
                )
                .first()
            )
    except (OperationalError, ProgrammingError):
        pass
    return None


def get_detailed_treatment(label: str, severity_pct: int) -> dict:
    """Get comprehensive treatment information for detailed display.

    Returns the formatted dict from the best-matching TreatmentRecommendation,
    or a minimal fallback dict when no DB record exists.

    Flow:
    Detection Result (DiseaseType) -> TreatmentRecommendation (metadata)
    -> KnowledgeBaseEntry (symptoms/causes/prevention).

    Tagalog: Hindi na nagsi-duplicate ang symptoms/prevention sa TreatmentRecommendation.
    """
    obj = get_treatment_object(label, severity_pct)
    if obj is not None:
        data = obj.get_formatted_treatment()
        data['treatment_pk'] = obj.pk
        data['priority']     = obj.priority
        data['knowledge_entries'] = data.get('knowledge_entries', [])
        return data

    # Fallback — no DB TreatmentRecommendation record for this disease/severity.
    # Try to use DiseaseType.primary_knowledge if configured.
    from .models import DiseaseType

    fallback_entries = []
    disease = DiseaseType.objects.filter(name__iexact=label).first()
    if disease and getattr(disease, 'primary_knowledge', None):
        entry = disease.primary_knowledge
        fallback_entries = [{
            'name': entry.name,
            'category': entry.category,
            'description': entry.description,
            'symptoms': entry.symptoms,
            'causes': entry.causes,
            'prevention': entry.prevention,
            'pk': entry.pk,
        }]

    return {
        'short_text':          _treatment_for(label, severity_pct),
        'detailed_text':       '',
        'symptoms':            fallback_entries[0]['symptoms'] if fallback_entries else '',
        'factors_favoring':    '',
        'factors_favoring_lines': [],
        'factors_with_actions': [],
        'cultural_practices':  '',
        'chemical_control':    '',
        'preventive_measures': fallback_entries[0]['prevention'] if fallback_entries else '',
        'knowledge_entries':   fallback_entries,
        'severity_range':      f'{severity_pct}%',
        'treatment_pk':        None,
        'priority':            5,
        'severity_threshold':  70,
        'severity_high_msg':   '',
    }


def get_historical_yield_data(planting) -> dict:
    """Return historical yield data to seed yield prediction inputs.

    Returns a dict with the following keys:
      - historical_yield: average yield (tons/ha)
      - historical_production: estimated production (tons) for the current field area
      - record_count: number of HarvestRecord entries used
      - source: one of ['harvest_records_field', 'harvest_records_variety', 'variety_default']
      - season: which season was matched ('wet'/'dry') or 'any'

    Logic (in priority order):
    1) Same field + same variety + same season (last 2 years)
    2) Same field + same variety (any season, last 2 years)
    3) Same variety + same season (any field, last 2 years)
    4) Same variety (any season, last 2 years)
    5) Fallback to variety.default average yield

    Tagalog:
    - Ang wet season ay natural na mas mataas ang ani kaysa dry season.
      Kaya ang pinaka-tumpak na historical baseline ay yung same season records.
    - Kung wala pang same-season records, mag-fallback sa broader queries para
      hindi maging zero.
    """

    from datetime import timedelta
    from django.db.models import Avg

    from .models import HarvestRecord

    if not planting or not planting.field or not planting.variety:
        return {
            'historical_yield': 0.0,
            'historical_production': 0.0,
            'record_count': 0,
            'source': 'variety_default',
        }

    today = timezone.now().date()
    two_years_ago = today - timedelta(days=365 * 2)

    season = planting.season or ''

    # 1) Same field + same variety + same season (e.g. wet-wet, dry-dry)
    field_same_season_qs = HarvestRecord.objects.filter(
        planting__field=planting.field,
        planting__variety=planting.variety,
        planting__season=season,
        harvest_date__gte=two_years_ago,
    ).exclude(planting=planting)

    field_same_season_avg = field_same_season_qs.aggregate(avg=Avg('yield_tons_per_ha'))['avg']
    if field_same_season_avg is not None:
        yield_avg = float(field_same_season_avg)
        production = yield_avg * float(planting.field.area_hectares or 0)
        return {
            'historical_yield': yield_avg,
            'historical_production': production,
            'record_count': field_same_season_qs.count(),
            'source': 'harvest_records_field',
            'season': season,
        }

    # 2) Same field + same variety (any season)
    field_any_season_qs = HarvestRecord.objects.filter(
        planting__field=planting.field,
        planting__variety=planting.variety,
        harvest_date__gte=two_years_ago,
    ).exclude(planting=planting)

    field_any_season_avg = field_any_season_qs.aggregate(avg=Avg('yield_tons_per_ha'))['avg']
    if field_any_season_avg is not None:
        yield_avg = float(field_any_season_avg)
        production = yield_avg * float(planting.field.area_hectares or 0)
        return {
            'historical_yield': yield_avg,
            'historical_production': production,
            'record_count': field_any_season_qs.count(),
            'source': 'harvest_records_field',
            'season': 'any',
        }

    # 3) Same variety + same season (any field)
    variety_same_season_qs = HarvestRecord.objects.filter(
        planting__variety=planting.variety,
        planting__season=season,
        harvest_date__gte=two_years_ago,
    ).exclude(planting=planting)

    variety_same_season_avg = variety_same_season_qs.aggregate(avg=Avg('yield_tons_per_ha'))['avg']
    if variety_same_season_avg is not None:
        yield_avg = float(variety_same_season_avg)
        production = yield_avg * float(planting.field.area_hectares or 0)
        return {
            'historical_yield': yield_avg,
            'historical_production': production,
            'record_count': variety_same_season_qs.count(),
            'source': 'harvest_records_variety',
            'season': season,
        }

    # 4) Same variety (any season)
    variety_any_season_qs = HarvestRecord.objects.filter(
        planting__variety=planting.variety,
        harvest_date__gte=two_years_ago,
    ).exclude(planting=planting)

    variety_any_season_avg = variety_any_season_qs.aggregate(avg=Avg('yield_tons_per_ha'))['avg']
    if variety_any_season_avg is not None:
        yield_avg = float(variety_any_season_avg)
        production = yield_avg * float(planting.field.area_hectares or 0)
        return {
            'historical_yield': yield_avg,
            'historical_production': production,
            'record_count': variety_any_season_qs.count(),
            'source': 'harvest_records_variety',
            'season': 'any',
        }

    # Fallback: variety default - typically stored on RiceVariety
    variety_yield = getattr(planting.variety, 'average_yield_t_ha', None)
    yield_avg = float(variety_yield or 0.0)
    production = yield_avg * float(planting.field.area_hectares or 0)
    return {
        'historical_yield': yield_avg,
        'historical_production': production,
        'record_count': 0,
        'source': 'variety_default',
        'season': 'any',
    }


def _is_likely_rice_leaf(image: Image.Image) -> Tuple[bool, str]:
    """Check if image is likely a rice leaf using basic heuristics.

    Checks are ordered cheapest → most specific to fail-fast.
    All checks operate on the already-resized (224×224) RGB image that will
    be fed into the model, so thresholds are calibrated for that resolution.

    Returns:
        (is_valid, reason) - True if likely rice leaf, False with reason otherwise
    """
    arr = np.asarray(image, dtype=np.float32)  # shape (224, 224, 3), values 0-255

    # ── 1. Brightness ────────────────────────────────────────────────────────
    mean_brightness = float(np.mean(arr))
    if mean_brightness < 20:
        return False, "Image too dark - use better lighting"
    if mean_brightness > 240:
        return False, "Image overexposed - reduce brightness or avoid direct flash"

    # ── 2. Variance / uniform solid-color guard ───────────────────────────────
    if float(np.var(arr)) < 100:
        return False, "Image too uniform - ensure rice leaf is in frame"

    # ── 3. Blur detection (Laplacian variance on green channel) ───────────────
    # Sharp images have high edge-contrast; blurry ones do not.
    # The Laplacian is approximated via array-slicing (no scipy/cv2 needed).
    # Threshold is calibrated for 224×224 input — high-res source photos that
    # are downscaled naturally have lower Laplacian variance than their originals,
    # so we use a conservative threshold to avoid rejecting valid sharp images.
    green = arr[:, :, 1]
    lap = (
        green[:-2, 1:-1] + green[2:, 1:-1]
        + green[1:-1, :-2] + green[1:-1, 2:]
        - 4 * green[1:-1, 1:-1]
    )
    blur_score = float(np.var(lap))
    if blur_score < 15:  # <15 at 224×224 → severely blurry; conservative to avoid
                         # rejecting phone-camera shots that score 20–30 after resize
        return False, "Image too blurry - hold camera steady and focus on the leaf"

    # ── 4. Color-channel analysis ─────────────────────────────────────────────
    r_mean = float(np.mean(arr[:, :, 0]))
    g_mean = float(np.mean(arr[:, :, 1]))
    b_mean = float(np.mean(arr[:, :, 2]))

    # Grayscale / monochrome image — all channels nearly equal.
    # Catches B&W screenshots, grayscale camera outputs, etc.
    channel_spread = max(r_mean, g_mean, b_mean) - min(r_mean, g_mean, b_mean)
    if channel_spread < 10 and 40 < mean_brightness < 210:
        return False, "Image appears grayscale - please use a colour photo of the rice leaf"

    # Predominantly blue → likely sky, water, or blue background
    if b_mean > g_mean + 30 and b_mean > r_mean + 30:
        return False, "Image appears to be sky/water - focus on rice leaf"

    # Predominantly red with very little green → skin, brick, red cloth, etc.
    # Guard is tightened: only reject when green is substantially below red AND
    # blue is also low (avoids mis-rejecting tungro/leaf-scald with warm tones).
    if r_mean > g_mean + 50 and r_mean > b_mean + 50:
        return False, "Image appears to be non-plant material - capture a rice leaf"

    # Near-black across all channels (edge-case not caught by check 1)
    if g_mean < 25 and r_mean < 40 and b_mean < 40:
        return False, "No plant material detected - capture rice leaf"

    # ── 5. Green-content sanity check ────────────────────────────────────────
    # Rice leaves (even heavily diseased) retain *some* green dominance
    # relative to their surroundings.  This catches mid-brightness non-plant
    # scenes (soil, asphalt, concrete) where green is the weakest channel.
    if g_mean < r_mean - 20 and g_mean < b_mean - 20 and mean_brightness < 150:
        return False, "Image does not appear to contain plant material - capture rice leaf"

    return True, "OK"


def classify_leaf_image(
    image_path: Path,
    confidence_threshold: int | None = None,
    enable_validation: bool = True,
) -> LeafPrediction:
    """Classify a rice leaf image using the TFLite model.

    Args:
        image_path: Path to the image file
        confidence_threshold: Minimum confidence % to accept prediction.
            If not provided, the admin-configured value from SiteSetting is used.
        enable_validation: Whether to validate if image is likely a rice leaf (default: True)

    Returns:
        LeafPrediction with disease classification or UNKNOWN_LABEL if validation fails
    """
    if confidence_threshold is None:
        confidence_threshold = get_detection_confidence_threshold()

    interpreter, input_details, output_details = _ensure_tflite_interpreter()
    image = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
    
    # Pre-validate image before running expensive model inference
    if enable_validation:
        is_valid, reason = _is_likely_rice_leaf(image)
        if not is_valid:
            return LeafPrediction(
                label=UNKNOWN_LABEL,
                confidence_pct=0,
                severity_pct=0,
                severity_label="N/A",
                treatment=f"❌ {reason}\n\n"
                         "Please retake photo with:\n"
                         "✓ Clear rice leaf visible\n"
                         "✓ Natural daylight (avoid flash)\n"
                         "✓ Focus on disease symptoms\n"
                         "✓ Fill frame with leaf"
            )
    
    arr = np.asarray(image, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    with _INTERPRETER_LOCK:
        interpreter.set_tensor(input_details[0]["index"], arr)
        interpreter.invoke()
        output = interpreter.get_tensor(output_details[0]["index"])

    probs = output.squeeze().astype(float)
    class_labels = _load_class_labels()
    if probs.ndim == 0:
        probs = np.array([float(probs)])
    
    # Calculate entropy to detect ambiguous predictions
    # High entropy = model is uncertain between multiple classes
    probs_safe = np.clip(probs, 1e-7, 1.0)  # Avoid log(0)
    entropy = -np.sum(probs_safe * np.log(probs_safe))
    max_entropy = np.log(len(class_labels))  # Maximum possible entropy
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    best_idx = int(np.argmax(probs))
    best_prob = float(probs[best_idx])
    raw_label = class_labels[best_idx]
    
    confidence = int(round(best_prob * 100))
    
    # Multi-layered validation:
    # 1. Low confidence check
    if confidence < confidence_threshold:
        return LeafPrediction(
            label=UNKNOWN_LABEL,
            confidence_pct=confidence,
            severity_pct=0,
            severity_label="N/A",
            treatment=f"⚠️ Low confidence ({confidence}%)\n\n"
                     "Image quality too low or not a rice leaf.\n"
                     "Please retake photo with:\n"
                     "✓ Clear rice leaf in frame\n"
                     "✓ Good lighting (natural daylight)\n"
                     "✓ Focus on disease symptoms\n"
                     "✓ Avoid blurry or dark images"
        )
    
    # 2. High entropy check (model is confused between multiple classes)
    # 0.85 ceiling: a well-trained model on a clear rice leaf gives low entropy.
    # Using 0.85 (not 0.80) avoids over-rejecting edge cases like heavily diseased
    # leaves where two classes share probability — the confidence check (75%) is
    # already the primary guard against non-rice images.
    if normalized_entropy > 0.85:  # Model is very uncertain
        return LeafPrediction(
            label=UNKNOWN_LABEL,
            confidence_pct=confidence,
            severity_pct=0,
            severity_label="N/A",
            treatment="⚠️ Image ambiguous - model cannot classify confidently\n\n"
                     "Possible issues:\n"
                     "• Multiple diseases present\n"
                     "• Poor image quality\n"
                     "• Not a typical rice leaf\n\n"
                     "Please retake with clearer symptoms"
        )
    
    label = _pretty_label(raw_label)
    slug = _slugify(raw_label)
    
    if slug == "healthy":
        severity_pct = 0
    else:
        severity_pct = min(100, max(35, confidence))
    severity_label = _severity_bucket(severity_pct)
    treatment = _treatment_for(label, severity_pct)
    return LeafPrediction(label=label, confidence_pct=confidence, severity_pct=severity_pct, severity_label=severity_label, treatment=treatment)


def _get_active_model_version():
    try:
        from .models import ModelVersion

        return ModelVersion.objects.filter(is_active=True).order_by("-created_at").first()
    except (OperationalError, ProgrammingError):
        return None


def store_detection_result(prediction: LeafPrediction, image_rel_path: str, source: str = "web", planting=None, user=None):
    """Persist a detection prediction into the database.
    
    Best Practice: planting should always be provided for proper tracking.
    Field is automatically derived from planting.field relationship.
    """

    try:
        from .models import DetectionRecord, DiseaseType

        rel_path_str = str(image_rel_path)
        disease_obj = None
        if prediction.label:
            disease_obj, _ = DiseaseType.objects.get_or_create(name=prediction.label)

        # Validate: planting should be provided
        if not planting:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Detection saved without planting - field information cannot be derived. Please provide planting information.")

        detection = DetectionRecord.objects.create(
            image_path=rel_path_str,
            disease=disease_obj,
            confidence_pct=prediction.confidence_pct,
            severity_pct=prediction.severity_pct,
            treatment_text=prediction.treatment,
            model_version=_get_active_model_version(),
            source=source,
            planting=planting,
            user=user,
        )
        return detection
    except (OperationalError, ProgrammingError):
        # Database might not be ready (e.g. during migrations); ignore silently
        return None


def _ensure_yield_model():
    if joblib is None:
        raise RuntimeError("joblib is required to load the yield model. Install scikit-learn/joblib to continue.")

    global _YIELD_MODEL
    if _YIELD_MODEL is None:
        with _YIELD_MODEL_LOCK:
            if _YIELD_MODEL is None:
                model_path = MODELS_DIR / "yield_model.joblib"
                if not model_path.exists():
                    raise FileNotFoundError(f"Missing yield model at {model_path}")
                _YIELD_MODEL = joblib.load(model_path)
    return _YIELD_MODEL


def _load_yield_report() -> Dict[str, Any]:
    global _YIELD_REPORT
    if _YIELD_REPORT is None:
        report_path = MODELS_DIR / "yield_report.json"
        if report_path.exists():
            with report_path.open("r", encoding="utf-8") as f:
                _YIELD_REPORT = json.load(f)
        else:
            _YIELD_REPORT = {}
    return _YIELD_REPORT


def _build_rice_yield_cnn(torch_mod):
    nn = torch_mod.nn

    class RiceYieldCNN(nn.Module):
        def __init__(self):
            super().__init__()

            self.conv_1 = nn.Conv2d(3, 45, (3, 3), stride=(1, 1), padding=(1, 1))
            self.pool_1 = nn.AvgPool2d((2, 1), stride=(2, 1))
            self.norm_1 = nn.BatchNorm2d(45)
            self.act_1 = nn.ReLU()
            self.conv_2 = nn.Conv2d(45, 25, (3, 3), stride=(1, 1), padding=(1, 1))
            self.norm_2 = nn.BatchNorm2d(25)
            self.act_2 = nn.LeakyReLU(0.1)
            self.pool_2 = nn.MaxPool2d((2, 2), stride=(2, 2))

            self.conv_3 = nn.Conv2d(25, 50, (3, 3), stride=(1, 1), padding=(1, 1))
            self.norm_3 = nn.BatchNorm2d(50)
            self.pool_3 = nn.AvgPool2d((2, 3), stride=(2, 3))
            self.norm_4 = nn.BatchNorm2d(50)
            self.act_3 = nn.ReLU()
            self.pool_4 = nn.MaxPool2d((3, 3), stride=(3, 3))

            self.conv_4 = nn.Conv2d(25, 25, (3, 3), stride=(1, 1), padding=(1, 1))
            self.norm_5 = nn.BatchNorm2d(25)
            self.pool_5 = nn.AvgPool2d((2, 3), stride=(2, 3))
            self.norm_6 = nn.BatchNorm2d(25)
            self.act_4 = nn.ReLU()
            self.pool_6 = nn.MaxPool2d((3, 3), stride=(3, 3))

            self.conv_5 = nn.Conv2d(50, 16, (1, 1), stride=(1, 1), padding=(1, 1))
            self.norm_7 = nn.BatchNorm2d(16)
            self.act_5 = nn.ELU(1.0)

            self.conv_6 = nn.Conv2d(75, 16, (1, 1), stride=(1, 1), padding=(1, 1))
            self.norm_8 = nn.BatchNorm2d(16)
            self.act_6 = nn.ELU(1.0)

            self.conv_7 = nn.Conv2d(16, 16, (3, 3), stride=(1, 1), padding=(1, 1))
            self.pool_7 = nn.AvgPool2d((2, 2), stride=(2, 2))
            self.norm_9 = nn.BatchNorm2d(16)
            self.act_7 = nn.ReLU()

            self.conv_8 = nn.Conv2d(16, 16, (3, 3), stride=(1, 1), padding=(1, 1))
            self.norm_10 = nn.BatchNorm2d(16)
            self.act_8 = nn.ReLU()
            self.conv_9 = nn.Conv2d(16, 16, (3, 3), stride=(1, 1), padding=(1, 1))
            self.pool_8 = nn.AvgPool2d((2, 2), stride=(2, 2))
            self.norm_11 = nn.BatchNorm2d(16)

            self.flat = nn.Flatten()
            self.fc = nn.Linear(2640, 1)
            self.act_9 = nn.ReLU()

        def forward(self, x):
            x = self.conv_1(x)
            x = self.pool_1(x)
            x = self.norm_1(x)
            x = self.act_1(x)
            x = self.conv_2(x)
            x = self.norm_2(x)
            x = self.act_2(x)
            x = self.pool_2(x)

            x_1 = x.clone()
            x_1 = self.conv_3(x_1)
            x_1 = self.norm_3(x_1)
            x_1 = self.pool_3(x_1)
            x_1 = self.norm_4(x_1)
            x_1 = self.act_3(x_1)
            x_1 = self.pool_4(x_1)

            x_2 = x.clone()
            x_2 = self.conv_4(x_2)
            x_2 = self.norm_5(x_2)
            x_2 = self.pool_5(x_2)
            x_2 = self.norm_6(x_2)
            x_2 = self.act_4(x_2)
            x_2 = self.pool_6(x_2)

            x_3 = self.conv_5(x_1)
            x_3 = self.norm_7(x_3)
            x_3 = self.act_5(x_3)

            x_4 = torch_mod.cat([x_1, x_2], dim=1)
            x_4 = self.conv_6(x_4)
            x_4 = self.norm_8(x_4)
            x_4 = self.act_6(x_4)

            x_5 = torch_mod.mul(x_3, x_4)
            x_5 = self.conv_7(x_5)
            x_5 = self.pool_7(x_5)
            x_5 = self.norm_9(x_5)
            x_5 = self.act_7(x_5)

            x_6 = self.conv_8(x_4)
            x_6 = self.norm_10(x_6)
            x_6 = self.act_8(x_6)
            x_6 = self.conv_9(x_6)
            x_6 = self.pool_8(x_6)
            x_6 = self.norm_11(x_6)

            x_m = torch_mod.add(x_5, x_6)
            x_m = self.flat(x_m)
            x_m = self.fc(x_m)
            return self.act_9(x_m)

    return RiceYieldCNN()


def _ensure_yield_cnn_model():
    global _TORCH
    if _TORCH is None:
        try:
            torch_mod = importlib.import_module("torch")
        except Exception as exc:  # pragma: no cover - runtime dependency
            raise RuntimeError(
                "PyTorch is required for CNN yield prediction. Please install torch/torchvision."
            ) from exc
        _TORCH = torch_mod

    torch = _TORCH

    checkpoint_path = Path(getattr(settings, "YIELD_CNN_CHECKPOINT_PATH", MODELS_DIR / "rice_yield_CNN.pth"))
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Missing CNN checkpoint at {checkpoint_path}")

    global _YIELD_CNN_MODEL, _YIELD_CNN_DEVICE
    if _YIELD_CNN_MODEL is None:
        with _YIELD_CNN_LOCK:
            if _YIELD_CNN_MODEL is None:
                requested_device = str(getattr(settings, "YIELD_CNN_DEVICE", "cpu")).lower()
                if requested_device.startswith("cuda") and torch.cuda.is_available():
                    device = torch.device(requested_device)
                else:
                    device = torch.device("cpu")

                model = _build_rice_yield_cnn(torch)
                checkpoint = torch.load(str(checkpoint_path), map_location=device)
                state_dict = checkpoint.get("state_dict", checkpoint)
                model.load_state_dict(state_dict, strict=True)
                model.to(device)
                model.eval()

                _YIELD_CNN_MODEL = model
                _YIELD_CNN_DEVICE = device
    return _YIELD_CNN_MODEL, _YIELD_CNN_DEVICE


def _predict_yield_cnn_tons_per_ha(image_file: Any) -> float:
    if image_file is None:
        raise ValueError("Canopy image is required for CNN yield prediction.")

    _validate_cnn_canopy_image(image_file)

    model, device = _ensure_yield_cnn_model()
    torch = _TORCH

    # Tagalog: I-match ang preprocess sa reference implementation (512x512, mean/std=0.5).
    img = Image.open(image_file).convert("RGB").resize((512, 512))
    arr = np.asarray(img).astype(np.float32) / 255.0
    arr = (arr - np.float32(0.5)) / np.float32(0.5)
    arr = arr.transpose(2, 0, 1)

    tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0).to(device)
    with torch.no_grad():
        pred_gpm2 = float(model(tensor).squeeze().detach().cpu().numpy())

    # g/m^2 to t/ha conversion.
    return pred_gpm2 / 100.0


def _validate_cnn_canopy_image(image_file: Any) -> None:
    # Tagalog: Basic quality gate para iwas noisy/bad predictions sa sobrang dilim, silaw, o malabong larawan.
    try:
        if hasattr(image_file, "seek"):
            image_file.seek(0)
        img = Image.open(image_file).convert("RGB")
        arr = np.asarray(img).astype(np.float32)
        gray = arr.mean(axis=2)

        brightness = float(gray.mean())
        contrast = float(gray.std())
        # Lightweight sharpness proxy using neighboring pixel differences.
        sharpness = float(np.var(np.diff(gray, axis=0)) + np.var(np.diff(gray, axis=1)))

        if hasattr(image_file, "seek"):
            image_file.seek(0)

        if brightness < 35:
            raise ValueError("Canopy image is too dark for reliable CNN prediction. Please retake in better light.")
        if brightness > 230:
            raise ValueError("Canopy image is overexposed for reliable CNN prediction. Please avoid direct glare.")
        if contrast < 15:
            raise ValueError("Canopy image has very low contrast. Please retake with clearer canopy texture.")
        if sharpness < 20:
            raise ValueError("Canopy image appears blurry. Please retake with stable focus.")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Unable to process canopy image for CNN quality checks.") from exc


def _resolve_harvest_and_readiness(planting_date, growth_days: int) -> Tuple[datetime, str]:
    if planting_date is None:
        planting_date = datetime.now().date()

    harvest_date = planting_date + timedelta(days=growth_days)
    harvest_datetime = datetime.combine(harvest_date, datetime.min.time(), tzinfo=dt_timezone.utc)

    days_since_planting = (datetime.now().date() - planting_date).days
    progress_pct = (days_since_planting / growth_days) * 100 if growth_days > 0 else 0

    if progress_pct < 40:
        readiness = 'early'
    elif progress_pct < 65:
        readiness = 'vegetative'
    elif progress_pct < 85:
        readiness = 'reproductive'
    elif progress_pct < 100:
        readiness = 'ripening'
    else:
        readiness = 'harvest_ready'
    return harvest_datetime, readiness


def _normalize_yield_model_version(selected_model: str) -> str:
    if selected_model == "cnn_yield":
        return "RiceYieldCNN_v1.0"
    return "LinearRegression_v2.0"


def _parse_health_value(value: Any) -> float:
    if value is None:
        return float("nan")
    text = str(value).strip().lower()
    mapping = {
        "healthy": 0.0,
        "none": 0.0,
        "good": 0.0,
        "moderate": 0.5,
        "medium": 0.5,
        "diseased": 1.0,
        "sick": 1.0,
        "bad": 1.0,
    }
    if text in mapping:
        return mapping[text]
    try:
        return float(text)
    except ValueError:
        return float("nan")


def predict_yield(
    features: Dict[str, Any],
    detection=None,
    override_with_detection: bool = True,
    selected_model: str = "linear_regression",
    canopy_image: Any = None,
) -> YieldPredictionResult:
    """
    Predict rice yield from features using the new model structure.
    
    BEST PRACTICE: Pass detection record to auto-fill data from disease detection.
    
    Required Args in features dict:
        - variety (str): Rice variety code
        - field_area_ha (float): Field area in hectares
        - historical_production_tons (float): Previous harvest total
        - historical_yield_tons_per_ha (float): Previous yield per hectare
        - planting_date (date|str): Planting date
        - average_growth_duration_days (int): Growth duration
    
    Optional Args in features dict (enhance accuracy):
        - health_status (float): 0.0=healthy, 1.0=diseased
    
    Args:
        detection (DetectionRecord, optional): If provided, will use detection data
            to automatically determine health status and link to planting record.
        override_with_detection (bool): When True (default), detection.planting data
            overrides the supplied features.  Set to False when the caller has already
            manually filled features and wants detection used ONLY for health_status.
    
    Returns:
        YieldPredictionResult with predicted yield values and readiness
    """
    # Ensure ecosystem_type is always present (it is used as a categorical feature)
    features.setdefault('ecosystem_type', '')

    # If detection is provided, use its data (BEST PRACTICE)
    if detection is not None:
        planting = detection.planting
        if planting and override_with_detection:
            # Override with detection's planting data
            features = features.copy()  # Don't modify original
            if planting.variety:
                features["variety"] = planting.variety.code
            if planting.field:
                features["field_area_ha"] = float(planting.field.area_hectares)
                features["ecosystem_type"] = planting.field.ecosystem_type or ""
                # Tagalog: Isama ang season (wet/dry) mula sa planting record.
                # Ang season ay mahalagang categorical feature para sa model.
                if planting.season:
                    features["season"] = planting.season
            if planting.planting_date:
                features["planting_date"] = planting.planting_date
            if planting.average_growth_duration_days:
                features["average_growth_duration_days"] = planting.average_growth_duration_days
            
            # Historical data is now sourced from HarvestRecord history (last 2 years),
            # not from legacy PlantingRecord fields.
            from .services import get_historical_yield_data
            hist = get_historical_yield_data(planting)
            features["historical_production_tons"] = float(hist.get("historical_production") or 0.0)
            features["historical_yield_tons_per_ha"] = float(hist.get("historical_yield") or 0.0)
        
        # Always use detection severity as health value (regardless of override flag)
        if detection.severity_pct is not None:
            features["health_status"] = detection.severity_pct / 100.0
        elif detection.disease:
            features["health_status"] = 0.5  # Has disease = moderate
        else:
            features["health_status"] = 0.0  # No disease = healthy

    planting_date = features.get("planting_date")
    if isinstance(planting_date, str):
        try:
            planting_date = datetime.fromisoformat(planting_date).date()
        except Exception:
            planting_date = None

    # Ensure robust numeric conversion (NaN from pandas can break int())
    growth_days = features.get("average_growth_duration_days")
    if pd is not None and pd.isna(growth_days):
        growth_days = None

    try:
        growth_days = int(growth_days)
    except Exception:
        growth_days = 120  # fallback default

    area = float(features.get("field_area_ha", 0.0))
    if area <= 0:
        raise ValueError("Field area must be greater than 0.")

    harvest_datetime, yield_readiness = _resolve_harvest_and_readiness(planting_date, growth_days)

    if selected_model == "cnn_yield":
        if not get_yield_cnn_enabled():
            raise RuntimeError("CNN yield model is currently disabled by system settings.")
        tons_per_ha = _predict_yield_cnn_tons_per_ha(canopy_image)
        confidence_pct = 70
    else:
        model = _ensure_yield_model()
        report = _load_yield_report()

        if pd is None:
            raise RuntimeError("pandas is required to prepare features for the yield model. Install pandas to continue.")

        planting_month = 1
        if planting_date:
            planting_month = int(getattr(planting_date, 'month', 1))

        seed_rate = features.get("seed_rate_kg_per_ha")
        try:
            seed_rate_val = float(seed_rate) if seed_rate is not None else np.nan
        except Exception:
            seed_rate_val = np.nan

        row = {
            "variety": features["variety"],
            "field_area_ha": area,
            "historical_production_tons": float(features.get("historical_production_tons", 0.0)),
            "historical_yield_tons_per_ha": float(features.get("historical_yield_tons_per_ha", 0.0)),
            "planting_month": planting_month,
            "average_growth_duration_days": growth_days,
            "ecosystem_type": str(features.get("ecosystem_type", "")),
            "season": str(features.get("season", "")),
            "seed_rate_kg_per_ha": seed_rate_val,
            "health_status": _parse_health_value(features.get("health_status", 0.0)),
        }

        df = pd.DataFrame([row])
        tons_per_ha = float(model.predict(df)[0])

        r2 = report.get("r2", 0.65)
        if pd is not None and pd.isna(r2):
            r2 = 0.0
        else:
            r2 = float(r2)

        base_confidence = max(55, min(95, int(round(r2 * 100))))
        has_historical = (
            row.get("historical_production_tons", 0.0) > 0
            or row.get("historical_yield_tons_per_ha", 0.0) > 0
        )
        confidence_pct = base_confidence if has_historical else min(base_confidence, 70)

    total_tons = tons_per_ha * area
    sacks_per_ha = tons_per_ha * 20
    total_sacks = total_tons * 20

    return YieldPredictionResult(
        tons_per_ha=tons_per_ha,
        total_tons=total_tons,
        confidence_pct=confidence_pct,
        harvest_date=harvest_datetime,
        yield_readiness=yield_readiness,
        sacks_per_ha=sacks_per_ha,
        total_sacks=total_sacks,
    )


def store_yield_prediction(
    result: YieldPredictionResult,
    form_data: Dict[str, Any],
    detection=None,
    planting=None,
    model_version: str = "linear_regression",
):
    """
    Persist yield prediction output to the database.

    Args:
        result:     YieldPredictionResult from predict_yield()
        form_data:  form.cleaned_data dict from the view
        detection:  DetectionRecord linked to this prediction (optional)
        planting:   PlantingRecord to link explicitly (optional).
                    Priority order: explicit planting arg → detection.planting
                    → form_data["planting"].  This ensures the planting is
                    always saved even when the view used manual entry fields
                    after auto-filling from a planting record.
    """

    try:
        from .models import YieldPrediction

        tons_per_ha = Decimal(str(result.tons_per_ha)).quantize(Decimal("0.01"))
        confidence = Decimal(str(result.confidence_pct)).quantize(Decimal("0.01"))
        total_tons = Decimal(str(result.total_tons)).quantize(Decimal("0.01"))
        
        # Legacy conversions
        sacks = Decimal(str(result.sacks_per_ha)).quantize(Decimal("0.01"))
        total_sacks = Decimal(str(result.total_sacks)).quantize(Decimal("0.01"))

        # Resolve planting: explicit arg → detection.planting → form_data["planting"]
        resolved_planting = (
            planting
            or (detection.planting if detection else None)
            or form_data.get("planting")
        )
        
        # Get area from planting if available
        area_dec = None
        if resolved_planting and resolved_planting.field:
            area_dec = resolved_planting.field.area_hectares
        elif form_data.get("area"):
            area = form_data.get("area")
            area_dec = Decimal(str(area)).quantize(Decimal("0.01"))

        # Build model metadata
        meta_segments = [
            f"variety={form_data.get('variety', 'unknown')}",
            f"readiness={result.yield_readiness}",
            f"model={model_version}",
        ]
        if form_data.get('season'):
            meta_segments.append(f"season={form_data.get('season')}")
        meta = ";".join(filter(None, meta_segments))

        record = YieldPrediction.objects.create(
            planting=resolved_planting,
            detection=detection,
            predicted_yield_tons_per_ha=tons_per_ha,
            predicted_total_production_tons=total_tons,
            confidence_pct=confidence,
            model_version=_normalize_yield_model_version(model_version),
            yield_readiness=result.yield_readiness,
            estimated_harvest_date=result.harvest_date.date(),
            # Legacy fields for backward compatibility
            predicted_sacks_per_ha=sacks,
            area_hectares=area_dec,
            total_sacks=total_sacks,
            total_tons=total_tons,
            harvest_date=result.harvest_date.date(),
            model_meta=meta[:120],
        )
        return record
    except (OperationalError, ProgrammingError):
        return None


def delete_detection_image(image_rel_path: str) -> None:
    if not image_rel_path:
        return
    rel = Path(str(image_rel_path).lstrip("/"))
    path = rel if rel.is_absolute() else Path(settings.MEDIA_ROOT) / rel
    try:
        if path.exists():
            path.unlink()
    except OSError:
        pass


def get_variety_choices() -> Sequence[Tuple[str, str]]:
    try:
        from .models import RiceVariety

        varieties = [
            (v.code, f"{v.code} - {v.name}" if v.name else v.code)
            for v in RiceVariety.objects.filter(is_active=True).order_by("code")
        ]
        if varieties:
            return varieties
    except (OperationalError, ProgrammingError):
        pass

    sample_csv = DATASET_DIR / "yield_sample.csv"
    if sample_csv.exists() and pd is not None:
        series = pd.read_csv(sample_csv).get("variety")
        if series is not None:
            cleaned = sorted({str(val).strip() for val in series.dropna() if str(val).strip()})
            if cleaned:
                return [(val, val) for val in cleaned]
    return DEFAULT_VARIETIES


def get_last_detection_time() -> Optional[datetime]:
    if not DETECTIONS_DIR.exists():
        return None
    latest: Optional[Path] = None
    for path in DETECTIONS_DIR.glob("*"):
        if path.is_file() and (latest is None or path.stat().st_mtime > latest.stat().st_mtime):
            latest = path
    if latest:
        return datetime.fromtimestamp(latest.stat().st_mtime, tz=dt_timezone.utc)
    return None


def get_model_version_label() -> str:
    try:
        from .models import ModelVersion

        active = ModelVersion.objects.filter(is_active=True).order_by("-created_at").first()
        if active:
            return active.version
    except (OperationalError, ProgrammingError):
        pass

    default_model = MODELS_DIR / "agriscan.tflite"
    if default_model.exists():
        ts = datetime.fromtimestamp(default_model.stat().st_mtime, tz=dt_timezone.utc)
        return f"tflite-{ts.strftime('%Y%m%d')}"
    return "N/A"


def get_tip_of_the_day() -> str:
    if not DEFAULT_TIPS:
        return ""
    index = timezone.now().toordinal() % len(DEFAULT_TIPS)
    return DEFAULT_TIPS[index]


def dashboard_metrics(user_profile=None, role='farmer') -> Dict[str, Any]:
    from django.db.models import Avg, Count, Q

    labels = list_detection_classes()
    last_detection = get_last_detection_time()
    detections_count = 0
    yield_count = 0
    healthy_count = 0
    diseased_count = 0
    harvest_ready_count = 0
    still_growing_count = 0
    active_fields = 0
    active_plantings = 0
    knowledge_count = 0
    varieties_count = 0
    avg_yield_by_barangay = []
    avg_yield_by_field = []
    variety_trend = []
    knowledge_trend = []
    severity_distribution = []

    # UNKNOWN_LABEL constant — must match services.py top-level
    _UNKNOWN = UNKNOWN_LABEL  # "Unknown/Not Rice"

    try:
        from .models import DetectionRecord, YieldPrediction, Field, PlantingRecord, SeasonLog, KnowledgeBaseEntry, RiceVariety

        # Role-based filtering
        # Admin/Technician: See ALL data
        # Farmer: See only OWN data
        if user_profile and role == 'farmer':
            detections_qs = DetectionRecord.objects.filter(user=user_profile, is_active=True)
            yield_qs = YieldPrediction.objects.filter(planting__field__owner=user_profile, is_active=True)
            fields_qs = Field.objects.filter(owner=user_profile, is_active=True)
            plantings_qs = PlantingRecord.objects.filter(field__owner=user_profile, is_active=True)
        else:
            # Admin/Technician: System-wide stats (active only)
            detections_qs = DetectionRecord.objects.filter(is_active=True)
            yield_qs = YieldPrediction.objects.filter(is_active=True)
            fields_qs = Field.objects.filter(is_active=True)
            plantings_qs = PlantingRecord.objects.filter(is_active=True)

        # Exclude model-rejected / unclassified scans from all dashboard counts
        classified_qs = detections_qs.exclude(
            Q(disease__isnull=True) |
            Q(disease__name__iexact=_UNKNOWN) |
            Q(disease__name__iexact='Unknown')
        )

        detections_count = classified_qs.count()
        yield_count = yield_qs.count()
        active_fields = fields_qs.count()
        active_plantings = plantings_qs.count()

        # Knowledge base counts (Agri Knowledge)
        if user_profile and role == 'farmer':
            knowledge_count = KnowledgeBaseEntry.objects.filter(is_active=True, is_published=True).count()
        else:
            knowledge_count = KnowledgeBaseEntry.objects.filter(is_active=True).count()

        # Crop variety / rice variety count
        varieties_count = RiceVariety.objects.filter(is_active=True).count()

        # Healthy = disease name contains "healthy" (case-insensitive), from classified only
        healthy_count = classified_qs.filter(disease__name__icontains='healthy').count()
        diseased_count = classified_qs.exclude(disease__name__icontains='healthy').count()

        try:
            harvest_ready_count = yield_qs.filter(yield_readiness='harvest_ready').count()
            still_growing_count = yield_qs.exclude(yield_readiness='harvest_ready').count()
        except (OperationalError, ProgrammingError):
            pass
        
        # Calculate average yield per barangay
        # Group by barangay and calculate average estimated yield
        barangay_yields = (
            yield_qs
            .filter(
                planting__field__barangay__isnull=False,
                predicted_yield_tons_per_ha__isnull=False
            )
            .exclude(planting__field__barangay='')
            .exclude(planting__field__barangay='None')  # Exclude string "None"
            .values('planting__field__barangay')
            .annotate(
                avg_yield=Avg('predicted_yield_tons_per_ha'),
                count=Count('id')
            )
            .order_by('-avg_yield')[:10]  # Top 10 barangays
        )
        avg_yield_by_barangay = list(barangay_yields)
        
        # Calculate average yield per field
        field_yields = (
            yield_qs
            .filter(
                planting__field__name__isnull=False,
                predicted_yield_tons_per_ha__isnull=False
            )
            .exclude(planting__field__name='')
            .values('planting__field__name', 'planting__field__id')
            .annotate(
                avg_yield=Avg('predicted_yield_tons_per_ha'),
                count=Count('id')
            )
            .order_by('-avg_yield')[:10]  # Top 10 fields
        )
        avg_yield_by_field = list(field_yields)

        # Variety trend (top varieties by plantings)
        variety_qs = PlantingRecord.objects.filter(is_active=True, variety__isnull=False, variety__is_active=True)
        if user_profile and role == 'farmer':
            variety_qs = variety_qs.filter(field__owner=user_profile)

        variety_trend = (
            variety_qs
            .values('variety__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        variety_trend = list(variety_trend)

        # Knowledge view trend (top viewed entries)
        if user_profile and role == 'farmer':
            knowledge_qs = KnowledgeBaseEntry.objects.filter(is_active=True, is_published=True)
        else:
            knowledge_qs = KnowledgeBaseEntry.objects.filter(is_active=True)

        knowledge_trend = (
            knowledge_qs
            .values('name', 'view_count')
            .order_by('-view_count')[:10]
        )
        knowledge_trend = list(knowledge_trend)
        
        # Severity distribution — use classified_qs so rejected scans don't skew ranges
        severity_ranges = [
            {'label': 'Low (0-25%)', 'min': 0, 'max': 25},
            {'label': 'Moderate (26-50%)', 'min': 26, 'max': 50},
            {'label': 'High (51-75%)', 'min': 51, 'max': 75},
            {'label': 'Severe (76-100%)', 'min': 76, 'max': 100},
        ]

        for severity_range in severity_ranges:
            count = classified_qs.filter(
                severity_pct__gte=severity_range['min'],
                severity_pct__lte=severity_range['max']
            ).count()
            severity_distribution.append({
                'label': severity_range['label'],
                'count': count
            })

    except (OperationalError, ProgrammingError):
        pass

    health_percentage = round((healthy_count / detections_count * 100) if detections_count > 0 else 0, 1)
    diseased_percentage = round(100 - health_percentage, 1)

    return {
        "detectable_classes": len(labels),
        "model_version": get_model_version_label(),
        "last_sync": timezone.localtime(last_detection).strftime("%b %d, %Y %I:%M %p") if last_detection else None,
        "tip": get_tip_of_the_day(),
        "detections_count": detections_count,
        "yield_count": yield_count,
        "healthy_count": healthy_count,
        "diseased_count": diseased_count,
        "harvest_ready_count": harvest_ready_count,
        "still_growing_count": still_growing_count,
        "health_percentage": health_percentage,
        "diseased_percentage": diseased_percentage,
        "active_fields": active_fields,
        "active_plantings": active_plantings,
        "knowledge_count": knowledge_count,
        "varieties_count": varieties_count,
        "avg_yield_by_barangay": avg_yield_by_barangay,
        "avg_yield_by_field": avg_yield_by_field,
        "variety_trend": variety_trend,
        "knowledge_trend": knowledge_trend,
        "severity_distribution": severity_distribution,
    }


# ============================================================================
# ANNOUNCEMENT SYSTEM (Local - No Internet Required)
# ============================================================================

def get_user_announcements(user_profile, limit=None, unread_only=False):
    """Get announcements visible to a specific user (NO INTERNET REQUIRED).
    
    Args:
        user_profile: Profile instance
        limit: Max number of announcements to return (None = all)
        unread_only: If True, only return unread announcements
    
    Returns:
        QuerySet of Announcement objects with is_read annotation
    """
    from django.db.models import Q, Exists, OuterRef
    from django.utils import timezone
    from .models import Announcement, UserNotification
    
    now = timezone.now()
    
    # Base query: active, not deleted, visible announcements
    announcements = Announcement.objects.filter(
        is_active=True,
        is_deleted=False,
    ).filter(
        Q(published_at__isnull=True) | Q(published_at__lte=now)
    ).filter(
        Q(expires_at__isnull=True) | Q(expires_at__gte=now)
    )
    
    # Filter by target audience
    if user_profile.role == 'farmer':
        announcements = announcements.filter(
            Q(target_audience='all') |
            Q(target_audience='farmers') |
            (Q(target_audience='barangay') & 
             Q(target_barangay__in=user_profile.fields.values_list('barangay', flat=True))) |
            Q(target_user=user_profile)
        )
    elif user_profile.role == 'technician':
        announcements = announcements.filter(
            Q(target_audience='all') |
            Q(target_audience='technicians') |
            Q(target_user=user_profile)
        )
    # Admin sees everything (no filter needed)
    
    # Annotate with read status
    announcements = announcements.annotate(
        is_read=Exists(
            UserNotification.objects.filter(
                announcement=OuterRef('pk'),
                user=user_profile,
                is_read=True
            )
        )
    )
    
    # Filter unread only if requested
    if unread_only:
        announcements = announcements.filter(is_read=False)
    
    # Order by priority then date
    announcements = announcements.order_by('-priority', '-created_at')
    
    if limit:
        announcements = announcements[:limit]
    
    return announcements


def get_unread_announcements_count(user_profile):
    """Get count of unread announcements for badge (NO INTERNET REQUIRED).
    
    Args:
        user_profile: Profile instance
    
    Returns:
        Integer count of unread announcements
    """
    return get_user_announcements(user_profile, unread_only=True).count()


def mark_announcement_as_read(announcement, user_profile):
    """Mark an announcement as read by a user (NO INTERNET REQUIRED).
    
    Args:
        announcement: Announcement instance or ID
        user_profile: Profile instance
    
    Returns:
        Tuple (UserNotification, created: bool)
    """
    from django.utils import timezone
    from .models import UserNotification, Announcement
    
    try:
        # Handle both Announcement instance and ID
        if isinstance(announcement, Announcement):
            announcement_obj = announcement
        else:
            announcement_obj = Announcement.objects.get(pk=announcement)
            
        notification, created = UserNotification.objects.get_or_create(
            user=user_profile,
            announcement=announcement_obj
        )
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        return notification, created
    except Announcement.DoesNotExist:
        return None, False


def get_announcement_stats(announcement):
    """Get statistics for an announcement (for admin analytics).
    
    Args:
        announcement: Announcement instance
    
    Returns:
        Dict with statistics
    """
    from .models import UserNotification
    
    target_users_count = announcement.get_target_users().count()
    notifications = UserNotification.objects.filter(announcement=announcement)
    read_count = notifications.filter(is_read=True).count()
    
    return {
        'target_users': target_users_count,
        'delivered': notifications.count(),
        'read': read_count,
        'read_percentage': round((read_count / target_users_count * 100) if target_users_count > 0 else 0, 1),
    }


def _emails_are_enabled() -> bool:
    """I-check kung handa ang SMTP config bago mag-send ng email.

    Flow:
    1) Kailangan naka-on ang EMAIL_ENABLED.
    2) Kailangan kumpleto ang critical SMTP fields.
    """
    if not get_email_enabled():
        return False

    required = (
        'EMAIL_HOST',
        'EMAIL_PORT',
        'EMAIL_HOST_USER',
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL',
    )
    return all(bool(getattr(settings, key, '')) for key in required)


def _app_url(path: str) -> str:
    """Bumuo ng absolute URL gamit APP_BASE_URL para env-driven ang links."""
    base = getattr(settings, 'APP_BASE_URL', 'http://127.0.0.1:8000').rstrip('/')
    return f"{base}/{path.lstrip('/')}"


def send_notification_email(notification):
    """
    Send an email alert for a system Notification (disease / yield_drop / announcement).

    Only sends if:
    - EMAIL is enabled and SMTP settings are complete
    - The recipient has an email address on their User account

    Called from signals.py after each Notification is created.
    Fails silently — email errors never break the web request.
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        # Tagalog: iwas failed sends kung kulang pa ang env SMTP config.
        if not _emails_are_enabled():
            return

        from django.core.mail import send_mail

        recipient_email = notification.recipient.user.email
        if not recipient_email:
            return

        # Build subject and body based on notification type
        type_icons = {
            'disease': '[DISEASE ALERT]',
            'yield_drop': '[YIELD DROP ALERT]',
            'advisory': '[ANNOUNCEMENT]',
            'knowledge': '[KNOWLEDGE]',
            'treatment': '[TREATMENT]',
            'system': '[SYSTEM]',
        }
        prefix = type_icons.get(notification.type, '[AgriScan+]')
        subject = f"{prefix} {notification.title}"

        body = (
            f"Hello {notification.recipient.user.get_full_name() or notification.recipient.user.username},\n\n"
            f"{notification.message}\n\n"
        )

        # Add a link to the relevant page
        if notification.type == 'disease' and notification.related_detection:
            body += f"View your detection records: {_app_url('/detections/')}\n\n"
        elif notification.type == 'yield_drop':
            body += f"View your yield records: {_app_url('/yield-records/')}\n\n"
        elif notification.type == 'advisory':
            body += f"View announcements: {_app_url('/announcements/')}\n\n"
        elif notification.type == 'knowledge':
            body += f"View the knowledge base: {_app_url('/knowledge/')}\n\n"
        elif notification.type == 'treatment':
            body += f"View treatment recommendations: {_app_url('/treatments/')}\n\n"
        elif notification.type == 'system':
            body += f"View system settings: {_app_url('/system-settings/')}\n\n"

        body += (
            f"---\n"
            f"This is an automated alert from AgriScan+.\n"
            f"Log in to view and manage your notifications: {_app_url('/notifications/')}\n"
        )

        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,
        )
        logger.info("Email sent to %s for notification type=%s", recipient_email, notification.type)

    except Exception:
        logger.exception("Failed to send email for Notification pk=%s", notification.pk)


def send_plain_email(recipient_email, subject, body):
    """
    Low-level helper — send a plain-text email to any address.

    Respects EMAIL_ENABLED + complete SMTP env config guard.
    Fails silently — never breaks the calling request.
    """
    import logging
    _logger = logging.getLogger(__name__)
    try:
        # Tagalog: isang guard lang para consistent ang behavior ng lahat ng email senders.
        if not _emails_are_enabled():
            return
        if not recipient_email:
            return
        from django.core.mail import send_mail
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=True,
        )
        _logger.info("Plain email sent to %s | subject: %s", recipient_email, subject)
    except Exception:
        _logger.exception("Failed to send plain email to %s", recipient_email)


def send_announcement_emails_to_targets(announcement):
    """
    Send bulk email to all users targeted by an Announcement.

    Resolves the target_audience field and emails every matching Profile
    that has a valid email address.  Respects EMAIL_ENABLED guard.
    Fails silently per recipient.

    Call this once right after announcement.save() in announcement_create().
    """
    import logging
    _logger = logging.getLogger(__name__)
    try:
        if not _emails_are_enabled():
            return

        from .models import Profile

        audience = announcement.target_audience

        if audience == 'all':
            profiles = Profile.objects.select_related('user').filter(user__is_active=True)
        elif audience == 'farmers':
            profiles = Profile.objects.select_related('user').filter(role='farmer', user__is_active=True)
        elif audience == 'technicians':
            profiles = Profile.objects.select_related('user').filter(role='technician', user__is_active=True)
        elif audience == 'barangay' and announcement.target_barangay:
            # Match farmers whose fields are in the target barangay
            profiles = Profile.objects.select_related('user').filter(
                role='farmer',
                user__is_active=True,
                fields__barangay__iexact=announcement.target_barangay,
            ).distinct()
        elif audience == 'user' and announcement.target_user:
            profiles = Profile.objects.select_related('user').filter(
                pk=announcement.target_user_id,
                user__is_active=True,
            )
        else:
            return  # Unknown audience — skip

        priority_labels = {
            'info':    '[INFO]',
            'advisory':'[ANNOUNCEMENT]',
            'warning': '[WARNING]',
            'urgent':  '[URGENT]',
        }
        prefix = priority_labels.get(announcement.priority, '[AgriScan+]')
        subject = f"{prefix} {announcement.title}"

        sent = 0
        for profile in profiles:
            email = profile.user.email
            if not email:
                continue
            name = profile.user.get_full_name() or profile.user.username
            body = (
                f"Hello {name},\n\n"
                f"{announcement.content}\n\n"
                f"---\n"
                f"This is an automated announcement from AgriScan+.\n"
                f"Log in to read it: {_app_url('/announcements/')}\n"
            )
            send_plain_email(email, subject, body)
            sent += 1

        _logger.info("Announcement #%s emailed to %d recipients", announcement.pk, sent)
        return sent
    except Exception:
        _logger.exception("Failed to send announcement emails for Announcement pk=%s", announcement.pk)


# FUTURE: Announcement bulk-email service (ready to use when needed)
def send_announcement_emails(announcement_id):
    """[FUTURE] Send email notifications for an announcement (REQUIRES INTERNET).
    
    Configure SMTP values in .env when ready (see .env.example):
    - EMAIL_BACKEND / EMAIL_HOST / EMAIL_PORT / EMAIL_USE_TLS
    - EMAIL_HOST_USER / EMAIL_HOST_PASSWORD
    - DEFAULT_FROM_EMAIL / EMAIL_ENABLED
    
    Args:
        announcement_id: Announcement ID
    
    Returns:
        Dict with send statistics
    """
    # Uncomment when ready to enable email
    """
    from django.core.mail import send_mass_mail
    from django.template.loader import render_to_string
    from .models import Announcement
    
    try:
        announcement = Announcement.objects.get(pk=announcement_id)
        
        if not announcement.send_email or announcement.email_sent:
            return {'status': 'skipped', 'reason': 'Email not requested or already sent'}
        
        target_users = announcement.get_target_users()
        emails = []
        
        for user in target_users:
            if user.user.email:
                subject = f"[AgriScan+] {announcement.title}"
                message = render_to_string('emails/announcement.html', {
                    'announcement': announcement,
                    'user': user,
                })
                emails.append((
                    subject, 
                    message, 
                    'noreply@agriscan.ph',  # Change to your email
                    [user.user.email]
                ))
        
        if emails:
            sent_count = send_mass_mail(emails, fail_silently=False)
            
            from django.utils import timezone
            announcement.email_sent = True
            announcement.email_sent_at = timezone.now()
            announcement.save()
            
            return {
                'status': 'success',
                'sent_count': sent_count,
                'total_targets': len(emails)
            }
        
        return {'status': 'no_emails', 'reason': 'No users have email addresses'}
        
    except Announcement.DoesNotExist:
        return {'status': 'error', 'reason': 'Announcement not found'}
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}
    """
    
    return {
        'status': 'disabled',
        'reason': 'Email integration not yet enabled. See services.py for setup instructions.'
    }

