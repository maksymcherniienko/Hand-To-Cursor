import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def calculate_distance(self, p1, p2):
        return math.hypot(p2.x - p1.x, p2.y - p1.y)

    def process_frame(self, rgb_frame):
        results = self.hands.process(rgb_frame)
        hand_data = {}

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            wrist = landmarks.landmark[0]
            middle_mcp = landmarks.landmark[9]
            thumb = landmarks.landmark[4]
            index_tip = landmarks.landmark[8]

            base_dist = self.calculate_distance(wrist, middle_mcp)
            pinch_dist = self.calculate_distance(thumb, index_tip)
            
            hand_data['normalized_pinch'] = pinch_dist / base_dist
            hand_data['pointer_x'] = middle_mcp.x
            hand_data['pointer_y'] = middle_mcp.y
            hand_data['raw_landmarks'] = landmarks # щоб намалювати сітку в main.py

        return hand_data