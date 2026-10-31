import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
import time
import pygame

from mediapipe.tasks.python import vision as mp_vision
sounds_mapping = {
    1: "sounds_swaras/1_Sa.mp3",
    2: "sounds_swaras/2_Re.mp3",
    3: "sounds_swaras/3_Ga.mp3",
    4: "sounds_swaras/4_Ma.mp3",
    5: "sounds_swaras/5_Pa.mp3",
    6: "sounds_swaras/6_Dha.mp3",
    7: "sounds_swaras/7_Ni.mp3",
    8: "sounds_swaras/8_Sa_upper.mp3"

}
def draw_landmarks(frame, hand_landmarks):
    h, w, _ = frame.shape
    HAND_CONNECTIONS = [(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(5,9),(9,10),(10,11),(11,12),(9,13),(13,14),(14,15),(15,16),(13,17),(17,18),(18,19),(19,20),(0,17)]
    # Convert each landmark to pixel coordinates
    points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
    # Draw lines between connected landmarks (green)
    for start_idx, end_idx in HAND_CONNECTIONS:
        cv2.line(frame, points[start_idx], points[end_idx], (0,255,0), 2)
    # Draw a dot at each landmark (red, filled)
    for x, y in points:
        cv2.circle(frame, (x, y), 4, (0,0,255), -1)

def count(result, frame):
    count = 0
    for i , hand_landmarks in enumerate(result.hand_landmarks):
        label = result.handedness[i][0].category_name
        # print(label, hand_landmarks[4].x, hand_landmarks[1].x)
        if label == 'Left':
            if hand_landmarks[4].x < hand_landmarks[1].x:
                count+=1
        elif label == 'Right':
            if hand_landmarks[4].x > hand_landmarks[1].x:
                count+=1
        
        if hand_landmarks[8].y < hand_landmarks[6].y:
            count+=1
        if hand_landmarks[12].y < hand_landmarks[10].y:
            count+=1
        if hand_landmarks[16].y < hand_landmarks[14].y:
            count+=1
        if hand_landmarks[20].y < hand_landmarks[18].y:
            count+=1
    cv2.putText(frame, f"Count is {count}",(20,50), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,0), 2,cv2.LINE_AA)
    return count
    


# MAIN CODE
MODEL_PATH = "hand_landmarker.task"
base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
options = mp_vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=mp_vision.RunningMode.VIDEO,
    num_hands=2,                      # two hands -> counts up to 10
)
landmarker = mp_vision.HandLandmarker.create_from_options(options)
cap = cv2.VideoCapture(0)
start_time = time.time()
previouscounts = 0
counts = 0
lastplay = -2
pygame.mixer.init()
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    timestamp_ms = int((time.time() - start_time) * 1000)

    
    result = landmarker.detect_for_video(mp_image, timestamp_ms)
    
    for hand_landmarks in result.hand_landmarks:
        draw_landmarks(frame, hand_landmarks)
        counts = count(result, frame)
    curtime = time.time()
    if counts in sounds_mapping:
        if counts != previouscounts:
            if curtime >= 1.5 + lastplay:
                pygame.mixer.music.load(sounds_mapping[counts])
                pygame.mixer.music.play()
                lastplay = curtime
    if curtime - lastplay >= 1:
        pygame.mixer.music.stop()
    previouscounts = counts
    cv2.imshow("Live feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
landmarker.close()
pygame.mixer.quit()
cap.release()
cv2.destroyAllWindows()