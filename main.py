import time 
import random
import names
import pyperclip
import warnings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime as dt
from config import PASSWORD


CHROME_DRIVER = "requirements\chromedriver.exe"

def create_wallet(driver):
        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/button'))).click()

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="createWallet"]/div/div[2]/div/button[1]'))).click()

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div/div/div/div/input'))).send_keys(
                f"{names.get_first_name().lower()}{names.get_last_name().lower()}{random.randrange(0, 1999)}")   

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div/button'))).click()

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div/div[1]/div/input'))).send_keys(PASSWORD)

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div/div[2]/div/input'))).send_keys(PASSWORD)

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div/div[3]/div/label/span[1]'))).click()

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div/button'))).click()

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/button'))).click()
        
        mnemonic = pyperclip.paste().split(' ')

        with open("aurox_wallets.txt", "a") as file:
            file.write(f"{pyperclip.paste()} \n")
            file.close()
        
        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/div[3]/div/label/span[1]'))).click()

        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="app"]/div/div/div[1]/div[3]/button'))).click()
            
        print(f"{dt.now().time()} Сохраняю MNEMONIC")
        element = []
        for i in range(12):
            fromMnemo = driver.find_element(By.XPATH, f'//*[@id="app"]/div/div/div[1]/div[2]/div[1]/div[{i + 1}]/div/span')
            element.append(fromMnemo.text)
        
        print(f"{dt.now().time()} Подтверждаю MNEMONIC")
        for mnemo in mnemonic:
            iter = 0
            for elem in element: 
                if elem == mnemo:
                    WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
                        (By.XPATH, f'//*[@id="app"]/div/div/div[1]/div[2]/div[1]/div[{iter + 1}]/div/span'))).click()
                else:
                    iter += 1
        time.sleep(3)
        WebDriverWait(driver, 20, 0.005).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div/div/div[1]/div[2]/button'))).click()
        
      
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_extension("requirements\wallet_aurox.crx")
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=options)
    driver.maximize_window()

    return driver

def main():
    accCount = 0
    while True:
        print(f"{dt.now().time()} Создаю аккаунт №{accCount}")
        driver = create_driver()
        driver.get("chrome-extension://kilnpioakcdndlodeeceffgjdpojajlo/onboarding.html")
        create_wallet(driver)
        time.sleep(10)
        driver.quit()
        accCount += 1

if __name__ == "__main__":
    main()


        