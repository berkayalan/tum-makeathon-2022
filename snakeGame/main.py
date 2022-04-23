import math
import random
import cvzone
import cv2
import numpy as np
import pygame
from cvzone.HandTrackingModule import HandDetector
import speech_recognition as sr
from pygame import mixer
import pygame as pg
from network import Network

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=2)


class SnakeGameClass:
    def __init__(self, pathFood, obsPath):
        #self.net = Network()
        self.points = []  # all points of the snake
        self.lengths = []  # distance between each point
        self.currentLength = 0  # total length of the snake
        self.allowedLength = 150  # total allowed Length
        self.previousHead = 0, 0  # previous head point

        # Food
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.random_food_location()

        # obstacle
        self.imgObs = cv2.imread(obsPath, cv2.IMREAD_UNCHANGED)
        self.hObs, self.wObs, _ = self.imgObs.shape
        self.obsPoint = 0, 0
        self.random_obstacle_location()

        # scores
        self.score = 0
        self.obsScore = 0
        self.gameOver = False

        pg.init()
        pg.time.set_timer(pg.USEREVENT + 1, 5000)
        # for event in pygame.event.get():
        #     if event.type == USEREVENT + 1:
        #         functionName()
        #     if event.type == QUIT:
        #         pygame.quite()
        #         sys.exit()

    def random_food_location(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def random_obstacle_location(self):
        self.obsPoint = random.randint(100, 1000), random.randint(100, 600)

    def punch(self, imgMain, leftIndex):

        # # # Draw Obstacle
        # ox, oy = self.obsPoint
        # imgMain = cvzone.overlayPNG(imgMain, self.imgObs, (ox - self.wObs // 2, oy - self.hObs // 2))
        # Check if obstacle is caught
        cx, cy = leftIndex
        rx, ry = self.obsPoint
        # catch obstacles
        if rx - self.wObs // 2 < cx < rx + self.wObs // 2 and ry - self.hObs // 2 < cy < ry + self.hObs // 2:
            self.random_obstacle_location()
            self.obsScore += 1
            print(self.obsScore)

        if self.gameOver:
            self.obsScore = 0


        return imgMain


    def update(self, imgMain, currentHead):
        events = pygame.event.get()
        for event in events:
            if event.type == pg.USEREVENT + 1:
                self.random_obstacle_location()

        nl = '\n'
        scores = [self.score, self.obsScore]

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [250, 300],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f"Your Score:{self.score}", [250, 450],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f"Obstacles caught:{self.obsScore}", [100, 550],
                               scale=7, thickness=5, offset=20,colorT=(255, 0, 0))

        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            # Length Reduction
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Check if snake ate the Food
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                mixer.music.load("./data/Pop-sound.mp3")

                # Setting the volume
                mixer.music.set_volume(0.7)

                # Start playing the song
                mixer.music.play()
                self.random_food_location()

                self.allowedLength += 50
                self.score += 1
                print(self.score)

            # Draw Snake
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, tuple(self.points[i - 1]), tuple(self.points[i]), (0, 0, 255), 20)
                cv2.circle(imgMain, tuple(self.points[-1]), 20, (0, 255, 0), cv2.FILLED)

            # Draw Food
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

            # Draw food score
            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],
                               scale=3, thickness=3, offset=10)

            # Draw obstacle score
            cvzone.putTextRect(imgMain, f'ObstacleScore: {self.obsScore}', [800, 80], colorR=(255, 0, 0), scale=3,
                               thickness=3, offset=10)

            # Draw Obstacle
            ox, oy = self.obsPoint
            imgMain = cvzone.overlayPNG(imgMain, self.imgObs, (ox - self.wObs // 2, oy - self.hObs // 2))

            # Check for Collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            print(minDist)

            if -0.5 <= minDist <= 0.5:
                print("Hit")
                self.gameOver = True
                self.points = []  # all points of the snake
                self.lengths = []  # distance between each point
                self.currentLength = 0  # total length of the snake
                self.allowedLength = 150  # total allowed Length
                self.previousHead = 0, 0  # previous head point
                self.random_food_location()

            # game over if we hit obstacle

            if ox - self.wObs // 2 < cx < ox + self.wObs // 2 and oy - self.hObs // 2 < cy < oy + self.hObs // 2:
                print("we are in the if")
                self.obsScore = 0
                # self.random_obstacle_location()
                self.gameOver = True

        return imgMain

    # def send_data(self):
    #     """
    #     Send position to server
    #     :return: None
    #     """
    #     data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
    #     reply = self.net.send(data)
    #     return reply


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


game = SnakeGameClass("./data/coffee.png", "./data/Donut.png") # arg1 = food image, arg2 = obstacle image

if __name__ == "__main__":


    # Voice recognition
    # Starting the mixer
    mixer.init()

    # Loading the song
    mixer.music.load("./data/Tada-sound.mp3")

    # Setting the volume
    mixer.music.set_volume(0.7)

    # Start playing the song
    mixer.music.play()

    # set the list of words, max number of guesses, and prompt limit
    WORDS = ["art", "start", "begin", "play"]
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        # create recognizer and mic instances
        guess = recognize_speech_from_mic(recognizer, microphone)
        guess_is_correct = False
        print(guess)

        # keep checking till words in WORDS
        if guess["transcription"]:
            if guess["transcription"].lower() in WORDS:
                guess_is_correct = True
                break

    NUM_GUESSES = 3
    PROMPT_LIMIT = 5


    if guess_is_correct:
        guess_is_correct = False
        run = True
        while run:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)

            for hand in hands:
                if hand['type'] == 'Left':
                    lmList = hand['lmList']
                    leftIndex = lmList[8][0:2]
                    img = game.punch(img,hand['center'])
                    print (" yes left")
                if hand['type'] == 'Right':
                    lmList = hand['lmList']
                    pointIndex = lmList[8][0:2]
                    img = game.update(img, pointIndex)



            # if hands:
            #     lmList = hands[0]['lmList']
            #     pointIndex = lmList[8][0:2]
            #     img = game.update(img, pointIndex)


            cv2.imshow("Image", img)
            key = cv2.waitKey(1)

            # guess = recognize_speech_from_mic(recognizer, microphone)
            #
            # if guess["transcription"]:
            #     guess_is_correct = guess["transcription"].lower() == "stop"
            # if guess_is_correct:
            #     run = False

            if key == ord('r'):
                game.gameOver = False
