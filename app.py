from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend import database_operations

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, username, role, email):
        self.id = id
        self.username = username
        self.role = role
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    # Load a user from the database based on user_id
    user = database_operations.get_user_by_id(user_id)
    if user:
        user_id, username, role, email = user  # Unpack the tuple
        return User(user_id, username, role, email)
    else:
        return None


registered_users = {}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Perform validation and user registration (replace with your own logic)
        if username and email and phone and password:
            registered_users[username] = {
                'email': email,
                'phone': phone,
                'password': password
            }
            database_operations.create_user(username, email, generate_password_hash(password), phone)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

        flash('Registration failed. Please check your input.', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = database_operations.get_user_by_username(username)

        if user and check_password_hash(user[2], password):  # 'password_hash' is in the third position (index 2)
            user_id, username, email, role = user  # Unpack the tuple, ignoring the email field (index 2)
            user_obj = User(user_id, username, role, email)
            login_user(user_obj)
            flash('Login successful.', 'success')
            if role:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'error')

    return render_template('login.html')


@app.route('/user_dashboard')
@login_required
def user_dashboard():
    client_case_data = database_operations.get_client_cases(current_user.email)
    return render_template('user_dashboard.html', client_case_data=client_case_data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    return render_template('admin_dashboard.html')


@app.route('/clients')
@login_required
def get_clients():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    clients_records = database_operations.get_clients()
    return render_template('clients.html', records=clients_records)


@app.route('/client_cases')
@login_required
def get_client_cases():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    client_email = request.args.get('client_email')
    client_case_data = database_operations.get_client_cases(client_email)
    return render_template('client_cases.html', client_case_data=client_case_data)


@app.route('/cases')
@login_required
def display_cases():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    cases = database_operations.get_all_cases()

    return render_template('cases.html', cases=cases)


@app.route('/case_details_admin')
@login_required
def display_case_details_admin():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))

    case_id = request.args.get('case_id')

    case_details = database_operations.get_case_details(case_id)
    columns = database_operations.get_case_columns()

    case_data = {columns[i]: case_details[0][i] for i in range(len(columns))}

    return render_template('case_details_admin.html', case_details=case_data)


@app.route('/case_details_user')
@login_required
def display_case_details_user():
    case_id = request.args.get('case_id')

    case_details = database_operations.get_case_details(case_id)
    columns = database_operations.get_case_columns()
    if current_user.email == case_details[0][1]:
        case_data = {columns[i]: case_details[0][i] for i in range(len(columns))}

        return render_template('case_details_user.html', case_details=case_data)
    else:
        flash('Access Denied: You do not have access to this case.', 'error')
        return redirect(url_for('user_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
