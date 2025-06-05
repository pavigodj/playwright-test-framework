from __future__ import annotations

import logging

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from utils.common import broken_assets_response
from utils.common import get_credentials

logger = logging.getLogger(__name__)

# SMK-1 : Test to validate the title of homepage


def test_login_page_title(navigate_to_login: Page):
    logger.info("Validating login page title")
    homepage_title = navigate_to_login.title()
    assert "Login" in homepage_title, f"Title found as {homepage_title}"


# Sample code to showcase useful markers such as xfail for failed test cases
# SMK-2: test to check broken assets


@pytest.mark.xfail
def test_no_broken_assets(page_sync: Page, base_url):
    broken_assets = broken_assets_response(page_sync)
    page_sync.goto(base_url)
    if broken_assets:
        logger.error(f"Broken assets found at {base_url}: {broken_assets}")
    else:
        logger.info(f"No broken assets found once navigated to {base_url}")
    assert not broken_assets, f"Broken assets found: {broken_assets}"


# SMK-3 : test to verify logo


def test_logo_presence(navigate_to_login):
    login_page = LoginPage(navigate_to_login)
    login_page.logo_visibility()
    assert login_page.logo_visibility(), "Missing logo"


# SMK-4: test to check presence of username, password input fields,
# login and cant login links


def test_presence_of_elements(navigate_to_login):
    login_page = LoginPage(navigate_to_login)
    assert login_page.username_field(), "username input field missing"
    assert login_page.password_field(), "username input field missing"
    assert login_page.login_bttn(), "login button not enabled"
    assert login_page.cant_login_link(), "cant login button not enabled"


# SMK-5 : test login functionality


def test_login(navigate_to_login):
    login_page = LoginPage(navigate_to_login)
    username, password = get_credentials()
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.select_location_session(session_type="Registration Desk")
    login_page.click_login_button()
    assert (
        "Home" in navigate_to_login.title()
    ), f"Has {navigate_to_login.title()} as title"
