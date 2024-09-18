from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError
import boto3
import uuid
from datetime import datetime
from config import settings
from exceptions import InvalidInputError
from schemas import DragonRequestModel, DragonResponseModel

logger = Logger(service="dragon_service")
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION_NAME)
table = dynamodb.Table(settings.TABLE_NAME)


def create_dragon_in_db(dragon_data: DragonRequestModel) -> None:
    table.put_item(Item={"dragon_id": str(uuid.uuid4()), "created_at": str(datetime.now()), **dragon_data.model_dump()})


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    try:
        dragon_request = DragonRequestModel.model_validate_json(event.body)
    except (ValidationError, InvalidInputError) as e:
        raise InvalidInputError(f"Invalid input: {str(e)}")

    create_dragon_in_db(dragon_request)

    response_body = DragonResponseModel(**dragon_request.model_dump())

    logger.info(f"Dragon created successfully: {response_body}")

    return {"statusCode": 201, "body": response_body.model_dump_json()}
