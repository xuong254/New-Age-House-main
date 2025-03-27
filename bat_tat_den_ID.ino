int ledPin = 13; // Chân điều khiển LED

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600); // Khởi động Serial
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read(); // Đọc lệnh từ máy tính
        if (command == '1') {
            digitalWrite(ledPin, HIGH); // Bật đèn
        } else if (command == '0') {
            digitalWrite(ledPin, LOW); // Tắt đèn
        }
    }
}
