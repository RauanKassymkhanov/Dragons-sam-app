from datetime import datetime
from uuid import uuid4
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser.models import APIGatewayProxyEventModel
from botocore.exceptions import ClientError
from base.config import settings
from base.exceptions import NotFoundError, ForbiddenError, UnauthorizedError
from base.schemas import DragonRequestModel, DragonResponseModel

logger = Logger(service="dragon_service")
sqs = boto3.client("sqs", region_name=settings.AWS_REGION_NAME)


def get_owner_id(event: APIGatewayProxyEventModel) -> str:
    owner_id = event.requestContext.authorizer.claims.get("sub")
    if not owner_id:
        raise UnauthorizedError
    return owner_id


class DragonService:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION_NAME)
        self.table = self.dynamodb.Table(table_name)

    def create_dragon_in_db(self, dragon_data: DragonRequestModel, owner_id: str) -> DragonResponseModel:
        dragon_id = str(uuid4())
        created_at = str(datetime.now())
        dragon_item = {
            "owner_id": owner_id,
            "dragon_id": dragon_id,
            "created_at": created_at,
            **dragon_data.model_dump(),
        }
        self.table.put_item(Item=dragon_item)
        return DragonResponseModel(dragon_id=dragon_id, created_at=created_at, **dragon_data.model_dump())

    def get_dragons_from_db(self) -> list[DragonResponseModel]:
        response = self.table.scan()
        items = response.get("Items", [])
        return [DragonResponseModel(**item) for item in items]

    def get_dragon_by_id_from_db(self, dragon_id: str) -> DragonResponseModel:
        response = self.table.get_item(Key={"dragon_id": dragon_id})
        item = response.get("Item")
        if not item:
            raise NotFoundError(f"Dragon with id {dragon_id}")
        return DragonResponseModel(**item)

    def update_dragon_in_db(
        self, dragon_id: str, dragon_data: DragonRequestModel, owner_id: str
    ) -> DragonResponseModel:
        try:
            response = self.table.update_item(
                Key={"dragon_id": dragon_id},
                UpdateExpression="SET #name=:n, breed=:b, danger_rating=:d, description=:desc",
                ConditionExpression="owner_id = :owner_id",
                ExpressionAttributeNames={"#name": "name"},
                ExpressionAttributeValues={
                    ":n": dragon_data.name,
                    ":b": dragon_data.breed,
                    ":d": dragon_data.danger_rating,
                    ":desc": dragon_data.description,
                    ":owner_id": owner_id,
                },
                ReturnValues="ALL_NEW",
            )
            updated_dragon = response["Attributes"]
            return DragonResponseModel(**updated_dragon)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ForbiddenError

    def delete_dragon_from_db(self, dragon_id: str, owner_id: str) -> None:
        try:
            self.table.delete_item(
                Key={"dragon_id": dragon_id},
                ConditionExpression="owner_id = :owner_id",
                ExpressionAttributeValues={":owner_id": owner_id},
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                raise ForbiddenError
