# Sistema de Notificações Assíncronas com FastAPI e RabbitMQ

## Descrição do Projeto
Este projeto é um sistema backend desenvolvido em Python utilizando o framework FastAPI, integrado ao RabbitMQ para gerenciar notificações assíncronas. Ele foi projetado para suportar múltiplos consumidores, reprocessamento de falhas, Dead Letter Queue (DLQ), status em memória e endpoints REST para interação.

## Funcionalidades
- **Publicação de notificações**: Envio de mensagens para filas específicas no RabbitMQ.
- **Consumidores assíncronos**: Processamento de mensagens em filas de entrada, retry, validação e DLQ.
- **Reprocessamento de falhas**: Mensagens com falhas são reencaminhadas para filas de retry ou DLQ.
- **Status em memória**: Armazenamento temporário do status das notificações.
- **Endpoints REST**: Interação com o sistema via API.

## Estrutura do Projeto
```
notificacao_app/
├── app/
│   ├── api/
│   │   └── routes.py  # Endpoints REST
│   ├── models/
│   │   └── models.py  # Modelos de dados
│   └── utils/
│       └── utils.py   # Funções utilitárias
├── infra/
│   ├── rabbitmq/
│   │   └── rabbitmq.py  # Conexão e publicação no RabbitMQ
│   └── storage/
│       └── memoria.py   # Armazenamento em memória
├── consumers/
│   ├── entrada/
│   │   └── consumidor_entrada.py  # Consumidor da fila de entrada
│   ├── retry/
│   │   └── consumidor_retry.py    # Consumidor da fila de retry
│   ├── validacao/
│   │   └── consumidor_validacao.py  # Consumidor da fila de validação
│   └── dlq/
│       └── consumidor_dlq.py      # Consumidor da fila DLQ
└── tests/
    └── test_publicador.py  # Testes unitários
```

## Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- RabbitMQ ou LavinMQ configurado e em execução

### Passos para execução
1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd notificacao_app
   ```

2. **Crie e ative o ambiente virtual**:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o RabbitMQ**:
   Certifique-se de que as filas necessárias estão criadas:
   - `fila.notificacao.entrada.lidio`
   - `fila.notificacao.retry.lidio`
   - `fila.notificacao.validacao.lidio`
   - `fila.notificacao.dlq.lidio`

5. **Execute a API**:
   ```bash
   uvicorn notificacao_app.main:app --reload
   ```

6. **Acesse a API**:
   - Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Endpoint raiz: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

7. **Execute os consumidores**:
   Cada consumidor deve ser executado separadamente. Por exemplo:
   ```bash
   python -m notificacao_app.consumers.entrada.consumidor_entrada
   ```

## Motivações Técnicas

### FastAPI
- Escolhido por sua performance e suporte a APIs assíncronas.
- Documentação automática via Swagger e OpenAPI.

### RabbitMQ
- Utilizado para gerenciar filas e garantir a entrega de mensagens.
- Suporte a Dead Letter Queue (DLQ) para mensagens com falhas.

### Estrutura Modular
- Organização em camadas para facilitar a manutenção e escalabilidade.
- Separação clara entre API, infraestrutura e consumidores.

### Testes Unitários
- Garantia de qualidade e confiabilidade do código.
- Testes para publicação de mensagens no RabbitMQ.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Formatação de Código

Todo o código foi formatado utilizando o [Black](https://black.readthedocs.io/en/stable/) para garantir conformidade com a PEP 8 e consistência no estilo de código.
