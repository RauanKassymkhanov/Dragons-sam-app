import json
from tests.conftest import dynamodb_mock
from create_dragon.create_dragon import lambda_handler as create_dragon
from retrieve_dragon.retrieve_dragon import lambda_handler as retrieve_dragon
from tests.factory_schemas import APIGatewayEventFactory
from update_dragon.update_dragon import lambda_handler as update_dragon


def test_update_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        dragon = create_dragon(apigw_event, lambda_context)
        dragon_id = json.loads(dragon["body"])["dragon_id"]
        updated_event = APIGatewayEventFactory.build()
        updated_event.pathParameters = {"dragon_id": dragon_id}

        updated_dragon = update_dragon(updated_event, lambda_context)

        response = retrieve_dragon(updated_event, lambda_context)

        assert response["statusCode"] == 200

        expected_dragon = json.loads(updated_dragon["body"])
        response_body = json.loads(response["body"])

        assert expected_dragon == response_body
