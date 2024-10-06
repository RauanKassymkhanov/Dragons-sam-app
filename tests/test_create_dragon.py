import json
from create_dragon.app.create_dragon import lambda_handler
from tests.conftest import dynamodb_mock


def test_create_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        response = lambda_handler(apigw_event, lambda_context)
        response_dragon = json.loads(response["body"])

        expected_data = json.loads(apigw_event.body)
        response_data = {
            "name": response_dragon["name"],
            "breed": response_dragon["breed"],
            "danger_rating": response_dragon["danger_rating"],
            "description": response_dragon["description"],
        }
        assert response["statusCode"] == 201
        assert expected_data == response_data

        dragon_id = response_dragon["dragon_id"]
        dragon_from_db = table.get_item(Key={"dragon_id": dragon_id})
        del dragon_from_db["Item"]["owner_id"]
        assert response_dragon == dragon_from_db["Item"]


def test_create_dragon_invalid_input(apigw_event_invalid, lambda_context) -> None:
    with dynamodb_mock():
        request = lambda_handler(apigw_event_invalid, lambda_context)

        assert request["statusCode"] == 400

def test_create_dragon_unauthorized(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        del apigw_event.requestContext.authorizer.claims["sub"]
        response = lambda_handler(apigw_event, lambda_context)
        assert response["statusCode"] == 401
