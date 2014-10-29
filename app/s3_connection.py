from boto.s3.connection import S3Connection

from .conf import get_s3_credentials


def get_s3_connection():
    access, secret = get_s3_credentials()
    return S3Connection(access, secret)