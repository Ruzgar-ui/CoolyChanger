##############
#!Version: 1 #
#!Ruzgar-ui  #
##############
import time

import colorama
from selenium import webdriver
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
    options = Options()
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://web.whatsapp.com')
    print(f"{purple}Please log in to whatsapp.{cyan}")
    input('When you log in, press "enter" key')
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
        )                                                #data-tab="-1"
        div_button.click()
        time.sleep(0.1)

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
    except Exception as e:
        print(e)

def main():
    driver = login_whatsapp()
    image_path, loop, sec = get_image_path()
    change_profile_picture(driver, image_path, loop, sec)
    driver.quit()

if __name__ == "__main__":
    main()
#Her 5 döngüde 1 kez 20 saniye mola verir.
#ikinci aracı sadece bana özel yapacağım.
#3 resimden sonra 10 saniye duracak. buna da renkli colorama