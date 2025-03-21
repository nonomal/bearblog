from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

import logging
import requests
import traceback
import sys
from datetime import datetime
import time


def logger_test(request):
    x = 100/0


@staff_member_required
def timout_test(request):
    time.sleep(31)
    return HttpResponse("Hello, world. You're at the timeout test.")


class SlackExceptionHandler(logging.Handler):
    def emit(self, record):
        self.slack_logger(record)

    def slack_logger(self, record):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_traceback = ''.join(traceback.format_tb(exc_traceback))
        pretty_traceback = f'{exc_type.__name__}: {exc_value}\n' + formatted_traceback

        message = (
            f"*{settings.PROJECT_NAME}*\n\n"
            f"*Log Level:* {record.levelname}\n"
            f"*Log Message:* {record.getMessage()}\n"
            f"*Traceback:* ```{pretty_traceback}```\n"
            f"*Time of Log:* {datetime.now()}\n"
        )
        data = {'text': message}
        response = requests.post(settings.SLACK_WEBHOOK, json=data)
        return response.status_code
