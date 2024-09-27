import json
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from config import settings
from exceptions import NotFoundError
from schemas import GetDragonResponseModel

logger = Logger(service="dragon_service")
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION_NAME)
table = dynamodb.Table(settings.TABLE_NAME)


def get_dragon_by_id_from_db(dragon_id: str) -> GetDragonResponseModel:
    response = table.get_item(Key={"dragon_id": dragon_id})
    item = response.get("Item")

    if not item:
        raise NotFoundError(f"Dragon with id {dragon_id}")

    return GetDragonResponseModel(**item)


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    dragon_id = event.pathParameters.get("dragon_id")
    try:
        dragon = get_dragon_by_id_from_db(dragon_id)
        logger.info(f"Fetched dragon with ID {dragon_id} from the database")

        return {"statusCode": 200, "body": json.dumps(dragon.model_dump())}
    except NotFoundError as e:
        return {"statusCode": 404, "body": json.dumps({"message": str(e)})}
