import allure
from ui.pages.basket_page import BasketPage
from playwright.sync_api import Page


class BasketSteps:

    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(self.page)

    @allure.step("Открываем корзину")
    def open_shopping_cart(self):
        return self.basket_page.open_shopping_cart()

    @allure.step("Получаем данные товара {product_name} в корзине")
    def get_cart_item(self, product_name: str):
        return self.basket_page.get_cart_item(product_name)

    @allure.step("Получаем имена товаров в корзине")
    def get_cart_item_names(self) -> list[str]:
        return self.basket_page.get_cart_item_names()

    @allure.step("Удаляем товар на из корзины")
    def remove_item_from_cart(self, product_name: str):
        return self.basket_page.remove_item_from_cart(product_name)

    @allure.step("Получаем общую сумму товаров из корзины")
    def get_items_total_price(self) -> float:
        return self.basket_page.get_items_total_price()

    @allure.step("Начинам заполнение данных для заказа")
    def checkout(self):
        return self.basket_page.checkout()































