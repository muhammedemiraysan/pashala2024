import serial, time
from kumanda import JoystickController
from PID import PID
import pygame
from gorev3 import ColorDetection
port = 'COM8'
Sensor_Pressure = 0
Sensor_Voltage = 0
kv = 0
kp = 0
kx = 0
ky = 0
gx = 0
gy = 0
baudrate = 115200
pid = PID(1,0,0)
kalibre = False
manuel = True
if manuel:
    kumanda = JoystickController()
if not manuel:
    color_detection = ColorDetection(1)
    while 1:
        try:
            results = color_detection.run()
            break
        except:
            print("kamera hatası")
            time.sleep(0.1)
while 1:
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        break
    except:
        print("robota bağlantı hatası")
        time.sleep(0.1)
        
pid_valueangle = 0
motor_speeds = [0] * 9  # 9 motor için hızlar
motor_rotations = [1,1,-1,1,1,1,-1,-1,1] # sol ön , sol üst , sol arka , sağ ön , sağ üst , sağ arka, sol atış , sağ atış , servo
def send_command(command):
    ser.write((command + '\n').encode('utf-8'))  # Komutu gönder
    response = ser.readline().decode('utf-8').strip()  # Cevabı oku
    return response
def update_motor_speeds(forward_backward, left_right, up_down, turret, servo, pid_valueangle, crab):
    motor_speeds[0] = (forward_backward - left_right + crab) * motor_rotations[0]  # sol ön motor
    motor_speeds[1] = (up_down - pid_valueangle) * motor_rotations[1] # sol üst motor
    motor_speeds[2] = (forward_backward - left_right - crab) * motor_rotations[2] # sol arka motor
    motor_speeds[3] = (forward_backward + left_right - crab) * motor_rotations[3]  # sağ ön motor
    motor_speeds[4] = (up_down + pid_valueangle) * motor_rotations[4] # sağ üst motor
    motor_speeds[5] = (forward_backward + left_right + crab) * motor_rotations[5]  # sağ arka motor
    motor_speeds[6] = turret * motor_rotations[6] # sol atış
    motor_speeds[7] = turret * motor_rotations[7] # sağ atış
    motor_speeds[8] = servo * motor_rotations[8] # servo1

    # motor_speeds[3] = 0
    # motor_speeds[5] = 0
    # print((forward_backward + left_right) * motor_rotations[5], (forward_backward + left_right) * motor_rotations[3])
def map(value, in_min, in_max, out_min, out_max):
    scale = (out_max - out_min) / (in_max - in_min)
    mapped_value = out_min + (value - in_min) * scale
    return mapped_value
def rotation(a):
    if a == True:
        return 1
    if a == False:
        return -1
try:
    update_motor_speeds(0,0,0,0,0,pid_valueangle,0)
    while True:
        
        #print(kumanda.joystick.get_axis(3))
        if manuel:
            #color_detection.run()
            #print(Sensor_Pressure)
            #print(f"gx:{gx} kx:{kx} gy:{gy} ky:{ky} voltage:{Sensor_Voltage} kv:{kv} pressure:{Sensor_Pressure} kp:{kp}" )
            #print(motor_speeds[1],motor_speeds[4])
            kumanda.listen()
            if kumanda.keyboard_data.get(pygame.K_o):
                #color_detection = ColorDetection(1)
                manuel = False
            elif kumanda.keyboard_data.get(pygame.K_k):
                if kalibre == False:
                    kp = Sensor_Pressure
                    kv = Sensor_Voltage
                    kx = gx
                    ky = gy
                kalibre = True
            #results = color_detection.run()
            #print(kumanda.axis_data.get(2))
            print(kumanda.button_data.get(2))
            update_motor_speeds(
                kumanda.axis_data.get(1),
                kumanda.axis_data.get(0),
                -kumanda.axis_data.get(2),
                kumanda.button_data.get(0),
                rotation(kumanda.button_data.get(2)),
                pid_valueangle,
                kumanda.axis_data.get(3)
                )
        else: #otonom
            #pid_valueangle = pid.compute(0,float(gy))
            #print(results)
            results = color_detection.run()
            try:
                if results:
                    for key, value in results.items():
                        width = value['width']
                        height = value['height']
                        center = value['center']
                        print(f"ID: {key} -> Center: {center}")
                    pidy = map(pid.compute(height/2,center[1]),-320,320,-1,1)
                    pidx = map(pid.compute(width/2,center[0]),-240,240,-1,1)
                    print(pidx,pidy)
                    update_motor_speeds(0,0,-pidy,0,0,pid_valueangle,pidx/10)
            except:
                update_motor_speeds(0,0,0,0,0,pid_valueangle,0)
                #update_motor_speeds(0.3,0.3,-0.3,0,0,pid_valueangle,0,0)
                print("gezin")
        response = send_command(
            str(motor_speeds[0]) + ","
            + str(motor_speeds[1]) + ","
            + str(motor_speeds[2]) + ","
            + str(motor_speeds[3]) + ","
            + str(motor_speeds[4]) + ","
            + str(motor_speeds[5]) + ","
            + str(motor_speeds[6]) + ","
            + str(motor_speeds[7]) + ","
            + str(motor_speeds[8]))
        #gy, gx, Sensor_Voltage, Sensor_Pressure = response.split(',')
        #Sensor_Voltage = float(Sensor_Voltage)-kv
        #Sensor_Pressure = float(Sensor_Pressure)-kp
        #gx = float(gx)-kx
        #gy = float(gy)-ky
        
        if manuel:    
            pid_valueangle = 0
                #print("Pico'dan gelen cevap:", response)
        else: #otonom
            pass
            #pid_valueangle = pid.compute(0,float(gy))
except KeyboardInterrupt:
    print("Program durduruldu.")
finally:
    update_motor_speeds(0,0,0,0,0,pid_valueangle,0)
    response = send_command(
            str(motor_speeds[0]) + ","
            + str(motor_speeds[1]) + ","
            + str(motor_speeds[2]) + ","
            + str(motor_speeds[3]) + ","
            + str(motor_speeds[4]) + ","
            + str(motor_speeds[5]) + ","
            + str(motor_speeds[6]) + ","
            + str(motor_speeds[7]) + ","
            + str(motor_speeds[8]))
    ser.close()
