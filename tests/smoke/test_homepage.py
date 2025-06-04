from __future__ import annotations

import logging

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


def test_homepage_title(navigate_to_homepage: Page):
    homepage_title = navigate_to_homepage.title()
    assert "Login" in homepage_title, f"Title found as {homepage_title}"


def test_no_broken_assets(page_sync: Page, base_url):
    broken_assets = []

    def log_failed_requests(response):
        if response.status >= 400:
            broken_assets.append((response.url, response.status))

    page_sync.on("response", log_failed_requests)
    page_sync.goto(base_url)
    assert not broken_assets, f"Broken assets found: {broken_assets}"
