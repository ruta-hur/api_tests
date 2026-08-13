from playwright.sync_api import expect
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps


def test_add_item_and_check_in_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Fleece Jacket")

    basket = BasketSteps(page)
    basket.open_shopping_cart()
    assert "Sauce Labs Fleece Jacket" in basket.get_cart_item_names(), "Товар не был добавлен в корзину"

def test_add_items_and_check_in_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Backpack")
    steps.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket = BasketSteps(page)
    basket.open_shopping_cart()
    assert "Sauce Labs Backpack" and "Sauce Labs Bolt T-Shirt" in basket.get_cart_item_names(), "Товар(ы) не добавлен(ы) в корзину"


def test_remove_item_from_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Onesie")

    basket = BasketSteps(page)
    basket.open_shopping_cart()
    basket.remove_item_from_cart("Sauce Labs Onesie")
    expect(basket.get_cart_item("Sauce Labs Onesie")).to_have_count(0), "Товар не был удален из корзины"

def test_remove_items_from_cart(page):
    steps = CatalogSteps(page)
    steps.login("standard_user", "secret_sauce")

    steps.add_to_cart("Sauce Labs Backpack")
    steps.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket = BasketSteps(page)
    basket.open_shopping_cart()

    basket.remove_item_from_cart("Sauce Labs Backpack")
    expect(basket.get_cart_item("Sauce Labs Backpack")).to_have_count(0), "Товар не был удален из корзины"

    basket.remove_item_from_cart("Test.allTheThings() T-Shirt (Red)")
    expect(basket.get_cart_item("Test.allTheThings() T-Shirt (Red)")).to_have_count(0), "Товар не был удален из корзины"

def test_checkout_multiple_items(page):
    catalog = CatalogSteps(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket = BasketSteps(page)
    basket.open_shopping_cart()
    basket.get_items_total_price()
    basket.checkout()

    checkout = CheckoutSteps(page)
    checkout.enter_first_name("Anna")
    checkout.enter_last_name("Green")
    checkout.enter_zip_postal_code("1234567899")
    checkout.continue_placing_order()

    total = checkout.get_items_total()
    subtotal = checkout.get_items_subtotal()
    tax = checkout.get_items_tax()
    assert total == round(subtotal + tax, 2), f"Total {total} не сопадает с item total + tax"

    checkout.finish_placing_order()
    checkout.confirm_order_message(), "Нет подтверждающего сообщения о размещении заказа"


def test_checkout_without_postal_code(page ):
    catalog = CatalogSteps(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket = BasketSteps(page)
    basket.open_shopping_cart()
    basket.checkout()

    checkout = CheckoutSteps(page)
    checkout.enter_first_name("Anna")
    checkout.enter_last_name("Green")
    # Пропускаем добавление postal code

    checkout.continue_placing_order()
    checkout.zip_postal_code_error(), "Нет ошибки о необходимости заполнения почтового кода"