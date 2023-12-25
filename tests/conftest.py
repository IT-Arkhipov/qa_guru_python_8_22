import allure
import pytest
import allure_commons
import os
import config

from selene import browser, support
from utils import attach
from appium import webdriver
from config import settings


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope='function', autouse=True)
def mobile_management(context):
    settings.context = context

    with allure.step('Initialization'):
        options = config.to_driver_options()
        print(settings.remote_url)
        browser.config.driver = webdriver.Remote(
            settings.remote_url,
            options=options
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    attach.screenshot()
    attach.page_source()

    session_id = browser.driver.session_id

    with allure.step('tear down app session with id: ' + session_id):
        browser.quit()

    if settings.context == 'bstack':
        attach.video(session_id)
