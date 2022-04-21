from keras.models import load_model
import cv2 as cv
import mediapipe as mp
import numpy as np

model = load_model('./train/old/keras_model.h5')
min_confidence = 0.65

cap = cv.VideoCapture("A.mp4")
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence = 0.55)
mpDraw = mp.solutions.drawing_utils

labels = {0:"A", 1:"B", 2:"C", 3:"G", 4:"K", 5:"L", 6:"M", 7:"O", 8:"Y"}
while True:
    sign = None
    success, img = cap.read()
    RGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(RGB)
    h,w,c = img.shape
    img_1 = np.zeros([h,w,3],dtype=np.uint8)
    img_1.fill(255)
    
    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]           
        mpDraw.draw_landmarks(img_1, handLms, mpHands.HAND_CONNECTIONS)
        
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image_array = cv.resize(img_1,(224,224))
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array

        prediction = model.predict(data)
        
        if np.amax(prediction) > min_confidence:
            sign = labels[np.argmax(prediction)]
        else:
            sign = None 
        cv.putText(img, sign, (10,70), cv.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    
    cv.imshow("Image", img)
    cv.imshow("white", img_1)
    
    if cv.waitKey(1) == ord("q"):
        break
    
cap.release()
cv.destroyAllWindows()