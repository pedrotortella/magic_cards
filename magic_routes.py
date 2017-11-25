from flask import Flask


app = Flask(__name__)


@app.route('/movecards/<int:expansion_id>', methods=['POST'])
def move_cards(expansion_id):

    return "Expansion id: {}".format(expansion_id)


@app.route('/moveall>', methods=['GET'])
def move_cards():
    return "Moveall"


@app.route('/card/<int:card_id>', methods=['GET'])
def move_cards(card_id):
    return "Card id: {}".format(card_id)