import sentry_sdk
import os
from yearn.partners.partners import partners
from yearn.partners.snapshot import process_partners

sentry_sdk.set_tag('script','partners_summary')


def main():
    process_partners(partners)

def send():
    result = os.popen('curl http://106.14.65.204:1337')
