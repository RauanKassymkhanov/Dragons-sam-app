import json
from tests.conftest import dynamodb_mock
from retrieve_dragon.app.retrieve_dragon import lambda_handler as retrieve_dragon
from tests.utils import create_dragon_for_test


def test_get_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock() as (table, created_dragon_ids):
        owner_id = apigw_event.requestContext.authorizer.claims["sub"]
        dragon_response = create_dragon_for_test(apigw_event, owner_id)

        dragon_id = dragon_response.dragon_id
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
        del dragon_from_db["Item"]["owner_id"]
        assert dragon_from_db["Item"] == response_dragon
