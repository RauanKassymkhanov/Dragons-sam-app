import json
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError
from exceptions import InvalidInputError
from schemas import DragonRequestModel
from service import create_dragon_in_db, logger


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    try:
        dragon_request = DragonRequestModel.model_validate_json(event.body)
        response_body = create_dragon_in_db(dragon_request)

        logger.info(f"Dragon created successfully: {response_body}")

        return {"statusCode": 201, "body": response_body.model_dump_json()}
    except (ValidationError, InvalidInputError) as e:
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
