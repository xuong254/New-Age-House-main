import cv2
import numpy as np
import speech_recognition as sr
import serial
import time

# Kết nối với Arduino (kiểm tra cổng COM của bạn)
try:
    ser = serial.Serial('COM4', 9600, timeout=1)
    time.sleep(2)  # Chờ Arduino khởi động
    print("Kết nối Arduino thành công trên COM4")
except serial.SerialException as e:
    print("Không thể kết nối với Arduino trên COM4:", e)
    ser = None

# Tải mô hình nhận diện khuôn mặt đã được huấn luyện
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trained_model.yml")

# Tải Haar Cascade để phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def face_recognition_check(conf_threshold=50):
    cap = cv2.VideoCapture(0)
    recognized = False
    recognized_id = None
    print("Đang kiểm tra khuôn mặt, vui lòng đối diện với camera...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không thể truy cập camera.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            id_pred, confidence = recognizer.predict(face_roi)
            if confidence < conf_threshold:
                recognized = True
                recognized_id = id_pred
                cv2.putText(frame, f"ID: {id_pred} ({round(confidence,2)})", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            else:
                cv2.putText(frame, f"Unk ({round(confidence,2)})", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)

        cv2.imshow("Face Recognition", frame)

        if recognized:
            print(f"Khuôn mặt được nhận diện với ID: {recognized_id}")
            time.sleep(2)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return recognized

def recognize_speech():
    recognizer_speech = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bạn cần gì?")
        recognizer_speech.adjust_for_ambient_noise(source)
        audio = recognizer_speech.listen(source)

    try:
        command = recognizer_speech.recognize_google(audio, language='vi-VN')
        print("Bạn nói: " + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Không nhận diện được giọng nói.")
        return ""
    except sr.RequestError as e:
        print("Lỗi kết nối API nhận diện giọng nói:", e)
        return ""

def main():
    # Bước 1: Nhận diện và xác thực khuôn mặt qua camera laptop
    if not face_recognition_check():
        print("Không nhận diện được khuôn mặt. Thoát chương trình.")
        return

    # Bước 2: Sau khi khuôn mặt được nhận diện, chuyển sang nhận diện giọng nói
    while True:
        command = recognize_speech()
        if "bật đèn" in command:
            if ser:
                ser.write(b'1')
                print("Gửi lệnh bật đèn.")
                time.sleep(1)  # Chờ xử lý lệnh
                print("✅ Đã thực hiện xong!")
            else:
                print("Arduino chưa được kết nối.")
        elif "tắt đèn" in command:
            if ser:
                ser.write(b'0')
                print("Gửi lệnh tắt đèn.")
                time.sleep(1)  # Chờ xử lý lệnh
                print("✅ Đã thực hiện xong!")
            else:
                print("Arduino chưa được kết nối.")
        elif "thoát" in command:
            print("Dừng chương trình.")
            break

if __name__ == "__main__":
    main()
