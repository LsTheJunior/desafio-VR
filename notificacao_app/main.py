# main.py
from fastapi import FastAPI
from notificacao_app.app.api.routes import router
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI()

# Incluindo rotas
app.include_router(router)


@app.get("/")
def read_root():
    """
    Endpoint raiz para verificar o status do sistema.

    Returns:
        dict: Mensagem de boas-vindas.
    """
    logger.info("Endpoint raiz acessado.")
    return {"message": "Sistema de Notificações Assíncronas"}
