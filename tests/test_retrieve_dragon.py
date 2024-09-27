import json
from retrieve_dragon.retrieve_dragon import lambda_handler as retrieve_dragon
from tests.conftest import dynamodb_mock
from create_dragon.create_dragon import lambda_handler as create_dragon


def test_get_dragon(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        dragon = create_dragon(apigw_event, lambda_context)

        dragon_id = json.loads(dragon["body"])["dragon_id"]

        apigw_event.pathParameters = {"dragon_id": dragon_id}

        response = retrieve_dragon(apigw_event, lambda_context)

        assert response["statusCode"] == 200

        expected_dragon = json.loads(dragon["body"])
        response_body = json.loads(response["body"])

        assert expected_dragon == response_body
