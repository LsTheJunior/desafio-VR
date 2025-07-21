import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
from fastapi.testclient import TestClient
from notificacao_app.main import app
from notificacao_app.infra.storage.memoria import memoria

client = TestClient(app)

def test_consultar_status():
    # Configurar um traceId e dados iniciais na memória
    trace_id = "12345"
    memoria.set(trace_id, {"status": "RECEBIDO"})

    # Fazer a requisição para consultar o status
    response = client.get(f"/api/notificacao/status/{trace_id}")

    # Verificar a resposta inicial
    assert response.status_code == 200
    assert response.json() == {"status": "RECEBIDO"}

    # Atualizar o status na memória
    memoria.set(trace_id, {"status": "PROCESSADO"})

    # Fazer a requisição novamente para verificar a atualização
    response = client.get(f"/api/notificacao/status/{trace_id}")

    # Verificar a resposta atualizada
    assert response.status_code == 200
    assert response.json() == {"status": "PROCESSADO"}
