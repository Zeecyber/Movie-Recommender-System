from flask import Flask, render_template, request, redirect, url_for, flash, session
import utility_fun
utility_fun.app

@utility_fun.app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    recommended_movies = []
    selected_movie = None
    
    if 'user_id' not in session:
        flash("You need to log in to access recommendations.", "error")
        return redirect(url_for('signin'))

    user_id = session['user_id']

    if request.method == 'POST':
        selected_movie = request.form['movie']

        try:
            utility_fun.insert_search_history(user_id, selected_movie)
            recommended_movies = utility_fun.recommend(selected_movie)
            flash(f"Search for '{selected_movie}' added to history!", "success")
        except Exception as e:
            flash(f"An error occurred while processing your search: {e}", "error")

    return render_template('recommendation.html', movies=utility_fun.movies['title'].tolist(), recommended_movies=recommended_movies, selected_movie=selected_movie)

if __name__ == "__main__":
    utility_fun.app.run(debug=True, port=5002)
