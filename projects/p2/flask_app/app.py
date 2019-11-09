from flask import Flask, render_template
from model import PokeClient
app = Flask(__name__)

poke_client = PokeClient()

@app.route('/')
def index():
    pokemon = poke_client.get_pokemon_list()
    return render_template('index.html', pokemon=pokemon, pokemon_length = len(pokemon))

@app.route('/pokemon/<name>')
def pokemon_info(name):
    """
    Must show all the info for a pokemon identified by name

    Check the README for more detail
    """
    pokemon = poke_client.get_pokemon_info(name)
    return render_template('pokemon.html', pokemon=pokemon, pokemon_moves_length = len(pokemon['moves']), pokemon_abilities_length=len(pokemon['abilities']))

@app.route('/ability/<ability>')
def pokemon_with_ability(ability):
    """
    Must show a list of pokemon

    Check the README for more detail
    """
    pokemon = poke_client.get_pokemon_with_ability(ability)
    return render_template('ability.html', ability=ability, pokemon_length = len(pokemon), pokemon = pokemon)
