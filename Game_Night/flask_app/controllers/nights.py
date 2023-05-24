from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_app.models.rate import Rating
# from flask_app import placeholder in case we need icons!

@app.route('/new/night')
def new_game_night():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    return render_template('new_game_night.html', user=user)

@app.route('/new/night/entry', methods=['POST'])
def game_night_hosting():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Night.validate_night(request.form):
        return redirect('/new/night')

    data = {
        'user_id': session['user_id'],
        'host': request.form['host'],
        'alt_host': request.form['alt_host'],
        'player_amount': request.form['player_amount'],
        'game_location': request.form['game_location'],
        'game_date': request.form['game_date'],
        'game_time': request.form['game_time'],
        'night_description': request.form['night_description'],
        'event_type': 'Game Night',
    }
    
    Night.save_night(data)
    return redirect('/dashboard')

@app.route('/gamenights')
def my_game_nights():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    game_nights = Night.get_all()
    # Might need to look into this one based on how we have the games table set atm.

    return render_template('my_game_nights.html', user=user, game_nights=game_nights)

@app.route('/gamenights/<int:night_id>')
def game_night_details(night_id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    night = Night.get_by_id(night_id)

    return render_template('game_night_details.html', user=user, night=night)