# from __future__ import annotations
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from cryptography.fernet import Fernet

from utils._secrets import ENCRYPTED_PASSWORD
from utils._secrets import ENCRYPTED_USERNAME
from utils._secrets import PASSWORD_KEY
from utils._secrets import USERNAME_KEY

# To return broken assets when made a call to any event


def broken_assets_response(page):
    broken_assets = []

    def log_failed_requests(response):
        if response.status >= 400:
            broken_assets.append((response.url, response.status))

    page.on("response", log_failed_requests)

    return broken_assets


# To fetch the POST request made when an action performed in the FE


def fetch_requested_api(page):
    api_requests = []

    def track_api(request):
        if request.method == "POST":
            api_requests.append(request.url)

    page.on("request", track_api)
    return api_requests


# To fetch the credentials(can be parametrized as well),
# generally got from secrets from the environments(eg:git secrets)


def get_credentials():
    cipher_suite = Fernet(PASSWORD_KEY)
    password = cipher_suite.decrypt(ENCRYPTED_PASSWORD.encode()).decode()
    cipher_suite = Fernet(USERNAME_KEY)
    username = cipher_suite.decrypt(ENCRYPTED_USERNAME.encode()).decode()
    return (username, password)


# To set up directory structure for log file


def get_custom_log_path():
    is_ci = os.getenv("GITHUB_ACTIONS") == "true"
    c_time = datetime.now()
    if is_ci:
        # GitHub Actions uses GITHUB_WORKSPACE as working directory
        base_path = Path(os.getenv("GITHUB_WORKSPACE", ".")) / "test-reports"
    else:
        # Local environment (default)
        base_path = (
            Path.home()
            / "Reports"
            / str(c_time.year)
            / f"Month_{str(c_time.month)}"
            / f"Day_{str(c_time.day)}"
            / str(c_time.time())
        )

    base_path.mkdir(parents=True, exist_ok=True)

    if not is_ci:
        # Only create symlink locally (GitHub runners often don't
        #  support this well)

        latest_log_link_pathobj = Path.home() / "Reports" / "latest"
        if (
            latest_log_link_pathobj.exists()
            or latest_log_link_pathobj.is_symlink()
        ):
            latest_log_link_pathobj.unlink()
        latest_log_link_pathobj.symlink_to(base_path, target_is_directory=True)

    return base_path
