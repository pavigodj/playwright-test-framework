from __future__ import annotations

import logging

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from utils.common import broken_assets_response
from utils.common import fetch_requested_api
from utils.common import get_credentials

logger = logging.getLogger(__name__)

# SMK-1 : Test to validate the title of homepage


def test_login_page_title(navigate_to_login: Page):
    logger.info("Validating login page title")
    homepage_title = navigate_to_login.title()
    assert "Login" in homepage_title, f"Title found as {homepage_title}"


# Sample code to showcase useful markers(in pytest),
# such as xfail for failed test cases
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


# Combined SMK-1, SMK-3 and SMK-4 using subtests :
# To showcase that logically associated
# test cases can be combined together


def test_login_page_ui_elements(navigate_to_login, subtests):
    login_page = LoginPage(navigate_to_login)

    with subtests.test(msg="Title validation"):
        assert (
            "Login" in login_page.title()
        ), f"Title found as {login_page.title()}"

    with subtests.test(msg="Logo is visible"):
        assert login_page.logo_visibility(), "Missing logo"

    with subtests.test(msg="Username field present"):
        assert login_page.username_field(), "Username input field missing"

    with subtests.test(msg="Password field present"):
        assert login_page.password_field(), "Password input field missing"

    with subtests.test(msg="Login button enabled"):
        assert login_page.login_bttn(), "Login button not enabled"

    with subtests.test(msg="Can't log in link present"):
        assert login_page.cant_login_link(), "Can't login link not enabled"


# SMK-6 : API request validation after login
# (To check if FE is communicating with BE)


def test_login_api_called_on_login(page_sync, base_url):
    api_requests = fetch_requested_api(page_sync)
    page_sync.goto(base_url)
    username, password = get_credentials()
    login_page = LoginPage(page_sync)
    login_page.login_by_enter_credentials(
        username,
        password,
        session_type="Registration Desk",
    )

    assert any(
        "login" in url for url in api_requests
    ), "Login API not triggered!"
