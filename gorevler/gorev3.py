import cv2
import numpy as np
import json
import os

class ColorDetection:
    def __init__(self, camera_port=0):
        self.selected_color = {
            'lower_h': 0, 'lower_s': 0, 'lower_v': 0,
            'upper_h': 179, 'upper_s': 255, 'upper_v': 255
        }
        self.camera_port = camera_port
        self.cap = cv2.VideoCapture(self.camera_port)
        
        if not self.cap.isOpened():
            raise Exception("Kamera açılamıyor!")

        # Ekran boyutunu 6/4 oranında artır
        original_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_width = int(original_width * 1.5)
        self.frame_height = int(original_height * 1.5)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        print(f"Video Stream Size: {self.frame_width}x{self.frame_height}")

        self.create_color_trackbars()
        self.load_selected_color()
        self.create_color_selection_window()
        
        self.color_buttons = {
            'Green': (50, 100, 70, 100, 255, 255),
            'Blue': (100, 80, 120, 130, 255, 255),
            'Red': (150, 100, 100, 180, 255, 255),
            'Yellow': (0, 100, 100, 30, 255, 255)
        }
        self.current_color = None

    def create_color_trackbars(self):
        cv2.namedWindow('Color Trackbars')
        cv2.createTrackbar('Lower H', 'Color Trackbars', 0, 179, self.update_color)
        cv2.createTrackbar('Lower S', 'Color Trackbars', 0, 255, self.update_color)
        cv2.createTrackbar('Lower V', 'Color Trackbars', 0, 255, self.update_color)
        cv2.createTrackbar('Upper H', 'Color Trackbars', 179, 179, self.update_color)
        cv2.createTrackbar('Upper S', 'Color Trackbars', 255, 255, self.update_color)
        cv2.createTrackbar('Upper V', 'Color Trackbars', 255, 255, self.update_color)

    def update_color(self, _):
        lower_h = cv2.getTrackbarPos('Lower H', 'Color Trackbars')
        lower_s = cv2.getTrackbarPos('Lower S', 'Color Trackbars')
        lower_v = cv2.getTrackbarPos('Lower V', 'Color Trackbars')
        upper_h = cv2.getTrackbarPos('Upper H', 'Color Trackbars')
        upper_s = cv2.getTrackbarPos('Upper S', 'Color Trackbars')
        upper_v = cv2.getTrackbarPos('Upper V', 'Color Trackbars')

        self.selected_color = {
            'lower_h': lower_h,
            'lower_s': lower_s,
            'lower_v': lower_v,
            'upper_h': upper_h,
            'upper_s': upper_s,
            'upper_v': upper_v
        }
        self.save_selected_color()

    def create_color_selection_window(self):
        cv2.namedWindow('Color Selection')
        # Renk seçim penceresinin boyutunu yarıya indir
        self.color_selection = np.zeros((75, 600, 3), dtype=np.uint8)  
        cv2.rectangle(self.color_selection, (0, 0), (150, 75), (0, 255, 0), -1)  # Green
        cv2.rectangle(self.color_selection, (150, 0), (300, 75), (255, 0, 0), -1)  # Blue
        cv2.rectangle(self.color_selection, (300, 0), (450, 75), (0, 0, 255), -1)  # Red
        cv2.rectangle(self.color_selection, (450, 0), (600, 75), (0, 255, 255), -1)  # Yellow
        cv2.imshow('Color Selection', self.color_selection)
        cv2.setMouseCallback('Color Selection', self.select_color)

    def select_color(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if y < 75:
                if x < 150:
                    self.current_color = self.color_buttons['Green']
                elif x < 300:
                    self.current_color = self.color_buttons['Blue']
                elif x < 450:
                    self.current_color = self.color_buttons['Red']
                else:
                    self.current_color = self.color_buttons['Yellow']
                self.update_trackbars()

    def update_trackbars(self):
        if self.current_color:
            lower_h, lower_s, lower_v, upper_h, upper_s, upper_v = self.current_color
            cv2.setTrackbarPos('Lower H', 'Color Trackbars', lower_h)
            cv2.setTrackbarPos('Lower S', 'Color Trackbars', lower_s)
            cv2.setTrackbarPos('Lower V', 'Color Trackbars', lower_v)
            cv2.setTrackbarPos('Upper H', 'Color Trackbars', upper_h)
            cv2.setTrackbarPos('Upper S', 'Color Trackbars', upper_s)
            cv2.setTrackbarPos('Upper V', 'Color Trackbars', upper_v)
            self.update_color(None)

    def create_color_mask(self, hsv_image):
        lower_h = self.selected_color['lower_h']
        lower_s = self.selected_color['lower_s']
        lower_v = self.selected_color['lower_v']
        upper_h = self.selected_color['upper_h']
        upper_s = self.selected_color['upper_s']
        upper_v = self.selected_color['upper_v']

        lower_bound = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
        upper_bound = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        if lower_h == 0 and upper_h == 10:
            lower_bound2 = np.array([0, lower_s, lower_v], dtype=np.uint8)
            upper_bound2 = np.array([10, upper_s, upper_v], dtype=np.uint8)
            mask2 = cv2.inRange(hsv_image, lower_bound2, upper_bound2)
            mask |= mask2

        return mask

    def detect_colors(self, frame):
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = self.create_color_mask(hsv_image)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def analyze_contours(self, frame, contours):
        results = {}
        for i, contour in enumerate(contours):
            if cv2.contourArea(contour) > 500:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                if len(approx) >= 4:
                    rect = cv2.minAreaRect(approx)
                    box = cv2.boxPoints(rect)
                    box = np.array(box, dtype=np.int32)
                    center, (w, h), _ = rect
                    cX, cY = int(center[0]), int(center[1])
                    aspect_ratio = w / h if h != 0 else 0
                    shape_type = "Rectangle" if (0.8 <= aspect_ratio <= 1.2) else "Not a Rectangle"
                    command = self.get_direction_command(cX, cY, frame.shape[1], frame.shape[0])

                    results[i] = {
                        "center": (cX, cY),
                        "width": w,
                        "height": h,
                        "aspect_ratio": aspect_ratio,
                        "shape_type": shape_type,
                        "command": command
                    }
                    
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                    cv2.circle(frame, (cX, cY), 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"Aspect Ratio: {aspect_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(frame, f"Shape: {shape_type}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return results

    def get_direction_command(self, x, y, frame_width, frame_height):
        grid_width = frame_width // 3
        grid_height = frame_height // 3
        
        x_pos = "Left" if x < grid_width else "Center" if x < 2 * grid_width else "Right"
        y_pos = "Top" if y < grid_height else "Middle" if y < 2 * grid_height else "Bottom"
        
        return f"{y_pos} {x_pos}"

    def save_selected_color(self):
        with open('selected_color.json', 'w') as file:
            json.dump(self.selected_color, file)

    def load_selected_color(self):
        if os.path.exists('selected_color.json'):
            with open('selected_color.json', 'r') as file:
                self.selected_color = json.load(file)

    def draw_color_example(self, frame):
        example_size = 100  # Boyutları yarıya indir
        example_img = np.zeros((example_size, example_size, 3), dtype=np.uint8)
        
        lower_h = self.selected_color['lower_h']
        lower_s = self.selected_color['lower_s']
        lower_v = self.selected_color['lower_v']
        upper_h = self.selected_color['upper_h']
        upper_s = self.selected_color['upper_s']
        upper_v = self.selected_color['upper_v']
        
        avg_h = (lower_h + upper_h) / 2
        avg_s = (lower_s + upper_s) / 2
        avg_v = (lower_v + upper_v) / 2
        avg_hsv = np.array([avg_h, avg_s, avg_v], dtype=np.uint8)
        avg_bgr = cv2.cvtColor(np.reshape(avg_hsv, (1, 1, 3)), cv2.COLOR_HSV2BGR)[0, 0]
        
        example_img[:, :] = avg_bgr
        
        x_offset = frame.shape[1] - example_size
        y_offset = 0
        frame[y_offset:y_offset+example_size, x_offset:x_offset+example_size] = example_img

    def run(self):
        ret, self.frame = self.cap.read()
        if not ret:
            print("Kare alınamıyor!")
            return {}
        
        # Ekranı 6/4 oranında büyütmek için boyutları yeniden ayarla
        self.frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))
        
        contours = self.detect_colors(self.frame)
        results = self.analyze_contours(self.frame, contours)
        
        self.draw_color_example(self.frame)
        
        cv2.imshow('Video Stream', self.frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            return results
        
        return results
    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
# Usage
if __name__ == "__main__":
    color_detection = ColorDetection()
    while True:
        results = color_detection.run()
        if results:
            for key, value in results.items():
                center = value['center']
                print(f"ID: {key} -> Center: {center}")
        else:
            print("No results found.")
