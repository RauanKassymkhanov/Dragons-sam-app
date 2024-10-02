import json
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from base.exceptions import NotFoundError
from service import DragonService, logger
from .config import settings


@event_parser(model=APIGatewayProxyEventModel)
def lambda_handler(event: APIGatewayProxyEventModel, context: LambdaContext) -> dict:
    dragon_id = event.pathParameters.get("dragon_id")
    try:
        dragon_service = DragonService(table_name=settings.TABLE_NAME)
        dragon = dragon_service.get_dragon_by_id_from_db(dragon_id)
        logger.info(f"Fetched dragon with ID {dragon_id} from the database")

        return {"statusCode": 200, "body": json.dumps(dragon.model_dump())}
    except NotFoundError as e:
        return {"statusCode": 404, "body": json.dumps({"message": str(e)})}
