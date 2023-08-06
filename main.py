from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.instagram.com")

driver.find_element(By.XPATH, "//button[text()='Allow all cookies']").click()