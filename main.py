from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml
import logging as log

log.basicConfig(
    filename="log.txt",
    filemode="a",
    level=log.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

MAX_TIMEOUT = 7

def driver_init():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def read_files():
    with open("user_config.yaml", "r") as user_stream, open("message_config.yaml", "r") as message_stream:
        try: 
            user_config = yaml.safe_load(user_stream)
            message_config = yaml.safe_load(message_stream)
            return user_config, message_config
        except yaml.YAMLError as exc:
            log.error(exc)
            exit(1)

def init(driver):
    driver.get("https://www.instagram.com")
    log.info("Directed to instagram.com")

def login(driver, user_config):
    username = user_config["username"]
    password = user_config["password"]
    username_input = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, MAX_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']//div[text()='Log in']")))
    login_button.click()

    log.info("Login info entered, login button clicked")

def accept_cookies(driver):
    try:
        cookie_button = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']")))
        cookie_button.click()
        log.info("Cookies accepted")
        WebDriverWait(driver, MAX_TIMEOUT).until(EC.invisibility_of_element_located((By.XPATH, "//button[text()='Allow all cookies']")))
    except NoSuchElementException as exc:
        log.warn("Accept cookies not needed")

def redirect_to_user_profile(driver, message_config):
    driver.get("https://www.instagram.com/" + message_config["username"])

    log.info("Redirected to user profile (instagram.com/" + message_config["username"] + ")")

def click_on_message(driver):
    try:
        message_button = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Message']")))
        message_button.click()
        log.info("Clicked on \"Message\" button")
    except NoSuchElementException as exc:
        log.error("You don't have the necessary rights to message this user or there is no user with this username.")

def not_save_info(driver):
    not_save_login_info = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Not Now']")))
    not_save_login_info.click()

    log.info("Saving info declined")

def decline_notifications(driver):
    try:
        notifications = WebDriverWait(driver, MAX_TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
        notifications.click()

        log.info("Declined notifications")
    except NoSuchElementException as exc:
        log.warn("Declining notifications not needed")

def send_message(driver, message_config):
    send_message_textbox = WebDriverWait(driver, MAX_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @aria-label='Message']")))
    send_message_textbox.send_keys(message_config["message"])

    WebDriverWait(driver, MAX_TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//div[@role='button' and text()='Send']")))

    driver.find_element(By.XPATH, "//div[@role='button' and text()='Send']").click()

    log.info("Message \"" + message_config["message"] + "\" sent successfully to user " + message_config["username"] + "\n\n")

if __name__ == "__main__":
    driver = driver_init()
    user_config, message_config = read_files()
    init(driver)
    accept_cookies(driver)
    login(driver, user_config)
    not_save_info(driver)
    decline_notifications(driver)
    redirect_to_user_profile(driver, message_config)
    click_on_message(driver)
    send_message(driver, message_config)
    driver.close()
