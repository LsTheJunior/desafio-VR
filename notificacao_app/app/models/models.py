# models.py
from pydantic import BaseModel
from typing import Optional


class NotificacaoRequest(BaseModel):
    mensagemId: Optional[str]
    conteudoMensagem: str
    tipoNotificacao: str  # EMAIL, SMS, PUSH


class NotificacaoStatus(BaseModel):
    traceId: str
    mensagemId: str
    conteudoMensagem: str
    tipoNotificacao: str
    status: str
