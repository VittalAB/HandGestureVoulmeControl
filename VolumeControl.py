import cv2
import time
import HantrackingModule as htm
import math
import numpy as np
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# importing the library for controlling the volume called pycaw just pip install it

################################################
wCam, hCam = 640, 480
################################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()  # min=-65.25 max=0.0
# volume.SetMasterVolumeLevel(0.0, None)

minVol = volRange[0]
maxVol = volRange[1]
vol =0
volBar = 400
volPer = 0



while True:
    succes, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, 0, draw=False)

    if len(lmlist)!=0:
        # print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2

        cv2.circle(img, (x1, y1), 10, (255, 0 , 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
        cv2.line(img,(x1, y1),(x2, y2),(0,255,0), 3)

        cv2.circle(img, (cx,cy) ,10, (0,255,0), cv2.FILLED)
        length = math.hypot(x2-x1,y2-y1)
        # print(int(length))

        # HandRange from 50 to 175
        # VolumeRange from -65.25 to 0
        vol = np.interp(length, [29, 175], [minVol,maxVol])
        volPer = np.interp(length,[29, 175], [0, 100])
        volBar = np.interp(length, [29, 175], [400, 150])
        # print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
    cv2.rectangle(img, (50,150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'Volume {int(volPer)} %', (40,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cTime = time.time()
    fps  = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS :- {int(fps)}', (40,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 0, 0), 3)

    cv2.imshow("img", img)
    cv2.waitKey(1) # to give 1ms delay
