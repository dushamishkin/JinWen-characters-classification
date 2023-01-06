import gc
import os
import requests
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# simple logger
def log(message):
    with open('C:/Users/yddev/PycharmProjects/jinwen_parse/log.txt', 'a') as f:
        f.write(f'\n\n{datetime.now().replace(microsecond=0)}:\n{message}')
        f.close()


output_path = 'C:/Users/yddev/PycharmProjects/jinwen_parse/reload'
service = Service(executable_path="C:/Users/yddev/geckodriver.exe")
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'}


for char_id in range(1, 3610):
    try:
        driver_last = webdriver.Firefox(service=service)
        driver_last.set_script_timeout(30)
        driver_last.set_page_load_timeout(30)

        driver_last.get('https://xiaoxue.iis.sinica.edu.tw/jinwen?')
        driver_last.implicitly_wait(2)

        input_char = driver_last.find_element(by=By.ID, value='ZiOrder')
        input_char.send_keys(str(char_id))
        input_char.send_keys(Keys.ENTER)
        driver_last.implicitly_wait(3)

        select_char_num = Select(WebDriverWait(driver_last, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/table[2]/tbody/tr/td[3]/form/table/tbody/tr[2]/td/select[1]'))))
        select_char_num.select_by_value('50')
        driver_last.implicitly_wait(5)
            
        select_char_size = Select(WebDriverWait(driver_last, 20).until(EC.presence_of_all_elements_located((By.ID, 'ImageSize')))[1])
        select_char_size.select_by_value('72')
        driver_last.implicitly_wait(3)

        chars = driver_last.find_elements(By.CLASS_NAME, 'charValue')
    except Exception as e:
        log(f"MAIN BLOCK // Char #{char_id}: {e}")
        reload.append(char_id)
    
    try:
        src_list = []
        for id, c in enumerate(chars):
            src = c.get_attribute('src')
            src_list.append(src)

        os.mkdir(f'{output_path}/{char_id}')
        for img in range(len(src_list)):
            try:
                r = requests.get(src_list[img], timeout=20, headers=headers)
                with open(f"{output_path}/{char_id}/{char_id}_{img}.png","wb") as file:
                    file.write(r.content)
                sleep(1)
            except requests.exceptions.ReadTimeout:
                log(f"Timeout char #{char_id} glyph #{img}")
                continue
    except Exception as e:
        log(f"DOWNLOAD BLOCK // Char #{char_id}: {e}")
        reload.append(char_id)
    else:
        log(f"SUCCESSFULLY DONE CHAR #{char_id}")

                
    gc.collect()
    driver_last.quit()