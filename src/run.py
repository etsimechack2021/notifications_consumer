#!/usr/bin/python
import logging
import os

from notifications.consumer import Consumer

logging.basicConfig(level=logging.DEBUG)


def check_env_variables():
    logging.debug("Checking required environment variables")

    mandatory_env_vars = []#["PROMETHEUS_PUSH_GATEWAY"]

    for var in mandatory_env_vars:
        if var not in os.environ:
            print("Failed because {} is not set.\n".format(var))
            help()

    print("Environment variables:")
    for var in mandatory_env_vars:
        print("\t"+var+": "+os.getenv(var))


def help():
    print("Required environment variables:")
    print("\tPROMETHEUS_PUSH_GATEWAY: URL where the PROMETHEUS PUSH_GATEWAY will be running")
    exit(0)


def main():
    check_env_variables()    
    consumer_api = Consumer()
    consumer_api.start()
    
if __name__ == '__main__':
    main()
