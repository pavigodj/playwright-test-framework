from __future__ import annotations

from playwright.async_api import Page as async_page

from utils.locators import HomepageLocators


class LoginPage:
    def __init__(self, page: async_page):
        self.page = page

    async def logo_visibility(self):
        return await self.page.locator(HomepageLocators.logo).is_visible()

    def username_field(self):
        return self.page.get_by_role("textbox", name="Username")

    def password_field(self):
        return self.page.get_by_role("textbox", name="Password")

    def login_bttn(self):
        return self.page.get_by_role("button", name="Log In")

    def cant_login_link(self):
        return self.page.get_by_text("Can't log In")

    async def enter_username(self, username):
        await self.username_field().type(username)

    async def enter_password(self, password):
        await self.password_field().type(password)

    async def select_location_session(self, session_type):
        await self.page.get_by_text(session_type).click()

    async def click_login_button(self):
        await self.login_bttn().click()

    async def login_by_enter_credentials(
        self, username, password, session_type
    ):
        await self.enter_username(username)
        await self.enter_password(password)
        await self.select_location_session(session_type)
        await self.click_login_button()

    async def is_cant_login_modal(self):
        await self.page.get_by_role("link", name="Can't log in?").click()
        return await self.page.locator(
            HomepageLocators.modal_pop_up
        ).is_visible()
