import asyncio

from aiokafka import AIOKafkaProducer

from broker.base import IBrokerProducer

event_loop = asyncio.get_event_loop()


class KafkaProducer(IBrokerProducer):
    _producer: AIOKafkaProducer
    _topic: str

    def __init__(self, host: str, port: str, topic: str) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=f"{host}:{port}",
            loop=event_loop,
        )

        self._topic = topic

    async def produce(self, message: str) -> None:
        await self._producer.start()
        try:
            await self._producer.send_and_wait(
                topic=self._topic,
                value=message.encode(),
            )

        finally:
            await self._producer.stop()
