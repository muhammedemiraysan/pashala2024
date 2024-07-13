import serial
import time
from kumanda import JoystickController
# Seri port ayarları
port = 'COM11'  # Windows için örnek. Linux/Mac için '/dev/ttyUSB0' veya '/dev/ttyACM0' olabilir.
baudrate = 115200
ser = serial.Serial(port, baudrate, timeout=1)
kumanda = JoystickController()
def send_command(command):
    ser.write((command + '\n').encode('utf-8'))  # Komutu gönder
    response = ser.readline().decode('utf-8').strip()  # Cevabı oku
    return response

try:
    while True:
        command = str(kumanda.get_axes_values())
        response = send_command(command)
        print("Pico'dan gelen cevap:", response)
except KeyboardInterrupt:
    print("Program durduruldu.")
finally:
    ser.close()
