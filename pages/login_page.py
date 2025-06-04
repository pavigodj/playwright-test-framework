from __future__ import annotations

from playwright.async_api import Page as async_page
from playwright.sync_api import Page as sync_page

from utils.locators import HomepageLocators


class Login:
    def __init__(self, page: sync_page | async_page):
        self.page = page

    def logo_visibility(self):
        return self.page.locator(HomepageLocators.logo).is_visible()

    def username_field(self):
        return self.page.get_by_role("textbox", name="Username")

    def password_field(self):
        return self.page.get_by_role("textbox", name="Password")

    def login_bttn(self):
        return self.page.get_by_role("button", name="Log In")

    def cant_login_link(self):
        return self.page.get_by_text("Can't log In")

    def enter_username(self, username):
        self.username_field().type(username)
        # self.page.locator(HomepageLocators.username).type(username)

    def enter_password(self, password):
        self.password_field().type(password)
        # self.page.locator(HomepageLocators.password).type(password)

    def select_location_session(self, session_type):
        self.page.get_by_text(session_type).click()

    def click_login_button(self):
        self.login_bttn().click()
