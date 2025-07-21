# test_publicador.py
import pytest
from unittest.mock import AsyncMock, patch
from infra.rabbitmq.rabbitmq import publish_message


@pytest.mark.asyncio
@patch("notificacao_app.rabbitmq.get_rabbitmq_connection")
async def test_publish_message(mock_get_connection):
    # Mock the connection and channel
    mock_connection = AsyncMock()
    mock_channel = AsyncMock()
    mock_get_connection.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel

    # Call the function
    queue_name = "fila.notificacao.entrada.lidio"
    message = "test-message"
    await publish_message(queue_name, message)

    # Assert that the publish method was called with the correct parameters
    mock_channel.default_exchange.publish.assert_called_once()
    args, kwargs = mock_channel.default_exchange.publish.call_args
    assert args[0].body.decode() == message
    assert kwargs["routing_key"] == queue_name
