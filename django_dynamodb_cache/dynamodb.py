import boto3
from botocore.exceptions import ClientError

from .helper import logger


def get_dynamodb(settings):
    session = boto3.session.Session()
    region = settings.aws_region_name or session.region_name
    dynamodb = boto3.resource("dynamodb", region_name=region)
    return dynamodb


def get_table(settings, dynamodb):
    return dynamodb.Table(settings.table_name)


def create_table(settings, dynamodb):
    table = None
    exists = False
    try:
        kwargs = {
            "TableName": settings.table_name,
            "KeySchema": [
                {
                    "AttributeName": settings.key_column,
                    "KeyType": "HASH",  # Partition key
                }
            ],
            "AttributeDefinitions": [{"AttributeName": settings.key_column, "AttributeType": "S"}],
            "BillingMode": "PAY_PER_REQUEST" if settings.is_on_demand else "PROVISIONED",
        }
        if not settings.is_on_demand:
            kwargs["ProvisionedThroughput"] = {
                "ReadCapacityUnits": settings.read_capacity_units,
                "WriteCapacityUnits": settings.write_capacity_units,
            }
        table = dynamodb.create_table(**kwargs)
    except ClientError as e:
        if e.response["Error"]["Code"] == "LimitExceededException":
            logger.warn("API call limit exceeded; backing off and retrying...")
            raise e
        elif e.response["Error"]["Code"] == "ResourceInUseException":
            logger.info("Table %s already exists", settings.table_name)
            exists = True
        else:
            raise e

    if not table:
        table = dynamodb.Table(settings.table_name)

    logger.info("Waiting %s status: %s", table.table_name, table.table_status)
    table.meta.client.get_waiter("table_exists").wait(TableName=settings.table_name)
    table = dynamodb.Table(settings.table_name)

    if not exists:
        create_ttl(table, settings)

    logger.info("Table %s status: %s", table.table_name, table.table_status)

    return table


def create_ttl(table, settings):
    try:
        response = table.meta.client.update_time_to_live(  # noqa
            TableName=settings.table_name,
            TimeToLiveSpecification={
                "Enabled": True,
                "AttributeName": settings.expiration_column,
            },
        )
        return True
    except Exception as e:
        logger.exception("Error on TTL creation", exc_info=e)
        return False
