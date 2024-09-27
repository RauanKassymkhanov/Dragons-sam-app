from datetime import datetime
from uuid import uuid4
import boto3
from aws_lambda_powertools import Logger
from config import settings
from exceptions import NotFoundError
from schemas import DragonRequestModel, DragonResponseModel

logger = Logger(service="dragon_service")
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION_NAME)
table = dynamodb.Table(settings.TABLE_NAME)
sqs = boto3.client("sqs", region_name=settings.AWS_REGION_NAME)


def create_dragon_in_db(dragon_data: DragonRequestModel) -> DragonResponseModel:
    dragon_id = str(uuid4())
    created_at = str(datetime.now())

    dragon_item = {"dragon_id": dragon_id, "created_at": created_at, **dragon_data.model_dump()}

    table.put_item(Item=dragon_item)

    return DragonResponseModel(dragon_id=dragon_id, created_at=created_at, **dragon_data.model_dump())


def get_dragons_from_db() -> list[DragonResponseModel]:
    response = table.scan()
    items = response.get("Items", [])
    return [DragonResponseModel(**item) for item in items]


def get_dragon_by_id_from_db(dragon_id: str) -> DragonResponseModel:
    response = table.get_item(Key={"dragon_id": dragon_id})
    item = response.get("Item")

    if not item:
        raise NotFoundError(f"Dragon with id {dragon_id}")

    return DragonResponseModel(**item)


def update_dragon_in_db(dragon_id: str, dragon_data: DragonRequestModel) -> DragonResponseModel:
    existing_dragon = get_dragon_by_id_from_db(dragon_id)

    updated_dragon = {**existing_dragon.model_dump(), **dragon_data.model_dump()}

    table.put_item(Item=updated_dragon)

    return DragonResponseModel(**updated_dragon)
