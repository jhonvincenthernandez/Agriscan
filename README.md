# AgriScan+

Agricultural management system for rice farming with disease detection and yield prediction.

## Quick Start

```bash

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Access at: `http://127.0.0.1:8000`

## Features

- 🌾 Rice disease detection (CNN-based)
- 📊 Yield prediction
- 👥 Role-based access (Admin, Technician, Farmer)
- 📱 Mobile-friendly interface
- 📈 Dashboard analytics

## Project Structure
```bash
Python 3.8+
Django 5.2
MySQL 8.0+
```

### Setup
```bash
# Clone repository
git clone <repository-url>
cd AgriScan/mysite



# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Environment Configuration
```env
# Add to settings.py or .env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://user:password@localhost/agriscan_db
```

---

## Features

### 1. 🌾 Disease Detection System
- **Upload/Capture** leaf images
- **AI-Powered Detection** using CNN model (agriscan_best.h5)
- **10 Disease Types** supported:
  - Bacterial Leaf Blight
  - Brown Spot
  - Healthy (no disease)
  - Leaf Blast
  - Leaf Scald
  - Narrow Brown Spot
  - Neck Blast
  - Rice Hispa
  - Sheath Blight
  - Tungro
- **Treatment Recommendations** for each disease
- **Detection History** with filtering and search

### 2. 📊 Yield Prediction Tool
- **Two Access Modes:**
  1. **From Scan Results** - Auto-filled with locked fields
  2. **Direct Access** - Manual entry mode

#### Auto-Fill from Detection Features:
- 🔒 **Locked Core Fields:**
  - Field Area (hectares)
  - Rice Variety
  - Planting Date
  - Growth Duration (days)
  
- ✏️ **Editable Historical Fields:**
  - Historical Production (tons)
  - Historical Yield (tons/ha) - Auto-calculated

- 🧮 **Real-Time Auto-Calculate:**
  ```
  Historical Yield = Historical Production ÷ Field Area
  ```
  - Calculates as you type
  - Light green background when auto-calculated
  - Can be manually overridden

#### Visual Indicators:
- 🔒 **Blue Badge**: "Auto-filled" (data from detection)
- 🧮 **Green Badge**: "Auto-calculated" (computed value)
- ✏️ **Yellow Badge**: "Manual Entry" (no historical data)

### 3. 🏗️ Field Management
- **Create/Edit/Delete** fields
- **Auto-Computed Farm Size:**
  - Sum of all field areas
  - Updates automatically via Django signals
  - Displayed on farmer profile (read-only)
  
- **Role-Based Ownership:**
  - Farmers manage only their fields
  - Technicians/Admins can manage any farmer's fields
  - Searchable owner dropdown for Admin/Tech

- **Barangay Field:**
  - Free-text CharField (flexible entry)
  - No predefined list required

### 4. 🌱 Planting Records
- **Track Multiple Plantings** per field
- **Linked to Detections** for accurate yield prediction
- **Historical Data Storage:**
  - Previous production amounts
  - Historical yields
  - Growth duration tracking

- **RBAC-Enabled:**
  - Searchable planting dropdown in scan form
  - Role-based filtering (farmers see only own)
  - Enhanced labels showing owner for Admin/Tech

### 5. 👥 User Management
- **Three User Roles:**
  1. **Admin/DA Officer** - Full system access
  2. **Field Technician** - Manage all farmers' data
  3. **Farmer** - Manage own fields and plantings

- **Profile Features:**
  - Auto-computed farm size display
  - Phone and location tracking
  - Notes field for additional info
  - Change password functionality

### 6. 📈 Dashboard & Reports
- **Detection Statistics:**
  - Monthly trends
  - Disease distribution
  - Severity analysis
  
- **Yield Analytics:**
  - Predictions vs actuals
  - Field performance comparison
  - Variety yield analysis

- **Export Options:**
  - PDF reports
  - CSV data exports
  - Filtered views by date range

---

## Recent Updates

### February 12, 2026 - v1.5.1
**✅ Fixed: Real-Time Auto-Calculate in Yield Prediction**
- Removed early return that prevented event listeners from attaching
- Auto-calculate now works properly when coming from detection
- Console logging added for debugging

**Key Fix:**
```javascript
// Before (BROKEN):
if (!plantingSelect) return;  // ❌ Stopped execution

// After (FIXED):
if (plantingSelect) {  // ✅ Optional, continues to auto-calc code
    // ... planting selection logic ...
}
```

### February 10, 2026 - v1.5.0
**🎯 Yield Prediction Auto-Fill from Detection**
- Unified tool accessible from scan results and main menu
- Core fields locked when auto-filled (data integrity)
- Real-time historical yield calculation
- Visual feedback with color-coded badges
- Backend auto-calculation fallback
- 100ms delay for DOM readiness

**🔒 Auto-Filled Field Behavior:**
- Area, Variety, Dates → Locked (gray, cursor:not-allowed)
- Production, Yield → Editable (allows corrections)
- SELECT fields → Disabled with hidden inputs for form submission
- Lock badges added to field labels

### February 2026 - v1.4.0
**✅ Auto-Computed Farm Size**
- Signal-based automatic calculation
- `editable=False` on model field
- Real-time updates on field create/update/delete
- Displayed on farmer profile page

**✅ Text-Based Barangay**
- Migrated from ForeignKey to CharField
- Flexible free-text entry
- Supports any barangay name

**✅ Searchable Dropdowns**
- Field owner selection (Admin/Tech)
- Planting cycle selection (all roles)
- JavaScript-based client-side search
- Enhanced labels with contextual info

**✅ Red Logout Buttons**
- Security best practice (red = destructive action)
- Consistent across desktop, mobile, profile page

---

## Best Practices

### 1. Role-Based Access Control (RBAC)
**✅ Implemented:**
```python
# Query-level filtering (SECURE)
def get_queryset(self):
    if self.request.user.profile.role == 'farmer':
        return Field.objects.filter(owner=self.request.user.profile)
    return Field.objects.all()  # Admin/Tech see all
```

**❌ Avoid:**
```python
# Template-level filtering (INSECURE)
{% if user.profile.role == 'farmer' %}
    {# Don't rely on template logic for security #}
{% endif %}
```

### 2. Auto-Computed Fields
**✅ Implemented:**
```python
class Profile(models.Model):
    farm_size_ha = models.DecimalField(editable=False)
    
    def update_farm_size(self):
        from django.db.models import Sum
        total = self.fields.aggregate(total=Sum('area_hectares'))['total']
        self.farm_size_ha = total or 0
        self.save(update_fields=['farm_size_ha'])

# Signals for automatic updates
@receiver(post_save, sender=Field)
def update_farm_size_on_field_save(sender, instance, **kwargs):
    instance.owner.update_farm_size()
```

### 3. Data Integrity
**Locked Fields Pattern:**
```javascript
// Make field read-only with visual feedback
field.readOnly = true;
field.style.backgroundColor = '#f3f4f6';  // Gray
field.style.cursor = 'not-allowed';

// For SELECT fields, disable and add hidden input
field.disabled = true;
const hiddenInput = document.createElement('input');
hiddenInput.type = 'hidden';
hiddenInput.name = field.name;
hiddenInput.value = field.value;
field.parentNode.appendChild(hiddenInput);
```

### 4. Real-Time Calculations
**Event Listeners:**
```javascript
productionField.addEventListener('input', () => {
    const area = parseFloat(areaField.value);
    const production = parseFloat(productionField.value);
    
    if (area > 0 && production > 0 && yieldField.dataset.manualEdit !== 'true') {
        yieldField.value = (production / area).toFixed(2);
        yieldField.style.backgroundColor = '#f0fdf4';  // Light green
    }
});
```

### 5. Form Submission
**Enable Readonly Fields Before Submit:**
```javascript
form.addEventListener('submit', function(e) {
    // Remove readonly so fields submit
    form.querySelectorAll('input[readonly]').forEach(field => {
        field.readOnly = false;
    });
    
    // Enable disabled fields
    form.querySelectorAll('select[disabled], input[disabled]').forEach(field => {
        field.disabled = false;
    });
});
```

---

## Database Schema

### Core Models

#### Profile
```python
- user (OneToOne → User)
- role (CharField: admin/technician/farmer)
- phone (CharField)
- location (CharField)
- farm_size_ha (DecimalField, editable=False)  # Auto-computed
- notes (TextField)
```

#### Field
```python
- owner (ForeignKey → Profile)
- barangay (CharField)  # Free text
- name (CharField)
- area_hectares (DecimalField)
- gps_lat (DecimalField)
- gps_lon (DecimalField)
```

#### PlantingRecord
```python
- field (ForeignKey → Field)
- variety (ForeignKey → RiceVariety)
- planting_date (DateField)
- expected_harvest_date (DateField)
- average_growth_duration_days (PositiveIntegerField)
- notes (TextField)
```

> Note: Historical yield values are computed from `HarvestRecord` history (not stored on PlantingRecord).
#### DetectionRecord
```python
- planting (ForeignKey → PlantingRecord)
- disease (ForeignKey → DiseaseType)
- image (ImageField)
- confidence_score (FloatField)
- severity_pct (FloatField)
- detected_at (DateTimeField)
- notes (TextField)
```

#### YieldPrediction
```python
- planting (ForeignKey → PlantingRecord)
- detection (ForeignKey → DetectionRecord, nullable)
- predicted_yield_tons_per_ha (DecimalField)
- predicted_sacks_per_ha (DecimalField)
- confidence_pct (FloatField)
- predicted_at (DateTimeField)
```

### Recent Migrations
1. **0007_alter_field_barangay.py**
   - Changed Field.barangay from ForeignKey to CharField(max_length=100)

2. **0008_alter_profile_farm_size_ha.py**
   - Set Profile.farm_size_ha to editable=False
   - Added help_text for auto-compute explanation

---

## API Reference

### Internal API Endpoints

#### Get Planting Data

> Note: `historical_production_tons` and `historical_yield_tons_per_ha` are computed from recent `HarvestRecord` history (or fall back to variety averages).

```
GET /api/planting/<id>/
Response: {
    "area": 5.0,
    "variety": "Rc222",
    "planting_date": "2026-01-15",
    "growth_duration_days": 120,
    "historical_production_tons": 10.5,
    "historical_yield_tons_per_ha": 2.1,
    "field_name": "Rice Field A"
}
```

### View Functions

#### Yield Prediction
```python
@login_required
def yield_prediction(request):
    detection_id = request.GET.get('detection_id')
    
    if detection_id:
        # Auto-fill mode
        detection = DetectionRecord.objects.get(pk=detection_id)
        initial_data = {
            'area': detection.planting.field.area_hectares,
            'variety': detection.planting.variety.code,
            # ... other fields
        }
        from_detection = True
    else:
        # Manual entry mode
        initial_data = {}
        from_detection = False
    
    form = YieldPredictionForm(initial=initial_data)
    
    return render(request, 'yield_prediction.html', {
        'form': form,
        'from_detection': from_detection,
        'detection': detection
    })
```

---

## Testing Guide

### Manual Testing Checklist

#### Farm Size Auto-Compute
- [ ] Create new field → Check profile shows updated farm size
- [ ] Edit field area → Verify farm size recalculates
- [ ] Delete field → Confirm farm size decreases
- [ ] Multiple fields → Ensure correct sum

#### Yield Prediction (Detection Flow)
- [ ] Scan leaf image → Get detection result
- [ ] Click "🌾 Yield Prediction Tool" button
- [ ] Verify core fields are locked (gray background)
- [ ] Check auto-filled values are correct
- [ ] Type in Historical Production → Yield calculates instantly
- [ ] Check light green background on yield field
- [ ] Verify 🧮 badge appears on Historical Yield label
- [ ] Submit form → Prediction saves successfully

#### Yield Prediction (Manual Entry)
- [ ] Access from main menu
- [ ] All fields editable (white background)
- [ ] Type Production and Area → Yield auto-calculates
- [ ] Select planting record → Fields auto-fill
- [ ] Submit → Prediction saves

#### Real-Time Auto-Calculate
- [ ] Open browser console (F12)
- [ ] Type in Production field
- [ ] Watch console for "🧮 Real-time calculation triggered"
- [ ] Verify yield field updates as you type
- [ ] Check manualEdit flag behavior

#### Role-Based Access
- [ ] Login as Farmer → See only own data
- [ ] Login as Technician → See all data
- [ ] Login as Admin → Manage all users and data
- [ ] Test searchable dropdowns for each role

### Console Testing

**Check Auto-Calculate Logs:**
```javascript
// Expected output when typing in Production:
🧮 Real-time calculation triggered: { area: 5, production: 10, manualEdit: "false" }
  → Calculated: 2.00 Manual edit? false
  ✅ Auto-calculated and updated field: 2.00
```

**Check Detection Auto-Fill Logs:**
```javascript
🔒 Locking auto-filled fields from detection...
✅ Locked: Field Area
✅ Locked: Variety
✅ Locked: Planting Date
✅ Locked: Growth Duration
🧮 Checking auto-compute conditions...
  Area field: found (value: 5.0)
  Production field: found (value: "10.5")
  Yield field: found (value: "2.1")
  Parsed values - Area: 5 Production: 10.5
  Calculated yield: 2.10
✅ Auto-calculated Historical Yield: 2.10 tons/ha (10.5 ÷ 5)
```

### Unit Tests

```python
# Test farm size auto-compute
def test_farm_size_updates_on_field_create(self):
    profile = Profile.objects.get(user__username='farmer1')
    Field.objects.create(owner=profile, name='Test Field', area_hectares=2.5)
    profile.refresh_from_db()
    self.assertEqual(profile.farm_size_ha, 2.5)

# Test RBAC filtering
def test_farmer_sees_only_own_fields(self):
    self.client.login(username='farmer1', password='pass')
    response = self.client.get('/fields/')
    fields = response.context['fields']
    for field in fields:
        self.assertEqual(field.owner, self.farmer_profile)
```

---

## Troubleshooting

### Common Issues

#### 1. Farm Size Not Updating
**Symptoms:** Farm size stays at 0 or old value

**Solutions:**
```python
# Check signals are registered
# In polls/apps.py:
class PollsConfig(AppConfig):
    def ready(self):
        import polls.signals  # Make sure this is present

# Manual update via shell
python manage.py shell
>>> from polls.models import Profile
>>> profile = Profile.objects.get(user__username='farmer1')
>>> profile.update_farm_size()
>>> print(profile.farm_size_ha)
```

#### 2. Auto-Calculate Not Working
**Symptoms:** Yield field doesn't update when typing production

**Check Console:**
1. Open F12 → Console tab
2. Type in Production field
3. Look for "🧮 Real-time calculation triggered"

**Common Causes:**
- `manualEdit` flag set to 'true' (user typed in yield field)
- Event listeners not attached (check for JavaScript errors)
- Fields not found (check element IDs)

**Fix:**
```javascript
// Reset manualEdit flag
yieldField.dataset.manualEdit = 'false';
yieldField.style.backgroundColor = '#f0fdf4';

// Manually trigger calculation
const event = new Event('input', { bubbles: true });
productionField.dispatchEvent(event);
```

#### 3. Locked Fields Not Submitting
**Symptoms:** Form submits but locked field data missing

**Solutions:**
- Check form submission script runs before submit
- Verify hidden inputs created for disabled SELECT fields
- Look for console logs: "✅ Enabled readonly field"

**Debug:**
```javascript
form.addEventListener('submit', function(e) {
    e.preventDefault();  // Temporarily prevent submit
    console.log('Form data:', new FormData(form));
    // Check if locked fields have values
});
```

#### 4. Detection Not Loading
**Symptoms:** "Detection #X not found" error

**Check:**
```python
# In Django shell
>>> from polls.models import DetectionRecord
>>> DetectionRecord.objects.get(pk=X)
# Should return detection object

>>> detection = DetectionRecord.objects.get(pk=X)
>>> detection.planting  # Should not be None
>>> detection.planting.field  # Should have field
>>> detection.planting.variety  # Should have variety
```

#### 5. Planting Dropdown Empty
**Symptoms:** No options in planting dropdown

**Check RBAC Filtering:**
```python
# For farmers
PlantingRecord.objects.filter(field__owner=user.profile)

# For admin/tech
PlantingRecord.objects.all()
```

**Verify Data:**
```python
python manage.py shell
>>> from polls.models import PlantingRecord
>>> PlantingRecord.objects.count()  # Should be > 0
```

---

## Development Tips

### Console Debugging
Always open browser console (F12) when developing/testing:
- JavaScript errors appear immediately
- Console.log statements show execution flow
- Network tab shows API calls and responses

### Django Debug Toolbar
```python
# Install for development
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Shows SQL queries, template context, signals fired
```

## Project Structure

```
mysite/
├── manage.py           # Django CLI
├── requirements.txt    # Dependencies
├── mysite/            # Settings
├── polls/             # Main app
├── templates/         # HTML files
├── models/            # ML models
└── dataset/           # Training data
```

## Configuration

**Important**: Set timezone in `mysite/settings.py`:
```python
TIME_ZONE = 'Asia/Manila'
USE_TZ = True
```

## Tech Stack

- Django 5.2.8
- Python 3.13.7
- MySQL 8.0
- TensorFlow/Keras
- Tailwind CSS

## License

Proprietary - Department of Agriculture

---

**Version**: 1.0  
**Last Updated**: 2026-02-22

*Version: 1.5.1*
