import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
data_path = 'faces2/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]#listdir 모든 파일과 폴더를 리스트 형태로 반환
Training_Data, Labels = [], []
for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(0)

if len(Labels) == 0:
    print("There is no data to train.")
    exit()
Labels = np.asarray(Labels, dtype=np.int32)
model = cv2.face.LBPHFaceRecognizer_create()
model.train(np.asarray(Training_Data), np.asarray(Labels))
print("모델 학습 완료")

#### 여긴 Part1.py와 거의 동일
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def face_detector(img, size = 0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)#이미지가 얼마나 줄얻ㅡ는지 지정하는 매개변수, 직사각형을 유지해야하는 이웃 수 매개변수
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))
    return img,roi   #검출된 좌표에 사각 박스 그리고(img), 검출된 부위를 잘라(roi) 전달
#### 여기까지 Part1.py와 거의 동일
#카메라 열기
cap = cv2.VideoCapture(0)
count_a = 0
count_b = 0
while True:
    #카메라로 부터 사진 한장 읽기
    ret, frame = cap.read()
    # 얼굴 검출 시도
    image, face = face_detector(frame)
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        result = model.predict(face)
        if result[1] < 50:
            count_a = count_a + 1
        if result[1] > 50:
            count_b = count_b + 1
        if count_a+count_b == 10:
            break
        print(count_a+count_b)
    except:
        #얼굴 검출 안됨
        cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Face Cropper', image)
        pass
    if cv2.waitKey(1)==13:
        break
result = count_a/(count_a+count_b)*100
if result > 70 :
    print("return : 0 User")
if result < 70 :
    print("return : 1 Stranger")
cap.release()
cv2.destroyAllWinzdows()