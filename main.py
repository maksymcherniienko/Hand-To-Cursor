import cv2, pyautogui
from src.hand_tracker import HandTracker
from src.mouse_control import MouseController
import src.config as config

def main():
    cap = cv2.VideoCapture(config.CAM_INDEX)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

    tracker = HandTracker()
    mouse = MouseController()

    ret, frame = cap.read()
    frame = cv2.flip(frame, config.CAM_FLIP)
    
    # Вибір зони
    x_area, y_area, w_area, h_area = cv2.selectROI("Select work area", frame, showCrosshair=True, fromCenter=False)
    cv2.destroyWindow("Select work area")
    
    if w_area == 0 or h_area == 0:
        cap.release()
        return

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, config.CAM_FLIP)

        # Малюємо зону
        cv2.rectangle(frame, (x_area, y_area), (x_area + w_area, y_area + h_area), (0, 0, 255), 2)

        cropped_frame = frame[y_area:y_area+h_area, x_area:x_area+w_area]
        rgb_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
        
        # 1. Отримуємо дані руки
        hand_data = tracker.process_frame(rgb_frame)

        if hand_data:
            # Малюємо скелет
            tracker.mp_draw.draw_landmarks(cropped_frame, hand_data['raw_landmarks'], tracker.mp_hands.HAND_CONNECTIONS)
            
            # Рухаємо мишку
            mouse.move_cursor(hand_data['pointer_x'], hand_data['pointer_y'])
            
            # Обробляємо кліки
            status = mouse.handle_gestures(hand_data['normalized_pinch'])
            
            # Вивід статусу на екран
            if status == "DRAGGING":
                cv2.putText(frame, "DRAGGING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif status in ["CLICK_STARTED", "RELEASED"]:
                cv2.putText(frame, "CLICK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Hand Mouse Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Безпечний вихід
    if mouse.is_dragging:
        pyautogui.mouseUp()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()