from flask import Flask, render_template, request, redirect, url_for, flash, session
import utility_fun
app = Flask(__name__)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'user_id' not in session:
        flash("You need to log in to access the admin dashboard.", "error")
        return redirect(url_for('signin'))

    user_id = session['user_id']
    recommended_movies = []  # Initialize recommended_movies as an empty list
    selected_username = None
    
    try:
        # Query for users who have logged in
        connection =  utility_fun.get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE LastLogin IS NOT NULL AND Role != 'admin'")
            users = cursor.fetchall()

        if request.method == 'POST':
            user_id = request.form.get('user_id')
            
            if user_id:
                # Query for the selected user's username
                selected_user =  utility_fun.get_user_by_id(user_id)
                selected_username = selected_user['Username'] if selected_user else None
                
                # Query for the selected user's search history
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM SearchHistory WHERE UserID = %s", (user_id,))
                    history = cursor.fetchall()
                
                # Generate recommended movies based on search history
                recommended_movies = [ utility_fun.History_display(record['SearchQuery']) for record in history]
                
            connection.close()

        return render_template(
            'admin_dashboard.html',
            users=users,
            user_history=recommended_movies,
            selected_username=selected_username
        )
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('admin_dashboard'))

if __name__ == "__main__":
    app.run(debug=True, port=5003)
