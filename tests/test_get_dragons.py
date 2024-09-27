import json
from create_dragon.create_dragon import lambda_handler as create_dragon
from get_dragons.get_dragons import lambda_handler as get_dragons
from tests.conftest import dynamodb_mock


def test_get_dragons(apigw_event, lambda_context) -> None:
    with dynamodb_mock():
        dragon = create_dragon(apigw_event, lambda_context)
        response = get_dragons(apigw_event, lambda_context)
        assert response["statusCode"] == 200

        expected_dragon = json.loads(dragon["body"])
        response_dragons = json.loads(response["body"])

        assert [expected_dragon] == response_dragons
