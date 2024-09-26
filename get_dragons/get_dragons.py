import json
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from config import settings
from schemas import GetDragonsResponseModel

logger = Logger(service="dragon_service")
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION_NAME)
table = dynamodb.Table(settings.TABLE_NAME)


def get_dragons_from_db() -> list[GetDragonsResponseModel]:
    response = table.scan()
    items = response.get("Items", [])
    return [GetDragonsResponseModel(**item) for item in items]


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    dragons = get_dragons_from_db()

    logger.info(f"Fetched {len(dragons)} dragons from the database")

    return {"statusCode": 200, "body": json.dumps([dragon.model_dump() for dragon in dragons])}
