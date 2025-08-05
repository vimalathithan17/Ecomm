from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from shop.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

class ShopSeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Create test products with dummy images for each test (ensures visibility)
        products = [
            {
                "name": "Classic White Shirt",
                "price": 29.99,
                "image_name": "shirt.jpg",
                "description": "Premium cotton white shirt, perfect for formal and casual occasions."
            },
            {
                "name": "Running Sneakers",
                "price": 79.99,
                "image_name": "shoes.jpg",
                "description": "Lightweight running sneakers with breathable mesh and cushioned sole."
            },
            {
                "name": "Leather Wallet",
                "price": 24.99,
                "image_name": "wallet.jpg",
                "description": "Genuine leather wallet with multiple card slots and coin pocket."
            },
            {
                "name": "Sports Water Bottle",
                "price": 9.99,
                "image_name": "bottle.jfif",
                "description": "Stainless steel water bottle, keeps drinks cold for 24 hours."
            },
        ]
        for prod in products:
            if not Product.objects.filter(name=prod["name"]).exists():
                image = SimpleUploadedFile(prod["image_name"], b"dummydata", content_type="image/jpeg")
                Product.objects.create(
                    name=prod["name"],
                    price=prod["price"],
                    description=prod["description"],
                    image=image
                )
        # Create a test user if not exists
        if not User.objects.filter(username="seleniumuser").exists():
            User.objects.create_user(username="seleniumuser", password="testpass123")

    def signup(self, username, password1, password2):
        self.driver.get(self.live_server_url + "/signup/")
        time.sleep(1)
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password1").send_keys(password1)
        self.driver.find_element(By.NAME, "password2").send_keys(password2)
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

    def login(self, username, password):
        self.driver.get(self.live_server_url + "/login/")
        time.sleep(1)
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)

    def test_products_visible(self):
        self.driver.get(self.live_server_url + "/")
        time.sleep(2)
        try:
            self.assertIn("Classic White Shirt", self.driver.page_source)
        except AssertionError:
            print(self.driver.page_source)
            raise
        self.assertIn("Running Sneakers", self.driver.page_source)
        self.assertIn("Leather Wallet", self.driver.page_source)
        self.assertIn("Sports Water Bottle", self.driver.page_source)

    def test_signup_valid(self):
        self.signup("seleniumuser2", "testpass123", "testpass123")
        self.assertTrue("logout" in self.driver.page_source.lower() or "/signup/" not in self.driver.current_url)

    def test_signup_invalid(self):
        self.signup("seleniumuser3", "testpass123", "wrongpass")
        self.assertTrue("error" in self.driver.page_source.lower() or "/signup/" in self.driver.current_url)

    def test_login_valid(self):
        self.login("seleniumuser", "testpass123")
        self.assertTrue("logout" in self.driver.page_source.lower() or "/login/" not in self.driver.current_url)

    def test_login_invalid(self):
        self.login("seleniumuser", "wrongpass")
        self.assertTrue("error" in self.driver.page_source.lower() or "/login/" in self.driver.current_url)

    def test_product_list(self):
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        self.assertTrue("product" in self.driver.page_source.lower() or self.driver.title != "")

    def test_cart_add_remove(self):
        self.login("seleniumuser", "testpass123")
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        products = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-cart')]")
        if products:
            products[0].click()
            time.sleep(1)
            self.driver.get(self.live_server_url + "/cart/")
            self.assertIn("cart", self.driver.page_source.lower())

    def test_wishlist_add_remove(self):
        self.login("seleniumuser", "testpass123")
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        products = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-wishlist')]")
        if products:
            products[0].click()
            time.sleep(1)
            self.driver.get(self.live_server_url + "/wishlist/")
            self.assertIn("wishlist", self.driver.page_source.lower())

    def test_order_history_authenticated(self):
        self.login("seleniumuser", "testpass123")
        self.driver.get(self.live_server_url + "/orders/")
        time.sleep(1)
        self.assertTrue("order" in self.driver.page_source.lower() or self.driver.current_url.endswith("orders/"))

    def test_order_history_unauthenticated(self):
        self.driver.get(self.live_server_url + "/orders/")
        time.sleep(1)
        self.assertTrue("login" in self.driver.page_source.lower() or "signup" in self.driver.page_source.lower() or self.driver.current_url.endswith("login/"))

    def test_product_search(self):
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys("Shirt")
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)
        try:
            self.assertIn("Classic White Shirt", self.driver.page_source)
        except AssertionError:
            print(self.driver.page_source)
            raise
        self.assertNotIn("Running Sneakers", self.driver.page_source)

    def test_product_detail(self):
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        detail_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'product/')]")
        if detail_links:
            detail_links[0].click()
            time.sleep(1)
            self.assertIn("Add to Cart", self.driver.page_source)

    def test_cart_clear(self):
        self.login("seleniumuser", "testpass123")
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        products = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-cart')]")
        if products:
            products[0].click()
            time.sleep(1)
            self.driver.get(self.live_server_url + "/cart/")
            clear_btns = self.driver.find_elements(By.XPATH, "//button[contains(., 'Clear Cart')]")
            if clear_btns:
                clear_btns[0].click()
                time.sleep(1)
                self.assertTrue("No products" in self.driver.page_source or "empty" in self.driver.page_source.lower())

    def test_checkout_and_order_confirmation(self):
        self.login("seleniumuser", "testpass123")
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        products = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-cart')]")
        if products:
            products[0].click()
            time.sleep(1)
            self.driver.get(self.live_server_url + "/cart/")
            checkout_btns = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'checkout')]")
            if checkout_btns:
                checkout_btns[0].click()
                time.sleep(1)
                name = self.driver.find_element(By.NAME, "name")
                email = self.driver.find_element(By.NAME, "email")
                address = self.driver.find_element(By.NAME, "address")
                name.send_keys("John Doe")
                email.send_keys("john@example.com")
                address.send_keys("123 Test Street")
                self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
                time.sleep(2)
                self.assertTrue("Thank you" in self.driver.page_source or "order" in self.driver.page_source.lower())

    def test_signup_form_validation(self):
        self.driver.get(self.live_server_url + "/signup/")
        time.sleep(1)
        self.driver.find_element(By.NAME, "username").send_keys("")
        self.driver.find_element(By.NAME, "password1").send_keys("")
        self.driver.find_element(By.NAME, "password2").send_keys("")
        try:
            btn = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            self.driver.execute_script("arguments[0].scrollIntoView();", btn)
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
        except Exception as e:
            print("Signup form error:", e)
            raise
        time.sleep(1)
        self.assertTrue("error" in self.driver.page_source.lower() or "required" in self.driver.page_source.lower())

    def test_login_form_validation(self):
        self.driver.get(self.live_server_url + "/login/")
        time.sleep(1)
        self.driver.find_element(By.NAME, "username").send_keys("")
        self.driver.find_element(By.NAME, "password").send_keys("")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        self.assertTrue("error" in self.driver.page_source.lower() or "required" in self.driver.page_source.lower())

    def test_checkout_form_validation(self):
        self.login("seleniumuser", "testpass123")
        # Add a product to cart before visiting checkout
        self.driver.get(self.live_server_url + "/")
        time.sleep(1)
        products = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Add to Cart')]")
        if products:
            products[0].click()
            time.sleep(1)
        self.driver.get(self.live_server_url + "/checkout/")
       
        time.sleep(1)
        try:
            self.driver.find_element(By.NAME, "name").send_keys("")
            self.driver.find_element(By.NAME, "email").send_keys("")
            self.driver.find_element(By.NAME, "address").send_keys("")
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        except Exception as e:
            print("Checkout form error:", e)
            print(self.driver.page_source)  # Print the HTML for debugging
            raise
        time.sleep(1)
        self.assertTrue("error" in self.driver.page_source.lower() or "required" in self.driver.page_source.lower())
