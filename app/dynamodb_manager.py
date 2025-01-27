import aioboto3
from botocore.exceptions import ClientError

from app import settings


class DynamoDBClient:

    def __init__(self, region_name: str, table_name: str, endpoint_url: str = None):
        self.region_name = region_name
        self.table_name = table_name
        self.endpoint_url = endpoint_url

    async def log_event(self, log_data: dict) -> None:
        session = aioboto3.Session()
        async with session.resource(
            "dynamodb",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        ) as dynamodb:
            table = await dynamodb.Table(self.table_name)

            try:
                await table.put_item(Item=log_data)
                print(f"Event logged: {log_data}")
            except ClientError as e:
                error_message = e.response["Error"]["Message"]
                print(f"Failed to log event: {error_message}")
                raise

    async def create_table_if_not_exists(self) -> None:
        session = aioboto3.Session()

        async with session.client(
            "dynamodb",
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY
        ) as dynamodb_client:
            try:
                response = await dynamodb_client.describe_table(TableName=self.table_name)
                table_status = response["Table"]["TableStatus"]
                print(f"Table '{self.table_name}' already exists. Status: {table_status}")
            except ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    print(f"Table '{self.table_name}' does not exist. Creating...")
                    try:
                        await dynamodb_client.create_table(
                            TableName=self.table_name,
                            KeySchema=[
                                {
                                    "AttributeName": "Location",
                                    "KeyType": "HASH"
                                }
                            ],
                            AttributeDefinitions=[
                                {
                                    "AttributeName": "Location",
                                    "AttributeType": "S"
                                }
                            ],
                            ProvisionedThroughput={
                                "ReadCapacityUnits": 5,
                                "WriteCapacityUnits": 5
                            },
                        )
                        print(f"Table '{self.table_name}' created successfully.")
                    except ClientError as creation_error:
                        print(
                            f"Error creating table '{self.table_name}': "
                            f"{creation_error.response['Error']['Message']}"
                        )
                        raise
                else:
                    error_message = e.response["Error"]["Message"]
                    print(f"Error while checking table existence: {error_message}")
                    raise