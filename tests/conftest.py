import os
from contextlib import contextmanager
from unittest.mock import Mock
import boto3
import pytest
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel, DynamoDBStreamModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from moto import mock_aws
from moto.dynamodb.models import Table
from tests.factory_schemas import APIGatewayEventFactory, APIGatewayInvalidEventFactory, DynamodbStreamEventFactory


def pytest_configure(config: pytest.Config):
    """
    This hook is called for every plugin and conftest file after command line options have been parsed.
    It configures the environment variables for testing.
    """
    os.environ["ENVIRONMENT"] = "test"
    os.environ["AWS_REGION_NAME"] = "us-east-1"
    os.environ["TABLE_NAME"] = "dragons-test-db"
    os.environ["SQS_QUEUE_URL"] = "https://sqs.us-east-1.amazonaws.com/123456789012/sqs"


@pytest.fixture()
def apigw_event() -> APIGatewayProxyEventModel:
    dragon_data = APIGatewayEventFactory.build()
    return dragon_data


@pytest.fixture()
def apigw_event_invalid() -> APIGatewayProxyEventModel:
    dragon_data = APIGatewayInvalidEventFactory.build()

    return dragon_data


@pytest.fixture()
def dynamodb_stream_event() -> DynamoDBStreamModel:
    event_data = DynamodbStreamEventFactory.build()

    return event_data


@contextmanager
def dynamodb_mock() -> Table:
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="dragons-test-db",
            KeySchema=[{"AttributeName": "dragon_id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "dragon_id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="dragons-test-db")
        created_dragon_ids = []

        yield table, created_dragon_ids

        with table.batch_writer() as batch:
            for dragon_id in created_dragon_ids:
                batch.delete_item(Key={"dragon_id": dragon_id})


@pytest.fixture
def lambda_context() -> LambdaContext:
    context = Mock()
    context.function_name = "dragon_create_function"
    context.memory_limit_in_mb = 128
    context.invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:dragon_create_function"
    context.aws_request_id = "fake_request_id"
    return context
