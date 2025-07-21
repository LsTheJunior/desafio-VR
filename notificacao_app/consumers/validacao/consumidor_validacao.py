# consumidor_validacao.py
import asyncio
import logging
import random
import json
from notificacao_app.infra.rabbitmq.rabbitmq import get_rabbitmq_connection, publish_message
from notificacao_app.infra.storage.memoria import memoria
from notificacao_app.app.utils.utils import simular_falha

VALIDACAO_QUEUE = "fila.notificacao.validacao.lidio"
DLQ_QUEUE = "fila.notificacao.dlq.lidio"

# Configuração de logging
logger = logging.getLogger("consumidor_validacao")
logging.basicConfig(level=logging.INFO)

async def processar_mensagem(message):
    """
    Processa uma mensagem da fila de validação.

    Args:
        message (Any): Mensagem recebida da fila.
    """
    try:
        # Decodificar a mensagem recebida
        mensagem = json.loads(message.body.decode())
        trace_id = mensagem["traceId"]
        tipo_notificacao = mensagem["tipoNotificacao"]
        logger.info(f"Mensagem recebida para validação: {mensagem}")

        # Simular envio baseado no tipo de notificação
        await asyncio.sleep(random.uniform(0.5, 1))

        if simular_falha(0.05):
            # Atualizar status para falha no envio final
            memoria.set(trace_id, {"status": "FALHA_ENVIO_FINAL"})
            logger.warning(f"Falha simulada no envio final para {trace_id}. Enviando para DLQ.")
            # Publicar na DLQ
            await publish_message(DLQ_QUEUE, mensagem)
            logger.info(f"Mensagem {trace_id} publicada na DLQ: {DLQ_QUEUE}")
        else:
            # Atualizar status para enviado com sucesso
            memoria.update_status(trace_id, "ENVIADO_SUCESSO")
            logger.info(f"Status atualizado para ENVIADO_SUCESSO para {trace_id}")
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)

async def consumidor_validacao():
    """
    Consumidor para a fila de validação.
    """
    try:
        connection = await get_rabbitmq_connection()
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(VALIDACAO_QUEUE)

            logger.info(f"Consumidor de validação iniciado. Aguardando mensagens na fila: {VALIDACAO_QUEUE}")

            async for message in queue:
                async with message.process():
                    await processar_mensagem(message)
    except Exception as e:
        logger.critical(f"Erro crítico no consumidor de validação: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(consumidor_validacao())
