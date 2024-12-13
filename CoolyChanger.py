##################
#!Version: 2.0.0 #
#!By:  Ruzgar-ui #
##################
import os
import time
from datetime import datetime

import colorama
import keyboard
import requests
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

white="\033[97m"
cyan="\033[96m"
purple="\033[95m"
blue="\033[94m"
yellow="\033[93m"
green="\033[92m"
red="\033[91m"
gray="\033[90m"
reset="\033[00m"
colorama.init()

def login_whatsapp():
    print(f"{colorama.Fore.LIGHTRED_EX}Trying to open whatsapp.")
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://web.whatsapp.com')
    driver.set_window_position(-10000, 0)
    print("Waiting for QR Code...")

    qrcode_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//canvas[@aria-label="Scan this QR code to link a device!"]'))
    )

    screenshot = "qrcode_screenshot.png"
    driver.save_screenshot(screenshot)
    qrpath = os.path.abspath(f"{screenshot}")
    print(f"{green}QR Code is saved in {qrpath}")

    img = Image.open(f"{qrpath}")
    img.show()

    print(f"{purple}Please log in to whatsapp.{cyan}")
    start_time = time.time()

    while True:
        xyz = int(time.time() - start_time)
        if xyz!=0 and xyz%60 == 0 and xyz!=180 and xyz<=180 and xyz<180:
            print(f"{red}QR Code is refreshed{cyan}")
            os.system("taskkill /f /im dllhost.exe")
            driver.save_screenshot(screenshot)
            qrpath = os.path.abspath(f"{screenshot}")
            print(f"{green}QR Code is saved in {qrpath}")
            img = Image.open(f"{qrpath}")
            img.show()
            time.sleep(1)
        elif xyz == 240:
            os.system("taskkill /f /im dllhost.exe")
            print("Failed to read QR code.")
            return None
        else:
            try:
                qrcode_element = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, '//canvas[@aria-label="Scan this QR code to link a device!"]'))
                )
            except TimeoutException:
                print("Login successful!")
                os.system("taskkill /f /im dllhost.exe")
                break
    return driver

def get_image_path():
    choice = input("How many images do you want to use: ")
    image_paths = []
    print(f"{green}Drag your image here")
    if int(choice) <= 1:
        print(f"{red}You cant loop for 1 image{green}")
    for i in range(int(choice)):
        user_input = input(f"{i+1}. Image: ")
        image_paths.append(user_input)
    loop = input("How many loop (press i for infinity): ")
    sec = int(input("How often should the profile change (3 second is recommended): "))
    return image_paths, loop, sec

def loopi(driver, image_path, sec):
    for val in image_path:
        file_input = driver.find_element(By.XPATH, '//input[@type="file"]')

        file_input.send_keys(val)

        time.sleep(sec/2)
        butt = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Görseli gönder"]'))
        )
        butt.click()
        time.sleep(sec/2)

def change_profile_picture(driver, image_path, loop, sec):
    try:
        wait = WebDriverWait(driver, 15)
        profile_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="settings-outline"]'))
        )
        profile_button.click()
        time.sleep(0.1)

        div_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="x1c4vz4f xs83m0k xdl72j9 x1g77sc7 x78zum5 xozqiw3 x1oa3qoh x12fk4p8 xeuugli x2lwn1j xdt5ytf x12lumcd x1qjc9v5 xl56j7k x9f619 x1pi30zi x1y1aw1k xwib8y2"]'))
        )
        div_button.click()
        time.sleep(0.1)

        image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "pps.whatsapp.net")]'))
        )
        image_url = image.get_attribute('src')
        response = requests.get(image_url)
        file_name = "downloaded_image.jpg"
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Old profile picture: {file_name}")
        else:
            print(f"Error: {response.status_code}")
        old_image = os.path.abspath(f"{file_name}")
        print(f"Old image path: {old_image} {green}")
        try:
            print(f"{cyan}")
            if loop == "i":
                num=0
                while True:
                    print(f"Loop: {loop}")
                    if num % 5 == 0: time.sleep(20)
                    num+=1
                    loopi(driver, image_path, sec)
            else:
                num = 0
                loop = int(loop)
                while num < loop:
                    if num%5 == 0:time.sleep(20)
                    num += 1
                    print(f"Loop: {loop}/{num}")
                    loopi(driver, image_path, sec)
        except KeyboardInterrupt:
            print("Logging out...")
        finally:
            print("Thanks for using...")
            old_image_folder = os.path.dirname(os.path.abspath("downloaded_image.jpg"))
            os.startfile(old_image_folder)
            print(f"Old Profile Picture location: {old_image_folder}")
    except Exception as e:
        print(f"Exception: {e}")

def main():
    driver = login_whatsapp()
    if driver != None and driver:
        image_path, loop, sec = get_image_path()
        change_profile_picture(driver, image_path, loop, sec)
    driver.quit()

if __name__ == "__main__":
    main()
