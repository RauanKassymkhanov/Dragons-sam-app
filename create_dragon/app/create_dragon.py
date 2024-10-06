import json
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError
from .config import settings
from base.exceptions import InvalidInputError, UnauthorizedError
from base.schemas import DragonRequestModel
from service import DragonService, logger, get_owner_id


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    try:
        owner_id = get_owner_id(event)
        dragon_request = DragonRequestModel.model_validate_json(event.body)
        dragon_service = DragonService(table_name=settings.TABLE_NAME)
        response_body = dragon_service.create_dragon_in_db(dragon_request, owner_id)

        logger.info(f"Dragon created successfully: {response_body}")

        return {"statusCode": 201, "body": response_body.model_dump_json()}
    except (ValidationError, InvalidInputError) as e:
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except UnauthorizedError as e:
        return {"statusCode": 401, "body": json.dumps({"message": str(e)})}
