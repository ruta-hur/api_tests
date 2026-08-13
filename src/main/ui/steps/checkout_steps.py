import allure
from ui.pages.checkout_page import CheckoutPage
from playwright.sync_api import Page, expect

class CheckoutSteps:

    def __init__(self, page: Page):
        self.page = page
        self.checkout_page = CheckoutPage(self.page)

    @allure.step("Заполняем поле имени")
    def enter_first_name(self, text: str):
        return self.checkout_page.enter_first_name(text)

    @allure.step("Заполняем поле фамилии")
    def enter_last_name(self, text: str):
        return self.checkout_page.enter_last_name(text)

    @allure.step("Заполняем поле кода")
    def enter_zip_postal_code(self, text: str):
        return self.checkout_page.enter_zip_postal_code(text)

    @allure.step("Сообщение о незаполненном поле почтового индекса")
    def zip_postal_code_error(self):
        error_text = self.checkout_page.address_error.inner_text()
        assert error_text == "Error: Postal Code is required", "Нет сообщения, что поле почтового кода обязательно для заполнения"

    @allure.step("Жмем кнопку 'продолжить' после заполнения имени и адреса")
    def continue_placing_order(self):
        return self.checkout_page.continue_placing_order()

    @allure.step("Отмена размещения заказа после заполнения имени и адреса")
    def cancel_shopping_order(self):
        return self.checkout_page.cancel_shopping_order()

    @allure.step("Получаем стоимость товаров без учета налога")
    def get_items_subtotal(self):
        return self.checkout_page.get_items_subtotal()

    @allure.step("Получаем сумму налога")
    def get_items_tax(self):
        return self.checkout_page.get_items_tax()

    @allure.step("Получаем итоговую стоимость товаров с учетом налога")
    def get_items_total(self):
        return  self.checkout_page.get_items_total()

    @allure.step("Подтверждаем заказ")
    def finish_placing_order(self):
        self.checkout_page.finish_placing_order()

    @allure.step("Получаем подтверждение заказа")
    def confirm_order_message(self):
        confirm = self.checkout_page.confirm_order_message()
        assert confirm == "Thank you for your order!", "Нет сообщения, подтверждающего получение заказа"









