from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong, random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mysecretpassword@localhost:5432/teradrive'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    role = db.Column(db.Boolean, nullable=False, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Implement user authentication logic here, e.g., check credentials against the database
        user = User.query.filter_by(username=username).first()

        if user and user.password_hash == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            if user.role:
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
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.role:
        flash('Access Denied: You are not an admin.', 'error')
        return redirect(url_for('user_dashboard'))
    return render_template('admin_dashboard.html')

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html.html')

if __name__ == '__main__':
    app.run(debug=True)
