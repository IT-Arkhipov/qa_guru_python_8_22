from allure_commons._allure import step
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have, be


def test_search():

    with step('Skip wellcome screen'):
        browser.element((AppiumBy.ID, 'org.wikipedia.alpha:id/fragment_onboarding_skip_button')).click()

    with step('Type search'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia")).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('Appium')

    with step('Verify content found'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


def test_getting_started():
    with (step('Check initial page and continue')):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")
                        ).should(have.text('The Free Encyclopedia'))
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")).click()

    with (step('Check next page')):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")
                        ).should(have.text('New ways to explore'))
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")).click()

    with (step('Check next page')):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")
                        ).should(have.text('Reading lists with sync'))
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/fragment_onboarding_forward_button")).click()

    with (step('Check final initial page and accept')):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/primaryTextView")
                        ).should(have.text('Send anonymous data'))
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/acceptButton")).click()

    with (step('Check for main logo WikipediA')):
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/main_toolbar_wordmark")
                        ).should(be.visible)
