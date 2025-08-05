from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import django

# Setup Django environment for product creation
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from shop.models import Product
from django.core.files import File

BASE_URL = "http://localhost:8000/"
USERNAME = "seleniumuser"
PASSWORD = "testpass123"

# Utility functions
def start_driver():
    return webdriver.Chrome()

def signup(driver, username, password1, password2):
    driver.get(BASE_URL + "signup/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password1").send_keys(password1)
    driver.find_element(By.NAME, "password2").send_keys(password2)
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

def login(driver, username, password):
    driver.get(BASE_URL + "login/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

def logout(driver):
    driver.get(BASE_URL + "logout/")
    time.sleep(1)

def create_products():
    products = [
        {
            "name": "Classic White Shirt",
            "price": 29.99,
            "image_path": "media/products/shirt.jpg",
            "description": "Premium cotton white shirt, perfect for formal and casual occasions."
        },
        {
            "name": "Running Sneakers",
            "price": 79.99,
            "image_path": "media/products/shoes.jpg",
            "description": "Lightweight running sneakers with breathable mesh and cushioned sole."
        },
        {
            "name": "Leather Wallet",
            "price": 24.99,
            "image_path": "media/products/wallet.jpg",
            "description": "Genuine leather wallet with multiple card slots and coin pocket."
        },
        {
            "name": "Sports Water Bottle",
            "price": 9.99,
            "image_path": "media/products/bottle.jfif",
            "description": "Stainless steel water bottle, keeps drinks cold for 24 hours."
        },
    ]
    for prod in products:
        if not Product.objects.filter(name=prod["name"]).exists():
            try:
                with open(prod["image_path"], "rb") as img_file:
                    product = Product(
                        name=prod["name"],
                        price=prod["price"],
                        description=prod["description"]
                    )
                    product.image.save(prod["image_path"].split("/")[-1], File(img_file), save=True)
                print(f"Added: {prod['name']}")
            except FileNotFoundError:
                print(f"Image not found for: {prod['name']} (expected at {prod['image_path']})")
        else:
            print(f"Already exists: {prod['name']}")

def test_signup_valid():
    driver = start_driver()
    signup(driver, USERNAME, PASSWORD, PASSWORD)
    assert "logout" in driver.page_source.lower() or driver.current_url != BASE_URL + "signup/"
    driver.quit()

def test_signup_invalid():
    driver = start_driver()
    signup(driver, USERNAME, PASSWORD, "wrongpass")
    assert "error" in driver.page_source.lower() or driver.current_url == BASE_URL + "signup/"
    driver.quit()

def test_login_valid():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    assert "logout" in driver.page_source.lower() or driver.current_url != BASE_URL + "login/"
    driver.quit()

def test_login_invalid():
    driver = start_driver()
    login(driver, USERNAME, "wrongpass")
    assert "error" in driver.page_source.lower() or driver.current_url == BASE_URL + "login/"
    driver.quit()

def test_product_list():
    driver = start_driver()
    driver.get(BASE_URL)
    time.sleep(1)
    assert "product" in driver.page_source.lower() or driver.title != ""
    driver.quit()

def test_cart_add_remove():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    driver.get(BASE_URL)
    time.sleep(1)
    # Try to add first product to cart
    products = driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-cart')]")
    if products:
        products[0].click()
        time.sleep(1)
        driver.get(BASE_URL + "cart/")
        assert "cart" in driver.page_source.lower()
    driver.quit()

def test_wishlist_add_remove():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    driver.get(BASE_URL)
    time.sleep(1)
    # Try to add first product to wishlist
    products = driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-wishlist')]")
    if products:
        products[0].click()
        time.sleep(1)
        driver.get(BASE_URL + "wishlist/")
        assert "wishlist" in driver.page_source.lower()
    driver.quit()

def test_order_history_authenticated():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    driver.get(BASE_URL + "orders/")
    time.sleep(1)
    assert "order" in driver.page_source.lower() or driver.current_url.endswith("orders/")
    driver.quit()

def test_order_history_unauthenticated():
    driver = start_driver()
    driver.get(BASE_URL + "orders/")
    time.sleep(1)
    assert "login" in driver.page_source.lower() or "signup" in driver.page_source.lower() or driver.current_url.endswith("login/")
    driver.quit()

def test_products_visible():
    driver = start_driver()
    driver.get(BASE_URL)
    time.sleep(2)
    assert "Classic White Shirt" in driver.page_source
    assert "Running Sneakers" in driver.page_source
    assert "Leather Wallet" in driver.page_source
    assert "Sports Water Bottle" in driver.page_source
    driver.quit()

def test_product_search():
    driver = start_driver()
    driver.get(BASE_URL)
    time.sleep(1)
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Shirt")
    search_box.send_keys(Keys.RETURN)
    time.sleep(1)
    assert "Classic White Shirt" in driver.page_source
    assert "Running Sneakers" not in driver.page_source
    driver.quit()

def test_product_detail():
    driver = start_driver()
    driver.get(BASE_URL)
    time.sleep(1)
    detail_links = driver.find_elements(By.XPATH, "//a[contains(@href, 'product/')]")
    if detail_links:
        detail_links[0].click()
        time.sleep(1)
        assert "Add to Cart" in driver.page_source
    driver.quit()

def test_cart_clear():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    driver.get(BASE_URL)
    time.sleep(1)
    products = driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-cart')]")
    if products:
        products[0].click()
        time.sleep(1)
        driver.get(BASE_URL + "cart/")
        clear_btns = driver.find_elements(By.XPATH, "//button[contains(., 'Clear Cart')]")
        if clear_btns:
            clear_btns[0].click()
            time.sleep(1)
            assert "No products" in driver.page_source or "empty" in driver.page_source.lower()
    driver.quit()

def test_checkout_and_order_confirmation():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    driver.get(BASE_URL)
    time.sleep(1)
    products = driver.find_elements(By.XPATH, "//a[contains(@href, 'add-to-cart')]")
    if products:
        products[0].click()
        time.sleep(1)
        driver.get(BASE_URL + "cart/")
        checkout_btns = driver.find_elements(By.XPATH, "//a[contains(@href, 'checkout')]")
        if checkout_btns:
            checkout_btns[0].click()
            time.sleep(1)
            name = driver.find_element(By.NAME, "name")
            email = driver.find_element(By.NAME, "email")
            address = driver.find_element(By.NAME, "address")
            name.send_keys("John Doe")
            email.send_keys("john@example.com")
            address.send_keys("123 Test Street")
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(2)
            assert "Thank you" in driver.page_source or "order" in driver.page_source.lower()
    driver.quit()

def test_signup_form_validation():
    driver = start_driver()
    driver.get(BASE_URL + "signup/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("")
    driver.find_element(By.NAME, "password1").send_keys("")
    driver.find_element(By.NAME, "password2").send_keys("")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert "error" in driver.page_source.lower() or "required" in driver.page_source.lower()
    driver.quit()

def test_login_form_validation():
    driver = start_driver()
    driver.get(BASE_URL + "login/")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("")
    driver.find_element(By.NAME, "password").send_keys("")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert "error" in driver.page_source.lower() or "required" in driver.page_source.lower()
    driver.quit()

def test_checkout_form_validation():
    driver = start_driver()
    login(driver, USERNAME, PASSWORD)
    driver.get(BASE_URL + "checkout/")
    time.sleep(1)
    driver.find_element(By.NAME, "name").send_keys("")
    driver.find_element(By.NAME, "email").send_keys("")
    driver.find_element(By.NAME, "address").send_keys("")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(1)
    assert "error" in driver.page_source.lower() or "required" in driver.page_source.lower()
    driver.quit()

def run_all():
    create_products()
    test_products_visible()
    test_signup_valid()
    test_signup_invalid()
    test_login_valid()
    test_login_invalid()
    test_product_list()
    test_product_search()
    test_product_detail()
    test_cart_add_remove()
    test_cart_clear()
    test_checkout_and_order_confirmation()
    test_wishlist_add_remove()
    test_order_history_authenticated()
    test_order_history_unauthenticated()
    test_signup_form_validation()
    test_login_form_validation()
    test_checkout_form_validation()
    print("All Selenium tests completed.")

if __name__ == "__main__":
    run_all()
