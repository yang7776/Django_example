from kombu import Connection, Queue, Exchange
media_exchange = Exchange('media', 'direct', durable=True)
video_queue = Queue('video', exchange=media_exchange, routing_key='video')

try:
    with Connection('redis://:seckerredis_868@10.33.70.242:6379/1') as conn:
        for i in range(2):
            producer = conn.Producer(serializer='json')
            producer.publish({'name': '/tmp/lolcat1.avi', 'size': 1301444013},
                             exchange=media_exchange, routing_key='video',
                             declare=[video_queue])
except Exception as e:
    print(f'aaaaa client start error: {e}')