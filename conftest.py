from __future__ import annotations

import pytest
from playwright.async_api import async_playwright
from playwright.async_api._generated import Browser as async_Browser
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Browser


# ────────────────────────────────
# SYNC FIXTURES
# ────────────────────────────────
@pytest.fixture(scope="session")
def browser_sync():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page_sync(browser_sync: Browser):
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


@pytest.fixture
async def page_async(browser_async: async_Browser):
    page = await browser_async.new_page()
    yield page
    await page.close()
