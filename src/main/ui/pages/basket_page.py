from playwright.sync_api import Page


class BasketPage:
    URL = "https://www.saucedemo.com/"
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.locator(".shopping_cart_link")
        self.item_cards = page.locator(".cart_item")
        self.item_list = page.locator('[data-test="cart-list"]')
        self.inventory_list = page.locator(".inventory_item_price")
        self.remove_button = page.locator('[data-test="remove"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.error_message = page.locator('[data-test="error"]')

    def open_shopping_cart(self):
        self.cart_link.click()

    def get_cart_item(self, product_name: str):
        return self.page.locator(".cart_item").filter(has_text=product_name)

    def get_cart_item_names(self):
        return self.item_list.inner_text()

    def remove_item_from_cart(self, product_name: str):
        self.get_cart_item(product_name).get_by_role("button", name="Remove").click()

    def get_cart_price(self, product_name: str):
        card = self.page.locator(".cart_item").filter(has_text=product_name)
        price = card.locator(".inventory_item_price").inner_text()
        return float(price.replace("$", ""))

    def get_items_total_price(self) -> float:
        prices = self.page.locator(".inventory_item_price").all_inner_texts()

        return sum(
            float(price.replace("$", ""))
            for price in prices
        )

    def checkout(self):
        self.checkout_button.click()