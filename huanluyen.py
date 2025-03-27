import cv2
import os
import numpy as np

# Đường dẫn đến thư mục dataset
dataset_path = r"C:\iot\AI&IOT\dataset_path"

def get_images_and_labels(dataset_path):
    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(dataset_path):
        print(f"LỖI: Thư mục '{dataset_path}' không tồn tại!")
        return [], []
    
    # Lấy danh sách ảnh (hỗ trợ cả .jpg và .png)
    image_paths = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path)
                   if f.endswith('.jpg') or f.endswith('.png')]

    face_samples = []
    ids = []

    for image_path in image_paths:
        # Đọc ảnh theo grayscale
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Lỗi khi đọc ảnh: {image_path}")
            continue
        
        try:
            # Lấy ID từ tên file (giả sử định dạng "ID_Tên.jpg")
            id = int(os.path.split(image_path)[-1].split('_')[0])
            face_samples.append(image)
            ids.append(id)
        except ValueError:
            print(f"Lỗi khi trích xuất ID từ file: {image_path}")

    return face_samples, ids

if __name__ == "__main__":
    faces, ids = get_images_and_labels(dataset_path)
    
    if len(faces) == 0:
        print("Không có ảnh nào được huấn luyện. Thoát chương trình.")
        exit()

    print(f"Số lượng ảnh được huấn luyện: {len(faces)}")
    print(f"IDs: {set(ids)}")  # Hiển thị các ID duy nhất

    # Kiểm tra xem OpenCV có hỗ trợ module "face" không
    if not hasattr(cv2.face, "LBPHFaceRecognizer_create"):
        print("LỖI: OpenCV của bạn không hỗ trợ LBPHFaceRecognizer.")
        print("Hãy cài đặt lại bằng lệnh: pip install opencv-contrib-python")
        exit()

    # Khởi tạo LBPH Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Huấn luyện mô hình
    recognizer.train(faces, np.array(ids))

    # Lưu mô hình đã huấn luyện
    model_path = "trained_model.yml"
    recognizer.write(model_path)
    print(f"Huấn luyện xong và lưu model vào '{model_path}'")
