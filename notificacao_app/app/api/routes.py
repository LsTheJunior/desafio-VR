# routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
from notificacao_app.app.models.models import NotificacaoRequest
from notificacao_app.infra.rabbitmq.rabbitmq import publish_message
from notificacao_app.infra.storage.memoria import memoria
import logging

# Configuração de logging
logger = logging.getLogger("routes")

router = APIRouter()


@router.post("/api/notificar")
async def notificar(notificacao: NotificacaoRequest):
    """
    Endpoint para receber notificações e iniciar o pipeline de processamento assíncrono.

    Args:
        notificacao (NotificacaoRequest): Dados da notificação.

    Returns:
        dict: Trace ID e mensagem ID.
    """
    try:
        trace_id = str(uuid4())
        mensagem_id = notificacao.mensagemId or str(uuid4())

        # Atualizar status inicial no armazenamento em memória
        memoria.set(
            trace_id,
            {
                "traceId": trace_id,  
                "mensagemId": mensagem_id,
                "conteudoMensagem": notificacao.conteudoMensagem,
                "tipoNotificacao": notificacao.tipoNotificacao,
                "status": "RECEBIDO",

            },
        )

        # Publicar mensagem no RabbitMQ com metadados detalhados
        mensagem = {
            "traceId": trace_id,
            "mensagemId": mensagem_id,
            "conteudoMensagem": notificacao.conteudoMensagem,
            "tipoNotificacao": notificacao.tipoNotificacao
        }

        await publish_message(f"fila.notificacao.entrada.lidio", mensagem)

        logger.info(f"Notificação recebida e publicada: {trace_id}")
        return JSONResponse(content={"traceId": trace_id, "mensagemId": mensagem_id}, status_code=202)
    except Exception as e:
        logger.error(f"Erro ao processar notificação: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/api/notificacao/status/{traceId}")
async def consultar_status(traceId: str):
    """
    Endpoint para consultar o status de uma notificação.

    Args:
        traceId (str): ID da notificação.

    Returns:
        dict: Status da notificação.
    """
    try:
        status = memoria.get(traceId)
        if not status:
            logger.warning(f"Notificação não encontrada: {traceId}")
            raise HTTPException(status_code=404, detail="Notificação não encontrada")
        return status
    except Exception as e:
        logger.error(f"Erro ao consultar status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
