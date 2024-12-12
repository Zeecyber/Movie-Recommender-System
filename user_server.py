from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import utility_fun
utility_fun.app
utility_fun.app.secret_key
@utility_fun.app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))

        try:
            user = utility_fun.get_user_by_email(email)

            if user:
                flash("Username or email already registered!", "error")
                return redirect(url_for('signup'))

            password_hash = generate_password_hash(password)
            utility_fun.insert_user(username, email, password_hash)
            flash("Signup successful! Please check your email to verify your account.", "success")
            return redirect(url_for('signin'))
        except Exception as e:
            flash(f"An error occurred during signup: {e}", "error")
        return redirect(url_for('signup'))
    return render_template('signup.html')

@utility_fun.app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = utility_fun.get_user_by_email(email)
            
            if user and check_password_hash(user['PasswordHash'], password):
                connection = utility_fun.get_db_connection()
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE users SET LastLogin = NOW() WHERE UserID = %s", (user['UserID'],))
                    connection.commit()
                connection.close()
                
                session['user_id'] = user['UserID']
                if user['Role'] == 'admin':
                    flash("Welcome Admin!", "success")
                    return redirect(url_for('admin_dashboard'))
                elif user['Role'] == 'user':
                    flash("Welcome back!", "success")
                    return redirect(url_for('recommendation'))
            else:
                flash("Invalid email or password.", "error")
        except Exception as e:
            flash(f"An error occurred during signin: {e}", "error")
        return redirect(url_for('signin'))
    return render_template('signin.html')



if __name__ == "__main__":
    utility_fun.app.run(debug=True, port=5001)
