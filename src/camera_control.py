import cv2

def get_available_cameras(max_to_test=7):
    available_cameras = []
    
    for index in range(max_to_test):
        # cv2.CAP_DSHOW значно прискорює ініціалізацію та пропуск неіснуючих камер на Windows
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available_cameras.append(str(index))
            cap.release()

    return available_cameras