import json
from tests.conftest import dynamodb_mock
from tests.factory_schemas import APIGatewayEventFactory
from tests.utils import create_dragon_for_test
from update_dragon.app.update_dragon import lambda_handler as update_dragon


def test_update_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)

        dragon_id = dragon_response.dragon_id
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
        del dragon_from_db["Item"]["owner_id"]
        assert dragon_from_db["Item"] == response_dragon


def test_update_dragon_forbidden(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)

        dragon_id = dragon_response.dragon_id
        updated_event = APIGatewayEventFactory.build()
        updated_event.pathParameters = {"dragon_id": dragon_id}
        updated_event.requestContext.authorizer.claims["sub"] = "another owner_id"

        updated_dragon = update_dragon(updated_event, lambda_context)
        assert updated_dragon["statusCode"] == 403


def test_update_dragon_unauthorized(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)

        dragon_id = dragon_response.dragon_id
        updated_event = APIGatewayEventFactory.build()
        updated_event.pathParameters = {"dragon_id": dragon_id}
        del updated_event.requestContext.authorizer.claims["sub"]

        updated_dragon = update_dragon(updated_event, lambda_context)
        assert updated_dragon["statusCode"] == 401
