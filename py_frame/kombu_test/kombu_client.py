
from kombu import Connection, Queue, Exchange
from kombu.mixins import ConsumerProducerMixin



class KombuClient(ConsumerProducerMixin):

    __flag = None

    def __new__(cls, *args, **kwargs):
        if not cls.__flag:
            cls.__flag = super().__new__(cls)
        return cls.__flag

    def __init__(self, func, queue_name, url):
        self.url = url
        self.func = func
        self.connection = Connection(
            self.url,

            transport_options={"max_retries":3}
        )
        self.queue_name = queue_name
        # self._init_env()

    def get_consumers(self, Consumer, channel):
        # registry.enable('text/plain')
        print(self.connection)
        return [Consumer(queues=Queue(self.queue_name),
                         on_message=self.handle_message,)]

    def handle_message(self, message):
        result = self.func(message.payload)

        # send result back
        # if message.properties.get('reply_to'):
        #     self.producer.publish(
        #         {'result': result},
        #         exchange='', routing_key=message.properties['reply_to'],
        #         correlation_id=message.properties['correlation_id'],
        #         serializer='json',
        #         retry=True,
        #     )

        message.ack()

    def start_consuming(self):
        try:
            self.run()
        except Exception as e:
            print(f'Error: {e}')
        finally:
            print("啊啊啊啊啊啊啊啊啊啊")
            self.close()

    def clean(self):
        channel = self.connection.channel()
        channel.queue_purge(self.queue_name)

    def close(self):
        self.connection.close()

