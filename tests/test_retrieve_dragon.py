import json
from retrieve_dragon.retrieve_dragon import lambda_handler as retrieve_dragon
from tests.conftest import dynamodb_mock
from create_dragon.create_dragon import lambda_handler as create_dragon


def test_get_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        dragon = create_dragon(apigw_event, lambda_context)
        dragon_id = json.loads(dragon["body"])["dragon_id"]
        apigw_event.pathParameters = {"dragon_id": dragon_id}

        response = retrieve_dragon(apigw_event, lambda_context)
        response_dragon = json.loads(response["body"])
        expected_data = json.loads(apigw_event.body)
        response_data = {
            "name": response_dragon["name"],
            "breed": response_dragon["breed"],
            "danger_rating": response_dragon["danger_rating"],
            "description": response_dragon["description"],
        }
        assert response["statusCode"] == 200
        assert expected_data == response_data

        dragon_from_db = table.get_item(Key={"dragon_id": dragon_id})
        assert dragon_from_db["Item"] == response_dragon
