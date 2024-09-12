import sys
import serial
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QCheckBox, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from subsystems.kumanda import JoystickController
from subsystems.PID import PID
from gorevler.gorev3 import ColorDetection
from gorevler.gorev1 import CircleDetection
import pygame

# Sinyal sınıfı
class Communicator(QObject):
    update_motor_speeds_signal = pyqtSignal(list)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Başlangıç ayarları
        self.kapidangec = False
        self.port = 'COM8' 
        self.baudrate = 115200
        self.ser = None
        self.kumanda = None
        self.color_detection = None
        self.pid = PID(1, 0, 0)
        self.manual_mode = False
        self.semi_auto_mode = False
        self.kalibre = False
        while 1:
            try:
                self.ser = serial.Serial(self.port, self.baudrate, timeout=0.03)
                break
            except:
                pass
        # PID ve motor kontrol değişkenleri
        self.pid_valueangle = 0
        self.motor_speeds = [0] * 9  # 9 motor için hızlar
        self.motor_rotations = [1,1,1,-1,-1,-1,-1,-1,1]  # Motor rotasyon yönleri
        self.pidx = 0
        self.pidy = 0

        # Sinyal iletişimi
        self.communicator = Communicator()
        self.communicator.update_motor_speeds_signal.connect(self.update_motor_speeds_display)

        # Arka planda çalışacak iş parçacığı
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()
        
    def init_ui(self):
        self.setWindowTitle('PASHALA')

        # Görev Seçimi
        self.task_label = QLabel('Görev Seçimi')
        self.task_combo = QComboBox()
        self.task_combo.addItems(['Boşta', 'Manuel', 'Yarı Otonom', 'Otonom'])
        self.task_combo.currentIndexChanged.connect(self.update_mode)

        # COM Port Seçimi
        self.com_port_label = QLabel('COM Port Seçimi')
        self.com_port_combo = QComboBox()
        self.com_port_combo.addItems(['COM8', 'COM10', 'COM11'])
        
        # Bağlanma Tuşu
        self.connect_button = QPushButton('Bağlan')
        self.connect_button.clicked.connect(self.connect_serial)

        # Kalibrasyon
        self.calibrate_check = QCheckBox('Kalibrasyon')
        self.calibrate_check.stateChanged.connect(self.toggle_calibration)

        # Motor Hızları
        self.motor_speeds_display = QTextEdit()
        self.motor_speeds_display.setReadOnly(True)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.task_label)
        layout.addWidget(self.task_combo)
        layout.addWidget(self.com_port_label)
        layout.addWidget(self.com_port_combo)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.calibrate_check)
        layout.addWidget(QLabel('Motor Hızları'))
        layout.addWidget(self.motor_speeds_display)
        
        self.update_mode(0)
        self.setLayout(layout)
        self.show()
        
    def update_mode(self, index):
        if index == 1:  # Manuel Mod
            self.manual_mode = True
            self.semi_auto_mode = False
            self.kumanda = JoystickController()
            self.circle_detection = CircleDetection(1)
            
            self.color_detection = None
        elif index == 2:  # Yarı Otonom Mod
            self.manual_mode = False
            self.semi_auto_mode = True
            self.color_detection = None
            self.kumanda = JoystickController()
        elif index == 3:  # Otonom Mod
            self.manual_mode = False
            self.semi_auto_mode = False
            self.color_detection = ColorDetection(0)
            self.kumanda = None
    
    def connect_serial(self):
        port = self.com_port_combo.currentText()
        if self.ser:
            self.ser.close()
        
        
    def toggle_calibration(self, state):
        self.kalibre = (state == Qt.Checked)

    def update_motor_speeds_display(self, motor_speeds):
        motor_names = [
            "Motor 1",
            "Motor 2",
            "Motor 3",
            "Motor 4",
            "Motor 5",
            "Motor 6",
            "Motor 7",
            "Motor 8",
            "Motor 9"
        ]
        
        display_text = "\n".join(f"{name}: {speed}" for name, speed in zip(motor_names, motor_speeds))
        if not self.manual_mode and not self.semi_auto_mode:
            display_text += f"\n\nPID X: {self.pidx}\nPID Y: {self.pidy}"
        
        self.motor_speeds_display.setPlainText(display_text)

    def send_command(self, command):
        if self.ser:
            try:
                self.ser.write((command + '\n').encode('utf-8'))
                response = self.ser.readline().decode('utf-8').strip()
                print(f"Sent: {command}, Received: {response}")
                return response
            except Exception as e:
                print(f"Failed to send command: {e}")
                return None
    def update_motor_speeds(self, forward_backward, left_right, up_down, turret, servo, pid_valueangle, crab):
        self.motor_speeds[0] = (forward_backward - left_right) * self.motor_rotations[0]
        self.motor_speeds[1] = (up_down - pid_valueangle) * self.motor_rotations[1]
        self.motor_speeds[2] = (forward_backward - left_right) * self.motor_rotations[2]
        self.motor_speeds[3] = (forward_backward + left_right) * self.motor_rotations[3]
        self.motor_speeds[4] = (up_down + pid_valueangle) * self.motor_rotations[4]
        self.motor_speeds[5] = (forward_backward + left_right) * self.motor_rotations[5]
        self.motor_speeds[6] = turret * self.motor_rotations[6]
        self.motor_speeds[7] = turret * self.motor_rotations[7]
        self.motor_speeds[8] = servo * self.motor_rotations[8]
        self.communicator.update_motor_speeds_signal.emit(self.motor_speeds)

    def run(self):
        while True:
            try:
                if self.manual_mode:
                    results = self.circle_detection.run()
                    if self.kumanda:
                        self.kumanda.listen()
                        self.update_motor_speeds(
                            self.kumanda.axis_data.get(1),
                            self.kumanda.axis_data.get(0),
                                -self.kumanda.axis_data.get(2),
                                self.kumanda.button_data.get(0),
                                self.rotation(self.kumanda.button_data.get(2)),
                                self.pid_valueangle,
                                self.kumanda.axis_data.get(3)
                            )
                elif self.semi_auto_mode:
                    if self.kumanda:
                        self.kumanda.listen()
                        self.update_motor_speeds(
                            self.kumanda.axis_data.get(1),
                            self.kumanda.axis_data.get(0),
                            -self.kumanda.axis_data.get(2),
                            self.kumanda.button_data.get(0),
                            self.rotation(self.kumanda.button_data.get(2)),
                            self.pid_valueangle,
                            self.kumanda.axis_data.get(3)
                        )
                else:  # Otonom Mod
                    if self.color_detection:
                        results = self.color_detection.run()
                        if results:
                            for key, value in results.items():
                                screen_width = 720
                                screen_height = 960
                                center = value['center']
                                center_x = center[0]
                                center_y = center[1]
                                pid_x = (screen_width/2) - center_x
                                pid_y = (screen_height/2) - center_y
                                
                                self.pidx = self.map_value(pid_x, -screen_width / 2, screen_width / 2, -1, 1)
                                self.pidy = self.map_value(pid_y, -screen_height / 2, screen_height / 2, -1, 1)
                                
                                if self.pid.is_within_tolerance(self.pidx, 0, 0.1) and self.pid.is_within_tolerance(self.pidy, 0, 0.1):
                                    #kapıdan geç
                                    self.kapidangec = True
                                else:
                                    self.update_motor_speeds(0, 0, -self.pidy, 0, 0, self.pid_valueangle, self.pidx)
                        else:
                            self.update_motor_speeds(0, 0, 0, 0, 0, self.pid_valueangle, 0)

                command = ','.join(map(str, self.motor_speeds))
                response = self.send_command(command)
                print(response)
                # if self.manual_mode or self.semi_auto_mode:
                #     self.pid_valueangle = 0
                # else:
                #     pass
            except KeyboardInterrupt:
                print("Program durduruldu.")
                break
            except Exception as e:
                print(f"Bir hata oluştu: {e}")

        # Kapatma işlemleri
        self.update_motor_speeds(0, 0, 0, 0, 0, self.pid_valueangle, 0)
        self.send_command(','.join(map(str, self.motor_speeds)))
    def map_value(self, value, from_min, from_max, to_min, to_max):
        return (value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min
    
    def rotation(self, a):
        return 1 if a else -1
    
    def update_ui(self):
        # Perform any necessary UI updates here
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
