# consumidor_entrada.py
import asyncio
import logging
import random
import json
from notificacao_app.infra.rabbitmq.rabbitmq import get_rabbitmq_connection, publish_message
from notificacao_app.infra.storage.memoria import  memoria
from notificacao_app.app.utils.utils import simular_falha

QUEUE_NAME = "fila.notificacao.entrada.lidio"
RETRY_QUEUE = "fila.notificacao.retry.lidio"
VALIDACAO_QUEUE = "fila.notificacao.validacao.lidio"

# Configuração de logging
logger = logging.getLogger("consumidor_entrada")
logging.basicConfig(level=logging.INFO)

async def processar_mensagem(message):
    """
    Processa uma mensagem da fila de entrada.

    Args:
        message (Any): Mensagem recebida da fila.
    """
    try:
        # Decodificar a mensagem recebida
        mensagem = json.loads(message.body.decode())
        trace_id = mensagem["traceId"]
        logger.info(f"Mensagem recebida: {mensagem}")

        if simular_falha(0.15):
            # Atualizar status para falha inicial
            logger.warning(f"Falha simulada no processamento inicial para {trace_id}. Enviando para retry.")
            # Publicar na fila de retry
            await publish_message(RETRY_QUEUE, mensagem)
            logger.info(f"Mensagem {trace_id} publicada na fila de retry: {RETRY_QUEUE}")
        else:
            # Simular processamento
            await asyncio.sleep(random.uniform(1, 1.5))
            # Publicar na fila de validação
            await publish_message(VALIDACAO_QUEUE, mensagem)
            logger.info(f"Mensagem {trace_id} publicada na fila de validação: {VALIDACAO_QUEUE}")
            # Atualizar status para processado intermediário
            memoria.update_status(trace_id, "PROCESSADO_INTERMEDIARIO")
            logger.info(f"Status atualizado para PROCESSADO_INTERMEDIARIO para {trace_id}")
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)

async def consumidor_entrada():
    """
    Consumidor para a fila de entrada.
    """
    try:
        logger.info("Iniciando consumidor de entrada...")
        connection = await get_rabbitmq_connection()
        logger.info("Conexão com RabbitMQ estabelecida.")

        async with connection:
            channel = await connection.channel()
            logger.info("Canal do RabbitMQ criado.")

            queue = await channel.declare_queue(QUEUE_NAME)
            logger.info(f"Fila {QUEUE_NAME} declarada com sucesso.")

            logger.info(f"Consumidor de entrada iniciado. Aguardando mensagens na fila: {QUEUE_NAME}")

            async for message in queue:
                async with message.process():
                    await processar_mensagem(message)
    except Exception as e:
        logger.critical(f"Erro crítico no consumidor de entrada: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(consumidor_entrada())
