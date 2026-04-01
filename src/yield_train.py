"""
Train a rice yield regression model using Linear Regression.

Model: Linear Regression
Language: Python (scikit-learn)
Data Sources: Django Database (recommended) OR CSV file
Output: Rice yield prediction (tons per hectare)

REQUIRED INPUTS (Core):
- field_area_ha (float): Field area in hectares
- historical_production_tons (float): Total harvested rice from previous cycles
- historical_yield_tons_per_ha (float): Computed as Production ÷ Area
- planting_date (str|date): Date when field was planted
- average_growth_duration_days (int): Days until harvest
- variety (str): Rice variety code (e.g., Rc222, Rc160, Rc216)
- ecosystem_type (str): Field ecosystem type (e.g., irrigated, rainfed)
- season (str): Planting season (wet/dry) as recorded in the database

OPTIONAL INPUTS (Enhance Accuracy):
- health_status (str/float): Disease severity from CNN detection
- seed_rate_kg_per_ha (float): Seed sowing rate in kg per hectare

TARGET VARIABLE:
- yield_tons_per_ha (float): Actual yield in tons per hectare

Output artifacts written to models/:
- yield_model.joblib         (full sklearn Pipeline with LinearRegression)
- yield_report.json          (MAE, RMSE, R² metrics)
- yield_model_meta.json      (metadata: features, target, created_at)

Examples:

  # BEST PRACTICE: Train from database (production data)
  python src/yield_train.py --from-db

  # Alternative: Train from CSV file (testing/import)
  python src/yield_train.py --csv dataset/yield_sample.csv
  
  # Custom output location
  python src/yield_train.py --from-db --out models/my_yield_model.joblib
  
  # Adjust minimum samples requirement
  python src/yield_train.py --from-db --min-samples 100
  
Why Linear Regression:
- Fast training and prediction
- Interpretable coefficients
- Works well with continuous harvest data
- Low risk of overfitting with limited data
- Standard approach in rice yield research papers
"""

from __future__ import annotations
import argparse
import json
import os
from datetime import datetime, timezone
from typing import List

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression  # Changed to Linear Regression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # Added StandardScaler for Linear Regression
from sklearn.impute import SimpleImputer


def parse_args() -> argparse.Namespace:
	p = argparse.ArgumentParser(description="Train rice yield regressor")
	
	# Data source options (mutually exclusive)
	source = p.add_mutually_exclusive_group(required=True)
	source.add_argument("--csv", help="Path to input CSV file")
	source.add_argument("--from-db", action="store_true", help="Load data directly from Django database (BEST PRACTICE)")
	
	# Output options
	p.add_argument("--outdir", default=os.path.join(os.path.dirname(__file__), '..', 'models'), help="Output directory for model artifacts (ignored if --out is a file path)")
	p.add_argument("--out", default=None, help="Optional output model file path (e.g., models/yield_model.joblib)")
	
	# Training options
	p.add_argument("--test-size", type=float, default=0.2)
	p.add_argument("--random-state", type=int, default=42)
	p.add_argument("--min-samples", type=int, default=50, help="Minimum samples required for training")
	
	return p.parse_args()


REQUIRED = [
	'variety', 'field_area_ha', 'historical_production_tons',
	'historical_yield_tons_per_ha', 'planting_date',
	'average_growth_duration_days', 'ecosystem_type', 'season',
	'yield_tons_per_ha'
]

# Optional features (enhance accuracy but not required)
OPTIONAL = [
	'health_status',
	'seed_rate_kg_per_ha',
]

RENAMES = {
	'area_ha': 'field_area_ha',
	'area': 'field_area_ha',
	'production_tons': 'historical_production_tons',
	'production': 'historical_production_tons',
	'yield_per_ha': 'historical_yield_tons_per_ha',
	'yield': 'yield_tons_per_ha',
	'growth_duration': 'average_growth_duration_days',
	'growth_days': 'average_growth_duration_days',
	'health': 'health_status',
}


def load_from_database() -> pd.DataFrame:
    """Load training data directly from Django database (BEST PRACTICE).

    IMPORTANT: Retrain the model after changing this file or the feature set.
    Run:
        python src/yield_train.py --from-db
    """

    import sys
    import django

    # Setup Django environment
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.insert(0, project_root)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()

    from polls.models import HarvestRecord, PlantingRecord, DetectionRecord
    from polls.services import get_historical_yield_data
    from django.db.models.functions import Coalesce

    print("\n📊 Loading data from database...")

    # Query HarvestRecord (actual measured yields) with related planting + variety + field
    # Only include records where planting and variety exist.
    queryset = HarvestRecord.objects.select_related(
        'planting',
        'planting__field',
        'planting__variety',
    ).filter(
        planting__isnull=False,
        planting__field__isnull=False,
        planting__variety__isnull=False,
    )

    count = queryset.count()
    print(f"   Found {count} yield records with actual harvest data")

    if count == 0:
        print("\n⚠️  No yield prediction records with actual harvest data found in database!")
        print("   Options:")
        print("   1. Use --csv with sample data")
        print("   2. Add actual harvest yields through the web app")
        print("   3. Import historical data with actual_harvest_date field")
        sys.exit(1)

    # Build DataFrame from queryset
    data = []
    skipped_missing_season = 0

    # Pre-import for performance (and clarity)
    from django.db.models import Avg
    from datetime import timedelta

    # Tagalog: Gamitin ang 'season' field mula sa PlantingRecord bilang single source of truth.
    # Kung nawawala ang season, hindi natin sasali ang record para maiwasan ang maling feature.
    for hr in queryset:
        planting = hr.planting
        field = planting.field
        variety = planting.variety

        season = getattr(planting, 'season', None)
        if not season:
            skipped_missing_season += 1
            continue

        # Core features (REQUIRED)
        # Historical data: 2-year average for this field + variety up to current harvest.
        # Use yield_tons_per_ha (not raw production) to avoid leakage from varying area sizes.
        two_years_ago = hr.harvest_date - timedelta(days=365 * 2) if hr.harvest_date else None
        hist_qs = HarvestRecord.objects.none()
        if two_years_ago and planting.field and planting.variety:
            hist_qs = HarvestRecord.objects.filter(
                planting__field=planting.field,
                planting__variety=planting.variety,
                harvest_date__lt=hr.harvest_date,
                harvest_date__gte=two_years_ago,
            )

        hist_count = hist_qs.count() if two_years_ago else 0
        if hist_count > 0:
            avg_yield = hist_qs.aggregate(avg=Avg('yield_tons_per_ha'))['avg'] or 0.0
        else:
            # Fallback to variety default yield (no past harvest history available)
            avg_yield = float(variety.average_yield_t_ha or 0.0)

        # Compute production using current field area (avoid leaking historical area changes)
        avg_prod = avg_yield * float(field.area_hectares or 0)

        row = {
            'variety': variety.code,
            'field_area_ha': float(field.area_hectares),
            'ecosystem_type': planting.field.ecosystem_type or '',
            'season': season,
            'historical_production_tons': float(avg_prod),
            'historical_yield_tons_per_ha': float(avg_yield),
            'planting_date': planting.planting_date.strftime('%Y-%m-%d'),
            'average_growth_duration_days': planting.average_growth_duration_days or 120,
            'seed_rate_kg_per_ha': float(planting.seed_rate_kg_per_ha) if planting.seed_rate_kg_per_ha is not None else np.nan,
            'yield_tons_per_ha': float(hr.yield_tons_per_ha),  # Actual yield (target)
        }

        # Get health status from most recent detection for this planting
        # (0 = healthy, 1 = severe)
        latest_detection = planting.detections.order_by('-created_at').first()
        if latest_detection and latest_detection.severity_pct is not None:
            row['health_status'] = latest_detection.severity_pct / 100.0
        else:
            row['health_status'] = 0.0  # Assume healthy if no detections

        data.append(row)

    if skipped_missing_season:
        print(f"   ⚠️ Skipped {skipped_missing_season} record(s) because planting.season was missing (season is required)")

    df = pd.DataFrame(data)
    print(f"   ✓ Loaded {len(df)} records")
    print(f"   Varieties: {df['variety'].nunique()} unique")
    print(f"   Date range: {df['planting_date'].min()} to {df['planting_date'].max()}")

    # Show optional features coverage
    optional_cols = [col for col in OPTIONAL if col in df.columns]
    if optional_cols:
        print(f"   Optional features available: {', '.join(optional_cols)}")
        for col in optional_cols:
            coverage = df[col].notna().sum() / len(df) * 100
            print(f"      - {col}: {coverage:.1f}% coverage")

    return df


def _parse_health_value(v):
    """Map health to numeric: healthy->0, moderate->0.5, diseased->1.0, else float if possible."""
    if pd.isna(v):
        return np.nan
    s = str(v).strip().lower()
    if s in {"healthy", "none", "good", "0"}:
        return 0.0
    if s in {"moderate", "medium", "0.5"}:
        return 0.5
    if s in {"diseased", "sick", "bad", "severe", "1", "1.0"}:
        return 1.0
    try:
        return float(s)
    except Exception:
        return np.nan


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
	"""Normalize column names and values."""
	# Trim/rename common variants
	df = df.rename(columns={c: c.strip() for c in df.columns})
	df = df.rename(columns=RENAMES)
	
	# Normalize health_status
	if 'health_status' in df.columns:
		df['health_status'] = df['health_status'].apply(_parse_health_value)
	
	# Normalize variety
	if 'variety' in df.columns:
		df['variety'] = df['variety'].astype(str).str.strip()

	# Normalize season and ecosystem_type (derived from PlantingRecord)
	if 'season' in df.columns:
		df['season'] = df['season'].astype(str).str.strip().str.lower()
	if 'ecosystem_type' in df.columns:
		df['ecosystem_type'] = df['ecosystem_type'].astype(str).str.strip().str.lower()

	return df


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
	# Parse planting_date to planting_month (1..12)
	def parse_date(x):
		if pd.isna(x):
			return np.nan
		for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):  # best-effort
			try:
				return datetime.strptime(str(x), fmt)
			except ValueError:
				continue
		# last resort: pandas parser
		try:
			return pd.to_datetime(x)
		except Exception:
			return pd.NaT

	dt = df['planting_date'].apply(parse_date)
	df['planting_month'] = dt.dt.month.fillna(0).astype(int)
	return df


def build_pipeline(df: pd.DataFrame) -> tuple[Pipeline, List[str], List[str]]:
	"""
	Build sklearn Pipeline with Linear Regression.
	
	Dynamically determines which features are available (core + optional).
	
	Pipeline steps:
	1. Preprocessing:
	   - Categorical features (variety, season): OneHotEncoding
	   - Numeric features: StandardScaler (important for Linear Regression!)
	2. Model: LinearRegression
	
	StandardScaler is crucial for Linear Regression because:
	- Features have different scales (e.g., area_ha vs growth_days)
	- Linear models are sensitive to feature scales
	- Improves convergence and coefficient interpretability
	"""
	# Core features (always included)
	# Tagalog: Ang ecosystem_type (irrigated/rainfed/upland/flood_prone/saline)
	# at season (wet/dry) ay nakakaapekto sa yield potential.
	categorical: List[str] = ['variety', 'ecosystem_type', 'season']
	numeric: List[str] = [
		'field_area_ha',
		'historical_production_tons',
		'historical_yield_tons_per_ha',
		'planting_month',
		'average_growth_duration_days',
	]
	
	# Add optional numeric features if available
	optional_numeric = ['health_status', 'seed_rate_kg_per_ha']
	for feat in optional_numeric:
		if feat in df.columns and df[feat].notna().any():
			numeric.append(feat)
	
	print(f"\n📋 Building pipeline with features:")
	print(f"   Categorical: {categorical}")
	print(f"   Numeric: {numeric}")

	pre = ColumnTransformer(
		transformers=[
			('cat', Pipeline(steps=[
				('imputer', SimpleImputer(strategy='most_frequent')),
				('onehot', OneHotEncoder(handle_unknown='ignore'))
			]), categorical),
			('num', Pipeline(steps=[
				('imputer', SimpleImputer(strategy='median')),
				('scaler', StandardScaler())  # Scale numeric features for Linear Regression
			]), numeric)
		]
	)

	# Linear Regression: Simple, fast, interpretable
	model = LinearRegression()
	pipe = Pipeline(steps=[('pre', pre), ('model', model)])
	return pipe, categorical, numeric


def get_feature_names(pipe: Pipeline, categorical: List[str], numeric: List[str]) -> List[str]:
	"""Get feature names after preprocessing for interpretation.

	This is used to map linear regression coefficients back to human-friendly
	feature names (including one-hot encoded categories).
	"""
	pre = pipe.named_steps['pre']

	feature_names: List[str] = []
	# Categorical features are one-hot encoded
	if categorical:
		cat_pipe = pre.named_transformers_['cat']
		ohe = cat_pipe.named_steps['onehot']
		feature_names.extend(list(ohe.get_feature_names_out(categorical)))

	# Numeric features pass through unchanged
	feature_names.extend(numeric)
	return feature_names


def main():
	args = parse_args()
	
	# Load data from either CSV or database
	if args.from_db:
		print("🗄️  Loading data from Django database (BEST PRACTICE)")
		df = load_from_database()
		data_source = "database"
	else:
		csv_path = os.path.abspath(args.csv)
		print(f"📁 Loading data from CSV: {csv_path}")
		if not os.path.isfile(csv_path):
			print(f"❌ CSV file not found: {csv_path}")
			return
		df = pd.read_csv(csv_path)
		data_source = csv_path
	
	# Normalize and validate data
	df = normalize_columns(df)

	# Ensure ecosystem_type exists even if missing in the source data
	# (required because we now train on this categorical feature)
	if 'ecosystem_type' not in df.columns:
		df['ecosystem_type'] = ''
	else:
		df['ecosystem_type'] = df['ecosystem_type'].fillna('')

	# Check minimum samples requirement
	if len(df) < args.min_samples:
		print(f"\n⚠️  WARNING: Only {len(df)} samples found (minimum recommended: {args.min_samples})")
		print(f"   Linear Regression needs 50-100+ samples for good performance")
		print(f"   Current training will likely produce poor R² score")
		
		response = input(f"\n   Continue anyway? [y/N]: ").strip().lower()
		if response != 'y':
			print("   Training cancelled. Collect more data first.")
			return

	# Resolve output paths – support either --out (file) or --outdir (dir)
	model_path: str
	if args.out:
		proposed = os.path.abspath(args.out)
		# If looks like a file (has extension), use directly; else treat as directory
		if os.path.splitext(proposed)[1]:
			model_path = proposed
			os.makedirs(os.path.dirname(model_path) or '.', exist_ok=True)
		else:
			os.makedirs(proposed, exist_ok=True)
			model_path = os.path.join(proposed, 'yield_model.joblib')
	else:
		outdir = os.path.abspath(args.outdir)
		os.makedirs(outdir, exist_ok=True)
		model_path = os.path.join(outdir, 'yield_model.joblib')

	# Validate required columns
	missing = [c for c in REQUIRED if c not in df.columns]
	if missing:
		raise SystemExit(f"Data missing required columns: {missing}")

	df = add_date_features(df)

	# Determine which features are actually available
	core_features = [
		'variety', 'ecosystem_type', 'season',
		'field_area_ha', 'historical_production_tons',
		'historical_yield_tons_per_ha', 'planting_month',
		'average_growth_duration_days',
	]
	
	# Optional features (enhance accuracy but not required)
	optional_features = []
	for feat in ['health_status', 'seed_rate_kg_per_ha']:
		if feat in df.columns and df[feat].notna().any():
			optional_features.append(feat)
	
	features = core_features + optional_features
	target = 'yield_tons_per_ha'

	X = df[features]
	y = df[target]

	X_train, X_test, y_train, y_test = train_test_split(
		X, y, test_size=args.test_size, random_state=args.random_state
	)

	# Build and fit pipeline
	pipe, categorical, numeric = build_pipeline(df)
	pipe.fit(X_train, y_train)

	# Metrics
	y_pred = pipe.predict(X_test)
	mae = float(mean_absolute_error(y_test, y_pred))
	rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
	r2 = float(r2_score(y_test, y_pred))

	# Interpretability: map coefficients to feature names
	lr_model = pipe.named_steps['model']
	feature_names = get_feature_names(pipe, categorical, numeric)
	coeff_pairs = list(zip(feature_names, lr_model.coef_))
	# Sort by absolute impact
	coeff_pairs_sorted = sorted(coeff_pairs, key=lambda x: abs(x[1]), reverse=True)

	coefficients = {
		'intercept': float(lr_model.intercept_),
		'n_features': int(len(lr_model.coef_)),
		'top_weights': [
			{'feature': name, 'weight': float(weight)}
			for name, weight in coeff_pairs_sorted[:20]
		],
	}

	report = {
		'model_type': 'Linear Regression',
		'mae': mae,
		'rmse': rmse,
		'r2': r2,
		'n_train': int(len(X_train)),
		'n_test': int(len(X_test)),
		'coefficients': coefficients,
		'features_used': features,
		'core_features': core_features,
		'optional_features': optional_features,
		'interpretation': {
			'mae_meaning': f"Predictions are off by ±{mae:.2f} tons/ha on average",
			'r2_meaning': f"Model explains {r2*100:.1f}% of yield variance",
			'model_equation': 'yield_tons_per_ha = intercept + (weights × features)',
			'units': 'tons per hectare'
		}
	}

	# Save artifacts
	joblib.dump(pipe, model_path)

	outdir = os.path.dirname(model_path)
	report_path = os.path.join(outdir, 'yield_report.json')
	with open(report_path, 'w', encoding='utf-8') as f:
		json.dump(report, f, indent=2)

	meta = {
		'created_at': datetime.now(timezone.utc).isoformat(),
		'data_source': data_source,
		'n_samples': int(len(df)),
		'model_file': model_path,
		'report_file': report_path,
		'features': features,
		'core_features': core_features,
		'optional_features': optional_features,
		'target': target,
		'target_units': 'tons/ha',
	}
	meta_path = os.path.join(outdir, 'yield_model_meta.json')
	with open(meta_path, 'w', encoding='utf-8') as f:
		json.dump(meta, f, indent=2)

	print("\n" + "="*60)
	print("✅ LINEAR REGRESSION MODEL TRAINING COMPLETE")
	print("="*60)
	print(f"\n📊 Model Performance:")
	print(f"  - MAE (Mean Absolute Error): {mae:.2f} tons/ha")
	print(f"  - RMSE (Root Mean Squared Error): {rmse:.2f} tons/ha")
	print(f"  - R² Score: {r2:.4f} ({r2*100:.1f}% variance explained)")
	print(f"\n📈 Training Data:")
	print(f"  - Training samples: {len(X_train)}")
	print(f"  - Test samples: {len(X_test)}")
	print(f"  - Core features: {', '.join(core_features)}")
	if optional_features:
		print(f"  - Optional features: {', '.join(optional_features)}")
	print(f"\n🔢 Model Equation (approx):")
	print(f"  yield_tons_per_ha = {lr_model.intercept_:.2f} + (sum(weights × features))")
	print(f"\n📌 Top feature weights (absolute value, indicative of importance):")
	for name, weight in coeff_pairs_sorted[:10]:
		print(f"  - {name}: {weight:.4f}")

	print(f"\n💡 Interpretation:")
	print(f"  - Predictions are typically ±{mae:.2f} tons/ha from actual yield")
	print(f"  - Model explains {r2*100:.1f}% of yield variation")
	print(f"  - Output unit: tons per hectare (industry standard)")
	print(f"\n📁 Saved Artifacts:")
	print(f"  - Model: {model_path}")
	print(f"  - Report: {report_path}")
	print(f"  - Metadata: {meta_path}")
	print("="*60 + "\n")


if __name__ == '__main__':
	main()

