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
import time

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
pinch_start_time = None
hands = mp_hands.Hands(
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) #отримує тільки один свіжий кадр
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = 0, 0

is_dragging = False
is_clicked = False

ret, frame = cap.read()
#frame = cv2.flip(frame, 0)

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

    #frame = cv2.flip(frame, -1)

    cv2.rectangle(frame, (x_area, y_area), (x_area + w_area, y_area + h_area), (0, 0, 255), 2)
    cv2.putText(frame, "Work area", (x_area, y_area - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

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

        index_finger_x, index_finger_y = int(index_finger_tip.x * w_area), int(index_finger_tip.y * h_area)
        thumb_x, thumb_y = int(thumb.x * w_area), int(thumb.y * h_area)
        ring_finger_x,ring_finger_y = int(ring_finger_tip.x * w_area), int(ring_finger_tip.y * h_area)
        ring_finger_mcp_x,ring_finger_mcp_y = int(ring_finger_mcp.x * w_area), int(ring_finger_mcp.y * h_area)

        # --- рух курсора ---
        margin = 0.3  # вважаємо "мертвою зоною"
        screen_x = np.interp(middle_finger_mcp.x, (margin, 1 - margin), (0, screen_w)) #слідкує за відповідною точкою
        screen_y = np.interp(middle_finger_mcp.y, (margin, 1 - margin), (0, screen_h))


        if pinch_start_time is None or is_dragging:
        #динамічне адаптивне згладжування
            distanceMoved = math.hypot(screen_x - prev_x, screen_y - prev_y)
            smoothening = np.interp(distanceMoved, [10, 70], [15, 1.1]) # дистанцію від 5 до 40 пікселів перетворюєм у значення від 5 до 1.3 плавно
            if distanceMoved < 10:
                curr_x, curr_y = prev_x, prev_y
                #print("deadzone!")
            else:
                curr_x = prev_x + (screen_x - prev_x) / smoothening
                curr_y = prev_y + (screen_y - prev_y) / smoothening
                #print(f"smoothering is {smoothening} now")
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y
        else: pass
        # --- перевірка щипка (для drag) ---
        #distance_drag = math.hypot(thumb_x - index_finger_x, thumb_y - index_finger_y)
        distance_click = math.hypot(thumb_x - index_finger_x, thumb_y - index_finger_y)


        if distance_click < h_area*0.07:
            if pinch_start_time is None:
                pinch_start_time = time.time()
            
            elif (time.time() - pinch_start_time) > 0.3:
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
            if is_dragging:
                cv2.putText(frame, "DRAGGING", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "CLICK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        else:
            if pinch_start_time is not None:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                else:
                    pyautogui.click()
                pinch_start_time = None

    cv2.imshow("Hand Mouse Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
if is_dragging:
    pyautogui.mouseUp()
cap.release()
cv2.destroyAllWindows()