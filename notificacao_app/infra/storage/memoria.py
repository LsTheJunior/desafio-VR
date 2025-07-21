# memoria.py
from typing import Dict, Any
import logging
import threading

# Configuração de logging
logger = logging.getLogger("memoria")
logging.basicConfig(level=logging.INFO)


class Memoria:
    """
    Singleton para armazenamento em memória com segurança para threads.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Verificação dupla
                    cls._instance = super(Memoria, cls).__new__(cls)
                    cls._instance.data = {}
                    logger.info("Instância de Memoria criada.")
        return cls._instance

    def set(self, key: str, value: Dict[str, Any]):
        """
        Atualiza ou armazena um valor associado a uma chave.

        Args:
            key (str): Chave para o valor.
            value (Dict[str, Any]): Dicionário contendo os dados a serem armazenados ou atualizados.
        """
        if not key:
            logger.error("Chave inválida fornecida para set.")
            return
        if not isinstance(value, dict):
            logger.error("O valor fornecido deve ser um dicionário.")
            return
        with self._lock:
            existing_value = self.data.get(key, {})
            if not isinstance(existing_value, dict):
                existing_value = {}
            updated_value = {**existing_value, **value}
            logger.info(f"Set: {key} -> {updated_value} (anterior: {existing_value})")
            self.data[key] = updated_value

    def get(self, key: str) -> Dict[str, Any]:
        """
        Recupera um valor associado a uma chave.

        Args:
            key (str): Chave do valor.

        Returns:
            Dict[str, Any]: Dicionário associado à chave, ou None se não existir.
        """
        if not key:
            logger.error("Chave inválida fornecida para get.")
            return None
        with self._lock:
            value = self.data.get(key)
            if value is None:
                logger.warning(f"Chave não encontrada: {key}")
            else:
                logger.info(f"Get: {key} -> {value}")
            return value
            
    def update_status(self, key: str, status: str) -> bool:
        """
        Atualiza apenas o status de uma entrada existente. Se a entrada não existir,
        cria uma nova com o status especificado.
        
        Args:
            key (str): Chave da notificação.
            status (str): Novo status a ser definido.
            
        Returns:
            bool: True se atualizado com sucesso, False caso contrário.
        """
        if not key or not status:
            logger.error(f"Chave ou status inválido: key={key}, status={status}")
            return False
            
        with self._lock:
            # Verifica se a chave existe
            existing_data = self.data.get(key, {})
            if not existing_data:
                logger.warning(f"Chave não encontrada, criando nova entrada: {key}")
                existing_data = {"traceId": key, "status": "RECEBIDO"}
            
            # Guarda o status anterior para logging
            old_status = existing_data.get("status", "DESCONHECIDO")
            
            # Atualiza apenas o campo status
            existing_data["status"] = status
            
            logger.info(f"Status atualizado: {key} -> {old_status} -> {status}")
            
            # Salva os dados atualizados de volta no dicionário
            self.data[key] = existing_data
            
            # Confirma que os dados foram salvos
            saved_status = self.data[key].get("status")
            logger.info(f"Verificação: status salvo = {saved_status}")
            
            return saved_status == status

# Instância global de Memoria
memoria = Memoria()
