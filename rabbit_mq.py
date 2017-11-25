import pika  # RabbitMQ


class rabbit_mq:
    conn = None
    channel = None

    def __init__(self):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.conn.channel()
        self.declare_exchange('cards')
        self.declare_queue('moving_cards',)

    def close(self):
        self.conn.close()

    def publish(self, exchange, routing_key, body):
        return self.channel.basic_publish(exchange, routing_key, body)

    def declare_queue(self, queue_name):
        return self.channel.queue_declare(queue_name)

    def declare_exchange(self, exchange_name):
        return self.channel.exchange_declare(exchange_name)