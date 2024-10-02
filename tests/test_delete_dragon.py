import json
from tests.conftest import dynamodb_mock
from create_dragon.create_dragon import lambda_handler as create_dragon
from tests.factory_schemas import APIGatewayEventFactory
from delete_dragon.delete_dragon import lambda_handler as delete_dragon


def test_delete_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        dragon = create_dragon(apigw_event, lambda_context)
        dragon_id = json.loads(dragon["body"])["dragon_id"]
        deleted_event = APIGatewayEventFactory.build()
        deleted_event.pathParameters = {"dragon_id": dragon_id}

        response = delete_dragon(deleted_event, lambda_context)
        assert response["statusCode"] == 204

        response = table.get_item(Key={"dragon_id": dragon_id})
        assert response.get("Item") is None
