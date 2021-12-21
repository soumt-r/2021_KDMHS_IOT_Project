from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from colorama import init, Fore
import os
import pyfiglet
import time
import json
import sys
init()

#자가진단 수행 소스코드
#Selenium WebDriver 사용
#Json 파일에서 학생 데이터 받아 자가진단 수행

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


options = webdriver.ChromeOptions()
#options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_experimental_option("excludeSwitches", ['enable-logging'])
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(options=options, executable_path='chromedriver')
driver.implicitly_wait(3)
wait = WebDriverWait(driver, 5, 0.2)

cls()
f = pyfiglet.Figlet()
f2 = pyfiglet.Figlet(font='alphabet')
print(Fore.LIGHTRED_EX + f.renderText('Self-diagnosis') + Fore.LIGHTCYAN_EX + f.renderText('Automation') + Fore.RESET + 'Covid 19 Self-diagnosis Automation V3')
print('')

jindan_URL = 'https://hcs.eduro.go.kr/#/loginHome'

with open(sys.argv[1], 'r') as f:
    json_data = json.load(f)

student_name = json_data["name"]
student_birth = json_data["birth"]
student_pass = json_data["pw"]

school_location = "경기도"
school_level = "고등학교"
school_name = "한국디지털미디어고등학교"

print("현재 시각 : " + time.strftime('%X %x %Z'))

print(student_birth," " , student_name, " ", student_pass)

print('')
try:
    driver.delete_all_cookies()

    print('')
    print('자가진단 페이지 접속...: ', end="")
    driver.get(jindan_URL)
    sleep(2)
    driver.find_element(by=By.ID, value='btnConfirm2').click()
    driver.find_element(by=By.CLASS_NAME, value='searchBtn').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')

    print('')
    print('지역 선택...: ', end="")
    Select(driver.find_element(by=By.ID, value='sidolabel')).select_by_visible_text(school_location)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학교급 선택...: ', end="")
    Select(driver.find_element(by=By.ID, value='crseScCode')).select_by_visible_text(school_level)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학교 이름 입력...: ', end="")
    driver.find_element(by=By.ID, value='orgname').send_keys(school_name)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('검색 버튼 클릭...: ', end="")
    driver.find_element(by=By.CLASS_NAME, value='searchBtn').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학교 선택...: ', end="")
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a')))
    driver.find_element(by=By.XPATH, value='//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('확인 버튼 클릭...: ', end="")
    driver.find_element(by=By.CLASS_NAME, value='layerFullBtn').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    sleep(1)

    print('')
    print('학생 이름 입력...: ', end="")
    driver.find_element(by=By.ID, value='user_name_input').send_keys(student_name)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학생 생년월일 입력...: ', end="")
    driver.find_element(by=By.ID, value='birthday_input').send_keys(student_birth)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')    
    print('확인 버튼 클릭...: ', end="")
    driver.find_element(by=By.ID, value="btnConfirm").click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    sleep(1)

    print('')
    print('비밀번호 입력', end="")
    driver.find_element(by=By.XPATH, value='//*[@id="password"]').click()
    for i in student_pass:
      print('.', end="")
      driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value=f"//*[@aria-label='{i}']"))
    print(':', end="")
    wait.until(expected_conditions.presence_of_element_located((By.ID, 'btnConfirm')))
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'btnConfirm')))
    driver.find_element(by=By.XPATH, value='//*[@id="btnConfirm"]').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    sleep(1)

    print('자가진단을 수행합니다...')

    items = driver.find_element(by=By.XPATH, value='//*[@id="container"]/div/section[2]/div[2]/ul').find_elements_by_tag_name('li')

    sleep(0.5)
    item = items[0]
    name = item.find_element(by=By.CLASS_NAME, value='name').get_attribute('innerHTML')
      
    item.find_element(by=By.CLASS_NAME, value='name').click()
    print('')
    print('자가진단 대상 : ' + name)
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'survey_q1a1')))
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(by=By.XPATH, value='//*[@id="survey_q1a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value='//*[@id="survey_q1a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value='//*[@id="survey_q2a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value='//*[@id="survey_q3a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element(by=By.XPATH, value='//*[@id="survey_q4a1"]'))

    sleep(2)
    print('확인 버튼 클릭...: ', end="")    
    driver.find_element(by=By.ID, value="btnConfirm").click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
      
    print('')
    print('자가진단이 완료되었습니다.')
  
except:
    print('[' + Fore.LIGHTRED_EX + 'ERROR' + Fore.RESET + ']')
    print("과정중 오류가 발생하였습니다.")
finally:
    driver.stop_client()
