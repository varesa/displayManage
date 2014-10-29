import os
import sys

config_file = "displaymanage.conf"


def initialize_config():
    with open(config_file, 'w') as conf:
            conf.writelines(("s3_access: <access key>", "s3_secret: <secret>"))


def get_s3_credentials():
    s3_access = None
    s3_secret = None

    if os.path.isfile(config_file):
        with open(config_file, 'r') as conf:
            for line in conf:
                key, value = line.split(':', maxsplit=1)
                if key == 's3_access':
                    s3_access = value
                elif key == 's3_secret':
                    s3_secret = value

            if s3_access and s3_secret:
                return s3_access, s3_secret
            else:
                print(config_file + " does not contain s3_access: and s3_secret:")
                sys.exit(1)
    else:
        initialize_config()