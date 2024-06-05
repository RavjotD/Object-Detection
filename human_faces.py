import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685
from picamera2 import Picamera2
import cv2
import numpy as np

class Ultrasonic:
    def __init__(self):        
        GPIO.setwarnings(False)        
        self.trigger_pin = 27
        self.echo_pin = 22
        self.MAX_DISTANCE = 500             # define the maximum measuring distance, unit: cm
        self.timeOut = self.MAX_DISTANCE*30   # calculate timeout according to the maximum measuring distance
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)
        self.servo=Servo()
        self.PWM=Motor()
        self.pwm_S=Servo()
        
    def set_upwards(self):
        self.pwm_S.setServoPwm('1', 135)
        time.sleep(1)
        
    def pulseIn(self,pin,level,timeOut): # obtain pulse time of a pin under timeOut
        t0 = time.time()
        while(GPIO.input(pin) != level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0;
        t0 = time.time()
        while(GPIO.input(pin) == level):
            if((time.time() - t0) > timeOut*0.000001):
                return 0;
        pulseTime = (time.time() - t0)*1000000
        return pulseTime
    
    def get_distance(self):     # get the measurement results of ultrasonic module,with unit: cm
        distance_cm=[0,0,0,0,0]
        for i in range(5):
            GPIO.output(self.trigger_pin,GPIO.HIGH)      # make trigger_pin output 10us HIGH level 
            time.sleep(0.00001)     # 10us
            GPIO.output(self.trigger_pin,GPIO.LOW) # make trigger_pin output LOW level 
            pingTime = self.pulseIn(self.echo_pin,GPIO.HIGH,self.timeOut)   # read plus time of echo_pin
            distance_cm[i] = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s
        distance_cm=sorted(distance_cm)
        return  int(distance_cm[2])
    
    def run_motor(self,L,M,R):
        if (L < 30 and M < 30 and R <30) or M < 30 :
            print("dead end")
            PWM.setMotorModel(-1450,-1450,-1450,-1450) 
            time.sleep(0.1)   
            if L < R:
                PWM.setMotorModel(1450,1450,-1450,-1450)
            else :
                PWM.setMotorModel(-1450,-1450,1450,1450)
        elif L < 30 and M < 30:
            print("turn right")
            PWM.setMotorModel(1500,1500,-1500,-1500)
        elif R < 30 and M < 30:
            print("turn left")
            PWM.setMotorModel(-1500,-1500,1500,1500)
        elif L < 20 :
            print("L<20")
            PWM.setMotorModel(2000,2000,-500,-500)
            if L < 10 :
                print("L<10")
                PWM.setMotorModel(1500,1500,-1000,-1000)
        elif R < 20 :
            print("R<20")
            PWM.setMotorModel(-250,-250,2000,2000)
            if R < 10 :
                print("backward and go left")
                PWM.setMotorModel(-2000,0,-2000,0)  
        else :
            print("freedom")
            self.PWM.setMotorModel(800,800,800,800)
                
    def run(self):
        self.PWM=Motor()
        self.pwm_S=Servo()
        self.pwm_S.setServoPwm('1', 130)
        
        keep_running = True
        
        for i in range(30,151,60):
            self.pwm_S.setServoPwm('0',i)
            time.sleep(0.2)
            if i==30:
                L = self.get_distance()
            elif i==90:
                M = self.get_distance()
            else:
                R = self.get_distance()
            
            if self.detect_faces():
                keep_running = False
                break
            
        while(keep_running):
            for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                    
                if self.detect_faces():
                    keep_running = False
                    break
                
                # self.run_motor(L,M,R)
 
            for i in range(90,30,-60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                    
                if self.detect_faces():
                    keep_running = False
                    break
                #self.run_motor(L,M,R)
                
            for i in range(30,151,60):
                self.pwm_S.setServoPwm('0',i)
                time.sleep(0.2)
                if i==30:
                    L = self.get_distance()
                elif i==90:
                    M = self.get_distance()
                else:
                    R = self.get_distance()
                
                if self.detect_faces():
                    keep_running = False
                    break
                #self.run_motor(L,M,R)
                
    def detect_faces(self):
        im = picam2.capture_array()
        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
        faces = face_detector.detectMultiScale(grey, 1.1, 3)
        
        if (len(faces) > 0):
            for (x, y, w, h) in faces:
                print("Face found")
                cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow('Face Detection', im)
                cv2.waitKey()
            return True
        return False
     
ultrasonic=Ultrasonic()              

if __name__ == '__main__':
    print ('Program is starting ... ')
    ultrasonic.set_upwards()
    time.sleep(1)
    try:
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        cv2.startWindowThread()
        
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        picam2.start() 
        
        print("Hello")
        while(True):
            ultrasonic.run()
    
    except KeyboardInterrupt:
        PWM.setMotorModel(0,0,0,0)
        ultrasonic.pwm_S.setServoPwm('0',90)
        cv2.destroyAllWindows()
