import firebase_admin
import RPi.GPIO as GPIO
import time
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("housekeeper4-c499d-firebase-adminsdk-lfhja-b0f0d8483e.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

doc_ref_doorlock=db.collection(u'housekeeper').document(u'doorlock')# motor data 
doc_ref_detect=db.collection(u'housekeeper').document(u'detect')# detect data 0: user / 1: stranger
doc_ref_detect.set({#initial value 0:no detect
	u'detect' : "0"
})
doc_ref_doorlock.set({#initial value 0:no detect
	u'doorlock' : "1"
})


motorpin=18#use GPIO number
trigpin=2#microwave T
echopin=3#microwave R

#initialize element
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorpin,GPIO.OUT)
GPIO.setup(trigpin,GPIO.OUT)
GPIO.setup(echopin,GPIO.IN)

#initialize motor angle
motormove=GPIO.PWM(motorpin,50)
motormove.start(0)
motormove.ChangeDutyCycle(2.5)
time.sleep(1)
#function
def distance_cal():
    GPIO.output(trigpin, True)
    time.sleep(0.00001)
    GPIO.output(trigpin, False)    
    while GPIO.input(echopin) == 0:
        pass
    start = time.time()
    while GPIO.input(echopin) == 1:
        pass
    stop = time.time()
    TimeElapsed = stop - start
    distance = (TimeElapsed*34300)/2
    time.sleep(1)
    print("measured distance = %.1f cm" % distance)
    if(distance < 50):
        return 1
    else :
        return 0


while True:
    #door open open/close if
    button = distance_cal()
    if button == 0 :
        print('door locked')
    elif button == 1:
        print('door open')
        print('User : 0 stranger: 1')
        detect = input()#model input
        
        if detect == '0' :#face recognize -> 0 : user / 1 : stranger
            print('user recognized')
        elif detect == '1':
            print('stranger recognized')
            #video streaming
            doc_ref_detect.set({
                u'detect' : '1'
            })
            # user button click!!
            k=1
            while True:
                doorlock=doc_ref_doorlock.get().to_dict()
                print(doorlock)
                time.sleep(1)
                k=k+1
                if doorlock == {'doorlock': '0'}:
                    print("door lock clear")
                    motormove.ChangeDutyCycle(7.5)
                    time.sleep(2)
                    break
                if k == 50:
                    doc_ref_detect.set({
                        u'detect' : '0'
                    })
                    break