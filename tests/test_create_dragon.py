import json
from create_dragon.create_dragon import lambda_handler
import pytest
from create_dragon.exceptions import InvalidInputError
from tests.conftest import dynamodb_mock


def test_lambda_handler(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        request = lambda_handler(apigw_event, lambda_context)
        expected_data = json.loads(apigw_event.body)
        request_body = json.loads(request["body"])
        response_data = {
            "name": request_body["name"],
            "breed": request_body["breed"],
            "danger_rating": request_body["danger_rating"],
            "description": request_body["description"],
        }
        assert response_data == expected_data


def test_lambda_handler_invalid_input(apigw_event_invalid, lambda_context) -> None:
    with dynamodb_mock():
        with pytest.raises(InvalidInputError) as exc_info:
            lambda_handler(apigw_event_invalid, lambda_context)

        assert "Invalid input" in str(exc_info.value)
