# utils.py
import random
import asyncio
import logging

# Configuração de logging padrão
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("utils")


def simular_falha(probabilidade: float) -> bool:
    """
    Simula uma falha com base em uma probabilidade.

    Args:
        probabilidade (float): Probabilidade de falha (0 a 1).

    Returns:
        bool: True se falhar, False caso contrário.
    """
    return random.uniform(0, 1) < probabilidade


async def aguardar(segundos: int):
    """
    Aguarda um número específico de segundos de forma assíncrona.

    Args:
        segundos (int): Tempo em segundos para aguardar.
    """
    logger.info(f"Aguardando {segundos} segundos...")
    await asyncio.sleep(segundos)
