
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from risk_engine import RiskAssessmentEngine
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
    risk_engine = RiskAssessmentEngine(model_path="models/insurance_risk_model.pkl")
    logger.info("✓ Risk Assessment Engine initialized")
except Exception as e:
    logger.error(f"✗ Failed to initialize Risk Engine: {e}")
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
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0')
    except Exception:
        pass  # Column already exists
    
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
            insured_pct = round((df['Insurance'].sum() / len(df)) * 100, 1)
            
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


@app.route('/eda')
def eda():
    """Exploratory Data Analysis page."""
    # Check if user is logged in
    if not session.get('logged_in'):
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    import os
    
    # Check for existing plots in static/eda directory
    eda_dir = os.path.join('static', 'eda')
    plots = []
    
    if os.path.exists(eda_dir):
        # Get all plot files
        plot_files = [f for f in os.listdir(eda_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        # Add relative path for template (eda/filename.png)
        plots = [f'eda/{f}' for f in plot_files]
    
    return render_template('eda.html', plots=plots, username=session.get('username'))


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

