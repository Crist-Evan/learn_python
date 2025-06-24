from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import requests
import os
import whisper
import warnings
import time
warnings.filterwarnings("ignore")

driver = webdriver.Chrome()

model = whisper.load_model("base")

#captcha solver
def transcribe(url):
    with open('.temp', 'wb') as f:
        f.write(requests.get(url).content)
    result = model.transcribe('.temp')
    return result["text"].strip()

def click_checkbox(driver):
    #driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='reCAPTCHA']"))
    driver.find_element(By.ID, "recaptcha-anchor-label").click()
    #driver.switch_to.default_content()

def request_audio_version(driver):
    #driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, "recaptcha-audio-button").click()

def solve_audio_captcha(driver):
    text = transcribe(driver.find_element(By.ID, "audio-source").get_attribute('src'))
    driver.find_element(By.ID, "audio-response").send_keys(text)
    driver.find_element(By.ID, "recaptcha-verify-button").click()

# start
def login_webmail(email, password):
    driver.get('https://cardamom.iixcp.rumahweb.net:2096/')

    email_input = driver.find_element(By.ID, 'user')
    email_input.send_keys(email)

    password_input = driver.find_element(By.ID, 'pass')
    password_input.send_keys(password)

    login_button = driver.find_element(By.ID, 'login_submit')
    login_button.click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'launchActiveButton'))).click()

def open_steam_registration(email):
    driver.execute_script("window.open('https://store.steampowered.com/join/', '_blank');")
    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'email'))).send_keys(email)
    driver.find_element(By.ID, 'reenter_email').send_keys(email)
    driver.find_element(By.ID, 'country').send_keys('United States')
    driver.find_element(By.ID, 'i_agree_check').click()
    
    time.sleep(5)
    driver.switch_to.default_content()
    click_checkbox(driver)
    time.sleep(1)
    driver.switch_to.default_content()
    time.sleep(1)
    request_audio_version(driver)
    time.sleep(1)
    solve_audio_captcha(driver)
    time.sleep(10)
    
    driver.switch_to.default_content()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="createAccountButton"]').click()
    
def verify_steam_email(page):

    driver.switch_to.window(driver.window_handles[0])

    time.sleep(20)
    driver.refresh()

    steam_email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "New Steam Account Email Verification")]'))
    )
    steam_email.click()

    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@id='messagecontframe']"))
    time.sleep(1)
    verification_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Verify My Email Address")]'))
    )
    verification_link.click()
    time.sleep(1)

    driver.switch_to.default_content()
    driver.switch_to.window(driver.window_handles[page])
    
    time.sleep(2)
    if driver.find_element(By.XPATH, '//*[contains(text(), "Unable to Verify Email Address")]'):
        page += 1
        verify_steam_email(page)
    elif driver.find_element(By.XPATH, '//*[contains(text(), "Email Verified")]'):
        pass
    time.sleep(10)

def create_steam_username_password(username, password):
    
    driver.switch_to.window(driver.window_handles[1])
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'accountname')))
    driver.find_element(By.ID, 'accountname').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'reenter_password').send_keys(password)
    time.sleep(2)
    driver.find_element(By.ID, 'create_account_button').click()
    time.sleep(5)

def open_ubisoft_registration(username, email, password):
    driver.switch_to.default_content()
    driver.execute_script("window.open('https://account.ubisoft.com/login', '_blank');")
    driver.switch_to.window(driver.window_handles[1])

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="privacy__modal__accept"]'))).click()
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, "//h1[@class='PageTitle-title-0-2-24 PageTitle-titleCentered-0-2-26']"), "Manage your Ubisoft account"))
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/iframe"))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'title-link'))).click()
    
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn")))
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, "//span[@id='IdCreateText']"), "CREATE AN ACCOUNT"))
    driver.find_element(By.ID, 'AccountDobDay').send_keys('01')
    driver.find_element(By.ID, 'AccountDobMonth').send_keys('01')
    driver.find_element(By.ID, 'AccountDobYear').send_keys('1990')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".btn").click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn:nth-child(9)")))
    driver.find_element(By.ID, 'AccountEmail').send_keys(email)
    driver.find_element(By.ID, 'ConfirmAccountEmail').send_keys(email)
    driver.find_element(By.ID, 'AccountPassword').send_keys(password)
    driver.find_element(By.ID, 'Username').send_keys(username)
    checkbox1 = driver.find_element(By.XPATH, '//*[@id="tosCheckbox"]')
    checkbox2 = driver.find_element(By.XPATH, '//*[@id="ubiOptInCheckbox"]')
    driver.execute_script("arguments[0].click();", checkbox1)
    driver.execute_script("arguments[0].click();", checkbox2)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(9)").click()
    
    captcha_resolved = False
    while not captcha_resolved:
        try:
            captcha_label = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "Please complete the captcha challenge.")]'))
            )

            if captcha_label:
                time.sleep(5)
                click_checkbox(driver)
                driver.switch_to.default_content()
                time.sleep(1)
                WebDriverWait(driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/iframe"))
                )
                request_audio_version(driver)
                time.sleep(1)
                solve_audio_captcha(driver)
                time.sleep(10)
                driver.switch_to.default_content()
                WebDriverWait(driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/iframe"))
                )
                driver.find_element(By.CSS_SELECTOR, "button.btn:nth-child(9)").click()
            else:
                captcha_resolved = True
        except:
            captcha_resolved = True
    
def complete_ubisoft_verification():
    driver.switch_to.default_content()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(10)
    driver.refresh()

    try:
        security_code_element = driver.find_element(By.XPATH, '//span[contains(text(), "Ubisoft Account Security Code")]')
        security_code_element.click()

    except NoSuchElementException:
        complete_ubisoft_verification()
    
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@id='messagecontframe']"))
    time.sleep(1)
    verification_code = driver.find_element(By.XPATH, '//strong').text
    time.sleep(1)

    driver.switch_to.window(driver.window_handles[2])
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/iframe"))
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'verification_code'))).send_keys(verification_code)
    time.sleep(1)
    driver.find_element(By.ID, 'verify_button').click()


page = 2
#login_webmail("test@hycome.my.id", "nQ]m^CtZ0=5U")
#open_steam_registration("test@hycome.my.id")
#time.sleep(2)
#verify_steam_email(page)
#create_steam_username_password("test235x", "nQ]m^CtZ0=5U")
#time.sleep(2)
open_ubisoft_registration("robertysec234", "test2@hycome.my.id", "[!k9+1L{)zdC")
time.sleep(5)
#complete_ubisoft_verification()


#driver.find_element(By.XPATH, ".//span[@title='Add to Library']").click()