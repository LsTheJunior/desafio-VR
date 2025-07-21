# consumidor_retry.py
import asyncio
import json
import logging
from notificacao_app.infra.rabbitmq.rabbitmq import get_rabbitmq_connection, publish_message
from notificacao_app.infra.storage.memoria import memoria
from notificacao_app.app.utils.utils import simular_falha

RETRY_QUEUE = "fila.notificacao.retry.lidio"
VALIDACAO_QUEUE = "fila.notificacao.validacao.lidio"
DLQ_QUEUE = "fila.notificacao.dlq.lidio"

# Configuração de logging
logger = logging.getLogger("consumidor_retry")
logging.basicConfig(level=logging.INFO)

async def processar_mensagem(message):
    """
    Processa uma mensagem da fila de retry.

    Args:
        message (Any): Mensagem recebida da fila.
    """
    try:
        # Decodificar a mensagem recebida
        mensagem = json.loads(message.body.decode())
        trace_id = mensagem["traceId"]
        logger.info(f"Mensagem recebida para retry: {mensagem}")

        # Simular atraso antes do reprocessamento
        await asyncio.sleep(3)

        if simular_falha(0.2):
            # Atualizar status para falha final no reprocessamento
            memoria.set(trace_id, {"status": "FALHA_FINAL_REPROCESSAMENTO"})
            logger.warning(f"Falha simulada no reprocessamento final para {trace_id}. Enviando para DLQ.")
            # Publicar na DLQ
            await publish_message(DLQ_QUEUE, mensagem)
            logger.info(f"Mensagem {trace_id} publicada na DLQ: {DLQ_QUEUE}")
        else:
            # Publicar na fila de validação
            await publish_message(VALIDACAO_QUEUE, mensagem)
            logger.info(f"Mensagem {trace_id} publicada na fila de validação: {VALIDACAO_QUEUE}")
            # Atualizar status para reprocessado com sucesso
            memoria.update_status(trace_id, "REPROCESSADO_COM_SUCESSO")
            logger.info(f"Status atualizado para REPROCESSADO_COM_SUCESSO para {trace_id}")
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)

async def consumidor_retry():
    """
    Consumidor para a fila de retry.
    """
    try:
        connection = await get_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(RETRY_QUEUE)

            logger.info(f"Consumidor de retry iniciado. Aguardando mensagens na fila: {RETRY_QUEUE}")

            async for message in queue:
                async with message.process():
                    await processar_mensagem(message)
    except Exception as e:
        logger.critical(f"Erro crítico no consumidor de retry: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(consumidor_retry())
