from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend import database_operations

app = Flask(__name__)
app.secret_key = 'your_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)

USER_ROLE_ADMIN = 'admin'
USER_ROLE_USER = 'user'


class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


@login_manager.user_loader
def load_user(user_id):
    # Load a user from the database based on user_id
    user = database_operations.get_user_by_id(user_id)
    if user:
        user_id, username, role = user  # Unpack the tuple
        return User(user_id, username, role)
    else:
        return None



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        user_id = database_operations.create_user(username, email, password_hash)
        if user_id:
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. User already exists.', 'error')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database_operations.get_user_by_username(username)

        if user and check_password_hash(user[2], password):  # 'password_hash' is in the third position (index 2)
            user_id, username, _, role = user  # Unpack the tuple, ignoring the email field (index 2)
            user_obj = User(user_id, username, role)
            login_user(user_obj)
            flash('Login successful.', 'success')
            if role:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('admin_dashboard.html')


@app.route('/clients')
def get_clients():
    clients_records = database_operations.get_clients()
    return render_template('clients.html', records=clients_records)


@app.route('/client_cases')
def get_client_cases():
    client_email = request.args.get('client_email')

    client_case_data = database_operations.get_client_cases(client_email)
    return render_template('client_cases.html', client_case_data=client_case_data)


@app.route('/cases')
def display_cases():
    cases = database_operations.get_all_cases()

    return render_template('cases.html', cases=cases)


@app.route('/case_details')
def display_case_details():
    case_id = request.args.get('case_id')

    case_details = database_operations.get_case_details(case_id)

    return render_template('case_details.html', case_details=case_details)


if __name__ == '__main__':
    app.run(debug=True)
