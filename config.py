import os
from typing import Literal

from pydantic import BaseModel
from dotenv import load_dotenv
from utils import file


context_type = Literal['local_emulator', 'local_real', 'bstack']


class Settings(BaseModel):
    context: context_type = 'bstack'
    user_name: str = os.getenv('user_name')
    access_key: str = os.getenv('access_key')
    app: str = os.getenv('app', '')
    remote_url: str = os.getenv('remote_url', '')


load_dotenv(file.abs_path_from_project('.env.credentials'))
settings = Settings(
    user_name=os.getenv('user_name'),
    access_key=os.getenv('access_key'),
)


def to_driver_options():
    from appium.options.android import UiAutomator2Options
    options = UiAutomator2Options()

    if settings.context not in ['local_emulator', 'local_real', 'bstack']:
        raise RuntimeError('Wrong context type!')

    load_dotenv(file.abs_path_from_project(f'.env.{settings.context}'))
    settings.app = os.getenv('app')
    settings.remote_url = os.getenv('remote_url')

    if settings.context == 'bstack':
        options.set_capability('platformVersion', '9.0')
        options.set_capability('deviceName', 'Google Pixel 3')
        options.set_capability('app', settings.app)
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
        options.set_capability('udid', os.getenv('udid'))
        options.set_capability('app', settings.app)
        options.set_capability('appWaitActivity', os.getenv('appWaitActivity'))
    return options
