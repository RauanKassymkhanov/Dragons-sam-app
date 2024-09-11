from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from polyfactory.factories.pydantic_factory import ModelFactory

from lambda_handler.schemas import DragonRequestModel, DragonInvalidRequestModel


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
