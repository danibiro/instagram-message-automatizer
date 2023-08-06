from selenium import webdriver
from selenium.webdriver.common.by import By
import yaml

driver = webdriver.Chrome()
driver.get("https://www.instagram.com")

driver.find_element(By.XPATH, "//button[text()='Allow all cookies']").click()

with open("user_config.yaml", "r") as stream:
    try: 
        user_config = yaml.safe_load(stream)
        username = user_config["username"]
        password = user_config["password"]
        driver.find_element(By.XPATH, "//input[@name='username']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    except yaml.YAMLError as exc:
        print(exc)