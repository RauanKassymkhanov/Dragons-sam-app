from aws_lambda_powertools.utilities.parser.models.dynamodb import DynamoDBStreamModel
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext
from service import logger, sqs
from .config import settings

queue_url = settings.SQS_QUEUE_URL


@event_parser(model=DynamoDBStreamModel)
def lambda_handler(event: DynamoDBStreamModel, context: LambdaContext) -> None:
    for record in event.Records:
        response = sqs.send_message(
            QueueUrl=str(queue_url), MessageBody=record.model_dump_json(), MessageGroupId="default"
        )
        logger.info(response)
