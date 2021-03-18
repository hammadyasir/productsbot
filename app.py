#!/usr/bin/python3
import os
import schedule
import time
import ctypes
import creds
from selenium import webdriver
from playsound import playsound
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# op.add_argument("--headless")
# op.add_argument("--no-sandbox")
# op.add_argument("--disable-dev-shm-usage")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

# def main():
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install()) #For Firefox
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())  #For Chrome

wait = WebDriverWait(driver, 10)
def checkout():
    driver.find_element(By.CSS_SELECTOR, '#cartItemCount').click() # Gotocart
    driver.find_element(By.CSS_SELECTOR, '#btnCheckoutTop').click()
    driver.find_element(By.CSS_SELECTOR, '#btnSaveAndContinue').click() #Continuetopayment
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'#txtCreditCardNumber')))
    try:
        driver.find_element(By.CSS_SELECTOR, '#txtCreditCardNumber').click()
        driver.find_element(By.CSS_SELECTOR, '.dropdown-menu>li:nth-child(2)').click()
    except:
        pass
    driver.find_element(By.CSS_SELECTOR, '#txtCVV').send_keys(CVV)
    driver.find_element(By.CSS_SELECTOR, '#chkBillingSameAsShipping').click()
    driver.find_element(By.CSS_SELECTOR, '#txtPhone').send_keys(PH)
    driver.find_element(By.CSS_SELECTOR, '#btnSaveAndContinue').click()
    driver.find_element(By.CSS_SELECTOR, '#btnPlaceOrder').click()
    playsound('checkout.wav')
    ctypes.windll.user32.MessageBoxW(0, "Checkout Completed..Please check you cart...\nThank you...", "IN STOCK", 1)


url = 'https://www.brownells.com/aspx/account/login.aspx'
driver.get(url)
driver.maximize_window()

#Credentials
ID = 'billmanweh'
PASS = 'weh810'
PH = '8179055636'
CVV = '4035'

# Login
driver.find_element(By.NAME, 'ctl00$ContentPlaceHolderColMain$txtlogin').send_keys(ID)
driver.find_element(By.NAME, 'ctl00$ContentPlaceHolderColMain$txtpassword').send_keys(PASS)
driver.find_element(By.NAME, 'ctl00$ContentPlaceHolderColMain$btnSignIn').click()
availability = False
with open("Primers.txt") as f:
    for line in f:
        url = line.strip()  # to remove the trailing \n
        driver.get(url)
        prod_title = driver.find_element(By.CSS_SELECTOR, '#listMain .wrap span+ span').text
        print(prod_title,'Checking....')
        SKUS = []
        sku_elms = driver.find_elements(By.CSS_SELECTOR, '.lnkNameSku>span:nth-child(1)')
        for sku in sku_elms:
            SKUS.append(sku.text)
        for i in range(len(SKUS)):
            if i<9: stock = driver.find_element(By.CSS_SELECTOR, f'span[id$=ctl0{i+1}_mfr]').text
            elif i>10: stock = driver.find_element(By.CSS_SELECTOR, f'span[id$=ctl{i+1}_mfr]').text
            if stock == 'In Stock':
                availability = True
                driver.find_element(By.XPATH, f'//*[@sku="{SKUS[i]}"]').click()
                playsound('Instock.wav')
                print('In stock')
                driver.refresh()
            else:
                print('Out of stock')
    if availability == True: checkout()
    elif availability == False: print('There is no any available stock\nfor checkout...\nTry again!')
# Gotocart.schedule_1_.checkout()
driver.quit()


# if __name__ == "__main__":
#     schedule.every(4).minutes.do(main)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
    


