from playwright.sync_api import Page


class CheckoutPage:
    URL = "https://www.saucedemo.com/"
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator("input[placeholder='First Name']")
        self.last_name = page.locator("input[placeholder='Last Name']")
        self.zip_postal_code = page.locator("input[placeholder='Zip/Postal Code']")
        self.continue_shopping = page.locator("#continue")
        self.cancel = page.locator("#cancel")
        self.address_error = page.locator("[data-test='error']")
        self.subtotal = page.locator(".summary_subtotal_label")
        self.tax = page.locator(".summary_tax_label")
        self.total_line = page.locator(".summary_total_label")
        self.finish = page.locator("#finish")
        self.complete_header = page.locator(".complete-header")

    def enter_first_name(self, text: str):
        self.first_name.fill(text)

    def enter_last_name(self, text: str):
        self.last_name.fill(text)

    def enter_zip_postal_code(self, text: str):
        self.zip_postal_code.fill(text)

    def continue_placing_order(self):
        self.continue_shopping.click()

    def cancel_shopping_order(self):
        self.cancel.click()

    def get_items_subtotal(self):
        item_total_line = self.subtotal.inner_text()
        item_total = float(item_total_line.split("$")[1])
        return item_total

    def get_items_tax(self):
        item_tax_line = self.tax.inner_text()
        tax = float(item_tax_line.split("$")[1])
        return tax

    def get_items_total(self):
        total_line = self.total_line.inner_text()
        total = float(total_line.split("$")[1])
        return total

    def finish_placing_order(self):
        self.finish.click()

    def confirm_order_message(self):
        return self.complete_header.inner_text()

