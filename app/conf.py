import os
import sys

config_file = "displaymanage.conf"


def initialize_config():
    with open(config_file, 'w') as conf:
            conf.writelines(("s3_access: <access key>", "s3_secret: <secret>"))
    print("Config file created (" + config_file + "), please fill in values")
    sys.exit(1)


def get_s3_credentials():
    s3_access = None
    s3_secret = None

    if os.path.isfile(config_file):
        with open(config_file, 'r') as conf:
            for line in conf:
                key, value = line.split(':', maxsplit=1)
                if key == 's3_access':
                    s3_access = value.strip()
                elif key == 's3_secret':
                    s3_secret = value.strip()

            if s3_access and s3_secret:
                return s3_access, s3_secret
            else:
                print(config_file + " does not contain s3_access: and s3_secret:")
                sys.exit(1)
    else:
        initialize_config()