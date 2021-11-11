import time
import os
from selenium import webdriver
from time import sleep
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

MESSAGE = os.getenv("MESSAGE")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SHOULD_RUN = os.getenv("SHOULD_RUN")


def check_unread_and_notify():
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)

    driver.get('https://www.instagram.com/')
    driver.implicitly_wait(15)
    print("Opened Instagram...")

    username = driver.find_element("name", "username")
    username.send_keys(USERNAME)
    print("Username entered...")

    password = driver.find_element("name", "password")
    password.send_keys(PASSWORD)
    print("Password entered...")

    button = driver.find_element("xpath", "//button[@type='submit']")
    button.click()

    try:
        button = driver.find_element(
            "xpath", "//button[contains(text(), 'Not Now')]")
        button.click()
    except NoSuchElementException as e:
        print("Save password prompt not detected", e)

    try:
        button = driver.find_element(
            "xpath", "//button[contains(text(), 'Not Now')]")
        button.click()
    except NoSuchElementException as e:
        print("Notifications prompt not detected", e)

    links = driver.find_elements("tag name", "a")
    print("Opening messages tab...")
    click_messages_tab(links)
    time.sleep(5)  # Wait for messages to load

    messages = driver.find_elements(
        "xpath", "//div[contains(@aria-label, 'Unread')]")
    if messages:
        print("Responding to messages...")
        respond_to_unread(messages, driver)
    else:
        print("No unread messages found...")

    driver.close()
    print("Done.")


def respond_to_unread(messages, driver):
    while(messages):
        try:
            messages[0].click()

            text_box = driver.find_element(
                "xpath", "//textarea[contains(@placeholder, 'Message...')]")
            text_box.send_keys(MESSAGE)

            send_button = driver.find_element(
                "xpath", "//button[contains(text(), 'Send')]")
            send_button.click()

            messages = driver.find_elements(
                "xpath", "//div[contains(@aria-label, 'Unread')]")
        except BaseException as e:
            print("Unexpected" + e + " " + type(e))


def click_messages_tab(tab_links):
    for link in tab_links:  # Go through links and find the message one
        try:
            if link.get_attribute("href") == "https://www.instagram.com/direct/inbox/":
                link.click()
                break
        except BaseException as err:
            print("Unexpected" + err + " " + type(err))
            print("Direct messages opened...")


if SHOULD_RUN == True:
    print("Starting job...")
    check_unread_and_notify()
else:
    print("Config disabled. Not running job.")
