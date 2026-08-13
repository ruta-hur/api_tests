from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")
    assert steps.get_product_count() == 6, "количество товаров на странице не соответсвует ожидаемому"


def test_sorted_by_name(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("az")
    assert steps.get_product_names() == sorted(steps.get_product_names()), "Товары не отсортированы по имени a-z"

    steps.sort_items("za")
    assert steps.get_product_names() == sorted(steps.get_product_names(), reverse=True), "Товары не отсортированы по имени z-a"


def test_sorted_by_price(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.sort_items("lohi")
    assert steps.get_product_prices() == sorted(steps.get_product_prices()), "Товары не отсортированы по возрастающей цене"

    steps.sort_items("hilo")
    assert steps.get_product_prices() == sorted(steps.get_product_prices(), reverse=True), "Товары не отсортированы по убывающей цене"


def test_add_to_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")
    assert steps.get_cart_count() == 1, "Количество товаров в корзине не соответсвут выбранному"


def test_remove_from_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Fleece Jacket")
    assert steps.get_cart_count() == 1

    steps.remove_from_cart("Sauce Labs Fleece Jacket")
    assert steps.get_cart_count() == 0, "Количество товаров в корзине не изменилось"


def test_product_details_card_onesie(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")

    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Onesie")

    assert name == detail_name, "Название товара не совпадает"
    assert price == detail_price, "Цена товара не совпадает"


def test_product_details_card_jacket(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Fleece Jacket")

    name, price, detail_name, detail_price = steps.open_product_details("Sauce Labs Fleece Jacket")

    assert name == detail_name, "Название товара не совпадает"
    assert price == detail_price, "Цена товара не совпадает"

def test_remove_from_cart_sauce_labs_onesie(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")

    steps.remove_from_cart("Sauce Labs Onesie"), "Товар не был удален из корзины"

