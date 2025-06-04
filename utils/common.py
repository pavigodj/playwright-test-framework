from __future__ import annotations


def broken_assets_response(page):
    broken_assets = []

    def log_failed_requests(response):
        if response.status >= 400:
            broken_assets.append((response.url, response.status))

    page.on("response", log_failed_requests)

    return broken_assets
