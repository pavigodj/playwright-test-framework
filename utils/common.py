from __future__ import annotations

from cryptography.fernet import Fernet

from utils._secrets import ENCRYPTED_PASSWORD
from utils._secrets import ENCRYPTED_USERNAME
from utils._secrets import PASSWORD_KEY
from utils._secrets import USERNAME_KEY


def broken_assets_response(page):
    broken_assets = []

    def log_failed_requests(response):
        if response.status >= 400:
            broken_assets.append((response.url, response.status))

    page.on("response", log_failed_requests)

    return broken_assets


def get_credentials():
    cipher_suite = Fernet(PASSWORD_KEY)
    password = cipher_suite.decrypt(ENCRYPTED_PASSWORD.encode()).decode()
    cipher_suite = Fernet(USERNAME_KEY)
    username = cipher_suite.decrypt(ENCRYPTED_USERNAME.encode()).decode()
    return (username, password)
