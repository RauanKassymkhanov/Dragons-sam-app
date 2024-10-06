from delete_dragon.app.delete_dragon import lambda_handler as delete_dragon
from tests.conftest import dynamodb_mock
from tests.factory_schemas import APIGatewayEventFactory
from tests.utils import create_dragon_for_test


def test_delete_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)
        dragon_id = dragon_response.dragon_id

        deleted_event = APIGatewayEventFactory.build()
        deleted_event.pathParameters = {"dragon_id": dragon_id}

        response = delete_dragon(deleted_event, lambda_context)
        assert response["statusCode"] == 204

        response = table.get_item(Key={"dragon_id": dragon_id})
        assert response.get("Item") is None


def test_delete_dragon_forbidden(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)
        dragon_id = dragon_response.dragon_id

        deleted_event = APIGatewayEventFactory.build()
        deleted_event.pathParameters = {"dragon_id": dragon_id}
        deleted_event.requestContext.authorizer.claims["sub"] = "another owner id"

        response = delete_dragon(deleted_event, lambda_context)
        assert response["statusCode"] == 403


def test_delete_dragon_unauthorized(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)
        dragon_id = dragon_response.dragon_id

        deleted_event = APIGatewayEventFactory.build()
        deleted_event.pathParameters = {"dragon_id": dragon_id}
        del deleted_event.requestContext.authorizer.claims["sub"]

        response = delete_dragon(deleted_event, lambda_context)
        assert response["statusCode"] == 401
