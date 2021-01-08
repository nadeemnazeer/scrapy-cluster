from kafka import KafkaConsumer, TopicPartition

my_topic = 'events.crawled_firehose'


KAFKA_GROUP = None
KAFKA_FEED_TIMEOUT = 10
KAFKA_CONSUMER_AUTO_OFFSET_RESET = 'smallest'
KAFKA_CONSUMER_TIMEOUT = 50
KAFKA_CONSUMER_COMMIT_INTERVAL_MS = 5000
KAFKA_CONSUMER_AUTO_COMMIT_ENABLE = True
KAFKA_CONSUMER_FETCH_MESSAGE_MAX_BYTES = 10 * 1024 * 1024  # 10MB
offset = 'earliest'

consumer = KafkaConsumer(
    my_topic,
    group_id=KAFKA_GROUP,
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: m.decode('utf-8'),
    consumer_timeout_ms=KAFKA_CONSUMER_TIMEOUT,
    auto_offset_reset=offset,
    auto_commit_interval_ms=KAFKA_CONSUMER_COMMIT_INTERVAL_MS,
    enable_auto_commit=KAFKA_CONSUMER_AUTO_COMMIT_ENABLE,
    max_partition_fetch_bytes=KAFKA_CONSUMER_FETCH_MESSAGE_MAX_BYTES)
#kafka-console-consumer.sh --topic events.crawled_firehose --from-beginning --bootstrap-server localhost:9092

num_records = 0
total_bytes = 0
item = None


for message in consumer:
    val = message.value
    print(val)
