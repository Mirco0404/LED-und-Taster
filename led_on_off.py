import RPi.GPIO as GPIO
import time
import sqlite3
from datetime import datetime


GPIO.setmode(GPIO.BOARD)

ledState = False

class SQLite:
    def __init__(self, file):
        self.file = file
        self.con = sqlite3.connect(self.file)
        self.cur = self.con.cursor()
        
        #try:
            #tmp = open('example.sql')
            #sql = tmp.read()
            #self.cur.executescript(sql)
        #except:
            #pass
        
    def execute(self, script):
        self.con.execute(script)
        self.con.commit()
        
     
class LED:
    def __init__(self, pin):
        self.pin = pin
        self.state = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        
    def state(self):
        self.state = not self.state
    
    def on_off(self):
        GPIO.output(self.pin, self.state)
        
class Button:
    def __init__(self, pin):
        self.pin = pin
        self.pos = None
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    def is_pressed(self):
        return bool(GPIO.input(37))
        
        
led = LED(38)
bt = Button(37)
db = SQLite('/home/pi/Desktop/PC/led.db')

try:
    while True:
        bt.is_pressed()
        if GPIO.input(37) == True:
            buttonTimepressed = time.time()
            while GPIO.input(37) == GPIO.HIGH:
                #print("t")
                buttonTimepressed2 = time.time()
                timz = buttonTimepressed2 - buttonTimepressed
                #print(timz)
                
        else:
            timz = 0
            #print("t2")
                
        if float(timz) <= 1 and float(timz) > 0:
            ledState = not ledState
            #print(ledState)
            date_time_now = datetime.now()
            #print(date_time_now)
            time_now = date_time_now.strftime("Date: %d-%b-%Y | Time: %H:%M:%S.%f")
            print(time_now)
            #print(type(time_now))
            #db.execute(f'INSERT INTO status(led_status) VALUES ("{ledState}")')
        #try:
            db.execute(f'INSERT INTO status(led_status) VALUES ("{ledState}")')
            #print("Insertet")
        #except sqlite3.Error as er:
            #print('SQLite error: %s' % (' '.join(er.args)))
            #print("Exception class is: ", er.__class__)
            #print('SQLite traceback: ')
            #exc_type, exc_value, exc_tb = sys.exc_info()
            #print(traceback.format_exception(exc_type, exc_value, exc_tb))
                
                
                
        if ledState == True:
            GPIO.output(38, GPIO.HIGH)
        else:
            GPIO.output(38, GPIO.LOW)
            #print('test2')
                
except KeyboardInterrupt:
    GPIO.cleanup()
    