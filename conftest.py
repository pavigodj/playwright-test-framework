from __future__ import annotations

import logging
import os
from pathlib import Path

import pytest
from playwright.async_api import async_playwright
from playwright.async_api import Page as Async_Page
from playwright.async_api._generated import Browser as Async_Browser
from playwright.sync_api import Page as Sync_Page
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser as Sync_Browser

from utils.common import get_custom_log_path
from utils.settings import BASE_URL_DEV
from utils.settings import BASE_URL_STAGE

logger = logging.getLogger(__name__)


# ────────────────────────────────
# SYNC FIXTURES
# ────────────────────────────────
@pytest.fixture(scope="session")
def browser_sync(request):
    browser_type = request.config.getoption("--browser")
    if browser_type == "chromium":
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            yield browser
            browser.close()
    elif browser_type == "firefox":
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=False)
            yield browser
            browser.close()
    else:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            yield browser
            browser.close()


@pytest.fixture(scope="function")
def page_sync(browser_sync: Sync_Browser):
    page = browser_sync.new_page()
    yield page
    page.close()


# ────────────────────────────────
# ASYNC FIXTURES
# ────────────────────────────────
@pytest.fixture(scope="session")
async def browser_async():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def page_async(browser_async: Async_Browser):
    page = await browser_async.new_page()
    yield page
    await page.close()


# ------------------------------------------
# pytest annotation to handle various envs
# -------------------------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="stage",
        help="Selecting environment to run tests stage|dev",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Selecting browser type chromium|firefox|safari",
    )


@pytest.fixture(scope="session")
def env(request: pytest.FixtureRequest):
    env = request.config.getoption("--env")
    return env


@pytest.fixture(scope="session")
def browser_type(request: pytest.FixtureRequest):
    browser_type = request.config.getoption("--browser")
    return browser_type


# --------------------------------------
# Set up URL based on env
# --------------------------------------


@pytest.fixture(scope="session")
def base_url(env):
    os.environ["env"] = env

    if env == "dev":
        return BASE_URL_DEV
    elif env == "stage":
        return BASE_URL_STAGE
    else:
        return BASE_URL_STAGE


# ------------------------------------------
# Navigate to homepage fixture
# ------------------------------------------


@pytest.fixture(scope="function")
def navigate_to_login(page_sync: Sync_Page, base_url):
    try:
        logger.info("Navigating to {base_url}")
        page_sync.goto(base_url)
        yield page_sync
    except (Exception, TimeoutError) as e:
        pytest.fail(f"Unable to login to {base_url} with exception {e}")


async def navigate_to_login_async(page_async: Async_Page, base_url):
    try:
        logger.info("Navigating to {base_url}")
        await page_async.goto(base_url)
        yield page_async
    except (Exception, TimeoutError) as e:
        pytest.fail(f"Unable to login to {base_url} with exception {e}")


# -----------------------------------------------------
# HTML Test Report generation handled using hooks
# (pytest_cmdline_main : hook that gets called once before
# the tests are run, and it lets you customize the test
# execution environment.)
# -----------------------------------------------------


def pytest_cmdline_main(config):
    config.custom_log_path = get_custom_log_path()  # Custom logs directory
    html_file = str(
        config.custom_log_path / "pytest_report.html"
    )  # Final report path
    config.option.htmlpath = (
        html_file  # Set HTML report path for pytest-html plugin
    )
    config.option.self_contained_html = True  # Bundle CSS, JS into one file
    config.is_log_path_set = False  # Used as a flag for logging setup


# ----------------------------------------------------------
# this is a hook which runs before every tests
# -----------------------------------------------------------


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_setup(item):
    config = item.config
    if not config.is_log_path_set:
        logging_plugin = config.pluginmanager.get_plugin("logging-plugin")
        filename = Path("pytest_console.log")
        logging_plugin.set_log_path(str(config.custom_log_path / filename))
        config.is_log_path_set = True  # Ensure this runs only once
    yield


#  -----------------------------------------------
# Browser factory : for multiple session tests
# ------------------------------------------------


@pytest.fixture()
async def browser_factory(browser_type, request):
    browser_type = request.config.getoption("--browser")
    async with async_playwright() as p:
        launched_browsers = []

        async def create_browsers(n: int):
            for _ in range(n):
                if browser_type == "chromium":
                    browser = await p.chromium.launch(headless=True)
                elif browser_type == "firefox":
                    browser = await p.firefox.launch(headless=True)
                else:
                    browser = await p.chromium.launch(headless=True)
                launched_browsers.append(browser)
            return launched_browsers

        yield create_browsers

        for browser in launched_browsers:
            await browser.close()
