from flask import Flask, abort, jsonify  # Routes
import db  # MySQL
import rabbit_mq as mq  #rabiit_mq
import json
from sys import platform
import getpass
from multiprocessing.dummy import Pool


app = Flask(__name__)
pool = Pool(10)


def move_cards_method(expansion_id):
    """
    Publish to the 'moving_cards' queue of RabbitMQ the cards that have the 'expansion_id' passed by parameter.
    This expansion_id can be a list of ids or a single id
    If the expansion_id is single and does not exist, the route will return 404:Not found
    :param expansion_id: List of expansion ids or single expansion id
    :return expansion_name: The name of the expansion_id. Return '' if the expansion_id is a list
    :return count: Number of cards wrote in RabbitMQ
    """
    mq_conn = mq.rabbit_mq()
    conn = db.Database()
    expansion_name = None
    if type(expansion_id) != list:
        expansion_name = conn.is_valid_expansion(expansion_id)
        if not expansion_name:
            # Invalid expansion id
            abort(404)
    try:
        data, count = conn.get_by_expansion_id(expansion_id)
        mq_conn.publish('', 'moving_cards', json.dumps(data))
    except Exception as e:
        raise(e)
    finally:
        conn.close()
    return expansion_name, count


def move_all_assync():
    """
    This is a assync method called by moveall endpont to get all the expansion_ids in database
    and Publish to RabbitMQ all the cards that have have these ids
    """
    conn = db.Database()
    ids = conn.get_expansion_ids()
    move_cards_method(ids)
    conn.close()


@app.route('/movecards/<int:expansion_id>', methods=['POST'])
def move_cards(expansion_id):
    expansion_name, count = move_cards_method(expansion_id)
    return "expansion_name: {a}, number_of_cards: {b}".format(a=expansion_name, b=count)


@app.route('/moveall', methods=['GET'])
def move_all():
    pool.apply_async(move_all_assync)
    return jsonify({"success": True}), 202


@app.route('/card/<int:card_id>', methods=['GET'])
def get_card(card_id):
    if platform == "linux" or platform == "linux2":
        file = open("/tmp/cards_db.txt", "r")
    elif platform == "win32":
        file = open("C:\\Users\\{}\\AppData\\Local\\Temp\\cards_db.txt".format(getpass.getuser()), "r")
    data = list(set(file.readlines()))
    file.close()
    for card in data:
        card_json = json.loads(card)
        card_id = str(card_id)
        if card_json.get('GathererId') == card_id:
            return json.dumps(card_json)
    # Card Id not found
    abort(404)
