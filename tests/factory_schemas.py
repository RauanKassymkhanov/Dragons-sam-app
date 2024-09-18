from aws_lambda_powertools.utilities.parser.models import (
    APIGatewayProxyEventModel,
    DynamoDBStreamModel,
    DynamoDBStreamRecordModel,
    DynamoDBStreamChangedRecordModel,
)
from polyfactory.factories.pydantic_factory import ModelFactory

from create_dragon.schemas import DragonRequestModel, DragonInvalidRequestModel


class DragonBodyCreateFactory(ModelFactory[DragonRequestModel]):
    __model__ = DragonRequestModel


class DragonInvalidBodyCreateFactory(ModelFactory[DragonInvalidRequestModel]):
    __model__ = DragonInvalidRequestModel


class APIGatewayEventFactory(ModelFactory[APIGatewayProxyEventModel]):
    __model__ = APIGatewayProxyEventModel

    @classmethod
    def process_kwargs(cls, **kwargs) -> dict:
        kwargs["requestContext"] = {"messageId": None}
        return super().process_kwargs(**kwargs)

    @classmethod
    def body(cls) -> str:
        dragon_data = DragonBodyCreateFactory.build()
        return dragon_data.model_dump_json()


class APIGatewayInvalidEventFactory(ModelFactory[APIGatewayProxyEventModel]):
    __model__ = APIGatewayProxyEventModel

    @classmethod
    def process_kwargs(cls, **kwargs) -> dict:
        kwargs["requestContext"] = {"messageId": None}
        return super().process_kwargs(**kwargs)

    @classmethod
    def body(cls) -> str:
        dragon_data = DragonInvalidBodyCreateFactory.build()
        return dragon_data.model_dump_json()


class DynamoDBStreamChangedRecordFactory(ModelFactory[DynamoDBStreamChangedRecordModel]):
    __model__ = DynamoDBStreamChangedRecordModel

    @classmethod
    def NewImage(cls):
        return None

    @classmethod
    def OldImage(cls):
        return None


class DynamoDBStreamRecordFactory(ModelFactory[DynamoDBStreamRecordModel]):
    __model__ = DynamoDBStreamRecordModel

    @classmethod
    def dynamodb(cls) -> DynamoDBStreamChangedRecordModel:
        return DynamoDBStreamChangedRecordFactory.build()


class DynamodbStreamEventFactory(ModelFactory[DynamoDBStreamModel]):
    __model__ = DynamoDBStreamModel

    @classmethod
    def Records(cls) -> list:
        return [DynamoDBStreamRecordFactory.build()]
