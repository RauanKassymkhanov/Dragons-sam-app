import json
from create_dragon.create_dragon import lambda_handler as create_dragon
from get_dragons.get_dragons import lambda_handler as get_dragons
from tests.conftest import dynamodb_mock
from tests.factory_schemas import APIGatewayEventFactory


def test_get_dragons(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        create_dragon(apigw_event, lambda_context)

        apigw_event_2 = APIGatewayEventFactory.build()
        create_dragon(apigw_event_2, lambda_context)

        response = get_dragons(apigw_event, lambda_context)
        response_dragons = json.loads(response["body"])
        expected_data = [json.loads(apigw_event.body), json.loads(apigw_event_2.body)]
        response_data = [
            {
                "name": response_dragons[0]["name"],
                "breed": response_dragons[0]["breed"],
                "danger_rating": response_dragons[0]["danger_rating"],
                "description": response_dragons[0]["description"],
            },
            {
                "name": response_dragons[1]["name"],
                "breed": response_dragons[1]["breed"],
                "danger_rating": response_dragons[1]["danger_rating"],
                "description": response_dragons[1]["description"],
            },
        ]
        response_data_sorted = sorted(response_data, key=lambda x: x["name"])
        expected_data_sorted = sorted(expected_data, key=lambda x: x["name"])
        assert response["statusCode"] == 200
        assert expected_data_sorted == response_data_sorted

        dragons_from_db = table.scan().get("Items", [])
        assert dragons_from_db == response_dragons
