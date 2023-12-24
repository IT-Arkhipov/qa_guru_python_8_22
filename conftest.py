import allure
import pytest
import allure_commons
import os

from selene import browser, support
from utils import config, attach
from appium import webdriver

from utils.config import settings


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    with allure.step('Initialization'):
        browser.config.driver = webdriver.Remote(
            settings.remote_url,
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

    if config.runs_on_bstack:
        attach.video(session_id)