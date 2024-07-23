from aiokafka import AIOKafkaConsumer

from config.settings import settings
from services import storage


async def download_images() -> None:
    consumer = AIOKafkaConsumer(
        settings.broker_topic,
        bootstrap_servers=f"{settings.broker_host}:{settings.broker_port}",
        enable_auto_commit=False,
        group_id="memes",
        auto_offset_reset="earliest",
    )

    await consumer.start()
    try:
        async for msg in consumer:
            await storage.upload_image(image_name=msg.value.decode())
            await consumer.commit()

    finally:
        await consumer.stop()
