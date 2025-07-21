# rabbitmq.py
import aio_pika
import logging
import json

# Configuração de logging
logger = logging.getLogger("rabbitmq")
logging.basicConfig(level=logging.INFO)

RABBITMQ_URL = "amqp://bjnuffmq:gj-YQIiEXyfxQxjsZtiYDKeXIT8ppUq7@jaragua-01.lmq.cloudamqp.com/bjnuffmq"


async def get_rabbitmq_connection():
    """
    Estabelece uma conexão com o RabbitMQ.

    Returns:
        aio_pika.Connection: Conexão com o RabbitMQ.
    """
    try:
        logger.info(f"Tentando conectar ao RabbitMQ com a URL: {RABBITMQ_URL}")
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        logger.info("Conexão com RabbitMQ estabelecida com sucesso.")
        return connection
    except Exception as e:
        logger.critical(f"Erro ao conectar ao RabbitMQ: {e}", exc_info=True)
        raise


async def publish_message(queue_name: str, message: dict):
    """
    Publica uma mensagem em uma fila do RabbitMQ.

    Args:
        queue_name (str): Nome da fila.
        message (dict): Mensagem a ser publicada.
    """
    try:
        connection = await get_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()
            # Serializar a mensagem como JSON
            message_body = json.dumps(message)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key=queue_name,
            )
            logger.info(f"Mensagem publicada na fila {queue_name}: {message_body}")
    except Exception as e:
        logger.error(f"Erro ao publicar mensagem: {e}", exc_info=True)
        raise
