import cv2
import json
import os

class CircleDetection:
    def __init__(self, camera_port=0):
        self.camera_port = camera_port
        self.cap = cv2.VideoCapture(self.camera_port)
        if not self.cap.isOpened():
            raise Exception("Kamera açılamıyor!")

        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Video Stream Size: {self.frame_width}x{self.frame_height}")

        # Nişangah ayarları
        self.crosshair_x = self.frame_width // 2
        self.crosshair_y = self.frame_height // 2
        self.crosshair_size = 50

        # Trackbar oluşturma
        cv2.namedWindow('Control Panel')
        cv2.createTrackbar('Crosshair X', 'Control Panel', self.crosshair_x, self.frame_width, self.update_crosshair)
        cv2.createTrackbar('Crosshair Y', 'Control Panel', self.crosshair_y, self.frame_height, self.update_crosshair)
        cv2.createTrackbar('Crosshair Size', 'Control Panel', self.crosshair_size, min(self.frame_width, self.frame_height) // 2, self.update_crosshair)
        cv2.createTrackbar('Reset', 'Control Panel', 0, 1, self.reset_crosshair)
        cv2.createTrackbar('Save Settings', 'Control Panel', 0, 1, self.save_settings_trackbar)
        cv2.createTrackbar('Load Settings', 'Control Panel', 0, 1, self.load_settings_trackbar)
        # Yüklenen ayarları
        self.load_settings()

    def update_crosshair(self, _):
        # Trackbar'lardan ayarları al
        self.crosshair_x = cv2.getTrackbarPos('Crosshair X', 'Control Panel')
        self.crosshair_y = cv2.getTrackbarPos('Crosshair Y', 'Control Panel')
        self.crosshair_size = cv2.getTrackbarPos('Crosshair Size', 'Control Panel')

    def reset_crosshair(self, _):
        # Reset işlevi: Trackbar'ları sıfırla
        self.crosshair_x = self.frame_width // 2
        self.crosshair_y = self.frame_height // 2
        self.crosshair_size = 50

        # Trackbar'ları güncelle
        cv2.setTrackbarPos('Crosshair X', 'Control Panel', self.crosshair_x)
        cv2.setTrackbarPos('Crosshair Y', 'Control Panel', self.crosshair_y)
        cv2.setTrackbarPos('Crosshair Size', 'Control Panel', self.crosshair_size)
        
        # Ayarları kaydet
        self.save_settings()

    def save_settings(self, _=None):
        settings = {
            'crosshair_x': self.crosshair_x,
            'crosshair_y': self.crosshair_y,
            'crosshair_size': self.crosshair_size
        }
        with open('settings.json', 'w') as file:
            json.dump(settings, file)
        print("Ayarlar kaydedildi!")

    def save_settings_trackbar(self, _):
        # Kaydetme işlevi: Trackbar değerlerini kaydet
        self.save_settings()

    def load_settings_trackbar(self, _):
        # Yükleme işlevi: Trackbar değerlerini yükle
        self.load_settings()

    def load_settings(self):
        if os.path.exists('settings.json'):
            with open('settings.json', 'r') as file:
                settings = json.load(file)
                self.crosshair_x = settings.get('crosshair_x', self.frame_width // 2)
                self.crosshair_y = settings.get('crosshair_y', self.frame_height // 2)
                self.crosshair_size = settings.get('crosshair_size', 50)

                # Trackbar'ları güncelle
                cv2.setTrackbarPos('Crosshair X', 'Control Panel', self.crosshair_x)
                cv2.setTrackbarPos('Crosshair Y', 'Control Panel', self.crosshair_y)
                cv2.setTrackbarPos('Crosshair Size', 'Control Panel', self.crosshair_size)
            print("Ayarlar yüklendi!")
        else:
            print("Ayarlar dosyası bulunamadı!")

    def draw_crosshair(self, frame):
        # Nişangah çiz
        cv2.line(frame, (self.crosshair_x - self.crosshair_size, self.crosshair_y), (self.crosshair_x + self.crosshair_size, self.crosshair_y), (0, 255, 255), 2)
        cv2.line(frame, (self.crosshair_x, self.crosshair_y - self.crosshair_size), (self.crosshair_x, self.crosshair_y + self.crosshair_size), (0, 255, 255), 2)

    def run(self):
        ret, self.frame = self.cap.read()
        if not ret:
            print("Kare alınamıyor!")
            return {}

        # Nişangah çiz
        self.draw_crosshair(self.frame)

        cv2.imshow('Video Stream', self.frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            return {}  # Return an empty dictionary after closing the window
        
        return {}  # Return an empty dictionary for each frame processed

# Usage
if __name__ == "__main__":
    circle_detection = CircleDetection()
    while True:
        results = circle_detection.run()
        if results:
            print("No results found.")
