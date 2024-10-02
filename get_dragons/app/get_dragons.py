import json
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from service import DragonService, logger
from .config import settings


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    dragon_service = DragonService(table_name=settings.TABLE_NAME)
    dragons = dragon_service.get_dragons_from_db()

    logger.info(f"Fetched {len(dragons)} dragons from the database")

    return {"statusCode": 200, "body": json.dumps([dragon.model_dump() for dragon in dragons])}
