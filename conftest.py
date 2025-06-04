from __future__ import annotations

import os

import pytest
from playwright.async_api import async_playwright
from playwright.async_api._generated import Browser as Async_Browser
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser as Sync_Browser

from utils.settings import BASE_URL_DEV
from utils.settings import BASE_URL_STAGE


# ────────────────────────────────
# SYNC FIXTURES
# ────────────────────────────────
@pytest.fixture(scope="session")
def browser_sync() -> Sync_Browser:
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
async def browser_async() -> Async_Browser:
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
