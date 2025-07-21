# consumidor_dlq.py
import asyncio
import logging
import json
from typing import Any
from notificacao_app.infra.rabbitmq.rabbitmq import get_rabbitmq_connection
from notificacao_app.infra.storage.memoria import memoria

DLQ_QUEUE = "fila.notificacao.dlq.lidio"

# Configuração de logging
logger = logging.getLogger("consumidor_dlq")
logging.basicConfig(level=logging.INFO)


async def processar_mensagem(message: Any) -> None:
    """
    Processa uma mensagem da fila DLQ.

    Args:
        message (Any): Mensagem recebida da fila.
    """
    try:
        # Decodificar a mensagem recebida
        mensagem = json.loads(message.body.decode())
        trace_id = mensagem["traceId"]
        logger.info(f"Processando mensagem na DLQ: {mensagem}")
        # Aqui você pode adicionar lógica adicional, se necessário

        # Atualizar status na DLQ
        memoria.update_status(trace_id, "PROCESSADO_DLQ")
        logger.info(f"Status atualizado para PROCESSADO_DLQ para {trace_id}")
    except Exception as e:
        logger.error(f"Erro ao processar mensagem na DLQ: {e}", exc_info=True)


async def consumidor_dlq():
    """
    Consumidor para a fila DLQ.
    """
    try:
        connection = await get_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(DLQ_QUEUE)

            logger.info(
                f"Consumidor DLQ iniciado. Aguardando mensagens na fila: {DLQ_QUEUE}"
            )

            async for message in queue:
                async with message.process():
                    await processar_mensagem(message)
    except Exception as e:
        logger.critical(f"Erro crítico no consumidor DLQ: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(consumidor_dlq())
