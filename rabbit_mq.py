import pika  # RabbitMQ


class rabbit_mq:
    conn = None
    channel = None

    def __init__(self):
        """
        The constructor initializes RabbitMQ connection and the channel
        Also, this constructor initializes the 'cards' exchange and the 'moving_cards' queue
        """
        self.conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.conn.channel()
        self.declare_exchange('cards')
        self.declare_queue('moving_cards',)

    def close(self):
        """
        Closes the RabbitMQ connection
        """
        self.conn.close()

    def publish(self, exchange, routing_key, body):
        """
        Publish data to RabbitMQ
        :param exchange: Exchange name
        :param routing_key: Routing key name
        :param body: Data to be published
        :return True or False
        """
        return self.channel.basic_publish(exchange, routing_key, body)

    def declare_queue(self, queue_name):
        """
        Declare a queue in RabbitMQ
        :param queue_name: Name of the queue to be declared
        :return True or False
        """
        return self.channel.queue_declare(queue_name)

    def declare_exchange(self, exchange_name):
        """
        Declare a exchange in RabbitMQ
        :param exchange_name: Name of the exchange to be declared
        :return True or False
        """
        return self.channel.exchange_declare(exchange_name)