import rabbit_mq as mq


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


mq_conn = mq.rabbit_mq()
mq_conn.channel.basic_consume(callback, queue='moving_cards', no_ack=True)
print("Waiting for messages. Press CTRL + C to exit")
mq_conn.channel.start_consuming()
