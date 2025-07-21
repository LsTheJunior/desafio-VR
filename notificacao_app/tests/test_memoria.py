import pytest
from notificacao_app.infra.storage.memoria import Memoria

def test_memoria_set_and_get():
    memoria = Memoria()

    # Teste de armazenamento
    memoria.set("chave1", {"status": "RECEBIDO"})
    assert memoria.get("chave1") == {"status": "RECEBIDO"}

    # Teste de atualização
    memoria.set("chave1", {"status": "PROCESSADO"})
    assert memoria.get("chave1") == {"status": "PROCESSADO"}

    # Teste de chave inexistente
    assert memoria.get("chave_inexistente") is None

def test_memoria_singleton():
    memoria1 = Memoria()
    memoria2 = Memoria()

    # Teste de instância única
    memoria1.set("chave2", {"status": "UNICO"})
    assert memoria2.get("chave2") == {"status": "UNICO"}
