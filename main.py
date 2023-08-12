# Built by Raymond Family

from imu import MPU6050
import time
from machine import Pin, I2C, ADC
led = Pin(25, Pin.OUT)
led.value(0)

from MCP49XX import MCP
C_SELECT = 13
myMCP = MCP("MCP4922", C_SELECT) #Creation of an MCP object instance MCP(chipName, chipSelectPin)

#i2cm = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
i2ch = I2C(1, sda=Pin(18), scl=Pin(19), freq=400000)
#i2cdac = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)

#imum = MPU6050(i2cm)
imuh = MPU6050(i2ch)

adcx = ADC(Pin(26))
adcy = ADC(Pin(27))

#Compensation Gyro
cgxh = 0.7
cgyh = 1.2
cgzh = 1

#compensation joystick
cadcx = 31847
cadcy = 33032

led.value(1)

while True:
    # Déclaration
    gyhc = 0
    gzhc = 0
    # Following print shows original data get from libary. You can uncomment to see raw data
    #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')
    #timer.init(freq=25, mode=Timer.PERIODIC, callback=blink)
    # Following rows round values get for a more pretty print:
    #gxm=round(imum.gyro.x+cgxm,1)
    #gym=round(imum.gyro.y+cgym,1)
    #gzm=round(imum.gyro.z+cgzm,1)
    # lecture gyroTête: capteur sur coté droit de la tête
    #gxh=round(imuh.gyro.x+cgxh,1)    #tete regarder à gauche ou droite: + vers la gauche et - vers la droite
    gyh=round(imuh.gyro.y+cgyh,1)    # pencher à gauche ou a droite
    if gyh > 2:
        gyhc = gyh + 56
    if gyh < -2:
        gyhc = gyh - 56
    #tete regarder en haut ou en bas
    gzh=round(imuh.gyro.z+cgzh,1)
    if gzh > 2:
        gzhc = gzh + 50
    if gzh < -2:
        gzhc = gzh - 50
   # Lecture info joystick, connecteur vers le bas
    radcx = adcx.read_u16()
    radcy = adcy.read_u16()
    #print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
    #print(gyh,"\t",gyhc,"\t",end="\r")
    #print(radcx,"\t",radcy)
    #print(racdx-cacdx,"\t",racdy-cacdy)
    # calcul de la valeur de X doit etre entre 0 et 500:
    # le but est de tout ramener une valeur de + ou - 250. 131,072=16(bit)*8,192
    #valeur haut bas
    outputvaluex = round(2048+(((radcx-cadcx)/16)*0.75)+(-gzhc*8*1))#+(gxm*8*0.05))# info de gyro *8 pour passer de + ou - 250 à + ou - 2048
    if outputvaluex > 4095:
        outputvaluex == 4095
    if outputvaluex < 1:
        outputvaluex == 1
    #valeur gauche droit
    outputvaluey = round(2048+(((radcy-cadcy)/16)*0.75)+(-gyhc*8*1))#+(gym*8*0.05))
    if outputvaluey > 4095:
        outputvaluey == 4095
    if outputvaluey < 1:
        outputvaluey == 1  

    # Injection de la tension
    myMCP.writevalueA(outputvaluex)
    myMCP.writevalueB(outputvaluey)
       
    time.sleep(0.01)


