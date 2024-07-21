import serial
import time
from kumanda import JoystickController
from motoryonsecim import ROVController
# Seri port ayarları
port = 'COM11'  # Windows için örnek. Linux/Mac için '/dev/ttyUSB0' veya '/dev/ttyACM0' olabilir.
baudrate = 115200
ser = serial.Serial(port, baudrate, timeout=1)
kumanda = JoystickController()
motor_speeds = [0] * 8  # 8 motor için hızlar
def send_command(command):
    ser.write((command + '\n').encode('utf-8'))  # Komutu gönder
    response = ser.readline().decode('utf-8').strip()  # Cevabı oku
    return response
# İleri-geri, sağ-sol ve yukarı-aşağı kontrolü
def update_motor_speeds(forward_backward, left_right, up_down, turret):
    motor_speeds[0] = forward_backward - left_right  # sol ön motor
    motor_speeds[1] = up_down # sol üst motor
    motor_speeds[2] = forward_backward - left_right  # sol arka motor
    motor_speeds[3] = forward_backward + left_right  # sağ ön motor
    motor_speeds[4] = up_down  # sağ üst motor
    motor_speeds[5] = forward_backward + left_right  # sağ arka motor
    motor_speeds[6] = up_down
    motor_speeds[7] = -up_down
try:
    while True:
        command = str(kumanda.get_axes_values())
        update_motor_speeds(kumanda.joystick.get_axis(1),kumanda.joystick.get_axis(0),kumanda.joystick.get_axis(2),kumanda.joystick.get_axis(3))
        response = send_command(str(motor_speeds[0]) + "," + str(motor_speeds[1]) + "," + str(motor_speeds[2]) + "," + str(motor_speeds[3]) + "," + str(motor_speeds[4]) + "," + str(motor_speeds[5]) + str(motor_speeds[6]) + "," + str(motor_speeds[7]))
        print("Pico'dan gelen cevap:", response)
except KeyboardInterrupt:
    print("Program durduruldu.")
finally:
    ser.close()
