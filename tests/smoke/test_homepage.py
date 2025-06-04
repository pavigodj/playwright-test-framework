from __future__ import annotations

import logging

import pytest
from playwright.sync_api import Page

from utils.common import broken_assets_response

logger = logging.getLogger(__name__)


def test_homepage_title(navigate_to_homepage: Page):
    homepage_title = navigate_to_homepage.title()
    assert "Login" in homepage_title, f"Title found as {homepage_title}"


# Sample code to showcase useful markers such as xfail for failed test cases
@pytest.mark.xfail
def test_no_broken_assets(page_sync: Page, base_url):
    broken_assets = broken_assets_response(page_sync)
    page_sync.goto(base_url)
    assert not broken_assets, f"Broken assets found: {broken_assets}"
