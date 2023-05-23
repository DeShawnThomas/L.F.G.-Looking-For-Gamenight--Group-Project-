from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.game import Game
from flask_app.models.user import User
from flask_app.models.rate import Rating
# from flask_app import placeholder in case we need icons!

@app.route('/new/night')
def new_game_night():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('new_game_night.html', user=user)

@app.route('/new/game')
def add_a_game():
    if 'user_id' not `i`n session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('add_a_game.html', user=user)

@app.route('/new/night/entry', methods=['POST'])
def game_night_hosting():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Game.validate_game_night(request.form):
        return redirect('/new/diary')

    data = {
        'user_id': session['user_id'],
        'host': request.form['host'],
        'player_amount': request.form['player_amount'],
        'game_location': request.form['game_location'],
        'game_date': request.form['game_date'],
    }

    Game.save(data)
    return redirect('/dashboard')

@app.route('/new/game/entry', methods=['POST'])
def addition_to_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Game.validate_game(request.form):
        return redirect('/new/diary')

    data = {
        'user_id': session['user_id'],
        'game_name': request.form['game_name'],
        'game_type': request.form['game_type'],
        'game_description': request.form['game_description'],
        'game_image': request.form['game_image'],
    }

    Game.save(data)
    return redirect('/dashboard')

@app.route('/collection')
def my_game_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    games = Game.get_all()

    return render_template('collection.html', user=user, games=games)

@app.route('/gamenights')
def my_game_nights():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    game_nights = Game.get_all()
    # Might need to look into this one based on how we have the games table set atm.

    return render_template('my_game_nights.html', user=user, game_nights=game_nights)

@app.route('/game/<int:id>')
def view_game(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_one(session['user_id'])

    return render_template('view_game.html', user=user, game=Game.get_one_by_id({'id': id}))

@app.route('/edit/<int:id>')
def edit_game(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_one(session['user_id'])

    return render_template('edit_game.html', user=user, game=Game.get_one_by_id({'id': id}))

@app.route('/edit/game/<int:id>', methods=['POST'])
def edit_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Game.validate_game(request.form):
        return redirect(f'/edit/{id}')

    data = {
        'id': id,
        'game_name': request.form['game_name'],
        'game_type': request.form['game_type'],
        'game_description': request.form['game_description'],
        'game_image': request.form['game_image'],
    }
    
    Game.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def never_happened(id):
    if 'user_id' not in session:
        return redirect('/logout')

    Game.delete({'id':id})
    return redirect('/dashboard')

@app.route('/rate')
def rate_game(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_one(session['user_id'])

    return render_template('past_game_nights.html', user=user, game=Game.get_all())