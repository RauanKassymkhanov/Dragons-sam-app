from unittest.mock import patch, Mock
from stream_handler.stream_handler import lambda_handler


@patch("stream_handler.stream_handler.sqs.send_message", new_callable=Mock)
def test_stream_handler(mock_send_message, dynamodb_stream_event, lambda_context) -> None:
    lambda_handler(dynamodb_stream_event, lambda_context)

    assert mock_send_message.call_count == len(dynamodb_stream_event.Records)
