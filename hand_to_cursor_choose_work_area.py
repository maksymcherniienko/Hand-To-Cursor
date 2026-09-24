'''
Код для використання руки замість курсора миші та для клікання/перетягування 
камера розміщується над робочою поверхнею і визначає її область
після чого на цій області буде розпізнаватись рука і виконуватимуться дії прив'язані до відповідних жестів користувача
'''
import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import math

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = 0, 0
smoothening = 2

is_dragging = False
is_clicked = False

ret, frame = cap.read()
frame = cv2.flip(frame, 1)

print("Виділи робочу зону мишкою і натисни ENTER (або SPACE)")
x_area, y_area, w_area, h_area = cv2.selectROI(
    "Select work area (Press SPACE or ENTER after choosing)", frame, showCrosshair=True, fromCenter=False
)
cv2.destroyWindow("Select work area (Press SPACE or ENTER after choosing)")

if w_area == 0 or h_area == 0:
    print("Зону не обрано, завершення програми.")
    cap.release()
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    cv2.rectangle(frame, (x_area, y_area), (x_area + w_area, y_area + h_area), (0, 0, 255), 2)
    cv2.putText(frame, "Work area", (x_area, y_area - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    h, w, _ = frame.shape

    cropped_frame = frame[y_area:y_area+h_area, x_area:x_area+w_area]
    rgb_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(cropped_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        middle_finger_mcp = hand_landmarks.landmark[9]
        index_finger_tip = hand_landmarks.landmark[8]
        thumb = hand_landmarks.landmark[4]
        ring_finger_tip = hand_landmarks.landmark[16]
        ring_finger_mcp = hand_landmarks.landmark[14]

        index_finger_x, index_finger_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
        thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
        ring_finger_x,ring_finger_y = int(ring_finger_tip.x * w), int(ring_finger_tip.y * h)
        ring_finger_mcp_x,ring_finger_mcp_y = int(ring_finger_mcp.x * w), int(ring_finger_mcp.y * h)

        # --- рух курсора ---
        margin = 0.24  # вважаємо "мертвою зоною"
        screen_x = np.interp(middle_finger_mcp.x, (margin, 1 - margin), (0, screen_w)) #слідкує за відповідною точкою
        screen_y = np.interp(middle_finger_mcp.y, (margin, 1 - margin), (0, screen_h))

        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening

        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y
        # --- перевірка щипка (для drag) ---
        distance_drag = math.hypot(thumb_x - index_finger_x, thumb_y - index_finger_y)
        distance_click = math.hypot(ring_finger_x - ring_finger_mcp_x, ring_finger_y - ring_finger_mcp_y)

        if (distance_click < h_area*0.06):
            if not is_clicked:
                pyautogui.click()
                is_clicked = True
            cv2.putText(frame, "CLICK!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        else: is_clicked = False

        if distance_drag < w_area*0.08:
            if not is_dragging:
                pyautogui.mouseDown()
                is_dragging = True
            cv2.putText(frame, "DRAGGING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            if is_dragging:
                pyautogui.mouseUp()
                is_dragging = False

    else:
        # якщо рука зникла з кадру - про всяк випадок відпускаємо кнопку
        if is_dragging:
            pyautogui.mouseUp()
            is_dragging = False

    cv2.imshow("Hand Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
if is_dragging:
    pyautogui.mouseUp()
cap.release()
cv2.destroyAllWindows()