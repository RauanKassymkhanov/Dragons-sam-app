import json

from tests.conftest import dynamodb_mock
from create_dragon.create_dragon import lambda_handler as create_dragon
from tests.factory_schemas import APIGatewayEventFactory
from update_dragon.update_dragon import lambda_handler as update_dragon


def test_update_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        dragon = create_dragon(apigw_event, lambda_context)
        dragon_id = json.loads(dragon["body"])["dragon_id"]
        updated_event = APIGatewayEventFactory.build()
        updated_event.pathParameters = {"dragon_id": dragon_id}

        updated_dragon = update_dragon(updated_event, lambda_context)
        response_dragon = json.loads(updated_dragon["body"])
        expected_data = json.loads(updated_event.body)
        response_data = {
            "name": response_dragon["name"],
            "breed": response_dragon["breed"],
            "danger_rating": response_dragon["danger_rating"],
            "description": response_dragon["description"],
        }
        assert updated_dragon["statusCode"] == 200
        assert expected_data == response_data

        dragon_from_db = table.get_item(Key={"dragon_id": dragon_id})
        assert dragon_from_db["Item"] == response_dragon
