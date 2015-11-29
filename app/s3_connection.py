import os
import sys

from boto.s3.connection import S3Connection

import app.vars


def initialize_config():
    with open(app.vars.s3authfile, 'w') as conf:
        conf.writelines(("s3_access: <access key>\n", "s3_secret: <secret>\n"))
    print("Config file created (" + app.vars.s3authfile + "), please fill in values")
    sys.exit(1)


def get_s3_credentials():
    s3_access = None
    s3_secret = None

    if os.path.isfile(app.vars.s3authfile):
        with open(app.vars.s3authfile, 'r') as conf:
            for line in conf:
                if ':' not in line:
                    continue
                key, value = line.split(':', maxsplit=1)
                if key == 's3_access':
                    s3_access = value.strip()
                elif key == 's3_secret':
                    s3_secret = value.strip()

            if s3_access and s3_secret:
                return s3_access, s3_secret
            else:
                print(app.vars.s3authfile + " does not contain s3_access: and s3_secret:")
                sys.exit(1)
    else:
        initialize_config()


def get_s3_connection():
    access, secret = get_s3_credentials()
    return S3Connection(access, secret)
