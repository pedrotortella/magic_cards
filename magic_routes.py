from flask import Flask, abort
import db

app = Flask(__name__)


@app.route('/movecards/<int:expansion_id>', methods=['POST'])
def move_cards(expansion_id):
    conn = db.Database()
    conn.connect()
    try:
        expansion_name = conn.is_valid_expansion(expansion_id)
        if not expansion_name:
            # Invalid expansion name
            abort(404)
        data = conn.get_by_expansion_id(expansion_id)
    finally:
        conn.close()
    print(expansion_name)
    return "expansion_name: {a}, number_of_cards: {b}".format(a=expansion_name, b=len(data))


@app.route('/moveall', methods=['GET'])
def move_all():
    return "Moveall"


@app.route('/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    return "Card id: {}".format(card_id)