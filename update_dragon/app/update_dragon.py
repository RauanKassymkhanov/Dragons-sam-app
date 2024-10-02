import json
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError
from base.exceptions import NotFoundError, InvalidInputError, ForbiddenError, UnauthorizedError
from base.schemas import DragonRequestModel
from service import DragonService, logger, get_owner_id
from .config import settings


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    dragon_id = event.pathParameters.get("dragon_id")
    try:
        owner_id = get_owner_id(event)
        dragon_service = DragonService(table_name=settings.TABLE_NAME)
        dragon_request = DragonRequestModel.model_validate_json(event.body)

        updated_dragon = dragon_service.update_dragon_in_db(dragon_id, dragon_request, owner_id)

        logger.info(f"Dragon with ID {dragon_id} updated successfully")

        return {"statusCode": 200, "body": json.dumps(updated_dragon.model_dump())}
    except NotFoundError as e:
        return {"statusCode": 404, "body": json.dumps({"message": str(e)})}
    except (ValidationError, InvalidInputError) as e:
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except ForbiddenError as e:
        return {"statusCode": 403, "body": json.dumps({"message": str(e)})}
    except UnauthorizedError as e:
        return {"statusCode": 401, "body": json.dumps({"message": str(e)})}
