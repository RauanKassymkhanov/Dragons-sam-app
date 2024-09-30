from aws_lambda_powertools.utilities.parser.models.dynamodb import DynamoDBStreamModel
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.utilities.typing import LambdaContext
from config import settings
from service import logger, sqs


@event_parser(model=DynamoDBStreamModel)
def lambda_handler(event: DynamoDBStreamModel, context: LambdaContext) -> None:
    for record in event.Records:
        response = sqs.send_message(
            QueueUrl=str(settings.SQS_QUEUE_URL), MessageBody=record.model_dump_json(), MessageGroupId="default"
        )
        logger.info(response)
