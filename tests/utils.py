from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel

from create_dragon.app.config import settings
from shared_layer.base.schemas import DragonResponseModel, DragonRequestModel
from shared_layer.service import DragonService


def create_dragon_for_test(event: APIGatewayProxyEventModel, owner_id: str) -> DragonResponseModel:
    dragon_request = DragonRequestModel.model_validate_json(event.body)
    dragon_service = DragonService(table_name=settings.TABLE_NAME)
    return dragon_service.create_dragon_in_db(dragon_request, owner_id)
