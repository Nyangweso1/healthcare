
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import contextlib
import traceback
from ml.risk_engine import RiskAssessmentEngine
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "healthcare_insurance_risk_secret_key_2026"

# Database configuration
DATABASE = 'instance/users.db'

# Initialize Risk Assessment Engine
try:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "models", "insurance_risk_model.pkl")
    logger.info(f"Initializing Risk Assessment Engine with model: {model_path}")
    risk_engine = RiskAssessmentEngine(model_path=model_path)
    logger.info("✓ Risk Assessment Engine initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize Risk Engine: {e}")
    logger.error(traceback.format_exc())
    risk_engine = None


# ==================== DATABASE FUNCTIONS ====================

def init_db():
    """Initialize the database with users, assessments, and messages tables."""
    os.makedirs('instance', exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table with admin role
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Assessments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            age INTEGER,
            gender TEXT,
            marital_status TEXT,
            employment_status TEXT,
            income REAL,
            children INTEGER,
            education_level TEXT,
            residence_type TEXT,
            chronic_illness TEXT,
            family_size INTEGER,
            healthcare_knowledge TEXT,
            hospital_visit_gap REAL,
            routine_checkups INTEGER,
            cancer_screening INTEGER,
            dental_checkup INTEGER,
            mental_health_support INTEGER,
            risk_level TEXT,
            probability REAL,
            rule_based_score INTEGER,
            rule_based_category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Messages table for admin-user communication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_user_id) REFERENCES users (id),
            FOREIGN KEY (to_user_id) REFERENCES users (id)
        )
    ''')
    
    # Add is_admin column to existing users table if not exists
    with contextlib.suppress(Exception):
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
    
    conn.commit()
    conn.close()
    logger.info("✓ Database initialized")


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def is_admin():
    """Check if current user is admin."""
    return bool(session.get('logged_in')) and session.get('is_admin', 0) == 1


def admin_required(f):
    """Decorator for admin-only routes."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        if not is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html', username=session.get('username'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Insert into database
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, hashed_password)
            )
            conn.commit()
            conn.close()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validation
        if not username or not password:
            flash('Username and password are required!', 'danger')
            return redirect(url_for('login'))
        
        # Check credentials
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            # Set session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            session['logged_in'] = True
            
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/assess')
def assess():
    """Insurance risk assessment form."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access the risk assessment tool.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('assess.html', username=session.get('username'))


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request and return results."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access the risk assessment tool.', 'warning')
        return redirect(url_for('login'))
    
    if risk_engine is None:
        flash('Risk assessment engine is not available. Please contact administrator.', 'danger')
        return redirect(url_for('assess'))
    
    try:
        # Collect form data with additional features
        user_data = {
            'Age': int(request.form.get('age')),
            'Gender': request.form.get('gender'),
            'Marital Status': request.form.get('marital_status'),
            'Employment Status': request.form.get('employment_status'),
            'Monthly Household Income': float(request.form.get('income')),
            'num_children': int(request.form.get('children')),
            'education_level': request.form.get('education_level'),
            'residence_type': request.form.get('residence_type'),
            'chronic_illness': request.form.get('chronic_illness'),
            'family_size': int(request.form.get('family_size')),
            'healthcare_knowledge': request.form.get('healthcare_knowledge'),
            'hospital_visit_gap': float(request.form.get('hospital_visit_gap')),
            'routine_check': int(request.form.get('routine_check', 0)),
            'cancer_screening': int(request.form.get('cancer_screening', 0)),
            'dental_checkup': int(request.form.get('dental_checkup', 0)),
            'mental_health_support': int(request.form.get('mental_health_support', 0))
        }
        
        # Calculate preventive care score
        user_data['preventive_care_score'] = (
            user_data['routine_check'] + 
            user_data['cancer_screening'] + 
            user_data['dental_checkup'] + 
            user_data['mental_health_support']
        )
        
        # Get risk assessment
        result = risk_engine.predict_risk(user_data)
        
        # Save assessment to database
        try:
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO assessments (
                    user_id, age, gender, marital_status, employment_status, 
                    income, children, education_level, residence_type, 
                    chronic_illness, family_size, healthcare_knowledge,
                    hospital_visit_gap, routine_checkups, cancer_screening,
                    dental_checkup, mental_health_support, risk_level, probability,
                    rule_based_score, rule_based_category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session.get('user_id'),
                user_data['Age'],
                user_data['Gender'],
                user_data['Marital Status'],
                user_data['Employment Status'],
                user_data['Monthly Household Income'],
                user_data['num_children'],
                user_data['education_level'],
                user_data['residence_type'],
                user_data['chronic_illness'],
                user_data['family_size'],
                user_data['healthcare_knowledge'],
                user_data['hospital_visit_gap'],
                user_data['routine_check'],
                user_data['cancer_screening'],
                user_data['dental_checkup'],
                user_data['mental_health_support'],
                result['risk_level'],
                result['probability'],
                result.get('rule_based_score', 0),
                result.get('rule_based_category', 'Unknown')
            ))
            conn.commit()
            conn.close()
        except Exception as db_error:
            logger.warning(f"Failed to save assessment to database: {db_error}")
        
        # Store in session for results page
        session['assessment_result'] = result
        session['user_data'] = user_data
        
        return redirect(url_for('results'))
    
    except ValueError as e:
        flash(f'Invalid input: {e}. Please check your data.', 'danger')
        return redirect(url_for('assess'))
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        flash('An error occurred during risk assessment. Please try again.', 'danger')
        return redirect(url_for('assess'))


@app.route('/results')
def results():
    """Display risk assessment results."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access your results.', 'warning')
        return redirect(url_for('login'))
    
    # Get results from session
    result = session.get('assessment_result')
    user_data = session.get('user_data')
    
    if not result:
        flash('No assessment results found. Please complete an assessment first.', 'warning')
        return redirect(url_for('assess'))
    
    return render_template('results.html', 
                          result=result, 
                          user_data=user_data,
                          username=session.get('username'))


@app.route('/history')
def history():
    """Show assessment history from database."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to view your history.', 'warning')
        return redirect(url_for('login'))
    
    # Get user's assessment history
    conn = get_db_connection()
    assessments = conn.execute(
        'SELECT * FROM assessments WHERE user_id = ? ORDER BY created_at DESC LIMIT 20',
        (session.get('user_id'),)
    ).fetchall()
    conn.close()
    
    return render_template('history.html', 
                          assessments=assessments,
                          username=session.get('username'))


@app.route('/about')
def about():
    """about page."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('about.html', username=session.get('username'))


@app.route('/blog')
def blog():
    """Blog/Insurance Education page."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('blog.html', username=session.get('username'))


@app.route('/health-tips')
def health_tips():
    """Health tips page with statistics."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    try:
        import pandas as pd
        import os
        
        # Try to load dataset and calculate statistics
        data_path = os.path.join('data', 'healthcare_clean.csv')
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            insured_pct = round((df['insured'].sum() / len(df)) * 100, 1)
            
            # Calculate income bracket statistics
            if 'Monthly Household Income' in df.columns:
                income_brackets = pd.cut(df['Monthly Household Income'], 
                                        bins=[0, 10000, 20000, 30000, 100000],
                                        labels=['<10k', '10k-20k', '20k-30k', '>30k'])
                bracket_stats = df.groupby(income_brackets)['Insurance'].mean() * 100
                lowest_bracket = bracket_stats.idxmin()
                lowest_pct = round(bracket_stats.min(), 1)
                
                income_data = {
                    'low_bucket_label': lowest_bracket,
                    'low_bucket_pct': lowest_pct
                }
            else:
                income_data = {
                    'low_bucket_label': '<10k',
                    'low_bucket_pct': 65.0
                }
        else:
            insured_pct = 85.7
            income_data = {
                'low_bucket_label': '<10k',
                'low_bucket_pct': 65.0
            }
            
        return render_template('health_tips.html', 
                             insured_pct=insured_pct, 
                             income_mean=income_data,
                             username=session.get('username'))
    except Exception as e:
        print(f"Error in health_tips: {str(e)}")
        return render_template('health_tips.html', 
                             insured_pct=85.7, 
                             income_mean={'low_bucket_label': '<10k', 'low_bucket_pct': 65.0},
                             username=session.get('username'))


# Tips data used by the detail route
HEALTH_TIPS_DATA = {
    1: {
        'icon': '', 'title': 'Regular Check-ups Matter',
        'date': 'February 2026',
        'summary': 'People who schedule routine health check-ups are significantly more likely to have health insurance coverage.',
        'detail': 'Regular preventive care helps catch issues early and can reduce long-term healthcare costs. Studies consistently show that individuals who engage with the healthcare system proactively are more likely to maintain continuous insurance coverage and better health outcomes.',
        'points': [
            'Schedule annual physical examinations',
            'Stay up-to-date with recommended screenings',
            'Monitor chronic conditions regularly',
            'Build a relationship with a primary care physician',
        ],
    },
    2: {
        'icon': '', 'title': 'Income & Insurance Coverage',
        'date': 'February 2026',
        'summary': 'Data shows a strong correlation between income levels and insurance coverage.',
        'detail': 'Lower-income households often face significant barriers to accessing affordable coverage. Government assistance programs and employer-sponsored options can bridge this gap for many families.',
        'points': [
            'Explore SHA subsidised plans (from KES 500/month)',
            'Check employer-sponsored insurance options',
            'Compare community-based health plans',
            'Ask your county health office about subsidies',
        ],
    },
    3: {
        'icon': '', 'title': "Don't Neglect Dental Health",
        'date': 'February 2026',
        'summary': 'Dental check-ups are an important indicator of overall health consciousness.',
        'detail': 'Poor oral health can lead to serious systemic health issues including cardiovascular disease and diabetes complications. Including dental cover in your insurance plan is highly recommended.',
        'points': [
            'Visit a dentist every 6 months',
            'Brush twice daily and floss regularly',
            'Consider insurance plans that include dental add-ons',
            'Address tooth pain early — do not delay treatment',
        ],
    },
    4: {
        'icon': '', 'title': 'Mental Health Support',
        'date': 'February 2026',
        'summary': 'Mental health is as important as physical health.',
        'detail': 'Access to mental health support correlates with better overall health outcomes and insurance coverage. Many Kenyans overlook mental health services — but stress, anxiety, and depression directly affect physical health.',
        'points': [
            'Seek counselling if experiencing stress or anxiety',
            'Practice stress management techniques (exercise, sleep, community)',
            'Check if your insurance covers mental health services',
            'Use community health centres for low-cost support',
        ],
    },
    5: {
        'icon': '', 'title': 'Cancer Screening Saves Lives',
        'date': 'February 2026',
        'summary': 'Early detection through regular cancer screenings dramatically improves treatment outcomes and survival rates.',
        'detail': 'Many cancers are highly treatable when caught early. Kenya has seen a rise in cancer cases yet screening rates remain low. Most insurance plans cover basic cancer screenings.',
        'points': [
            'Follow age-appropriate screening guidelines',
            'Know your family medical history',
            'Discuss screening options with your healthcare provider',
            'Cervical, breast, and prostate screenings are widely available',
        ],
    },
    6: {
        'icon': '', 'title': 'Healthcare Knowledge is Power',
        'date': 'February 2026',
        'summary': 'Understanding healthcare systems, insurance options, and your rights as a patient helps you make better decisions.',
        'detail': 'Many uninsured individuals simply do not know what options are available to them. Reading your policy, knowing your benefits, and asking questions are the simplest steps toward better coverage.',
        'points': [
            'Read your insurance policy thoroughly',
            'Understand your benefits and coverage limits',
            'Ask questions during medical appointments',
            'Use the Insurance Guide page on this platform',
        ],
    },
}


@app.route('/health-tips/<int:tip_id>')
def health_tip_detail(tip_id):
    """Individual health tip detail view — rendered inside health_tips.html."""
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    tip = HEALTH_TIPS_DATA.get(tip_id)
    return render_template('health_tips.html',
                           tip=tip,
                           insured_pct=None,
                           income_mean=None,
                           username=session.get('username'))


@app.route('/eda')
def eda():
    """Interactive data insights dashboard powered by Chart.js."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    import pandas as pd

    data_path = os.path.join('data', 'healthcare_clean.csv')
    if not os.path.exists(data_path):
        flash('Dataset not found. Please run preprocessing first.', 'warning')
        return render_template('eda.html', username=session.get('username'), dashboard_data=None)

    try:
        df = pd.read_csv(data_path)
    except Exception as exc:
        logger.error(f"Failed to load dashboard dataset: {exc}")
        flash('Unable to load insights data right now.', 'danger')
        return render_template('eda.html', username=session.get('username'), dashboard_data=None)

    if 'insured' not in df.columns or df.empty:
        flash("Dataset does not contain the 'insured' target column.", 'warning')
        return render_template('eda.html', username=session.get('username'), dashboard_data=None)

    # Ensure target is numeric for all downstream coverage calculations.
    df['insured'] = pd.to_numeric(df['insured'], errors='coerce').fillna(0)

    def _first_col(candidates):
        cols_lower = {c.lower(): c for c in df.columns}
        for candidate in candidates:
            if candidate.lower() in cols_lower:
                return cols_lower[candidate.lower()]
        for c in df.columns:
            c_lower = c.lower()
            if any(candidate.lower() in c_lower for candidate in candidates):
                return c
        return None

    def _coverage(labels, subsets):
        counts = []
        rates = []
        for subset in subsets:
            subset_len = int(subset.shape[0])
            counts.append(subset_len)
            rate = float(round((subset['insured'].mean() * 100), 1)) if subset_len > 0 else 0.0
            rates.append(rate)
        return {'labels': labels, 'counts': counts, 'coverage': rates}

    dashboard_data = {
        'overview': {
            'samples': len(df),
            'features': max(df.shape[1] - 1, 0),
            'insured_pct': round(df['insured'].mean() * 100, 1),
            'uninsured_pct': round((1 - df['insured'].mean()) * 100, 1),
        }
    }

    # 1) Insurance coverage by income level
    income_col = _first_col(['Monthly Household Income', 'household income', 'income'])
    if income_col:
        income_series = pd.to_numeric(df[income_col], errors='coerce')
        income_bins = pd.cut(
            income_series,
            bins=[0, 10000, 20000, 40000, 80000, float('inf')],
            labels=['<10k', '10k-20k', '20k-40k', '40k-80k', '80k+'],
            include_lowest=True,
        )
        income_df = df.copy()
        income_df['income_band'] = income_bins
        income_summary = income_df.dropna(subset=['income_band']).groupby('income_band', observed=False).agg(
            count=('insured', 'size'),
            coverage=('insured', 'mean')
        )
        dashboard_data['income_coverage'] = {
            'labels': [str(label) for label in income_summary.index],
            'counts': [int(v) for v in income_summary['count'].tolist()],
            'coverage': [float(round(v * 100, 1)) for v in income_summary['coverage'].tolist()],
        }
    else:
        dashboard_data['income_coverage'] = {'labels': [], 'counts': [], 'coverage': []}

    # 2) Frequency of medical check-ups (routine + recency)
    routine_col = _first_col(['routine_check', 'routine check-up'])
    if routine_col:
        routine_vals = pd.to_numeric(df[routine_col], errors='coerce').fillna(0)
        yes_mask = routine_vals >= 1
        dashboard_data['checkup_frequency'] = {
            'labels': ['Routine Check-up: Yes', 'Routine Check-up: No'],
            'counts': [int(yes_mask.sum()), int((~yes_mask).sum())],
            'coverage': [
                float(round(df.loc[yes_mask, 'insured'].mean() * 100, 1)) if yes_mask.any() else 0.0,
                float(round(df.loc[~yes_mask, 'insured'].mean() * 100, 1)) if (~yes_mask).any() else 0.0,
            ]
        }
    else:
        dashboard_data['checkup_frequency'] = {'labels': [], 'counts': [], 'coverage': []}

    visit_gap_col = _first_col(['hospital_visit_gap', 'last time you visited a hospital'])
    if visit_gap_col:
        visit_gap = pd.to_numeric(df[visit_gap_col], errors='coerce')
        visit_band = pd.cut(
            visit_gap,
            bins=[-0.001, 1, 3, 6, 12, float('inf')],
            labels=['<1 month', '1-3 months', '3-6 months', '6-12 months', '12+ months'],
            include_lowest=True,
        )
        visit_df = df.copy()
        visit_df['visit_band'] = visit_band
        visit_summary = visit_df.dropna(subset=['visit_band']).groupby('visit_band', observed=False).agg(
            count=('insured', 'size'),
            coverage=('insured', 'mean')
        )
        dashboard_data['hospital_visit_pattern'] = {
            'labels': [str(label) for label in visit_summary.index],
            'counts': [int(v) for v in visit_summary['count'].tolist()],
            'coverage': [float(round(v * 100, 1)) for v in visit_summary['coverage'].tolist()],
        }
    else:
        dashboard_data['hospital_visit_pattern'] = {'labels': [], 'counts': [], 'coverage': []}

    # 3) Common health conditions from condition-like columns
    condition_keywords = ['chronic', 'condition', 'illness', 'disease', 'diabetes', 'hypertension', 'asthma', 'cancer']
    excluded_terms = ['score', 'risk', 'insurance', 'insured']
    condition_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(k in col_lower for k in condition_keywords) and all(ex not in col_lower for ex in excluded_terms) and col != 'insured':
            condition_cols.append(col)

    condition_rows = []
    for col in condition_cols:
        numeric_col = pd.to_numeric(df[col], errors='coerce')
        if numeric_col.notna().sum() == 0:
            continue
        prevalence = float(round((numeric_col.fillna(0) > 0).mean() * 100, 1))
        coverage = float(round(df.loc[numeric_col.fillna(0) > 0, 'insured'].mean() * 100, 1)) if (numeric_col.fillna(0) > 0).any() else 0.0
        if prevalence > 0:
            label = col.split('_')[-1].replace('-', ' ').strip().title()
            if len(label) < 3:
                label = col[:45]
            condition_rows.append((label, prevalence, coverage))

    condition_rows = sorted(condition_rows, key=lambda x: x[1], reverse=True)[:8]
    dashboard_data['common_conditions'] = {
        'labels': [r[0] for r in condition_rows],
        'prevalence': [r[1] for r in condition_rows],
        'coverage': [r[2] for r in condition_rows],
    }

    # 4) Additional insights: employment and preventive care
    employment_cols = [c for c in df.columns if c.lower().startswith('employment status_')]
    if employment_cols:
        emp_labels = []
        emp_subsets = []
        for col in employment_cols:
            label = col.split('_')[-1]
            mask = pd.to_numeric(df[col], errors='coerce').fillna(0) == 1
            emp_labels.append(label)
            emp_subsets.append(df[mask])
        dashboard_data['employment_coverage'] = _coverage(emp_labels, emp_subsets)
    else:
        dashboard_data['employment_coverage'] = {'labels': [], 'counts': [], 'coverage': []}

    preventive_col = _first_col(['preventive_care_score'])
    if preventive_col:
        preventive_vals = pd.to_numeric(df[preventive_col], errors='coerce').fillna(0)
        p_df = df.copy()
        p_df['preventive_score'] = preventive_vals.round().astype(int)
        p_summary = p_df.groupby('preventive_score', observed=False).agg(
            count=('insured', 'size'),
            coverage=('insured', 'mean')
        ).sort_index()
        dashboard_data['preventive_care_impact'] = {
            'labels': [str(v) for v in p_summary.index.tolist()],
            'counts': [int(v) for v in p_summary['count'].tolist()],
            'coverage': [float(round(v * 100, 1)) for v in p_summary['coverage'].tolist()],
        }
    else:
        dashboard_data['preventive_care_impact'] = {'labels': [], 'counts': [], 'coverage': []}

    return render_template('eda.html', dashboard_data=dashboard_data, username=session.get('username'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page - send messages to admin or users."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        to_user = request.form.get('to_user', 'admin')  # Default to admin
        
        if not subject or not message:
            flash('Subject and message are required!', 'danger')
            return redirect(url_for('contact'))
        
        # Get recipient user_id (admin or specific user)
        conn = get_db_connection()
        if to_user == 'admin':
            # Send to first admin user
            recipient = conn.execute('SELECT id FROM users WHERE is_admin = 1 LIMIT 1').fetchone()
            if not recipient:
                flash('No admin found. Please contact support.', 'danger')
                conn.close()
                return redirect(url_for('contact'))
            to_user_id = recipient['id']
        else:
            to_user_id = int(to_user)
        
        # Insert message
        conn.execute('''
            INSERT INTO messages (from_user_id, to_user_id, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (session.get('user_id'), to_user_id, subject, message))
        conn.commit()
        conn.close()
        
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    # Get user's sent and received messages
    conn = get_db_connection()
    sent_messages = conn.execute('''
        SELECT m.*, u.username as recipient_name 
        FROM messages m 
        JOIN users u ON m.to_user_id = u.id 
        WHERE m.from_user_id = ? 
        ORDER BY m.created_at DESC
    ''', (session.get('user_id'),)).fetchall()
    
    received_messages = conn.execute('''
        SELECT m.*, u.username as sender_name 
        FROM messages m 
        JOIN users u ON m.from_user_id = u.id 
        WHERE m.to_user_id = ? 
        ORDER BY m.created_at DESC
    ''', (session.get('user_id'),)).fetchall()
    
    # Mark received messages as read
    conn.execute('UPDATE messages SET is_read = 1 WHERE to_user_id = ?', (session.get('user_id'),))
    conn.commit()
    
    # Get all users if admin (for sending messages to specific users)
    users = []
    if is_admin():
        users = conn.execute('SELECT id, username, email FROM users WHERE id != ? ORDER BY username', 
                           (session.get('user_id'),)).fetchall()
    
    conn.close()
    
    return render_template('contact.html', 
                          username=session.get('username'),
                          sent_messages=sent_messages,
                          received_messages=received_messages,
                          users=users,
                          is_admin=is_admin())


# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with all users and assessments."""
    conn = get_db_connection()
    
    # Get all users
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    
    # Get total assessments count
    total_assessments = conn.execute('SELECT COUNT(*) as count FROM assessments').fetchone()['count']
    
    # Get recent assessments with user info
    recent_assessments = conn.execute('''
        SELECT a.*, u.username, u.email 
        FROM assessments a 
        JOIN users u ON a.user_id = u.id 
        ORDER BY a.created_at DESC 
        LIMIT 50
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html',
                          username=session.get('username'),
                          users=users,
                          total_assessments=total_assessments,
                          recent_assessments=recent_assessments)


@app.route('/admin/user/<int:user_id>')
@admin_required
def admin_view_user(user_id):
    """Admin view specific user's assessments."""
    conn = get_db_connection()
    
    # Get user info
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    # Get user's assessments
    assessments = conn.execute('''
        SELECT * FROM assessments 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return render_template('admin_user_view.html',
                          username=session.get('username'),
                          user=user,
                          assessments=assessments)


@app.route('/admin/send-message/<int:user_id>', methods=['POST'])
@admin_required
def admin_send_message(user_id):
    """Admin send message to specific user."""
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    if not subject or not message:
        flash('Subject and message are required!', 'danger')
        return redirect(url_for('admin_view_user', user_id=user_id))
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO messages (from_user_id, to_user_id, subject, message)
        VALUES (?, ?, ?, ?)
    ''', (session.get('user_id'), user_id, subject, message))
    conn.commit()
    conn.close()
    
    flash('Message sent successfully!', 'success')
    return redirect(url_for('admin_view_user', user_id=user_id))


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""

    return render_template('500.html'), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run app
    logger.info("=" * 60)
    logger.info("Starting Healthcare Insurance Risk Prediction System")
    logger.info("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

