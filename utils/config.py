import os
from typing import Literal

from pydantic import BaseModel
from dotenv import load_dotenv
from utils import file


class Settings(BaseModel):
    context: Literal['local_emulator', 'local_real', 'bstack'] = 'bstack'
    user_name: str = os.getenv('user_name')
    access_key: str = os.getenv('access_key')
    app: str = os.getenv('app', '')
    remote_url: str = os.getenv('remote_url', '')


load_dotenv(file.abs_path_from_project('.env.credentials'))
settings = Settings(
    user_name=os.getenv('user_name'),
    access_key=os.getenv('access_key'),
)
load_dotenv(file.abs_path_from_project(f'.env.{settings.context}'))
settings.app = os.getenv('app')
settings.remote_url = os.getenv('remote_url')

runs_on_bstack = os.getenv('app').startswith('bs://')


def to_driver_options():
    from appium.options.android import UiAutomator2Options
    options = UiAutomator2Options()

    if settings.context == 'bstack':
        options.set_capability('platformVersion', '9.0')
        options.set_capability(
            'bstack:options', {
                'projectName': 'First Python project',
                'buildName': 'browserstack-build-1',
                'sessionName': 'BStack first_test',

                'userName': settings.user_name,
                'accessKey': settings.access_key,
            },
        )
    else:
        options.set_capability('appWaitActivity', os.getenv('appWaitActivity'))
        options.set_capability('udid', os.getenv('udid'))
    return options
