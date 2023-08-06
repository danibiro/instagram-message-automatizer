from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import yaml
from time import sleep

def read_files():
    with open("user_config.yaml", "r") as user_stream, open("message_config.yaml", "r") as message_stream:
        try: 
            user_config = yaml.safe_load(user_stream)
            message_config = yaml.safe_load(message_stream)
            return user_config, message_config
        except yaml.YAMLError as exc:
            print(exc)

def login(driver, user_config):
    sleep(2)
    username = user_config["username"]
    password = user_config["password"]
    driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']//div[text()='Log in']").click()

def accept_cookies(driver):
    try:
        cookie_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Allow all cookies']")))
        cookie_button.click()
    except NoSuchElementException as exc:
        print('Accept cookies not needed')

def redirect_to_user_profile(driver, message_config):
        driver.get("https://www.instagram.com/" + message_config["username"])
        accept_cookies(driver)
        sleep(2)

def click_on_message(driver):
    message_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Message']")))
    message_button.click()

def not_save_info(driver):
    not_save_login_info = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and text()='Not Now']")))
    not_save_login_info.click()

def decline_notifications(driver):
    notifications = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']")))
    notifications.click()

def send_message(driver, message_config):
    driver.find_element(By.XPATH, "//div[@role='textbox' and @aria-label='Message']").send_keys(message_config["message"])
    driver.find_element(By.XPATH, "//div[@role='button' and text()='Send']").click()

if __name__ == "__main__":
    driver = webdriver.Chrome()
    user_config, message_config = read_files()
    redirect_to_user_profile(driver, message_config)
    click_on_message(driver)
    login(driver, user_config)
    not_save_info(driver)
    click_on_message(driver)
    decline_notifications(driver)
    send_message(driver, message_config)
    driver.close()