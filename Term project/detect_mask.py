import cv2
import cvlib as cv
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import ImageFont, ImageDraw, Image
from tkinter import messagebox
import pygame
from send_message import *
import time
import pyautogui as pg


# 모델을 로드, 경고음악 및 퇴출 음악 로드, 좌석번호 입력 및 경고창 생성
model = load_model('C:/Users/TFG242/python/project/best_model.h5')
pygame.init()
pygame.mixer.init()
warning_sound = pygame.mixer.Sound('C:/Users/TFG242/python/project/warning_sound.mp3')
exit_sound = pygame.mixer.Sound('C:/Users/TFG242/python/project/exit_sound.mp3')
seat_number = pg.prompt(text='안녕하세요 마스크 탐지기 입니다. 당신의 좌석번호를 입력해주세요. ', title='안녕하세요 마스크 탐지기 입니다.', default='당신의 좌석번호를 입력하세요.')
message = send_message(seat_number)
messagebox.showinfo(title="Mask detection Management", message='''이 프로그램은 마스크를 벗는 즉시 알림이 울립니다.
또한 3번 이상 미착용시 관리자에게 알림이 가게 되고 당신은 퇴출됩니다. 확인 하셨으면 확인 버튼을 눌러주세요.''')

#웹캠 오픈
webcam = cv2.VideoCapture(0)
warning = 0

if not webcam.isOpened():
    print("웹캠을 열수 없습니다.")
    exit()
    
#웹캠이 켜져 있을 동안 loop
while webcam.isOpened():

    #웹캠으로부터 프레임 읽음
    status, frame = webcam.read()
    
    if not status:
        print("프레임을 읽을 수 없습니다.")
        exit()

    #cv lib를 활용하여 얼굴 탐지
    face, confidence = cv.detect_face(frame)

    #얼굴을 탐지할 동안 loop
    for idx, f in enumerate(face):
        
        (startX, startY) = f[0], f[1]
        (endX, endY) = f[2], f[3]
        
        if 0 <= startX <= frame.shape[1] and 0 <= endX <= frame.shape[1] and 0 <= startY <= frame.shape[0] and 0 <= endY <= frame.shape[0]:
            
            face_region = frame[startY:endY, startX:endX]
            
            face_region1 = cv2.resize(face_region, (224, 224), interpolation = cv2.INTER_AREA)
            
            x = img_to_array(face_region1)
            x = np.expand_dims(face_region1, axis=0)
            x = preprocess_input(x)
            x = np.array(x)
            
            #학습한 모델로 predict
            prediction = model.predict(x)
            mask=prediction[0][0]
            nomask=prediction[0][1]
            
            # nomask로 판별 될 시! 1,2차 경고 및 3차 퇴출, 후 프로그램 종료, 관리자에게 메시지 전송
            if mask < nomask:
                warning += 1
                if warning == 3 : 
                    exit_sound.play(loops=1)
                    message.requests()
                    messagebox.showinfo(title="마스크 미착용 퇴출!", message=f"당신은 방역수칙 위반으로 퇴출입니다. 관리자를 호출중입니다.")
                    time.sleep(8)
                    exit()
                warning_sound.play(-1)
                messagebox.showinfo(title="마스크 착용 경고!", message=f"마스크를 착용 후 확인 버튼을 눌러주세요\n {warning}차 경고입니다. 3차 경고시 관리자를 호출해 퇴출하도록 하겠습니다.")
                cv2.rectangle(frame, (startX,startY), (endX,endY), (0,0,255), 2)
                Y = startY - 10 if startY - 10 > 10 else startY + 10
                text = "No Mask ({:.2f}%)".format((1 - prediction[0][0])*100)
                cv2.putText(frame, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

            # mask로 판별 될 시! 경고 음성을 멈춤.
            else: 
                warning_sound.stop()
                cv2.rectangle(frame, (startX,startY), (endX,endY), (0,255,0), 2)
                Y = startY - 10 if startY - 10 > 10 else startY + 10
                text = "Mask ({:.2f}%)".format(prediction[0][0]*100)
                cv2.putText(frame, text, (startX,Y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                
    # 타이틀
    cv2.imshow("mask nomask classify", frame)

    # 'q'키를 클릭 시 프로그램 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# 리소스 반환
webcam.release()
cv2.destroyAllWindows() 
