from broker.base import IBrokerProducer
from broker.kafka import KafkaProducer
from config.settings import settings


def get_producer() -> IBrokerProducer:
    return KafkaProducer(
        host=settings.broker_host,
        port=settings.broker_port,
        topic=settings.broker_topic,
    )
