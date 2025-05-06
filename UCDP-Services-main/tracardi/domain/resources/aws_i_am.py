from pydantic import BaseModel


class AwsIamAuth(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str


class AwsS3Auth(AwsIamAuth):
    bucket: str