import sys
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
#opsiyonel muhtemelen kullanmayız
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_RGB888)
        image_label.setPixmap(QtGui.QPixmap.fromImage(image))
def connect_function():
    baglanti_label.setText(f"Bağlanti: ✓")
def close_app():
    cap.release()
    app.quit()
def get_connection():
    return baglanti_label.text()
app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Kamera Uygulaması")

# Giriş kutuları
input1 = QtWidgets.QLineEdit(window)
input1.setPlaceholderText("Değişken 1")
input2 = QtWidgets.QLineEdit(window)
input2.setPlaceholderText("Değişken 2")

# Connect butonu
connect_button = QtWidgets.QPushButton("Connect", window)
connect_button.clicked.connect(connect_function)

# Sensör verisi göstergeleri
sensor_label1 = QtWidgets.QLabel("Sensör Verisi 1: ---", window)
sensor_label2 = QtWidgets.QLabel("Sensör Verisi 2: ---", window)
baglanti_label = QtWidgets.QLabel("Bağlanti: X", window)
# Kamera görüntü alanı
image_label = QtWidgets.QLabel(window)
image_label.setFixedSize(640, 480)

# Layout
layout = QtWidgets.QVBoxLayout()
layout.addWidget(input1)
layout.addWidget(input2)
layout.addWidget(connect_button)
layout.addWidget(sensor_label1)
layout.addWidget(sensor_label2)
layout.addWidget(baglanti_label)
layout.addWidget(image_label)
window.setLayout(layout)

# Timer
timer = QtCore.QTimer()
timer.timeout.connect(update_frame)
cap = cv2.VideoCapture(0)  # Kamerayı başlat
timer.start(30)

# Uygulamayı kapatırken kamerayı serbest bırakma
window.closeEvent = lambda event: close_app()

window.show()
sys.exit(app.exec_())
