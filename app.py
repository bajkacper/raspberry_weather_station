import subprocess
import threading
from flask import Flask, render_template, jsonify, request
import time
from  datetime import datetime
import Adafruit_CharLCD as LCD
try:
        from smbus import SMBus
except ImportError:
        from smbus import SMBus
from bme280 import BME280
import RPi.GPIO as GPIO
from gpiozero import Buzzer
app = Flask(__name__)

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#sensor 
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

#buttons
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(0,GPIO.IN, pull_up_down=GPIO.PUD_UP)

#buzzer
BUZZER = 16
GPIO.setup(BUZZER, GPIO.OUT)
def buzz(noteFreq, duration):
        halveWaveTime = 1 / (noteFreq * 2 )
        waves = int(duration * noteFreq)
        for i in range(waves):
                GPIO.output(BUZZER, True)
                time.sleep(halveWaveTime)
                GPIO.output(BUZZER, False)
                time.sleep(halveWaveTime)


def play():
    t = 0
    notes = [262, 294, 330, 262, 262, 294, 330, 262, 330, 349, 392, 330, 349, 392, 392, 440, 392, 349, 330, 262, 392,
             440, 392, 349, 330, 262, 262, 196, 262, 262, 196, 262]
    duration = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5,
                0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 1]
    for n in notes:
        buzz(n, duration[t])
        time.sleep(duration[t] * 0.1)
        if GPIO.input(6) == GPIO.LOW or GPIO.input(13) == GPIO.LOW or GPIO.input(19) == GPIO.LOW or GPIO.input(
                5) == GPIO.LOW or GPIO.input(0) == GPIO.LOW:
            break
        t += 1

# LCD
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

def led(ports):
	GPIO.output(21, GPIO.LOW)
	GPIO.output(20, GPIO.LOW)
	GPIO.output(26, GPIO.LOW)
	GPIO.output(ports, GPIO.HIGH)

# other variables
isWeather = False;
lcd.clear()
lcd.message("HELLO KACPER")
#RGB
def rgb():
    RUNNING = True

    green = 20
    red = 21
    blue = 26

    GPIO.setup(red, GPIO.OUT)
    GPIO.setup(green, GPIO.OUT)
    GPIO.setup(blue, GPIO.OUT)

    Freq = 100
    RED = GPIO.PWM(red,Freq)
    GREEN = GPIO.PWM(green, Freq)
    BLUE = GPIO.PWM(blue, Freq)
    while RUNNING:
            RED.start(100)
            GREEN.start(1)
            BLUE.start(1)
            for x in range(1,101):
                    GREEN.ChangeDutyCycle(x)
                    time.sleep(0.05)
            for x in range(1,101):
                    RED.ChangeDutyCycle(101-x)
                    time.sleep(0.025)
            for x in range(1,101):
                    GREEN.ChangeDutyCycle(101-x)
                    BLUE.ChangeDutyCycle(x)
                    time.sleep(0.025)
            for x in range(1,101):
                    RED.ChangeDutyCycle(x)
                    time.sleep(0.025)
            RUNNING = False
    RED.start(0)
    GREEN.start(0)
    BLUE.start(0)
    GPIO.cleanup(20)
    GPIO.cleanup(21)
    GPIO.cleanup(26)

lcd.clear()


alarm_set=False

#alarm
set_hour = 0
set_minute = 0
set_second = 0
hour = 0
minute = 0
def set_alarm_p():
    global set_hour
    global set_minute
    global set_second
    global hour
    global alarm
    global minute
    global alarm_set
    alarm_set = True
    lcd.clear()
    lcd.show_cursor(True)
    lcd.message("Set hour:")

    while GPIO.input(0) != GPIO.LOW:  
        if GPIO.input(13) == GPIO.LOW:  
            set_hour += 1
            time.sleep(0.2)
            set_hour = set_hour % 24

        elif GPIO.input(5) == GPIO.LOW:  
            set_hour -= 1
            time.sleep(0.2)
            set_hour = set_hour % 24

        hour = str(set_hour)

        while len(hour) < 2:
            hour = '0' + hour

        lcd.set_cursor(0,1)
        lcd.message(hour)
        lcd.set_cursor(0,1)

    lcd.clear()
    time.sleep(0.4)
    lcd.message("Set minute:")

    while GPIO.input(0) != GPIO.LOW:  
        if GPIO.input(13) == GPIO.LOW:  
            set_minute += 1
            time.sleep(0.2)
            set_minute = set_minute % 60

        elif GPIO.input(5) == GPIO.LOW:  
            set_minute -= 1
            time.sleep(0.2)
            set_minute = set_minute % 60

        minute = str(set_minute)
        while len(minute) < 2:
            minute = '0' + minute

        lcd.set_cursor(0, 1)
        lcd.message(minute)
        lcd.set_cursor(0, 1)

    lcd.clear()
    lcd.show_cursor(False)
    zm = f"{set_hour:02d}:{set_minute:02d}:00"
    save_alarm(True,zm,"lcd")
    return f"{set_hour:02d}:{set_minute:02d}:00"


alarm = "09:00:00"

def display_time():
    global alarm
    global alarm_set
    while True:
        read_alarm("lcd")
        lcd.clear()
        e = datetime.now()
        if e.strftime("%H:%M:%S") == alarm and alarm_set:
            lcd.clear()
            lcd.message("ALARM!!!")
            play()
            lcd.clear()
            alarm_set = False
        lcd.message(e.strftime("%d-%m-%y\n%H:%M:%S"))
        time.sleep(0.8)
        if GPIO.input(19) == GPIO.LOW:
            alarm = set_alarm_p()
            print(alarm)
        if GPIO.input(6) == GPIO.LOW:
            break

def display_temperature():
    global alarm
    global alarm_set
    while True:
         read_alarm("lcd")
         e = datetime.now()
         if e.strftime("%H:%M:%S") == alarm and alarm_set:
                lcd.clear()
                lcd.message("ALARM!!!")
                play()
                lcd.clear()
                alarm_set = False
         lcd.clear()
         temperature = bme280.get_temperature()-3
         if(temperature > 18 and temperature < 22):
                led(26)
         elif temperature <= 18:
                led(20)
         elif temperature >= 22:
                led(21)
         pressure = bme280.get_pressure()
         humidity = bme280.get_humidity()
         lcd.message('{:02.0f}*C {:02.0f}%\n{:03.0f}hPa'.format(temperature, humidity,pressure))
         time.sleep(0.8)
         if GPIO.input(19) == GPIO.LOW:
            alarm = set_alarm_p()
         if GPIO.input(6)==GPIO.LOW:
              break

def zapis_lcd(wzor):
	hours, minutes, seconds = map(int, wzor.split(':'))
	global set_hour
	global set_minute
	set_hour = hours
	set_minute = minutes

def read_alarm(typo):
	try:
		global alarm
		global alarm_set
		with open('alarm.txt', '+r') as file:
			content = file.readlines()
			if content:
				ts = content[2].strip('\n')
				if typo != ts:
					alarm_sett=content[0].strip()
					if alarm_sett == "1":
						alarm_set=True
					else:
						alarm_set=False
					alarm=content[1].strip('\n')
					if typo == "lcd":
						zapis_lcd(alarm)
					file.seek(0)
					file.truncate()
	except FileNotFoundError:
			return False


def save_alarm(alarm_set,alarm,typo):
	try:
		with open('alarm.txt', 'w') as file:
			if alarm_set == True:
				alarm_sett=1
			else:
				alarm_sett=0
			file.write(f"{alarm_sett}\n{alarm}\n{typo}")
	except Exception as e:
		print(f"Błąd podczas zapisywania do pliku: {e}")
def get_temperature():
    temperature = bme280.get_temperature() - 3
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    return '{:02.0f}*C\n{:03.0f}hPa {:02.0f}%'.format(temperature, pressure, humidity)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    data = request.get_json()
    new_alarm = data.get('alarm')

    global alarm
    global alarm_set
    alarm_set = True
    alarm = new_alarm
    save_alarm(True,new_alarm,"server")
    return jsonify({'alarm': new_alarm})

def get_current_time():
    return datetime.now().strftime("%d-%m-%y %H:%M")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_temperature')
def get_temperature_route():
    temperature = get_temperature()
    return jsonify({'temperature': temperature})


@app.route('/get_current_time')
def get_current_time_route():
    current_time = get_current_time()
    return jsonify({'current_time': current_time})

@app.route('/turn_off_alarm', methods=['POST'])
def turn_off_alarm():

    global alarm_set
    global alarm
    alarm_set = False
    save_alarm(False,alarm,"server")
    return jsonify({'message': 'Alarm turned off'})

def get_alarm_status():
    global alarm_set
    read_alarm("server")

    if alarm_set:
        return 'Wlaczony'
    else:
        return 'Wylaczony'


@app.route('/get_alarm_status')
def get_alarm_status_route():
    alarm_status = get_alarm_status()
    return jsonify({'alarm_status': alarm_status})

def get_alarm():
    global alarm
    read_alarm("server")
    return jsonify({'alarm': alarm})

@app.route('/get_alarm')
def get_alarm_route():
    global alarm
    read_alarm("server")
    alarm_status = get_alarm_status()
    alarm_data = {
      'alarm': alarm,
      'status': alarm_status
}
    return jsonify(alarm_data)

def lcd_thread():
    while True:
        display_temperature()
        display_time()
if __name__ == '__main__':
    
    lcd_thread = threading.Thread(target=lcd_thread)
    lcd_thread.start()

    # Running Flask server as seperated process
    subprocess.Popen(["python3", "server.py"])


