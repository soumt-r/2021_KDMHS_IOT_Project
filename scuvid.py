#import
import time
from pad4pi import rpi_gpio
import RPi.GPIO as GPIO
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import os
import json

#핀 세팅
LED_RED_PIN = 27
LED_BLUE_PIN = 22
BUZZER_PIN =17

#GPIO 세팅
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_RED_PIN, GPIO.OUT)
GPIO.setup(LED_BLUE_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

#입력받는 스트링
StudentKEY = ""


RESET_PIN = digitalio.DigitalInOut(board.D4)

#OLED 세팅
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=RESET_PIN)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
font3 = ImageFont.truetype("/home/pi/src4/BinggraeSamanco.ttf", 32)

#키페드 세팅
KEYPAD = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]
COL_PINS = [13, 6, 5, 0] # BCM numbering
ROW_PINS = [21, 20, 26, 19] # BCM numbering

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

#******************************************#


#키패드 입력시 호출 / 키 출력 및 글자수 확인
def printKey(key):
  global StudentKEY
  if(StudentKEY.__len__() < 4):
    StudentKEY = StudentKEY + key
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "Self Covid", font=font, fill=255)
    draw.text((0, 20), "Automanation", font=font2, fill=255)
    draw.text((0, 35), StudentKEY, font=font2, fill=255)
    oled.image(image)
    oled.show()
    print(key, end="")
    if(StudentKEY.__len__() == 4):
      student_check()
      print(" ")
      StudentKEY = ""

#4글자 채워졌을때 호출 / 키 확인 및 자가진단 수행
def student_check():
  global StudentKEY
  if(os.path.isfile("./students/"+StudentKEY+".json")):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    with open("./students/"+StudentKEY+".json", 'r') as f:
      json_data = json.load(f)
      draw.text((0, 0), json_data["name"], font=font3, fill=255)
    draw.text((0, 35), "Now Scuvid-ing...", font=font2, fill=255)
    oled.image(image)
    oled.show()
    GPIO.output(LED_BLUE_PIN, GPIO.HIGH)
    os.system("python3 scuvid_work.py ./students/"+StudentKEY+".json")
    
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_BLUE_PIN, GPIO.LOW)
    reset_screen()
  else:
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "Wrong", font=font, fill=255)
    draw.text((0, 20), "Student ID", font=font2, fill=255)
    draw.text((0, 35), "Try Again", font=font2, fill=255)
    oled.image(image)
    oled.show()
    GPIO.output(LED_RED_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_RED_PIN, GPIO.LOW)
    reset_screen()

#******************************************#

# printKey를 키패드 라이브러리에 등록
keypad.registerKeyPressHandler(printKey)

# 초기화면 출력
def reset_screen():
  image = Image.new("1", (oled.width, oled.height))
  draw = ImageDraw.Draw(image)
  draw.text((0, 0), "Self Covid", font=font, fill=255)
  draw.text((0, 20), "Automanation", font=font2, fill=255)
  draw.text((0, 30), "Wahcome!", font=font2, fill=255)
  oled.image(image)
  oled.show()

def main():
  # Main program block
  oled.fill(0)
  oled.show()
  reset_screen()
  
  #계속 기다림
  while True:
      time.sleep(1)


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    #Ctrl-C 종료시 GPIO CLEANUP, OLED 비움
    oled.fill(0)
    oled.show()
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.cleanup()
