import torch
import cv2

# YOLOv5 modelini yükleme (model_path.pt yerine kendi model yolunu gir)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='model_path.pt') 

# Kamerayı başlat
cap = cv2.VideoCapture(0)  # 0 default kamerayı seçer, birden fazla kamera varsa 1, 2... diye numaralandırabilirsin

while True:
    ret, frame = cap.read()  # Kameradan görüntü al
    if not ret:
        break

    # Tahmin yap
    results = model(frame)
    
    # Tahmin edilen sonuçlardan her birinin koordinatlarını ve etiketini al
    for detection in results.xyxy[0]:  # xyxy: [x_min, y_min, x_max, y_max, confidence, class]
        x_min, y_min, x_max, y_max, confidence, class_id = detection
        
        # Koordinatları ekrana yazdır
        print(f'Koordinatlar: x_min={int(x_min)}, y_min={int(y_min)}, x_max={int(x_max)}, y_max={int(y_max)}')
        print(f'Güven: {confidence}, Sınıf ID: {class_id}')
        
        # Çizim yap: dikdörtgenin köşelerini belirt ve kutuyu çiz
        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

    # Çizilmiş görüntüyü göster
    cv2.imshow('YOLOv5', frame)

    # Çıkmak için 'q' tuşuna bas
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamerayı serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
