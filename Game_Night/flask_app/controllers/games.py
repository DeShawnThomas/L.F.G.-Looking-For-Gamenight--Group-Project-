from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.game import Game
from flask_app.models.user import User
from flask_app.models.night import Night
from flask_app.models.rate import Rating
# from flask_app import placeholder in case we need icons!

@app.route('/new/game')
def add_a_game():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user = User.get_by_id(session['user_id'])

    return render_template('add_a_game.html', user=user)

@app.route('/new/game/entry', methods=['POST'])
def addition_to_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Game.validate_game(request.form):
        return redirect('/new/game')

    data = {
        'user_id': session['user_id'],
        'game_name': request.form['game_name'],
        'game_type': request.form['game_type'],
        'game_description': request.form['game_description'],
        'game_image': request.form['game_image'],
    }

    Game.save_game(data)
    return redirect('/dashboard')

@app.route('/collection')
def my_game_collection():
    if 'user_id' not in session:
        return redirect('/logout')
    
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user:
        games = user.get_user_games()
    else:
        games = []

    return render_template('collection.html', user=user, games=games)


@app.route('/game/<int:id>')
def view_game(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])

    return render_template('view_game.html', user=user, game=Game.get_one_by_id({'id': id}))

@app.route('/edit/game/<int:id>')
def edit_game(id):
    if 'user_id' not in session:
        return redirect('/logout')

    user = User.get_by_id(session['user_id'])
    game = Game.get_by_id({'id': id})

    return render_template('edit_game.html', user=user, game=game)

@app.route('/edit/game/<int:id>/update', methods=['POST'])
def edit_collection(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    if not Game.validate_game(request.form):
        return redirect(f'/edit/game/{id}')

    data = {
        'id': id,
        'game_name': request.form['game_name'],
        'game_type': request.form['game_type'],
        'game_description': request.form['game_description'],
        'game_image': request.form['game_image'],
    }

    Game.update(data)
    return redirect('/dashboard')

@app.route('/delete/game/<int:id>')
def never_happened(id):
    if 'user_id' not in session:
        return redirect('/logout')

    Game.delete({'id':id})
    return redirect('/dashboard')