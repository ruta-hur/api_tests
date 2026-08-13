from playwright.sync_api import Page, expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.steps.login_steps import LoginSteps


def test_auth_valid(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Нет товаров на странице каталога"


def test_auth_invalid(page: Page):
    # заблокированный пользователь
    steps = LoginSteps(page)
    steps.open_login_page().login("locked_out_user", "secret_sauce")

    error_text = steps.login_page.get_error()
    assert "locked out" in error_text, "Нет сообщения о заблоккированном пользователе"


def test_logout(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Нет товаров на странице каталога"

    catalog_page.logout()
    expect(page).to_have_url(LoginPage.URL)


def test_logout_visual_user(page: Page):
    steps = LoginSteps(page)
    steps.open_login_page().login("visual_user", "secret_sauce")
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Нет товаров на странице каталога"

    catalog_page.logout()
    expect(page).to_have_url(LoginPage.URL)