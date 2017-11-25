import rabbit_mq as mq
from sys import platform
import getpass


def callback(ch, method, properties, body):
    if platform == "linux" or platform == "linux2":
        with open("/tmp/cards_db.txt", "a") as file:
            file.write(body.decode('UTF-8') + "\n")
            file.close()
    elif platform == "win32":
        with open("C:\\Users\\{}\\AppData\\Local\\Temp\\cards_db.txt".format(getpass.getuser()), "a") as file:
            file.write(body.decode('UTF-8') + "\n")
            file.close()
    print(" [x] Received %r" % body.decode('UTF-8'))


mq_conn = mq.rabbit_mq()
mq_conn.channel.basic_consume(callback, queue='moving_cards', no_ack=True)
print("Waiting for messages. Press CTRL + C to exit")
mq_conn.channel.start_consuming()
