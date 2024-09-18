import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser.models.dynamodb import DynamoDBStreamModel
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext
from config import settings

sqs = boto3.client("sqs", region_name=settings.AWS_REGION_NAME)
logger = Logger(service="dragon_service")
SQS_QUEUE_URL = settings.SQS_QUEUE_URL


@event_parser(model=DynamoDBStreamModel)
def lambda_handler(event: DynamoDBStreamModel, context: LambdaContext) -> None:
    for record in event.Records:
        response = sqs.send_message(
            QueueUrl=str(SQS_QUEUE_URL), MessageBody=record.model_dump_json(), MessageGroupId="default"
        )
        logger.info(response)
