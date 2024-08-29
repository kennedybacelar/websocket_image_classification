import json

import aio_pika
from aio_pika import Connection, connect_robust

from config import load_config

global_config = load_config()

host = global_config.get("rabbitmq", {}).get("host", "localhost")
port = global_config.get("rabbitmq", {}).get("port", 5672)

# RabbitMQ URL
RABBITMQ_URL = f"amqp://guest:guest@{host}:{port}/"


async def get_rabbitmq_connection() -> Connection:
    return await connect_robust(RABBITMQ_URL)


async def publish_message(event: dict, routing_key: str):
    rabbitmq_conn = await get_rabbitmq_connection()
    async with rabbitmq_conn:
        channel = await rabbitmq_conn.channel()

        message_body = json.dumps(event).encode("utf-8")
        exchange = await channel.declare_exchange("new_hero", aio_pika.ExchangeType.TOPIC, durable=True)

        await exchange.publish(aio_pika.Message(body=message_body), routing_key=routing_key)
