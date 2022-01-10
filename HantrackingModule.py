import cv2
import mediapipe as mp
import time


class handDetector():

    def __init__(self, mode=False, MaxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.MaxHands = MaxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(False)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, drwa = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handmarks in self.results.multi_hand_landmarks:
                if drwa:
                    self.mpDraw.draw_landmarks(img, handmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo, draw=True):

        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand= self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                    # print(id , lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # The values present in lm are the ratio so multiply them with w and h
                    # print(id, cx, cy)
                    lmlist.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 10, (142, 0, 145), cv2.FILLED)
        return lmlist

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        lmlist = detector.findPosition(img, 0)
        if len(lmlist) !=0:
            print(lmlist[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__== "__main__":
    main()
