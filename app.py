from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend import database_operations
from datetime import datetime
import schedule
import time
import os

app = Flask(__name__)

# change to an environment variable
app.secret_key = os.environ.get('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, username, name, email, phone, role):
        self.id = id
        self.username = username
        self.name = name
        self.phone = phone
        self.role = role
        self.email = email


@login_manager.user_loader
def load_user(user_id):
    # Load a user from the database based on user_id
    user = database_operations.get_user_by_id(user_id)
    if user:
        id, username, name, email, phone, role = user  # Unpack the tuple
        return User(id, username, name, email, phone, role)
    else:
        return None


registered_users = {}

schedule.every(24).hours.do(database_operations.create_from_monday())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Perform validation and user registration (replace with your own logic)
        if username and email and phone and password:
            registered_users[username] = {
                'email': email,
                'name': name,
                'phone': phone,
                'password': password
            }
            database_operations.create_user(username, name, email, generate_password_hash(password), phone)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

        flash('Registration failed. Please check your input.', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Hello")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = database_operations.get_user_by_username(username)

        if user and check_password_hash(user[4], password):  # 'password_hash' is in the third position (index 2)
            id, username, name, email, password_hash, phone, role = user
            user_obj = User(id, username, name, email, phone, role)
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
    # return render_template('user_dashboard.html', client_case_data=client_case_data)
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
    client_case_data = database_operations.get_client_cases(current_user.email)
    clients_records = database_operations.get_clients()
    cases = database_operations.get_all_cases()
    # return render_template('admin_dashboard.html')
    return render_template('admin_dashboard.html', client_case_data=client_case_data, records=clients_records, cases=reversed(cases))



# This has been added to main admin page in admin_dashboard route

# @app.route('/clients')
# @login_required
# def get_clients():
#     if not current_user.role:
#         flash('Access Denied: You are not an admin.', 'error')
#         return redirect(url_for('user_dashboard'))
#     clients_records = database_operations.get_clients()
#     return render_template('clients.html', records=clients_records)


@app.route('/client_cases')
@login_required
def get_client_cases():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    client_email = request.args.get('client_email')
    client_case_data = database_operations.get_client_cases(client_email)
    print(client_email)
    print(client_case_data)
    return render_template('client_cases.html', client_case_data=client_case_data)


# This has been added to main admin page in admin_dashboard route

# @app.route('/cases')
# @login_required
# def display_cases():
#     if not current_user.role:
#         flash('Access Denied: You are not an admin.', 'error')
#         return redirect(url_for('user_dashboard'))
#     cases = database_operations.get_all_cases()

#     return render_template('cases.html', cases=reversed(cases))


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


@app.route('/update_case_form', methods=['GET', 'POST'])
@login_required
def update_case_form():
    case_id = request.args.get('case_id')
    case_statuses = ["None", "Confirmed", "Declined", "Quote Sent", "Evaluating", "En Route", "Closed",
                     "Evaluation Complete",
                     "Unrecoverable", "Completed"]

    case_progresses = ["None", "Waiting for parts", "Files sent", "In progress", "Completed", "Closed",
                       "File list sent",
                       "Cloning", "Waiting for drive", "Copying files", "Invoice sent", "Approved", "Paid",
                       "Shipped",
                       "Reasearch", "Super Rush"]

    date_values = {
        'day': get_days(),
        'month': get_months(),
        'year': get_current_and_next_year()
    }

    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))

    case_details = database_operations.get_case_details(case_id)
    columns = database_operations.get_case_columns()

    case_data = {columns[i]: case_details[0][i] for i in range(len(columns))}

    return render_template('update_case.html', case_details=case_data, progresses=case_progresses,
                           statuses=case_statuses, date_values=date_values)


@app.route('/update-case', methods=['GET', 'POST'])
@login_required
def update_case():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))

    updated_data = {}
    for key in request.form:
        if key.startswith('select-day-'):
            date_key = key.replace('select-day-', '')
            day = request.form.get(key)
            month = request.form.get(f'select-month-{date_key}')
            year = request.form.get(f'select-year-{date_key}')
            updated_data[date_key] = combine_date(day, month, year)
        elif key == 'case_quote':
            try:
                updated_data[key] = int(request.form[key])
            except ValueError:
                updated_data[key] = 0
        elif key == 'case_permissions':
            if request.form[key] == 'yes':
                updated_data[key] = True
            else:
                updated_data[key] = False
        else:
            updated_data[key] = request.form[key]

    database_operations.update_case(**updated_data)

    return redirect(url_for('admin_dashboard'))


# @app.route('/get_client_details')
# @login_required
# def get_client_details():
#     if not current_user.role:
#         flash('Access Denied: You are not an admin.', 'error')
#         return redirect(url_for('user_dashboard'))
#     client_id = request.args.get('client_id')
#     client_details = database_operations.get_client_details(client_id)
#     return render_template('client_details.html', client_details=client_details)


@app.route('/edit_credentials_form')
@login_required
def edit_credentials_form():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    client_id = request.args.get('client_id')
    user_details = database_operations.get_user_by_id(client_id)

    return render_template('edit_credentials_form.html', user_info=user_details)


@app.route('/edit_credentials', methods=['POST'])
@login_required
def edit_credentials():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))

    # get stuff from the form here

    credentials_data = {}

    for key in request.form:
        credentials_data[key] = request.form[key]

    if credentials_data['new_password'] == credentials_data['confirm_password'] and not None:
        password_hash = generate_password_hash(credentials_data['new_password'])

    role = False
    try:
        if credentials_data['admin_role']:
            role = True
    except:
        pass

    update_data = {
        'password_hash': password_hash,
        'email': credentials_data['user_email'],
        'phone': credentials_data['client_phone'],
        'name': credentials_data['client_name'],
        'username': credentials_data['username'],
        'role': role
    }
    database_operations.update_user_client(**update_data)
    return redirect(url_for('admin_dashboard'))


@app.route('/delete_case')
@login_required
def delete_case():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    case_id = request.args.get('case_id')
    return render_template('delete_confirmation.html', case_id=case_id)


@app.route('/confirm_delete_case', methods=['POST'])
@login_required
def confirm_delete_case():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    case_id = request.args.get('case_id')
    if case_id:

        database_operations.delete_case(case_id)
        return redirect(url_for('admin_dashboard'))
    else:
        # Handle invalid case_id
        return redirect(url_for('admin_dashboard'))


@app.route('/delete_case_confirmation')
@login_required
def delete_case_confirmation():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    case_id = request.args.get('case_id')
    return render_template('delete_confirmation.html', case_id=case_id)


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


'''
client_email, case_drop_off, case_status, case_work_progress,
        case_malfunction, case_quote, case_device_type, case_important_folders,
        case_size, case_permissions, case_date_recieved, case_date_quote_approved,
        case_completed_date, case_date_finalized, case_referred_by, case_notes
'''


@app.route('/create_case_form', methods=['GET', 'POST'])
@login_required
def create_case_form():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))

    case_statuses = ["None", "Confirmed", "Declined", "Quote Sent", "Evaluating", "En Route", "Closed",
                     "Evaluation Complete",
                     "Unrecoverable", "Completed"]

    case_progresses = ["None", "Waiting for parts", "Files sent", "In progress", "Completed", "Closed",
                       "File list sent",
                       "Cloning", "Waiting for drive", "Copying files", "Invoice sent", "Approved", "Paid",
                       "Shipped",
                       "Reasearch", "Super Rush"]

    years = get_current_and_next_year()

    return render_template('create_case.html', clients=database_operations.get_clients(), statuses=case_statuses,
                           progresses=case_progresses, years=years, months=get_months(),
                           days=get_days())


@app.route('/create-case', methods=['GET', 'POST'])
@login_required
def create_case_post():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    if request.method == 'POST':
        client_email = request.form['client_email']
        case_drop_off = get_formatted_date_from_form(request.form, 'select-day-case_drop_off',
                                                     'select-month-case_drop_off',
                                                     'select-year-case_drop_off')
        case_status = request.form['case_status']
        case_work_progress = request.form['case_work_progress']
        case_malfunction = request.form['case_malfunction']
        case_quote = request.form['case_quote']
        case_device_type = request.form['case_device_type']
        case_important_folders = request.form['case_important_folders']
        case_size = request.form['case_size']
        case_permissions = request.form.get('case_permissions')
        case_date_received = get_formatted_date_from_form(request.form, 'select-day-case_drop_off',
                                                          'select-month-case_drop_off',
                                                          'select-year-case_drop_off')
        case_date_quote_approved = get_formatted_date_from_form(request.form, 'select-day-case_drop_off',
                                                                'select-month-case_drop_off',
                                                                'select-year-case_drop_off')
        case_completed_date = None
        case_date_finalized = None
        case_referred_by = request.form['case_referred_by']
        case_notes = request.form['case_notes']

        case = (client_email, case_drop_off, case_status, case_work_progress,
                case_malfunction, case_quote, case_device_type, case_important_folders,
                case_size, case_permissions == 'yes', case_date_received, case_date_quote_approved,
                case_completed_date, case_date_finalized, case_referred_by, case_notes)

        database_operations.create_case(replace_empty_with_none(case))

        return redirect(url_for('admin_dashboard'))


def get_formatted_date_from_form(form, day_field, month_field, year_field, date_format="%Y-%m-%d"):
    day = int(form[day_field])
    month = int(form[month_field])
    year = int(form[year_field])
    date_object = datetime(year, month, day)
    return date_object.strftime(date_format)


def replace_empty_with_none(input_tuple):
    return tuple(None if element == '' else element for element in input_tuple)


def get_days():
    days = []
    for i in range(1, 32):
        days.append(i)
    return days


def get_months():
    months = []
    for i in range(1, 13):
        months.append(i)
    return months


def get_current_and_next_year():
    current_year = datetime.now().year
    next_year = current_year + 1
    return [current_year, next_year]


def combine_date(day, month, year):
    return f"{year}-{month}-{day}"


if __name__ == '__main__':
    app.run(debug=True)
