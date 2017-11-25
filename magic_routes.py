from flask import Flask, abort  # Routes
import db  # MySQL
import rabbit_mq as mq  #rabiit_mq
import json
from sys import platform
import getpass

app = Flask(__name__)


@app.route('/movecards/<int:expansion_id>', methods=['POST'])
def move_cards(expansion_id):
    mq_conn = mq.rabbit_mq()
    conn = db.Database()
    try:
        expansion_name = conn.is_valid_expansion(expansion_id)
        if not expansion_name:
            # Invalid expansion id
            abort(404)
        data, count = conn.get_by_expansion_id(expansion_id)
        for row in data:
            print(row)
            mq_conn.publish('', 'moving_cards', json.dumps(row))
    except Exception as e:
        raise(e)
    finally:
        conn.close()
    print(expansion_name)
    return "expansion_name: {a}, number_of_cards: {b}".format(a=expansion_name, b=count)


@app.route('/moveall', methods=['GET'])
def move_all():
    return "Moveall"


@app.route('/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    if platform == "linux" or platform == "linux2":
        file = open("/tmp/cards_db.txt", "r")
    elif platform == "win32":
        file = open("C:\\Users\\{}\\AppData\\Local\\Temp\\cards_db.txt".format(getpass.getuser()), "r")
    data = file.readlines()
    file.close()
    for card in data:
        card_json = json.loads(card)
        card_id = str(card_id)
        if card_json.get('GathererId') == card_id:
            return json.dumps(card_json)
    # Card Id not found
    abort(404)
