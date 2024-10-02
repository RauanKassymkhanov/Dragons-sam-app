import json
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from base.exceptions import NotFoundError, ForbiddenError, UnauthorizedError
from service import DragonService, logger, get_owner_id
from .config import settings


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    dragon_id = event.pathParameters.get("dragon_id")
    try:
        owner_id = get_owner_id(event)
        dragon_service = DragonService(table_name=settings.TABLE_NAME)
        dragon_service.delete_dragon_from_db(dragon_id, owner_id)

        logger.info(f"Deleted dragon with ID {dragon_id} from the database")

        return {"statusCode": 204}
    except NotFoundError as e:
        return {"statusCode": 404, "body": json.dumps({"message": str(e)})}
    except ForbiddenError as e:
        return {"statusCode": 403, "body": json.dumps({"message": str(e)})}
    except UnauthorizedError as e:
        return {"statusCode": 401, "body": json.dumps({"message": str(e)})}
