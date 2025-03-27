import speech_recognition as sr
import serial
import time



# Kết nối với Arduino (kiểm tra cổng COM của bạn)
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # Chờ Arduino khởi động

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Nói 'bật đèn' hoặc 'tắt đèn':")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio, language='vi-VN')
        print("Bạn nói: " + command)
        return command.lower()
    except sr.UnknownValueError:
        print("Không nhận diện được giọng nói.")
        return ""
    except sr.RequestError:
        print("Lỗi kết nối API nhận diện giọng nói.")
        return ""

def main():
    while True:
        command = recognize_speech()
        if "bật đèn" in command:
            ser.write(b'1')  # Gửi tín hiệu bật đèn đến Arduino
            print("Gửi lệnh bật đèn.")
        elif "tắt đèn" in command:
            ser.write(b'0')  # Gửi tín hiệu tắt đèn đến Arduino
            print("Gửi lệnh tắt đèn.")
        elif "thoát" in command:
            print("Dừng chương trình.")
            break

if __name__ == "__main__":
    main()
