import allure
import pytest
import allure_commons
import os

from selene import browser, support
from utils import config, attach
from appium import webdriver

from utils.config import settings


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


@pytest.fixture(scope='function', autouse=True)
def mobile_management(request):
    settings.context = request.config.getoption("--context")
    with allure.step('Initialization'):
        browser.config.driver = webdriver.Remote(
            # settings.remote_url,
            "http://127.0.0.1:4723/wd/hub",
            options=config.to_driver_options()
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
