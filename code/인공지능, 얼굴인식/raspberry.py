import cv2

# 얼국 인식용 xml 파일
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# 전체 사진에서 얼굴 부위만 잘라 리턴
def face_extraction(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return None
    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]
    return cropped_face


# 카메라 실행
cap = cv2.VideoCapture(0)
# 저장할 이미지 카운트 변수
count = 0

name = input("저장할 data의 이름을 입력하세요 :")

while True:
    ret, frame = cap.read()
    if face_extraction(frame) is not None:
        count = count + 1
        face = cv2.resize(face_extraction(frame), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        path = 'faces2/' + name + str(count) + '.jpg'
        cv2.imwrite(path, face)
        cv2.putText(face, str(count), (50, 50), 0, 1, (0, 255, 0), 2)
        cv2.imshow('data 저장중', face)
    else:
        pass
    if cv2.waitKey(1) == 13 or count == 100:
        break

cap.release()
cv2.destroyAllWindows()
print('데이터 저장이 완료되었습니다.')